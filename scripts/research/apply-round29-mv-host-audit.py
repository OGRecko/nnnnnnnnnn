#!/usr/bin/env python3
"""Round 29: demote MANUFACTURER_VERIFIED structural fields that sit on non-manufacturer hosts.

The 2026-10-19 owner instruction restricts MANUFACTURER_VERIFIED to manufacturer-owned hosts or explicitly
approved manufacturer copies. `source-host-allowlist.json` records which hosts are ESTABLISHED. Any
`driverCount`/`active` field marked MV whose source host is NOT_MANUFACTURER is therefore mislabelled: the
value is kept (it is not contradicted), the status becomes CITED_IN_NOTES_UNCHECKED, the original note is
preserved and a short policy sentence is appended, and the before/after pair goes into value history.

The report (`round29-mv-host-audit.json`) lists every row with its host, status and note so the demotion is
auditable. Re-running is a no-op once the statuses are CITED.
"""
import json
import os
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
ALLOWLIST = os.path.join(HERE, 'source-host-allowlist.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
REPORT = os.path.join(HERE, 'round29-mv-host-audit.json')
DATE = '2026-10-19'
ROUND = 29
SUFFIX = (' Round 29 (2026-10-19): host is NOT_MANUFACTURER in source-host-allowlist.json, so it cannot '
          'support MANUFACTURER_VERIFIED; demoted to CITED_IN_NOTES_UNCHECKED. The quoted evidence above is '
          'preserved.')


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def main():
    allow = {h['host']: h['status'] for h in json.load(open(ALLOWLIST, encoding='utf-8'))['hosts']}
    db = json.load(open(DATA, encoding='utf-8'))
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}

    rows = []
    for rec in db:
        for field in ('driverCount', 'active'):
            prov = rec.get(field + 'Provenance') or {}
            if prov.get('status') != 'MANUFACTURER_VERIFIED':
                continue
            source = prov.get('source') or ''
            host = urlparse(source).netloc.lower().replace('www.', '')
            if allow.get(host) != 'NOT_MANUFACTURER':
                continue
            before = {'value': rec.get(field), 'provenance': dict(prov)}
            note = (prov.get('note') or '').rstrip()
            if SUFFIX.strip() not in note:
                note = (note + SUFFIX).strip()
            new_prov = {'status': 'CITED_IN_NOTES_UNCHECKED', 'source': source,
                        'sourceType': None, 'note': note}
            rec[field + 'Provenance'] = new_prov
            if (rec['id'], field, 'DEMOTE_POLICY') not in seen:
                history['entries'].append({
                    'id': rec['id'], 'field': field, 'value': rec.get(field),
                    'before': before, 'after': {'value': rec.get(field), 'provenance': new_prov},
                    'round': ROUND, 'action': 'DEMOTE_POLICY', 'source': source,
                    'reason': 'host NOT_MANUFACTURER under the 2026-10-19 policy',
                })
                seen.add((rec['id'], field, 'DEMOTE_POLICY'))
            rows.append({'record': rec['id'], 'field': field, 'value': rec.get(field),
                         'host': host, 'hostStatus': 'NOT_MANUFACTURER', 'source': source,
                         'from': 'MANUFACTURER_VERIFIED', 'to': 'CITED_IN_NOTES_UNCHECKED'})

    report = {'schema': 'round29-mv-host-audit/v1', 'date': DATE, 'round': ROUND,
              'policy': ('MANUFACTURER_VERIFIED requires an ESTABLISHED manufacturer host or an approved '
                         'manufacturer copy; see source-host-allowlist.json and PROVENANCE-POLICY.md.'),
              'demoted': len(rows), 'rows': rows}
    dump(DATA, db)
    dump(HISTORY, history)
    dump(REPORT, report)
    print(f'round29 mv host audit: demoted={len(rows)}')


if __name__ == '__main__':
    main()
