#!/usr/bin/env python3
"""Rebuild round27-value-history.json from the Round 27 artifacts.

The first apply-round27-batch.py runs wrote the history file from a fresh list each
time, so a later idempotent run (0 writes) left it empty. Every before/after pair is
still recoverable from:
  - round27-url-results.json  (valueBefore / valueAfter / action / source)
  - queue-url-status.json     (pre-Round-27 snapshots, for the prior note/source)
  - src/data/speakers.json    (current after-state)
  - jbl-lsr32 frequencyResponse.resolution.priorPoints (the superseded series)

This script writes the recovered entries. It does not invent values.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
RESULTS = os.path.join(HERE, 'round27-url-results.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
HISTORY = os.path.join(HERE, 'round27-value-history.json')

ROUND = 27
QSC_SHEET = ('https://www.qscaudio.com/resource-files/productresources/spk/wideline_8/'
             'q_spk_wl8_specs.pdf')
QSC_PRIOR = {
    'qsc-wl3082': 'Round 22 (2026-10-19): manufacturer page evidence: QSC WideLine-8 specification '
                  'sheet: passive line-array element requiring external amplification.',
    'qsc-wl212-sw': 'Round 22 (2026-10-19): manufacturer page evidence: QSC WideLine-8 specification '
                    'sheet: passive subwoofer element requiring external amplification.',
}


def prior_note(status, record_id, field):
    for entry in status['urls']:
        for snap in entry.get('history', []):
            for fr in snap.get('entry', {}).get('fieldResults', []):
                if fr.get('record') == record_id and fr.get('field') == field:
                    return fr.get('note', '')
    return ''


def main():
    db = {r['id']: r for r in json.load(open(DATA, encoding='utf-8'))}
    results = json.load(open(RESULTS, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    entries = []
    for entry in results['entries']:
        for fr in entry['fieldResults']:
            if fr['outcome'] not in ('PROMOTED', 'CORRECTED') and fr.get('action') not in ('RESOURCE', 'RETRACT'):
                continue
            record = db[fr['record']]
            field = fr['field']
            if fr['record'] in QSC_PRIOR:
                before_prov = {'status': 'MANUFACTURER_VERIFIED', 'source': QSC_SHEET,
                               'sourceType': 'MANUFACTURER', 'note': QSC_PRIOR[fr['record']]}
            else:
                before_prov = {
                    'status': 'CITED_IN_NOTES_UNCHECKED', 'source': entry['url'], 'sourceType': None,
                    'note': prior_note(status, fr['record'], field)
                            or 'Cited-in-notes record opened in Round 27; prior note is preserved in '
                               'queue-url-status.json history.',
                }
            entries.append({
                'id': fr['record'], 'field': field, 'value': record.get(field),
                'before': {'value': fr['valueBefore'], 'provenance': before_prov},
                'after': {'value': record.get(field), 'provenance': record.get(field + 'Provenance')},
                'round': ROUND, 'action': fr.get('action') or 'PROMOTE',
                'source': entry['sourceUrl'],
            })

    lsr = db['jbl-lsr32']['frequencyResponse']
    res = lsr['resolution']
    entries.append({
        'id': 'jbl-lsr32', 'field': 'frequencyResponse.disputedPoints', 'value': len(lsr['points']),
        'before': {'status': res['priorDisputedStatus'], 'simulationExcluded': True,
                   'points': res['priorPoints']},
        'after': {'status': res['status'], 'pointsStatus': lsr['pointsStatus'],
                  'pointsSource': lsr['pointsSource'], 'points': lsr['points']},
        'round': ROUND, 'action': 'RESOLVE_SERIES', 'source': lsr['pointsSource'],
    })

    seen = set()
    unique = []
    for e in entries:
        key = (e['id'], e['field'], e.get('source'), e.get('action'))
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)
    out = {'round': ROUND, 'rebuiltFrom': ['round27-url-results.json', 'queue-url-status.json',
                                           'src/data/speakers.json'], 'entries': unique}
    with open(HISTORY, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f'rebuilt round27-value-history.json: {len(unique)} entries')


if __name__ == '__main__':
    main()
