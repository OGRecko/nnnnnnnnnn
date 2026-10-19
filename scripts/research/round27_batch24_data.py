#!/usr/bin/env python3
"""Round 27 batch 24 (2026-10-19): Bose 901 Series VI and REL S/812.

Bose's owner guide has a "Technical information" page whose first row is "Transducer complement":
"Nine (9) 4 1/2" (11.4 cm) full-range Helical Voice Coil drivers in each cabinet".

The REL S/812 brochure prints "TYPE | Front-firing active woofer, down-firing passive radiator",
"ACTIVE DRIVER SIZE & MATERIAL | 12 in.", "PASSIVE RADIATOR SIZE & MATERIAL | 12 in.", and an
"AMPLIFIER TYPE | NextGen5 Class D" with "POWER OUTPUT | 800 watts (RMS)". One driven transducer;
the passive radiator is not counted (repository convention).

The brochure is served from REL's Shopify CDN; www.rel.net is the allowlisted REL host and the
recorded source, and it resolves to that copy.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
BOSE = 'https://products.bose.com/pdf/customer_service/owners/og_901.pdf'
REL = 'https://rel.net/wp-content/uploads/2019/08/S812-brochure.pdf'
JL = 'https://www.jlaudio.com/products/f113v2-gloss-home-audio-fathom-powered-subwoofers-96142'

CHECKS = [
    {
        'url': BOSE,
        'sourceClass': 'MANUFACTURER',
        'document': 'Bose 901 Series VI owner guide, Technical information',
        'chunksOpened': [1, 4, 6],
        'chunksTotal': 9,
        'evidence': (
            'Technical information page: "Bose® 901® Series VI Direct/Reflecting® Loudspeakers"; '
            '"Transducer complement | Nine (9) 4 1/2” (11.4 cm) full-range Helical Voice Coil drivers in '
            'each cabinet"; "Nominal impedance | 8Ω (ohms)"; "Amplifier compatibility | Compatible with '
            'amplifiers/receivers rated from 10 - 450 watts RMS. Rated 250 watts IEC".'
        ),
        'results': [
            ('bose-901-series-vi.driverCount', 'PROMOTED', 9,
             'The manual\'s own "Transducer complement" row states nine full-range drivers in each '
             'cabinet.'),
        ],
    },
    {
        'url': REL,
        'sourceClass': 'MANUFACTURER',
        'document': 'REL Acoustics S/812 brochure, SPECIFICATIONS',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            '"TYPE | Front-firing active woofer, down-firing passive radiator"; "ACTIVE DRIVER SIZE & '
            'MATERIAL | 12 in., 300 mm, long-throw, die cast Aluminium chassis"; "PASSIVE RADIATOR SIZE & '
            'MATERIAL | 12 in., 300mm, Carbon/Carbon flat cone structure, steel chassis"; "POWER OUTPUT | '
            '800 watts (RMS)"; "AMPLIFIER TYPE | NextGen5 Class D". The recorded rel.net URL answered '
            'with a redirect; the fetcher reported the final URL as '
            'https://cdn.shopify.com/s/files/1/0702/9293/0776/files/S812-brochure.pdf.'
        ),
        'results': [
            ('rel-s812.driverCount', 'PROMOTED', 1,
             'One front-firing 12-inch active driver. The down-firing 12-inch passive radiator is not a '
             'driven transducer and is not counted.'),
            ('rel-s812.active', 'PROMOTED', True,
             'The brochure specifies the subwoofer\'s own NextGen5 Class D amplifier at 800 W RMS along '
             'with its input and daisy-chain output connectors.'),
        ],
    },
    {
        'url': JL,
        'sourceClass': 'MANUFACTURER',
        'document': 'JL Audio Fathom f113v2 product page (recorded source)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'The URL now redirects to garmin.com, which presents a JL Audio brand landing page listing '
            'marine, motorsport, car and home ranges; no f113v2 product page or specification table is '
            'served. No value can be read from the recorded source.'
        ),
        'results': [],
    },
]
