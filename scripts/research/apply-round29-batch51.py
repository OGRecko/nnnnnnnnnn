#!/usr/bin/env python3
"""Apply Round 29 batch 51 (2026-10-19): Klipsch owner's manuals -> active: false, manufacturer tier.

Idempotent: a promotion already recorded from the same source is skipped, and the URL status file keeps a
snapshot of the previous non-OPEN entry instead of overwriting it.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
LEDGER = os.path.join(HERE, 'provenance-source-ledger.json')


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
    ev = load('round29_batch51_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action'), h.get('source')) for h in history['entries']}

    promoted = skipped = 0
    for p in ev.PROMOTIONS:
        rec = by_id[p['record']]
        prov_key = p['field'] + 'Provenance'
        prov = rec.get(prov_key) or {}
        assert rec[p['field']] == p['value'], (p['record'], rec[p['field']])
        if prov.get('status') == 'MANUFACTURER_VERIFIED' and prov.get('source') == p['source']:
            skipped += 1
            continue
        assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', (p['record'], prov.get('status'))
        new_prov = {'status': 'MANUFACTURER_VERIFIED', 'source': p['source'],
                    'sourceType': 'MANUFACTURER', 'note': p['note']}
        before = {'value': rec[p['field']], 'provenance': dict(prov)}
        rec[prov_key] = new_prov
        if (p['record'], p['field'], 'PROMOTE', p['source']) not in seen:
            history['entries'].append({
                'id': p['record'], 'field': p['field'], 'value': p['value'],
                'before': before, 'after': {'value': p['value'], 'provenance': new_prov},
                'round': ev.ROUND, 'action': 'PROMOTE', 'source': p['source'],
            })
            seen.add((p['record'], p['field'], 'PROMOTE', p['source']))
        if p['notesAppend'].strip() and p['notesAppend'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['notesAppend']).strip()
        promoted += 1
    history['marker'] = 'round29-batch51-klipsch-manuals'

    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    for entry in ev.URL_RESULTS:
        url = entry['url']
        old = by_url.get(url)
        if old is None:
            old = {'url': url, 'status': 'OPEN', 'fieldResults': []}
            status['urls'].append(old)
        snapshots = list(old.get('history', []))
        if old.get('status') not in (None, 'OPEN') and old.get('round') != ev.ROUND:
            snapshots.append({'snapshotOfRound': old.get('round'),
                              'entry': {k: v for k, v in old.items() if k != 'history'}})
        merged = {f"{f['record']}.{f['field']}": f for f in old.get('fieldResults', [])}
        for f in entry['fieldResults']:
            merged[f"{f['record']}.{f['field']}"] = f
        by_url[url] = {
            'url': url, 'round': ev.ROUND, 'status': entry['status'],
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'checkedDate': ev.DATE, 'sourceClass': 'MANUFACTURER',
            'document': entry['document'], 'evidence': entry['evidence'],
            'fieldResults': list(merged.values()), 'history': snapshots,
        }
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    have = {s.get('url') for s in ledger['sources']}
    added = 0
    for entry in ev.URL_RESULTS:
        if entry['url'] in have:
            continue
        ledger['sources'].append({
            'url': entry['url'], 'host': ev.HOSTS[entry['url']], 'document': entry['document'],
            'status': entry['status'], 'openedDate': ev.DATE,
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'coverage': entry['evidence'],
            'decisions': [
                {'id': f['record'], 'field': f['field'], 'value': f['value'],
                 'result': 'CONFIRMED', 'decision': 'MANUFACTURER_VERIFIED', 'evidence': f['note']}
                for f in entry['fieldResults']
            ],
            'queueItemsResolved': len(entry['fieldResults']),
        })
        added += 1

    dump(DATA, db)
    dump(HISTORY, history)
    dump(STATUS, status)
    dump(LEDGER, ledger)
    print(f'round29 batch51: promotions={promoted} already_promoted={skipped} '
          f'url_results={len(ev.URL_RESULTS)} ledger_sources_added={added}')


if __name__ == '__main__':
    main()
