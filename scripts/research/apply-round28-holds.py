#!/usr/bin/env python3
"""Record the Round 28 reassessment of the four HELD_PENDING_URL_CHECK records (2026-10-19).

Reads round28_holds_data.py. This script deliberately does NOT write driverCount/active: the data rule
in src/data/speakers.round3.test.ts admits only CITED_IN_NOTES_UNCHECKED, UNSOURCED and
MANUFACTURER_VERIFIED for those fields, and none of these sources is a manufacturer host. Instead it:

  * asserts each field is still null/UNSOURCED (nothing moved since Round 4);
  * appends a dated reassessment sentence to the record notes;
  * writes round28-held-restore.json with the evidence, the would-be value and the exact blocker.

No history entry is created because no value changes. The test and the schema are left untouched.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
LEDGER = os.path.join(HERE, 'round28-held-restore.json')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ev = load('round28_holds_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    rows = []
    for a in ev.ASSESSMENTS:
        rec = by_id[a['record']]
        for field in ('driverCount', 'active'):
            prov = rec.get(field + 'Provenance') or {}
            assert rec[field] is None, f'{a["record"]}.{field} unexpectedly has a value'
            assert prov.get('status') == 'UNSOURCED', (a['record'], field, prov.get('status'))
            rows.append({
                'record': a['record'], 'field': field,
                'storedValue': None, 'storedStatus': 'UNSOURCED',
                'documentedValue': a[field],
                'evidence': a[field + 'Evidence'],
                'source': a['source'], 'sourceType': a['sourceType'], 'document': a['document'],
                'outcome': 'EVIDENCE_FOUND_SCHEMA_BLOCKED',
                'blocker': ('src/data/speakers.round3.test.ts admits only CITED_IN_NOTES_UNCHECKED, '
                            'UNSOURCED and MANUFACTURER_VERIFIED for driverCount/active; this source is '
                            'not a manufacturer host and the field has now been checked, so neither a '
                            'manufacturer nor an unchecked label would be true.'),
                'ownerDecisionNeeded': 'Whether driverCount/active may carry third-party or reputable-database provenance.',
            })
        assert a['notes_append'].strip() not in rec.get('notes', '')
        rec['notes'] = (rec.get('notes', '').rstrip() + a['notes_append']).strip()

    with open(DATA, 'w', encoding='utf-8') as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(LEDGER, 'w', encoding='utf-8') as fh:
        json.dump({
            'schema': 'round28-held-assessment/v1', 'round': ev.ROUND, 'date': ev.DATE,
            'description': ('The four records whose driverCount/active were held pending a URL check since '
                            'round 4. Each document was reopened and states the value; the values remain '
                            'unwritten because the data rule for these two fields admits only manufacturer '
                            'sources. Evidence and blocker are recorded per field.'),
            'valueChanges': 0,
            'entries': rows,
        }, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'round28 holds: fields_assessed={len(rows)} values_written=0 '
          f'records={len(ev.ASSESSMENTS)}')


if __name__ == '__main__':
    main()
