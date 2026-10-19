#!/usr/bin/env python3
"""Round 27 batch 28 (2026-10-19): Lumina I passive statement; Martin Audio CDD12.

The Sonus faber Lumina collection page describes the exact model: "Lumina I - A two-way passive
bookshelf speaker ideal for smaller listening environments." That promotes `active` (the stored value
was already false, but it was only cited in notes, never checked against an exact-model statement).

Martin Audio's CDD12 page states the model is "a compact, passive two-way system" three times (lead
paragraph, Features, Specification TYPE) and lists a 12" LF driver plus a coaxially mounted 1" exit HF
compression driver: two driven transducers. Neither field had a value before this batch.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
LUMINA_COLLECTION = 'https://www.sonusfaber.com/en/collections/lumina'
CDD12 = 'https://martin-audio.com/products/loudspeakers/cdd12'

CHECKS = [
    {
        'url': LUMINA_COLLECTION,
        'sourceClass': 'MANUFACTURER',
        'document': 'Sonus faber Lumina collection page, product cards',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Product card for the exact model: "Lumina I ... A two-way passive bookshelf speaker ideal '
            'for smaller listening environments." (The Lumina II card in the same list does not use the '
            'word passive, so only Lumina I is promoted here.)'
        ),
        'results': [
            ('sonus-faber-lumina-i.active', 'PROMOTED', False,
             'The exact model is described by the manufacturer as a two-way passive bookshelf speaker.'),
        ],
    },
    {
        'url': CDD12,
        'sourceClass': 'MANUFACTURER',
        'document': 'Martin Audio CDD12 product page',
        'chunksOpened': [0],
        'chunksTotal': 4,
        'evidence': (
            'Lead: "The CDD12 is a compact, passive two-way system". Features: "Compact, CDD™ passive '
            'two-way system". Specification: TYPE "Compact, high-output, Coaxial Differential Dispersion '
            'passive two-way system"; DRIVER "LF: 12" (300mm) ... HF: 1" (25mm) exit ... compression '
            'driver"; CROSSOVER "1.9kHz passive"; NOMINAL IMPEDANCE 8Ω.'
        ),
        'results': [
            ('martin-audio-cdd12.active', 'PROMOTED', False,
             'The page states three times that the exact model is a passive two-way system, and the '
             'crossover is described as passive.'),
            ('martin-audio-cdd12.driverCount', 'PROMOTED', 2,
             'One 12-inch low-frequency driver plus one coaxially mounted 1-inch compression driver: two '
             'driven transducers.'),
        ],
    },
]
