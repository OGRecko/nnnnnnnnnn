#!/usr/bin/env python3
"""Round 27 batch 14 (2026-10-19): the Neumann KH monitor line.

www.neumann.com was added to the source-host allowlist in this round with operator evidence
("newsletters from Georg Neumann GmbH"). Every value below comes from the model's own
"DATA & DIAGRAMS" table on neumann.com, which lists the driver dimensions, the amplifier output
per band and the mains supply.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
KH120 = 'https://www.neumann.com/en-us/products/historical/kh-120-a-g'
KH310 = 'https://www.neumann.com/en-us/products/historical/kh-310-a'
KH80 = 'https://www.neumann.com/en-us/products/monitors/kh-80-dsp-a-g'
KH120II = 'https://www.neumann.com/en-us/products/monitors/kh-120-ii/'
KH150 = 'https://www.neumann.com/en-us/products/monitors/kh-150'
KH420 = 'https://www.neumann.com/en-us/products/monitors/kh-420'
KH750 = 'https://www.neumann.com/en-us/products/monitors/kh-750-dsp'

CHECKS = [
    {
        'url': KH120,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 120 A G product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 1],
        'chunksTotal': 6,
        'evidence': (
            'Page heading "KH 120 A G - Two Way Nearfield Monitor". Table: "Woofer | 130 mm (5.25\\") '
            'magnetically shielded with protecting black metal grille"; "Tweeter | 25 mm (1\\") with '
            'protecting black metal grille"; "Controller design | Analog; active"; "Output power woofer '
            'amplifier (THD+N with limiter deactivated: 10%) | 80 W"; "Output power tweeter amplifier '
            '(THD+N with limiter deactivated: 10%) | 80 W"; "Mains Power Supply: SMPS: 100-240 V; 50/60 Hz".'
        ),
        'results': [
            ('neumann-kh120.driverCount', 'PROMOTED', 2,
             'One 130 mm (5.25") woofer plus one 25 mm (1") tweeter in a two-way system.'),
            ('neumann-kh120.active', 'PROMOTED', True,
             'On-board woofer and tweeter amplifiers (80 W each at the 10% THD+N condition) with an '
             'internal switched-mode mains supply; controller design "Analog; active".'),
        ],
    },
    {
        'url': KH310,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 310 A product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 2],
        'chunksTotal': 7,
        'evidence': (
            'Page heading "KH 310 A - Three Way Nearfield Monitor". Table: "Woofer | 210 mm (8 1/4\\") '
            'magnetically sheilded"; "Tweeter | 25 mm (1\\") with protecting black metal grille"; '
            '"Protection circuitry | Independent thermo limiters for woofer, midrange dome and tweeter"; '
            '"Crossover frequency | 650 Hz and 2.0 kHz"; "Controller design | Analog; active"; "Output '
            'power woofer amplifier (THD+N with limiter deactivated: 10%) | 210 W"; tweeter 90 W; "Mains '
            'Power Supply: SMPS: 100-240 V".'
        ),
        'results': [
            ('neumann-kh310.driverCount', 'PROMOTED', 3,
             'The three-way title, the two crossover frequencies (650 Hz and 2.0 kHz) and the protection '
             'clause naming "woofer, midrange dome and tweeter" enumerate three transducers.'),
            ('neumann-kh310.active', 'PROMOTED', True,
             'Built-in amplifiers per band (210 W woofer, 90 W tweeter at the 10% THD+N condition), '
             'internal SMPS; controller design "Analog; active".'),
        ],
    },
    {
        'url': KH80,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 80 DSP A G product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 2, 3],
        'chunksTotal': 7,
        'evidence': (
            '"Mechanics | Woofer | 100 mm (4\\") with protecting black metal grille"; "Tweeter | 25 mm (1\\") '
            'with protecting black metal grille"; "Controller design | Digital; active"; "Output power '
            'woofer amplifier (THD+N with limiter deactivated: 10%) | 120 W"; "Output power tweeter '
            'amplifier (THD+N with limiter deactivated: 10%) | 70 W"; "Mains Power Supply: input voltage; '
            'frequency | 100-240 V; 50/60 Hz".'
        ),
        'results': [
            ('neumann-kh-80-dsp.driverCount', 'PROMOTED', 2,
             'One 100 mm (4") woofer plus one 25 mm (1") tweeter; the protection and limiter text also '
             'names exactly a woofer and a tweeter.'),
            ('neumann-kh-80-dsp.active', 'PROMOTED', True,
             'On-board 120 W woofer / 70 W tweeter amplifiers with an internal universal mains supply; '
             'controller design "Digital; active".'),
        ],
    },
    {
        'url': KH120II,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 120 II product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 2],
        'chunksTotal': 6,
        'evidence': (
            'Page title "KH 120 II - Neumann Active Studio Monitor". Table: "Woofer | 130 mm; (5.25\\") with '
            'protecting black metal grille"; "Tweeter | 25 mm; (1\\") with protecting black metal grille"; '
            '"Output power woofer amplifier (THD+N with limiter deactivated: 10%) | 145 W"; "Output power '
            'tweeter amplifier (THD+N with limiter deactivated: 10%) | 100 W"; "Mains Power Supply: input '
            'voltage; frequency | 100-240 V; 50/60 Hz".'
        ),
        'results': [
            ('neumann-kh-120-ii.driverCount', 'PROMOTED', 2,
             'One 130 mm (5.25") woofer plus one 25 mm (1") tweeter in a two-way system.'),
            ('neumann-kh-120-ii.active', 'PROMOTED', True,
             'On-board 145 W woofer / 100 W tweeter amplifiers with an internal mains supply; the page '
             'title calls it an "Active Studio Monitor".'),
        ],
    },
    {
        'url': KH150,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 150 product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 2],
        'chunksTotal': 5,
        'evidence': (
            '"Mechanics | Woofer | 165 mm; (6.5\\") with protecting black metal grille"; "Tweeter | 25 mm; '
            '(1\\") with protecting black metal grille"; "Output power tweeter amplifier (THD+N with limiter '
            'deactivated: 10%) | 100 W"; "Output power woofer amplifier (THD+N with limiter deactivated: '
            '0.1%) | 120 W"; "Mains Power Supply: input voltage; frequency | 100-240 V; 50/60 Hz".'
        ),
        'results': [
            ('neumann-kh-150.driverCount', 'PROMOTED', 2,
             'One 165 mm (6.5") woofer plus one 25 mm (1") tweeter in a two-way monitor.'),
            ('neumann-kh-150.active', 'PROMOTED', True,
             'Separate built-in woofer and tweeter amplifiers and an internal mains supply.'),
        ],
    },
    {
        'url': KH420,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 420 product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 2],
        'chunksTotal': 6,
        'evidence': (
            'Page heading "KH 420 - Three Way Midfield Monitor". Table: "Woofer | 265 mm (10\\") with '
            'magnetic shielding"; "Tweeter | 25 mm (1\\") with protecting black metal grille"; "Protection '
            'circuitry | Independent thermo limiters for woofer, midrange dome and tweeter"; "Crossover '
            'frequency | 570 Hz and 2.0 kHz"; "Output power woofer amplifier (THD+N with limiter '
            'deactivated: 10%) | 330 W"; tweeter amplifier 140 W.'
        ),
        'results': [
            ('neumann-kh-420.driverCount', 'PROMOTED', 3,
             'Three-way title, two crossover frequencies and a protection clause naming woofer, midrange '
             'dome and tweeter enumerate three transducers.'),
            ('neumann-kh-420.active', 'PROMOTED', True,
             'Built-in per-band amplification (330 W woofer, 140 W tweeter at the 10% THD+N condition).'),
        ],
    },
    {
        'url': KH750,
        'sourceClass': 'MANUFACTURER',
        'document': 'Neumann KH 750 DSP product page, "DATA & DIAGRAMS"',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Description: "The newly designed 10\\" long-throw driver has a strong linear working magnet '
            'system with ELFF™ technology". Table: "Controller design | Digital; active"; "Output power '
            'woofer amplifier (THD+N with limiter deactivated: 10%) | 256 W"; "Mains Power Supply: input '
            'voltage; frequency | SMPS: 100-240 V; 50/60 Hz".'
        ),
        'results': [
            ('neumann-kh-750-dsp.driverCount', 'PROMOTED', 1,
             'A single 10" long-throw driver; the page describes no other transducer.'),
            ('neumann-kh-750-dsp.active', 'PROMOTED', True,
             'Built-in 256 W woofer amplifier and internal SMPS; controller design "Digital; active".'),
        ],
    },
]
