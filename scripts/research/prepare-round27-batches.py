#!/usr/bin/env python3
"""Prepare Round 27 dispute artifacts (2026-10-19).

Builds scripts/research/round27-url-results.json from round27_disputes_data.py and
validates every declared field against the live catalogue BEFORE anything is written.

A result tuple is (field, outcome, note [, valueToWrite [, action]]):
- PROMOTED without an action keeps the stored value and verifies it;
- CORRECTED writes valueToWrite and must differ from the stored value;
- RESOURCE writes the same value but re-points the provenance at the checked document;
- RETRACT writes None and returns the provenance to UNSOURCED.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
OUT = os.path.join(HERE, 'round27-url-results.json')

ALLOWED_BEFORE = {
    'PROMOTED': ('CITED_IN_NOTES_UNCHECKED', 'MANUFACTURER_VERIFIED'),
    'CORRECTED': ('CITED_IN_NOTES_UNCHECKED',),
    'NOT_STATED': ('CITED_IN_NOTES_UNCHECKED', 'MANUFACTURER_VERIFIED'),
    'SUPPORTED_NOT_PROMOTED': ('CITED_IN_NOTES_UNCHECKED',),
}


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ev = load('round27_disputes_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}

    prior = {}
    if os.path.exists(OUT):
        for e in json.load(open(OUT, encoding='utf-8'))['entries']:
            for fr in e['fieldResults']:
                prior[(fr['record'], fr['field'])] = fr

    entries = []
    for chk in ev.CHECKS:
        source = chk.get('sourceOverride', chk['url'])
        assert source.startswith('https://'), source
        field_results = []
        for result in chk['results']:
            key, outcome, note = result[0], result[1], result[2]
            record_id, field = key.split('.')
            record = by_id.get(record_id)
            assert record is not None, f'unknown record {record_id}'
            assert field in ('driverCount', 'active'), field
            prov = record.get(field + 'Provenance') or {}
            stored = record.get(field)
            action = result[4] if len(result) > 4 else None
            after = result[3] if len(result) > 3 else stored
            applied = (
                stored == after and
                ((action == 'RETRACT' and prov.get('status') == 'UNSOURCED') or
                 (action != 'RETRACT' and prov.get('status') == 'MANUFACTURER_VERIFIED'))
            )
            if applied:
                previous = prior.get((record_id, field))
                assert previous is not None, f'{key}: already applied but no prior result artifact'
                stored = previous['valueBefore']
                assert previous['valueAfter'] == after, f'{key}: prior artifact disagrees on the new value'
            else:
                assert prov.get('status') in ALLOWED_BEFORE[outcome], (
                    f'{key}: status {prov.get("status")} not valid for {outcome}')
            if (outcome in ('PROMOTED', 'CORRECTED', 'SUPPORTED_NOT_PROMOTED')
                    and action not in ('RESOURCE', 'RETRACT') and not applied):
                assert prov.get('source') == chk['url'], (
                    f'{key}: provenance source {prov.get("source")} != checked URL {chk["url"]}')
            if action == 'CORRECT':
                assert after != stored, f'{key}: CORRECT must change the value'
            if action == 'RESOURCE':
                assert after == stored, f'{key}: RESOURCE must keep the value'
            if action == 'RETRACT':
                assert after is None, f'{key}: RETRACT must clear the value'
            field_results.append({
                'record': record_id,
                'field': field,
                'valueBefore': stored,
                'valueAfter': after,
                'outcome': outcome,
                'action': action,
                'sourceUrl': source,
                'note': note,
            })
        statuses = {fr['outcome'] for fr in field_results}
        entry_status = 'CHECKED_PARTIAL'
        if statuses <= {'PROMOTED', 'CORRECTED'}:
            entry_status = 'CHECKED_CONFIRMED'
        entries.append({
            'url': chk['url'],
            'sourceUrl': source,
            'host': source.split('/')[2],
            'sourceClass': chk['sourceClass'],
            'round': ev.ROUND,
            'checkedDate': ev.CHECKED_DATE,
            'document': chk['document'],
            'chunksOpened': chk['chunksOpened'],
            'chunksTotal': chk['chunksTotal'],
            'status': entry_status,
            'evidence': chk['evidence'],
            'fieldResults': field_results,
        })

    out = {'round': ev.ROUND, 'checkedDate': ev.CHECKED_DATE, 'entries': entries}
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    total = sum(len(e['fieldResults']) for e in entries)
    writes = [fr for e in entries for fr in e['fieldResults']
              if fr['outcome'] in ('PROMOTED', 'CORRECTED')]
    print(f'round27-url-results.json: urls={len(entries)} field_results={total} '
          f'value_writes={len(writes)}')
    for e in entries:
        print(f"  {e['status']:15s} {len(e['fieldResults'])}  {e['sourceUrl']}")


if __name__ == '__main__':
    main()
