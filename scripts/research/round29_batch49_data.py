#!/usr/bin/env python3
"""Round 29 batch 49 (2026-10-19): four more driver complements, no `active` changes.

  elac-uni-fi-ub5 — ELAC Uni-Fi sell sheet (Andrew Jones series): the UB5 column reads "3-way bass reflex",
    "Tweeter 1-inch soft dome", "Mid-Range 4-inch aluminum", "Woofer 5.25-inch aluminum". Three drive-unit
    rows, so three transducers; the concentric tweeter/midrange pair is counted as its two transducers, the
    convention already used for the KEF Uni-Q records (the LS50 and Q100 entries). This supersedes the
    round-29 CONFLICT row, which recorded a counting question rather than a contradicting source.
    `active` stays NOT_STATED: the sheet gives impedance, "Maximum Power Input" and binding posts only.

  kef-reference-1 — SoundStage! Hi-Fi review of the KEF Reference 1: "the newest version of KEF's Uni-Q
    driver array: a 1\\" aluminum-dome tweeter nestled into the center of an ideally shaped 5\\" aluminum cone
    for the midrange"; "Below the Uni-Q, and crossed over to it at 350Hz, is a 6.5\\" woofer"; and, of the
    listening, "the outputs of the Reference 1's three drivers coalesced as one". Three transducers.
    `active` stays NOT_STATED: the review describes binding posts and a recommended 50-200W, but it does not
    instruct the user to connect an external amplifier, so it does not meet an accepted evidence form.

  legacy-kef-4 (KEF Reference 105) — stereonomono reproduction of the KEF Reference Series brochure:
    "Three fine drive units are used in Model 105"; "The low frequency unit is a 300 mm (12\\") driver";
    "The 110 mm (5\\") mid range unit"; "The high frequency unit is a 52 mm (2\\") radiator". Three
    transducers. `active` stays NOT_STATED ("Amplifier Requirements: 40 watts minimum into 8 ohms" only).

  legacy-kef-1 (KEF Concord) — Radiomuseum model page: "Loudspeaker: 2 Loudspeakers"; "2-way hi-fi
    stand/floorstanding loudspeakers"; specification "Drive units: B139 bass unit (A6171), T15 tweeter
    (A6236)". Two transducers. The page also prints "Power type and voltage: No Power needed"; that is a
    database field rather than one of the three accepted `active: false` forms, so the value is recorded as
    SUPPORTED_NOT_PROMOTED for an owner decision instead of being promoted here.
"""
DATE = '2026-10-19'
ROUND = 29

ELAC = 'https://cdn.elac.com/uploads/2016/08/29132944/Uni-Fi-Sell-Sheet.pdf'
REF1 = 'https://www.soundstagehifi.com/index.php/equipment-reviews/807-kef-reference-1-loudspeakers'
KEF105 = 'https://stereonomono.blogspot.com/2010/08/kef-model-105.html'
CONCORD = 'https://www.radiomuseum.org/r/kef_concord_a6243.html'

ELAC_WHY = ('The sell sheet is ELAC-authored but is served from cdn.elac.com, an asset CDN rather than the '
            'product page, so manufacturer-host ownership of the document URL is not established.')
REF1_WHY = ('SoundStage! is an independent review publication; the review is not a KEF document.')
KEF105_WHY = ('The brochure text is reproduced by a hobby blog; no KEF-hosted copy of this 1970s brochure was '
              'opened.')
CONCORD_WHY = ('Radiomuseum is a volunteer equipment database; its model page is not a KEF publication.')

