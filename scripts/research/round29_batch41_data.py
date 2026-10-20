#!/usr/bin/env python3
"""Round 29 batch 41 (2026-10-19): aggregator-hosted manufacturer documents with explicit wording.

  Tannoy System 600 (manualzz copy of the Tannoy manual):
    "Using an advanced Dual Concentric 6.5\" driver"; the servicing chapter separates "The HF unit" and
    "The LF unit" ("The HF unit may be fitted with a new diaphragm assembly", "The LF unit may be re-coned
    in the normal way"), i.e. two transducers in one Dual Concentric chassis. The connection chapter says
    the terminals "must be connected to the red or positive terminal on the power amplifier", and a
    "Power amplifiers" chapter matches amplifier power to the speaker: passive.
    (The separate System 600a model is a different, active product and is not this record.)

  Spendor SP-100 (manualmachine copy of the Spendor owner's manual):
    "Low Frequency unit Spendor 300mm Bextrene", "Mid Frequency unit Spendor 160mm Homopolymer
    Polypropylene", "High Frequency unit 19mm Soft Dome" = 3 transducers. The wiring chapter instructs the
    user to connect the terminals to the amplifier's channels and describes bi-/tri-wiring: passive.

  KEF LS3/5A (manualsnet copy of the KEF Reference Series sheet):
    "This ultra compact system used the KEF B110 and T27 bass and treble units"; "Drive units B110
    bass/midrange unit (SP1228), and T27 tweeter (SP1032)" = 2 transducers. Only "Amplifier requirements
    25-75W (into 8 ohms)" is printed, which the policy excludes as passive evidence: active NOT_STATED.

  Meyer MJF-212 (Sound & Video Contractor announcement, 2007):
    "a self-powered stage monitor loudspeaker"; "high-frequency section comprises a 4in. diaphragm
    compression driver"; "A pair of high-power 12in. neodymium magnet cone drivers"; "Each of the drivers is
    powered by one channel of a 3-channel class AB/H amplifier" = 3 transducers, active.

  Electro-Voice Sentry 500 (manualzz copy of the EV data sheet):
    "The low-frequency section of the Sentry 500 is a 12-inch direct radiator woofer" plus the Super-Dome
    tweeter = 2 transducers. "The integral crossover network is a 12-dB/octave type"; "Bi-amplification is
    easily accomplished ... Woofer and tweeter input connections are then made on the system input board";
    "amplifiers as large as 400 watts can be used": passive.

  Electro-Voice Sx100+ (manualzz copy of the EV data sheet, Rev E 7/2006):
    "LF Transducer: 12\" (300mm)", "HF Transducer: 1\" (25mm) exit DH3 Comp. Driver" = 2 transducers.
    The sheet gives only power handling and Speakon connectors, no passive/active wording: active
    NOT_STATED.

  dB Technologies Opera 405 (manualslib, Opera Live manual page 6): the specification table's four model
  columns (202/205/402/405) do not extract in a column-aligned way, so no model-specific quote for the 405
  could be read. Recorded NOT_EXTRACTED for both fields; the values stay untouched.
"""
DATE = '2026-10-19'
ROUND = 29

TANNOY = 'https://www.manualzz.com/doc/2104058/tannoy-system-600-near-field-reference-monitor-user-manual'
SPENDOR = 'https://manualmachine.com/spendor/sp100/2351828-owners-manual/'
KEF_LS35A = 'https://manualsnet.com/kef/reference-series-model-ls3-5a'
MEYER = 'https://www.svconline.com/products/meyer-sound-announces-mjf-212-high-power-stage-monitor-366663'
EV_SENTRY = 'https://manualzz.com/doc/22701574/electro-voice-sentry500-data-sheet'
EV_SX100 = 'https://manualzz.com/doc/3125205/electro-voice-sx100--user-s-manual'
DB_OPERA = 'https://www.manualslib.com/manual/759581/Db-Technologies-Opera-Live.html?page=6'

TANNOY_WHY = ('The Tannoy manual is served from manualzz.com, a document aggregator, not from a Tannoy '
              'host.')
SPENDOR_WHY = ('The Spendor manual is served from manualmachine.com, a document aggregator, not from a '
               'Spendor host.')
KEF_WHY = ('The KEF sheet is served from manualsnet.com, a document aggregator, not from a KEF host; the '
           'KEF archive PDFs are redirect stubs.')
MEYER_WHY = ('The announcement is a trade-press item on svconline.com; no Meyer-hosted MJF-212 datasheet '
             'was opened in this session.')
EV_WHY = ('The Electro-Voice data sheet is served from manualzz.com, a document aggregator, not from an '
          'Electro-Voice host.')

