#!/usr/bin/env python3
"""Round 29 batch 48 (2026-10-19): KEF driver complements from three opened documents.

  legacy-kef-5 (KEF Q100) — Q series brochure, specification page: the Q100 column reads "Two-way bass
    reflex", "130mm (5.25in.) aluminium Uni-Q", "25mm (1in.) vented aluminium dome HF". The Uni-Q array is
    counted as its two transducers (mid/bass cone + concentric HF dome), the same convention used for the
    KEF LS50 record. The LF/ABR rows below belong to the Q600c/Q200c columns, which is why only the two
    Q100 lines are quoted. `active` stays NOT_STATED: the brochure prints "Amplifier N/A" and "Amplifier
    requirements 10 - 100W", and the installation manual's wiring pages extract as images, so no
    amplifier-connection instruction could be read.

  legacy-kef-7 (KEF Blade) — Blade owner's manual, specification page: "Uni-Q driver array: MF: 125mm (5in.)
    Li-Mg-Al/LCP hybrid cone HF: 25mm (1in.) Al dome; Bass units: LF: 4 x 225mm (9in.) with force
    cancelling" — six transducers. The connection page instructs "Single, Bi-Wire and Bi-Amp Connections"
    and says "KEF recommends that high quality speaker cable be used for connecting your Blade speakers":
    speaker-level wiring from external amplifiers, no mains inlet, so `active: false` is supportable.

  kef-reference-5 — Stereophile specification sidebar: "Uni-Q driver array with 1\" (25mm) vented
    aluminum-dome tweeter, 5\" (125mm) aluminum-cone midrange unit, four 6.5\" (165mm) aluminum-cone
    woofers" — six transducers. `active` stays NOT_STATED: the sidebar gives only "Recommended amplifier
    power: 50-400W".
"""
DATE = '2026-10-19'
ROUND = 29

Q100 = 'https://www.manualslib.com/manual/286175/Kef-Q100.html?page=12'
BLADE_SPEC = 'https://www.manualslib.com/manual/1412330/Kef-Blade.html?page=10'
BLADE_WIRE = 'https://www.manualslib.com/manual/1412330/Kef-Blade.html?page=9'
REF5 = 'https://www.stereophile.com/content/kef-reference-5-loudspeaker-specifications'

MANUALSLIB_WHY = ('The KEF document is mirrored by manualslib.com, a manual library, not a KEF host.')
STEREO_WHY = ('Stereophile is an independent review publication, not the manufacturer; the sidebar is its '
              'own transcription of the specification.')

PROMOTIONS = [
    {'record': 'legacy-kef-5', 'field': 'driverCount', 'value': 2, 'source': Q100,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KEF Q series brochure and specification sheet (manualslib copy), Q100 column',
     'whyNotManufacturer': MANUALSLIB_WHY,
     'note': ('Round 29 (2026-10-19): KEF Q series specification page — the Q100 column reads "Two-way bass '
              'reflex", "130mm (5.25in.) aluminium Uni-Q" and "25mm (1in.) vented aluminium dome HF". Two '
              'transducers: the Uni-Q mid/bass cone plus its concentric HF dome.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified from the Q series specification page; '
                     'active stays unresolved because the wiring pages of the installation manual extract as '
                     'images and the brochure prints only "Amplifier N/A" and an amplifier-requirements '
                     'figure.')},
    {'record': 'legacy-kef-7', 'field': 'driverCount', 'value': 6, 'source': BLADE_SPEC,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "KEF Blade owner's manual, specifications page (manualslib copy)",
     'whyNotManufacturer': MANUALSLIB_WHY,
     'note': ('Round 29 (2026-10-19): KEF Blade manual — "Uni-Q driver array: MF: 125mm (5in.) Li-Mg-Al /LCP '
              'hybrid cone HF: 25mm (1in.) Al dome; Bass units: LF: 4 x 225mm (9in.) with force cancelling". '
              'Two Uni-Q transducers plus four bass units.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 6 and active false verified from the Blade owner\'s '
                     'manual (specification page and "Single, Bi-Wire and Bi-Amp Connections").')},
    {'record': 'legacy-kef-7', 'field': 'active', 'value': False, 'source': BLADE_WIRE,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "KEF Blade owner's manual, 'Single, Bi-Wire and Bi-Amp Connections' page (manualslib copy)",
     'whyNotManufacturer': MANUALSLIB_WHY,
     'note': ('Round 29 (2026-10-19): same manual, connection page — the section is titled "Single, Bi-Wire '
              'and Bi-Amp Connections", the diagrams label HF/LF terminal pairs with LINK bars, and the text '
              'says "KEF recommends that high quality speaker cable be used for connecting your Blade '
              'speakers". Speaker-level wiring from external amplifiers; bi-amping only makes sense with '
              'external amplifier channels.'),
     'notesAppend': ''},
    {'record': 'kef-reference-5', 'field': 'driverCount', 'value': 6, 'source': REF5,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Stereophile, "KEF Reference 5 loudspeaker Specifications", Sidebar 1: Specifications',
     'whyNotManufacturer': STEREO_WHY,
     'note': ('Round 29 (2026-10-19): Stereophile sidebar — "Three-way, reflex-loaded, floorstanding '
              'loudspeaker. Drive-units: Uni-Q driver array with 1\\" (25mm) vented aluminum-dome tweeter, 5\\" '
              '(125mm) aluminum-cone midrange unit, four 6.5\\" (165mm) aluminum-cone woofers." Two Uni-Q '
              'transducers plus four woofers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 6 verified from the Stereophile specification '
                     'sidebar; active stays unresolved because the sidebar prints only "Recommended amplifier '
                     'power: 50-400W".')},
]

