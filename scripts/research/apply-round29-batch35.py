#!/usr/bin/env python3
"""Apply Round 29 batch 35: Bose 802 Series II THIRD_PARTY_VERIFIED promotions."""
import importlib.util
import json
import os

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


def main():
    ev = load('round29_batch35_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}
    ledger = json.load(open(LEDGER, encoding='utf-8'))
    for p in ev.PROMOTIONS:
        rec = by_id[p['record']]
        key = p['field'] + 'Provenance'
        prov = rec.get(key) or {}
        assert rec[p['field']] == p['value'], (p['record'], rec[p['field']])
        if prov.get('status') == 'THIRD_PARTY_VERIFIED' and prov.get('source') == p['source']:
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
        if p['notesAppend'].strip() and p['notesAppend'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['notesAppend']).strip()
        ledger.setdefault('records', []).append({
            'record': p['record'], 'field': p['field'], 'value': p['value'],
            'source': p['source'], 'sourceType': p['sourceType'], 'status': p['status'],
            'note': p['note']})

    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    for entry in ev.URL_RESULTS:
        url = entry['url']
        old = by_url[url]
        merged = {f"{f['record']}.{f['field']}": f for f in old.get('fieldResults', [])}
        for f in entry['fieldResults']:
            merged[f"{f['record']}.{f['field']}"] = f
        old.update({'round': ev.ROUND, 'status': entry['status'], 'chunksOpened': entry['chunksOpened'],
                    'chunksTotal': entry['chunksTotal'], 'checkedDate': ev.DATE,
                    'evidence': entry['evidence'], 'fieldResults': list(merged.values())})
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    dump(DATA, db)
    dump(STATUS, status)
    dump(HISTORY, history)
    dump(LEDGER, ledger)
    print('round29 batch35: promotions=%d url_results=%d' % (len(ev.PROMOTIONS), len(ev.URL_RESULTS)))


if __name__ == '__main__':
    main()
