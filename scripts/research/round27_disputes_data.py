#!/usr/bin/env python3
"""Round 27 (2026-10-19): disputed-record adjudication, verbatim evidence.

Every statement below was read from the document named in ``document`` after the
whole table/section was retrieved. Quotations are copied verbatim from the
retrieved text (whitespace normalised only). Nothing here is inferred from a
related model, a search snippet or a distributor copy.

Two kinds of record appear:

* CHECKS  - a URL was opened; each tied field gets an explicit outcome
            (PROMOTED / SUPPORTED_NOT_PROMOTED / NOT_STATED / CONFLICT).
* results may carry an optional fourth element (the value to write) and fifth
            element (the action: CORRECT, RESOURCE or RETRACT) when the document
            contradicts what the record currently stores.
"""

CHECKED_DATE = '2026-10-19'
ROUND = 27

# ---------------------------------------------------------------------------
# Documents opened in this batch
# ---------------------------------------------------------------------------

CHECKS = [
    {
        'url': 'https://www.adam-audio.com/en/s-series/s3v/',
        'sourceClass': 'MANUFACTURER',
        'document': 'ADAM Audio S3V product page (live manufacturer page, 3 chunks retrieved)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Driver complement: "9-inch Extended Linear Excursion (ELE) LF driver ... '
            '4-inch DCH mid-range driver ... S-ART folded-ribbon HF driver"; the specification '
            'panel repeats "German Handmade Precision S-ART Tweeter with HPS Waveguide / 4\\" Dome / '
            'Cone Hybrid (Carbon Composite) / 9\\" Woofer (Hexacone)". One woofer, one midrange and '
            'one tweeter: three transducers. The page also states internal amplification (500 W RMS '
            'bass, 300 W RMS mid, 50 W Class A/B tweeter) and "Total RMS Amp. Power: 850 W".'
        ),
        'results': [
            ('adam-audio-s3v.driverCount', 'PROMOTED',
             'The exact S3V page lists one 9-inch ELE woofer, one 4-inch DCH midrange and one S-ART '
             'tweeter: 3 transducers, matching the stored value.'),
        ],
    },
    {
        'url': 'https://www.adam-audio.com/en/sx-series/s3x-v/',
        'sourceClass': 'MANUFACTURER',
        'document': 'ADAM Audio S3X-V archived-product page (live, 2 chunks; Technical Data section read)',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Technical Data tables give per-section "Number" rows: Woofer "Number 1, Basket 9\\" (228 mm)"; '
            'Midrange "Number 1, Basket 4.5\\" (116 mm)"; Tweeter "Number 1, Type X-ART". '
            'Three transducers, one of each. The page is the archived S3X-V, not the S3V successor.'
        ),
        'results': [
            ('adam-s3x.driverCount', 'PROMOTED',
             'The S3X-V Technical Data tables state Number 1 for woofer, midrange and tweeter: '
             '3 transducers, matching the stored value.'),
        ],
    },
    {
        'url': 'https://www.adam-audio.com/en/a-series/a8h/',
        'sourceClass': 'MANUFACTURER',
        'document': 'ADAM Audio A8H product page (live, 3 chunks)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Page: "The A8H incorporates an 8-inch resonant Multi-Layer Mineral (MLM) fiber woofer, '
            'innovative midrange driver, and handmade precision X-ART tweeter"; bullets list '
            '"8\'\' Woofer (Multi-Layer Mineral)" and "3.5\\" DCH Midrange Driver". The page title is '
            '"A8H Active Studio Monitor (Midfield)", the introduction calls it "a 3-way speaker", and the '
            'specification panel gives "Total Peak Amp. Power: 340 W" with a "Hybrid Amplification" section.'
        ),
        'results': [
            ('adam-a8h.driverCount', 'PROMOTED',
             'One 8-inch MLM woofer, one 3.5-inch DCH midrange and one X-ART tweeter: 3 transducers, '
             'matching the stored value.'),
            ('adam-a8h.active', 'PROMOTED',
             'The exact page names the product an "Active Studio Monitor" and publishes internal '
             'amplification ("Total Peak Amp. Power: 340 W", hybrid amplification).'),
        ],
    },
    {
        'url': 'https://www.martinlogan.com/uploads/documents/brochures/brochure_motion40.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'MartinLogan Motion 40 brochure (single-page PDF, 1 chunk)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specifications: "High Frequency Driver 1\\" x 1.4\\" (2.6cm x 3.6cm) Folded Motion Transducer"; '
            '"Mid Frequency Transducer 5-1/2\\" (14cm) aluminum cone woofer"; "Low Frequency Transducer '
            'Two 6-1/2\\" (16.5cm) aluminum cone woofers". One tweeter + one midrange + two woofers = 4 '
            'drive units. The earlier queue note added these to 5; that arithmetic was wrong.'
        ),
        'results': [
            ('martinlogan-motion-40.driverCount', 'PROMOTED',
             'The brochure lists 1 Folded Motion tweeter + 1 midrange + two 6.5-inch woofers = 4 drive '
             'units, matching the stored value. The earlier "5 drive units" note was a mis-addition.'),
        ],
    },
    {
        'url': 'https://media.focal-naim.com/dam/scala-utopia-evo/fp_scala_utopia_evo_en.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Focal Scala Utopia Evo product data sheet (single-page PDF, 1 chunk)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specification table "Speakers" row: "11\\" (27cm) \'W\' woofer / Power Flower 61/2\\" (16.5cm) '
            '\'W\' midrange, with TMD suspension, with NIC motor / 11/16\\" (27mm) \'IAL2\' pure Beryllium '
            'inverted dome tweeter". One woofer, one midrange and one tweeter: 3 transducers. The "1", "2", '
            '"3" in the callouts are numbered feature markers, not quantities. No explicit passive/active '
            'wording appears anywhere in the sheet; only "Recommended amplifier power 50 - 500W".'
        ),
        'results': [
            ('focal-scala-utopia-evo.driverCount', 'PROMOTED',
             'The exact sheet lists one 27 cm woofer, one 16.5 cm midrange and one 27 mm tweeter = 3 '
             'transducers. The earlier CONFLICT note read the feature-callout numbers as quantities.'),
            ('focal-scala-utopia-evo.active', 'NOT_STATED',
             'The sheet gives only a recommended amplifier power range (50-500 W); it never states '
             'passive, active, powered or built-in amplification. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://jblpro.com/en-US/site_elements/jrx225-spec-sheet',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL JRX225 spec sheet (c)2013 JBL Professional (2-page PDF, 1 chunk)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specifications: "Low Frequency Driver: JBL M115-8A x 2"; "High Frequency Driver: JBL 2414H-C, '
            '1\\" exit compression driver mounted on Progressive Transition Waveguide"; "System Type: Dual 15\\" '
            '2-way, sound reinforcement speaker". Two woofers plus one compression driver = 3 transducers. '
            'The sheet says "passive" nowhere; it gives "Recommended Amplifier Power: 500-1000 watts @ 4 ohms", '
            'Speakon NL-4 and 1/4-inch inputs, and a 500 W power capacity.'
        ),
        'results': [
            ('jbl-jrx225.driverCount', 'PROMOTED',
             'The sheet lists "JBL M115-8A x 2" low-frequency drivers plus one 2414H-C compression driver: '
             '3 transducers, matching the stored value.'),
            ('jbl-jrx225.active', 'NOT_STATED',
             'The sheet publishes a recommended external amplifier range and passive-cabinet style inputs but '
             'never writes passive/active, powered or built-in amplification. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://usa.yamaha.com/products/audio_visual/speaker_systems/ns-6490/specs.html',
        'sourceClass': 'MANUFACTURER',
        'document': 'Yamaha NS-6490 specifications page, Yamaha Corporation of America (1 chunk)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specification table row "Driver": "8\\" Cone Woofer, 4\\" Cone Mid-Range, 7/8\\" Balanced Dome '
            'Tweeter" (three transducers). The same table gives "Nominal Impedance 8 ohms" for this US variant. '
            'The host is ESTABLISHED in source-host-allowlist.json (Yamaha Corporation of America), so the '
            'earlier note that withheld promotion pending a host decision is superseded.'
        ),
        'results': [
            ('yamaha-ns-6490.driverCount', 'PROMOTED',
             'The US manufacturer specification table lists an 8-inch woofer, a 4-inch midrange and a 7/8-inch '
             'tweeter: 3 transducers, matching the stored value. Host is ESTABLISHED (Yamaha Corporation of '
             'America); this is not evidence for any other regional variant.'),
        ],
    },
    {
        'url': 'https://international.kef.com/products/q750-floorstanding-speaker',
        'sourceClass': 'MANUFACTURER',
        'document': 'KEF Q750 product page, KEF International (3 chunks; specifications accordion read)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'Specifications "Drive Units": "165mm (6.5in.) aluminium Uni-Q / 25mm (1in.) vented aluminium dome '
            'HF / 165mm (6.5in.) aluminium LF / 2 x 165mm (6.5in.) aluminium ABR". The Uni-Q section contributes '
            'one MF cone and one HF dome; with the separate LF driver that is 3 driven transducers, plus two '
            'ABRs (passive radiators). The page gives only "Amplifier Requirements 15-150W" and never states '
            'passive, active, powered or built-in amplification.'
        ),
        'results': [
            ('kef-q750.driverCount', 'CORRECTED',
             'The page lists a Uni-Q (MF cone + HF dome), one LF driver and two ABRs. Under the convention '
             'already recorded for jbl-charge5, jbl-flip6 and klipsch-forte-iv, passive radiators are not '
             'counted as drivers, so the count is 3, not 5. The record\'s own note already stated that ABRs '
             'are not counted; the stored value contradicted it.', 3, 'CORRECT'),
            ('kef-q750.active', 'NOT_STATED',
             'Only a recommended amplifier power range (15-150 W) is given; no passive/active, powered or '
             'built-in amplification wording. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://www.adam-audio.com/en/archived-products/s3a/',
        'sourceClass': 'MANUFACTURER',
        'document': ('ADAM Audio S3A archived-product page and its linked operation manual '
                     '(adam-audio-user-manual-S3A-en-de.pdf, 6 chunks; introduction read)'),
        'chunksOpened': [0],
        'chunksTotal': 6,
        'evidence': (
            'The archived page has no specification table but links the exact S3A operation manual. The manual '
            'states: "The S3A is a three-way ported active system that uses a single ART tweeter, ensuring full '
            'compatibility with the latest expanded high frequency resolution media formats, and two '
            'HexaCone-bass/midrange drivers. One woofer acts as a full-range driver with the second woofer '
            'joining it only below 150 Hz". One tweeter + two bass/midrange drivers = 3 transducers. The A and B '
            'variants differ only in the left/right placement of the two woofers, not in driver count.'
        ),
        'results': [
            ('legacy-adam-1.driverCount', 'PROMOTED',
             'The exact S3A operation manual describes one ART tweeter and two HexaCone bass/midrange '
             'drivers = 3 transducers, matching the stored value. The provenance source is set to the manual '
             'because the archived page itself carries no specification table.'),
        ],
        'sourceOverride': 'https://www.adam-audio.com/content/uploads/2016/12/adam-audio-user-manual-S3A-en-de.pdf',
    },
    {
        'url': 'https://www.qscaudio.com/resource-files/productresources/spk/wideline_8/q_spk_wl8_usermanual.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'QSC WideLine-8 Series Loudspeaker System User Manual, TD-000237-00 rev D (4 chunks)',
        'chunksOpened': [0, 2],
        'chunksTotal': 4,
        'evidence': (
            'WL3082: "The WL3082 input connectors are a pair of Neutrik NL8\'s wired in parallel ... The WL3082 '
            'loudspeaker is not equipped with a crossover network. All signal processing must be done before '
            'connecting audio power to the loudspeaker." The manual documents only NL8/NL4 audio-power inputs, '
            'per-band nominal impedance and continuous power capacity; it lists no mains connection, no '
            'amplifier output rating and no gain/level control. WL212-sw: "The WL212-sw is equipped with two NL8 '
            'connectors with pins 1+ and 1- connected to the transducers", and "Its two ceramic magnet, 4\" voice '
            'coil, 12\" transducers provide 1100 watt continuous power handling capability." The subwoofer '
            'section never uses the words passive, active, powered or built-in amplification.'
        ),
        'results': [
            ('qsc-wl3082.active', 'PROMOTED',
             'The exact-model QSC manual states that "audio power" is connected to the loudspeaker and that it '
             'has no crossover network or internal processing; the only inputs are NL8 audio-power connectors. '
             'This is an explicit statement of the external-amplification signal path, so the stored passive '
             'value is retained and re-sourced from the specification sheet to the manual.', False, 'RESOURCE'),
            ('qsc-wl212-sw.active', 'NOT_STATED',
             'Neither the specification sheet nor the user manual states passive/active or built-in '
             'amplification for the WL212-sw; the manual only describes the NL8/NL4 wiring to the transducers '
             'and a 1100 W continuous power-handling capability. Under the standing explicit-evidence rule the '
             'Round 22 manufacturer-verified promotion is retracted and the field returns to unknown.', None, 'RETRACT'),
        ],
    },
]

# ---------------------------------------------------------------------------
# Value corrections that are not simple CITED -> VERIFIED promotions
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# JBL LSR32: verbatim Amplitude & Phase table from the owner's manual
# ---------------------------------------------------------------------------

LSR32_MANUAL = 'https://jblpro.com/zh/site_elements/lsr-series-owner-s-manual'
LSR32_TABLE = [
    (20, 70), (30, 80), (40, 86), (50, 90), (60, 92), (70, 93), (80, 93.5), (90, 93.5),
    (100, 93.5), (200, 93), (300, 93), (400, 93), (500, 93), (600, 93), (700, 92.5),
    (800, 92), (900, 92), (1000, 92.5), (2000, 92.5), (3000, 92.5), (4000, 92.5),
    (5000, 92.5), (6000, 92.5), (7000, 92.5), (8000, 92.5), (9000, 92.5), (10000, 92.5),
    (20000, 92),
]
LSR32_CONTEXT = (
    'Exact JBL LSR Series Owner\'s Manual, LSR32 "Amplitude & Phase" table, SPL (dB) column transcribed '
    'verbatim, 28 rows (20 Hz - 20 kHz). The manual states: "All measurements unless otherwise stated made '
    'anechoically at 2 meters and referenced to 1 meter by the inverse square law"; the microphone is '
    '"perpendicular to the centerline of the mid and high frequency transducers, at the point 55 mm (2.2 in.) '
    'below the center of the tweeter diaphragm". Drive level is not stated, so the series is used as normalised '
    'response shape only; absolute loudness comes from the verified sensitivity field. Published tolerance is '
    '+1/-1.5 dB (60 Hz - 22 kHz), -3 dB at 54 Hz and -10 dB at 35 Hz. No phase column is imported and no point '
    'is interpolated.'
)
LSR32_RESOLUTION_NOTE = (
    'Round 27 (2026-10-19): the 20 kHz self-conflict is resolved. The same manual\'s LSR32 Amplitude & Phase '
    'table reads 92 dB at 20 kHz and the LSR32 Acoustic Contribution fundamental table also reads 92 dB at '
    '20 kHz. The 61 dB value belongs to the LSR28P section (Amplitude and Phase, 61 dB at 10 kHz with a blank '
    '20 kHz row), not to the LSR32. The stored 27-row series was also not the LSR32 table: 12 of its 27 values '
    'differed (30, 40, 50, 70, 80, 300, 400, 500, 600, 700, 900, 1000 Hz) and it omitted the 20 kHz row. It has '
    'been replaced by the verbatim 28-row table; the superseded rows are preserved in this resolution record '
    'and in scripts/research/round27-value-history.json.'
)

# ---------------------------------------------------------------------------
# ELX200-15: edition comparison outcome (no value is written)
# ---------------------------------------------------------------------------

ELX = {
    'record': 'electro-voice-elx200-15',
    'frEdition': ('https://assets.electrovoicedynacord.com/asset/c2b9bf16-1e17-4053-847a-20773866d7f8/'
                  'ELX200-15-Engineering-Data-Sheet.pdf'),
    'enEdition': 'https://products.electrovoice.com/binary/ELX200-15_BDL_en.pdf',
    'facts': {
        'frRows': 86, 'enRows': 87, 'storedRows': 85, 'storedAlternateRows': 87,
        'frMissingHz': [2500], 'enMissingHz': [], 'storedMissingHz': [2400, 2600],
        'storedVsFrDiffs': 9, 'storedVsEnDiffs': 61, 'frVsEnSharedDiffs': 64,
        'frMinImpedanceOhm': 1.1, 'enMinImpedanceOhm': 6.5, 'statedMinImpedanceOhm': 7.0,
        'statedMinus3dB': '77 Hz - 16 kHz', 'statedMinus10dB': '52 Hz - 19 kHz',
        'frTableMinus3dB': '75 Hz - 13 kHz', 'frTableMinus10dB': '55 Hz - 17 kHz',
        'enTableMinus3dB': '80 Hz - 17 kHz', 'enTableMinus10dB': '55 Hz - 19 kHz',
    },
    'verdict': 'STILL_IRRECONCILABLE',
    'reason': (
        'Two official editions of the same sheet disagree with each other and with both stored series. The FR '
        'edition has 86 rows (2400 and 2600 Hz, no 2500 Hz); the EN edition has 87 rows (2400, 2500, 2600 Hz) and '
        '64 of the shared sensitivity values differ. The FR impedance column falls to 1.1 ohm, below the 7.0 ohm '
        'minimum the same sheet publishes; the EN column peaks at 110 ohm at 2500 Hz. The stored 85-point series '
        'matches neither edition (9 values differ from FR, 61 from EN, and it has 2500 Hz without 2400/2600). '
        'Text-derived -3 dB and -10 dB crossings from either table do not reproduce the stated 77 Hz-16 kHz / '
        '52 Hz-19 kHz limits, so the published limits cannot validate the tables either. Response data stays '
        'excluded from simulation; no series is adopted and no point is rewritten.'
    ),
}