URL_RESULTS = [
    {'url': Q100, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1], 'chunksTotal': 3,
     'evidence': ('Q100 column: "Two-way bass reflex"; "130mm (5.25in.) aluminium Uni-Q"; "25mm (1in.) vented '
                  'aluminium dome HF"; "Amplifier N/A"; "Amplifier requirements 10 - 100W".'),
     'fieldResults': [
         {'record': 'legacy-kef-5', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: Uni-Q mid/bass cone + concentric HF dome.'},
         {'record': 'legacy-kef-5', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: "Amplifier N/A" plus an amplifier-requirements figure only; policy excludes.'},
     ]},
    {'url': BLADE_SPEC, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1], 'chunksTotal': 3,
     'evidence': ('"Uni-Q driver array: MF: 125mm (5in.) ... HF: 25mm (1in.) Al dome"; "Bass units: LF: 4 x '
                  '225mm (9in.) with force cancelling"; "Amplifier requirements 50 - 400W".'),
     'fieldResults': [
         {'record': 'legacy-kef-7', 'field': 'driverCount', 'value': 6, 'outcome': 'PROMOTED',
          'note': 'Round 29: MF + HF + four LF.'},
         {'record': 'legacy-kef-7', 'field': 'active', 'value': False, 'outcome': 'SUPPORTED_NOT_PROMOTED',
          'note': 'Round 29: promotion cites the connection page of the same manual instead.'},
     ]},
    {'url': BLADE_WIRE, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('Section "Single, Bi-Wire and Bi-Amp Connections"; HF/LF terminal pairs with LINK bars; '
                  '"KEF recommends that high quality speaker cable be used for connecting your Blade '
                  'speakers"; single / bi-wire / bi-amp diagrams.'),
     'fieldResults': [
         {'record': 'legacy-kef-7', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: speaker-cable wiring for single, bi-wire and bi-amp; external amplifiers.'},
     ]},
    {'url': REF5, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"Uni-Q driver array with 1\\" (25mm) vented aluminum-dome tweeter, 5\\" (125mm) '
                  'aluminum-cone midrange unit, four 6.5\\" (165mm) aluminum-cone woofers"; "Recommended '
                  'amplifier power: 50-400W"; no passive wording.'),
     'fieldResults': [
         {'record': 'kef-reference-5', 'field': 'driverCount', 'value': 6, 'outcome': 'PROMOTED',
          'note': 'Round 29: two Uni-Q transducers + four woofers.'},
         {'record': 'kef-reference-5', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: recommended amplifier power only.'},
     ]},
]
