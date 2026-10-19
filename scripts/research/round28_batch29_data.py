#!/usr/bin/env python3
"""Round 28 batch 29 data (2026-10-19): response-dataset audit, JBL 4310/4311.

Everything here was read from a document opened during this session. Nothing is inferred.

The JBL 4311 table below is the 1/3-octave response column as printed on the manufacturer page,
transcribed row by row. Blank rows (20 Hz and 20 kHz) are omitted, exactly as the page prints them.
It is used ONLY to compare against the stored series; no stored point is changed by this batch.
"""

ROUND = 28
DATE = '2026-10-19'

JBL_4311_URL = 'https://jblpro.com/en-US/site_elements/4311-information'
JBL_4310_URL = ('https://tile.loc.gov/storage-services/master/mbrs/recording_preservation/manuals/'
                'JBL%20Prof.%20Series%20Model%204310%20Control%20Room%20Monitor.pdf')

# 1/3-octave band centre frequency -> Response (dB) as printed, 0 dB at 1 kHz.
JBL_4311_TABLE = [
    (31.5, -11), (40, -7), (50, -1), (63, 3), (80, 2), (100, 1), (125, 0), (160, -1),
    (200, -1), (250, -3), (315, -2), (400, 0), (500, 1), (630, 1), (800, 1), (1000, 0),
    (1250, -2), (1600, 0), (2000, 2), (2500, 2), (3150, 1), (4000, 2), (5000, 2), (6300, 5),
    (8000, 1), (10000, 2), (12500, 2), (16000, -5),
]

# ---------------------------------------------------------------- URL rechecks
URL_RESULTS = [
    {
        'url': JBL_4310_URL,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0, 1],
        'evidence': (
            'Both pages of the JBL Professional Series Model 4310 brochure were opened. Chunk 1: '
            '"The loudspeaker system shall consist of three direct-radiator transducers and frequency '
            'dividing network installed in a tube-ported enclosure" and the Model 4310 specifications '
            'table (power capacity 50 W program, crossover 1500 and 7000 Hz, nominal impedance 8 ohms, '
            'dispersion 90 degrees, 45-15000 Hz +/-3 dB, sensitivity 42 dB at 30 ft with 1 mW). The '
            'document never uses the words passive, active or powered and gives no amplifier or mains '
            'input, but that absence is not treated as evidence; active stays unresolved.'
        ),
        'fieldResults': [
            {
                'record': 'jbl-4310', 'field': 'driverCount', 'value': 3,
                'outcome': 'SUPPORTED_NOT_PROMOTED',
                'note': ('Round 28: Architectural Specifications say "three direct-radiator transducers" '
                         '(12 in LF, 5 in MF, 1.75 in HF direct radiator). Value is supported by this '
                         'document but cannot be promoted: tile.loc.gov is not an established manufacturer '
                         'host under the Round 14 host policy.'),
            },
            {
                'record': 'jbl-4310', 'field': 'active', 'value': False,
                'outcome': 'NOT_STATED',
                'note': ('Round 28: both pages read; the brochure describes a frequency dividing network '
                         'inside the enclosure and a 50 W program power capacity, but never states passive '
                         'or self-powered and shows no amplifier. Value remains unresolved, not promoted.'),
            },
        ],
    },
    {
        'url': JBL_4311_URL,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0, 1],
        'evidence': (
            'Both chunks opened. The page describes a matched frequency dividing network with front-panel '
            'controls, 8-ohm nominal impedance, 75 W continuous-program capacity and a 1 W / 1 m response '
            'table; it never uses the words passive, active or powered, so active remains unresolved. The '
            'chunk-1 text is the sensitivity footnote and the JBL address block.'
        ),
        'fieldResults': [
            {
                'record': 'jbl-4311', 'field': 'active', 'value': False,
                'outcome': 'NOT_STATED',
                'note': ('Round 28: both chunks read; no passive/active/powered statement and no amplifier '
                         'rating. The record note claiming a "passive monitor" was corrected in this batch.'),
            },
        ],
    },
]

# ---------------------------------------------------------------- note corrections
# The record notes said "passive monitor"; the opened page never says passive. Keep every verified
# fact, replace only the unsupported characterisation.
JBL_4311_NOTES_FIND = 'It specifies a three-way, three-driver passive monitor;'
JBL_4311_NOTES_REPLACE = (
    'It specifies a three-way, three-driver monitor system with a matched frequency dividing network '
    'installed in the enclosure; the page never states passive or self-powered, so `active` stays '
    'unresolved. Round 28 (2026-10-19) removed the word "passive" from this note for that reason;'
)
JBL_4311_DATASET_NOTE = (
    ' Round 28 (2026-10-19) response-table recheck: the page was fetched again and its Response column '
    'transcribed row by row (28 printed rows; 20 Hz and 20 kHz blank). The stored 29-point series does '
    'not reproduce that column: it adds a 25 Hz point the page leaves blank and differs at 15 shared '
    'frequencies, mostly by 0.5 dB. The earlier Round 21 statement that only two points differed is not '
    'reproduced. No point was changed; the owner decision of 2026-10-12 that keeps the stored values '
    'stands, and this dataset stays flagged for adjudication.'
)
