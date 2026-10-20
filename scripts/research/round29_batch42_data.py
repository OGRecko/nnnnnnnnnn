#!/usr/bin/env python3
"""Round 29 batch 42 (2026-10-19): retailer-hosted Electro-Voice documents and a Library of Congress
archive copy of the JBL 4310 manual.

  electro-voice-tx1122 — Full Compass listing titled
    "Electro-Voice Tour X TX1122 12\" 2-Way 90x50 500W Passive Loudspeaker, Black"; the specification list
    prints "LF Transducer: SMX2120", "HF Transducer: DH3", "Internal Crossover: Yes" and "Nominal
    Impedance (Passive): 8 Ohms". The title's "Passive Loudspeaker" is the explicit passive wording the
    policy accepts; two transducers are named. Both fields promoted.

  electro-voice-zx4 — Electro-Voice ZX4 engineering data sheet, Part Number 38110416 Rev D (12/2010),
    served from fullcompass.com: "EVS15-SF 15\" LF Transducer" and "DH3 1.25\" Voice Coil, 1\" Exit
    Compression Driver", i.e. two transducers. The sheet shows a block diagram with an "HPF PASSIVE
    LIMITER" and Speakon inputs and lists an external "CP2200, 120V Power Amplifier" under Performance
    Match, but it never calls the system passive and gives no connection instruction, so `active` is
    NOT_STATED (power handling and connectors are not evidence under the policy).

  jbl-4310 — JBL Professional Series Model 4310 manual, hosted by the Library of Congress:
    "The loudspeaker system shall consist of three direct-radiator transducers and frequency dividing
    network installed in a tube-ported enclosure", plus a 12-inch LF, 5-inch midrange and 1-3/4-inch
    ultra-high transducer described in the component section. Three transducers. `active` is NOT_STATED:
    the manual prints only "Power capacity 50 watts program" and the presence of a dividing network.

  jbl-4311 — jblpro.com information page re-read: "Components: 300-mm (12-in), long excursion, low
    frequency loudspeaker; 130-mm (5-in) midrange loudspeaker; 36-mm (1.4-in) high frequency direct
    radiator". driverCount is already MANUFACTURER_VERIFIED. `active` stays NOT_STATED: the page gives
    "Power Capacity 75 W continuous program" and a "frequency dividing network", never the word passive.
"""
DATE = '2026-10-19'
ROUND = 29

TX1122 = ('https://www.fullcompass.com/prod/133348-electro-voice-tx1122-tour-x-12-2-way-90-x-50-500w-'
          'passive-loudspeaker-black')
ZX4 = 'https://www.fullcompass.com/common/files/19733-ElectroVoiceZX4Datasheet.pdf'
JBL4310 = ('https://tile.loc.gov/storage-services/master/mbrs/recording_preservation/manuals/JBL%20Prof.%20'
           'Series%20Model%204310%20Control%20Room%20Monitor.pdf')
JBL4311 = 'https://jblpro.com/en-US/site_elements/4311-information'

TX1122_WHY = ('The listing is served from fullcompass.com, a retailer, not from an Electro-Voice host; the '
              'manufacturer page for this legacy model was not opened.')
ZX4_WHY = ('The data sheet is manufacturer-authored (Part Number 38110416 Rev D) but is served from '
           'fullcompass.com, a retailer, so the manufacturer-host requirement is not met.')
JBL4310_WHY = ('The JBL manual is served from tile.loc.gov (Library of Congress), an archive rather than a '
               'JBL host.')

