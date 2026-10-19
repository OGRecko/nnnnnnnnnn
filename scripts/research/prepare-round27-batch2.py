#!/usr/bin/env python3
"""Append Round 27 batch 2 URL results (see round27_batch2_data.py) to the round artifact."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'src', 'data', 'speakers.json')
OUT = os.path.join(HERE, 'round27-url-results.json')


def main():
    spec = importlib.util.spec_from_file_location('b2', os.path.join(HERE, 'round27_batch2_data.py'))
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    db = {r['id']: r for r in json.load(open(DATA, encoding='utf-8'))}
    out = json.load(open(OUT, encoding='utf-8'))
    known = {e['url'] for e in out['entries']}
    added = 0
    for chk in ev.CHECKS:
        if chk['url'] in known:
            continue
        field_results = []
        for key, outcome, note in chk['results']:
            record_id, field = key.split('.')
            record = db[record_id]
            prov = record.get(field + 'Provenance') or {}
            assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', f'{key}: {prov.get("status")}'
            value = record.get(field)
            field_results.append({
                'record': record_id, 'field': field, 'valueBefore': value, 'valueAfter': value,
                'outcome': outcome, 'action': None, 'sourceUrl': chk['url'], 'note': note,
            })
        statuses = {fr['outcome'] for fr in field_results}
        out['entries'].append({
            'url': chk['url'], 'sourceUrl': chk['url'], 'host': chk['url'].split('/')[2],
            'sourceClass': chk['sourceClass'], 'round': ev.ROUND, 'checkedDate': ev.CHECKED_DATE,
            'document': chk['document'], 'chunksOpened': chk['chunksOpened'],
            'chunksTotal': chk['chunksTotal'],
            'status': 'CHECKED_CONFIRMED' if statuses <= {'PROMOTED', 'CORRECTED'} else 'CHECKED_PARTIAL',
            'evidence': chk['evidence'], 'fieldResults': field_results,
        })
        added += 1
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f'batch2 appended: urls={added} total={len(out["entries"])}')


if __name__ == '__main__':
    main()
