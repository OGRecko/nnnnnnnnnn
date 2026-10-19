#!/usr/bin/env python3
"""Round 29: close queue rows whose record is archived.

`build-field-provenance-inventory.py` still lists driverCount/active for records that were retired into
`removed-*.json` (Bose smart speakers, Sonos, Turbosound iP15B, legacy JBL/Focal/EV). Those fields cannot be
written, so leaving them as open rows inflates the backlog and hides the live work. Each row is marked
RECORD_ARCHIVED with a pointer to the archive file; the record stays in the archive (nothing is deleted)
and the queue keeps the outcome instead of counting it as outstanding.
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
STATUS = os.path.join(HERE, 'queue-url-status.json')
QUEUE = os.path.join(HERE, 'field-provenance-url-queue.json')
DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def main():
    db = json.load(open(os.path.join(ROOT, 'src', 'data', 'speakers.json'), encoding='utf-8'))
    live = {r['id'] for r in db}
    archived = {}
    for path in sorted(glob.glob(os.path.join(HERE, 'removed-*.json'))):
        data = json.load(open(path, encoding='utf-8'))
        for item in data.get('records', []):
            rec = item.get('record', item) if isinstance(item, dict) else {}
            if rec.get('id'):
                archived[rec['id']] = os.path.basename(path)

    raw = json.load(open(QUEUE, encoding='utf-8'))
    urls = raw if isinstance(raw, list) else raw.get('urls') or raw.get('items')
    wanted = {}
    for row in urls:
        for f in row.get('fields', []):
            if f.get('location') == 'ARCHIVED' and f['record'] in archived:
                wanted.setdefault(row['url'], set()).add((f['record'], f['field']))

    status = json.load(open(STATUS, encoding='utf-8'))
    added = 0
    for entry in status['urls']:
        pairs = wanted.get(entry['url'])
        if not pairs:
            continue
        recorded = {(f.get('record'), f.get('field')) for f in entry.get('fieldResults', [])}
        for rid, field in sorted(pairs):
            if (rid, field) in recorded:
                continue
            entry.setdefault('fieldResults', []).append({
                'record': rid, 'field': field, 'value': None, 'outcome': 'RECORD_ARCHIVED',
                'note': (f'Round 29 (2026-10-19): record retired into {archived[rid]}; the field cannot be '
                         'written and is no longer outstanding.'),
            })
            added += 1

    dump(STATUS, status)
    print(f'round29 archived rows: added={added} urls={len(archived)} archived_records={len(archived)}')


if __name__ == '__main__':
    main()
