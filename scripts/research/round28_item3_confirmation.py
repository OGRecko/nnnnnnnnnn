#!/usr/bin/env python3
"""Round 28 item 3 (2026-10-19): re-verify the five disputed items and write the confirmation ledger.

Read-only for src/data/speakers.json: this script asserts the stored state and records, per item, the
document that was opened in this session, the exact wording, and whether the stored value/status is
still correct. It writes scripts/research/round28-item3-ledger.json.

Items: yamaha-ns-6490, electro-voice-elx200-15, focal-sopra-n-2, turbosound-ip15b (archived),
qsc-wl3082 / qsc-wl212-sw.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
ARCHIVE = os.path.join(ROOT, 'scripts', 'research', 'removed-unavailable-2026-10-12.json')
OUT = os.path.join(HERE, 'round28-item3-ledger.json')
DATE = '2026-10-19'
ROUND = 28

YAMAHA_US = 'https://usa.yamaha.com/products/audio_visual/speaker_systems/ns-6490/specs.html'
FOCAL = 'https://media.focal-naim.com/dam/sopra-n-2/fp_sopra_n2_en.pdf'
QSC_MANUAL = ('https://www.qscaudio.com/resource-files/productresources/spk/wideline_8/'
              'q_spk_wl8_usermanual.pdf')

ITEMS = [
    {
        'record': 'yamaha-ns-6490',
        'field': 'impedance',
        'stored': {'value': 8, 'status': 'MANUFACTURER_VERIFIED'},
        'verdict': 'CONFIRMED_US_VARIANT',
        'document': YAMAHA_US,
        'evidence': ('Opened the US specification page: "Nominal Impedance | 8 ohms", '
                     '"Sensitivity | 90 dB/2.83 V/m", drivers "8\\" Cone Woofer, 4\\" Cone Mid-Range, '
                     '7/8\\" Balanced Dome Tweeter", "45 Hz - 23 kHz", nominal 70 W / maximum 140 W.'),
        'regionalCheck': ('The Malaysia URL recorded in the notes (my.yamaha.com .../ns-6490/specs.html) '
                          'now redirects to the generic Malaysia products page, so its 6-ohm figure could '
                          'not be re-read in this round. The stored 8 ohm stays a US-variant value under '
                          'owner decision 7; the two regional values are not merged and no Malaysian '
                          'specification is applied.'),
        'action': 'NONE',
    },
    {
        'record': 'electro-voice-elx200-15',
        'field': 'frequencyResponse.disputedPoints',
        'stored': {'points': 85, 'status': 'UNRESOLVED_ROW_COUNT', 'simulationExcluded': True},
        'verdict': 'DOCUMENTED_AND_EXCLUDED',
        'document': 'scripts/research/round27-field-and-dataset-ledger.json (both editions, round 27)',
        'evidence': ('The record already carries the edition comparison: FR edition 86 rows (2400 and '
                     '2600 Hz, no 2500 Hz), EN edition 87 rows (2400, 2500, 2600 Hz), 9 stored-vs-FR '
                     'differences and 61 stored-vs-EN differences, FR impedance falling to 1.1 ohm below '
                     'the stated 7.0 ohm minimum, and neither table reproducing the stated -3 dB / -10 dB '
                     'limits (77 Hz-16 kHz / 52 Hz-19 kHz).'),
        'action': 'NONE — the series stays excluded; no point was replaced and no alternate series adopted.',
    },
    {
        'record': 'focal-sopra-n-2',
        'field': 'sensitivity',
        'stored': {'value': 91, 'reference': '2.83V/1m', 'status': 'MANUFACTURER_VERIFIED'},
        'verdict': 'CONFIRMED_WITH_REFERENCE',
        'document': FOCAL,
        'evidence': ('The product sheet was opened in this session and its specification table reads '
                     '"Sensitivity (2.83V / 1m) | 91dB", "Nom. impedance | 8Ω", "Minimum impedance | '
                     '3.1Ω", "Frequency response (+/- 3dB) | 34Hz - 40kHz".'),
        'regionalCheck': ('The brief asked to retain 91 dB "at third-party level without an exact-model '
                          'source naming the sensitivity reference". That premise is not reproduced: the '
                          'exact-model manufacturer sheet is live and names the 2.83 V / 1 m reference. '
                          'The stored manufacturer-level provenance and reference are therefore kept; no '
                          'downgrade would be evidence-based.'),
        'action': 'NONE',
    },
    {
        'record': 'turbosound-ip15b',
        'field': 'sourceType',
        'stored': {'live': False, 'location': 'ARCHIVED (removed-unavailable-2026-10-12.json)'},
        'verdict': 'NOT_ON_A_LIVE_RECORD',
        'document': ARCHIVE,
        'evidence': ('The iP15B record is archived, not live, so there is no live sourceType to change. '
                     'The archived note cites the Turbosound Product Information Document as a third-party '
                     'mirror and identifies the manufacturer PDF.'),
        'regionalCheck': ('Owner policy forbids restoring archived products, so the distributor-datasheet '
                          'origin question has no live effect in this round. It is recorded here for the '
                          'owner rather than acted on.'),
        'action': 'NONE — archived record left untouched.',
    },
    {
        'record': 'qsc-wl3082',
        'field': 'active',
        'stored': {'value': False, 'status': 'MANUFACTURER_VERIFIED'},
        'verdict': 'CONFIRMED_BY_EXPLICIT_STATEMENT',
        'document': QSC_MANUAL,
        'evidence': ('"WL3082 Connections" section: "The WL3082 loudspeaker is not equipped with a '
                     'crossover network. All signal processing must be done before connecting audio power '
                     'to the loudspeaker. Do not connect full-range audio to the high-frequency '
                     'transducer or damage may result!" The introduction also lists two 8" low-frequency '
                     'drivers and one 3.0" voice-coil compression driver (three transducers).'),
        'regionalCheck': 'The value comes from an explicit statement, not from the absence of a crossover mention.',
        'action': 'NONE',
    },
    {
        'record': 'qsc-wl212-sw',
        'field': 'active',
        'stored': {'value': None, 'status': 'UNAVAILABLE'},
        'verdict': 'STILL_UNSTATED',
        'document': QSC_MANUAL,
        'evidence': ('Introduction confirms "two ceramic magnet, 4” voice coil, 12” transducers provide '
                     '1100 watt continuous power handling"; the connections section describes NL8/NL4 '
                     'audio-power connectors but never states passive or powered.'),
        'regionalCheck': 'No active/passive statement, so the field stays unknown.',
        'action': 'NONE',
    },
]


def main():
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    checks = []

    y = by_id['yamaha-ns-6490']
    assert y['impedance']['value'] == 8 and y['impedance']['status'] == 'MANUFACTURER_VERIFIED'
    assert y['sensitivity']['value'] == 90

    elx = by_id['electro-voice-elx200-15']['frequencyResponse']['disputedPoints']
    assert elx['status'] == 'UNRESOLVED_ROW_COUNT' and elx['simulationExcluded'] is True
    assert len(elx['points']) == 85
    facts = elx['editionComparison']['facts']
    assert facts['frRows'] == 86 and facts['enRows'] == 87 and facts['storedVsFrDiffs'] == 9
    assert facts['storedMissingHz'] == [2400, 2600] and facts['frMissingHz'] == [2500]

    f = by_id['focal-sopra-n-2']['sensitivity']
    assert f['value'] == 91 and f['reference'] == '2.83V/1m' and f['status'] == 'MANUFACTURER_VERIFIED'

    w = by_id['qsc-wl3082']
    assert w['active'] is False and w['activeProvenance']['status'] == 'MANUFACTURER_VERIFIED'
    assert w['driverCount'] == 3
    s = by_id['qsc-wl212-sw']
    assert s['active'] is None and s['activeProvenance']['status'] in ('UNAVAILABLE', 'UNSOURCED')
    assert s['driverCount'] == 2

    arch = json.load(open(ARCHIVE, encoding='utf-8'))['records']
    assert any(r['id'] == 'turbosound-ip15b' for r in arch)
    assert not any(r['id'] == 'turbosound-ip15b' for r in db), 'iP15B must not be live'

    for item in ITEMS:
        checks.append(item)

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({
            'schema': 'round28-item3-ledger/v1', 'round': ROUND, 'date': DATE,
            'note': ('Item 3 of the 2026-10-19 brief. Every document listed here was opened in this '
                     'session. No stored value or status was changed; the entries record why.'),
            'items': checks,
            'valueChanges': 0,
        }, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'round28 item3: items={len(checks)} value_changes=0')


if __name__ == '__main__':
    main()
