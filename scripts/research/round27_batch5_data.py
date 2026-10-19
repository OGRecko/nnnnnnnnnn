#!/usr/bin/env python3
"""Round 27 batch 5 (2026-10-19): the whole Klipsch spec-sheet cluster.

Every sheet below was retrieved in full. All of them publish a peak/continuous
power-handling figure and passive input terminals but none of them writes
"passive", "active", "powered" or "built-in amplification". Each `active` field is
therefore NOT_STATED: power handling is not a classification statement.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
HOST = 'https://assets.klipsch.com/product-specsheets/'

# (file, record, sheet title, power handling line, inputs line)
SHEETS = [
    ('AWR-650-SM.pdf', 'klipsch-awr650sm', 'AWR-650-SM outdoor speaker',
     '"power handling 50W continuous / 200W peak", "recommended amplifier power 100 W / 200 W peak"',
     'the data table lists no input connectors at all'),
    ('Forte-IV-Spec-Sheet-v01-1.pdf', 'klipsch-forte-iv', 'Forte IV',
     '"POWER HANDLING (CONT/PEAK) 100W / 400W"',
     '"INPUTS Dual binding posts / bi-wire / bi-amp"'),
    ('Heresy-IV-Spec-Sheet-v04.pdf', 'klipsch-heresy-iv', 'Heresy IV',
     '"POWER HANDLING (CONT/PEAK) 100W/400W"',
     '"INPUTS Dual binding posts / bi-wire / bi-amp"'),
    ('R-41M_Spec-Sheet_GM_v01.pdf', 'legacy-klip-8', 'R-41M',
     '"POWER HANDLING (CONT/PEAK) 50W/200W"',
     '"INPUTS Single Gold Plated Binding Posts"'),
    ('RP-5000F-II_Spec-Sheet_v02.pdf', 'klipsch-rp-5000f-ii', 'RP-5000F II',
     '"POWER HANDLING (CONT/PEAK) 100W / 400W"',
     '"INPUTS Dual aluminum binding posts / bi-wire / bi-amp with Dolby Atmos passthrough"'),
    ('RP-500M-II_Spec-Sheet_v02_2022-05-18-131859_rlqj.pdf', 'klipsch-rp500m', 'RP-500M II',
     '"POWER HANDLING (CONT/PEAK) 75W/300W"', '"INPUTS Single aluminum binding posts"'),
    ('RP-500M_Spec-Sheet_v01.pdf', 'klipsch-rp-500m', 'RP-500M',
     '"POWER HANDLING (CONT/PEAK) 75W/300W"', '"INPUTS Single binding posts"'),
    ('RP-6000F-II_Spec-Sheet_v02.pdf', 'klipsch-rp6000f', 'RP-6000F II',
     '"POWER HANDLING (CONT/PEAK) 125W/500W"', '"INPUTS Dual binding posts / bi-wire / bi-amp"'),
    ('RP-600M-II_Spec-Sheet_v02.pdf', 'klipsch-rp600m', 'RP-600M II',
     '"POWER HANDLING (CONT/PEAK) 100W/400W"', '"INPUTS Dual aluminum binding posts/bi-wire/bi-amp"'),
    ('RP-600M_Spec-Sheet_v01.pdf', 'klipsch-rp-600m', 'RP-600M',
     '"POWER HANDLING (CONT/PEAK) 100W/400W"', '"INPUTS Dual binding posts/bi-wire/bi-amp"'),
    ('RP-8000F-II_Spec-Sheet_v02.pdf', 'klipsch-rp-8000f-ii', 'RP-8000F II',
     '"POWER HANDLING (CONT/PEAK) 150W / 600W"',
     '"INPUTS Dual aluminum binding posts / bi-wire / bi-amp with Dolby Atmos passthrough"'),
    ('RP-8060FA-II_Spec-Sheet_v02.pdf', 'klipsch-rp8060fa', 'RP-8060FA II',
     '"POWER HANDLING (CONT/PEAK) 150W / 600W"', '"INPUTS Dual aluminum binding posts / bi-wire / bi-amp"'),
]

CHECKS = []
for fname, record, title, power, inputs in SHEETS:
    CHECKS.append({
        'url': HOST + fname,
        'sourceClass': 'MANUFACTURER',
        'document': f'Klipsch {title} spec sheet ({fname})',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            f'Specifications table: {power}; {inputs}; nominal impedance 8 ohms compatible. The sheet '
            'never uses the words passive, active, powered or built-in amplification. In the Forte IV '
            'sheet "PASSIVE RADIATOR" refers to the KD-15 driver, which the same table lists as a '
            '"Passive cone radiator" beside the active woofer, not to the loudspeaker system.'
        ),
        'results': [
            (record + '.active', 'NOT_STATED',
             f'The {title} spec sheet publishes power handling and passive input terminals but never '
             'states passive/active, powered or built-in amplification. Field stays unverified.'),
        ],
    })

CHECKS.append({
    'url': HOST + 'Cornwall-2019-Spec-Sheet-v03.pdf',
    'sourceClass': 'MANUFACTURER',
    'document': 'Klipsch Cornwall IV spec sheet link',
    'chunksOpened': [0],
    'chunksTotal': 1,
    'evidence': (
        'The URL does not serve a document: the response is an S3 XML error, "<Code>AccessDenied</Code> '
        '<Message>Access Denied</Message>". No specification text is served, so the field cannot be '
        'assessed from this URL.'
    ),
    'results': [
        ('klipsch-cornwall-iv.active', 'INACCESSIBLE',
         'The spec-sheet URL returns an S3 AccessDenied error document instead of a PDF. Field left '
         'unchanged.'),
    ],
})
