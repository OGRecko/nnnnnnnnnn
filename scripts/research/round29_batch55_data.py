#!/usr/bin/env python3
"""Round 29 batch 55 (2026-10-19): NS-1000M, SC207 and BX5 D3 from owner-facing documents.

Three studio monitors where the same document settles both open fields: the drive complement and whether
the box is powered.

`yamaha-ns1000m` and `m-audio-bx5` are written at MANUFACTURER_VERIFIED from the maker's own PDF/page.
`eve-audio-sc207` is written at THIRD_PARTY_VERIFIED: EVE Audio's product page carries no specification
table and only links to a PDF that is served from their Webflow asset host, so the document is genuine but
the host is not eve-audio.com.
"""
DATE = '2026-10-19'
ROUND = 29

YAM = 'https://usa.yamaha.com/files/download/other_assets/5/333935/NS-1000M.pdf'
MAD = 'https://www.m-audio.com/monitors-headphones/bx5d3.html'
EVE = ('https://cdn.prod.website-files.com/64e73b2facaf3da66d66c009/'
       '65818de121e0eb407e084dbb_EveAudio_SpecSheet_SC207_EN.pdf')

WHY_EVE = ('eve-audio.com/products/sc207 has no specification table in the page body; the only technical '
           'document it offers is this PDF, which is served from EVE Audio\'s Webflow asset host '
           '(cdn.prod.website-files.com) rather than from eve-audio.com.')

YAM_DOC = 'Yamaha NS-1000 / NS-1000M Owner\'s Manual'
MAD_DOC = 'M-Audio BX5-D3 product page and specifications table'
EVE_DOC = 'EVE Audio "SC207 - Spec sheet" (English)'

PROMOTIONS = [
    {'record': 'yamaha-ns1000m', 'field': 'driverCount', 'value': 3, 'source': YAM,
     'sourceType': 'MANUFACTURER', 'document': YAM_DOC,
     'note': ('Round 29 (2026-10-19): Yamaha NS-1000/NS-1000M Owner\'s Manual, Specifications — "Type | '
              'Infinite baffle, 3-way system"; Speaker Complement "Woofer | 30 cm cone type (JA-3058)/'
              'NS-1000M: (JA-3058A)", "Squawker | 8.8 cm dome type (JA-0801)", "Tweeter | 3 cm dome type '
              '(JA-0513)". Three transducers, and the manual distinguishes the M variant by its woofer.'),
     'append': (' Round 29 (2026-10-19): driverCount 3 verified from the Yamaha NS-1000/NS-1000M Owner\'s '
                'Manual ("3-way system"; JA-3058A woofer, JA-0801 squawker, JA-0513 tweeter).')},
    {'record': 'yamaha-ns1000m', 'field': 'active', 'value': False, 'source': YAM,
     'sourceType': 'MANUFACTURER', 'document': YAM_DOC,
     'note': ('Round 29 (2026-10-19): Yamaha NS-1000/NS-1000M Owner\'s Manual, "Connecting the Amplifier" — '
              '"Connect the input terminal on the rear of the speaker to the output terminal on the '
              'amplifier with the speaker cord which is included. Make sure the amplifier is turned off." '
              'Impedance section: "If a transistor amplifier is used, the speakers can be connected without '
              'giving any consideration to impedance." The speaker is driven from an external amplifier and '
              'the manual describes no mains inlet or built-in amplifier.'),
     'append': (' Round 29 (2026-10-19): active false verified from the Yamaha NS-1000/NS-1000M Owner\'s '
                'Manual, which instructs the user to connect the speaker terminals to an external amplifier '
                'and describes no built-in amplifier or mains inlet.')},
    {'record': 'eve-audio-sc207', 'field': 'driverCount', 'value': 2, 'source': EVE,
     'sourceType': 'THIRD_PARTY', 'document': EVE_DOC, 'whyNotManufacturer': WHY_EVE,
     'note': ('Round 29 (2026-10-19): EVE Audio SC207 spec sheet — heading "Active 2-Way 7 in Studio '
              'Monitor"; Specification Chart "Tweeter | AMT RS2" and "Mid-Woofer | 165mm/6.5 in". Two '
              'transducers.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the EVE Audio SC207 spec sheet '
                '("Active 2-Way"; AMT RS2 tweeter and 165 mm mid-woofer).')},
    {'record': 'eve-audio-sc207', 'field': 'active', 'value': True, 'source': EVE,
     'sourceType': 'THIRD_PARTY', 'document': EVE_DOC, 'whyNotManufacturer': WHY_EVE,
     'note': ('Round 29 (2026-10-19): EVE Audio SC207 spec sheet — "Active 2-Way 7 in Studio Monitor"; '
              'Specification Chart "Number of amplifiers | 2", "Output power (woofer) | 100W", "Output '
              'power (tweeter) | 50W", and a "Power consumption" block. Built-in amplification, so the '
              'monitor is powered.'),
     'append': (' Round 29 (2026-10-19): active true verified from the EVE Audio SC207 spec sheet, which '
                'lists two built-in amplifiers (100 W woofer, 50 W tweeter) and describes the product as '
                '"Active 2-Way".')},
    {'record': 'm-audio-bx5', 'field': 'driverCount', 'value': 2, 'source': MAD,
     'sourceType': 'MANUFACTURER', 'document': MAD_DOC,
     'note': ('Round 29 (2026-10-19): M-Audio BX5-D3 specifications table — "Type | 2-way near-field studio '
              'reference monitors"; "Low Freq. Driver | 5 inch (127mm) Kevlar curved cone with high '
              'temperature voice coil and damped rubber surround"; "High Freq. Driver | 1 inch (25mm) '
              'magnetically shielded natural silk dome". Two transducers.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the M-Audio BX5-D3 specification table '
                '("2-way near-field studio reference monitors"; 5-inch Kevlar woofer and 1-inch silk dome '
                'tweeter).')},
    {'record': 'm-audio-bx5', 'field': 'active', 'value': True, 'source': MAD,
     'sourceType': 'MANUFACTURER', 'document': MAD_DOC,
     'note': ('Round 29 (2026-10-19): M-Audio BX5-D3 product page — "Driving the BX5-D3 monitors are two '
              'Class A/B internal amplifiers that power the woofer and tweeter separately"; key feature '
              '"Bi-amplified design with 100 watts (60 LF, 40 HF)"; the specification table lists "Power | '
              'Voltage: 100-120V, 50/60 Hz / 220-240V, 50/60 Hz" and an "external mains fuse". Built-in '
              'amplification with mains power.'),
     'append': (' Round 29 (2026-10-19): active true verified from the M-Audio BX5-D3 page, which describes '
                '"two Class A/B internal amplifiers" and lists mains voltage and fuse specifications.')},
]

HOSTS = {EVE: 'cdn.prod.website-files.com'}
