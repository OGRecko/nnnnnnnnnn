#!/usr/bin/env python3
"""Apply Round 29 batch 32: re-read locate.gov 4310 manual; refresh queue rows + ledger."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
STATUS = os.path.join(HERE, 'queue-url-status.json')
LEDGER = os.path.join(HERE, 'round29-unsourced-ledger.json')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def main():
    ev = load('round29_batch32_data')
    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    entry = by_url[ev.URL]
    snapshots = list(entry.get('history', []))
    snapshots.append({'snapshotOfRound': entry.get('round'),
                      'entry': {k: v for k, v in entry.items() if k != 'history'}})
    merged = {f"{f['record']}.{f['field']}": f for f in entry.get('fieldResults', [])}
    for f in ev.FIELD_RESULTS:
        merged[f"{f['record']}.{f['field']}"] = f
    by_url[ev.URL] = {
        'url': ev.URL, 'round': ev.ROUND, 'status': 'CHECKED_CONFIRMED',
        'chunksOpened': [0], 'chunksTotal': 2, 'checkedDate': ev.DATE,
        'evidence': ev.EVIDENCE, 'fieldResults': list(merged.values()), 'history': snapshots,
    }
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    for row in ev.LEDGER_ROWS:
        if not any(r.get('record') == row['record'] and r.get('field') == row['field']
                   for r in ledger['assessments']):
            ledger['assessments'].append(row)

    dump(STATUS, status)
    dump(LEDGER, ledger)
    print(f'round29 batch32: queue_rows={len(merged)} snapshots={len(snapshots)}')


if __name__ == '__main__':
    main()
