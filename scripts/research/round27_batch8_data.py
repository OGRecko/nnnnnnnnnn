#!/usr/bin/env python3
"""Round 27 batch 8 (2026-10-19): DALI OBERON driver counts and the Genelec 8000/1032/SAM monitors.

Two separate situations:

* The DALI OBERON manual never printed Table 2 (the field was left NOT_EXTRACTED), but DALI's own
  technical-information PDF does print the driver table for all four models. That table is the source
  used here; the values already in the catalogue are confirmed, not invented.
* The Genelec records had no claim at all. Each value comes from the exact model's own datasheet,
  manual or product page, opened in this round.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
CDN = 'https://assets.ctfassets.net/4zjnzn055a4v/'

CHECKS = [
    {
        'url': 'https://www.dali-speakers.com/media/5341/techninformationen_dali_oberon.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'DALI OBERON technical information (Technische Information), table "TECHNISCHE DATEN"',
        'chunksOpened': [0, 1, 2],
        'chunksTotal': 3,
        'evidence': (
            'The closing "TECHNISCHE DATEN" table gives, per model, "Hochtöner: 1 x 29 mm φ Gewebekalotte" '
            'and "Tiefmitteltöner": OBERON 1 "1 x 130 mm φ (5 1/4\\")", OBERON 3 "1 x 180 mm φ (7\\")", '
            'OBERON 5 "2 x 130 mm φ (5 1/4\\")", OBERON 7 "2 x 180 mm φ (7\\")"; "Prinzip: 2-Wege" for all '
            'four. The accompanying text describes the OBERON 5 as having "zwei 130 mm (5 1/4\\") großen '
            'Holzfaser-Tiefmitteltönern" and the OBERON 7 as "zwei 180 mm (7\\") großen Tiefmitteltönern".'
        ),
        'results': [
            ('dali-oberon-3.driverCount', 'PROMOTED', 2,
             'Technical data table: 1 x 29 mm fabric-dome tweeter + 1 x 180 mm (7") wood-fibre '
             'mid/bass driver in a 2-way system. Confirms the value that was cited but not extractable '
             'from the manual.'),
            ('dali-oberon-5.driverCount', 'PROMOTED', 3,
             'Technical data table: 1 x 29 mm fabric-dome tweeter + 2 x 130 mm (5 1/4") wood-fibre '
             'mid/bass drivers in a 2-way system.'),
            ('dali-oberon7.driverCount', 'PROMOTED', 3,
             'Technical data table: 1 x 29 mm fabric-dome tweeter + 2 x 180 mm (7") wood-fibre '
             'mid/bass drivers in a 2-way system.'),
        ],
    },
    {
        'url': CDN + 'r3fD1Y5Q2x94TjJUvhZFk/cd8f56d80ca1cfbb48cbd8357a26e1de/8040B_datasheet_2023.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8040B datasheet (2023)',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            'Heading "8040B Active Monitoring System"; body: "The Genelec 8040B is a compact bi-amplified '
            'active monitor system". Drivers: "A 19 mm (3/4\\") metal dome tweeter" and "The 165 mm (6.5\\") '
            'bass cone driver"; "The bass and treble amplifiers produce 90 W of output power each".'
        ),
        'results': [
            ('genelec-8040b.driverCount', 'PROMOTED', 2,
             'Drivers section: 19 mm (3/4") metal dome tweeter + 165 mm (6.5") bass cone driver.'),
            ('genelec-8040b.active', 'PROMOTED', True,
             '"8040B Active Monitoring System", "compact bi-amplified active monitor system" with '
             'built-in 90 W bass and 90 W treble amplifiers.'),
        ],
    },
    {
        'url': CDN + '40XD9oi8UXnPIU4N6HS9CB/14c755715192ad67bb4dd8f2fa6a2ceb/GENELEC____________-8040b-8050b-______________________________________.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8040B / 8050B Operating Manual',
        'chunksOpened': [0],
        'chunksTotal': 8,
        'evidence': (
            'Manual title: "Genelec 8040B and 8050B Active Monitoring Systems". System section: "The '
            'GENELEC 8040B and 8050B are two way active monitoring loudspeakers ... Designed as active '
            'loudspeakers, they contain drivers, power amplifiers, active crossover filters and protection '
            'circuitry." Drivers: "The bass driver dimensions are 165 mm (6 1/2\\") and 205 mm (8\\") for '
            '8040B and 8050B respectively ... The high frequency driver is a 19 mm (3/4\\") metal dome on '
            'the 8040B and a 25 mm (1\\") metal dome on the 8050B."'
        ),
        'results': [
            ('legacy-gen-5.driverCount', 'PROMOTED', 2,
             '8050B: 205 mm (8") bass driver + 25 mm (1") metal dome high-frequency driver.'),
            ('legacy-gen-5.active', 'PROMOTED', True,
             'Manual title "8040B and 8050B Active Monitoring Systems"; "Designed as active loudspeakers, '
             'they contain drivers, power amplifiers, active crossover filters and protection circuitry."'),
        ],
    },
    {
        'url': 'https://www.genelec.com/previous-models/8351a',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8351A product page (technical specifications)',
        'chunksOpened': [0, 1],
        'chunksTotal': 4,
        'evidence': (
            'Technical Specifications: "Amplifier Power 150 W Bass (Class D) + 120 W Midrange (Class D) + '
            '90 W Treble (Class AB)"; "Driver Dimensions ⌀ 19 mm Treble + ⌀ 120 mm Midrange + 2 x H 100 x '
            'W 215 mm Bass". The model is presented as a "SAM™ Studio Monitor" (Smart Active Monitoring).'
        ),
        'results': [
            ('genelec-8351a.driverCount', 'PROMOTED', 4,
             'Driver dimensions: 19 mm treble + 120 mm midrange (coaxial pair) + two 100 x 215 mm '
             'racetrack bass drivers, i.e. four transducers.'),
            ('genelec-8351a.active', 'PROMOTED', True,
             'On-board amplification listed per band (150 W bass, 120 W midrange, 90 W treble) in a '
             'Genelec "Smart Active Monitoring (SAM™)" monitor.'),
        ],
    },
    {
        'url': CDN + '1CrttMuYgAaMuawMUAOOEu/2dbe47e74ff875175d05cc9f6f191cc9/genelec_8240_8250_8351_8260_opman.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 8240A / 8250A / 8351A / 8260A Operating Manual, SPECIFICATIONS table',
        'chunksOpened': [0, 4, 5],
        'chunksTotal': 11,
        'evidence': (
            'SPECIFICATIONS table, "Drivers" row: 8351A "Dual 8 1/2 x 4 in / 120 mm (5 in) Coax Al-cone / '
            '19 mm (3/4 in) Coax Al-dome"; 8260A "255 mm (10 in) / 120 mm (5 in) Coax Al-cone / 19 mm '
            '(3/4 in) Coax Al-dome". Amplifier row: 8351A 150 W bass + 120 W midrange + 90 W treble; '
            '8260A 150 W bass + 120 W midrange + 120 W treble. Back panel of the 8260A is labelled '
            '"8260A DSP TRI-AMPLIFIED MONITORING SYSTEM"; the manual states "The amplifier unit is mounted '
            'in the rear of the monitor enclosure."'
        ),
        'results': [
            ('genelec-8351a.driverCount', 'PROMOTED', 4,
             'Specifications: dual 8 1/2 x 4 in bass + 120 mm coaxial midrange + 19 mm coaxial treble.'),
            ('genelec-8351a.active', 'PROMOTED', True,
             'Specifications list three amplifier output powers (150 W bass, 120 W midrange, 90 W treble) '
             'mounted inside the monitor enclosure.'),
            ('genelec-8260a.driverCount', 'PROMOTED', 3,
             'Specifications: 255 mm (10 in) bass + 120 mm coaxial midrange + 19 mm coaxial treble.'),
            ('genelec-8260a.active', 'PROMOTED', True,
             'Back panel reads "8260A DSP TRI-AMPLIFIED MONITORING SYSTEM"; amplifier row lists 150 W '
             'bass + 120 W midrange + 120 W treble in the enclosure.'),
        ],
    },
    {
        'url': 'https://www.genelec.com/1032c',
        'sourceClass': 'MANUFACTURER',
        'document': 'Genelec 1032C product page (technical specifications)',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Technical Specifications: "Amplifier Power 250 W Bass (Class D) + 150 W Treble (Class D)"; '
            '"Driver Dimensions ⌀ 250 mm Bass + ⌀ 25 mm Treble". Feature text: "the 1032C now features '
            'digital connectivity, a universal power supply and powerful Class D amplification". Key '
            'technologies list "Active Crossovers" and "Smart Active Monitoring (SAM™)".'
        ),
        'results': [
            ('genelec-1032c.driverCount', 'PROMOTED', 2,
             'Driver dimensions: ⌀ 250 mm bass + ⌀ 25 mm treble.'),
            ('genelec-1032c.active', 'PROMOTED', True,
             'On-board 250 W bass and 150 W treble Class D amplification, "Active Crossovers" and '
             '"Smart Active Monitoring (SAM™)".'),
        ],
    },
]
