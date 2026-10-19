#!/usr/bin/env python3
"""Apply a third-party batch: promote explicit fields, record URL outcomes and ledger rows.

Usage: python3 scripts/research/apply-third-party-batch.py round29_batch36_data

The data module provides:

  ROUND, DATE
  PROMOTIONS: [{record, field, value, source, sourceType, status, note, notesAppend, document,
                whyNotManufacturer}]
  URL_RESULTS: [{url, status, chunksOpened, chunksTotal, evidence,
                 fieldResults: [{record, field, value, outcome, note}], dropRows: [[record, field]]}]

Every promotion must quote the document in `note` and name that document in `document`; the ledger row
records why MANUFACTURER_VERIFIED was unavailable. Values are never inferred: the caller asserts the
current stored value equals the promoted value.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
LEDGER = os.path.join(HERE, 'round29-third-party-ledger.json')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def main(name):
    ev = load(name)
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}
    ledger = json.load(open(LEDGER, encoding='utf-8'))
    ledger_entries = ledger.setdefault('entries', [])

    applied = 0
    for p in ev.PROMOTIONS:
        rec = by_id[p['record']]
        key = p['field'] + 'Provenance'
        prov = rec.get(key) or {}
        assert rec[p['field']] == p['value'], (p['record'], p['field'], rec[p['field']], p['value'])
        assert len(p['note']) >= 40 and '"' in p['note'], (p['record'], 'note must quote the document')
        if prov.get('status') == p['status'] and prov.get('source') == p['source']:
            continue
        assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', (p['record'], prov.get('status'))
        new_prov = {'status': p['status'], 'source': p['source'],
                    'sourceType': p['sourceType'], 'note': p['note']}
        before = {'value': rec[p['field']], 'provenance': dict(prov)}
        rec[key] = new_prov
        if (p['record'], p['field'], 'PROMOTE_THIRD_PARTY') not in seen:
            history['entries'].append({
                'id': p['record'], 'field': p['field'], 'value': p['value'], 'before': before,
                'after': {'value': p['value'], 'provenance': new_prov},
                'round': ev.ROUND, 'action': 'PROMOTE_THIRD_PARTY', 'source': p['source']})
            seen.add((p['record'], p['field'], 'PROMOTE_THIRD_PARTY'))
        if p.get('notesAppend') and p['notesAppend'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['notesAppend']).strip()
        if not any(e.get('record') == p['record'] and e.get('field') == p['field']
                   for e in ledger_entries):
            ledger_entries.append({
                'record': p['record'], 'field': p['field'],
                'valueBefore': before['value'], 'valueAfter': p['value'],
                'status': p['status'], 'sourceType': p['sourceType'], 'source': p['source'],
                'document': p['document'], 'evidence': p['note'],
                'whyNotManufacturer': p['whyNotManufacturer'],
                'decision': ('Promoted per PROVENANCE-POLICY.md: exact model, explicit wording, opened '
                             'https source, quoted evidence, this ledger row.'),
            })
        applied += 1

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
        for rid, field in entry.get('dropRows', []):
            merged.pop(f'{rid}.{field}', None)
        for f in entry['fieldResults']:
            merged[f"{f['record']}.{f['field']}"] = f
        by_url[url] = {'url': url, 'round': ev.ROUND, 'status': entry['status'],
                       'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
                       'checkedDate': ev.DATE, 'evidence': entry['evidence'],
                       'fieldResults': list(merged.values()), 'history': snapshots}
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    dump(DATA, db)
    dump(STATUS, status)
    dump(HISTORY, history)
    dump(LEDGER, ledger)
    print(f'{name}: promotions={applied} url_results={len(ev.URL_RESULTS)}')


if __name__ == '__main__':
    main(sys.argv[1])
