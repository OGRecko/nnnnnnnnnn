#!/usr/bin/env python3
"""Round 27 batch 18 (2026-10-19): JBL Control 1 (vintage) driver complement.

JBL's own archive specification sheet enumerates the transducers in two places - the feature
list ("Components: 135 mm (5 1/4 in) low frequency loudspeaker, 19 mm (3/4 in) polycarbonate
dome tweeter") and the architectural specification that begins "The loudspeaker system shall
consist of a 135 mm low-frequency transducer, 19 mm dome high-frequency transducer ...".

The sheet prints nominal impedance (4 ohms) and power capacity, but no passive/active
classification, so `active` is deliberately not written (see round 27 batch 15).
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
C1 = 'https://jblpro.com/en-US/site_elements/vintage-control-1-spec-sheet'

CHECKS = [
    {
        'url': C1,
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL Control 1 miniature loudspeaker system specification sheet (archive)',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"Components: 135 mm (5 1/4 in) low frequency loudspeaker, 19 mm (3/4 in) polycarbonate dome '
            'tweeter". Architectural specification: "The loudspeaker system shall consist of a 135 mm '
            '(5 1/4 in) low-frequency transducer, 19 mm (3/4 in) dome high-frequency transducer, and '
            'frequency dividing network installed in a ported enclosure." No passive/active row.'
        ),
        'results': [
            ('jbl-control-1.driverCount', 'PROMOTED', 2,
             'Specification sheet lists exactly one low-frequency and one high-frequency transducer.'),
        ],
    },
]
