#!/usr/bin/env python3
"""Round 27 batch 12 (2026-10-19): Mackie Thump 2022 series and JBL SRX800P powered speakers.

Mackie's two 2022 specification sheets print the transducer complement and the built-in amplifier
per model. JBL's product pages print a "Specifications" table that enumerates each driver by model
number and states "Nominal Impedance: NA - amplification is integrated".
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27

CHECKS = [
    {
        'url': 'https://mackie.com/img/file_resources/THUMP_2022_SS.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Mackie Thump212 / Thump215 1400W Powered Loudspeaker Series specification sheet (SW1377 Rev. A 07/22)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Transducers: "Low Frequency | 12 in / 305 mm [Thump212] 15 in / 381 mm [Thump215] with '
            'ferrite"; "High Frequency | 1.0 in / 25 mm polymer compression driver". Power amplifiers: '
            '"System Power Amplification | Rated Power 1400 watts peak"; "Low Frequency Power Amplifier '
            '| Rated Power 1200 watts peak"; "High Frequency Power Amplifier | Rated Power 200 watts '
            'peak"; "Design | Class D"; "Line input | 100-240V~, 50-60 Hz, 75W".'
        ),
        'results': [
            ('mackie-thump212.driverCount', 'PROMOTED', 2,
             'One 12 in (305 mm) ferrite woofer plus one 1.0 in (25 mm) polymer compression driver.'),
            ('mackie-thump212.active', 'PROMOTED', True,
             'Built-in 1400 W Class D system amplification (1200 W LF + 200 W HF) with an IEC mains inlet.'),
            ('mackie-thump215.driverCount', 'PROMOTED', 2,
             'One 15 in (381 mm) ferrite woofer plus one 1.0 in (25 mm) polymer compression driver.'),
            ('mackie-thump215.active', 'PROMOTED', True,
             'Built-in 1400 W Class D system amplification (1200 W LF + 200 W HF) with an IEC mains inlet.'),
        ],
    },
    {
        'url': 'https://mackie.com/img/file_resources/THUMP_SUBS_2022_SS.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Mackie Thump115S / Thump118S 1400W Powered Subwoofer Series specification sheet',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Transducers: "Low Frequency | 15 in / 381 mm [Thump115S] 18 in / 457 mm [Thump118S] with '
            'ferrite" - no high-frequency device is listed. Power amplifiers: "System Power '
            'Amplification | Rated Power 1400 watts peak"; "Low Frequency Power Amplifier | Rated Power '
            '1400 watts peak"; "Design | Class D"; "Line input | 100-120V~ ... 220-240V~".'
        ),
        'results': [
            ('mackie-thump118s.driverCount', 'PROMOTED', 1,
             'A single 18 in (457 mm) ferrite low-frequency transducer; the sheet lists no high-frequency '
             'driver.'),
            ('mackie-thump118s.active', 'PROMOTED', True,
             'Built-in 1400 W Class D amplification with a detachable IEC line cord.'),
        ],
    },
    {
        'url': 'https://jblpro.com/en-US/products/srx815p',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional SRX815P product page, "Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Headline: "15-inch 2-Way Multipurpose Powered Speaker". Specifications: "System Type | Self '
            'powered 15\\", two-way, bass-reflex"; "Amplifier Design | Class D"; "Power Rating | 2000 W '
            'Peak"; "Nominal Impedance | NA - amplification is integrated"; "LF Driver | 1 x 2275F, '
            'Differential Drive®, 15\\" diameter"; "HF Driver | 1 x 2432H compression driver".'
        ),
        'results': [
            ('jbl-srx815p.driverCount', 'PROMOTED', 2,
             'One 2275F 15" low-frequency driver plus one 2432H compression driver in a two-way system.'),
            ('jbl-srx815p.active', 'PROMOTED', True,
             '"Self powered"; 2000 W Class D amplification is integrated (nominal impedance is stated as '
             '"NA - amplification is integrated").'),
        ],
    },
    {
        'url': 'https://jblpro.com/en-US/products/srx835p',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional SRX835P product page, "Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Headline: "15-inch 3-Way Point-Source Powered Speaker". Specifications: "System Type | Self '
            'powered 15\\", three-way, bass-reflex"; "LF Driver | 1 x 2275F, Differential Drive®, 15\\" '
            'diameter"; "MF Driver | 1 x 2107H"; "HF Driver | 1 x 2432H compression driver"; "Nominal '
            'Impedance | NA - amplification is integrated".'
        ),
        'results': [
            ('jbl-srx835p.driverCount', 'PROMOTED', 3,
             'One 2275F 15" LF driver, one 2107H midrange driver and one 2432H compression driver.'),
            ('jbl-srx835p.active', 'PROMOTED', True,
             '"Self powered"; 2000 W Class D amplification is integrated.'),
        ],
    },
]
