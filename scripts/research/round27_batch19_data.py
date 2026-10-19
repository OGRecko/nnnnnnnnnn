#!/usr/bin/env python3
"""Round 27 batch 19 (2026-10-19): Dynaudio LYD 5 / LYD 7 / LYD 48.

Dynaudio's specification tables list one row per transducer ("Tweeter", "Midrange/Woofer",
"Midrange", "Woofer") and a per-band "Amplifier Power" row plus an AC power input. The
transducer rows give the driver count directly; the amplifier rows describe amplification
built into the monitor, not a recommended external amplifier.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
L5 = 'https://dynaudio.com/professional-audio/lyd/lyd-5'
L7 = 'https://dynaudio.com/professional-audio/lyd/lyd-7'
L48 = 'https://dynaudio.com/professional-audio/lyd/lyd-48'

CHECKS = [
    {
        'url': L5,
        'sourceClass': 'MANUFACTURER',
        'document': 'Dynaudio LYD 5 product page, Specifications',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specification rows: "Crossover 2-way DSP-based"; "Crossover Frequency (Hz) 5200 Hz"; '
            '"Tweeter 1.1in soft dome"; "Midrange/Woofer 5in MSP"; "Amplifier Power Woofer (W) 50"; '
            '"Amplifier Power Tweeter (W) 50"; "AC Power Input 100-240V 50/60Hz".'
        ),
        'results': [
            ('dynaudio-lyd-5.driverCount', 'PROMOTED', 2,
             'Two transducer rows: one 5in MSP midrange/woofer and one 1.1in soft dome tweeter in a '
             '2-way system.'),
        ],
    },
    {
        'url': L7,
        'sourceClass': 'MANUFACTURER',
        'document': 'Dynaudio LYD 7 product page, Specifications',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specification rows: "Crossover 2-way DSP-based"; "Crossover Frequency (Hz) 4300 Hz"; '
            '"Tweeter 1.1in soft dome"; "Midrange/Woofer 7in MSP"; "Amplifier Power Woofer (W) 50"; '
            '"Amplifier Power Tweeter (W) 50"; "AC Power Input 100-240V 50/60Hz".'
        ),
        'results': [
            ('dynaudio-lyd-7.driverCount', 'PROMOTED', 2,
             'Two transducer rows: one 7in MSP midrange/woofer and one 1.1in soft dome tweeter in a '
             '2-way system.'),
        ],
    },
    {
        'url': L48,
        'sourceClass': 'MANUFACTURER',
        'document': 'Dynaudio LYD 48 product page, Specifications',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specification rows: "Crossover 3-way DSP-based"; "Crossover Frequency (Hz) 460/5500 Hz"; '
            '"Tweeter 1.1in soft dome"; "Midrange 4in MSP"; "Woofer 8in MSP"; "Amplifier Power Woofer (W) '
            '80"; "Amplifier Power midrange (W) 50"; "Amplifier Power Tweeter (W) 50"; "AC Power Input '
            '100-240V 50/60Hz".'
        ),
        'results': [
            ('dynaudio-lyd-48.driverCount', 'PROMOTED', 3,
             'Three transducer rows: 8in MSP woofer, 4in MSP midrange and 1.1in soft dome tweeter in a '
             '3-way system.'),
            ('dynaudio-lyd-48.active', 'PROMOTED', True,
             'A separate amplifier power row per band (80 W / 50 W / 50 W) plus a 100-240 V AC input and a '
             'DSP crossover: the amplification is built into the monitor.'),
        ],
    },
]
