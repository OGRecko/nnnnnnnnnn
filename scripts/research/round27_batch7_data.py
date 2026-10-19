#!/usr/bin/env python3
"""Round 27 batch 7 (2026-10-19): Genelec active monitors and the PreSonus Eris E8 XT.

Every record below had both fields UNSOURCED (no claim at all). Each value comes from the
exact model's own datasheet or product page, opened in this round. Active status is taken
from the manufacturer's own words ("Active Monitoring System", "bi-amplified active monitor
system", "2-Way Active Studio Monitor"), not inferred from the presence of a mains inlet.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
BI = 'https://www.genelec.com/previous-models/'
CDN = 'https://assets.ctfassets.net/4zjnzn055a4v/'

CHECKS = [
    {
        'url': CDN + 'n5pJxfnNVm8eqKuWCsSeA/7eb8afbf22d64f536bfc447c9ec0ae89/8050A_datasheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8050A datasheet',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Heading "8050A Active Monitoring System"; body: "The Genelec 8050A is a powerful '
            'bi-amplified active monitor system". Drivers: "25 mm (1\") metal dome tweeter" and '
            '"205 mm (8\") bass cone driver". Amplifiers "150 and 120 watts of output power each".'
        ),
        'results': [
            ('genelec-8050a.driverCount', 'PROMOTED', 2,
             'Drivers section: 25 mm (1") metal dome tweeter + 205 mm (8") bass cone driver.'),
            ('genelec-8050a.active', 'PROMOTED', True,
             'Sheet title "8050A Active Monitoring System" and text "bi-amplified active monitor '
             'system", with 150 W bass / 120 W treble amplifiers.'),
        ],
    },
    {
        'url': CDN + 'xjY6MIRReKqGu48sSkgEe/390d8f322adbae6773953b1c121078b8/8030A_datasheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8030A datasheet',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Heading "8030A Active Monitoring System"; body: "The Genelec 8030A is a very compact '
            'bi-amplified active monitor system". Drivers: "19 mm (3/4\") metal dome tweeter" and '
            '"130 mm (5\") bass cone driver"; "The bass and treble amplifiers produce 40 W of output '
            'power each".'
        ),
        'results': [
            ('genelec-8030a.driverCount', 'PROMOTED', 2,
             'Drivers section: 19 mm (3/4") metal dome tweeter + 130 mm (5") bass cone driver.'),
            ('genelec-8030a.active', 'PROMOTED', True,
             'Sheet title "8030A Active Monitoring System" and "bi-amplified active monitor system", '
             'with separate 40 W bass and treble amplifiers.'),
        ],
    },
    {
        'url': CDN + '671bY6aA8wCWeOuyc8SOYO/67d2bc20c4299aa8404be6a62080a5aa/1030A_datasheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 1030A datasheet',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Text: "The Genelec 1030A is a very compact bi-amplified active monitoring system ... two '
            'power amplifiers, one for each driver". Drivers: "19 mm (3/4\") metal dome driver" and '
            '"high efficiency 170 mm (6 1/2\") polymer composite cone driver"; bass and treble '
            'amplifiers "produce 80 Watts and 50 Watts of short term power".'
        ),
        'results': [
            ('genelec-1030a.driverCount', 'PROMOTED', 2,
             'Drivers section: 19 mm (3/4") metal dome driver + 170 mm (6 1/2") polymer composite '
             'cone bass driver.'),
            ('genelec-1030a.active', 'PROMOTED', True,
             '"bi-amplified active monitoring system" with two power amplifiers, one per driver, '
             'built into the enclosure.'),
        ],
    },
    {
        'url': CDN + '5C4rCdOHwAIWM6yoQ24s6q/4091d26f60d3e5e1669800d8fdc1f625/1032A_datasheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 1032A datasheet',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Cover reads "1032A Bi-amplified Active Monitoring System"; system section: "two-way active '
            'monitoring system including ... multiple power amplifiers and active, low signal level '
            'crossover". System specifications list exactly two entries under "Drivers": "Bass 250 mm '
            '(10") cone" and "Treble 25 mm (1") metal dome", followed by "Both drivers are magnetically '
            'shielded".'
        ),
        'results': [
            ('genelec-1032a.driverCount', 'PROMOTED', 2,
             'Specifications list two drivers: Bass 250 mm (10") cone + Treble 25 mm (1") metal dome, '
             'with the note "Both drivers are magnetically shielded".'),
            ('genelec-1032a.active', 'PROMOTED', True,
             'Cover and system text: "Bi-amplified Active Monitoring System", with multiple power '
             'amplifiers and an active low-level crossover.'),
        ],
    },
    {
        'url': CDN + '7547Y1zhZuQeaO68yMCYGe/98dd2e2995803eae08cddc2709797e38/1029A_datasheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 1029A datasheet',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Heading "1029A Active Monitoring System"; text: "very compact bi-amplified active monitor '
            'system ... two power amplifiers, one for each driver". Drivers: "19 mm (3/4\") metal dome '
            'tweeter" and "130 mm (5\") woofer ... bass cone driver"; bass and treble amplifiers 40 W each.'
        ),
        'results': [
            ('genelec-1029a.driverCount', 'PROMOTED', 2,
             'Drivers section: 19 mm (3/4") metal dome tweeter + 130 mm (5") bass cone woofer.'),
            ('genelec-1029a.active', 'PROMOTED', True,
             'Sheet title "1029A Active Monitoring System" and "bi-amplified active monitor system", '
             'with two power amplifiers, one per driver.'),
        ],
    },
    {
        'url': 'https://www.presonus.com/products/eris-e8-xt-monitor',
        'sourceClass': 'MANUFACTURER',
        'document': 'PreSonus Eris E8 XT product page',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Overview heading: "2-Way Active Studio Monitor with EBM Waveguide". Features: "8-inch woven '
            'composite low-frequency transducer", "1.25-inch (32 mm), ultra-low-mass, silk-dome, '
            'high-frequency transducer", "140 Watt, Class AB bi-amplification drives up to 105 dB of '
            'sound". Specs: LF Transducers "8" Reinforced Woofer", HF Transducers "1.25" Silk Dome '
            'Tweeter", crossover 2.2 kHz, balanced XLR/TRS and RCA line inputs.'
        ),
        'results': [
            ('presonus-eris-e8.driverCount', 'PROMOTED', 2,
             'Features list exactly two transducers: 8-inch woven composite low-frequency transducer and '
             '1.25-inch silk-dome high-frequency transducer.'),
            ('presonus-eris-e8.active', 'PROMOTED', True,
             'Overview heading "2-Way Active Studio Monitor"; "140 Watt, Class AB bi-amplification"; '
             'line-level inputs only.'),
        ],
    },
]
