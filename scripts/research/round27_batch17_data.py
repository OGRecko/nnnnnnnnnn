#!/usr/bin/env python3
"""Round 27 batch 17 (2026-10-19): KEF KC62 and JBL Control 25-1.

KC62 is a self-amplified subwoofer: KEF's own product copy says the two drive units are
"powered by 1,000W RMS of specially designed Class D amplification", so both the transducer
count and the amplification are stated outright.

Control 25-1's specification table lists exactly two transducers (LF 135 mm, HF 19 mm); the
page does not print a passive/active classification, so only the driver count is written.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
KC62 = 'https://international.kef.com/products/kc62-subwoofer'
C251 = 'https://jblpro.com/en-US/products/control-25-1'

CHECKS = [
    {
        'url': KC62,
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF KC62 product page',
        'chunksOpened': [0],
        'chunksTotal': 5,
        'evidence': (
            '"KC62 is an incredibly compact subwoofer ... the football-sized KC62 features two 6.5inch '
            'force cancelling drive units powered by 1,000W RMS of specially designed Class D '
            'amplification." The page describes no other transducer.'
        ),
        'results': [
            ('kef-kc62.driverCount', 'PROMOTED', 2,
             'Two 6.5 inch force-cancelling drive units, stated in KEF\'s product copy.'),
            ('kef-kc62.active', 'PROMOTED', True,
             'The same sentence says the drivers are powered by 1,000 W RMS of Class D amplification '
             'built into the subwoofer.'),
        ],
    },
    {
        'url': C251,
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional Control 25-1 product page, Specifications table',
        'chunksOpened': [1],
        'chunksTotal': 3,
        'evidence': (
            '"Drivers | LF: 135 mm (5.25 in), woven-fiberglass cone ... HF: 19 mm (0.75 in) PEI '
            'diaphragm, low-viscosity ferro-magnetic fluid, and lightweight Kapton™ voice coil former." '
            'The table also prints "Impedance | 8 ohms (THRU setting)" and "Power Rating | 200 W '
            'Continuous Program (2 hrs)" but no passive/active row.'
        ),
        'results': [
            ('jbl-control-25.driverCount', 'PROMOTED', 2,
             'The specification table lists one LF driver (135 mm) and one HF driver (19 mm).'),
        ],
    },
]
