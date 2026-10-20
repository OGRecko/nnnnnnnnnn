#!/usr/bin/env python3
"""Round 29 batch 40 (2026-10-19): Sonus faber manuals on manualslib (aggregator copy of the manufacturer
owner's manual). These are the fields demoted earlier today by the MV host audit; the evidence is now read
from the pages and promoted under the third-party tier instead.

Homage Tradition manual (page header on every page: "Homage tradition passive loudspeakers"):
  AMATI     "3.5 way floorstanding loudspeaker system" — H28 XTR-04 28 mm tweeter, M15 XTR-04 150 mm
            midrange, 2 x W22XTR-08 220 mm woofers = 4 transducers (page 29).
  GUARNERI  "2 way stand mount loudspeaker system" — H28 XTR-04 tweeter, W15 XTR-04 150 mm midwoofer
            = 2 transducers (page 30).
  SERAFINO  "3.5 way floorstanding loudspeaker system" — H28 XTR-04 tweeter, M15 XTR-04 midrange,
            2 x W18XTR-08 180 mm woofers = 4 transducers (page 30).

Olympica Nova manual (technical specifications pages 42–43; connection chapter page 20):
  Nova I     "2 way ... stand mount" — H28 XTR3 tweeter + MW15 XTR2-04 150 mm driver = 2.
  Nova II    "3 way ... floorstanding" — H28 + M15 + W18XTR2-04 = 3.
  Nova III   "3 way ... floorstanding" — H28 + M15 + 2 x W18XTR2-08 = 4.
  Nova V     "3 way ... floorstanding" — H28 + M15 + 3 x W18XTR2-12 = 5.
  Passive evidence: "Use a single stereo amplifier or two mono amplifiers and a pair of power cables" and the
  bi-wiring/bi-amping sections, which drive the loudspeaker from external amplifiers only; no mains inlet is
  described for any model.
"""
DATE = '2026-10-19'
ROUND = 29

HOMAGE_P29 = 'https://www.manualslib.com/manual/1290952/Sonus-Faber-Serafino-Tradition.html?page=29#manual'
HOMAGE_P30 = 'https://www.manualslib.com/manual/1290952/Sonus-Faber-Serafino-Tradition.html?page=30#manual'
OLYMPICA_P42 = 'https://www.manualslib.com/manual/1744876/Sonus-Faber-Olympica-Nova.html?page=42#manual'
OLYMPICA_P43 = 'https://www.manualslib.com/manual/1744876/Sonus-Faber-Olympica-Nova.html?page=43#manual'
OLYMPICA_P20 = 'https://www.manualslib.com/manual/1744876/Sonus-Faber-Olympica-Nova.html?page=20'

HOMAGE_DOC = "Sonus faber Homage Tradition owner's manual (manualslib copy), technical specifications"
OLYMPICA_DOC = "Sonus faber Olympica Nova owner's manual (manualslib copy), technical specifications"

_HOMAGE_WHY = ('The manual is a Sonus faber publication, but the retained copy is served by manualslib.com, '
               'a document aggregator, not by a Sonus faber host.')
_OLYMPICA_WHY = ('The manual is a Sonus faber publication, but the retained copy is served by manualslib.com, '
                 'a document aggregator, not by a Sonus faber host.')

