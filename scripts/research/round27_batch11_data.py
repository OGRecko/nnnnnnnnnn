#!/usr/bin/env python3
"""Round 27 batch 11 (2026-10-19): Mackie CR-X driver counts and the JBL 3 Series MkII monitors.

The Mackie owner's manual prints one specification table covering CR3-X, CR4-X and CR5-X:
each model has one polypropylene woofer and the shared 19 mm silk-dome tweeter.

For JBL, each product page's headline states the model's woofer size and "Two-Way", and the features
list states "Dual integrated, custom Class-D amplifiers". The 306P and 308P pages reuse the 305P's
body paragraph verbatim, including its "long-throw 5\\" woofer" sentence; that sentence is a template
error on those two pages and is NOT used here. The headline and the dual-amplifier statement are.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27

CHECKS = [
    {
        'url': 'https://mackie.com/img/file_resources/CR-X_Series_OM.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': "Mackie CR-X Series Owner's Manual, \"Appendix B: Technical Information\"",
        'chunksOpened': [0, 3],
        'chunksTotal': 5,
        'evidence': (
            '"CR-X Series Specifications": "Low Frequency | 3.0 in / 76 mm [CR3-X]"; "Low Frequency | '
            '4.0 in / 102 mm [CR4-X]"; "Low Frequency | 5.0 in / 127 mm [CR5-X]"; "Polypropylene-coated '
            'woofer"; "High Frequency | 0.75 in / 19 mm ferrofluid-cooled silk-dome tweeter"; "Crossover '
            'Frequency | 3.0 kHz"; "Rated Power | 50 watts peak [CR3-X, CR4-X] / 80 watts peak [CR5-X]".'
        ),
        'results': [
            ('mackie-cr3-x.driverCount', 'PROMOTED', 2,
             'One 3.0 in (76 mm) polypropylene woofer plus the shared 0.75 in (19 mm) silk-dome tweeter.'),
            ('mackie-cr4-x.driverCount', 'PROMOTED', 2,
             'One 4.0 in (102 mm) polypropylene woofer plus the shared 0.75 in (19 mm) silk-dome tweeter.'),
            ('mackie-cr5-x.driverCount', 'PROMOTED', 2,
             'One 5.0 in (127 mm) polypropylene woofer plus the shared 0.75 in (19 mm) silk-dome tweeter.'),
        ],
    },
    {
        'url': 'https://jblpro.com/en/products/305p-mkii',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional 305P MkII product page',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Headline: "Powered 5\\" Two-Way Studio Monitor". Body: "a long-throw 5\\" woofer" and "the '
            'woven-composite 1\\" Neodymium tweeter". Features: "Dual integrated, custom Class-D amplifiers '
            'provide 82 watts of power".'
        ),
        'results': [
            ('jbl-305p-mkii.driverCount', 'PROMOTED', 2,
             'A 5" woofer and a 1" neodymium tweeter in a two-way system.'),
            ('jbl-305p-mkii.active', 'PROMOTED', True,
             '"Powered ... Studio Monitor" with dual integrated custom Class-D amplifiers (82 W).'),
        ],
    },
    {
        'url': 'https://jblpro.com/en/products/306p-mkii',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional 306P MkII product page',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Headline: "Powered 6\\" Two-Way Studio Monitor". Features: "Dual integrated, custom Class-D '
            'amplifiers provide 112 watts of power". Limitation: the body paragraph is copied verbatim from '
            'the 305P page and still says "long-throw 5\\" woofer"; that sentence contradicts the headline '
            'and was not used.'
        ),
        'results': [
            ('jbl-306p-mkii.driverCount', 'PROMOTED', 2,
             'Headline specifies a 6" two-way monitor and the features list two amplifiers, one per '
             'transducer. The copied "5 inch woofer" sentence in the body was disregarded.'),
            ('jbl-306p-mkii.active', 'PROMOTED', True,
             '"Powered ... Studio Monitor" with dual integrated custom Class-D amplifiers (112 W).'),
        ],
    },
    {
        'url': 'https://jblpro.com/en/products/308p-mkii',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Professional 308P MkII product page',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Headline: "Powered 8\\" Two-Way Studio Monitor". Features: "Dual integrated, custom Class-D '
            'amplifiers provide 112 watts of power". Limitation: the same copied body paragraph says '
            '"long-throw 5\\" woofer"; not used.'
        ),
        'results': [
            ('jbl-308p-mkii.driverCount', 'PROMOTED', 2,
             'Headline specifies an 8" two-way monitor and the features list two amplifiers, one per '
             'transducer. The copied "5 inch woofer" sentence in the body was disregarded.'),
            ('jbl-308p-mkii.active', 'PROMOTED', True,
             '"Powered ... Studio Monitor" with dual integrated custom Class-D amplifiers (112 W).'),
        ],
    },
]
