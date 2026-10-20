#!/usr/bin/env python3
"""Round 29 batch 50 (2026-10-19): an explicit "passive loudspeaker" statement for the B&W CM10.

Sound & Vision's Test Bench page for the Bowers & Wilkins CM10 states: "The passive loudspeaker was measured
with the grille at a distance of 1 meter with a 2.83-volt input." That is the policy's first accepted form for
`active: false` — the document calls the product passive — and the same sentence documents a 2.83 V input,
i.e. speaker-level drive with no mains connection. The page does not enumerate drive units, so `driverCount`
is left untouched.
"""
DATE = '2026-10-19'
ROUND = 29

CM10 = 'https://www.soundandvision.com/content/bowers-wilkins-cm10-loudspeaker-test-bench'

WHY = ('Sound & Vision is an independent review magazine; the Test Bench measurement report is not a '
       'Bowers & Wilkins document.')

PROMOTIONS = [
    {'record': 'legacy-bw-6', 'field': 'active', 'value': False, 'source': CM10,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Sound & Vision, "Bowers & Wilkins CM10 Loudspeaker Test Bench"',
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Sound & Vision Test Bench — "The passive loudspeaker was measured with '
              'the grille at a distance of 1 meter with a 2.83-volt input." The measurement report calls the '
              'CM10 a passive loudspeaker and drives it at speaker level (2.83 V), with no mains connection.'),
     'notesAppend': (' Round 29 (2026-10-19): active false verified from the Sound & Vision Test Bench '
                     '("The passive loudspeaker was measured ..."); driverCount remains unresolved because '
                     'the page does not enumerate the drive units.')},
]

URL_RESULTS = [
    {'url': CM10, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1, 3], 'chunksTotal': 5,
     'evidence': ('"The passive loudspeaker was measured with the grille at a distance of 1 meter with a '
                  '2.83-volt input."; "Sensitivity: 88.5 dB from 500 Hz to 2 kHz"; impedance minimum '
                  '3.72 ohms; no drive-unit list.'),
     'fieldResults': [
         {'record': 'legacy-bw-6', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: the report calls the CM10 "the passive loudspeaker".'},
         {'record': 'legacy-bw-6', 'field': 'driverCount', 'value': 5, 'outcome': 'NOT_STATED',
          'note': 'Round 29: the page measures the system but never lists its drive units.'},
     ]},
]
