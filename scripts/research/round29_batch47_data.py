#!/usr/bin/env python3
"""Round 29 batch 47 (2026-10-19): two Stereophile specification sidebars — driver complement only.

  harbeth-shl5 — Stereophile's Super HL5 plus specification sidebar: "Three-way, reflex-loaded,
    stand-mounted loudspeaker. Drive-units: 0.78\" (20mm) titanium-dome and 1\" (25mm) aluminum-dome
    tweeters; 7.8\" (200mm) polymeric composite-cone mid/woofer." Three drive units.

  snell-typeAIII — Stereophile's Snell Type A specification sidebar (A/III column): "Three-way dynamic,
    acoustic-suspension loudspeaker. Drive-units: 10\" cone-woofer, 4\" midrange, 1\" soft-dome tweeter,
    rear-firing supertweeter (A/III)." Four drive units.

Both pages print only impedance and sensitivity, never passive or powered wording, so `active` stays
NOT_STATED in both records; only the driver counts are promoted.
"""
DATE = '2026-10-19'
ROUND = 29

HARBETH = 'https://www.stereophile.com/content/harbeth-super-hl5plus-loudspeaker-specifications'
SNELL = 'https://www.stereophile.com/content/snell-type-loudspeaker-specifications'

WHY = ('Stereophile is an independent review publication, not the manufacturer; the sidebar is its own '
       'transcription of the manufacturer specification.')

PROMOTIONS = [
    {'record': 'harbeth-shl5', 'field': 'driverCount', 'value': 3, 'source': HARBETH,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Stereophile, "Harbeth Super HL5 plus loudspeaker Specifications", Sidebar 1: Specifications',
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Stereophile sidebar — "Three-way, reflex-loaded, stand-mounted '
              'loudspeaker. Drive-units: 0.78\\" (20mm) titanium-dome and 1\\" (25mm) aluminum-dome tweeters; '
              '7.8\\" (200mm) polymeric composite-cone mid/woofer." Three drive units.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified from the Stereophile specification '
                     'sidebar; active stays unresolved because the sidebar prints only impedance and '
                     'sensitivity.')},
    {'record': 'snell-typeAIII', 'field': 'driverCount', 'value': 4, 'source': SNELL,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Stereophile, "Snell Type A loudspeaker Specifications", Sidebar 2: Specifications',
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Stereophile sidebar — "Three-way dynamic, acoustic-suspension '
              'loudspeaker. Drive-units: 10\\" cone-woofer, 4\\" midrange, 1\\" soft-dome tweeter, '
              'rear-firing supertweeter (A/III)." Four drive units for the A/III.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 4 verified from the Stereophile specification '
                     'sidebar; active stays unresolved because the sidebar prints only impedance and '
                     'sensitivity.')},
]

URL_RESULTS = [
    {'url': HARBETH, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"Three-way, reflex-loaded, stand-mounted loudspeaker"; "0.78\\" (20mm) titanium-dome and '
                  '1\\" (25mm) aluminum-dome tweeters; 7.8\\" (200mm) ... mid/woofer"; no passive wording.'),
     'fieldResults': [
         {'record': 'harbeth-shl5', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: two tweeters + mid/woofer.'},
         {'record': 'harbeth-shl5', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: impedance and sensitivity only.'},
     ]},
    {'url': SNELL, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"Three-way dynamic, acoustic-suspension loudspeaker"; "10\\" cone-woofer, 4\\" midrange, '
                  '1\\" soft-dome tweeter, rear-firing supertweeter (A/III)"; no passive wording.'),
     'fieldResults': [
         {'record': 'snell-typeAIII', 'field': 'driverCount', 'value': 4, 'outcome': 'PROMOTED',
          'note': 'Round 29: woofer, midrange, tweeter, supertweeter.'},
         {'record': 'snell-typeAIII', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: impedance and sensitivity only.'},
     ]},
]