PROMOTIONS = [
    {'record': 'electro-voice-tx1122', 'field': 'driverCount', 'value': 2, 'source': TX1122,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing, 'Electro-Voice Tour X TX1122 12\" 2-Way 90x50 500W Passive "
                 "Loudspeaker, Black', MFR # F.01U.302.272",
     'whyNotManufacturer': TX1122_WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX1122 listing — "LF Transducer: SMX2120" and "HF '
              'Transducer: DH3"; the overview calls them "EV\'s SMX woofers" driving a two-way system. Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Full Compass '
                     'listing, whose title reads "Passive Loudspeaker" and whose spec list prints "Internal '
                     'Crossover: Yes".')},
    {'record': 'electro-voice-tx1122', 'field': 'active', 'value': False, 'source': TX1122,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing, 'Electro-Voice Tour X TX1122 12\" 2-Way 90x50 500W Passive "
                 "Loudspeaker, Black', MFR # F.01U.302.272",
     'whyNotManufacturer': TX1122_WHY,
     'note': ('Round 29 (2026-10-19): same listing — the product name is "Electro-Voice Tour X TX1122 12\\" '
              '2-Way 90x50 500W Passive Loudspeaker, Black", and the specification list prints "Internal '
              'Crossover: Yes" with "Nominal Impedance (Passive): 8 Ohms". Explicit passive wording.'),
     'notesAppend': ''},
    {'record': 'electro-voice-zx4', 'field': 'driverCount', 'value': 2, 'source': ZX4,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Electro-Voice Zx4 engineering data sheet, Part Number 38110416 Rev D (12/2010)',
     'whyNotManufacturer': ZX4_WHY,
     'note': ('Round 29 (2026-10-19): EV Zx4 data sheet — "LF Transducer: EVS15-SF, 15 in (381mm) Driver" '
              'and "HF Transducer: DH3, 1 in (25.4mm) exit Compression Driver"; crossover 1.5 kHz. Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified from the Zx4 data sheet; active stays '
                     'unresolved because the sheet gives power handling and Speakon connectors but no '
                     'passive statement or amplifier-connection instruction.')},
    {'record': 'jbl-4310', 'field': 'driverCount', 'value': 3, 'source': JBL4310,
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'JBL Professional Series Model 4310 control room monitor manual (architectural '
                 'specifications)',
     'whyNotManufacturer': JBL4310_WHY,
     'note': ('Round 29 (2026-10-19): JBL 4310 manual — "The loudspeaker system shall consist of three '
              'direct-radiator transducers and frequency dividing network installed in a tube-ported '
              'enclosure"; the component section describes the 12-inch woofer, the 5-inch midrange '
              'transducer and the 1-3/4-inch ultra-high frequency transducer. Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified from the JBL 4310 manual (Library of '
                     'Congress copy); active stays unresolved because the manual prints only a power-capacity '
                     'rating and a dividing network.')},
]

URL_RESULTS = [
    {'url': TX1122, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('Title "Passive Loudspeaker"; "LF Transducer: SMX2120"; "HF Transducer: DH3"; "Internal '
                  'Crossover: Yes"; "Nominal Impedance (Passive): 8 Ohms"; 500/1000/2000 W handling.'),
     'fieldResults': [
         {'record': 'electro-voice-tx1122', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: LF SMX2120 + HF DH3.'},
         {'record': 'electro-voice-tx1122', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: title says "Passive Loudspeaker"; internal passive crossover.'},
     ]},
    {'url': ZX4, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('"EVS15-SF, 15 in (381mm) Driver"; "DH3, 1 in (25.4mm) exit Compression Driver"; block '
                  'diagram shows "HPF PASSIVE LIMITER"; Speakon NL4 inputs; no passive sentence.'),
     'fieldResults': [
         {'record': 'electro-voice-zx4', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: 15 in LF + DH3 HF.'},
         {'record': 'electro-voice-zx4', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: no passive wording or amplifier-connection instruction.'},
     ]},
    {'url': JBL4310, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1], 'chunksTotal': 2,
     'evidence': ('"three direct-radiator transducers and frequency dividing network"; 12 in woofer, 5 in '
                  'midrange, 1-3/4 in ultra-high transducer; "Power capacity 50 watts program".'),
     'fieldResults': [
         {'record': 'jbl-4310', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: three transducers enumerated.'},
         {'record': 'jbl-4310', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: power capacity and dividing network only.'},
     ]},
    {'url': JBL4311, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1], 'chunksTotal': 2,
     'evidence': ('"300-mm (12-in), long excursion, low frequency loudspeaker; 130-mm (5-in) midrange '
                  'loudspeaker; 36-mm (1.4-in) high frequency direct radiator"; "Power Capacity 75 W '
                  'continuous program"; no passive wording.'),
     'fieldResults': [
         {'record': 'jbl-4311', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: the page never states passive; the value stays unverified.'},
     ]},
]
