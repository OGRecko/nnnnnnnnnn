#!/usr/bin/env python3
"""Round 27 batch 23 (2026-10-19): JBL 4429, JBL L112 and Klipsch RP-8000F driver complements.

Three documents that enumerate their transducers row by row:

- the JBL 4429 product page has a "General Specifications" table with one row each for the
  low-frequency, high-frequency and ultrahigh-frequency transducer;
- the JBL L112 instruction manual has a COMPONENTS section with a LOW FREQUENCY, a MIDRANGE and a
  HIGH FREQUENCY paragraph naming one transducer each (and a matching removal procedure per driver);
- the Klipsch RP-8000F specification sheet has one HIGH FREQUENCY DRIVER row (1" tweeter) and one
  LOW FREQUENCY DRIVER row ("Dual 8" ... Woofers").

None of the three prints a passive/active classification, so `active` is left alone.
The JBL 4429 page also carries a second, contradictory "Audio Specifications" block (2 kHz / 5 kHz
crossovers, 93 dB); that conflict affects fields other than the driver list and is recorded here
rather than used.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
J4429 = 'https://www.jbl.com/4429.html'
L112 = 'https://support.jbl.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dweb63c766/pdfs/L112_OM_EN.pdf'
RP8000F = 'https://assets.klipsch.com/product-specsheets/RP-8000F_Spec-Sheet_v01.pdf'

CHECKS = [
    {
        'url': J4429,
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL 4429 product page, General Specifications',
        'chunksOpened': [0],
        'chunksTotal': 2,
        'evidence': (
            '"12”, 3-way Studio Monitor"; "Low-frequency transducer | 300mm pure-pulp cone woofer '
            '1200FE-8"; "High-frequency transducer | 50mm titanium diaphragm 175Nd-3"; '
            '"Ultrahigh-frequency transducer | 19mm titanium diaphragm 138Nd". The page additionally '
            'prints a second, conflicting "Audio Specifications" block (crossovers 2kHz/5kHz, '
            'sensitivity 93dB) that is not used here.'
        ),
        'results': [
            ('jbl-4429.driverCount', 'PROMOTED', 3,
             'One low-frequency, one high-frequency and one ultrahigh-frequency transducer, each with '
             'its own row and model number.'),
        ],
    },
    {
        'url': L112,
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL L112 instruction manual, COMPONENTS section',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            '"LOW FREQUENCY—A 300 mm (12 in) driver with a 4.7 kg (10¼ lb) magnetic assembly"; '
            '"MIDRANGE—The 130 mm (5 in) midrange loudspeaker, housed within an isolated subchamber"; '
            '"HIGH FREQUENCY—Designed specifically for the L112, the new 25 mm (1 in) high frequency dome '
            'radiator". The COMPONENT REMOVAL procedure likewise describes removing one low frequency, '
            'one midrange and one high frequency unit.'
        ),
        'results': [
            ('jbl-l112.driverCount', 'PROMOTED', 3,
             'One 300 mm low-frequency driver, one 130 mm midrange and one 25 mm high-frequency dome.'),
        ],
    },
    {
        'url': RP8000F,
        'sourceClass': 'MANUFACTURER',
        'document': 'Klipsch RP-8000F specification sheet',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'SPECIFICATIONS table: "HIGH FREQUENCY DRIVER | 1\\" Titanium LTS Vented Tweeter with Hybrid '
            'Cross-Section Tractrix® Horn"; "LOW FREQUENCY DRIVER | Dual 8\\" Cerametalic Cone Woofers".'
        ),
        'results': [
            ('klipsch-rp8000f.driverCount', 'PROMOTED', 3,
             'One 1-inch high-frequency driver plus "Dual 8\\" " low-frequency woofers.'),
        ],
    },
]
