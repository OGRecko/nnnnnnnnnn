#!/usr/bin/env python3
"""Apply Round 29 batch 31: two MV promotions on EKX-15P; write the unsourced/no-provenance ledger."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
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
    ev = load('round29_batch31_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}

    applied = 0
    for p in ev.PROMOTIONS:
        rec = by_id[p['record']]
        key = p['field'] + 'Provenance'
        assert rec[p['field']] is None, (p['record'], p['field'], rec[p['field']])
        assert (rec.get(key) or {}).get('status') == 'UNSOURCED', (p['record'], key)
        new_prov = {'status': 'MANUFACTURER_VERIFIED', 'source': p['source'],
                    'sourceType': 'MANUFACTURER', 'note': p['note']}
        if (p['record'], p['field'], 'PROMOTE') in seen:
            continue
        before = {'value': None, 'provenance': dict(rec.get(key) or {})}
        rec[p['field']] = p['value']
        rec[key] = new_prov
        history['entries'].append({
            'id': p['record'], 'field': p['field'], 'value': p['value'],
            'before': before, 'after': {'value': p['value'], 'provenance': new_prov},
            'round': ev.ROUND, 'action': 'PROMOTE', 'source': p['source'],
        })
        seen.add((p['record'], p['field'], 'PROMOTE'))
        applied += 1
        if p['notesAppend'] and p['notesAppend'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['notesAppend']).strip()

    ledger = {'schema': 'round29-unsourced-ledger/v1', 'date': ev.DATE, 'round': ev.ROUND,
              'note': ('Outcomes for fields that carried no provenance or UNSOURCED status. A row is an '
                       'outcome record, not a provenance object; fields without explicit evidence keep '
                       'their null and their status.'),
              'promotions': [{'record': p['record'], 'field': p['field'], 'value': p['value'],
                              'status': 'MANUFACTURER_VERIFIED', 'source': p['source']}
                             for p in ev.PROMOTIONS],
              'assessments': ev.ASSESSMENTS}

    dump(DATA, db)
    dump(HISTORY, history)
    dump(LEDGER, ledger)
    print(f'round29 batch31: promotions_applied={applied} assessments={len(ev.ASSESSMENTS)}')


if __name__ == '__main__':
    main()
