#!/usr/bin/env python3
"""Round 28 (2026-10-19): close the four HELD_PENDING_URL_CHECK records at the evidence level.

Round 4 removed `driverCount` and `active` from these four records and stored them as
HELD_PENDING_URL_CHECK until the fields were checked against the URL already used for their sibling
fields. This batch performs that check and records the result.

Every document below was opened in this session and states the fact directly. None of the eight values
can be written, however: `src/data/speakers.round3.test.ts` admits only three provenance statuses for
`driverCount` / `active` — `CITED_IN_NOTES_UNCHECKED`, `UNSOURCED`, `MANUFACTURER_VERIFIED`. These
documents are third-party copies or reputable-database pages, so `MANUFACTURER_VERIFIED` would be false,
and `CITED_IN_NOTES_UNCHECKED` would also be false because the field *has* now been checked. The
evidence is therefore recorded here and in each record's notes, while the values stay null and
`UNSOURCED` until the owner decides whether to widen the schema for these two fields. No test or schema
rule was changed.

Sources opened:
  legacy-mack-4  Mackie CR3 owner's manual (pdf-manuals.com copy)
  legacy-mack-5  Mackie Thump15 specification text (proacousticsusa.com)
  equator-d5     Equator D5 product page (gear4music.com)
  beolab-5       Bang & Olufsen BeoLab 5 brochure '16055_BL5_Tekn_EU_UK'
                 (content.abt.com/documents/6162/1680009_specs.pdf)
"""
DATE = '2026-10-19'
ROUND = 28

CR3 = ('https://www.pdf-manuals.com/pdf/mackie-cr3-3-woofer-creative-reference-cr3-pair-b-h-330662-'
       'user-manual.pdf')
THUMP15 = 'https://www.proacousticsusa.com/mackie-thump15-powered-loudspeaker.html'
D5 = ('https://www.gear4music.com/Recording-and-Computers/Equator-D5-Active-Studio-Monitors-with-'
      'Internal-DSP-Pair/LA3')
BEOLAB5 = 'https://content.abt.com/documents/6162/1680009_specs.pdf'

ASSESSMENTS = [
    {
        'record': 'legacy-mack-4',
        'source': CR3,
        'sourceType': 'THIRD_PARTY',
        'document': "Mackie CR Series owner's manual, Appendix B (CR3 table)",
        'driverCount': 2,
        'driverCountEvidence': (
            'Appendix B "Transducers": "Low Frequency 3.0 in / 76 mm polypropylene-coated woofer [CR3]" '
            'and "High Frequency 0.75 in / 19 mm silk dome tweeter" — two transducers.'),
        'active': True,
        'activeEvidence': (
            'The "Amplifiers" table gives "Rated Power 28 watts rms 50 watts peak" and "Design Class AB"; '
            'the "Power Requirements" table gives AC mains voltages, so the unit is self-powered.'),
        'notes_append': (
            ' Round 28 (2026-10-19) reassessment: the CR3 manual copy was reopened and states the CR3 '
            'transducer pair (3.0 in LF, 0.75 in HF) and its internal 28 W Class AB amplifiers, so driverCount '
            '2 and active true are evidence-backed. The values stay null because the driverCount/active '
            'schema admits only manufacturer-verified sources and this is a third-party manual copy; owner '
            'decision needed. The CR3 vs CR3-X ambiguity does not affect these two facts (the manual names '
            'CR3 and its 3.0 in LF driver).'),
    },
    {
        'record': 'legacy-mack-5',
        'source': THUMP15,
        'sourceType': 'REPUTABLE_DATABASE',
        'document': 'Mackie Thump15 specification page (proacousticsusa.com, discontinued listing)',
        'driverCount': 2,
        'driverCountEvidence': (
            'Specification table: "Woofer Diameter 15\\" (381 mm)" and "Compression Driver 1.4\\" (36 mm)", '
            'with "Precision 2-way crossover" — two transducers.'),
        'active': True,
        'activeEvidence': (
            'Page title "Mackie Thump15 Powered Loudspeaker"; "1000 W total system power"; '
            '"Ultra-efficient Class-D amplification"; a "Power Amplifiers" table.'),
        'notes_append': (
            ' Round 28 (2026-10-19) reassessment: the Thump15 specification page was reopened and states the '
            '15 in woofer, the 1.4 in compression driver, a 2-way crossover and a powered amplifier section, '
            'so driverCount 2 and active true are evidence-backed. The values stay null because the schema '
            'admits only manufacturer-verified sources for these two fields and this is a reputable-database '
            'page; owner decision needed. Thump15A and THUMP15BST remain other products and were not merged.'),
    },
    {
        'record': 'equator-d5',
        'source': D5,
        'sourceType': 'THIRD_PARTY',
        'document': 'Equator D5 product page (gear4music.com)',
        'driverCount': 2,
        'driverCountEvidence': (
            'Product description: "coaxially designed transducer with a 5.25\\" woofer and a 1\\" silk '
            'tweeter"; specification bullets "Coaxial Designed 5.25\\" Diameter Polypropylene Woofer" and '
            '"Coaxial Designed 1\\" Diameter Silk Tweeter" — two transducers.'),
        'active': True,
        'activeEvidence': (
            'Product title "Equator D5 Active Studio Monitors with Internal DSP (Pair)"; the description '
            'describes the internal digital amplifier and DSP.'),
        'notes_append': (
            ' Round 28 (2026-10-19) reassessment: the recorded gear4music page was reopened and still states '
            'the coaxial 5.25 in woofer plus 1 in silk tweeter and the active/internal-amplifier design, so '
            'driverCount 2 and active true are evidence-backed. The values stay null because the schema '
            'admits only manufacturer-verified sources for these two fields and this is a third-party page; '
            'owner decision needed. The manufacturer site remains unreachable (equatoraudio.com D5 path 404).'),
    },
    {
        'record': 'beolab-5',
        'source': BEOLAB5,
        'sourceType': 'REPUTABLE_DATABASE',
        'document': 'Bang & Olufsen BeoLab 5 brochure 16055_BL5_Tekn_EU_UK (PDF served by abt.com)',
        'driverCount': 4,
        'driverCountEvidence': (
            'Driver call-outs: "3/4\\" treble driver", "3\\" mid-range driver", "6 1/2\\" upper bass driver", '
            '"Long-throw 15\\" lower bass driver" — four transducers.'),
        'active': True,
        'activeEvidence': (
            '"4 way active technology with 4 ICEpower amplifiers"; "ICEpower, digital amplification".'),
        'notes_append': (
            ' Round 28 (2026-10-19) reassessment: the B&O brochure was reopened at content.abt.com/documents/'
            '6162/1680009_specs.pdf (its earlier /documents/16055_BL5_Tekn_EU_UK.pdf path now 404s) and lists '
            'four drivers plus "4 way active technology with 4 ICEpower amplifiers", so driverCount 4 and '
            'active true are evidence-backed. The values stay null because the schema admits only '
            'manufacturer-verified sources for these two fields and this is a retailer-hosted copy; owner '
            'decision needed. The MK2 generation caveat is unchanged.'),
    },
]
