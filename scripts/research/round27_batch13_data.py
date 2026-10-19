#!/usr/bin/env python3
"""Round 27 batch 13 (2026-10-19): JBL M2 Master Reference Monitor and 708P.

The M2 page is explicit that the loudspeaker itself has no amplification: it lists spring-terminal
inputs and states that the system "Requires One Crown iTech 5000HD power amp for each speaker".
The 708P page lists its own Class D amplifier power. Both pages enumerate the drivers by part number.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27

CHECKS = [
    {
        'url': 'https://jblpro.com/en-US/products/m2',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional M2 Master Reference Monitor product page, "Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 4,
        'evidence': (
            '"System Format | 2-Way Floor Standing or Soffit Mountable"; "HF Driver | D2430K Dual '
            'Diaphragm Dual Voice Coil Compression Driver"; "LF Driver | 2216Nd 15 in (381 mm) '
            'Differential Drive® Woofer"; "The System Requires | One Crown® iTech 5000HD power amp for '
            'each speaker, or One Crown® iTech 3x3500HD power amp for two (2) speakers"; "Input '
            'Connectors | Spring Terminals".'
        ),
        'results': [
            ('jbl-m2.driverCount', 'PROMOTED', 2,
             'One D2430K dual-diaphragm compression driver plus one 2216Nd 15" woofer in a two-way system.'),
            ('jbl-m2.active', 'PROMOTED', False,
             'The loudspeaker has spring-terminal inputs and the page states the system "requires" an '
             'external Crown iTech power amplifier; no amplifier is integrated in the cabinet.'),
        ],
    },
    {
        'url': 'https://jblpro.com/en-US/products/708p',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional 708P product page, "Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            '"HF Driver | 2409H"; "LF Driver | 728G - 8in (203mm)"; "Dividing Network Transition '
            'Frequency | 1.7 kHz"; "LF Driver Power Handling | 250W Class D"; "Amplifier Power Rating | '
            '250W"; inputs are XLR analog and XLR AES3.'
        ),
        'results': [
            ('jbl-708p.driverCount', 'PROMOTED', 2,
             'One 2409H high-frequency driver plus one 728G 8 in (203 mm) low-frequency driver.'),
            ('jbl-708p.active', 'PROMOTED', True,
             'On-board "250W Class D" amplifier with XLR analog and AES3 inputs; no external amplifier '
             'is specified.'),
        ],
    },
]
