#!/usr/bin/env python3
"""Apply Round 29 batch 55: UNSOURCED nulls promoted at the THIRD_PARTY_VERIFIED tier.

`apply-structural-batch.py` only writes MANUFACTURER_VERIFIED, so this companion does the same job for a
manufacturer-authored document served from a non-manufacturer host. It enforces the provenance policy's
six conditions rather than assuming them:

- the field is currently null with status UNSOURCED (nothing cited is overwritten);
- the source is an https URL that was opened this session;
- the note quotes the document (>= 40 chars, contains a literal double quote);
- the document is named, and the reason MANUFACTURER_VERIFIED is unavailable is recorded.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
HISTORY = os.path.join(HERE, 'round29-structural-history.json')
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
    ev = load('round29_batch55_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    hist = json.load(open(HISTORY, encoding='utf-8')) if os.path.exists(HISTORY) else {'entries': []}
    seen = {(h['id'], h['field'], h['after']['provenance'].get('source')) for h in hist['entries']}

    written = skipped = 0
    for p in ev.PROMOTIONS:
        assert p['source'].startswith('https://'), p['source']
        assert len(p['note']) >= 40 and '"' in p['note'], (p['record'], 'note must quote the document')
        assert p.get('document'), p['record']
        if p['sourceType'] == 'THIRD_PARTY':
            assert p.get('whyNotManufacturer'), p['record']
        rec = by_id[p['record']]
        key = p['field'] + 'Provenance'
        prov = rec.get(key) or {}
        want = 'MANUFACTURER_VERIFIED' if p['sourceType'] == 'MANUFACTURER' else 'THIRD_PARTY_VERIFIED'
        if rec.get(p['field']) == p['value'] and prov.get('status') == want \
                and prov.get('source') == p['source']:
            skipped += 1
            continue
        assert rec.get(p['field']) is None, f"{p['record']}.{p['field']} already {rec.get(p['field'])!r}"
        assert prov.get('status') == 'UNSOURCED', f"{p['record']}.{p['field']} status {prov.get('status')}"
        new = {'status': want, 'source': p['source'],
               'sourceType': p['sourceType'], 'note': p['note']}
        rec[p['field']] = p['value']
        rec[key] = new
        if (p['record'], p['field'], p['source']) not in seen:
            hist['entries'].append({
                'id': p['record'], 'field': p['field'],
                'before': {'value': None, 'provenance': dict(prov)},
                'after': {'value': p['value'], 'provenance': new},
                'round': ev.ROUND,
                'action': 'PROMOTE_MANUFACTURER' if p['sourceType'] == 'MANUFACTURER'
                          else 'PROMOTE_THIRD_PARTY',
                'source': p['source'],
                'reason': ('Exact-model manufacturer document opened; explicit statement recorded.'
                           if p['sourceType'] == 'MANUFACTURER' else
                           'Exact-model manufacturer datasheet opened; explicit statement recorded. '
                           'Host is not the manufacturer: ' + p['whyNotManufacturer']),
            })
            seen.add((p['record'], p['field'], p['source']))
        if p['append'].strip() and p['append'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['append']).strip()
        written += 1
    if hist.get('entries'):
        hist.setdefault('round', ev.ROUND)

    # Record the two documents against the URL queue so the provenance queue sees them.
    dump(DATA, db)
    dump(HISTORY, hist)

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    entries = ledger.setdefault('entries', [])
    have = {e.get('url') for e in entries}
    added = 0
    for url in {p['source'] for p in ev.PROMOTIONS if p['sourceType'] == 'THIRD_PARTY'}:
        if url in have:
            continue
        mine = [p for p in ev.PROMOTIONS if p['source'] == url]
        entries.append({
            'url': url, 'host': ev.HOSTS[url], 'document': mine[0]['document'],
            'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
            'openedDate': ev.DATE, 'round': ev.ROUND,
            'whyNotManufacturer': mine[0]['whyNotManufacturer'],
            'decisions': [{'id': p['record'], 'field': p['field'], 'value': p['value'],
                           'result': 'CONFIRMED', 'decision': 'THIRD_PARTY_VERIFIED',
                           'evidence': p['note']} for p in mine],
        })
        added += 1
    dump(LEDGER, ledger)
    print(f'round29 batch55: written={written} skipped={skipped} ledger_sources_added={added}')


if __name__ == '__main__':
    main()
