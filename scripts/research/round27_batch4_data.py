#!/usr/bin/env python3
"""Round 27 batch 4 (2026-10-19): driver complements on four manufacturer documents."""
CHECKED_DATE = '2026-10-19'
ROUND = 27
CHECKS = [
    {
        'url': 'https://dynaudio.com/discontinued-models/evidence/evidence-platinum',
        'sourceClass': 'MANUFACTURER',
        'document': 'Dynaudio Evidence Platinum discontinued-model page, Specifications block (3 chunks)',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specifications block: "Tweeter 2x 28mm Esotar2", "Midrange 2x15 cm MSP", "Woofer 4x18 cm MSP". '
            'Two tweeters + two midranges + four woofers = 8 drive units. The description confirms "Why use '
            'four woofers, housed in two separate cabinets" and "precisely positioned dual woofers, midrange '
            'drive units ... Esotar2 tweeters ... mirrored up the length of the ... baffle".'
        ),
        'results': [
            ('legacy-dyn-4.driverCount', 'PROMOTED',
             'The exact Dynaudio specification block states 2x 28 mm Esotar2 tweeter, 2x15 cm MSP midrange and '
             '4x18 cm MSP woofer: 8 drive units, matching the stored value.'),
        ],
    },
    {
        'url': 'https://www.dali-speakers.com/en-us/products/opticon-mk2/opticon-8-mk2/',
        'sourceClass': 'MANUFACTURER',
        'document': 'DALI OPTICON 8 MK2 product page (3 chunks)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Page: "The two 8\\" bass drivers and dedicated 6-1/2\\" midrange driver"; separately, "The OPTICON 8 '
            'MK2 hybrid tweeter module marries a 29 mm soft dome tweeter with a custom 17 x 45 mm planar element. '
            'Both drivers are mounted on a cast aluminium faceplate". Two bass drivers + one midrange + two '
            'hybrid-tweeter elements = 5 drive units.'
        ),
        'results': [
            ('dali-opticon-8-mk2.driverCount', 'PROMOTED',
             'The exact page enumerates two 8-inch bass drivers, one 6.5-inch midrange and a hybrid tweeter '
             'module that "marries a 29 mm soft dome tweeter with a custom 17 x 45 mm planar element. Both '
             'drivers are mounted...": 5 drive units, matching the stored value.'),
        ],
    },
    {
        'url': 'https://www.martinlogan.com/en/product/electromotion-esl-x',
        'sourceClass': 'MANUFACTURER',
        'document': 'MartinLogan ElectroMotion ESL X product page (3 chunks)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Page: "The ElectroMotion ESL X features a new larger XStat electrostatic transducer ... Twin '
            '8-inch high-excursion woofers are housed in a non-resonant asymmetrical bass reflex (ported) '
            'chamber". One electrostatic panel plus two 8-inch woofers = 3 drive units. The same page also '
            'describes "a naturally dipolar radiation pattern".'
        ),
        'results': [
            ('martinlogan-esl-x.driverCount', 'PROMOTED',
             'The exact page states one XStat electrostatic transducer plus "Twin 8-inch high-excursion '
             'woofers": 3 drive units, matching the stored value.'),
        ],
    },
    {
        'url': 'https://www.sony.com/electronics/support/sound-bars-home-theater-systems-sound-bars-surround-speakers/ht-a7000/specifications',
        'sourceClass': 'MANUFACTURER',
        'document': 'Sony HT-A7000 specifications page, Sony USA (single page)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'The page lists "Amplifier Channels 11ch", "Amplifier Type Digital Amplifier, S-Master HX", '
            '"Speaker Structure 7.1.2ch (Built-in Subwoofer)" and "Subwoofer Type Built-in". It does not '
            'enumerate loudspeaker drive units anywhere, so the stored value of 11 reproduces the amplifier '
            'channel count rather than a documented driver complement.'
        ),
        'results': [
            ('sony-sony-ht-a7000.driverCount', 'RETRACTED',
             'The specifications page states 11 amplifier channels and a 7.1.2-channel speaker structure, but '
             'never enumerates drive units. The stored 11 is the amplifier channel count, not a documented '
             'driver complement, so the value is removed rather than kept as an unsupported inference.', None,
             'RETRACT'),
        ],
    },
]
