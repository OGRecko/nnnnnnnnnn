#!/usr/bin/env python3
"""Apply Round 29 batch 52 (2026-10-19): alternate sources for dead URLs.

Writes MANUFACTURER_VERIFIED when the evidence is on the manufacturer's own host, THIRD_PARTY_VERIFIED when
it is an accepted database entry (audio-database), and nothing at all for NOT_STATED /
SUPPORTED_NOT_PROMOTED. Idempotent; the queue keeps a snapshot of every replaced URL entry.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round29-value-history.json')
LEDGER = os.path.join(HERE, 'provenance-source-ledger.json')

TIERS = {
    'MANUFACTURER': ('MANUFACTURER_VERIFIED', 'MANUFACTURER'),
    'REPUTABLE_DATABASE': ('THIRD_PARTY_VERIFIED', 'REPUTABLE_DATABASE'),
    'THIRD_PARTY': ('THIRD_PARTY_VERIFIED', 'THIRD_PARTY'),
}


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
    ev = load('round29_batch52_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action'), h.get('source')) for h in history['entries']}

    promoted = skipped = 0
    for p in ev.PROMOTIONS:
        status, source_type = TIERS[p['tier']]
        rec = by_id[p['record']]
        key = p['field'] + 'Provenance'
        prov = rec.get(key) or {}
        assert rec[p['field']] == p['value'], (p['record'], rec[p['field']], p['value'])
        if prov.get('status') == status and prov.get('source') == p['source']:
            skipped += 1
            continue
        assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', (p['record'], prov.get('status'))
        if p['tier'] != 'MANUFACTURER':
            # policy condition 3: the retained source must be https and must have been opened.
            assert p['source'].startswith('https://'), p['source']
        new = {'status': status, 'source': p['source'], 'sourceType': source_type, 'note': p['note']}
        before = {'value': rec[p['field']], 'provenance': dict(prov)}
        rec[key] = new
        if (p['record'], p['field'], 'PROMOTE', p['source']) not in seen:
            history['entries'].append({
                'id': p['record'], 'field': p['field'], 'value': p['value'],
                'before': before, 'after': {'value': p['value'], 'provenance': new},
                'round': ev.ROUND, 'action': 'PROMOTE', 'source': p['source'],
            })
            seen.add((p['record'], p['field'], 'PROMOTE', p['source']))
        if p['append'].strip() and p['append'].strip() not in rec.get('notes', ''):
            rec['notes'] = (rec.get('notes', '').rstrip() + p['append']).strip()
        promoted += 1
    history['marker'] = 'round29-batch52-alternate-sources'

    # Non-promoted outcomes: assert the stored value still matches, then write nothing to speakers.json.
    for n in ev.NOT_PROMOTED:
        rec = by_id[n['record']]
        assert rec[n['field']] == n['value'], (n['record'], rec[n['field']])
        prov = rec.get(n['field'] + 'Provenance') or {}
        assert prov.get('status') == 'CITED_IN_NOTES_UNCHECKED', (n['record'], prov.get('status'))

    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    field_index = {}
    for p in ev.PROMOTIONS:
        field_index.setdefault(p['source'], []).append(
            {'record': p['record'], 'field': p['field'], 'value': p['value'],
             'outcome': 'PROMOTED', 'note': p['fieldNote']})
    for n in ev.NOT_PROMOTED:
        field_index.setdefault(n['source'], []).append(
            {'record': n['record'], 'field': n['field'], 'value': n['value'],
             'outcome': n['outcome'], 'note': n['note']})

    for entry in ev.URL_RESULTS:
        url = entry['url']
        old = by_url.get(url)
        if old is None:
            old = {'url': url, 'status': 'OPEN', 'fieldResults': []}
            status['urls'].append(old)
        snapshots = list(old.get('history', []))
        if old.get('status') not in (None, 'OPEN') and old.get('round') != ev.ROUND:
            snapshots.append({'snapshotOfRound': old.get('round'),
                              'entry': {k: v for k, v in old.items() if k != 'history'}})
        merged = {f"{f['record']}.{f['field']}": f for f in old.get('fieldResults', [])}
        for f in field_index.get(url, []):
            merged[f"{f['record']}.{f['field']}"] = f
        by_url[url] = {
            'url': url, 'round': ev.ROUND, 'status': entry['status'],
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'checkedDate': ev.DATE, 'sourceClass': entry['sourceClass'],
            'document': entry['document'], 'evidence': entry['evidence'],
            'fieldResults': list(merged.values()), 'history': snapshots,
        }
    status['urls'] = [by_url[u['url']] for u in status['urls']]

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    have = {s.get('url') for s in ledger['sources']}
    added = 0
    for entry in ev.URL_RESULTS:
        if entry['url'] in have:
            continue
        decisions = []
        for f in field_index.get(entry['url'], []):
            decisions.append({
                'id': f['record'], 'field': f['field'], 'value': f['value'],
                'result': 'CONFIRMED' if f['outcome'] == 'PROMOTED' else f['outcome'],
                'decision': TIERS[[p for p in ev.PROMOTIONS
                                   if p['record'] == f['record'] and p['field'] == f['field']][0]['tier']]
                            if f['outcome'] == 'PROMOTED' else 'UNCHANGED',
                'evidence': f['note']})
        ledger['sources'].append({
            'url': entry['url'], 'host': ev.HOSTS[entry['url']], 'document': entry['document'],
            'status': entry['status'], 'openedDate': ev.DATE,
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'sourceClass': entry['sourceClass'], 'coverage': entry['evidence'],
            'decisions': decisions,
            'queueItemsResolved': sum(1 for d in decisions if d['result'] == 'CONFIRMED'),
        })
        added += 1

    dump(DATA, db)
    dump(HISTORY, history)
    dump(STATUS, status)
    dump(LEDGER, ledger)
    print(f'round29 batch52: promotions={promoted} already_promoted={skipped} '
          f'url_results={len(ev.URL_RESULTS)} unchanged_outcomes={len(ev.NOT_PROMOTED)} '
          f'ledger_sources_added={added}')


if __name__ == '__main__':
    main()
