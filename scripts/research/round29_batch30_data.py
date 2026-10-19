#!/usr/bin/env python3
"""Round 29 batch 30 (2026-10-19): manufacturer-host queue processing.

Every document below was opened in this session. Outcomes:

  legacy-yam-3 driverCount 3  -> PROMOTED, ca.yamaha.com NS-5000/NS-690 history page:
                                 "The NS-690, equipped with a soft-dome tweeter and midrange, was introduced
                                 in 1973 ... both speaker systems shared the same 30 cm (12") 3-way
                                 bookshelf design" and, for the NS-5000 lineage, "all three drivers".
                                 The NS-690 is a three-way system with a 30 cm woofer, a midrange and a
                                 tweeter: three transducers.
  kef-q150 / kef-q350 active   -> NOT_STATED. The pages give "Amplifier Requirements 10-100W" (a
                                 recommended amplifier range) and never state passive/powered.
  marshall 1936                -> INACCESSIBLE retry: the manufacturer URL still returns "Page not found".
  legacy-yam-2 (NS-10M)        -> INACCESSIBLE retry: hub.yamaha.com article returns 404.
  elac-uni-fi-ub5 driverCount  -> left unresolved: "3-way" plus a concentric tweeter/midrange unit makes
                                 the transducer count ambiguous (2 drive units vs 3 transducers).

No other value is written. The Klipsch Cornwall sheet (S3 AccessDenied) and the KEF archive PDFs remain
inaccessible from earlier checks and are not re-attempted here.
"""
DATE = '2026-10-19'
ROUND = 29
YAMAHA_HISTORY = 'https://ca.yamaha.com/en/audio/home-audio/explore/ns-5000/history.html'
KEF_Q150 = 'https://international.kef.com/products/q150-bookshelf-speaker'
KEF_Q350 = 'https://international.kef.com/products/q350-bookshelf-speaker'
MARSHALL = 'https://www.marshall.com/us/en/product/1936-2x12-cabinet?pid=1007263'
YAMAHA_HUB = 'https://hub.yamaha.com/proaudio/recording/a-history-of-yamaha-studio-monitors/'
ELAC = 'https://cdn.elac.com/uploads/2016/08/29132944/Uni-Fi-Sell-Sheet.pdf'

PROMOTION = {
    'record': 'legacy-yam-3',
    'field': 'driverCount',
    'value': 3,
    'source': YAMAHA_HISTORY,
    'note': ('Round 29 (2026-10-19): Yamaha history page — "The NS-690, equipped with a soft-dome tweeter '
             'and midrange, was introduced in 1973 ... both speaker systems shared the same 30 cm (12") '
             '3-way bookshelf design"; the NS-5000 lineage text also refers to "all three drivers". A '
             'three-way system with a 30 cm woofer, a midrange and a tweeter has three transducers.'),
    'notesAppend': (' Round 29 (2026-10-19): driverCount 3 promoted from the Yamaha NS-690/NS-5000 history '
                    'page, which states the 30 cm (12") 3-way design with soft-dome tweeter and midrange. '
                    'The previously cited hub.yamaha.com URL returns 404 and is retired as evidence.'),
}

URL_RESULTS = [
    {
        'url': YAMAHA_HISTORY,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0, 1, 3],
        'chunksTotal': 4,
        'evidence': ('NS-690 "30 cm (12") 3-way bookshelf design" with soft-dome tweeter and midrange; '
                     'NS-5000 "all three drivers". Also read chunks 0 and 3 (page frame and location list); '
                     'the page carries no separate specification table.'),
        'fieldResults': [
            {'record': 'legacy-yam-3', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
             'note': 'Three-way system with 30 cm woofer, midrange and tweeter; Yamaha host.'},
        ],
    },
    {
        'url': KEF_Q150,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0],
        'chunksTotal': 4,
        'evidence': ('Specifications: "2-way bass reflex", Drive Units "130mm (5.25in.) aluminium Uni-Q" and '
                     '"25mm (1in.) vented aluminium dome HF", "Amplifier Requirements 10-100W". No '
                     'passive/active/powered wording; an amplifier requirement is not a passive statement.'),
        'fieldResults': [
            {'record': 'kef-q150', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
             'note': 'Round 29: opened the KEF page; only "Amplifier Requirements 10-100W" is given.'},
        ],
    },
    {
        'url': KEF_Q350,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0],
        'chunksTotal': 4,
        'evidence': ('Same KEF template: 2-way bass reflex with Uni-Q drive units and "Amplifier '
                     'Requirements"; no passive/active/powered statement.'),
        'fieldResults': [
            {'record': 'kef-q350', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
             'note': 'Round 29: opened the KEF page; amplifier requirement only.'},
        ],
    },
    {
        'url': MARSHALL,
        'status': 'INACCESSIBLE',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ('Retry returned "Page not found - Sorry, the page you are looking for does not exist." '
                     'The 1936 2x12 cabinet product page is still unavailable on marshall.com.'),
        'fieldResults': [
            {'record': 'marshall-marshall-1936', 'field': 'driverCount', 'value': 2, 'outcome': 'INACCESSIBLE',
             'note': 'Round 29 retry: 404 page, no specification text.'},
            {'record': 'marshall-marshall-1936', 'field': 'active', 'value': False, 'outcome': 'INACCESSIBLE',
             'note': 'Round 29 retry: 404 page, no specification text.'},
        ],
    },
    {
        'url': YAMAHA_HUB,
        'status': 'INACCESSIBLE',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ('Retry returned "Oops! That page can\'t be found." The Yamaha studio-monitor history '
                     'article is no longer served, so the NS-10M driver count stays unresolved.'),
        'fieldResults': [
            {'record': 'legacy-yam-2', 'field': 'driverCount', 'value': 2, 'outcome': 'INACCESSIBLE',
             'note': 'Round 29 retry: 404 page.'},
        ],
    },
    {
        'url': ELAC,
        'status': 'CHECKED_PARTIAL',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': ('UB5: "3-way bass reflex"; tweeter 1 in soft dome, mid-range 4 in aluminium, woofer '
                     '5.25 in aluminium; the text says the tweeter and midrange form one concentric driver. '
                     'The number of transducers is therefore ambiguous between two drive units and three '
                     'transducers; the existing driverCount stays unresolved.'),
        'fieldResults': [
            {'record': 'elac-uni-fi-ub5', 'field': 'driverCount', 'value': None, 'outcome': 'CONFLICT',
             'note': 'Round 29: concentric tweeter/midrange makes 2 vs 3 ambiguous; not promoted.'},
        ],
    },
]
