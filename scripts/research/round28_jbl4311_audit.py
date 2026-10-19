#!/usr/bin/env python3
"""Round 28 item 2/4 (2026-10-19): full-field audit of jbl-4311 against its opened manufacturer page.

The page https://jblpro.com/en-US/site_elements/4311-information was opened in this session (both
chunks). Every populated field of the record is compared with the wording on that page. Two changes are
made:

  * power gains a `notes` string recording that JBL's 75 W is *continuous program* power, defined by the
    page as 3 dB above continuous sine-wave (RMS) power, so the rating is not re-interpreted as RMS;
  * resonantFreq, previously UNAVAILABLE, is populated with 22 Hz from the page's "free air resonance is
    approximately 22 Hz" for the 12-inch low-frequency loudspeaker.

Nothing else changes. The response-point discrepancy documented in round 28 batch 29 is not touched.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
HISTORY = os.path.join(HERE, 'round28-value-history.json')
LEDGER = os.path.join(HERE, 'round28-field-audit-jbl4311.json')
URL = 'https://jblpro.com/en-US/site_elements/4311-information'
DATE = '2026-10-19'
ROUND = 28

POWER_NOTE = (
    'Round 28 (2026-10-19) field audit: the page\'s specification row is "Power Capacity: 75 W continuous '
    'program", and its footnote defines continuous program power as 3 dB greater than continuous sine '
    'wave (RMS) power. The stored scalar is that program rating; it is not RMS and must not be converted.'
)
RESONANT_NOTE = (
    'Round 28 (2026-10-19) field audit: the page states of the 12-inch low-frequency loudspeaker that '
    '"free air resonance is approximately 22 Hz". Stored as 22 Hz with the source\'s approximation; this '
    'is the driver free-air resonance, not an enclosure tuning frequency.'
)


def main():
    db = json.load(open(DATA, encoding='utf-8'))
    rec = next(r for r in db if r['id'] == 'jbl-4311')
    history = json.load(open(HISTORY, encoding='utf-8'))
    seen = {(h['id'], h['field'], h.get('action')) for h in history['entries']}

    checks = []

    def check(field, stored, evidence, outcome='MATCH'):
        checks.append({'field': field, 'stored': stored, 'evidence': evidence, 'outcome': outcome})

    check('driverCount', rec['driverCount'],
          'Components: 300-mm (12-in) LF, 130-mm (5-in) midrange, 36-mm (1.4-in) HF direct radiator = 3.')
    check('active', rec['active'],
          'The page never states passive/active/powered and shows no amplifier; value remains unresolved.',
          'UNRESOLVED_KEPT')
    check('sensitivity', rec['sensitivity'],
          '"Sensitivity: 91 dB, 1 W, 1 m (3.3 ft)" with controls set for flattest response.')
    check('impedance', rec['impedance'], '"Nominal Impedance: 8 Ω".')
    check('power', rec['power'],
          '"Power Capacity: 75 W continuous program"; footnote: program = 3 dB above continuous sine (RMS).',
          'MATCH_NOTE_ADDED')
    check('voiceCoil', rec['voiceCoil'], '"76-mm (3-in) diameter edgewound copper ribbon voice coil".')
    check('woofer', rec['woofer'], '"300-mm (12-in) low frequency loudspeaker".')
    check('frequencyResponse', {'low_hz': rec['frequencyResponse']['low_hz'],
                                'high_hz': rec['frequencyResponse']['high_hz']},
          '"Frequency Response: 45 Hz - 15 kHz ± 3 dB".')
    check('frequencyResponse.points', len(rec['frequencyResponse']['points']),
          'Stored series does not reproduce the re-fetched 28-row table; documented, not changed.',
          'DISCREPANCY_DOCUMENTED')
    check('resonantFreq', rec['resonantFreq'],
          '"free air resonance is approximately 22 Hz" (12-inch LF loudspeaker).', 'POPULATED')

    # power notes (no value/status change)
    assert 'continuous program' not in rec['power'].get('notes', '')
    rec['power']['notes'] = POWER_NOTE
    if ('jbl-4311', 'power', 'CORRECT_NOTE') not in seen:
        history['entries'].append({
            'id': 'jbl-4311', 'field': 'power', 'value': 75,
            'before': {'value': 75, 'notes': None}, 'after': {'value': 75, 'notes': POWER_NOTE},
            'round': ROUND, 'action': 'CORRECT_NOTE', 'source': URL,
        })
        seen.add(('jbl-4311', 'power', 'CORRECT_NOTE'))

    # resonantFreq promotion
    rf = rec['resonantFreq']
    assert rf['value'] is None and rf['status'] == 'UNAVAILABLE'
    before = {'value': None, 'provenance': dict(rf)}
    rec['resonantFreq'] = {
        'value': 22, 'unit': 'Hz', 'status': 'MANUFACTURER_VERIFIED',
        'source': URL, 'sourceType': 'MANUFACTURER', 'notes': RESONANT_NOTE,
    }
    if ('jbl-4311', 'resonantFreq', 'PROMOTE') not in seen:
        history['entries'].append({
            'id': 'jbl-4311', 'field': 'resonantFreq', 'value': 22,
            'before': before, 'after': {'value': 22, 'provenance': rec['resonantFreq']},
            'round': ROUND, 'action': 'PROMOTE', 'source': URL,
        })
        seen.add(('jbl-4311', 'resonantFreq', 'PROMOTE'))

    with open(DATA, 'w', encoding='utf-8') as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(HISTORY, 'w', encoding='utf-8') as fh:
        json.dump(history, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(LEDGER, 'w', encoding='utf-8') as fh:
        json.dump({
            'schema': 'round28-field-audit/v1', 'round': ROUND, 'date': DATE,
            'record': 'jbl-4311', 'source': URL, 'chunksOpened': [0, 1],
            'fields': checks,
            'valuesChanged': 1, 'notesChanged': 1,
            'responseSeries': 'unchanged; discrepancy documented in frequencyResponse.pointsContext',
        }, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'round28 jbl-4311 audit: fields={len(checks)} values_changed=1 notes_changed=1')


if __name__ == '__main__':
    main()
