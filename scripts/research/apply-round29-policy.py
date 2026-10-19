#!/usr/bin/env python3
"""Apply Round 29 (2026-10-19): first THIRD_PARTY_VERIFIED structural-field batch.

Reads round29_policy_data.py. The policy conditions (scripts/research/PROVENANCE-POLICY.md) are enforced
here, not assumed:

  * the record exists exactly once and the field is still null with UNSOURCED provenance;
  * source is https, sourceType is THIRD_PARTY or REPUTABLE_DATABASE;
  * the note contains a quotation mark (the evidence quote) and at least 40 characters;
  * a ledger row records prior state, new value, document, quote-bearing note and the owner instruction.

Writes src/data/speakers.json, round29-value-history.json and round29-third-party-ledger.json. No other
status is written; MANUFACTURER_VERIFIED is untouched.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
LEDGER = os.path.join(HERE, 'round29-third-party-ledger.json')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ev = load('round29_policy_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {}
    for r in db:
        assert r['id'] not in by_id, f'duplicate id {r["id"]}'
        by_id[r['id']] = r
    history = (json.load(open(HISTORY, encoding='utf-8')) if os.path.exists(HISTORY)
               else {'round': ev.ROUND, 'entries': []})
    history['round'] = ev.ROUND
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}
    rows, written = [], 0

    for entry in ev.ENTRIES:
        rec = by_id[entry['record']]
        assert entry['source'].startswith('https://')
        assert entry['sourceType'] in ('THIRD_PARTY', 'REPUTABLE_DATABASE')
        assert ev.NOTES_SUPERSEDE.strip() not in rec.get('notes', '')
        for field, payload in entry['fields'].items():
            prov_key = field + 'Provenance'
            prov = rec.get(prov_key) or {}
            assert rec[field] is None, f'{entry["record"]}.{field} already has a value'
            assert prov.get('status') == 'UNSOURCED', (entry['record'], field, prov.get('status'))
            note = payload['note']
            assert '"' in note and len(note) >= 40, (entry['record'], field, 'note lacks quoted evidence')
            before = {'value': None, 'provenance': dict(prov)}
            rec[field] = payload['value']
            new_prov = {
                'status': 'THIRD_PARTY_VERIFIED',
                'source': entry['source'],
                'sourceType': entry['sourceType'],
                'note': note,
            }
            rec[prov_key] = new_prov
            key = (entry['record'], field, 'PROMOTE_THIRD_PARTY')
            if key not in seen:
                history['entries'].append({
                    'id': entry['record'], 'field': field, 'value': payload['value'],
                    'before': before, 'after': {'value': payload['value'], 'provenance': new_prov},
                    'round': ev.ROUND, 'action': 'PROMOTE_THIRD_PARTY',
                    'source': entry['source'], 'decision': ev.DECISION,
                })
                seen.add(key)
            rows.append({
                'record': entry['record'], 'field': field,
                'valueBefore': None, 'valueAfter': payload['value'],
                'status': 'THIRD_PARTY_VERIFIED', 'sourceType': entry['sourceType'],
                'source': entry['source'], 'document': entry['document'],
                'evidence': note, 'decision': ev.DECISION,
                'whyNotManufacturer': ('The document is not served by the manufacturer and no owner-approved '
                                       'manufacturer copy exists for this model.'),
            })
            written += 1
        rec['notes'] = (rec.get('notes', '').rstrip() + ev.NOTES_SUPERSEDE).strip()

    with open(DATA, 'w', encoding='utf-8') as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(HISTORY, 'w', encoding='utf-8') as fh:
        json.dump(history, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(LEDGER, 'w', encoding='utf-8') as fh:
        json.dump({
            'schema': 'round29-third-party-ledger/v1', 'round': ev.ROUND, 'date': ev.DATE,
            'policy': 'scripts/research/PROVENANCE-POLICY.md',
            'ownerInstruction': ev.DECISION,
            'entries': rows, 'valuesWritten': written,
        }, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'round29 policy apply: records={len(ev.ENTRIES)} fields_written={written}')


if __name__ == '__main__':
    main()
