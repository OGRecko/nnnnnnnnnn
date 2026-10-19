#!/usr/bin/env python3
"""Round 27 batch 20 (2026-10-19): Meyer Sound LINA and LEOPARD.

Meyer Sound's own datasheets state the design in words - "The loudspeaker shall be a compact,
self-powered, linear, low-distortion, line array loudspeaker" - and then enumerate the
transducers and the internal amplifier. The host docs.meyersound.com was added to the
source-host allowlist in this batch with the documentation portal as operator evidence.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
LINA = 'https://docs.meyersound.com/products/en/datasheet---lina.html'
LEOPARD = 'https://docs.meyersound.com/products/en/datasheet---leopard---leopard-m80.html'

CHECKS = [
    {
        'url': LINA,
        'sourceClass': 'MANUFACTURER',
        'document': 'Meyer Sound LINA datasheet, Specifications and Architectural Specifications',
        'chunksOpened': [1],
        'chunksTotal': 3,
        'evidence': (
            'TRANSDUCERS: "Low Frequency | Two 6.5-inch long-excursion cone drivers; 4 Ω nominal '
            'impedance"; "High Frequency | One 3-inch diaphragm compression driver coupled to a '
            'constant-directivity horn through a patented REM® manifold; 8 Ω nominal impedance". '
            'AMPLIFIER: "Type | 3-channel, Class-D"; "Total Output Power | 1950 W peak". Architectural '
            'specification: "The loudspeaker shall be a compact, self-powered, linear, low-distortion, '
            'line array loudspeaker."'
        ),
        'results': [
            ('meyer-sound-lina.driverCount', 'PROMOTED', 3,
             'Two 6.5-inch low-frequency cone drivers plus one 3-inch compression driver.'),
            ('meyer-sound-lina.active', 'PROMOTED', True,
             'Datasheet states the cabinet is "self-powered" and documents its internal 3-channel '
             'class-D amplifier and AC power section.'),
        ],
    },
    {
        'url': LEOPARD,
        'sourceClass': 'MANUFACTURER',
        'document': 'Meyer Sound LEOPARD / LEOPARD-M80 datasheet, Specifications and Architectural Specifications',
        'chunksOpened': [1, 2],
        'chunksTotal': 3,
        'evidence': (
            'TRANSDUCERS: "Low Frequency | Two 9-inch long-excursion cone drivers; 2 Ω nominal '
            'impedance"; "High Frequency | One 3-inch diaphragm compression driver coupled to a '
            'constant-directivity horn through a patented REM® manifold; 4 Ω nominal impedance". '
            'AMPLIFIERS: "Type | 3-channel, open-loop, class D"; "Total Output Power | 3900 W peak". '
            'Architectural specification: "The loudspeaker shall be a compact, self-powered, linear, '
            'low-distortion, line array loudspeaker."'
        ),
        'results': [
            ('meyer-sound-leopard.driverCount', 'PROMOTED', 3,
             'Two 9-inch low-frequency cone drivers plus one 3-inch compression driver.'),
            ('meyer-sound-leopard.active', 'PROMOTED', True,
             'Datasheet states the cabinet is "self-powered" and documents its internal 3-channel '
             'class-D amplifier and AC power section.'),
        ],
    },
]
