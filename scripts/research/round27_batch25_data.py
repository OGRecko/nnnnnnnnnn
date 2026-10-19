#!/usr/bin/env python3
"""Round 27 batch 25 (2026-10-19): DALI OBERON 1 and OBERON 9; two dead ends recorded.

DALI's discontinued-product pages are still served from www.dali-speakers.com and print the
driver rows explicitly. OBERON 1: 2-way, 1 x 29 mm soft dome + 1 x 5 1/4 inch. OBERON 9: 3-way,
1 x 29 mm soft dome + 2 x 9 inch + 1 x 7 inch = 4 transducers.

Neither page states passive/active in the opened text (only nominal impedance and a recommended
amplifier-power range), so `active` stays CITED_IN_NOTES_UNCHECKED despite the value being false.

The Sonus faber first-generation Sonetto manual was located and opened. Its declaration calls the
system passive, but the technical-information table (section 6, page 34) did not extract to text in
the opened chunks, and the document is served from the brand's Storyblok CMS (a.storyblok.com),
which the host policy does not treat as a manufacturer host. No field is written.

Electro-Voice's Tour X product URLs no longer resolve: the na/en product page redirects to the
current electrovoice.com homepage, and the la/en path returns the Application Gateway 404. The
distributor copy remains the only opened support for those counts, so nothing is promoted from it.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
DALI1 = 'https://www.dali-speakers.com/en-us/products/discontinued/oberon/oberon-1/'
DALI9 = 'https://www.dali-speakers.com/en-us/products/discontinued/oberon/oberon-9/'
SONETTO = 'https://a.storyblok.com/f/259299/x/a134a54e57/owners_sonetto_148x210_low.pdf'
EV_TX1122 = 'https://products.electrovoice.com/na/en/tx1122'

CHECKS = [
    {
        'url': DALI1,
        'sourceClass': 'MANUFACTURER',
        'document': 'DALI OBERON 1 discontinued-product page, Specifications',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specifications: "Crossover Principle | 2-way"; "High Frequency Driver(s) | 1 x 29 mm soft '
            'dome"; "Low/Mid Frequency Driver(s) | 1 x 5¼ inch"; "Nominal Impedance [ohms] | 6"; '
            '"Recommended Amp. Power [watts] | 25 - 100". The page does not use the words passive, '
            'active, powered or built-in amplification.'
        ),
        'results': [
            ('dali-oberon-1.driverCount', 'PROMOTED', 2,
             'One 29 mm soft-dome HF driver plus one 5¼-inch low/mid driver: two driven transducers.'),
            ('dali-oberon-1.active', 'NOT_STATED', False,
             'The page lists a recommended amplifier-power range and nominal impedance but never states '
             'passive/active, powered/unpowered or built-in amplification. Field stays unverified.'),
        ],
    },
    {
        'url': DALI9,
        'sourceClass': 'MANUFACTURER',
        'document': 'DALI OBERON 9 discontinued-product page, Specifications',
        'chunksOpened': [0, 1],
        'chunksTotal': 3,
        'evidence': (
            'Specifications: "Crossover Principle | 3-way"; "Low/Mid Frequency Driver(s) | 2 x 9 inch / '
            '1 x 7 inch"; "High Frequency Driver(s) | 1 x 29 mm soft dome"; "Nominal Impedance [ohms] | '
            '4"; "Recommended Amp. Power [watts] | 50 - 400". The page does not use the words passive, '
            'active, powered or built-in amplification.'
        ),
        'results': [
            ('dali-oberon-9.driverCount', 'PROMOTED', 4,
             'Two 9-inch bass drivers, one 7-inch midrange and one 29 mm soft-dome HF driver: four driven '
             'transducers.'),
            ('dali-oberon-9.active', 'NOT_STATED', False,
             'The page lists a recommended amplifier-power range and nominal impedance but never states '
             'passive/active, powered/unpowered or built-in amplification. Field stays unverified.'),
        ],
    },
    {
        'url': SONETTO,
        'sourceClass': 'NON_MANUFACTURER_HOST',
        'document': 'Sonus faber Sonetto (first generation) owner manual, Italian and English sections',
        'chunksOpened': [0, 1, 2, 4, 5, 7],
        'chunksTotal': 9,
        'coverage': 'Six of nine chunks opened; the section 6 technical table did not extract to text.',
        'evidence': (
            'Contents: "6 Dati tecnici / 6 Technical information ... 34". The declaration of conformity '
            'covers "diffusori acustici passivi / passive loudspeaker system ... Sonetto modelli VIII, V, '
            'III, II, I, Center I, Center II, Wall". The technical-information table itself (section 6, '
            'page 34) is not present in the extracted text of any opened chunk; no driver row could be '
            'read. The PDF is served from a.storyblok.com, a multi-tenant CMS host that the source-host '
            'allowlist does not treat as a Sonus faber manufacturer host.'
        ),
        'results': [],
    },
    {
        'url': EV_TX1122,
        'sourceClass': 'MANUFACTURER',
        'document': 'Electro-Voice TX1122 product page (recorded manufacturer URL)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'The URL redirects to https://www.electrovoice.com/, the current brand homepage, which no '
            'longer lists the Tour X family. The la/en path was also tried and returned the Application '
            'Gateway 404 page. No TX1122 specification or driver row is served at the recorded path.'
        ),
        'results': [],
    },
]
