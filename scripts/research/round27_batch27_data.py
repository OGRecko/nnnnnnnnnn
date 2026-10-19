#!/usr/bin/env python3
"""Round 27 batch 27 (2026-10-19): Barefoot MicroMain27 and the Sonetto passive statement.

Barefoot Sound's own product page states the model is a "3.5-way active monitor" and its TECH SPECS
table lists the drive units (1 tweeter, two 5.25" midbass units, 2 x 10" subwoofers) with a power
amplifier for each - five driven transducers, no inference required.

The Sonus faber Sonetto collection page describes Sonetto I as "A compact passive bookshelf speaker"
and Sonetto II as "A passive bookshelf speaker", naming each model. The records carry no generation
suffix; both the first generation (whose owner's manual declares the family a passive loudspeaker
system) and the second generation (this page) are passive, so the statement settles the field either
way rather than transferring a value between different products.

The Olympica III page was opened as a possible driver-count source but now serves the current
"Olympica G3 III" generation while the record is the earlier Olympica III; the two generations are
different products, so no field was taken from it.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
BAREFOOT = 'https://barefootsound.com/micromain27/'
SONETTO_COLLECTION = 'https://www.sonusfaber.com/en/collections/sonetto'
OLYMPICA_III = 'https://www.sonusfaber.com/en/products/olympica-iii/tech-specs'

CHECKS = [
    {
        'url': BAREFOOT,
        'sourceClass': 'MANUFACTURER',
        'document': 'Barefoot Sound MicroMain27 product page and TECH SPECS table',
        'chunksOpened': [0, 1],
        'chunksTotal': 2,
        'evidence': (
            'Headline: "A 3.5-WAY ACTIVE STUDIO MONITOR WITH DUAL-FORCE™ AND MEME™ TECHNOLOGY"; body: '
            '"3.5-way active monitor", "1180 watts of power per monitor". TECH SPECS: Description "3.5-way '
            'active monitor with with Dual-Force™ and MEME™ Technologies"; Tweeter 1" ring radiator '
            '"Amplifier: 180W"; Midbass 1 and Midbass 2 5.25" cone, 250W each; Subwoofers "2 x 10" '
            'aluminum cone", 500W. The page also states "5 drive units" in its description of the model.'
        ),
        'results': [
            ('barefoot-micromain27.active', 'PROMOTED', True,
             'The exact model is described as an active monitor and every drive unit lists its own '
             'built-in amplifier (180 W, 250 W, 250 W, 500 W).'),
            ('barefoot-micromain27.driverCount', 'PROMOTED', 5,
             'One 1" tweeter, two 5.25" midbass drivers and two 10" subwoofers: five driven transducers, '
             'matching the page\'s own "5 drive units" statement.'),
        ],
    },
    {
        'url': SONETTO_COLLECTION,
        'sourceClass': 'MANUFACTURER',
        'document': 'Sonus faber Sonetto collection page, product cards',
        'chunksOpened': [0, 1],
        'chunksTotal': 2,
        'evidence': (
            'The collection page\'s product cards read: Sonetto I - "A compact passive bookshelf speaker '
            'ideal for smaller listening environments"; Sonetto II - "A passive bookshelf speaker with a '
            'deeply enriched low end bass response". The page introduces the collection as "the second '
            'generation of the Sonetto Collection".'
        ),
        'results': [
            ('sonus-faber-sonetto-i.active', 'PROMOTED', False,
             'The exact model is described by the manufacturer as a passive bookshelf speaker. The record '
             'has no generation suffix; the first-generation owner\'s manual also declares the family a '
             'passive loudspeaker system, so both generations agree.'),
            ('sonus-faber-sonetto-ii.active', 'PROMOTED', False,
             'The exact model is described by the manufacturer as a passive bookshelf speaker; the '
             'first-generation manual declares the same family passive, so the statement holds for either '
             'generation.'),
        ],
    },
    {
        'url': OLYMPICA_III,
        'sourceClass': 'MANUFACTURER',
        'document': 'Sonus faber "Olympica G3 III" technical specifications',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'The page is titled "Olympica G3 III" and lists Tw 28 mm DAD, Md 165 mm Camelia paper cone and '
            'W 2 x 165 mm paper cone (four transducers). The catalogue record is "Olympica III" without the '
            'G3 generation; a different generation is a different product, so no field is taken from it.'
        ),
        'results': [],
    },
]
