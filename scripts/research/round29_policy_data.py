#!/usr/bin/env python3
"""Round 29 (2026-10-19): first application of the third-party structural-field policy.

Owner instruction of 2026-10-19 added `THIRD_PARTY_VERIFIED` for `driverCount` and `active` under
scripts/research/PROVENANCE-POLICY.md. The four records below are the only ones written in this batch:
each was assessed in Round 28, the document was opened then, and the document states the field
explicitly. No cited field is promoted in bulk.

Sources (opened 2026-10-19; quotes are from those reads):
  legacy-mack-4  Mackie CR Series owner's manual, Appendix B (pdf-manuals.com copy)
  legacy-mack-5  Mackie Thump15 specification text (proacousticsusa.com)
  equator-d5     Equator D5 product page (gear4music.com)
  beolab-5       B&O BeoLab 5 brochure 16055_BL5_Tekn_EU_UK (content.abt.com/documents/6162/
                 1680009_specs.pdf)
"""
DATE = '2026-10-19'
ROUND = 29
DECISION = ('Owner instruction 2026-10-19: add THIRD_PARTY_VERIFIED for driverCount/active under '
            'scripts/research/PROVENANCE-POLICY.md')

CR3 = ('https://www.pdf-manuals.com/pdf/mackie-cr3-3-woofer-creative-reference-cr3-pair-b-h-330662-'
       'user-manual.pdf')
THUMP15 = 'https://www.proacousticsusa.com/mackie-thump15-powered-loudspeaker.html'
D5 = ('https://www.gear4music.com/Recording-and-Computers/Equator-D5-Active-Studio-Monitors-with-'
      'Internal-DSP-Pair/LA3')
BEOLAB5 = 'https://content.abt.com/documents/6162/1680009_specs.pdf'

ENTRIES = [
    {
        'record': 'legacy-mack-4',
        'source': CR3,
        'sourceType': 'THIRD_PARTY',
        'document': "Mackie CR Series owner's manual, Appendix B (CR3 table)",
        'fields': {
            'driverCount': {
                'value': 2,
                'note': ('Mackie CR Series owner\'s manual, Appendix B "Transducers": "Low Frequency 3.0 in '
                         '/ 76 mm polypropylene-coated woofer [CR3]" and "High Frequency 0.75 in / 19 mm silk '
                         'dome tweeter" — two transducers. Third-party manual copy; owner instruction '
                         '2026-10-19, PROVENANCE-POLICY conditions met (exact CR3 revision named).'),
            },
            'active': {
                'value': True,
                'note': ('Same manual, "Amplifiers": "Rated Power 28 watts rms 50 watts peak", "Design Class '
                         'AB"; "Power Requirements" lists AC mains voltages, so the monitor is self-powered. '
                         'Third-party manual copy under the 2026-10-19 policy.'),
            },
        },
    },
    {
        'record': 'legacy-mack-5',
        'source': THUMP15,
        'sourceType': 'REPUTABLE_DATABASE',
        'document': 'Mackie Thump15 specification page (proacousticsusa.com)',
        'fields': {
            'driverCount': {
                'value': 2,
                'note': ('Thump15 specification page: "Woofer Diameter 15\\" (381 mm)" and "Compression Driver '
                         '1.4\\" (36 mm)", with "Precision 2-way crossover" — two transducers. Reputable-'
                         'database page; exact model Thump15 (not Thump15A/THUMP15BST).'),
            },
            'active': {
                'value': True,
                'note': ('Same page: title "Mackie Thump15 Powered Loudspeaker", "1000 W total system power", '
                         '"Ultra-efficient Class-D amplification" and a "Power Amplifiers" table. '
                         'Reputable-database tier under the 2026-10-19 policy.'),
            },
        },
    },
    {
        'record': 'equator-d5',
        'source': D5,
        'sourceType': 'THIRD_PARTY',
        'document': 'Equator D5 product page (gear4music.com)',
        'fields': {
            'driverCount': {
                'value': 2,
                'note': ('gear4music D5 page: "coaxially designed transducer with a 5.25\\" woofer and a 1\\" '
                         'silk tweeter"; specification bullets name the 5.25\\" polypropylene woofer and the '
                         '1\\" silk tweeter — two transducers. Third-party retailer page under the '
                         '2026-10-19 policy; manufacturer site still unreachable.'),
            },
            'active': {
                'value': True,
                'note': ('Same page: product title "Equator D5 Active Studio Monitors with Internal DSP '
                         '(Pair)"; description states the internal digital amplifier and DSP. Third-party '
                         'tier under the 2026-10-19 policy.'),
            },
        },
    },
    {
        'record': 'beolab-5',
        'source': BEOLAB5,
        'sourceType': 'REPUTABLE_DATABASE',
        'document': 'Bang & Olufsen BeoLab 5 brochure 16055_BL5_Tekn_EU_UK (PDF served by abt.com)',
        'fields': {
            'driverCount': {
                'value': 4,
                'note': ('B&O BeoLab 5 brochure driver call-outs: "3/4\\" treble driver", "3\\" mid-range '
                         'driver", "6 1/2\\" upper bass driver", "Long-throw 15\\" lower bass driver" — four '
                         'transducers. Reputable-database copy of the manufacturer brochure under the '
                         '2026-10-19 policy; MK2 caveat unchanged.'),
            },
            'active': {
                'value': True,
                'note': ('Same brochure: "4 way active technology with 4 ICEpower amplifiers" and "ICEpower, '
                         'digital amplification". Reputable-database tier under the 2026-10-19 policy.'),
            },
        },
    },
]

NOTES_SUPERSEDE = (
    ' Round 29 (2026-10-19): the provenance policy was extended to allow THIRD_PARTY_VERIFIED for '
    'driverCount/active under scripts/research/PROVENANCE-POLICY.md. The Round 28 sentence above that '
    'said these values stay null is superseded: both fields are now stored at the third-party tier with '
    'the quoted evidence.'
)
