#!/usr/bin/env python3
"""Round 27 batch 6 (2026-10-19): filling UNSOURCED fields from manufacturer documents.

These records carry no cited claim at all (both fields UNSOURCED), so each write is a
first promotion backed by an exact-model manufacturer document opened in this round.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
YAMAHA_HS = 'https://usa.yamaha.com/products/proaudio/speakers/hs_series/specs.html'

CHECKS = [
    {
        'url': YAMAHA_HS,
        'sourceClass': 'MANUFACTURER',
        'document': 'Yamaha HS Series (HS5/HS5I/HS7/HS7I/HS8/HS8I) specifications table',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Specification table row "Speaker type" reads "2-way bi-amp powered studio monitor" for '
            'HS5, HS7 and HS8 alike. Components: HS5 LF 5" cone + HF 1" dome; HS7 LF 6.5" cone + HF '
            '1" dome; HS8 LF 8" cone + HF 1" dome. Output power HS5 70 W, HS7 95 W, HS8 120 W; I/O '
            'connectors XLR3-31 and PHONE (balanced) only, i.e. line-level inputs with no passive '
            'terminal. The model is named powered by the manufacturer itself.'
        ),
        'results': [
            ('yamaha-hs5.driverCount', 'PROMOTED', 2,
             'HS5: LF 5" cone + HF 1" dome in the "Components" row of the HS Series spec table.'),
            ('yamaha-hs5.active', 'PROMOTED', True,
             'HS5 row: "Speaker type 2-way bi-amp powered studio monitor" with 70 W output power and '
             'balanced line inputs.'),
            ('yamaha-hs7.driverCount', 'PROMOTED', 2,
             'HS7: LF 6.5" cone + HF 1" dome in the "Components" row of the HS Series spec table.'),
            ('yamaha-hs7.active', 'PROMOTED', True,
             'HS7 row: "Speaker type 2-way bi-amp powered studio monitor" with 95 W output power.'),
            ('yamaha-hs8.driverCount', 'PROMOTED', 2,
             'HS8: LF 8" cone + HF 1" dome in the "Components" row of the HS Series spec table.'),
            ('yamaha-hs8.active', 'PROMOTED', True,
             'HS8 row: "Speaker type 2-way bi-amp powered studio monitor" with 120 W output power.'),
        ],
    },
]
