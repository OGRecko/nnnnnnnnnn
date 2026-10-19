#!/usr/bin/env python3
"""Round 27 batch 26 (2026-10-19): ATC SCM45A Pro driver count; KEF legacy dead ends.

The ATC page lists "Drivers: HF 1"/25mm Dual-Suspension 'S-Spec', Mid 3"/75mm Soft Dome,
LF 6.5"/164mm short-coil carbon paper cone" - three driven transducers - and describes the
model as an "active 3-way studio monitor". The active field was already verified; this batch
promotes the count that the earlier round recorded as supported but not promoted.

KEF's legacy product URLs no longer serve data: /products/ls50 redirects to the JS-driven
Product Archive page, and the US LS50, Reference 1 and Reference 5 product paths return KEF's
404. No value is taken from those pages.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
ATC = 'https://atc.audio/professional/loudspeakers/scm45a-pro/'
KEF_LS50_INTL = 'https://international.kef.com/products/ls50'
KEF_LS50_US = 'https://us.kef.com/products/ls50'
KEF_REF1_US = 'https://us.kef.com/products/reference-1'
KEF_REF5_US = 'https://us.kef.com/products/reference-5'

CHECKS = [
    {
        'url': ATC,
        'sourceClass': 'MANUFACTURER',
        'document': 'ATC SCM45A Pro product page, Drivers and Specification',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Overview: "Mid-size very high performance active 3-way studio monitor". Drivers row: '
            '"HF 1″/25mm Dual-Suspension \'S-Spec\', Mid 3″/75mm Soft Dome, LF 6.5″/164mm short-coil '
            'carbon paper cone". Amplifier output: "Bass 150W rms, Mid 60W rms, High 25W rms"; crossover '
            'frequencies 380 Hz and 3.5 kHz.'
        ),
        'results': [
            ('atc-scm45a-pro.driverCount', 'PROMOTED', 3,
             'The exact-model Drivers row names one HF, one mid and one LF transducer: three driven '
             'transducers.'),
        ],
    },
    {
        'url': KEF_LS50_INTL,
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF International LS50 product path',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'The path redirects to https://international.kef.com/pages/product-archive. The archive page '
            'only offers a drop-down selector ("Initial Product Archive......") and serves no LS50 '
            'specification, driver row or datasheet in the opened text.'
        ),
        'results': [],
    },
    {
        'url': KEF_LS50_US,
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF US LS50 product path',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': 'The URL returns KEF\'s "404 Not Found" page. No product data is served.',
        'results': [],
    },
    {
        'url': KEF_REF1_US,
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF US Reference 1 product path',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': 'The URL returns KEF\'s "404 Not Found" page. No product data is served.',
        'results': [],
    },
    {
        'url': KEF_REF5_US,
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF US Reference 5 product path',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': 'The URL returns KEF\'s "404 Not Found" page. No product data is served.',
        'results': [],
    },
]