PROMOTIONS = [
    {'record': 'tannoy-system-600', 'field': 'driverCount', 'value': 2, 'source': TANNOY,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Tannoy System 600 near-field reference monitor user manual (Issue 2, part 6481 0256)',
     'whyNotManufacturer': TANNOY_WHY,
     'note': ('Round 29 (2026-10-19): Tannoy System 600 manual — "Using an advanced Dual Concentric 6.5\\" '
              'driver"; the servicing chapter separates the two transducers: "The HF unit may be fitted with '
              'a new diaphragm assembly" and "The LF unit may be re-coned in the normal way", the Dual '
              'Concentric integrating an HF unit and an LF unit in one chassis. Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Tannoy System '
                     '600 manual (manualzz copy); the separate System 600a active model is not this record.')},
    {'record': 'tannoy-system-600', 'field': 'active', 'value': False, 'source': TANNOY,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Tannoy System 600 near-field reference monitor user manual (Issue 2, part 6481 0256)',
     'whyNotManufacturer': TANNOY_WHY,
     'note': ('Round 29 (2026-10-19): same manual — the terminals "must be connected to the red or positive '
              'terminal on the power amplifier", and the manual carries a "Power amplifiers" chapter matching '
              'amplifier power to the speaker\'s rating. External amplification, no mains inlet described.'),
     'notesAppend': ''},
    {'record': 'spendor-sp100', 'field': 'driverCount', 'value': 3, 'source': SPENDOR,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Spendor SP-100 owner's manual, 'Specifications and Main Features'",
     'whyNotManufacturer': SPENDOR_WHY,
     'note': ('Round 29 (2026-10-19): Spendor SP-100 manual — "Low Frequency unit Spendor 300mm Bextrene", '
              '"Mid Frequency unit Spendor 160mm Homopolymer Polypropylene", "High Frequency unit 19mm Soft '
              'Dome"; crossover points 600 Hz, 4 kHz. Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 and active false verified from the Spendor SP-100 '
                     'owner\'s manual (manualmachine copy).')},
    {'record': 'spendor-sp100', 'field': 'active', 'value': False, 'source': SPENDOR,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Spendor SP-100 owner's manual, 'Specifications and Main Features'",
     'whyNotManufacturer': SPENDOR_WHY,
     'note': ('Round 29 (2026-10-19): same manual — the wiring chapter says "Switch off your amplifier. Take '
              'the first cable pair. Connect the black terminal on the amplifier left channel to the black '
              'HF terminal on the left loudspeaker", with bi-wiring and tri-wiring described. External '
              'amplifier drive only.'),
     'notesAppend': ''},
    {'record': 'kef-ls3-5a', 'field': 'driverCount', 'value': 2, 'source': KEF_LS35A,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KEF Reference Series Model LS3/5A installation sheet (1994-98)',
     'whyNotManufacturer': KEF_WHY,
     'note': ('Round 29 (2026-10-19): KEF LS3/5A sheet — "This ultra compact system used the KEF B110 and '
              'T27 bass and treble units"; "Drive units B110 bass/midrange unit (SP1228), and T27 tweeter '
              '(SP1032)". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified from the KEF LS3/5A sheet (manualsnet '
                     'copy); active stays unresolved because only "Amplifier requirements 25-75W" is '
                     'printed.')},
    {'record': 'meyer-mjf212', 'field': 'driverCount', 'value': 3, 'source': MEYER,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Sound & Video Contractor, "Meyer Sound Announces MJF-212 High-Power Stage Monitor", 2007-01-17',
     'whyNotManufacturer': MEYER_WHY,
     'note': ('Round 29 (2026-10-19): SVC announcement — "The MJF-212\'s high-frequency section comprises a '
              '4in. diaphragm compression driver"; "A pair of high-power 12in. neodymium magnet cone drivers '
              '... reproduces low frequencies". Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 and active true verified from the SVC announcement '
                     '(self-powered, three-channel amplifier).')},
    {'record': 'meyer-mjf212', 'field': 'active', 'value': True, 'source': MEYER,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Sound & Video Contractor, "Meyer Sound Announces MJF-212 High-Power Stage Monitor", 2007-01-17',
     'whyNotManufacturer': MEYER_WHY,
     'note': ('Round 29 (2026-10-19): same announcement — "the MJF-212, a self-powered stage monitor '
              'loudspeaker"; "Each of the drivers is powered by one channel of a 3-channel class AB/H '
              'amplifier". Built-in amplification.'),
     'notesAppend': ''},
    {'record': 'eV-sentry-500', 'field': 'driverCount', 'value': 2, 'source': EV_SENTRY,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Electro-Voice Sentry 500 professional monitor system data sheet',
     'whyNotManufacturer': EV_WHY,
     'note': ('Round 29 (2026-10-19): EV Sentry 500 data sheet — "The low-frequency section of the Sentry 500 '
              'is a 12-inch direct radiator woofer" and "The Sentry 500 employs a Super-Dome tweeter". Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the EV Sentry 500 '
                     'data sheet (manualzz copy).')},
    {'record': 'eV-sentry-500', 'field': 'active', 'value': False, 'source': EV_SENTRY,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Electro-Voice Sentry 500 professional monitor system data sheet',
     'whyNotManufacturer': EV_WHY,
     'note': ('Round 29 (2026-10-19): same sheet — "The integral crossover network is a 12-dB/octave type '
              'with crossover occurring at 1500 Hz"; "Bi-amplification is easily accomplished by removing '
              'the \'Bi-Amp Access Panel\' ... Woofer and tweeter input connections are then made on the '
              'system input board"; "amplifiers as large as 400 watts can be used". External amplifiers.'),
     'notesAppend': ''},
    {'record': 'electro-voice-sx100', 'field': 'driverCount', 'value': 2, 'source': EV_SX100,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Electro-Voice Sx100+ data sheet, part 535581 Rev E (7/2006)',
     'whyNotManufacturer': EV_WHY,
     'note': ('Round 29 (2026-10-19): EV Sx100+ data sheet — "LF Transducer: 12\\" (300mm)" and "HF '
              'Transducer: 1\\" (25mm) exit DH3 Comp. Driver"; "12-inch two-way". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified from the Sx100+ data sheet (manualzz '
                     'copy); active stays unresolved because the sheet gives only power handling and '
                     'connectors.')},
]

