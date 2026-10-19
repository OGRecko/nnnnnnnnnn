#!/usr/bin/env python3
"""Apply Round 28 batch 29 (2026-10-19).

Reads round28_batch29_data.py and writes:

- src/data/speakers.json   note corrections only (jbl-4311 notes, pointsContext); no value changes;
- round28-value-history.json   before/after for every touched note;
- queue-url-status.json    the two rechecked JBL URLs, with the prior entry kept in `history`;
- round28-url-results.json the recheck ledger;
- round28-response-dataset-reconciliation.json  the generated count reconciliation.

No field value or provenance status is changed. A recheck that supports a value but cannot promote it
stays exactly where it is; a field the document never states stays unresolved.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round28-value-history.json')
RESULTS = os.path.join(HERE, 'round28-url-results.json')
RECON = os.path.join(HERE, 'round28-response-dataset-reconciliation.json')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def walk_points(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'points' and isinstance(v, list) and v:
                yield path + '.' + k, obj, v
            else:
                yield from walk_points(v, path + '.' + k)


def main():
    ev = load('round28_batch29_data')
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8'))
    history['round'] = ev.ROUND
    seen = {(h['id'], h['field'], h.get('source'), h.get('action')) for h in history['entries']}
    notes_changed = []

    def log_note(rid, field, before, after, reason):
        key = (rid, field, None, 'CORRECT_NOTE')
        if key in seen:
            return
        history['entries'].append({
            'id': rid, 'field': field, 'value': None,
            'before': {'text': before}, 'after': {'text': after},
            'round': ev.ROUND, 'action': 'CORRECT_NOTE', 'source': None, 'reason': reason,
        })
        seen.add(key)

    # ------------------------------------------------- jbl-4311 record notes
    r = by_id['jbl-4311']
    old_notes = r['notes']
    assert ev.JBL_4311_NOTES_FIND in old_notes, 'jbl-4311 note text moved'
    new_notes = old_notes.replace(ev.JBL_4311_NOTES_FIND, ev.JBL_4311_NOTES_REPLACE)
    r['notes'] = new_notes
    log_note('jbl-4311', 'notes', old_notes, new_notes,
             'The opened page never says passive; the unsupported characterisation was removed.')
    notes_changed.append(('jbl-4311', 'notes'))

    fr = r['frequencyResponse']
    old_ctx = fr.get('pointsContext', '')
    if 'response-table recheck' not in old_ctx:
        new_ctx = old_ctx.rstrip() + ev.JBL_4311_DATASET_NOTE
        fr['pointsContext'] = new_ctx
        log_note('jbl-4311', 'frequencyResponse.pointsContext', old_ctx, new_ctx,
                 'The re-fetched table does not match the stored series; the discrepancy is recorded.')
        notes_changed.append(('jbl-4311', 'frequencyResponse.pointsContext'))

    # --------------------------------------------------- 4311 table comparison
    stored = {p['hz']: p['db'] for p in fr['points']}
    page = dict(ev.JBL_4311_TABLE)
    shared = sorted(set(stored) & set(page))
    differing = [{'hz': hz, 'stored': stored[hz], 'page': page[hz], 'delta': round(stored[hz] - page[hz], 2)}
                 for hz in shared if stored[hz] != page[hz]]
    comparison = {
        'record': 'jbl-4311',
        'source': ev.JBL_4311_URL,
        'checkedDate': ev.DATE,
        'storedPoints': len(stored),
        'printedRows': len(page),
        'sharedFrequencies': len(shared),
        'storedOnlyHz': sorted(set(stored) - set(page)),
        'pageOnlyHz': sorted(set(page) - set(stored)),
        'differingCount': len(differing),
        'differing': differing,
        'action': 'NONE — owner decision of 2026-10-12 keeps the stored series until adjudicated',
        'round21Claim': '2 differing points (800 Hz, 3150 Hz)',
        'round28Finding': f'{len(differing)} differing shared frequencies plus a stored-only 25 Hz row',
    }

    # -------------------------------------------- response dataset reconciliation
    blocks = []
    for rec in db:
        for path, parent, pts in walk_points(rec, rec['id']):
            hz = [p['hz'] for p in pts]
            bad = [i for i, p in enumerate(pts)
                   if not (isinstance(p.get('hz'), (int, float)) and isinstance(p.get('db'), (int, float)))]
            gaps = [[a, b] for a, b in zip(hz, hz[1:]) if a > 0 and b / a > 1.5]
            rel = path.split('.', 1)[1]
            blocks.append({
                'record': rec['id'],
                'path': rel,
                'role': 'ACTIVE_SERIES' if rel == 'frequencyResponse.points' else 'PRESERVED_OR_ALTERNATE_BLOCK',
                'points': len(pts),
                'hzMin': min(hz), 'hzMax': max(hz),
                'ascending': all(a < b for a, b in zip(hz, hz[1:])),
                'duplicateHz': sorted({h for h in hz if hz.count(h) > 1}),
                'malformedIndexes': bad,
                'gapCount': len(gaps),
                'excludedFromSimulation': bool(
                    parent.get('simulationExcluded')) if isinstance(parent, dict) else False,
                'pointsStatus': parent.get('pointsStatus') if isinstance(parent, dict) else None,
            })
    active = [b for b in blocks if b['role'] == 'ACTIVE_SERIES']
    preserved = [b for b in blocks if b['role'] != 'ACTIVE_SERIES']
    recon = {
        'schema': 'round28-response-dataset-reconciliation/v1',
        'generated': 'scripts/research/apply-round28-batch.py',
        'date': ev.DATE,
        'question': 'The round brief asks to reconcile the response-dataset count of 27.',
        'answer': {
            'pointBearingBlocks': len(blocks),
            'distinctRecords': len({b['record'] for b in blocks}),
            'activeSeriesBlocks': len(active),
            'preservedOrAlternateBlocks': len(preserved),
            'explanation': (
                '27 is the number of point-bearing blocks, not records. 24 live records each carry one '
                'active `frequencyResponse.points` series; electro-voice-elx200-15 contributes three '
                'further blocks — its excluded 85-point disputed series, the identical 85-point copy kept '
                'under primarySourceReconciliation, and the 87-row alternate published edition. So 24 + 3 '
                '= 27 blocks across 25 records, of which only the 24 active series are solver-eligible.'
            ),
        },
        'blocks': blocks,
        'jbl4311Comparison': comparison,
        'valueChanges': 0,
    }

    # ------------------------------------------------------------- URL status
    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    results_log = (json.load(open(RESULTS, encoding='utf-8')) if os.path.exists(RESULTS)
                   else {'schema': 'round28-url-results/v1', 'round': ev.ROUND, 'entries': []})
    have = {e['url'] for e in results_log['entries']}
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
        for f in entry['fieldResults']:
            merged[f"{f['record']}.{f['field']}"] = f
        updated = {
            'url': url, 'round': ev.ROUND, 'status': entry['status'],
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': 2,
            'checkedDate': ev.DATE, 'evidence': entry['evidence'],
            'fieldResults': list(merged.values()), 'history': snapshots,
        }
        by_url[url] = updated
        if url not in have:
            results_log['entries'].append({
                'url': url, 'status': entry['status'], 'checkedDate': ev.DATE,
                'chunksOpened': entry['chunksOpened'], 'evidence': entry['evidence'],
                'fieldResults': entry['fieldResults'],
                'hostPolicy': ('tile.loc.gov is not an established manufacturer host; the document is JBL\'s '
                               'own brochure, so the value is supported but not promotable.'
                               if 'loc.gov' in url else 'Manufacturer host; no promotion because the '
                               'document does not state the field.'),
            })
            have.add(url)

    dump(DATA, db)
    dump(HISTORY, history)
    dump(STATUS, status)
    dump(RESULTS, results_log)
    dump(RECON, recon)
    print(f'round28 batch29: notes_changed={len(notes_changed)} value_changes=0 '
          f'urls_rechecked={len(ev.URL_RESULTS)} '
          f'blocks={len(blocks)} active={len(active)} preserved={len(preserved)} '
          f'4311_diff={len(differing)} storedOnly={comparison["storedOnlyHz"]}')


if __name__ == '__main__':
    main()
