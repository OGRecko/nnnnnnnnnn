#!/usr/bin/env python3
"""Round 29 batch 45 (2026-10-19): two powered monitors with explicit "self-powered"/"Powered: Yes" text.

  fostex-6301b — Fostex Model 6301B Personal Monitor owner's manual (printed May 2004), hosted by
    tcfurlong.com: the cover reads "PERSONAL MONITOR Self-Powered"; the specification block prints
    "Speaker section Type 10cm full range single cone" and "Amplifier section (EXT SP jack) Output Higher
    than 10W RMS (8Ω load)" with "Mains power 120VAC 60Hz (USA/Canada) 33W". One transducer, built-in
    amplification and a mains inlet.

  kali-lp6 — Kali Audio LP-6 (Project Lone Pine) user manual, served from the Kali Squarespace CDN:
    "Powered: Yes", "Amplifier Class: D", "Power Configuration: Bi-Amped", "LF Driver: 6.5\" Woofer",
    "HF Driver: 1\" Soft Dome Tweeter", and "Power AC -100-240V 50/60Hz". Two transducers, active.
"""
DATE = '2026-10-19'
ROUND = 29

FOSTEX = 'https://tcfurlong.com/wp-content/uploads/Fostex-6301B-Rental-Manual.pdf'
KALI = ('https://static1.squarespace.com/static/5a6a2d73bff200e7e9dde1f9/t/5b5b68456d2a73ca7faa5fbd/'
        '1532717141711/LP-6+User%27s+Manual.pdf')

FOSTEX_WHY = ('The manual is Fostex-authored but is served by tcfurlong.com, a rental house, not by a Fostex '
              'host.')
KALI_WHY = ('The manual is served from the Squarespace asset CDN rather than the kaliaudio.com domain, so '
            'manufacturer-host ownership cannot be established from the URL alone.')

PROMOTIONS = [
    {'record': 'fostex-6301b', 'field': 'driverCount', 'value': 1, 'source': FOSTEX,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Fostex Model 6301B Personal Monitor owner's manual (Fostex, printed May 2004)",
     'whyNotManufacturer': FOSTEX_WHY,
     'note': ('Round 29 (2026-10-19): Fostex 6301B manual — "Speaker section Type 10cm full range single '
              'cone"; "Frequency range 80Hz ~ 13kHz". One full-range transducer, no separate HF device.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 1 and active true verified from the 6301B manual '
                     '("PERSONAL MONITOR Self-Powered", "Mains power 120VAC 60Hz").')},
    {'record': 'fostex-6301b', 'field': 'active', 'value': True, 'source': FOSTEX,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Fostex Model 6301B Personal Monitor owner's manual (Fostex, printed May 2004)",
     'whyNotManufacturer': FOSTEX_WHY,
     'note': ('Round 29 (2026-10-19): same manual — the cover reads "PERSONAL MONITOR Self-Powered", the '
              'specification lists an "Amplifier section (EXT SP jack) Output Higher than 10W RMS (8Ω load)" '
              'and "Mains power 120VAC 60Hz (USA/Canada) 33W". Built-in amplification.'),
     'notesAppend': ''},
    {'record': 'kali-lp6', 'field': 'driverCount', 'value': 2, 'source': KALI,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Kali Audio LP-6 User Manual (Project Lone Pine), 'Full Specifications' table",
     'whyNotManufacturer': KALI_WHY,
     'note': ('Round 29 (2026-10-19): Kali LP-6 manual — "LF Driver: 6.5\\" Woofer", "HF Driver: 1\\" Soft '
              'Dome Tweeter", "Crossover: 1.5 kHz". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true verified from the LP-6 manual '
                     '("Powered: Yes", "Amplifier Class: D", "Power AC -100-240V 50/60Hz").')},
    {'record': 'kali-lp6', 'field': 'active', 'value': True, 'source': KALI,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Kali Audio LP-6 User Manual (Project Lone Pine), 'Full Specifications' table",
     'whyNotManufacturer': KALI_WHY,
     'note': ('Round 29 (2026-10-19): same manual — the specification table opens "Powered: Yes", then '
              '"Amplifier Class: D", "Power Configuration: Bi-Amped", "LF Power: 40 W", "HF Power: 40 W"; '
              'the rear panel is labelled "Power AC -100-240V 50/60Hz".'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': FOSTEX, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"PERSONAL MONITOR Self-Powered"; "Speaker section Type 10cm full range single cone"; '
                  '"Amplifier section (EXT SP jack) Output Higher than 10W RMS"; "Mains power 120VAC 60Hz".'),
     'fieldResults': [
         {'record': 'fostex-6301b', 'field': 'driverCount', 'value': 1, 'outcome': 'PROMOTED',
          'note': 'Round 29: one 10 cm full-range cone.'},
         {'record': 'fostex-6301b', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "Self-Powered", mains power and amplifier section.'},
     ]},
    {'url': KALI, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0, 1], 'chunksTotal': 3,
     'evidence': ('"Powered: Yes"; "Amplifier Class: D"; "Power Configuration: Bi-Amped"; "LF Driver: 6.5\\" '
                  'Woofer"; "HF Driver: 1\\" Soft Dome Tweeter"; "Power AC -100-240V 50/60Hz".'),
     'fieldResults': [
         {'record': 'kali-lp6', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: 6.5 in woofer + 1 in soft dome.'},
         {'record': 'kali-lp6', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "Powered: Yes", bi-amped class D.'},
     ]},
]
