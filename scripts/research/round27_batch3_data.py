#!/usr/bin/env python3
"""Round 27 batch 3 (2026-10-19): Triangle Borea BR02 and the KEF archive redirect."""
CHECKED_DATE = '2026-10-19'
ROUND = 27
CHECKS = [
    {
        'url': 'https://trianglehifi.com/products/enceinte-bibliotheque-hi-fi-borea-br02',
        'sourceClass': 'MANUFACTURER',
        'document': 'Triangle Borea BR02 product page, Triangle HiFi (4 chunks; TECHNICAL SPECIFICATIONS read)',
        'chunksOpened': [2],
        'chunksTotal': 4,
        'evidence': (
            'Technical specifications: "Driver informations - 2 Drivers: 1 x 25mm silk dome tweeter; 1 x 13 cm '
            'midwoofer with natural cellulose pulp membrane". "Sensitivity (dB/W/m): 89dB" - explicitly a 1 W / '
            '1 m reference, not 2.83 V. "Nominal impedance: 8 Ohm", "Minimum impedance: 3,6 Ohm", "Bandwith '
            '(+/-3dB Hz): 51Hz-22 000Hz". Amplifier section: "Recommended Amplifier power: from 15 to 100 Watts '
            '(8 Ohms)", "Power Handling: 80W". The page never states passive, active, powered or built-in '
            'amplification.'
        ),
        'results': [
            ('triangle-borea-br02.driverCount', 'PROMOTED',
             'The exact product page lists "2 Drivers": one 25 mm silk dome tweeter and one 13 cm midwoofer, '
             'matching the stored value of 2.'),
            ('triangle-borea-br02.active', 'NOT_STATED',
             'Recommended amplifier power, power handling and impedance are given, but no passive/active, '
             'powered or built-in amplification wording appears. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://assets.kef.com/pdf_doc/product-archive/1970s/REFERENCE+SERIES+MODEL+103+(1976-77).pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF Reference Series Model 103 (1976-77) archive PDF link',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'The URL does not serve a document: the retrieved content is a single line, "redirecting to '
            '[kef.com](http://www.kef.com/)". No specification, driver complement or passive/active statement '
            'is available, so neither field can be assessed from this URL.'
        ),
        'results': [
            ('legacy-kef-3.driverCount', 'INACCESSIBLE',
             'The archive PDF URL returns only a redirect notice to kef.com; no document text is served. '
             'Field left unchanged.'),
            ('legacy-kef-3.active', 'INACCESSIBLE',
             'The archive PDF URL returns only a redirect notice; no passive/active statement is available. '
             'Field left unchanged.'),
        ],
    },
]
