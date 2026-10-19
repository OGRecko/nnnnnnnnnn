#!/usr/bin/env python3
"""Round 27 batch 9 (2026-10-19): Genelec 8020D/8030C and QSC KS112/KLA12/KLA181.

Every record here had either no provenance at all or only an UNSOURCED marker. Each value comes
from the exact model's own technical-specification block or manufacturer datasheet, opened in this
round. Documents that describe a *different* revision or product are listed at the end of the batch
note in RESEARCH-STATUS-ROUND27.md; they were not used.
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
    {
        'url': 'https://www.qscaudio.com/solutions-products/loudspeakers/portable/powered/subwoofers/ks-series/ks112/',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC KS112 product page, "Specifications"',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Introduction: "The KS112 is an ultra-compact active subwoofer ... a highly portable, '
            'single 12-inch bandpass design subwoofer, powered by a 2000 Watt peak power Class D '
            'amplifier module." Specification table: "Configuration | 6th-Order Bandpass Subwoofer"; '
            '"LF Transducer | 305 mm (12 in), Cone"; "Amplifier | Class D 2000W (peak)".'
        ),
        'results': [
            ('qsc-ks112.driverCount', 'PROMOTED', 1,
             'Single low-frequency transducer: "LF Transducer 305 mm (12 in), Cone"; no high-frequency '
             'device is listed in the specification table.'),
            ('qsc-ks112.active', 'PROMOTED', True,
             '"active subwoofer ... powered by a 2000 Watt peak power Class D amplifier module"; the '
             'specification table lists the amplifier as built into the product.'),
        ],
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/kla/q_spk_kla_specs.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC KLA Series specification sheet (KLA12 / KLA181)',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"The KLA Series is comprised of two models: the KLA12 12-inch, 2-way loudspeaker and the '
            'KLA181 18-inch subwoofer. The KLA12 features a highly efficient 500 W x 500 W power amp '
            'module and the KLA181 offers the same highly efficient power amp module in a 1000 W '
            'configuration." Specification table: KLA12 "Configuration | 2-way Line Array Element", '
            '"Low-Frequency | 12\\" cone transducer", "High-Frequency | 1.75\\" diaphragm compression '
            'driver", "Power Output | 500 W x 500 W power module"; KLA181 "Configuration | 18\\" ported '
            'subwoofer", "Low-Frequency | 18\\" cone transducer", "High-Frequency | —", "Power Output | '
            '1000 W power module". Both list powerCON AC In/Out and a balanced line-level XLR input.'
        ),
        'results': [
            ('qsc-kla12.driverCount', 'PROMOTED', 2,
             'KLA12: one 12" cone low-frequency transducer plus one 1.75" diaphragm compression driver.'),
            ('qsc-kla12.active', 'PROMOTED', True,
             '"500 W x 500 W power module" built into the enclosure; the sheet calls the KLA Series a '
             '"fixed arcuate, active line array system" and lists powerCON AC In/Out.'),
            ('qsc-kla181.driverCount', 'PROMOTED', 1,
             'KLA181: a single 18" cone low-frequency transducer; the high-frequency row is "—".'),
            ('qsc-kla181.active', 'PROMOTED', True,
             '"1000 W power module" built into the enclosure, with powerCON AC In/Out and a balanced '
             'line-level XLR input.'),
        ],
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/e/e110/q_spk_e_110_specsheet.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC E110 specification sheet ("Two-Way Passive Loudspeaker")',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Title: "E110 Two-Way Passive Loudspeaker". Specification table: "Configuration: 1 x 10-inch, '
            '2-way, non-powered"; "LF 254 mm (10-inch) driver with 64 mm 2.5-inch) voice coil"; "HF 25 mm '
            '(1-inch) exit, 45 mm (1.75-inch) voice coil, compression driver"; input connectors "2 x NL4 '
            '1 x barrier strip" with no mains inlet.'
        ),
        'results': [
            ('qsc-e110.driverCount', 'PROMOTED', 2,
             'One 254 mm (10-inch) low-frequency driver plus one 25 mm (1-inch) exit compression driver.'),
            ('qsc-e110.active', 'PROMOTED', False,
             'Configuration is "non-powered"; the input plate carries NL4/barrier-strip speaker-level '
             'inputs only and the sheet directs the user to QSC GXD/PLD amplifiers.'),
        ],
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/e/e115/q_spk_e_115_specs.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC E115 specification sheet ("15-inch Two-Way Passive Loudspeaker")',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Title: "E115 15-inch Two-Way Passive Loudspeaker". Specification table: "Configuration | '
            '1 x 15-inch, 2-way, passive"; "LF | 381 mm / 15-inch driver with 89 mm 3.5-inch voice coil"; '
            '"HF | 38 mm / 1.5-inch exit, 71 mm / 2.8-inch voice coil, compression driver"; input connectors '
            '"2 x NL4 1 x barrier strip".'
        ),
        'results': [
            ('qsc-e115.driverCount', 'PROMOTED', 2,
             'One 381 mm (15-inch) low-frequency driver plus one 38 mm (1.5-inch) exit compression driver.'),
            ('qsc-e115.active', 'PROMOTED', False,
             'Configuration is "passive" and the document is titled "Passive Loudspeaker"; speaker-level '
             'NL4/barrier-strip inputs only.'),
        ],
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/e/e215/q_spk_e_215_specs.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC E215 specification sheet ("Dual 15-inch Two-Way Passive Loudspeaker")',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Title: "Dual 15-inch Two-Way Passive Loudspeaker". Specification table: "Configuration: | 2 x '
            '15-inch, 2-way, non-powered"; "LF | 2 x 381 mm (15-inch) driver with 89 mm (3.5-inch) voice '
            'coil"; "HF | 38 mm (1.5-inch) exit, 71 mm (2.8-inch) voice coil, compression driver".'
        ),
        'results': [
            ('qsc-e215.driverCount', 'PROMOTED', 3,
             'Two 381 mm (15-inch) low-frequency drivers plus one 38 mm (1.5-inch) exit compression driver.'),
            ('qsc-e215.active', 'PROMOTED', False,
             'Configuration is "non-powered"; the input plate is NL4/barrier strip only and the sheet '
             'points to external QSC GXD/PLD amplification.'),
        ],
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/ad/q_spk_adc_820_821_specs.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC AD-C820/C821 AcousticDesign ceiling loudspeaker specification sheet (09/21/2020)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specification table: "Configuration | Passive"; "Transducers Low-frequency 8\" (203 mm) ferrite '
            'woofer / High-frequency 1.4\" (36 mm) neodymium compression driver"; "Nominal Impedance 16Ω"; '
            '"Power Rating RMS Power Handling 200 W"; the 1.4" compression driver "fires through the center '
            'of the woofer".'
        ),
        'results': [
            ('qsc-ad-c820.driverCount', 'PROMOTED', 2,
             'One 8" (203 mm) ferrite woofer plus one 1.4" (36 mm) neodymium compression driver in a coaxial '
             '2-way arrangement.'),
            ('qsc-ad-c820.active', 'PROMOTED', False,
             'Configuration is "Passive"; the sheet lists 70V/100V transformer taps and a 16 Ω nominal '
             'impedance with "Recommended Max Amp Power 400 W" rather than on-board amplification.'),
        ],
    },
]
