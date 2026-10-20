#!/usr/bin/env python3
"""Round 29 batch 46 (2026-10-19): two JBL/Mackie documents mirrored by ManualsLib.

  legacy-mack-2 (Mackie HR624) — HR Series specification sheet: "The HR624 studio monitors are
    high-resolution, two-way, bi-amplified, active monitors employing a 6th-order Butterworth system with a
    built-in rear-firing mass-loaded passive radiator"; "a 1-inch aluminum-alloy high-frequency transducer,
    a high-precision 6.7-inch die-cast magnesium frame low-frequency transducer, and a 6-inch x 9-inch
    elliptical flat piston passive radiator"; "The system is composed of a single, compact cabinet with
    built-in control and amplifier electronics." Two driven transducers — the passive radiator is not a
    driven transducer and is not counted, matching the record note. Active: built-in amplifier electronics.

  jbl-vrx932 (JBL VRX932LA) — user's guide specification page: "1 x JBL 2262H 305 mm (12 in) Differential
    Drive® woofer" and "3 x JBL 2407J, 25.4 mm (1 in) voice-coil, neodymium magnet compression driver" —
    four transducers. "Crossover Modes: Bi-amp / passive, externally switchable"; the functional block
    diagram shows NL4 inputs with PASSIVE MODE / BI-AMP MODE switching and no mains inlet; power ratings are
    quoted "Passive: 800 W / 1600 W / 3200 W". External amplification in both modes.
"""
DATE = '2026-10-19'
ROUND = 29

MACKIE = 'https://www.manualslib.com/manual/293781/Mackie-Hr624.html'
VRX = 'https://www.manualslib.com/manual/79243/Jbl-Vrx932la.html?page=4'

WHY = ('The document is manufacturer-authored but is mirrored by manualslib.com, a manual library, not a '
       'manufacturer host.')

PROMOTIONS = [
    {'record': 'legacy-mack-2', 'field': 'driverCount', 'value': 2, 'source': MACKIE,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Mackie HR Series specification sheet for the HR624, "Active 2-Way Studio Monitor"',
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Mackie HR624 sheet — "a 1-inch aluminum-alloy high-frequency '
              'transducer, a high-precision 6.7-inch die-cast magnesium frame low-frequency transducer, and '
              'a 6-inch x 9-inch elliptical flat piston passive radiator in the back". Two driven '
              'transducers; the passive radiator is not an electrically driven driver and is not counted.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true verified from the HR624 '
                     'specification sheet ("two-way, bi-amplified, active monitors"; "built-in control and '
                     'amplifier electronics").')},
    {'record': 'legacy-mack-2', 'field': 'active', 'value': True, 'source': MACKIE,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Mackie HR Series specification sheet for the HR624, "Active 2-Way Studio Monitor"',
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same sheet — "The HR624 studio monitors are high-resolution, two-way, '
              'bi-amplified, active monitors"; "The system is composed of a single, compact cabinet with '
              'built-in control and amplifier electronics"; "The low-frequency amplifier is rated at 100 '
              'watts rms continuous output, and the high-frequency amplifier is rated at 40 watts rms".'),
     'notesAppend': ''},
    {'record': 'jbl-vrx932', 'field': 'driverCount', 'value': 4, 'source': VRX,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "JBL VRX932LA user's guide, specifications page",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): VRX932LA guide — "LF Driver: 1 x JBL 2262H 305 mm (12 in) Differential '
              'Drive® woofer with neodymium-magnet and dual voice-coils"; "HF Driver: 3 x JBL 2407J, 25.4 mm '
              '(1 in) voice-coil, neodymium magnet compression driver". One woofer plus three HF drivers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 4 and active false verified from the VRX932LA '
                     'guide ("Crossover Modes: Bi-amp / passive, externally switchable", NL4 inputs).')},
    {'record': 'jbl-vrx932', 'field': 'active', 'value': False, 'source': VRX,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "JBL VRX932LA user's guide, specifications page",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same guide — "Crossover Modes: Bi-amp / passive, externally '
              'switchable"; "Power Rating (Continuous/Program/Peak): Passive: 800 W / 1600 W / 3200 W"; the '
              'functional block diagram shows "NL4 INPUT" feeding "PASSIVE MODE" and "BI-AMP MODE" networks '
              'with no mains inlet. Both modes take external amplifier feeds.'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': MACKIE, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"two-way, bi-amplified, active monitors"; 1 in HF transducer + 6.7 in LF transducer + a '
                  'passive radiator; "built-in control and amplifier electronics".'),
     'fieldResults': [
         {'record': 'legacy-mack-2', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two driven transducers; passive radiator excluded.'},
         {'record': 'legacy-mack-2', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "active monitors" with built-in amplifiers.'},
     ]},
    {'url': VRX, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('"1 x JBL 2262H 305 mm (12 in)"; "3 x JBL 2407J, 25.4 mm (1 in)"; "Bi-amp / passive, '
                  'externally switchable"; NL4 inputs, no mains.'),
     'fieldResults': [
         {'record': 'jbl-vrx932', 'field': 'driverCount', 'value': 4, 'outcome': 'PROMOTED',
          'note': 'Round 29: one woofer + three compression drivers.'},
         {'record': 'jbl-vrx932', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: passive mode and externally switched bi-amp; no mains.'},
     ]},
]
