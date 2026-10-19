#!/usr/bin/env python3
"""Apply Round 29 batch 33: JBL 4430 active promotion; KEF archive retry outcomes."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
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
    ev = load('round29_batch33_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}

    p = ev.PROMOTION
    rec = by_id[p['record']]
    key = p['field'] + 'Provenance'
    prov = rec.get(key) or {}
    assert rec[p['field']] is False, rec[p['field']]
    if not (prov.get('status') == 'MANUFACTURER_VERIFIED' and prov.get('source') == p['source']):
        assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', prov.get('status')
        new_prov = {'status': 'MANUFACTURER_VERIFIED', 'source': p['source'],
                    'sourceType': 'MANUFACTURER', 'note': p['note']}
        before = {'value': rec[p['field']], 'provenance': dict(prov)}
        rec[key] = new_prov
        if (p['record'], p['field'], 'PROMOTE') not in seen:
            history['entries'].append({
                'id': p['record'], 'field': p['field'], 'value': p['value'], 'before': before,
                'after': {'value': p['value'], 'provenance': new_prov},
                'round': ev.ROUND, 'action': 'PROMOTE', 'source': p['source'],
            })
            seen.add((p['record'], p['field'], 'PROMOTE'))
        if p['notesAppend'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['notesAppend']).strip()

    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    for entry in ev.URL_RESULTS:
        url = entry['url']
        old = by_url.get(url) or {'url': url, 'fieldResults': [], 'history': []}
        snapshots = list(old.get('history', []))
        if old.get('status') not in (None, 'OPEN') and old.get('round') != ev.ROUND:
            snapshots.append({'snapshotOfRound': old.get('round'),
                              'entry': {k: v for k, v in old.items() if k != 'history'}})
        merged = {f"{f['record']}.{f['field']}": f for f in old.get('fieldResults', [])}
        for f in entry['fieldResults']:
            merged[f"{f['record']}.{f['field']}"] = f
        by_url[url] = {'url': url, 'round': ev.ROUND, 'status': entry['status'],
                       'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
                       'checkedDate': ev.DATE, 'evidence': entry['evidence'],
                       'fieldResults': list(merged.values()), 'history': snapshots}
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    ledger.setdefault('promotions', []).append(
        {'record': p['record'], 'field': p['field'], 'value': p['value'],
         'status': 'MANUFACTURER_VERIFIED', 'source': p['source']})

    dump(DATA, db)
    dump(STATUS, status)
    dump(HISTORY, history)
    dump(LEDGER, ledger)
    print('round29 batch33: promotion=1 url_results=%d' % len(ev.URL_RESULTS))


if __name__ == '__main__':
    main()
