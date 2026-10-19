#!/usr/bin/env python3
"""Round 27 batch 9 (2026-10-19): Genelec 8020D and 8030C.

Both records carried no provenance at all. Each value comes from the model's own product page
technical-specification block, opened in this round.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27

CHECKS = [
    {
        'url': 'https://www.genelec.com/8020d',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8020D product page, "8020D Technical Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 5,
        'evidence': (
            'Technical Specifications: "Amplifier Power 50 W Bass (Class D) + 50 W Treble (Class D)"; '
            '"Driver Dimensions ⌀ 105 mm Bass + ⌀ 19 mm Treble"; 56 Hz - 25 kHz (-6 dB); '
            'connector "1 x XLR Analog Input".'
        ),
        'results': [
            ('genelec-8020d.driverCount', 'PROMOTED', 2,
             'Driver dimensions: ⌀ 105 mm bass + ⌀ 19 mm treble.'),
            ('genelec-8020d.active', 'PROMOTED', True,
             'On-board 50 W bass and 50 W treble Class D amplification with a line-level XLR input.'),
        ],
    },
    {
        'url': 'https://www.genelec.com/8030c',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8030C product page, "Technical Specifications"',
        'chunksOpened': [0, 1],
        'chunksTotal': 7,
        'evidence': (
            'Technical Specifications: "Amplifier Power 50 W Bass (Class D) + 50 W Treble (Class D)"; '
            '"Driver Dimensions ⌀ 130 mm Bass + ⌀ 19 mm Treble"; 47 Hz - 25 kHz (-6 dB).'
        ),
        'results': [
            ('genelec-8030c.driverCount', 'PROMOTED', 2,
             'Driver dimensions: ⌀ 130 mm bass + ⌀ 19 mm treble.'),
            ('genelec-8030c.active', 'PROMOTED', True,
             'On-board 50 W bass and 50 W treble Class D amplification.'),
        ],
    },
]