PROMOTIONS = [
    {'record': 'elac-uni-fi-ub5', 'field': 'driverCount', 'value': 3, 'source': ELAC,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'ELAC Uni-Fi series sell sheet, "Uni-Fi by Andrew Jones", UB5 specification column',
     'whyNotManufacturer': ELAC_WHY,
     'note': ('Round 29 (2026-10-19): ELAC Uni-Fi sell sheet — the UB5 column reads "3-way bass reflex", '
              '"Tweeter 1-inch soft dome", "Mid-Range 4-inch aluminum", "Woofer 5.25-inch aluminum". Three '
              'drive-unit rows: the concentric tweeter and 4-inch midrange count as two transducers, plus '
              'the 5.25-inch woofer.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified from the Uni-Fi sell sheet; the '
                     'concentric pair is counted as two transducers, the same convention as the KEF Uni-Q '
                     'records. active stays unresolved (impedance, maximum power input, binding posts).')},
    {'record': 'kef-reference-1', 'field': 'driverCount', 'value': 3, 'source': REF1,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'SoundStage! Hi-Fi, "KEF Reference 1 Loudspeakers" review by Doug Schneider (2014)',
     'whyNotManufacturer': REF1_WHY,
     'note': ('Round 29 (2026-10-19): SoundStage! review — "the newest version of KEF\'s Uni-Q driver array: '
              'a 1\\" aluminum-dome tweeter nestled into the center of an ideally shaped 5\\" aluminum cone for '
              'the midrange"; "Below the Uni-Q, and crossed over to it at 350Hz, is a 6.5\\" woofer"; and '
              '"the outputs of the Reference 1\'s three drivers coalesced as one". Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified from the SoundStage! review; active '
                     'stays unresolved because the review describes binding posts and a recommended 50-200W '
                     'without an amplifier-connection instruction.')},
    {'record': 'legacy-kef-4', 'field': 'driverCount', 'value': 3, 'source': KEF105,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KEF Reference Series Model 105 brochure text, reproduced by the stereonomono archive',
     'whyNotManufacturer': KEF105_WHY,
     'note': ('Round 29 (2026-10-19): KEF Model 105 brochure — "Three fine drive units are used in Model '
              '105"; "The low frequency unit is a 300 mm (12\\") driver"; "The 110 mm (5\\") mid range unit"; '
              '"The high frequency unit is a 52 mm (2\\") radiator". Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified from the KEF Model 105 brochure text; '
                     'active stays unresolved because the specification prints only "Amplifier Requirements: '
                     '40 watts minimum into 8 ohms".')},
    {'record': 'legacy-kef-1', 'field': 'driverCount', 'value': 2, 'source': CONCORD,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Radiomuseum model page, KEF Concord A6243 (ID 315059)', 'whyNotManufacturer': CONCORD_WHY,
     'note': ('Round 29 (2026-10-19): Radiomuseum page — "Drive units: B139 bass unit (A6171), T15 tweeter '
              '(A6236)"; "System type: Two-way, floor standing"; the technical block also lists "Loudspeaker: '
              '2 Loudspeakers". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified from the Radiomuseum model page; active '
                     'stays unresolved pending an owner decision on whether "Power type and voltage: No Power '
                     'needed" may count as passive evidence.')},
]

URL_RESULTS = [
    {'url': ELAC, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('UB5 column: "3-way bass reflex"; "Tweeter ... 1-inch soft dome"; "Mid-Range ... 4-inch '
                  'aluminum"; "Woofer ... 5.25-inch aluminum"; "Maximum Power Input ... 140 Watts"; "Binding '
                  'Posts ... 5-way custom metal".'),
     'fieldResults': [
         {'record': 'elac-uni-fi-ub5', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: three drive-unit rows; concentric pair counted as two.'},
         {'record': 'elac-uni-fi-ub5', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: impedance, power input and binding posts only.'},
     ]},
    {'url': REF1, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 2, 3], 'chunksTotal': 5,
     'evidence': ('"a 1\\" aluminum-dome tweeter nestled into the center of an ideally shaped 5\\" aluminum cone '
                  'for the midrange"; "Below the Uni-Q, and crossed over to it at 350Hz, is a 6.5\\" woofer"; '
                  '"the outputs of the Reference 1\'s three drivers coalesced as one".'),
     'fieldResults': [
         {'record': 'kef-reference-1', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: Uni-Q tweeter + midrange cone + 6.5 in woofer.'},
         {'record': 'kef-reference-1', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: binding posts and recommended amplifier power only.'},
     ]},
    {'url': KEF105, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 7,
     'evidence': ('"Three fine drive units are used in Model 105"; "300 mm (12\\") driver"; "110 mm (5\\") mid '
                  'range unit"; "52 mm (2\\") radiator"; "Amplifier Requirements: 40 watts minimum into 8 '
                  'ohms".'),
     'fieldResults': [
         {'record': 'legacy-kef-4', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: 12 in LF, 5 in midrange, 2 in HF.'},
         {'record': 'legacy-kef-4', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: amplifier-requirements figure only.'},
     ]},
    {'url': CONCORD, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('"Drive units: B139 bass unit (A6171), T15 tweeter (A6236)"; "Two-way, floor standing"; '
                  '"Loudspeaker: 2 Loudspeakers"; "Power type and voltage: No Power needed"; "Input '
                  'connections: Terminals".'),
     'fieldResults': [
         {'record': 'legacy-kef-1', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: B139 bass unit + T15 tweeter.'},
         {'record': 'legacy-kef-1', 'field': 'active', 'value': False, 'outcome': 'SUPPORTED_NOT_PROMOTED',
          'note': ('Round 29: "No Power needed" is an explicit no-supply statement but not one of the three '
                   'accepted forms in PROVENANCE-POLICY.md; flagged for an owner decision.')},
     ]},
]
