#!/usr/bin/env python3
"""Round 29 batch 36 (2026-10-19): three third-party documents with explicit wording.

1. JBL 4350 — Audio Database entry (reputable database).
   "Method: 4-Way, 5-Speaker, Bass Reflex System"; "Units Used: Low band 38 cm cone (2230A) x2;
   Medium Low Band 30 cm cone (2202A); Middle and High Area horn (2440 + 2311 + 2308); High Pass ring
   type (2405)". Five transducers.
   "The network section is a multi-amplifier system divided at a crossover frequency of 250 Hz. In
   addition to the power amplifier, a divider 5231 or 5232 and a filter board ... are required." The
   loudspeaker has no built-in amplification: the power amplifier and divider are external items the
   user must supply.

2. Mackie HR824 — Sound On Sound review, November 1997 (third-party magazine).
   "a compact, two-way active nearfield monitor"; "uses a substantial 8.75-inch woofer ... complemented
   by a 1-inch, ferrofluid-cooled aluminium domed tweeter"; "The bass/mid power amplifier is rated at
   150W ... the tweeter is driven from a 100W amplifier". Two drivers, built-in amplification.

3. JBL EON15 — JBL specification document hosted by Warehouse Sound (dealer copy, third-party host).
   "The EON 15 is a 15 inch two-way passive speaker system that features the same advanced packaging and
   transducer technology used in the powered version."; "15 inch Two-way Speaker System"; 380 mm LF
   transducer + 44 mm (1-3/4 in) titanium compression driver; Neutrik Speakon input, 8 ohms.
"""
DATE = '2026-10-19'
ROUND = 29

AD_4350 = 'https://audio-database.com/JBL/speaker/4350.html'
SOS_HR824 = 'https://www.soundonsound.com/reviews/mackie-hr824'
WS_EON15 = 'https://www.warehousesound.com/r/jblEon15.pdf'

