#!/usr/bin/env python3
"""Round 27 batch 10 (2026-10-19): Yamaha DXR / DXR mkII / DBR powered loudspeakers.

Nine records that carried neither a value nor a provenance entry. Both pages are Yamaha's own
professional-audio specification tables; each model's "Speaker type" row states "2-way, Bi-amp
powered speaker" and the "Components" rows enumerate exactly one low-frequency cone and one
high-frequency compression driver.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27

DXR = 'https://usa.yamaha.com/products/proaudio/speakers/dxr/specs.html'
DBR = 'https://usa.yamaha.com/products/proaudio/speakers/dbr/specs.html'

CHECKS = [
    {
        'url': DXR,
        'sourceClass': 'MANUFACTURER',
        'document': 'Yamaha USA, DXR mkII Series / DXR Series specifications table',
        'chunksOpened': [0, 1],
        'chunksTotal': 2,
        'evidence': (
            'Both tables print the same structure per column. mkII: "Speaker type | 15\\" 2-way, Bi-amp '
            'powered speaker, Bass-reflex type" (also 12\\", 10\\", 8\\"); "Components LF | Diameter:15\\" cone, '
            'Voice Coil:2.5\\", Magnet:Ferrite"; "HF | Diaphragm:1.75\\", Type: 1\\" throat compression driver, '
            'Magnet:Neodymium"; "Output power | Dynamic:1100W (LF: 950W HF: 150W)". DXR: "Speaker type | '
            '12\\" 2-way, Bi-amp powered speaker, Bass-reflex type" (also 15\\", 10\\", 8\\"); "HF | Diaphragm:1.4\\", '
            'Type: 1\\" throat compression driver, Magnet:Ferrite"; "Output power | Dynamic:1100W (LF: 950W '
            'HF: 150W) / Continuous: 700W (LF: 600W HF: 100W)".'
        ),
        'results': [
            ('yamaha-dxr8.driverCount', 'PROMOTED', 2,
             '"8\\" 2-way ... powered speaker"; one 8" cone LF driver plus one 1" throat compression driver.'),
            ('yamaha-dxr8.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr10.driverCount', 'PROMOTED', 2,
             '"10\\" 2-way ... powered speaker"; one 10" cone LF driver plus one 1" throat compression driver.'),
            ('yamaha-dxr10.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr12.driverCount', 'PROMOTED', 2,
             '"12\\" 2-way ... powered speaker"; one 12" cone LF driver plus one 1" throat compression driver.'),
            ('yamaha-dxr12.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr15.driverCount', 'PROMOTED', 2,
             '"15\\" 2-way ... powered speaker"; one 15" cone LF driver plus one 1" throat compression driver.'),
            ('yamaha-dxr15.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr10mkii.driverCount', 'PROMOTED', 2,
             '"10\\" 2-way ... powered speaker"; one 10" cone LF driver plus one 1.75" diaphragm / 1" throat '
             'compression driver.'),
            ('yamaha-dxr10mkii.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr12mkii.driverCount', 'PROMOTED', 2,
             '"12\\" 2-way ... powered speaker"; one 12" cone LF driver plus one 1.75" diaphragm / 1" throat '
             'compression driver.'),
            ('yamaha-dxr12mkii.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
            ('yamaha-dxr15mkii.driverCount', 'PROMOTED', 2,
             '"15\\" 2-way ... powered speaker"; one 15" cone LF driver plus one 1.75" diaphragm / 1" throat '
             'compression driver.'),
            ('yamaha-dxr15mkii.active', 'PROMOTED', True,
             '"Bi-amp powered speaker" with built-in output power (LF 950 W / HF 150 W dynamic).'),
        ],
    },
    {
        'url': DBR,
        'sourceClass': 'MANUFACTURER',
        'document': 'Yamaha USA, DBR series specifications table',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            '"Speaker type | 2-way, Bi-amp powered speaker, Bass-reflex type" for DBR15, DBR12 and DBR10; '
            '"Components LF | Diameter:15\\" cone, Voice Coil:2.5\\", Magnet:Ferrite" (DBR15) and '
            '"Diameter:12\\" cone, Voice Coil:2\\", Magnet:Ferrite" (DBR12); "HF | Diaphragm:1.4\\", Type: 1\\" '
            'throat compression driver, Magnet:Ferrite"; "Output power | Dynamic:1000 W (LF: 800 W, HF: 200 W)".'
        ),
        'results': [
            ('yamaha-dbr12.driverCount', 'PROMOTED', 2,
             'One 12" cone LF driver plus one 1.4" diaphragm / 1" throat compression driver.'),
            ('yamaha-dbr12.active', 'PROMOTED', True,
             '"2-way, Bi-amp powered speaker" with built-in output power (LF 800 W / HF 200 W dynamic).'),
            ('yamaha-dbr15.driverCount', 'PROMOTED', 2,
             'One 15" cone LF driver plus one 1.4" diaphragm / 1" throat compression driver.'),
            ('yamaha-dbr15.active', 'PROMOTED', True,
             '"2-way, Bi-amp powered speaker" with built-in output power (LF 800 W / HF 200 W dynamic).'),
        ],
    },
]