PROMOTIONS = [
    {'record': 'sonus-faber-homage-tradition-amati', 'field': 'driverCount', 'value': 4,
     'source': HOMAGE_P29, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): Homage Tradition manual, page 29 — "3.5 way floorstanding loudspeaker '
              'system"; "H28 XTR-04 ... 28 mm" tweeter, "M15 XTR-04 ... 150 mm" midrange, "2 x W22XTR-08 ... '
              '220 mm" woofers. Four transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 4 and active false re-verified from the Homage '
                     'Tradition manual pages 29-30 (manualslib copy); promoted under the third-party tier.')},
    {'record': 'sonus-faber-homage-tradition-amati', 'field': 'active', 'value': False,
     'source': HOMAGE_P29, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): Homage Tradition manual — every page is headed "Homage tradition '
              'passive loudspeakers"; the specification table gives "Suggested Amplifier Power Output" and '
              'the connection chapter drives the speakers from external amplifiers.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-homage-tradition-guarneri', 'field': 'driverCount', 'value': 2,
     'source': HOMAGE_P30, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): Homage Tradition manual, page 30, GUARNERI column — "2 way stand mount '
              'loudspeaker system"; "H28 XTR-04 ... 28 mm" tweeter and "W15 XTR-04 ... 150 mm" midwoofer. '
              'Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false re-verified from the Homage '
                     'Tradition manual pages 29-30 (manualslib copy).')},
    {'record': 'sonus-faber-homage-tradition-guarneri', 'field': 'active', 'value': False,
     'source': HOMAGE_P30, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): same manual — page header "Homage tradition passive loudspeakers"; the '
              'GUARNERI column lists only a "Suggested Amplifier Power Output" of 30-250 W.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-homage-tradition-serafino', 'field': 'driverCount', 'value': 4,
     'source': HOMAGE_P30, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): Homage Tradition manual, page 30, SERAFINO column — "3.5 way '
              'floorstanding loudspeaker system"; H28 XTR-04 tweeter, M15 XTR-04 midrange, "2 x W18XTR-08 ... '
              '180 mm" woofers. Four transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 4 and active false re-verified from the Homage '
                     'Tradition manual pages 29-30 (manualslib copy).')},
    {'record': 'sonus-faber-homage-tradition-serafino', 'field': 'active', 'value': False,
     'source': HOMAGE_P30, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': HOMAGE_DOC, 'whyNotManufacturer': _HOMAGE_WHY,
     'note': ('Round 29 (2026-10-19): same manual — "Homage tradition passive loudspeakers"; SERAFINO column '
              'gives "Suggested Amplifier Power Output" 80-350 W.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-olympica-nova-i', 'field': 'driverCount', 'value': 2,
     'source': OLYMPICA_P43, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): Olympica Nova manual, page 43, Olympica Nova I column — "2 way, full '
              'para-aperiodic vented box ... stand mount loudspeaker system"; "H28 XTR3 ... 28 mm" tweeter '
              'and "MW15 XTR2-04, 150mm" driver. Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Olympica Nova '
                     'manual (technical specifications and connection chapter, manualslib copy).')},
    {'record': 'sonus-faber-olympica-nova-i', 'field': 'active', 'value': False,
     'source': OLYMPICA_P20, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): Olympica Nova manual, page 20 "3.4.1 Standard connection" — "Use a '
              'single stereo amplifier or two mono amplifiers and a pair of power cables"; the bi-wiring and '
              'bi-amping sections add external amplifiers. No mains inlet is described for the loudspeaker.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-olympica-nova-ii', 'field': 'driverCount', 'value': 3,
     'source': OLYMPICA_P43, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): Olympica Nova manual, page 43, Olympica Nova II column — "3 way ... '
              'floorstanding loudspeaker system"; "H28 XTR3" tweeter, "M15 XTR2-04, 150mm" midrange, '
              '"W18XTR2-04" woofer. Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 and active false verified from the Olympica Nova '
                     'manual (manualslib copy).')},
    {'record': 'sonus-faber-olympica-nova-ii', 'field': 'active', 'value': False,
     'source': OLYMPICA_P20, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): same manual, page 20 — "Use a single stereo amplifier or two mono '
              'amplifiers and a pair of power cables"; bi-amping section uses external amplifiers only.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-olympica-nova-iii', 'field': 'driverCount', 'value': 4,
     'source': OLYMPICA_P42, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): Olympica Nova manual, page 42, Olympica Nova III column — "3 way ... '
              'floorstanding"; "H28 XTR3" tweeter, "M15 XTR2-04, 150mm" midrange, "2 x W18XTR2-08 cone '
              'drivers". Four transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 4 and active false verified from the Olympica Nova '
                     'manual (manualslib copy).')},
    {'record': 'sonus-faber-olympica-nova-iii', 'field': 'active', 'value': False,
     'source': OLYMPICA_P20, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): same manual, page 20 — "Use a single stereo amplifier or two mono '
              'amplifiers and a pair of power cables"; bi-wiring and bi-amping are described with external '
              'amplifiers only.'),
     'notesAppend': ''},
    {'record': 'sonus-faber-olympica-nova-v', 'field': 'driverCount', 'value': 5,
     'source': OLYMPICA_P42, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): Olympica Nova manual, page 42, Olympica Nova V column — "3 way ... '
              'floorstanding"; "H28 XTR3" tweeter, "M15 XTR2-04" midrange, "3 x W18XTR2-12 cone drivers". '
              'Five transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 5 and active false verified from the Olympica Nova '
                     'manual (manualslib copy).')},
    {'record': 'sonus-faber-olympica-nova-v', 'field': 'active', 'value': False,
     'source': OLYMPICA_P20, 'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': OLYMPICA_DOC, 'whyNotManufacturer': _OLYMPICA_WHY,
     'note': ('Round 29 (2026-10-19): same manual, page 20 — "Use a single stereo amplifier or two mono '
              'amplifiers and a pair of power cables"; no built-in amplification is described.'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': HOMAGE_P29, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [1], 'chunksTotal': 3,
     'evidence': ('Homage Tradition manual p.29: header "Homage tradition passive loudspeakers"; AMATI '
                  '"3.5 way floorstanding"; H28 28 mm tweeter, M15 150 mm midrange, 2 x W22XTR-08 220 mm '
                  'woofers.'),
     'fieldResults': [
         {'record': 'sonus-faber-homage-tradition-amati', 'field': 'driverCount', 'value': 4,
          'outcome': 'PROMOTED', 'note': 'Round 29: four enumerated transducers; manualslib copy.'},
         {'record': 'sonus-faber-homage-tradition-amati', 'field': 'active', 'value': False,
          'outcome': 'PROMOTED', 'note': 'Round 29: page header "Homage tradition passive loudspeakers".'},
     ]},
    {'url': HOMAGE_P30, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0, 1], 'chunksTotal': 3,
     'evidence': ('Homage Tradition manual p.30: GUARNERI "2 way stand mount", H28 + W15 150 mm; SERAFINO '
                  '"3.5 way floorstanding", H28 + M15 + 2 x W18XTR-08 180 mm.'),
     'fieldResults': [
         {'record': 'sonus-faber-homage-tradition-guarneri', 'field': 'driverCount', 'value': 2,
          'outcome': 'PROMOTED', 'note': 'Round 29: two enumerated transducers.'},
         {'record': 'sonus-faber-homage-tradition-guarneri', 'field': 'active', 'value': False,
          'outcome': 'PROMOTED', 'note': 'Round 29: "Homage tradition passive loudspeakers".'},
         {'record': 'sonus-faber-homage-tradition-serafino', 'field': 'driverCount', 'value': 4,
          'outcome': 'PROMOTED', 'note': 'Round 29: four enumerated transducers.'},
         {'record': 'sonus-faber-homage-tradition-serafino', 'field': 'active', 'value': False,
          'outcome': 'PROMOTED', 'note': 'Round 29: "Homage tradition passive loudspeakers".'},
     ]},
    {'url': OLYMPICA_P42, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [1], 'chunksTotal': 4,
     'evidence': ('Olympica Nova manual p.42: Nova V "3 way ... floorstanding" H28 + M15 + 3 x W18XTR2-12; '
                  'Nova III "3 way ..." H28 + M15 + 2 x W18XTR2-08.'),
     'fieldResults': [
         {'record': 'sonus-faber-olympica-nova-iii', 'field': 'driverCount', 'value': 4, 'outcome': 'PROMOTED',
          'note': 'Round 29: four enumerated transducers.'},
         {'record': 'sonus-faber-olympica-nova-v', 'field': 'driverCount', 'value': 5, 'outcome': 'PROMOTED',
          'note': 'Round 29: five enumerated transducers.'},
     ]},
    {'url': OLYMPICA_P43, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [1], 'chunksTotal': 3,
     'evidence': ('Olympica Nova manual p.43: Nova I "2 way ... stand mount" H28 + MW15 150 mm; Nova II '
                  '"3 way ... floorstanding" H28 + M15 + W18XTR2-04.'),
     'fieldResults': [
         {'record': 'sonus-faber-olympica-nova-i', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two enumerated transducers.'},
         {'record': 'sonus-faber-olympica-nova-ii', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: three enumerated transducers.'},
     ]},
    {'url': OLYMPICA_P20, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [1], 'chunksTotal': 3,
     'evidence': ('Olympica Nova manual p.20: "Use a single stereo amplifier or two mono amplifiers and a '
                  'pair of power cables"; bi-wiring and bi-amping sections; no mains inlet described.'),
     'fieldResults': [
         {'record': 'sonus-faber-olympica-nova-i', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external amplifier connection instructions.'},
         {'record': 'sonus-faber-olympica-nova-ii', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external amplifier connection instructions.'},
         {'record': 'sonus-faber-olympica-nova-iii', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external amplifier connection instructions.'},
         {'record': 'sonus-faber-olympica-nova-v', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external amplifier connection instructions.'},
     ]},
]