PROMOTIONS = [
    {'record': 'jbl-4350', 'field': 'driverCount', 'value': 5, 'source': AD_4350,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — JBL 4350/4350WX specification entry',
     'whyNotManufacturer': ('audio-database.com is a third-party specification archive; no JBL-hosted '
                            '4350 datasheet was opened in this session.'),
     'note': ('Round 29 (2026-10-19): Audio Database JBL 4350 entry — "Method: 4-Way, 5-Speaker, Bass '
              'Reflex System"; "Units Used: Low band: 38 cm cone type (2230A) x2 ... 30 cm cone type '
              '(2202A) ... Horn Type (2440 + 2311 + 2308) ... Ring Type (2405)". Five transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 5 and active false verified against the Audio '
                     'Database entry (5-speaker, multi-amplifier system with external power amplifier and '
                     'divider).')},
    {'record': 'jbl-4350', 'field': 'active', 'value': False, 'source': AD_4350,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — JBL 4350/4350WX specification entry',
     'whyNotManufacturer': ('audio-database.com is a third-party specification archive; no JBL-hosted '
                            '4350 datasheet was opened in this session.'),
     'note': ('Round 29 (2026-10-19): same entry — "The network section is a multi-amplifier system '
              'divided at a crossover frequency of 250 Hz. In addition to the power amplifier, a divider '
              '5231 or 5232 and a filter board ... are required." The power amplifier is an external item; '
              'the loudspeaker is not self-powered.'),
     'notesAppend': ''},
    {'record': 'mackie-hr824', 'field': 'driverCount', 'value': 2, 'source': SOS_HR824,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Sound On Sound, "Mackie HR824" review, November 1997, Paul White',
     'whyNotManufacturer': ('soundonsound.com is a magazine review; the original Mackie HR824 manual was '
                            'not served from a Mackie host in this session.'),
     'note': ('Round 29 (2026-10-19): Sound On Sound HR824 review — "a compact, two-way active nearfield '
              'monitor"; "uses a substantial 8.75-inch woofer ... complemented by a 1-inch, '
              'ferrofluid-cooled aluminium domed tweeter". Two drivers (the passive radiator is not a '
              'driven transducer).'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true verified against the Sound On '
                     'Sound review ("two-way active nearfield monitor").')},
    {'record': 'mackie-hr824', 'field': 'active', 'value': True, 'source': SOS_HR824,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Sound On Sound, "Mackie HR824" review, November 1997, Paul White',
     'whyNotManufacturer': ('soundonsound.com is a magazine review; no Mackie-hosted HR824 document was '
                            'served in this session.'),
     'note': ('Round 29 (2026-10-19): same review — "two-way active nearfield monitor"; "The bass/mid '
              'power amplifier is rated at 150W (350W burst power) and the tweeter is driven from a 100W '
              'amplifier"; "an EC mains inlet". Built-in amplification.'),
     'notesAppend': ''},
    {'record': 'jbl-eon15', 'field': 'driverCount', 'value': 2, 'source': WS_EON15,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'JBL EON15 specification document (JBL Professional; copy hosted by Warehouse Sound)',
     'whyNotManufacturer': ('The JBL document is served from warehousesound.com, a dealer host, not from a '
                            'JBL-owned URL.'),
     'note': ('Round 29 (2026-10-19): JBL EON15 specification sheet — "15 inch Two-way Speaker System"; '
              '"15 inch Differential Drive Low Frequency Transducer" and "1\\" Pure Titanium Diaphragm '
              'Compression Driver". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified against the JBL EON15 '
                     'specification sheet hosted at warehousesound.com.')},
    {'record': 'jbl-eon15', 'field': 'active', 'value': False, 'source': WS_EON15,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'JBL EON15 specification document (JBL Professional; copy hosted by Warehouse Sound)',
     'whyNotManufacturer': ('The JBL document is served from warehousesound.com, a dealer host, not from a '
                            'JBL-owned URL.'),
     'note': ('Round 29 (2026-10-19): same sheet — "The EON 15 is a 15 inch two-way passive speaker system '
              'that features the same advanced packaging and transducer technology used in the powered '
              'version." Neutrik Speakon input, 8 ohms, 250 W power handling.'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': AD_4350, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('JBL 4350: "4-Way, 5-Speaker, Bass Reflex System"; units: 2x 2230A, 2202A, 2440+2311+2308 '
                  'horn, 2405 ring tweeter; "multi-amplifier system divided at 250 Hz ... In addition to the '
                  'power amplifier, a divider 5231 or 5232 and a filter board ... are required".'),
     'fieldResults': [
         {'record': 'jbl-4350', 'field': 'driverCount', 'value': 5, 'outcome': 'PROMOTED',
          'note': 'Round 29: five enumerated transducers.'},
         {'record': 'jbl-4350', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external power amplifier and divider required; not self-powered.'},
     ]},
    {'url': SOS_HR824, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('Sound On Sound HR824 review: "compact, two-way active nearfield monitor"; 8.75-inch '
                  'woofer + 1-inch aluminium dome tweeter; bass/mid 150 W and tweeter 100 W amplifiers; '
                  'EC mains inlet.'),
     'fieldResults': [
         {'record': 'mackie-hr824', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two driven transducers named in the review.'},
         {'record': 'mackie-hr824', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "two-way active"; built-in amplifiers and mains inlet.'},
     ]},
    {'url': WS_EON15, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('JBL EON15 sheet: "15 inch Two-way Speaker System"; "The EON 15 is a 15 inch two-way '
                  'passive speaker system ..."; 380 mm LF transducer, 44 mm titanium compression driver, '
                  'Speakon input, 8 ohms.'),
     'fieldResults': [
         {'record': 'jbl-eon15', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two-way, two named transducers.'},
         {'record': 'jbl-eon15', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: explicit "passive speaker system".'},
     ]},
]
