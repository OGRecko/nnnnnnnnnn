#!/usr/bin/env python3
"""Round 27 batch 16 (2026-10-19): Focal Shape active nearfield monitors.

Focal's own product sheets print an "Electronic section" that belongs to the loudspeaker
itself: a mid/bass amplifier, a high-frequency amplifier, an IEC mains inlet and a standby
circuit. That is a direct statement that the cabinet contains its power amplifiers - it is
not a recommended external amplifier range. The same tables list the transducers, so the
driver count is one woofer plus one tweeter; the "double passive radiator" is not a driven
transducer and is not counted (the repository already treats ABRs/passive radiators as
non-drivers).
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
S40 = 'https://media.focal-naim.com/dam/shape-40/fp_shape40_en.pdf'
S50 = 'https://media.focal-naim.com/dam/shape-50/fp_shape50_en.pdf'
S65 = 'https://media.focal-naim.com/dam/shape-65/fp_shape65_en.pdf'

ELECTRONICS = (
    '"Electronic section" rows: "Midrange and low frequency amplifier | {lf}, Class AB"; '
    '"High frequency amplifier | {hf}, Class AB"; "Automatic standby"; "Electrical supply | '
    'Voltages | 220-240V ... or 100-120V"; "Electrical supply | Connection | IEC plug and '
    'detachable power cord". "Transducers": "Woofer | {w} Flax Cone"; "Tweeter | 1\" (25mm) '
    'profile Aluminum-Magnesium". The cabinet also carries a double passive radiator, which is '
    'not a driven transducer.'
)

CHECKS = [
    {
        'url': S40,
        'sourceClass': 'MANUFACTURER',
        'document': 'Focal Shape 40 product sheet (English), technical table',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ELECTRONICS.format(lf='25W', hf='25W', w='4" (10cm)') ,
        'results': [
            ('ath-focal-shape40.driverCount', 'PROMOTED', 2,
             'One 4" (10 cm) Flax woofer plus one 1" (25 mm) tweeter. The 4" double passive radiator is '
             'not a driven transducer and is not counted.'),
            ('ath-focal-shape40.active', 'PROMOTED', True,
             'The sheet lists the monitor\'s own mid/bass and high-frequency Class AB amplifiers, an IEC '
             'mains inlet and a standby circuit as part of the product.'),
        ],
    },
    {
        'url': S50,
        'sourceClass': 'MANUFACTURER',
        'document': 'Focal Shape 50 product sheet (English), technical table',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ELECTRONICS.format(lf='60W', hf='25W', w='5" (13cm)'),
        'results': [
            ('focal-shape-50.active', 'PROMOTED', True,
             'The sheet lists the monitor\'s own 60 W mid/bass and 25 W high-frequency Class AB '
             'amplifiers, an IEC mains inlet and a standby circuit as part of the product.'),
        ],
    },
    {
        'url': S65,
        'sourceClass': 'MANUFACTURER',
        'document': 'Focal Shape 65 product sheet (English), technical table',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ELECTRONICS.format(lf='80W', hf='25W', w='6.5" (16.5cm)'),
        'results': [
            ('ath-focal-shape65.driverCount', 'PROMOTED', 2,
             'One 6.5" (16.5 cm) Flax woofer plus one 1" (25 mm) tweeter. The 6.5" double passive '
             'radiator is not a driven transducer and is not counted.'),
            ('ath-focal-shape65.active', 'PROMOTED', True,
             'The sheet lists the monitor\'s own 80 W mid/bass and 25 W high-frequency Class AB '
             'amplifiers, an IEC mains inlet and a standby circuit as part of the product.'),
        ],
    },
]
