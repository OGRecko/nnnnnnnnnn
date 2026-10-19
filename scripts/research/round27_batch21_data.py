#!/usr/bin/env python3
"""Round 27 batch 21 (2026-10-19): Marshall Acton III / Stanmore III / Woburn III - checked only.

Marshall publishes a POWER AMPLIFIERS block that names the amplifier feeding each transducer group
("One 30 Watt Class D amplifier for the woofer / Two 15 Watt Class D amplifiers for the tweeters").
It is tempting to read a driver complement out of that block, but the repository forbids it:
`src/data/speakers.test.ts` asserts `driverCount === null` for all three models with the message
"do not infer driver count from amplifier channels". The three URLs are recorded so they close,
with no value written.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
ACTON = 'https://www.marshall.com/gb/en/product/acton-iii'
STANMORE = 'https://www.marshall.com/gb/en/product/stanmore-iii'
WOBURN = 'https://www.marshall.com/gb/en/product/woburn-iii'

NOTE = ('The page prints per-transducer-group amplifier rows, not a transducer count; repository '
        'rule forbids deriving driverCount from amplifier channels.')

CHECKS = [
    {
        'url': ACTON,
        'sourceClass': 'MANUFACTURER',
        'document': 'Marshall Acton III product page, POWER AMPLIFIERS block',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"POWER AMPLIFIERS | One 30 Watt Class D amplifier for the woofer; Two 15 Watt Class D '
            'amplifiers for the tweeters"; "MAINS INPUT VOLTAGE 100–240 V". No row states how many '
            'drive units the cabinet contains.'
        ),
        'results': [],
    },
    {
        'url': STANMORE,
        'sourceClass': 'MANUFACTURER',
        'document': 'Marshall Stanmore III product page, POWER AMPLIFIERS block',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"POWER AMPLIFIERS | One 50 Watt Class D amplifier for the woofer; Two 15 Watt Class D '
            'amplifiers for the tweeters"; "The two-way driver system delivers a heavy but balanced '
            'sound". No row states the number of drive units.'
        ),
        'results': [],
    },
    {
        'url': WOBURN,
        'sourceClass': 'MANUFACTURER',
        'document': 'Marshall Woburn III product page, POWER AMPLIFIERS block',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"POWER AMPLIFIERS | One 90 Watt Class D amplifier for the woofer; Two 15W Class D amplifiers '
            'for the mids; Two 15 Watt Class D amplifiers for the tweeters". Channel groups are not a '
            'transducer count.'
        ),
        'results': [],
    },
]