URL_RESULTS = [
    {'url': TANNOY, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0, 1, 2], 'chunksTotal': 3,
     'evidence': ('"Dual Concentric 6.5\\" driver"; HF unit and LF unit serviced separately; terminals connect '
                  'to the power amplifier; "Recommended amplifier power 50 to 150 W rms into 8 ohm".'),
     'fieldResults': [
         {'record': 'tannoy-system-600', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: HF unit + LF unit listed separately.'},
         {'record': 'tannoy-system-600', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external power amplifier connection and power-amplifier chapter.'},
     ]},
    {'url': SPENDOR, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('SP-100: 300 mm Bextrene LF, 160 mm mid, 19 mm soft dome HF; crossover 600 Hz/4 kHz; '
                  'wiring chapter drives the terminals from the amplifier, bi-/tri-wiring.'),
     'fieldResults': [
         {'record': 'spendor-sp100', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: three units listed.'},
         {'record': 'spendor-sp100', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: amplifier wiring instructions; passive.'},
     ]},
    {'url': KEF_LS35A, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('LS3/5A: B110 + T27 drive units; two-way closed box; "Amplifier requirements 25-75W (into '
                  '8 ohms)"; no passive/active statement.'),
     'fieldResults': [
         {'record': 'kef-ls3-5a', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two named drive units.'},
         {'record': 'kef-ls3-5a', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: amplifier-requirements figure only; policy excludes it.'},
     ]},
    {'url': MEYER, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"self-powered stage monitor"; 4 in compression driver + a pair of 12 in cone drivers; '
                  '3-channel class AB/H amplifier inside.'),
     'fieldResults': [
         {'record': 'meyer-mjf212', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: one HF + two LF drivers.'},
         {'record': 'meyer-mjf212', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "self-powered"; built-in three-channel amplifier.'},
     ]},
    {'url': EV_SENTRY, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('Sentry 500: 12 in woofer + Super-Dome tweeter; integral 12 dB/oct crossover at 1.5 kHz; '
                  'bi-amp access panel; amplifiers up to 400 W.'),
     'fieldResults': [
         {'record': 'eV-sentry-500', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: woofer + tweeter.'},
         {'record': 'eV-sentry-500', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: integral passive crossover, bi-amp with external amplifiers.'},
     ]},
    {'url': EV_SX100, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('Sx100+: "12-inch two-way"; LF 12 in, HF 1 in DH3 compression driver; 200 W continuous, '
                  'Speakon connectors; no passive/active statement.'),
     'fieldResults': [
         {'record': 'electro-voice-sx100', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: LF + HF transducers.'},
         {'record': 'electro-voice-sx100', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: power handling and connectors only.'},
     ]},
    {'url': DB_OPERA, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1, 2], 'chunksTotal': 4,
     'evidence': ('Opera Live manual page 6: four-column specification table (202/205/402/405) and an '
                  'amplifier section per model, but the extracted text is not column-aligned, so the 405 '
                  'column could not be read with certainty. The series heading reads "professional active '
                  'speaker".'),
     'fieldResults': [
         {'record': 'dbtechnologies-opera-405', 'field': 'driverCount', 'value': 2, 'outcome': 'NOT_EXTRACTED',
          'note': 'Round 29: 405 column not recoverable from the page; no model-specific quote.'},
         {'record': 'dbtechnologies-opera-405', 'field': 'active', 'value': True, 'outcome': 'NOT_EXTRACTED',
          'note': 'Round 29: series heading says "active", but the 405 row could not be isolated; not promoted.'},
     ]},
]
