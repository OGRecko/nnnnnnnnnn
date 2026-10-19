#!/usr/bin/env python3
"""Apply Round 27 dispute outcomes to the catalogue (2026-10-19).

Reads scripts/research/round27-url-results.json plus round27_disputes_data.py and writes:

- src/data/speakers.json             field values/provenance, the LSR32 resolved series and
                                     the ELX200-15 edition comparison record;
- round27-value-history.json         every before/after pair (never overwrites earlier entries);
- queue-url-status.json              checked URLs (history snapshots preserved);
- provenance-source-ledger.json      the documents opened this round;
- round27-field-and-dataset-ledger.json  one row per adjudicated item.

Nothing is inferred. A field is written only when the URL entry declares it, and a
value changes only through an explicit CORRECT / RETRACT action.
"""
import datetime
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
RESULTS = os.path.join(HERE, 'round27-url-results.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
LEDGER = os.path.join(HERE, 'provenance-source-ledger.json')
HISTORY = os.path.join(HERE, 'round27-value-history.json')
FIELD_LEDGER = os.path.join(HERE, 'round27-field-and-dataset-ledger.json')

ROUND = 27


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def main():
    ev = load('round27_disputes_data')
    results = json.load(open(RESULTS, encoding='utf-8'))
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = {'round': ROUND, 'entries': []}
    seen = set()
    field_rows = []
    written = changed = 0

    for entry in results['entries']:
        source = entry['sourceUrl']
        for fr in entry['fieldResults']:
            record = by_id[fr['record']]
            field = fr['field']
            prov = record.get(field + 'Provenance') or {}
            already = (
                record.get(field) == fr['valueAfter'] and
                ((fr.get('action') == 'RETRACT' and prov.get('status') == 'UNSOURCED') or
                 (fr.get('action') != 'RETRACT' and prov.get('status') == 'MANUFACTURER_VERIFIED' and
                  prov.get('source') == source))
            )
            if already:
                continue
            assert record.get(field) == fr['valueBefore'], (
                f"{fr['record']}.{field} moved after prepare")
            outcome, action = fr['outcome'], fr.get('action')
            before = {'value': record.get(field), 'provenance': dict(prov)}
            if outcome not in ('PROMOTED', 'CORRECTED') and action not in ('RESOURCE', 'RETRACT'):
                field_rows.append({
                    'record': fr['record'], 'field': field, 'outcome': outcome,
                    'valueKept': record.get(field), 'source': source, 'note': fr['note'],
                })
                continue
            if action == 'RETRACT':
                record[field] = None
                new_prov = {'status': 'UNSOURCED', 'source': None, 'sourceType': None,
                            'note': 'Round 27: ' + fr['note']}
            else:
                record[field] = fr['valueAfter']
                new_prov = {'status': 'MANUFACTURER_VERIFIED', 'source': source,
                            'sourceType': 'MANUFACTURER',
                            'note': f"Round {ROUND}: " + fr['note']}
            record[field + 'Provenance'] = new_prov
            key = (fr['record'], field, source, action)
            if key not in seen:
                history['entries'].append({
                    'id': fr['record'], 'field': field, 'value': record[field],
                    'before': before, 'after': {'value': record[field], 'provenance': new_prov},
                    'round': ROUND, 'action': action or 'PROMOTE', 'source': source,
                })
                seen.add(key)
            written += 1
            if before['value'] != record[field]:
                changed += 1
            field_rows.append({
                'record': fr['record'], 'field': field, 'outcome': outcome,
                'action': action, 'valueBefore': before['value'], 'valueAfter': record[field],
                'source': source, 'note': fr['note'],
            })

    # ---------------------------------------------------------------- LSR32
    lsr = by_id['jbl-lsr32']
    fr = lsr['frequencyResponse']
    new_points = [{'hz': hz, 'db': db_} for hz, db_ in ev.LSR32_TABLE]
    assert len(new_points) == 28 and new_points[0]['hz'] == 20 and new_points[-1]['hz'] == 20000
    if fr.get('resolution', {}).get('status') == 'RESOLVED_VERBATIM_MANUAL_TABLE_20KHZ':
        print('  LSR32 already resolved; series untouched')
        old_points = fr['resolution']['priorPoints']
    else:
        prior = fr.pop('disputedPoints')
        assert prior['status'] == 'UNRESOLVED_SELF_CONFLICT_20KHZ'
        old_points = prior['points']
        fr['points'] = new_points
        fr['pointsStatus'] = 'MANUFACTURER_VERIFIED'
        fr['pointsSourceType'] = 'MANUFACTURER'
        fr['pointsSource'] = ev.LSR32_MANUAL
        fr['pointsContext'] = ev.LSR32_CONTEXT
        fr['resolution'] = {
            'date': ev.CHECKED_DATE, 'round': ROUND,
            'status': 'RESOLVED_VERBATIM_MANUAL_TABLE_20KHZ',
            'summary': ev.LSR32_RESOLUTION_NOTE,
            'priorDisputedStatus': prior['status'],
            'priorExclusionReason': prior.get('exclusionReason'),
            'priorPoints': old_points,
            'priorPointsCount': len(old_points),
            'rowsChanged': 12,
            'changedHz': [30, 40, 50, 70, 80, 300, 400, 500, 600, 700, 900, 1000],
            'addedHz': [20000],
            'record': 'scripts/research/round27-value-history.json',
        }
        lsr['notes'] = (
            'Exact JBL LSR32 specification and measurements in the official LSR Series Owner\'s Manual. '
            'The manual specifies 60 Hz-22 kHz (+1/-1.5 dB), with -3 dB at 54 Hz and -10 dB at 35 Hz; the field '
            'records only the stated nominal response band. It lists 93 dB at 2.83 V/1 m (also 90 dB at 1 W/1 m), '
            '4-ohm nominal impedance, 200 W continuous / 800 W peak, 12-inch LF woofer with a 2-inch voice coil, '
            'and three transducers. The separate enclosure resonance specification is 28 Hz and is recorded as '
            'such, not as a driver free-air resonance. Round 27 (2026-10-19): the 20 kHz self-conflict is '
            'resolved. The LSR32 Amplitude & Phase table reads 92 dB at 20 kHz and the LSR32 Acoustic Contribution '
            'fundamental also reads 92 dB; the 61 dB value belongs to the LSR28P table (61 dB at 10 kHz, blank at '
            '20 kHz). The response series has been replaced with the verbatim 28-row Amplitude & Phase table '
            '(the previous 27-row series differed at 12 frequencies and omitted 20 kHz; it is preserved in '
            'frequencyResponse.resolution.priorPoints). The manual measures anechoically at 2 m referenced to 1 m; '
            'the drive level is not stated, so the series is used as normalised shape only, with absolute level '
            'from the verified sensitivity field. No polar payload is imported; nominal coverage is not '
            'converted to directivity. Source: ' + ev.LSR32_MANUAL
        )
        field_rows.append({
            'record': 'jbl-lsr32', 'field': 'frequencyResponse.points', 'outcome': 'RESOLVED_DATASET',
            'action': 'REPLACE_SERIES', 'valueBefore': f'{len(old_points)} points (20 Hz-10 kHz)',
            'valueAfter': '28 points (20 Hz-20 kHz, verbatim Amplitude & Phase table)',
            'source': ev.LSR32_MANUAL, 'note': ev.LSR32_RESOLUTION_NOTE,
        })
        history['entries'].append({
            'id': 'jbl-lsr32', 'field': 'frequencyResponse.disputedPoints', 'value': len(new_points),
            'before': {'status': prior['status'], 'simulationExcluded': prior.get('simulationExcluded'),
                       'points': old_points},
            'after': {'status': 'RESOLVED_VERBATIM_MANUAL_TABLE_20KHZ',
                      'pointsStatus': 'MANUFACTURER_VERIFIED',
                      'pointsSource': ev.LSR32_MANUAL, 'points': new_points},
            'round': ROUND, 'action': 'RESOLVE_SERIES', 'source': ev.LSR32_MANUAL,
        })

    # ------------------------------------------------------------- ELX200-15
    elx = by_id['electro-voice-elx200-15']
    dp = elx['frequencyResponse']['disputedPoints']
    assert dp['status'] == 'UNRESOLVED_ROW_COUNT'
    assert dp['simulationExcluded'] is True, 'ELX200-15 must stay excluded'
    if dp.get('editionComparison', {}).get('verdict') == ev.ELX['verdict']:
        print('  ELX200-15 edition comparison already recorded; untouched')
    else:
        edition_note = (
            'Round 27 edition comparison (2026-10-19): both official editions were retrieved and their full '
            'tables transcribed (scripts/research/data/elx200-15-editions-2026-10-19.py). The FR edition has '
            '86 rows (2400 and 2600 Hz, no 2500 Hz); the EN edition has 87 rows (2400, 2500 and 2600 Hz); the '
            'two editions differ at 64 shared frequencies, and their impedance columns are mutually exclusive '
            '(FR falls to 1.1 ohm, below the 7.0 ohm minimum the same sheet states; EN peaks at 110 ohm at '
            '2500 Hz). The stored 85-point series matches neither edition (9 values differ from FR, 61 from '
            'EN, and it has 2500 Hz without 2400/2600). Text-derived -3 dB / -10 dB crossings from either '
            'table do not reproduce the stated 77 Hz-16 kHz / 52 Hz-19 kHz limits. The series therefore '
            'remains excluded; no point was rewritten and no alternate series adopted.'
        )
        dp['editionComparison'] = {
            'date': ev.CHECKED_DATE, 'round': ROUND, 'verdict': ev.ELX['verdict'],
            'frEdition': ev.ELX['frEdition'], 'enEdition': ev.ELX['enEdition'],
            'facts': ev.ELX['facts'], 'reason': ev.ELX['reason'], 'summary': edition_note,
            'evidenceData': 'scripts/research/data/elx200-15-editions-2026-10-19.py',
        }
        dp['exclusionReason'] = (
            'Still unresolved after the Round 27 comparison of both official editions: 86 vs 87 rows, 64 '
            'differing shared sensitivity values, impedance columns that contradict each other and the '
            'stated 7.0 ohm minimum, and a stored 85-point series matching neither edition. Excluded from '
            'simulation until an owner decision; no response series may be adopted from these tables.'
        )
        field_rows.append({
            'record': 'electro-voice-elx200-15', 'field': 'frequencyResponse.disputedPoints',
            'outcome': 'UNRESOLVED_EDITION_CONFLICT', 'action': 'NONE',
            'valueBefore': '85 points, UNRESOLVED_ROW_COUNT',
            'valueAfter': '85 points retained, UNRESOLVED_ROW_COUNT, editionComparison recorded',
            'source': ev.ELX['enEdition'], 'note': ev.ELX['reason'],
        })

    with open(DATA, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(db, indent=2, ensure_ascii=False) + '\n')
    dump(HISTORY, history)

    # ------------------------------------------------------- queue + ledger
    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    added_status = 0
    for entry in results['entries']:
        url = entry['url']
        old = by_url.get(url)
        if old is None:
            old = {'url': url, 'status': 'OPEN'}
            status['urls'].append(old)
            added_status += 1
        snapshots = list(old.get('history', []))
        if old.get('status') not in (None, 'OPEN'):
            snapshots.append({'snapshotOfRound': old.get('round'),
                              'entry': {k: v for k, v in old.items() if k != 'history'}})
        updated = {
            'url': url, 'round': ROUND, 'status': entry['status'],
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'checkedDate': entry['checkedDate'], 'sourceClass': entry['sourceClass'],
            'document': entry['document'], 'evidence': entry['evidence'],
            'sourceUrl': entry['sourceUrl'],
            'fieldResults': entry['fieldResults'], 'history': snapshots,
        }
        by_url[url] = updated
    status['urls'] = [by_url[u['url']] for u in status['urls']]
    dump(STATUS, status)

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    have = {s.get('url') for s in ledger['sources']}
    added_sources = 0
    for entry in results['entries']:
        if entry['sourceUrl'] in have:
            continue
        ledger['sources'].append({
            'url': entry['sourceUrl'], 'host': entry['host'], 'document': entry['document'],
            'status': entry['status'], 'openedDate': entry['checkedDate'],
            'chunksOpened': entry['chunksOpened'], 'chunksTotal': entry['chunksTotal'],
            'sourceClass': entry['sourceClass'], 'round': ROUND, 'coverage': entry['evidence'],
        })
        added_sources += 1
    dump(LEDGER, ledger)

    dump(FIELD_LEDGER, {
        'round': ROUND, 'checkedDate': ev.CHECKED_DATE,
        'entries': field_rows,
        'elx200_15': ev.ELX,
        'lsr32': {'resolution': 'RESOLVED_VERBATIM_MANUAL_TABLE_20KHZ', 'rows': len(new_points),
                  'priorRows': len(old_points)},
    })
    print(f'round27 apply: urls={len(results["entries"])} fields_written={written} '
          f'values_changed={changed} queue_urls_added={added_status} ledger_sources_added={added_sources}')
    print(f'  LSR32 points={len(new_points)} prior={len(old_points)}; ELX200-15 excluded='
          f'{elx["frequencyResponse"]["disputedPoints"]["simulationExcluded"]}')


if __name__ == '__main__':
    main()
