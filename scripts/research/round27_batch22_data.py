#!/usr/bin/env python3
"""Round 27 batch 22 (2026-10-19): Celestion and Jensen guitar loudspeakers.

A guitar speaker sold as a component is one loudspeaker chassis, not a multi-way system. The
manufacturer pages used here describe a single chassis by construction - one nominal diameter,
one magnet (weight and type), one voice coil (diameter and material), one cone/basket - and the
product title is a singular "12 inch 60W Guitar Speaker". So `driverCount` is one, read off the
page's own single-chassis specification block rather than inferred from a cabinet or a sibling.

The Eminence Legend Series collection URL recorded on `eminence-legend` now returns 404; it is
recorded as inaccessible and no value is written from it.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
V30 = 'https://celestion.com/product/vintage-30/'
GB = 'https://celestion.com/product/g12m-greenback/'
G12H = 'https://celestion.com/product/g12h-anniversary/'
P12N = 'https://www.jensentone.com/specification-sheet/38'
P10R = 'https://www.jensentone.com/specification-sheet/36'
EMINENCE = 'https://eminence.com/collections/legend-series'

SINGLE = ('The product is one loudspeaker chassis: the page prints a single nominal diameter, one '
          'magnet (type and weight), one voice coil (diameter and material), one cone and one basket. '
          'No second transducer or crossover is documented.')

CHECKS = [
    {
        'url': V30,
        'sourceClass': 'MANUFACTURER',
        'document': 'Celestion Vintage 30 product page, Specifications',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Page title "Celestion Vintage 30 - 12 inch 60W Guitar Speaker"; strapline "12-inch guitar '
            'speaker with complex overtones". Specifications block: "Nominal diameter 305mm / 12in"; '
            '"Power rating 60W"; "Chassis type Pressed steel"; "Magnet type Ceramic"; "Magnet weight '
            '1.42kg / 50oz"; "Voice coil diameter 1.75in / 44mm"; "Frequency range 70-5000Hz". '
            'Mounting information lists "Number of mounting holes 4" for the single chassis.'
        ),
        'results': [
            ('celestion-v30.driverCount', 'PROMOTED', 1, SINGLE),
        ],
    },
    {
        'url': GB,
        'sourceClass': 'MANUFACTURER',
        'document': 'Celestion G12M Greenback product page, Specifications',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Page title "Celestion G12M Greenback - 12 inch 25W Guitar Speaker"; strapline "12-inch rock '
            'guitar speaker". Specifications block: "Nominal diameter 305mm / 12in"; "Power rating 25W"; '
            '"Chassis type Pressed steel"; "Magnet type Ceramic"; "Magnet weight 0.99kg / 35oz"; '
            '"Voice coil diameter 1.75in / 44mm"; "Frequency range 75-5000Hz".'
        ),
        'results': [
            ('celestion-greenback.driverCount', 'PROMOTED', 1, SINGLE),
        ],
    },
    {
        'url': G12H,
        'sourceClass': 'MANUFACTURER',
        'document': 'Celestion G12H Anniversary product page, Specifications',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Page title "Celestion G12H Anniversary - 12 inch 30W Guitar Speaker". Specifications block: '
            '"Nominal diameter 305mm / 12in"; "Power rating 30W"; "Chassis type Pressed steel"; "Magnet '
            'type Ceramic"; "Magnet weight 1.42kg / 50oz"; "Voice coil diameter 1.75in / 44mm"; '
            '"Frequency range 75-5000Hz". This is the page already recorded as the exact source for the '
            'record\'s sensitivity, power, impedance and woofer fields.'
        ),
        'results': [
            ('celestion-g12h30.driverCount', 'PROMOTED', 1, SINGLE),
        ],
    },
    {
        'url': P12N,
        'sourceClass': 'MANUFACTURER',
        'document': 'Jensen P12N specification sheet',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Page heading "Specification Sheet - P12N"; strapline "12\\" - 50 W Vintage Alnico '
            'Loudspeaker". One chassis table: "Nominal Overall Diameter 307 mm / 12 in"; "Nominal Voice '
            'Coil Diameter 38 mm / 1.5 in"; "Magnet Alnico"; "Voice Coil Winding Copper"; "Cone Material '
            'Paper"; "Basket Material Pressed Sheet Steel".'
        ),
        'results': [
            ('jensen-p12n.driverCount', 'PROMOTED', 1, SINGLE),
        ],
    },
    {
        'url': P10R,
        'sourceClass': 'MANUFACTURER',
        'document': 'Jensen P10R specification sheet',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Page heading "Specification Sheet - P10R"; strapline "10\\" - 25 W Vintage Alnico '
            'Loudspeaker". One chassis table: "Nominal Overall Diameter 259 mm / 10 in"; "Nominal Voice '
            'Coil Diameter 25 mm / 0.98 in"; "Magnet Alnico"; "Cone Material Paper"; "Basket Material '
            'Pressed Sheet Steel".'
        ),
        'results': [
            ('jensen-p10r.driverCount', 'PROMOTED', 1, SINGLE),
        ],
    },
    {
        'url': EMINENCE,
        'sourceClass': 'MANUFACTURER',
        'document': 'Eminence Legend Series collection page (recorded source)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'The URL now returns "404 Not Found - Eminence Speaker, LLC" with the body "Page not found / '
            'Looks like the page you\'re looking for no longer exists." No specification content is served.'
        ),
        'results': [],
    },
]
