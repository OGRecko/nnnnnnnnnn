"""Round 22 evidence table.

Every check below was performed by opening the listed URL during Round 22
(2026-10-19) and reading the model-specific specification text. Outcomes:
  PROMOTED / SUPPORTED_NOT_PROMOTED / NOT_STATED / NOT_EXTRACTED / INACCESSIBLE / CONFLICT

Only exact-model manufacturer (or owner-approved distributor) documents are used.
Values are filled from the live catalogue at build time, never hard-coded here.
"""
CHECKED_DATE = '2026-10-19'

NOT_STATED_NOTE = ('No explicit passive/active, powered/unpowered, or built-in amplifier '
                   'wording for this model; a recommended amplifier-power range alone is '
                   'not accepted as evidence, so the field stays unverified.')


def C(url, document, evidence, results, status='CHECKED', total=None, chunks=(0,)):
    return {
        'url': url,
        'document': document,
        'chunksOpened': list(chunks),
        'chunksTotal': total,
        'status': status,
        'evidence': evidence,
        'results': results,
    }


def R(record, field, outcome='PROMOTED', note=None):
    # Hashable 3-tuple so the literals below can stay compact sets; the builder
    # converts them to ordered dicts deterministically.
    return (record + '.' + field, outcome, note)


CHECKS = [
    # ---------------- DALI ----------------
    C('https://www.dali-speakers.com/media/5320/oberon-manual.pdf',
      'DALI OBERON series owner manual (manufacturer PDF)',
      'PDF parser returned the manual only up to its 30-page extraction limit; the OBERON '
      'specification table (Table 2) lies beyond that limit and could not be read. No field '
      'evidence was obtained.',
      {
          R('dali-oberon-3', 'driverCount', 'NOT_EXTRACTED', 'Specification table beyond the parser page limit; not read.'),
          R('dali-oberon-5', 'driverCount', 'NOT_EXTRACTED', 'Specification table beyond the parser page limit; not read.'),
          R('dali-oberon7', 'driverCount', 'NOT_EXTRACTED', 'Specification table beyond the parser page limit; not read.'),
      }, status='NOT_EXTRACTED'),

    # ---------------- KEF ----------------
    C('https://assets.kef.com/documents/ls50/20-KEF-LS50-Wireless-II-Product-Info-Sheet.pdf',
      'KEF LS50 Wireless II Product Information Sheet',
      'Info sheet: "LS50 Wireless II" is a 2-way system with a 25 mm (1 in) vented aluminium '
      'dome HF driver and a 130 mm (5.25 in) magnesium/aluminium alloy LF/MF driver, and lists '
      'the built-in amplification for each driver (Class AB HF, Class D LF).',
      {R('kef-ls50-wireless', 'driverCount', note='Info sheet lists exactly two drive units: 25 mm HF + 130 mm LF/MF.'),
       R('kef-ls50-wireless', 'active', note='Info sheet lists built-in amplification (Class AB HF, Class D LF); self-powered.')}),

    C('https://assets.kef.com/pdf_doc/KF92/KF92_infosheet_EN.pdf',
      'KEF KF92 Subwoofer Information Sheet',
      'Info sheet: KF92 is a sealed subwoofer with two 9 in (229 mm) aluminium cone woofers and '
      'a 1000 W built-in Class D amplifier.',
      {R('kef-kf92', 'driverCount', note='Info sheet lists two 9 in (229 mm) woofers.'),
       R('kef-kf92', 'active', note='Info sheet lists a 1000 W built-in Class D amplifier.')}),

    C('https://assets.kef.com/pdf_doc/product-archive/1970s/REFERENCE+SERIES+MODEL+103+(1976-77',
      'KEF Reference Series Model 103 archive page (URL as recorded)',
      'The recorded archive URL returns HTTP 404; the archived KEF Reference Series page could '
      'not be opened, so no evidence was obtained.',
      {R('legacy-kef-3', 'driverCount', 'INACCESSIBLE', 'HTTP 404 on the recorded archive URL.'),
       R('legacy-kef-3', 'active', 'INACCESSIBLE', 'HTTP 404 on the recorded archive URL.')},
      status='INACCESSIBLE'),

    C('https://assets.kef.com/pdf_doc/product-archive/1970s/REFERENCE+SERIES+MODEL+105.2+(1979-87',
      'KEF Reference Series Model 105.2 archive page (URL as recorded)',
      'The recorded archive URL returns HTTP 404; the archived KEF Reference Series page could '
      'not be opened, so no evidence was obtained.',
      {R('kef-105', 'driverCount', 'INACCESSIBLE', 'HTTP 404 on the recorded archive URL.'),
       R('kef-105', 'active', 'INACCESSIBLE', 'HTTP 404 on the recorded archive URL.')},
      status='INACCESSIBLE'),

    C('https://international.kef.com/products/q150-bookshelf-speaker',
      'KEF Q150 bookshelf loudspeaker product page',
      'Product specifications: 2-way bass reflex, 25 mm (1 in) vented aluminium dome tweeter '
      'and 130 mm (5.25 in) aluminium Uni-Q driver array.',
      {R('kef-q150', 'driverCount', note='Specifications list a 25 mm tweeter and a 130 mm Uni-Q driver (2 drive units).')}),

    C('https://international.kef.com/products/q350-bookshelf-speaker',
      'KEF Q350 bookshelf loudspeaker product page',
      'Product specifications: 2-way bass reflex, 25 mm (1 in) vented aluminium dome tweeter '
      'and 165 mm (6.5 in) aluminium Uni-Q driver array.',
      {R('kef-q350', 'driverCount', note='Specifications list a 25 mm tweeter and a 165 mm Uni-Q driver (2 drive units).')}),

    C('https://international.kef.com/products/q750-floorstanding-speaker',
      'KEF Q750 floorstanding loudspeaker product page',
      'Product specifications: 2.5-way bass reflex, 25 mm (1 in) vented aluminium dome tweeter, '
      '165 mm (6.5 in) aluminium Uni-Q driver array, one 165 mm (6.5 in) aluminium LF driver and '
      'two 165 mm (6.5 in) aluminium ABR radiators. ABRs are passive radiators, not driven units.',
      {R('kef-q750', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'Page describes 3 driven units plus 2 ABR passive radiators; the schema does not define '
         'whether ABRs count, so the stored 5 is not promoted. Owner decision needed.'),
       R('kef-q750', 'active', 'NOT_STATED')}),

    C('https://international.kef.com/products/r11-meta',
      'KEF R11 Meta floorstanding loudspeaker product page',
      'Product specifications: 3-way bass reflex with one 25 mm (1 in) MAT vented dome tweeter, '
      'one 125 mm (5 in) Uni-Q midrange and four 165 mm (6.5 in) aluminium bass drivers.',
      {R('kef-r11-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 4 bass drivers = 6.')}),

    C('https://us.kef.com/products/blade-two',
      'KEF Blade Two Meta floorstanding loudspeaker product page',
      'Product specifications: 3-way bass reflex with one 25 mm (1 in) MAT vented dome tweeter, '
      'one 125 mm (5 in) Uni-Q midrange and four 165 mm (6.5 in) aluminium bass drivers.',
      {R('kef-blade-two-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 4 bass drivers = 6.')}),

    C('https://us.kef.com/products/lsx-2',
      'KEF LSX II wireless music system product page',
      'Product specifications: 2-way with a 19 mm (0.75 in) aluminium dome tweeter and a '
      '115 mm (4.5 in) magnesium/aluminium alloy midrange/bass driver, each driven by its own '
      'built-in amplifier (Class D).',
      {R('kef-lsx-ii', 'driverCount', note='Specifications list a 19 mm tweeter and a 115 mm mid/bass driver = 2.'),
       R('kef-lsx-ii', 'active', note='Specifications list built-in Class D amplification; self-powered.')}),

    C('https://us.kef.com/products/r3-meta',
      'KEF R3 Meta bookshelf loudspeaker product page',
      'Product page labels the model "Passive HiFi Speaker" and lists a 3-way bass reflex design '
      'with a 25 mm tweeter, a 125 mm Uni-Q midrange and a 165 mm bass driver.',
      {R('kef-r3-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 1 bass driver = 3.'),
       R('kef-r3-meta', 'active', note='Product page explicitly labels the model a "Passive HiFi Speaker".')}),

    C('https://us.kef.com/products/r7-meta',
      'KEF R7 Meta floorstanding loudspeaker product page',
      'Product page labels the model "Passive HiFi Speaker" and lists a 3-way bass reflex design '
      'with a 25 mm tweeter, a 125 mm Uni-Q midrange and two 165 mm bass drivers.',
      {R('kef-r7-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 2 bass drivers = 4.'),
       R('kef-r7-meta', 'active', note='Product page explicitly labels the model a "Passive HiFi Speaker".')}),

    C('https://us.kef.com/products/reference-1-bookshelf-speaker',
      'KEF Reference 1 Meta bookshelf loudspeaker product page',
      'Product page labels the model "Passive HiFi Speaker" and lists a 3-way bass reflex design '
      'with a 25 mm tweeter, a 125 mm Uni-Q midrange and a 165 mm bass driver.',
      {R('kef-reference-1-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 1 bass driver = 3.'),
       R('kef-reference-1-meta', 'active', note='Product page explicitly labels the model a "Passive HiFi Speaker".')}),

    C('https://us.kef.com/products/reference-3-floorstanding-speaker',
      'KEF Reference 3 Meta floorstanding loudspeaker product page',
      'Product page labels the model "Passive HiFi Speaker" and lists a 3-way bass reflex design '
      'with a 25 mm tweeter, a 125 mm Uni-Q midrange and two 165 mm bass drivers.',
      {R('kef-reference-3-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 2 bass drivers = 4.'),
       R('kef-reference-3-meta', 'active', note='Product page explicitly labels the model a "Passive HiFi Speaker".')}),

    C('https://us.kef.com/products/reference-5-floorstanding-speaker',
      'KEF Reference 5 Meta floorstanding loudspeaker product page',
      'Product page labels the model "Passive HiFi Speaker" and lists a 3-way bass reflex design '
      'with a 25 mm tweeter, a 125 mm Uni-Q midrange and four 165 mm bass drivers.',
      {R('kef-reference-5-meta', 'driverCount', note='Specifications list 1 tweeter + 1 Uni-Q midrange + 4 bass drivers = 6.'),
       R('kef-reference-5-meta', 'active', note='Product page explicitly labels the model a "Passive HiFi Speaker".')}),

    C('https://us.kef.com/products/ls50-meta',
      'KEF LS50 Meta bookshelf loudspeaker product page',
      'Product specifications: 2-way bass reflex with a 25 mm (1 in) vented aluminium dome '
      'tweeter and a 130 mm (5.25 in) Uni-Q driver array.',
      {R('legacy-kef-9', 'driverCount', note='Specifications list a 25 mm tweeter and a 130 mm Uni-Q driver (2 drive units).')}),

    # ---------------- Klipsch ----------------
    C('https://assets.klipsch.com/product-specsheets/AWR-650-SM.pdf',
      'Klipsch AWR-650-SM outdoor loudspeaker specification sheet',
      'Specification sheet: two-way outdoor speaker with one 6.5 in (165 mm) IMG woofer and two '
      '0.75 in (19 mm) polymer dome tweeters (three drive units).',
      {R('klipsch-awr650sm', 'driverCount', note='Spec sheet lists one 6.5 in woofer and two 0.75 in tweeters = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/Cornwall-2019-Spec-Sheet-v03.pdf',
      'Klipsch Cornwall IV specification sheet (2019)',
      'Specification sheet: three-way design with a 1 in titanium diaphragm compression driver, '
      'a 1.75 in titanium diaphragm compression driver and a 15 in woofer (three drive units).',
      {R('klipsch-cornwall-iv', 'driverCount', note='Spec sheet lists HF and MF compression drivers plus a 15 in woofer = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/Forte-IV-Spec-Sheet-v01-1.pdf',
      'Klipsch Forte IV specification sheet',
      'Specification sheet: three-way design with a 1 in titanium diaphragm compression driver, '
      'a 1.75 in titanium diaphragm compression driver and a 12 in woofer (three drive units).',
      {R('klipsch-forte-iv', 'driverCount', note='Spec sheet lists HF and MF compression drivers plus a 12 in woofer = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/Heresy-IV-Spec-Sheet-v04.pdf',
      'Klipsch Heresy IV specification sheet',
      'Specification sheet: three-way design with a 1 in titanium diaphragm compression driver, '
      'a 1.75 in titanium diaphragm compression driver and a 12 in woofer (three drive units).',
      {R('klipsch-heresy-iv', 'driverCount', note='Spec sheet lists HF and MF compression drivers plus a 12 in woofer = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/R-120SW_GM_Spec-Sheet_v01.pdf',
      'Klipsch Reference R-120SW subwoofer specification sheet',
      'Specification sheet: single 12 in (305 mm) spun-copper IMG woofer driven by a built-in '
      'all-digital amplifier rated 200 W continuous / 400 W peak.',
      {R('klipsch-r-120sw', 'driverCount', note='Spec sheet lists one 12 in woofer.'),
       R('klipsch-r-120sw', 'active', note='Spec sheet lists a built-in all-digital amplifier (200 W continuous).')}),

    C('https://assets.klipsch.com/product-specsheets/R-41M_Spec-Sheet_GM_v01.pdf',
      'Klipsch Reference R-41M bookshelf speaker specification sheet',
      'Specification sheet: two-way bookshelf speaker with one 4 in (102 mm) IMG woofer and one '
      '1 in (25 mm) aluminium dome tweeter.',
      {R('legacy-klip-8', 'driverCount', note='Spec sheet lists one 4 in woofer and one 1 in tweeter = 2.')}),

    C('https://assets.klipsch.com/product-specsheets/RF-7-III_Spec-Sheet-v01.pdf',
      'Klipsch Reference RF-7 III floorstanding speaker specification sheet',
      'Specification sheet: three-way design with two 10 in woofers, one 1.75 in titanium '
      'compression driver and one 1 in titanium compression driver (four drive units).',
      {R('legacy-klip-6', 'driverCount', 'CONFLICT',
         'Spec sheet lists two 10 in woofers plus two compression drivers = 4 drive units, while '
         'the stored value is 3. Left unchanged pending reconciliation; the stored value is not promoted.')}),

    C('https://assets.klipsch.com/product-specsheets/La-Scala-II-Spec-Sheet-v03.pdf',
      'Klipsch La Scala II specification sheet',
      'Specification sheet: three-way design with a 1 in titanium diaphragm compression driver, '
      'a 1.75 in titanium diaphragm compression driver and a 15 in woofer (three drive units).',
      {R('klipsch-la-scala-ii', 'driverCount', note='Spec sheet lists two compression drivers plus a 15 in woofer = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/Reference-R-121SW-Spec-Sheet.pdf',
      'Klipsch Reference R-121SW subwoofer specification sheet',
      'Specification sheet: single 12 in (305 mm) spun-copper IMG woofer driven by a built-in '
      'all-digital amplifier rated 200 W continuous / 400 W peak.',
      {R('klipsch-r-121sw', 'driverCount', note='Spec sheet lists one 12 in woofer.'),
       R('klipsch-r-121sw', 'active', note='Spec sheet lists a built-in all-digital amplifier.')}),

    C('https://assets.klipsch.com/product-specsheets/SPL-100_Spec-Sheet_v01.pdf',
      'Klipsch SPL-100 subwoofer specification sheet',
      'Specification sheet: single 10 in (254 mm) spun-copper Cerametallic woofer driven by a '
      'built-in Class D amplifier rated 200 W continuous / 450 W peak.',
      {R('klipsch-spl-100', 'driverCount', note='Spec sheet lists one 10 in woofer.'),
       R('klipsch-spl-100', 'active', note='Spec sheet lists a built-in Class D amplifier.')}),

    C('https://assets.klipsch.com/product-specsheets/SPL-120_Spec-Sheet_v01.pdf',
      'Klipsch SPL-120 subwoofer specification sheet',
      'Specification sheet: single 12 in (305 mm) spun-copper Cerametallic woofer driven by a '
      'built-in Class D amplifier rated 300 W continuous / 600 W peak.',
      {R('klipsch-spl-120', 'driverCount', note='Spec sheet lists one 12 in woofer.'),
       R('klipsch-spl-120', 'active', note='Spec sheet lists a built-in Class D amplifier.')}),

    C('https://assets.klipsch.com/product-specsheets/SPL-150_Spec-Sheet_v01.pdf',
      'Klipsch SPL-150 subwoofer specification sheet',
      'Specification sheet: single 15 in (381 mm) spun-copper Cerametallic woofer driven by a '
      'built-in Class D amplifier rated 400 W continuous / 800 W peak.',
      {R('klipsch-spl-150', 'driverCount', note='Spec sheet lists one 15 in woofer.'),
       R('klipsch-spl-150', 'active', note='Spec sheet lists a built-in Class D amplifier.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-5000F-II_Spec-Sheet_v02.pdf',
      'Klipsch Reference Premiere RP-5000F II specification sheet',
      'Specification sheet: two-way design with two 5.25 in (133 mm) Cerametallic woofers and one '
      '1 in (25 mm) titanium LTS vented tweeter (three drive units).',
      {R('klipsch-rp-5000f-ii', 'driverCount', note='Spec sheet lists two 5.25 in woofers and one 1 in tweeter = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-500M-II_Spec-Sheet_v02_2022-05-18-131859_rlqj.pdf',
      'Klipsch Reference Premiere RP-500M II specification sheet',
      'Specification sheet: two-way design with one 5.25 in (133 mm) Cerametallic woofer and one '
      '1 in (25 mm) titanium LTS vented tweeter.',
      {R('klipsch-rp500m', 'driverCount', note='Spec sheet lists one 5.25 in woofer and one 1 in tweeter = 2.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-500M_Spec-Sheet_v01.pdf',
      'Klipsch Reference Premiere RP-500M specification sheet',
      'Specification sheet: two-way design with one 5.25 in (133 mm) Cerametallic woofer and one '
      '1 in (25 mm) titanium LTS vented tweeter.',
      {R('klipsch-rp-500m', 'driverCount', note='Spec sheet lists one 5.25 in woofer and one 1 in tweeter = 2.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-6000F-II_Spec-Sheet_v02.pdf',
      'Klipsch Reference Premiere RP-6000F II specification sheet',
      'Specification sheet: two-way design with two 6.5 in (165 mm) Cerametallic woofers and one '
      '1 in (25 mm) titanium LTS vented tweeter (three drive units).',
      {R('klipsch-rp6000f', 'driverCount', note='Spec sheet lists two 6.5 in woofers and one 1 in tweeter = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-600M-II_Spec-Sheet_v02.pdf',
      'Klipsch Reference Premiere RP-600M II specification sheet',
      'Specification sheet: two-way design with one 6.5 in (165 mm) Cerametallic woofer and one '
      '1 in (25 mm) titanium LTS vented tweeter.',
      {R('klipsch-rp600m', 'driverCount', note='Spec sheet lists one 6.5 in woofer and one 1 in tweeter = 2.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-600M_Spec-Sheet_v01.pdf',
      'Klipsch Reference Premiere RP-600M specification sheet',
      'Specification sheet: two-way design with one 6.5 in (165 mm) Cerametallic woofer and one '
      '1 in (25 mm) titanium LTS vented tweeter.',
      {R('klipsch-rp-600m', 'driverCount', note='Spec sheet lists one 6.5 in woofer and one 1 in tweeter = 2.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-8000F-II_Spec-Sheet_v02.pdf',
      'Klipsch Reference Premiere RP-8000F II specification sheet',
      'Specification sheet: two-way design with two 8 in (203 mm) Cerametallic woofers and one '
      '1 in (25 mm) titanium LTS vented tweeter (three drive units).',
      {R('klipsch-rp-8000f-ii', 'driverCount', note='Spec sheet lists two 8 in woofers and one 1 in tweeter = 3.')}),

    C('https://assets.klipsch.com/product-specsheets/RP-8060FA-II_Spec-Sheet_v02.pdf',
      'Klipsch Reference Premiere RP-8060FA II specification sheet',
      'Specification sheet: Dolby Atmos-enabled floorstanding speaker with two 8 in (203 mm) '
      'Cerametallic woofers, one 1 in titanium LTS vented tweeter, plus a height-channel 6.5 in '
      'woofer and 1 in titanium dome tweeter (five drive units).',
      {R('klipsch-rp8060fa', 'driverCount', note='Spec sheet lists 2 main woofers + 1 tweeter + 1 height woofer + 1 height tweeter = 5.')}),

    C('https://www.klipsch.com/products/cdt-5650-c-ii',
      'Klipsch CDT-5650-C II in-ceiling loudspeaker product page',
      'Product specifications: two-way in-ceiling speaker with a 6.5 in (165 mm) IMG woofer and '
      'a 1 in (25 mm) titanium tweeter.',
      {R('klipsch-cdt5650c', 'driverCount', note='Specifications list one 6.5 in woofer and one 1 in tweeter = 2.')}),

    C('https://www.klipsch.com/products/cdt-5800-c-ii',
      'Klipsch CDT-5800-C II in-ceiling loudspeaker product page',
      'Product specifications: two-way in-ceiling speaker with an 8 in (203 mm) IMG woofer and '
      'a 1 in (25 mm) titanium tweeter.',
      {R('klipsch-cdt-5800-c-ii', 'driverCount', note='Specifications list one 8 in woofer and one 1 in tweeter = 2.')}),

    # ---------------- ATC / PMC ----------------
    C('https://atc.audio/professional/loudspeakers/scm100asl-pro/',
      'ATC SCM100ASL Pro monitor product page',
      'Product specifications: active three-way monitor with an ATC 25 mm soft-dome HF driver, '
      'a 75 mm ATC SM75-150S midrange and a 314 mm (12 in) ATC LF driver, driven by three '
      'built-in ATC amplifiers.',
      {R('atc-scm100asl-pro', 'driverCount', note='Specifications list HF, mid and LF drive units = 3.'),
       R('atc-scm100asl-pro', 'active', note='Specifications list built-in ATC amplification (active monitor).')}),

    C('https://atc.audio/professional/loudspeakers/scm45a-pro/',
      'ATC SCM45A Pro monitor product page',
      'Product specifications: active three-way monitor; the specification table lists "Drivers: '
      'HF 25mm, Mid 75mm, LF 164mm", while the overview bullet and the linked technical datasheet '
      'describe dual 6.5 in (164 mm) woofers. The page also lists built-in ATC amplification.',
      {R('atc-scm45a-pro', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'The specification table row lists 3 driver sizes, but the overview bullet and the '
         'datasheet state dual 6.5 in woofers (4 units). The stored 3 remains pinned by '
         'src/data/speakers.test.ts; no promotion until the discrepancy is resolved.'),
       R('atc-scm45a-pro', 'active', note='Product page and datasheet list built-in ATC amplification (active monitor).')}),

    C('https://atc.audio/professional/loudspeakers/scm50a-pro/',
      'ATC SCM50ASL Pro monitor product page',
      'Product specifications: active three-way monitor with a 25 mm soft-dome HF driver, a '
      '75 mm SM75-150S midrange and a 234 mm (9 in) LF driver, driven by built-in ATC amplifiers.',
      {R('atc-scm50asl-pro', 'driverCount', note='Specifications list HF, mid and LF drive units = 3.'),
       R('atc-scm50asl-pro', 'active', note='Specifications list built-in ATC amplification (active monitor).')}),

    C('https://atc.audio/hi-fi/loudspeakers/entry-series/scm19/',
      'ATC SCM19 bookshelf loudspeaker product page',
      'Product specifications: two-way passive loudspeaker with an ATC 25 mm soft-dome tweeter '
      'and a 150 mm ATC mid/bass driver.',
      {R('atc-scm19', 'driverCount', note='Specifications list a 25 mm tweeter and a 150 mm mid/bass driver = 2.')}),

    C('https://pmc-speakers.com/studio/active/result6',
      'PMC Result6 active studio monitor product page',
      'Product specifications: active two-way monitor with a 27 mm soft-dome HF unit and a '
      '170 mm (6.5 in) LF driver, driven by two built-in Class D amplifiers.',
      {R('pmc-result6', 'driverCount', note='Specifications list a 27 mm HF unit and a 170 mm LF driver = 2.'),
       R('pmc-result6', 'active', note='Specifications list built-in Class D amplification (active monitor).')}),

    C('https://pmc-speakers.com/studio/pmc-6-2/',
      'PMC 6-2 active studio monitor product page',
      'Product specifications: active three-way monitor with a 27 mm HF unit, a 75 mm midrange '
      'and two 150 mm (6 in) LF drivers (four drive units), driven by built-in amplification.',
      {R('pmc-pmc6-2', 'driverCount', note='Specifications list 1 HF + 1 mid + 2 LF drive units = 4.'),
       R('pmc-pmc6-2', 'active', note='Specifications list built-in amplification (active monitor).')}),

    C('https://pmc-speakers.com/studio/pmc-8-2/',
      'PMC 8-2 active studio monitor product page',
      'Product specifications: active three-way monitor with a 27 mm HF unit, a 75 mm midrange '
      'and two 200 mm (8 in) LF drivers (four drive units), driven by built-in amplification.',
      {R('pmc-pmc8-2', 'driverCount', note='Specifications list 1 HF + 1 mid + 2 LF drive units = 4.'),
       R('pmc-pmc8-2', 'active', note='Specifications list built-in amplification (active monitor).')}),

    # ---------------- Electro-Voice ----------------
    C('https://products.electrovoice.com/binary/F01U303039.pdf',
      'Electro-Voice X12-128 engineering data sheet',
      'Data sheet: X12-128 is a passive two-way 12 in loudspeaker with a 12 in (305 mm) woofer '
      'and a 1.4 in (36 mm) titanium compression driver, specified for use with an external '
      'amplifier via Speakon connectors.',
      {R('electro-voice-x12-128', 'driverCount', note='Data sheet lists a 12 in woofer and a 1.4 in compression driver = 2.'),
       R('electro-voice-x12-128', 'active', note='Data sheet specifies passive operation with external amplification.')}),

    C('https://products.electrovoice.com/binary/Force_i_E_EDS.pdf',
      'Electro-Voice Force i engineering data sheet',
      'Data sheet: Force i is a passive two-way loudspeaker with a 15 in woofer and a 1.25 in '
      'compression driver, driven by an external amplifier.',
      {R('eV-force-i', 'driverCount', note='Data sheet lists a 15 in woofer and a 1.25 in compression driver = 2.'),
       R('eV-force-i', 'active', note='Data sheet specifies passive operation with an external amplifier.')}),

    C('https://products.electrovoice.com/binary/SB122%20EDS.pdf',
      'Electro-Voice SB122 engineering data sheet',
      'Data sheet: SB122 is a passive subwoofer with a single 12 in (305 mm) woofer and no '
      'built-in amplifier.',
      {R('electro-voice-sb122', 'driverCount', note='Data sheet lists one 12 in woofer.'),
       R('electro-voice-sb122', 'active', note='Passive subwoofer; no built-in amplifier is listed.')}),

    C('https://products.electrovoice.com/binary/Sx300PI_PIX_EDS.pdf',
      'Electro-Voice Sx300PI / Sx300PIX engineering data sheet',
      'Data sheet: Sx300PI and Sx300PIX are passive, weather-resistant two-way loudspeakers '
      'intended for external amplification.',
      {R('electro-voice-sx300pi', 'active', note='Passive model; data sheet lists no built-in amplifier.'),
       R('electro-voice-sx300pix', 'active', note='Passive model; data sheet lists no built-in amplifier.')}),

    C('https://products.electrovoice.com/binary/Sx300_Engineering_Data_Sheet.pdf',
      'Electro-Voice Sx300E engineering data sheet',
      'Data sheet: Sx300E is a passive two-way loudspeaker with a 12 in (305 mm) woofer and a '
      '1.25 in (32 mm) titanium compression driver, driven by an external amplifier.',
      {R('electro-voice-sx300e', 'driverCount', note='Data sheet lists a 12 in woofer and a 1.25 in compression driver = 2.'),
       R('electro-voice-sx300e', 'active', note='Passive model; data sheet lists no built-in amplifier.')}),

    C('https://products.electrovoice.com/binary/Sx600_High_Output_Two-way_Loudspeaker_Datasheet_51_en_9006674443.pdf',
      'Electro-Voice Sx600 high-output two-way loudspeaker data sheet',
      'Data sheet: Sx600 is a passive three-way-capable two-way loudspeaker with a 15 in woofer, '
      'a 6.5 in midrange and a 1.25 in compression driver (three drive units).',
      {R('electro-voice-sx600', 'driverCount', note='Data sheet lists 15 in woofer + 6.5 in midrange + 1.25 in compression driver = 3.'),
       R('electro-voice-sx600', 'active', note='Passive model; data sheet lists no built-in amplifier.')}),

    C('https://www.electrovoice.com/product/zlx-12-g2',
      'Electro-Voice ZLX-12-G2 product page',
      'Product page identifies the model as "Passive 12\\" 2-Way Loudspeaker" with a 12 in woofer '
      'and a 1 in compression driver.',
      {R('electro-voice-zlx-12-g2', 'driverCount', note='Page lists a 12 in woofer and a 1 in compression driver = 2.'),
       R('electro-voice-zlx-12-g2', 'active', note='Page explicitly labels the model "Passive".')}),

    C('https://www.electrovoice.com/product/zlx-15-g2',
      'Electro-Voice ZLX-15-G2 product page',
      'Product page identifies the model as "Passive 15\\" 2-Way Loudspeaker" with a 15 in woofer '
      'and a 1 in compression driver.',
      {R('electro-voice-zlx-15-g2', 'driverCount', note='Page lists a 15 in woofer and a 1 in compression driver = 2.'),
       R('electro-voice-zlx-15-g2', 'active', note='Page explicitly labels the model "Passive".')}),

    C('https://www.electrovoice.com/product/zlx-8-g2',
      'Electro-Voice ZLX-8-G2 product page',
      'Product page identifies the model as "Passive 8\\" 2-Way Loudspeaker" with an 8 in woofer '
      'and a 1 in compression driver.',
      {R('electro-voice-zlx-8-g2', 'driverCount', note='Page lists an 8 in woofer and a 1 in compression driver = 2.'),
       R('electro-voice-zlx-8-g2', 'active', note='Page explicitly labels the model "Passive".')}),

    # ---------------- JBL ----------------
    C('https://jblpro.com/en-US/products/lsr305.html',
      'JBL LSR305 studio monitor product page',
      'Product page: LSR305 is a two-way powered studio monitor with a 5 in (127 mm) woofer and '
      'a 1 in (25 mm) soft-dome tweeter, driven by dual built-in Class D amplifiers.',
      {R('jbl-lsr305', 'driverCount', note='Page lists a 5 in woofer and a 1 in tweeter = 2.'),
       R('jbl-lsr305', 'active', note='Page lists dual built-in Class D amplifiers (powered monitor).')}),

    C('https://jblpro.com/en-US/site_elements/4430-and-4435-information',
      'JBL 4430 / 4435 information sheet',
      'Information sheet describes the 4430 and 4435 as passive studio monitors intended for use '
      'with an external amplifier; no powered/active variant is listed.',
      {R('jbl-4430', 'active', 'NOT_STATED', 'The sheet recommends amplifier power but does not state passive/active wording explicitly.'),
       R('legacy-jbl-6', 'active', 'NOT_STATED', 'The sheet recommends amplifier power but does not state passive/active wording explicitly.')}),

    C('https://jblpro.com/en-US/site_elements/control-25-spec-sheet',
      'JBL Control 25 specification sheet',
      'Specification sheet: Control 25 is a two-way passive loudspeaker with a 5.25 in (130 mm) '
      'woofer and a 0.75 in (19 mm) titanium dome tweeter.',
      {R('legacy-jbl-11', 'driverCount', note='Spec sheet lists a 5.25 in woofer and a 0.75 in tweeter = 2.')}),

    C('https://jblpro.com/en-US/site_elements/control-50-spec-sheet',
      'JBL Control 50 specification sheet',
      'Specification sheet: Control 50 (stored as Control 52) is a passive subwoofer/satellite '
      'system whose subwoofer enclosure uses a single 8 in (200 mm) woofer.',
      {R('jbl-control-52', 'driverCount', note='Spec sheet lists a single 8 in woofer in the subwoofer enclosure.'),
       R('jbl-control-52', 'active', note='Passive system; spec sheet lists no built-in amplifier.')}),

    C('https://jblpro.com/en-US/site_elements/jrx225-spec-sheet',
      'JBL JRX225 specification sheet',
      'Specification sheet: JRX225 is a dual 15 in two-way passive loudspeaker with two 15 in '
      '(380 mm) woofers and one 1 in (25 mm) compression driver (three drive units).',
      {R('jbl-jrx225', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'The sheet lists two 15 in woofers plus one compression driver = 3, matching the stored '
         'value, but the sheet also describes the model as "dual 15 in" which could be read as two '
         'total transducers. Not promoted pending an owner ruling on counting compression drivers.'),
       R('jbl-jrx225', 'active', 'SUPPORTED_NOT_PROMOTED',
         'The sheet describes a passive model with Speakon inputs, but does not use the word '
         '"passive"; not promoted under the standing explicit-evidence rule.')}),

    C('https://jblpro.com/en-US/site_elements/srx828sp-spec-sheet',
      'JBL SRX828SP specification sheet',
      'Specification sheet: SRX828SP is a powered dual 18 in subwoofer with two 18 in (457 mm) '
      'woofers driven by a built-in 2000 W Class D amplifier.',
      {R('jbl-srx828sp', 'driverCount', note='Spec sheet lists two 18 in woofers.'),
       R('jbl-srx828sp', 'active', note='Spec sheet lists a built-in 2000 W Class D amplifier (powered subwoofer).')}),

    C('https://jblpro.com/zh/site_elements/lsr-series-owner-s-manual',
      'JBL LSR series owner manual (Chinese-language edition)',
      'Owner manual: LSR32 is a three-way passive studio monitor with a 12 in woofer, a 5 in '
      'midrange and a 1 in tweeter (three drive units), intended for external amplification.',
      {R('jbl-lsr32', 'driverCount', note='Manual lists a 12 in woofer, a 5 in midrange and a 1 in tweeter = 3.'),
       R('jbl-lsr32', 'active', note='Manual describes passive operation with an external amplifier.')}),

    # ---------------- Mackie ----------------
    C('https://mackie.com/img/file_resources/DLM8_12_SS.pdf',
      'Mackie DLM8 / DLM12 specification sheet',
      'Specification sheet: DLM8 and DLM12 are powered two-way loudspeakers with an 8 in or 12 in '
      'woofer and a 1.75 in compression driver, driven by built-in Class D amplification.',
      {R('legacy-mack-7', 'driverCount', note='Sheet lists a woofer and a 1.75 in compression driver = 2.'),
       R('legacy-mack-7', 'active', note='Sheet lists built-in Class D amplification (powered loudspeaker).')}),

    C('https://mackie.com/img/file_resources/SRM%20V-Class_SS.pdf',
      'Mackie SRM V-Class specification sheet',
      'Specification sheet: SRM212 is a powered two-way loudspeaker with a 12 in woofer and a '
      '1.4 in titanium compression driver, driven by built-in 2000 W Class D amplification.',
      {R('mackie-srm212', 'driverCount', note='Sheet lists a 12 in woofer and a 1.4 in compression driver = 2.'),
       R('mackie-srm212', 'active', note='Sheet lists built-in 2000 W Class D amplification (powered loudspeaker).')}),

    C('https://mackie.com/img/file_resources/SRM550_650_750_SS.pdf',
      'Mackie SRM550 / SRM650 / SRM750 specification sheet',
      'Specification sheet: SRM550 is a powered two-way loudspeaker with a 12 in woofer and a '
      '1.4 in titanium compression driver, driven by built-in Class D amplification.',
      {R('mackie-srm550', 'driverCount', note='Sheet lists a 12 in woofer and a 1.4 in compression driver = 2.'),
       R('mackie-srm550', 'active', note='Sheet lists built-in Class D amplification (powered loudspeaker).')}),

    C('https://mackie.com/img/file_resources/THUMPXT_2022_SS.pdf',
      'Mackie Thump XT 2022 specification sheet',
      'Specification sheet: Thump215XT is a powered two-way loudspeaker with a 15 in woofer and '
      'a 1.4 in titanium compression driver, driven by built-in 1400 W Class D amplification.',
      {R('mackie-thump215xt', 'driverCount', note='Sheet lists a 15 in woofer and a 1.4 in compression driver = 2.'),
       R('mackie-thump215xt', 'active', note='Sheet lists built-in 1400 W Class D amplification (powered loudspeaker).')}),

    # ---------------- Bose ----------------
    C('https://boseprofessional.com/products/loudspeakers/surface-mount/designmax-surface-mount/designmax-dm5se-1-pair',
      'Bose Professional DesignMax DM5SE product page',
      'Product page: DesignMax DM5SE is a passive two-way surface-mount loudspeaker with a '
      '5.25 in (133 mm) woofer and a 1 in (25 mm) tweeter, for use with an external amplifier.',
      {R('bose-designmax-dm5se', 'driverCount', note='Page lists a 5.25 in woofer and a 1 in tweeter = 2.'),
       R('bose-designmax-dm5se', 'active', note='Passive model; page lists no built-in amplifier.')}),

    # ---------------- Dynaudio ----------------
    C('https://dynaudio.com/discontinued-models/contour-2016/contour-20',
      'Dynaudio Contour 20 (2016) product page',
      'Archived product page under Dynaudio\'s "Passive Products" navigation; lists a 28 mm '
      'Esotar2 soft-dome tweeter and an 18 cm MSP mid/bass driver.',
      {R('legacy-dyn-7', 'driverCount', note='Page lists a 28 mm tweeter and an 18 cm mid/bass driver = 2.'),
       R('legacy-dyn-7', 'active', note='Page is filed under "Passive Products"; no built-in amplifier is listed.')}),

    C('https://dynaudio.com/discontinued-models/evidence/evidence-platinum',
      'Dynaudio Evidence Platinum product page',
      'Archived product page under "Passive Products"; lists one 28 mm Esotar2 tweeter, two '
      '15 cm midrange drivers and two 20 cm woofers per cabinet (five drive units).',
      {R('legacy-dyn-4', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'Page lists 1 tweeter + 2 midrange + 2 woofers = 5 drive units, while the stored value is 8. '
         'Left unchanged; the stored value is not promoted.'),
       R('legacy-dyn-4', 'active', note='Page is filed under "Passive Products"; no built-in amplifier is listed.')}),

    C('https://dynaudio.com/home-audio/confidence/confidence-20',
      'Dynaudio Confidence 20 product page',
      'Product page in Dynaudio\'s "Passive Products" range; lists a 28 mm Esotar3 tweeter and an '
      '18 cm MSP mid/bass driver.',
      {R('dynaudio-confidence-20', 'driverCount', note='Page lists a 28 mm tweeter and an 18 cm mid/bass driver = 2.'),
       R('dynaudio-confidence-20', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/confidence/confidence-30',
      'Dynaudio Confidence 30 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Esotar3 tweeter, a 15 cm MSP '
      'midrange and two 18 cm MSP woofers (four drive units).',
      {R('dynaudio-confidence-30', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 2 woofers = 4.'),
       R('dynaudio-confidence-30', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/confidence/confidence-50',
      'Dynaudio Confidence 50 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Esotar3 tweeter, a 15 cm MSP '
      'midrange and three 18 cm MSP woofers (five drive units).',
      {R('dynaudio-confidence-50', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 3 woofers = 5.'),
       R('dynaudio-confidence-50', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/contour-i/contour-20i',
      'Dynaudio Contour 20i product page',
      'Product page in the "Passive Products" range; lists a 28 mm Esotar2i tweeter and an 18 cm '
      'MSP mid/bass driver.',
      {R('dynaudio-contour-20i', 'driverCount', note='Page lists a 28 mm tweeter and an 18 cm mid/bass driver = 2.'),
       R('dynaudio-contour-20i', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/contour-i/contour-30i',
      'Dynaudio Contour 30i product page',
      'Product page in the "Passive Products" range; lists a 28 mm Esotar2i tweeter, a 15 cm MSP '
      'midrange and two 18 cm MSP woofers (four drive units).',
      {R('dynaudio-contour-30i', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 2 woofers = 4.'),
       R('dynaudio-contour-30i', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/contour-i/contour-60i',
      'Dynaudio Contour 60i product page',
      'Product page in the "Passive Products" range; lists a 28 mm Esotar2i tweeter, a 15 cm MSP '
      'midrange and three 18 cm MSP woofers (five drive units).',
      {R('dynaudio-contour-60i', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 3 woofers = 5.'),
       R('dynaudio-contour-60i', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/emit/emit-10',
      'Dynaudio Emit 10 product page',
      'Product page in the "Passive Products" range; lists a 28 mm soft-dome tweeter and a 14 cm '
      'MSP mid/bass driver.',
      {R('dynaudio-emit-10', 'driverCount', note='Page lists a 28 mm tweeter and a 14 cm mid/bass driver = 2.'),
       R('dynaudio-emit-10', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/emit/emit-20',
      'Dynaudio Emit 20 product page',
      'Product page in the "Passive Products" range; lists a 28 mm soft-dome tweeter and an 18 cm '
      'MSP mid/bass driver.',
      {R('dynaudio-emit-20', 'driverCount', note='Page lists a 28 mm tweeter and an 18 cm mid/bass driver = 2.'),
       R('dynaudio-emit-20', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/emit/emit-30',
      'Dynaudio Emit 30 product page',
      'Product page in the "Passive Products" range; lists a 28 mm soft-dome tweeter and two 14 cm '
      'MSP woofers (three drive units).',
      {R('dynaudio-emit-30', 'driverCount', note='Page lists 1 tweeter + 2 woofers = 3.'),
       R('dynaudio-emit-30', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/evoke/evoke-10',
      'Dynaudio Evoke 10 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Cerotar soft-dome tweeter and a '
      '14 cm MSP mid/bass driver.',
      {R('dynaudio-evoke-10', 'driverCount', note='Page lists a 28 mm tweeter and a 14 cm mid/bass driver = 2.'),
       R('dynaudio-evoke-10', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/evoke/evoke-20',
      'Dynaudio Evoke 20 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Cerotar soft-dome tweeter and an '
      '18 cm MSP mid/bass driver.',
      {R('dynaudio-evoke-20', 'driverCount', note='Page lists a 28 mm tweeter and an 18 cm mid/bass driver = 2.'),
       R('dynaudio-evoke-20', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/evoke/evoke-30',
      'Dynaudio Evoke 30 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Cerotar soft-dome tweeter and '
      'two 14 cm MSP woofers (three drive units).',
      {R('dynaudio-evoke-30', 'driverCount', note='Page lists 1 tweeter + 2 woofers = 3.'),
       R('dynaudio-evoke-30', 'active', note='Page is in the "Passive Products" range.')}),

    C('https://dynaudio.com/home-audio/evoke/evoke-50',
      'Dynaudio Evoke 50 product page',
      'Product page in the "Passive Products" range; lists a 28 mm Cerotar soft-dome tweeter, a '
      '15 cm MSP midrange and two 18 cm MSP woofers (four drive units).',
      {R('dynaudio-evoke-50', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 2 woofers = 4.'),
       R('dynaudio-evoke-50', 'active', note='Page is in the "Passive Products" range.')}),

    # ---------------- Focal ----------------
    C('https://dam.focal-naim.com/m/3432373bae914d13/original/FP_Chora806_GB-pdf.pdf',
      'Focal Chora 806 product sheet',
      'Product sheet: 2-way bass-reflex bookshelf speaker with a 1 in (25 mm) TNF aluminium/'
      'magnesium inverted dome tweeter and a 6.5 in (165 mm) Slatefiber mid/bass driver.',
      {R('focal-chora-806', 'driverCount', note='Sheet lists a 1 in tweeter and a 6.5 in mid/bass driver = 2.')}),

    C('https://dam.focal-naim.com/m/5b74d69b5e450e5b/original/FP_Chora826_GB-pdf.pdf',
      'Focal Chora 826 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and two 6.5 in woofers (four drive units).',
      {R('focal-chora-826', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://dam.focal-naim.com/m/733c5c6acac9341c/original/FP_Aria_906_GB-pdf.pdf',
      'Focal Aria 906 product sheet',
      'Product sheet: 2-way bass-reflex bookshelf speaker with a 1 in (25 mm) TNF aluminium/'
      'magnesium inverted dome tweeter and a 6.5 in (165 mm) Flax mid/bass driver.',
      {R('legacy-focal-8', 'driverCount', note='Sheet lists a 1 in tweeter and a 6.5 in mid/bass driver = 2.')}),

    C('https://dam.focal-naim.com/m/75f492b929881650/original/FP_Alpha_80_Evo_EN-pdf.pdf',
      'Focal Alpha 80 Evo product sheet',
      'Product sheet: active 2-way nearfield monitor with a 1 in (25 mm) aluminium inverted dome '
      'tweeter and an 8 in (203 mm) Slatefiber woofer, driven by built-in Class AB/Class D '
      'amplification.',
      {R('focal-alpha-80-evo', 'driverCount', note='Sheet lists a 1 in tweeter and an 8 in woofer = 2.'),
       R('focal-alpha-80-evo', 'active', note='Sheet lists built-in amplification (active monitor).')}),

    C('https://media.focal-naim.com/dam/aria-926/fp_aria_926_gb.pdf',
      'Focal Aria 926 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and two 6.5 in woofers (four drive units).',
      {R('focal-aria-926', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://media.focal-naim.com/dam/aria-936/fp_aria_936_gb.pdf',
      'Focal Aria 936 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and three 6.5 in woofers (five drive units).',
      {R('focal-aria-936', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 3 woofers = 5.')}),

    C('https://media.focal-naim.com/dam/aria-948/fp_aria_948_gb.pdf',
      'Focal Aria 948 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and two 8.25 in woofers (four drive units).',
      {R('focal-aria-948', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://media.focal-naim.com/dam/electra-sw1000-be/notice_electra1000_be-s.pdf',
      'Focal Electra SW 1000 Be owner manual',
      'Owner manual: the Electra SW 1000 Be subwoofer uses a single 13 in (330 mm) "W" cone '
      'woofer, driven by a built-in 1000 W BASH amplifier.',
      {R('legacy-focal-2', 'driverCount', 'CONFLICT',
         'Manual describes a single 13 in woofer for the SW 1000 Be subwoofer, while the stored '
         'record shows 4. Left unchanged; the stored value is not promoted.'),
       R('legacy-focal-2', 'active', 'PROMOTED', 'Manual lists a built-in 1000 W BASH amplifier (powered subwoofer).')}),

    C('https://media.focal-naim.com/dam/grande-utopia-em-evo/notice_grandeutopiaemevo_web.pdf',
      'Focal Grande Utopia EM Evo owner manual',
      'Owner manual: 4-way floorstanding loudspeaker with a 1 in IHL beryllium tweeter, a 6.5 in '
      'midrange, an 11 in midbass and two 16 in woofers (five drive units); the manual describes '
      'passive operation with external amplification.',
      {R('focal-grande-utopia-em-evo', 'driverCount', note='Manual lists 1 tweeter + 1 midrange + 1 midbass + 2 woofers = 5.'),
       R('focal-grande-utopia-em-evo', 'active', note='Manual describes passive operation with external amplification.')}),

    C('https://media.focal-naim.com/dam/kanta-n-1/fp_kantan-1_en.pdf',
      'Focal Kanta N°1 product sheet',
      'Product sheet: 2-way bass-reflex bookshelf speaker with a 1 in IHL beryllium tweeter and a '
      '6.5 in "W" midbass driver.',
      {R('focal-kanta-n-1', 'driverCount', note='Sheet lists a 1 in tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://media.focal-naim.com/dam/kanta-n-2/fp_kanta_n-2_en.pdf',
      'Focal Kanta N°2 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and two 6.5 in woofers (four drive units).',
      {R('focal-kanta-n-2', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://media.focal-naim.com/dam/kanta-n-3/fp_kanta_n-3_en.pdf',
      'Focal Kanta N°3 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in tweeter, a 6.5 in '
      'midrange and two 8.25 in woofers (four drive units).',
      {R('focal-kanta-n-3', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://media.focal-naim.com/dam/maestro-utopia-evo/notice_maestroutopiaevo_codo1510_bc_web.pdf',
      'Focal Maestro Utopia Evo owner manual',
      'Owner manual: 3-way floorstanding loudspeaker with a 1 in IHL beryllium tweeter, a 6.5 in '
      'midrange and two 11 in woofers (four drive units); passive operation with external '
      'amplification.',
      {R('focal-maestro-utopia-evo', 'driverCount', note='Manual lists 1 tweeter + 1 midrange + 2 woofers = 4.'),
       R('focal-maestro-utopia-evo', 'active', note='Manual describes passive operation with external amplification.')}),

    C('https://media.focal-naim.com/dam/scala-utopia-evo/fp_scala_utopia_evo_en.pdf',
      'Focal Scala Utopia Evo product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in IHL beryllium tweeter, a '
      '6.5 in midrange and two 8.25 in woofers (four drive units).',
      {R('focal-scala-utopia-evo', 'driverCount', 'CONFLICT',
         'Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4, while the stored value is 3. Left '
         'unchanged; the stored value is not promoted.')}),

    C('https://media.focal-naim.com/dam/sopra-n-1/fp_sopra_n1_en.pdf',
      'Focal Sopra N°1 product sheet',
      'Product sheet: 2-way bass-reflex bookshelf speaker with a 1 in IHL beryllium tweeter and a '
      '6.5 in "W" midbass driver.',
      {R('focal-sopra-n-1', 'driverCount', note='Sheet lists a 1 in tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://media.focal-naim.com/dam/sopra-n-2/fp_sopra_n2_en.pdf',
      'Focal Sopra N°2 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in IHL beryllium tweeter, a '
      '6.5 in "W" midrange and two 7 in "W" woofers (four drive units).',
      {R('focal-sopra-n-2', 'active', 'NOT_STATED',
         'Sheet gives only a recommended amplifier-power range (40-300 W) and no passive/active wording.'),
       R('focal-sopra-n-2', 'driverCount', 'PROMOTED', 'Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4 (already verified).')}),

    C('https://media.focal-naim.com/dam/sopra-n-3/fp_sopra_n3_en.pdf',
      'Focal Sopra N°3 product sheet',
      'Product sheet: 3-way bass-reflex floorstanding speaker with a 1 in IHL beryllium tweeter, a '
      '6.5 in "W" midrange and two 8.25 in "W" woofers (four drive units).',
      {R('focal-sopra-n-3', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://media.focal-naim.com/dam/sub-one/fp_sub_one_en.pdf',
      'Focal Sub One product sheet',
      'Product sheet: active subwoofer with two 8 in (20 cm) Slatefiber woofers and a built-in '
      '2 x 200 W Class D amplifier.',
      {R('focal-sub-one', 'driverCount', note='Sheet lists two 8 in woofers.'),
       R('focal-sub-one', 'active', note='Sheet lists a built-in 2 x 200 W Class D amplifier.')}),

    C('https://media.focal-naim.com/dam/sub6/fp_sub6_gb.pdf',
      'Focal Sub6 product sheet',
      'Product sheet: active subwoofer with a single 11 in (27 cm) "W" cone woofer and a built-in '
      '350 W BASH amplifier.',
      {R('focal-sub6', 'driverCount', note='Sheet lists one 11 in woofer.'),
       R('focal-sub6', 'active', note='Sheet lists a built-in 350 W BASH amplifier.')}),

    C('https://media.focal-naim.com/dam/trio6/fp_trio_6_black_en.pdf',
      'Focal Trio6 product sheet',
      'Product sheet: active 3-way monitor with a 1 in beryllium tweeter, a 5 in "W" midrange and '
      'an 8 in "W" woofer, driven by built-in Class AB/Class D amplification.',
      {R('focal-trio6', 'driverCount', note='Sheet lists a 1 in tweeter, a 5 in midrange and an 8 in woofer = 3.'),
       R('focal-trio6', 'active', note='Sheet lists built-in amplification (active monitor).')}),

    C('https://www.focal.com/products/alpha-65-evo',
      'Focal Alpha 65 Evo product page',
      'Product page: active 2-way nearfield monitor with a 1 in aluminium inverted dome tweeter '
      'and a 6.5 in Slatefiber woofer, driven by built-in amplification.',
      {R('focal-alpha-65-evo', 'driverCount', note='Page lists a 1 in tweeter and a 6.5 in woofer = 2.'),
       R('focal-alpha-65-evo', 'active', note='Page lists built-in amplification (active monitor).')}),

    # ---------------- Genelec ----------------
    C('https://www.genelec.com/-/new-genelec-4430-loudspeaker-gives-the-av-world-exceptional-sound-quality-over-ip-1',
      'Genelec press release: 4430A loudspeaker (stored as legacy-gen-8)',
      'Press release: the 4430A is an active two-way loudspeaker with two 130 mm (5 in) drivers '
      'and built-in amplification (Class D), networked over IP.',
      {R('legacy-gen-8', 'driverCount', note='Release lists two 130 mm drivers = 2.'),
       R('legacy-gen-8', 'active', note='Release describes an active loudspeaker with built-in amplification.')}),

    C('https://www.genelec.com/1237a',
      'Genelec 1237A studio monitor product page',
      'Product page: 1237A is an active three-way monitor with a 12 in woofer, a 5 in midrange and '
      'a 1 in tweeter (three drive units), driven by built-in Class D amplification.',
      {R('legacy-gen-9', 'driverCount', note='Page lists a 12 in woofer, a 5 in midrange and a 1 in tweeter = 3.'),
       R('legacy-gen-9', 'active', note='Page lists built-in Class D amplification (active monitor).')}),

    C('https://www.genelec.com/8361a',
      'Genelec 8361A studio monitor product page',
      'Product page: 8361A is an active three-way monitor with two 10 in woofers, a 5 in midrange '
      'and a 1 in tweeter (four drive units), driven by built-in Class D amplification.',
      {R('genelec-8361a', 'driverCount', note='Page lists two 10 in woofers + 5 in midrange + 1 in tweeter = 4.'),
       R('genelec-8361a', 'active', note='Page lists built-in Class D amplification (active monitor).')}),

    # ---------------- L-Acoustics ----------------
    C('https://www.l-acoustics.com/products/syva/',
      'L-Acoustics Syva product page',
      'Product page: Syva is a passive two-way colinear source with six 3 in midrange drivers and '
      'three 1.75 in compression drivers (nine drive units), for use with an external amplified '
      'controller.',
      {R('legacy-la-6', 'driverCount', note='Page lists six 3 in midrange drivers and three 1.75 in compression drivers = 9.'),
       R('legacy-la-6', 'active', note='Passive system; page specifies an external amplified controller.')}),

    C('https://www.l-acoustics.com/products/k1/',
      'L-Acoustics K1 product page',
      'Product page: K1 is a passive three-way line array with two 15 in woofers, four 6.5 in '
      'midrange drivers and three 2 in compression drivers (nine drive units).',
      {R('legacy-la-4', 'driverCount', note='Page lists 2 woofers + 4 midrange drivers + 3 compression drivers = 9.')}),

    C('https://www.l-acoustics.com/products/k2/',
      'L-Acoustics K2 product page',
      'Product page: K2 is a passive three-way line array with two 12 in woofers, four 6.5 in '
      'midrange drivers and two 3 in compression drivers (eight drive units).',
      {R('legacy-la-5', 'driverCount', note='Page lists 2 woofers + 4 midrange drivers + 2 compression drivers = 8.')}),

    # ---------------- MartinLogan ----------------
    C('https://www.martinlogan.com/en/product/electromotion-esl-x',
      'MartinLogan ElectroMotion ESL X product page',
      'Product page: ElectroMotion ESL X is a hybrid electrostatic floorstanding speaker with a '
      'Folded Motion XT tweeter, a 6.5 in midrange and two 8 in woofers (three conventional drive '
      'units plus the electrostatic panel).',
      {R('martinlogan-esl-x', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'Page describes an electrostatic panel plus 1 tweeter + 1 midrange + 2 woofers; the schema '
         'does not define whether the ESL panel counts, and the stored value is 3. Not promoted.'),
       R('martinlogan-esl-x', 'active', 'NOT_STATED', 'The page gives recommended amplifier power but no explicit passive/active wording.')}),

    C('https://www.martinlogan.com/en/product/motion-20',
      'MartinLogan Motion 20 product page',
      'Product page: Motion 20 is a 2.5-way floorstanding speaker with a Folded Motion tweeter, a '
      '5.5 in midrange and two 5.5 in woofers (three drive units).',
      {R('martinlogan-motion-20', 'driverCount', note='Page lists 1 tweeter + 1 midrange + 2 woofers = 3.'),
       R('martinlogan-motion-20', 'active', 'NOT_STATED', 'The page gives recommended amplifier power but no explicit passive/active wording.')}),

    C('https://www.martinlogan.com/en/product/motion-60xt',
      'MartinLogan Motion 60XT product page',
      'Product page specifications: 1.25 x 2.4 in Folded Motion XT tweeter, 6.5 in aluminium cone '
      'midrange and two 8 in aluminium cone woofers (four drive units); recommended amplifier '
      'power 20-400 W per channel, with no explicit passive/active wording.',
      {R('martinlogan-motion-60xt', 'active', 'NOT_STATED',
         'Specification table gives only recommended amplifier power (20-400 W/ch) and no passive/active wording.'),
       R('martinlogan-motion-60xt', 'driverCount', 'PROMOTED', 'Specification table lists 1 tweeter + 1 midrange + 2 woofers = 4 (already verified).')}),

    C('https://www.martinlogan.com/uploads/documents/brochures/brochure_motion40.pdf',
      'MartinLogan Motion 40 brochure',
      'Brochure: Motion 40 is a 2.5-way floorstanding speaker with a Folded Motion tweeter, a '
      '5.5 in midrange and two 5.5 in woofers (three drive units).',
      {R('martinlogan-motion-40', 'driverCount', 'CONFLICT',
         'Brochure lists 1 tweeter + 1 midrange + 2 woofers = 5 drive units, while the stored value '
         'is 4. Left unchanged; the stored value is not promoted.')}),

    # ---------------- Wharfedale ----------------
    C('https://www.wharfedale.co.uk/products/linton',
      'Wharfedale Linton heritage loudspeaker product page',
      'Product page specifications: 3-way bass-reflex with a 1 in (25 mm) textile dome tweeter, a '
      '5 in (130 mm) Kevlar midrange and an 8 in (200 mm) Kevlar woofer (three drive units).',
      {R('wharfedale-linton', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 1 woofer = 3.')}),

    C('https://www.wharfedale.co.uk/products/diamond-12-0',
      'Wharfedale Diamond 12.0 product page',
      'Product page specifications: 2-way bass-reflex bookshelf with a 1 in (25 mm) textile dome '
      'tweeter and a 4 in (100 mm) PP cone midbass driver.',
      {R('wharfedale-diamond-12-0', 'driverCount', note='Specifications list a 1 in tweeter and a 4 in midbass driver = 2.')}),

    C('https://www.wharfedale.co.uk/products/diamond-12-2',
      'Wharfedale Diamond 12.2 product page',
      'Product page specifications: 2-way bass-reflex bookshelf with a 1 in (25 mm) textile dome '
      'tweeter and a 6.5 in (150 mm) PP cone midbass driver.',
      {R('wharfedale-diamond-12-2', 'driverCount', note='Specifications list a 1 in tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://www.wharfedale.co.uk/products/evo4-1',
      'Wharfedale EVO4.1 product page',
      'Product page specifications: 2-way bass-reflex standmount with an AMT tweeter and a 5 in '
      '(130 mm) woven Kevlar midbass driver.',
      {R('wharfedale-evo4-1', 'driverCount', note='Specifications list an AMT tweeter and a 5 in midbass driver = 2.')}),

    C('https://www.wharfedale.co.uk/products/evo4-2',
      'Wharfedale EVO4.2 product page',
      'Product page specifications: 3-way bass-reflex standmount with an AMT tweeter, a 2 in '
      '(50 mm) soft-dome midrange and a 6.5 in (165 mm) woven Kevlar woofer (three drive units).',
      {R('wharfedale-evo4-2', 'driverCount', note='Specifications list AMT tweeter + 2 in midrange + 6.5 in woofer = 3.')}),

    # ---------------- DALI ----------------
    C('https://www.dali-speakers.com/en/products/discontinued/epicon/epicon-2/',
      'DALI EPICON 2 product page',
      'Product page specifications: 2-way bass-reflex standmount with a 29 mm soft-dome ribbon '
      'tweeter and a 6.5 in wood-fibre midbass driver.',
      {R('dali-epicon-2', 'driverCount', note='Specifications list a 29 mm tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://www.dali-speakers.com/en-us/products/discontinued/epicon/epicon-6/',
      'DALI EPICON 6 product page',
      'Product page specifications: 2.5-way bass-reflex floorstanding speaker with a 29 mm ribbon '
      'tweeter, a 6.5 in wood-fibre midrange and two 6.5 in wood-fibre woofers (four drive units).',
      {R('dali-epicon-6', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.dali-speakers.com/en/products/discontinued/epicon/epicon-8/',
      'DALI EPICON 8 product page',
      'Product page specifications: 3-way bass-reflex floorstanding speaker with a 29 mm ribbon '
      'tweeter, a 5 in midrange and three 8 in wood-fibre woofers (five drive units).',
      {R('dali-epicon-8', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 3 woofers = 5.')}),

    C('https://www.dali-speakers.com/en-us/products/opticon-mk2/opticon-8-mk2/',
      'DALI OPTICON 8 MK2 product page',
      'Product page specifications: 3-way bass-reflex floorstanding speaker with a 29 mm soft-dome '
      'tweeter, a 6.5 in midrange and two 8 in woofers plus two 8 in passive radiators. The driven '
      'count is five.',
      {R('dali-opticon-8-mk2', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
         'Page lists 5 driven units plus 2 passive radiators; the schema does not define whether '
         'passive radiators count, and the stored value is 5. Not promoted.')}),

    C('https://www.dali-speakers.com/en/products/opticon-mk2/opticon-2-mk2/',
      'DALI OPTICON 2 MK2 product page',
      'Product page specifications: 2-way bass-reflex standmount with a 29 mm soft-dome tweeter and '
      'a 6.5 in wood-fibre midbass driver.',
      {R('dali-opticon-2-mk2', 'driverCount', note='Specifications list a 29 mm tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://www.dali-speakers.com/en/products/opticon-mk2/opticon-6-mk2/',
      'DALI OPTICON 6 MK2 product page',
      'Product page specifications: 2.5-way bass-reflex floorstanding speaker with a 29 mm '
      'soft-dome tweeter, a 6.5 in midrange and two 6.5 in woofers (four drive units).',
      {R('dali-opticon-6-mk2', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.dali-speakers.com/en/products/discontinued/rubicon/rubicon-2/',
      'DALI RUBICON 2 product page',
      'Product page specifications: 2-way bass-reflex standmount with a 29 mm soft-dome ribbon '
      'tweeter and a 6.5 in wood-fibre midbass driver.',
      {R('dali-rubicon-2', 'driverCount', note='Specifications list a 29 mm tweeter and a 6.5 in midbass driver = 2.')}),

    C('https://www.dali-speakers.com/en/products/discontinued/rubicon/rubicon-6/',
      'DALI RUBICON 6 product page',
      'Product page specifications: 2.5-way bass-reflex floorstanding speaker with a 29 mm ribbon '
      'tweeter, a 6.5 in midrange and two 6.5 in woofers (four drive units).',
      {R('dali-rubicon-6', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.dali-speakers.com/en/products/discontinued/rubicon/rubicon-8/',
      'DALI RUBICON 8 product page',
      'Product page specifications: 3-way bass-reflex floorstanding speaker with a 29 mm ribbon '
      'tweeter, a 6.5 in midrange and three 6.5 in woofers (five drive units).',
      {R('dali-rubicon-8', 'driverCount', note='Specifications list 1 tweeter + 1 midrange + 3 woofers = 5.')}),

    # ---------------- ADAM Audio ----------------
    C('https://www.adam-audio.com/content/uploads/2016/12/adam-audio-user-manual-A7-fr.pdf',
      'ADAM Audio A7 user manual (French edition)',
      'User manual: A7 is an active 2-way nearfield monitor with a 1 in X-ART tweeter and a 7 in '
      'woofer, driven by built-in 2 x 100 W amplifiers.',
      {R('adam-a7', 'driverCount', note='Manual lists a 1 in tweeter and a 7 in woofer = 2.'),
       R('adam-a7', 'active', note='Manual lists built-in 2 x 100 W amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/a-series/a44h/',
      'ADAM Audio A44H product page',
      'Product page: A44H is an active 2-way monitor with two 4 in woofers and a 1 in X-ART '
      'tweeter (three drive units), driven by built-in DSP/amplification.',
      {R('adam-audio-a44h', 'driverCount', note='Page lists two 4 in woofers plus one 1 in tweeter = 3.'),
       R('adam-audio-a44h', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/a-series/a4v/',
      'ADAM Audio A4V product page',
      'Product page: A4V is an active 2-way monitor with a 4 in woofer and a 1 in X-ART tweeter, '
      'driven by built-in DSP/amplification.',
      {R('adam-a4v', 'driverCount', note='Page lists a 4 in woofer and a 1 in tweeter = 2.'),
       R('adam-a4v', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/a-series/a77h/',
      'ADAM Audio A77H product page',
      'Product page: A77H is an active 3-way monitor with two 7 in woofers, a 3.5 in midrange and '
      'a 1 in X-ART tweeter (four drive units), driven by built-in amplification.',
      {R('adam-audio-a77h', 'driverCount', note='Page lists two 7 in woofers + 3.5 in midrange + 1 in tweeter = 4.'),
       R('adam-audio-a77h', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/a-series/a7v/',
      'ADAM Audio A7V product page',
      'Product page: A7V is an active 2-way monitor with a 7 in woofer and a 1 in X-ART tweeter, '
      'driven by built-in amplification.',
      {R('legacy-adam-4', 'driverCount', note='Page lists a 7 in woofer and a 1 in tweeter = 2.'),
       R('legacy-adam-4', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/a-series/a8h/',
      'ADAM Audio A8H product page',
      'Product page: A8H is an active 3-way monitor with two 8 in woofers, a 3.5 in midrange and '
      'a 1 in X-ART tweeter (four drive units), driven by built-in amplification.',
      {R('adam-a8h', 'driverCount', 'CONFLICT',
         'Page lists two 8 in woofers + 3.5 in midrange + 1 in tweeter = 4, while the stored value '
         'is 3. Left unchanged; the stored value is not promoted.')}),

    C('https://www.adam-audio.com/en/archived-products/s3a/',
      'ADAM Audio S3A archived product page',
      'Archived product page: S3A is an active 3-way monitor with two 7 in woofers, a 4 in '
      'midrange and a 1 in X-ART tweeter (four drive units).',
      {R('legacy-adam-1', 'driverCount', 'CONFLICT',
         'Page lists two 7 in woofers + 4 in midrange + 1 in tweeter = 4, while the stored value is '
         '3. Left unchanged; the stored value is not promoted.'),
       R('legacy-adam-1', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/ax-series/a5x/',
      'ADAM Audio A5X product page',
      'Product page: A5X is an active 2-way monitor with a 5 in woofer and a 1 in X-ART tweeter, '
      'driven by built-in amplification.',
      {R('adam-a5x', 'driverCount', note='Page lists a 5 in woofer and a 1 in tweeter = 2.'),
       R('adam-a5x', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/s-series/s2v/',
      'ADAM Audio S2V product page',
      'Product page: S2V is an active 2-way monitor with a 7 in woofer and a 1 in S-ART tweeter, '
      'driven by built-in amplification.',
      {R('legacy-adam-6', 'driverCount', note='Page lists a 7 in woofer and a 1 in tweeter = 2.'),
       R('legacy-adam-6', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/s-series/s3h/',
      'ADAM Audio S3H product page',
      'Product page: S3H is an active 3-way monitor with two 7 in woofers, a 4 in midrange and a '
      '1 in S-ART tweeter (four drive units).',
      {R('adam-audio-s3h', 'driverCount', note='Page lists two 7 in woofers + 4 in midrange + 1 in tweeter = 4.'),
       R('adam-audio-s3h', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/s-series/s3v/',
      'ADAM Audio S3V product page',
      'Product page: S3V is an active 3-way monitor with two 7 in woofers and a 4 in midrange plus '
      'a 1 in S-ART tweeter (four drive units).',
      {R('adam-audio-s3v', 'driverCount', 'CONFLICT',
         'Page lists two 7 in woofers + 4 in midrange + 1 in tweeter = 4, while the stored value is '
         '3. Left unchanged; the stored value is not promoted.'),
       R('adam-audio-s3v', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/s-series/s5h/',
      'ADAM Audio S5H product page',
      'Product page: S5H is an active 3-way monitor with two 10 in woofers, a 4 in midrange and a '
      '1 in S-ART tweeter (four drive units).',
      {R('adam-audio-s5h', 'driverCount', note='Page lists two 10 in woofers + 4 in midrange + 1 in tweeter = 4.'),
       R('adam-audio-s5h', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/sx-series/s3x-v/',
      'ADAM Audio S3X-V product page',
      'Product page: S3X-V is an active 3-way monitor with two 7 in woofers, a 4 in midrange and a '
      '1 in X-ART tweeter (four drive units).',
      {R('adam-s3x', 'driverCount', 'CONFLICT',
         'Page lists two 7 in woofers + 4 in midrange + 1 in tweeter = 4, while the stored value is '
         '3. Left unchanged; the stored value is not promoted.'),
       R('adam-s3x', 'active', note='Page describes built-in amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/t-series/t5v/',
      'ADAM Audio T5V product page',
      'Product page: T5V is an active 2-way monitor with a 5 in woofer and a 1.9 in U-ART '
      'tweeter, driven by built-in 2 x 50 W amplification.',
      {R('adam-t5v', 'driverCount', note='Page lists a 5 in woofer and a 1.9 in tweeter = 2.'),
       R('adam-t5v', 'active', note='Page lists built-in 2 x 50 W amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/t-series/t7v/',
      'ADAM Audio T7V product page',
      'Product page: T7V is an active 2-way monitor with a 7 in woofer and a 1.9 in U-ART '
      'tweeter, driven by built-in 2 x 50 W amplification.',
      {R('adam-audio-t7v', 'driverCount', note='Page lists a 7 in woofer and a 1.9 in tweeter = 2.'),
       R('adam-audio-t7v', 'active', note='Page lists built-in 2 x 50 W amplification (active monitor).')}),

    C('https://www.adam-audio.com/en/t-series/t8v/',
      'ADAM Audio T8V product page',
      'Product page: T8V is an active 2-way monitor with an 8 in woofer and a 1.9 in U-ART '
      'tweeter, driven by built-in 2 x 50 W amplification.',
      {R('adam-audio-t8v', 'driverCount', note='Page lists an 8 in woofer and a 1.9 in tweeter = 2.'),
       R('adam-audio-t8v', 'active', note='Page lists built-in 2 x 50 W amplification (active monitor).')}),

    # ---------------- Bowers & Wilkins ----------------
    C('https://www.bowerswilkins.com/en-us/product/loudspeakers/603-s3/300659.html',
      'Bowers & Wilkins 603 S3 product page',
      'Product page technical details: 3-way vented-box system with one 25 mm titanium dome '
      'tweeter, one 150 mm Continuum FST midrange and two 165 mm paper-cone bass drivers (four '
      'drive units). The page lists no built-in amplifier.',
      {R('bowers-wilkins-603-s3', 'driverCount', note='Technical details list 1 tweeter + 1 midrange + 2 woofers = 4.'),
       R('bowers-wilkins-603-s3', 'active', 'NOT_STATED', 'Product page lists recommended amplifier power but no explicit passive/active wording.')}),

    C('https://www.bowerswilkins.com/en-us/product/subwoofers/asw-series/asw610/150059.html',
      'Bowers & Wilkins ASW610 subwoofer product page',
      'Product page: ASW610 is an active subwoofer with a single 250 mm (10 in) paper/AramID '
      'cone woofer and a built-in 200 W Class D amplifier.',
      {R('bowers-wilkins-asw610', 'driverCount', note='Page lists one 250 mm woofer.'),
       R('bowers-wilkins-asw610', 'active', note='Page lists a built-in 200 W Class D amplifier (active subwoofer).')}),

    C('https://www.bowerswilkins.com/en-us/product/system-products/607-s3/300661-01-00-005.html',
      'Bowers & Wilkins 607 S3 product page',
      'Product page technical details: 2-way vented-box system with one 25 mm titanium dome '
      'tweeter and one 130 mm Continuum cone bass/midrange driver (two drive units).',
      {R('bowers-wilkins-607-s3', 'driverCount', note='Technical details list a 25 mm tweeter and a 130 mm bass/midrange driver = 2.'),
       R('bowers-wilkins-607-s3', 'active', 'NOT_STATED', 'Product page lists recommended amplifier power but no explicit passive/active wording.')}),

    C('https://www.bowerswilkins.com/product/loudspeakers/606-s3/300660.html',
      'Bowers & Wilkins 606 S3 product page',
      'Product page technical details: 2-way vented-box system with one 25 mm titanium dome '
      'tweeter and one 165 mm Continuum cone bass/midrange driver (two drive units).',
      {R('bowers-wilkins-606-s3', 'driverCount', note='Technical details list a 25 mm tweeter and a 165 mm bass/midrange driver = 2.'),
       R('bowers-wilkins-606-s3', 'active', 'NOT_STATED', 'Product page lists recommended amplifier power but no explicit passive/active wording.')}),

    C('https://www.bowerswilkins.com/en/product/archive-speakers/formation-flex/FP41343P.html',
      'Bowers & Wilkins Formation Flex archived product page',
      'Archived product page: Formation Flex is a powered wireless speaker with two 25 mm '
      '(1 in) decoupled double-dome tweeters and two 90 mm (3.5 in) woofers, with built-in '
      'amplification.',
      {R('bowers-wilkins-formation-flex', 'driverCount', note='Page lists one 25 mm tweeter and one 90 mm woofer = 2 drive units.'),
       R('bowers-wilkins-formation-flex', 'active', note='Page describes a powered wireless speaker with built-in amplification.')}),

    C('https://www.bowerswilkins.com/en/product/archive/formation-wedge/FP40664P.html',
      'Bowers & Wilkins Formation Wedge archived product page',
      'Archived product page: Formation Wedge is a powered wireless speaker with one 25 mm '
      'double-dome tweeter, two 90 mm midrange drivers and two 150 mm woofers (five drive units).',
      {R('bowers-wilkins-formation-wedge', 'driverCount', note='Page lists 1 tweeter + 2 midrange + 2 woofers = 5.'),
       R('bowers-wilkins-formation-wedge', 'active', note='Page describes a powered wireless speaker with built-in amplification.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw0a89b49d/downloads/db1d-information-sheet.pdf',
      'Bowers & Wilkins DB1D information sheet',
      'Information sheet: DB1D is an active subwoofer with two 300 mm (12 in) Aerofoil cone '
      'woofers and a built-in 2000 W Class D amplifier.',
      {R('bowers-wilkins-db1d', 'driverCount', note='Sheet lists two 300 mm woofers.'),
       R('bowers-wilkins-db1d', 'active', note='Sheet lists a built-in 2000 W Class D amplifier (active subwoofer).')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw45a50a72/downloads/db4s-info-sheet.pdf',
      'Bowers & Wilkins DB4S information sheet',
      'Information sheet: DB4S is an active subwoofer with a single 300 mm (12 in) Aerofoil cone '
      'woofer and a built-in 1000 W Class D amplifier.',
      {R('bowers-wilkins-db4s', 'driverCount', note='Sheet lists one 300 mm woofer.'),
       R('bowers-wilkins-db4s', 'active', note='Sheet lists a built-in 1000 W Class D amplifier (active subwoofer).')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dwb626b11c/downloads/db3d-information-sheet.pdf',
      'Bowers & Wilkins DB3D information sheet',
      'Information sheet: DB3D is an active subwoofer with two 200 mm (8 in) Aerofoil cone woofers '
      'and a built-in 1000 W Class D amplifier.',
      {R('bowers-wilkins-db3d', 'driverCount', note='Sheet lists two 200 mm woofers.'),
       R('bowers-wilkins-db3d', 'active', note='Sheet lists a built-in 1000 W Class D amplifier (active subwoofer).')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dwd8ffb860/downloads/db2d-information-sheet.pdf',
      'Bowers & Wilkins DB2D information sheet',
      'Information sheet: DB2D is an active subwoofer with two 250 mm (10 in) Aerofoil cone '
      'woofers and a built-in 1000 W Class D amplifier.',
      {R('bowers-wilkins-db2d', 'driverCount', note='Sheet lists two 250 mm woofers.'),
       R('bowers-wilkins-db2d', 'active', note='Sheet lists a built-in 1000 W Class D amplifier (active subwoofer).')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_apac_shared/default/dw49334432/archive-manuals/800-d3-info-sheet.pdf',
      'Bowers & Wilkins 800 D3 information sheet (archive)',
      'Information sheet: 800 D3 is a 3-way vented-box system with one 25 mm diamond dome '
      'tweeter, one 150 mm Continuum FST midrange and two 250 mm Aerofoil bass drivers (four '
      'drive units).',
      {R('legacy-bw-7', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw5e6a829f/downloads/english--bw--702-s3-information-sheet.pdf',
      'Bowers & Wilkins 702 S3 information sheet',
      'Information sheet: 702 S3 is a 3-way vented-box system with one 25 mm carbon-dome '
      'tweeter, one 150 mm Continuum FST midrange and three 165 mm Aerofoil bass drivers (five '
      'drive units).',
      {R('bowers-wilkins-702-s3', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 3 woofers = 5.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw63583732/downloads/english--bw--704-s3-information-sheet.pdf',
      'Bowers & Wilkins 704 S3 information sheet',
      'Information sheet: 704 S3 is a 3-way vented-box system with one 25 mm carbon-dome '
      'tweeter, one 130 mm Continuum FST midrange and two 165 mm Aerofoil bass drivers (four '
      'drive units).',
      {R('bowers-wilkins-704-s3', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw7433324b/archive-manuals/eng_ft00061_dm6_info_sheet.pdf',
      'Bowers & Wilkins DM6 information sheet (archive)',
      'Archived information sheet: DM6 is a 3-way system with one 25 mm dome tweeter, one 130 mm '
      'midrange and one 200 mm woofer (three drive units).',
      {R('legacy-bw-1', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 1 woofer = 3.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw7f94b222/archive-manuals/802-d3-info-sheet.pdf',
      'Bowers & Wilkins 802 D3 information sheet (archive)',
      'Information sheet: 802 D3 is a 3-way vented-box system with one 25 mm diamond dome '
      'tweeter, one 150 mm Continuum FST midrange and two 200 mm Aerofoil bass drivers (four '
      'drive units).',
      {R('bw-802d3', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dwd7be5f6c/downloads/804d4-information-sheet.pdf',
      'Bowers & Wilkins 804 D4 information sheet',
      'Information sheet: 804 D4 is a 3-way vented-box system with one 25 mm diamond dome '
      'tweeter, one 130 mm Continuum FST midrange and two 165 mm Aerofoil bass drivers (four '
      'drive units).',
      {R('bowers-wilkins-804-d4', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dwdf0b2886/downloads/803D4-Information-Sheet.pdf',
      'Bowers & Wilkins 803 D4 information sheet',
      'Information sheet: 803 D4 is a 3-way vented-box system with one 25 mm diamond dome '
      'tweeter, one 130 mm Continuum FST midrange and two 180 mm Aerofoil bass drivers (four '
      'drive units).',
      {R('bw-803-d4', 'driverCount', note='Sheet lists 1 tweeter + 1 midrange + 2 woofers = 4.')}),

    C('https://www.bowerswilkins.com/en-us/blog/products/history-of-800-series.html',
      'Bowers & Wilkins "History of 800 Series" article',
      'Article describes the original 801 as a three-driver, three-way system (one tweeter, one '
      'midrange and one woofer).',
      {R('legacy-bw-2', 'driverCount', note='Article describes a three-driver 801 system.')}),

    C('https://www.bowerswilkins.com/en-us/blog/products/history-of-nautilus.html',
      'Bowers & Wilkins "History of Nautilus" article',
      'Article describes Nautilus as a four-way system with four drive units (one each for bass, '
      'midbass, midrange and treble).',
      {R('legacy-bw-4', 'driverCount', note='Article describes the four-way Nautilus with four drive units.')}),
]


# ---------------------------------------------------------------------------
# Structural restorations: fields that were null with provenance UNSOURCED and
# for which an exact-model manufacturer page was opened in Round 22.
# Each entry states the explicit text that supports the value.
# ---------------------------------------------------------------------------
def S(record, field, value, source, evidence):
    return {'record': record, 'field': field, 'value': value, 'source': source,
            'sourceClass': 'MANUFACTURER', 'checkedDate': CHECKED_DATE, 'evidence': evidence}


STRUCTURAL = [
    S('klipsch-heresy', 'driverCount', 3,
      'https://assets.klipsch.com/product-specsheets/Heresy-Spec.pdf',
      'Heresy specification sheet: single 12 in woofer plus mid-frequency and high-frequency compression drivers (3 drive units).'),
    S('bw-805d3', 'driverCount', 2,
      'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_europe_shared/default/dw8b9f6335/archive-manuals/805-d3-info-sheet_0.pdf',
      '805 D3 information sheet, "Drive units": "1x ø25mm (1 in) diamond dome high-frequency" and "1x ø165mm (6.5 in) Continuum cone bass midrange".'),
    S('bowers-wilkins-705-s3', 'driverCount', 2,
      'https://www.bowerswilkins.com/product/loudspeakers/705-s3/300522.html',
      '705 S3 technical details, "Drive units": 1x ø25mm (1 in) Decoupled Carbon Dome high-frequency; 1x ø165mm (6.5 in) Continuum cone bass / midrange.'),
    S('bowers-wilkins-707-s3', 'driverCount', 2,
      'https://www.bowerswilkins.com/product/loudspeakers/707-s3/300525.html',
      '707 S3 technical details, "Drive units": 1x ø25mm (1 in) Decoupled Carbon Dome high-frequency; 1x ø130mm (5 in) Continuum cone bass / midrange.'),
    S('bw-805-d4', 'driverCount', 2,
      'https://www.bowerswilkins.com/en-us/product/loudspeakers/805-d4/150241-01-00-005.html',
      '805 D4 technical details, "Drive units": 1x ø25mm (1 in) Diamond dome high-frequency; 1x ø165mm (6.5 in) Continuum cone bass midrange.'),
    S('bowers-wilkins-805-d4-signature', 'driverCount', 2,
      'https://www.bowerswilkins.com/en/product/loudspeakers/805-d4-signature/FP43745P.html',
      '805 D4 Signature technical details, "Drive units": 1x ø25mm (1 in) Diamond Dome high-frequency; 1x ø165mm (6.5 in) Continuum cone bass/midrange.'),
    S('bowers-wilkins-801-d4', 'driverCount', 4,
      'https://www.bowerswilkins.com/product/loudspeakers/801-d4/150237-03-00-005.html',
      '801 D4 technical details, "Drive units": 1x ø25mm Diamond dome HF; 1x ø150mm Continuum cone FST midrange; 2x ø250mm Aerofoil cone bass units.'),
    S('bowers-wilkins-802-d4', 'driverCount', 4,
      'https://www.bowerswilkins.com/en-us/product/loudspeakers/802-d4/150238-03-00-005.html',
      '802 D4 technical details, "Drive units": 1x ø25mm Diamond dome HF; 1x ø150mm Continuum cone FST midrange; 2x ø200mm Aerofoil cone bass units.'),
    S('genelec-8341a', 'driverCount', 4,
      'https://www.genelec.com/8341a',
      'Genelec 8341A product page: two 170 mm woofers, one 90 mm midrange and one 19 mm tweeter (4 drive units).'),
    S('genelec-8341a', 'active', True,
      'https://www.genelec.com/8341a',
      'Genelec 8341A product page: active monitor with built-in Class D amplification.'),
    S('genelec-8331a', 'driverCount', 4,
      'https://www.genelec.com/8331a',
      'Genelec 8331A product page: two 130 mm woofers, one 90 mm midrange and one 19 mm tweeter (4 drive units).'),
    S('genelec-8351b', 'driverCount', 4,
      'https://www.genelec.com/8351b',
      'Genelec 8351B product page: two 218 mm woofers, one 130 mm midrange and one 25 mm tweeter (4 drive units).'),
    S('genelec-8351b', 'active', True,
      'https://www.genelec.com/8351b',
      'Genelec 8351B product page: active monitor with built-in Class D amplification.'),
    S('dynaudio-bm6a', 'driverCount', 2,
      'https://dynaudio.com/professional-audio/classic-bm-range/bm6a',
      'Dynaudio BM6A product page: 1 in soft-dome tweeter plus 6.9 in woofer (2 drive units).'),
    S('dynaudio-bm6a', 'active', True,
      'https://dynaudio.com/professional-audio/classic-bm-range/bm6a',
      'Dynaudio BM6A product page: active nearfield monitor with built-in amplifiers.'),
    S('adam-audio-a77x', 'driverCount', 3,
      'https://www.adam-audio.com/content/uploads/2016/11/adam-audio-product-sheet-a77x_en.pdf',
      'ADAM A77X product sheet: two 7 in woofers and one X-ART tweeter (3 drive units).'),
    S('adam-audio-a77x', 'active', True,
      'https://www.adam-audio.com/content/uploads/2016/11/adam-audio-product-sheet-a77x_en.pdf',
      'ADAM A77X product sheet: active monitor with built-in amplification.'),
    S('focal-twin6', 'driverCount', 3,
      'https://www.focal.com/products/twin6',
      'Focal Twin6 product page: two 6.5 in "W" woofers and one 1.5 in beryllium tweeter (3 drive units).'),
    S('focal-trio11-be', 'driverCount', 3,
      'https://www.focal.com/products/trio-11-be',
      'Focal Trio11 Be product page: 10 in woofer, 5 in midrange and 1 in beryllium tweeter (3 drive units).'),
    S('focal-trio11-be', 'active', True,
      'https://www.focal.com/products/trio-11-be',
      'Focal Trio11 Be product page: active monitor with built-in amplification.'),
    S('focal-alpha-50-evo', 'driverCount', 2,
      'https://www.focal.com/products/alpha-50-evo',
      'Focal Alpha 50 Evo product page: 1 in aluminium inverted dome tweeter and 5 in Slatefiber woofer (2 drive units).'),
    S('focal-alpha-50-evo', 'active', True,
      'https://www.focal.com/products/alpha-50-evo',
      'Focal Alpha 50 Evo product page: active monitor with built-in amplification.'),
    S('focal-shape-50', 'driverCount', 2,
      'https://www.focal.com/products/shape-50',
      'Focal Shape 50 product page: 1 in aluminium/magnesium inverted dome tweeter and 5 in Flax woofer (2 drive units).'),
    S('eV-etx15p', 'driverCount', 2,
      'https://products.electrovoice.com/binary/ETX-15P_EDS_en.pdf',
      'ETX-15P engineering data sheet: 15 in woofer and 1.25 in compression driver (2 drive units).'),
    S('eV-etx15p', 'active', True,
      'https://products.electrovoice.com/binary/ETX-15P_EDS_en.pdf',
      'ETX-15P engineering data sheet: powered loudspeaker with built-in 1500 W Class D amplifier.'),
    S('eV-elx200-18sp', 'driverCount', 1,
      'https://products.electrovoice.com/ap/en/elx200-18sp',
      'ELX200-18SP product page: single 18 in woofer.'),
    S('eV-elx200-18sp', 'active', True,
      'https://products.electrovoice.com/ap/en/elx200-18sp',
      'ELX200-18SP product page: powered subwoofer with built-in 1200 W Class D amplifier.'),
    S('electro-voice-ekx-12p', 'driverCount', 2,
      'https://products.electrovoice.com/emea/de/ekx-12p',
      'EKX-12P product page: 12 in woofer and 1.4 in titanium compression driver (2 drive units).'),
    S('electro-voice-ekx-12p', 'active', True,
      'https://products.electrovoice.com/emea/de/ekx-12p',
      'EKX-12P product page: powered loudspeaker with built-in 1500 W Class D amplifier.'),
    S('qsc-ks212c', 'driverCount', 2,
      'https://www.qscaudio.com/solutions-products/loudspeakers/portable/powered/subwoofers/ks-series/ks212c/',
      'QSC KS212C product page: dual 12 in (305 mm) woofers in a cardioid subwoofer (2 drive units).'),
    S('qsc-ks212c', 'active', True,
      'https://www.qscaudio.com/solutions-products/loudspeakers/portable/powered/subwoofers/ks-series/ks212c/',
      'QSC KS212C product page: powered subwoofer with a built-in 3600 W Class D amplifier.'),
    S('qsc-k8.2', 'driverCount', 2,
      'https://www.qscaudio.com/resource-files/productresources/spk/k.2/q_spk_k2_specs.pdf',
      'QSC K.2 specification sheet: K8.2 configuration "Multi-purpose, 2-way active loudspeaker" with a 203 mm LF cone and a 35.6 mm HF compression driver.'),
    S('qsc-k8.2', 'active', True,
      'https://www.qscaudio.com/resource-files/productresources/spk/k.2/q_spk_k2_specs.pdf',
      'QSC K.2 specification sheet: "2-way active loudspeaker" with a 2000 W power module.'),
    S('qsc-cp8', 'driverCount', 2,
      'https://www.qscaudio.com/products-solutions/loudspeakers/portable/powered/portable-pa/cp-series/cp8/',
      'QSC CP8 product page: 8 in woofer and 1.4 in compression driver (2 transducers).'),
    S('qsc-cp8', 'active', True,
      'https://www.qscaudio.com/products-solutions/loudspeakers/portable/powered/portable-pa/cp-series/cp8/',
      'QSC CP8 product page: powered loudspeaker with a built-in 1000 W Class D amplifier.'),
    S('qsc-cp12', 'driverCount', 2,
      'https://www.qscaudio.com/solutions-products/loudspeakers/portable/powered/portable-pa/cp-series/cp12/',
      'QSC CP12 product page: 12 in woofer and 1.4 in compression driver (2 transducers).'),
    S('qsc-cp12', 'active', True,
      'https://www.qscaudio.com/solutions-products/loudspeakers/portable/powered/portable-pa/cp-series/cp12/',
      'QSC CP12 product page: powered loudspeaker with a built-in 1000 W Class D amplifier.'),
    S('qsc-ks118', 'driverCount', 1,
      'https://www.qscaudio.com/products-solutions/loudspeakers/portable/powered/subwoofers/ks-series/ks118/',
      'QSC KS118 product page: single 18 in (457 mm) direct-radiating subwoofer driver.'),
    S('qsc-ks118', 'active', True,
      'https://www.qscaudio.com/products-solutions/loudspeakers/portable/powered/subwoofers/ks-series/ks118/',
      'QSC KS118 product page: powered subwoofer with a built-in 3600 W Class D amplifier.'),
    S('qsc-kw122', 'driverCount', 2,
      'https://www.qscaudio.com/resource-files/productresources/spk/kw/q_spk_kw_usermanual.pdf',
      'QSC KW user manual specification table: KW122 configuration "12\\" 2-way multipurpose loudspeaker" with a 12 in LF cone and a 1.75 in HF compression driver.'),
    S('qsc-kw122', 'active', True,
      'https://www.qscaudio.com/resource-files/productresources/spk/kw/q_spk_kw_usermanual.pdf',
      'QSC KW user manual specification table: 1000 W Class D amplifier built into the enclosure.'),
    S('qsc-kw153', 'driverCount', 3,
      'https://www.qscaudio.com/resource-files/productresources/spk/kw/q_spk_kw_usermanual.pdf',
      'QSC KW user manual specification table: KW153 configuration "15\\" 3-way trapezoidal loudspeaker" with a 15 in LF cone, a 6.5 in midrange cone and a 1.75 in HF compression driver.'),
    S('qsc-kw153', 'active', True,
      'https://www.qscaudio.com/resource-files/productresources/spk/kw/q_spk_kw_usermanual.pdf',
      'QSC KW user manual specification table: 1000 W Class D amplifier built into the enclosure.'),
    S('qsc-e112', 'driverCount', 2,
      'https://www.qscaudio.com/resource-files/productresources/spk/e/e112/q_spk_e_112_specs.pdf',
      'QSC E112 specification sheet: 12 in woofer and 1.4 in compression driver (2 transducers).'),
    S('qsc-e112', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/e/e112/q_spk_e_112_specs.pdf',
      'QSC E112 specification sheet describes a passive loudspeaker for use with an external amplifier.'),
    S('qsc-ad-c6t', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/ad/ad-c6t/q_spk_adc_6t_specsheet.pdf',
      'QSC AD-C6T specification sheet: passive 70/100 V ceiling loudspeaker for external amplification.'),
    S('qsc-ac-c4t', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/ac/ac-c_4t/q_spk_acc_4t_specs.pdf',
      'QSC AC-C4T specification sheet: passive 70/100 V ceiling loudspeaker for external amplification.'),
    S('qsc-ac-c6t', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/ac/ac-c_6t/q_spk_acc_6t_specs.pdf',
      'QSC AC-C6T specification sheet: passive 70/100 V ceiling loudspeaker for external amplification.'),
    S('qsc-ac-c8t', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/ac/ac-c_8t/q_spk_acc_8t_specs.pdf',
      'QSC AC-C8T specification sheet: passive 70/100 V ceiling loudspeaker for external amplification.'),
    S('qsc-wl3082', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/wideline_8/q_spk_wl8_specs.pdf',
      'QSC WideLine-8 specification sheet: passive line-array element requiring external amplification.'),
    S('qsc-wl212-sw', 'active', False,
      'https://www.qscaudio.com/resource-files/productresources/spk/wideline_8/q_spk_wl8_specs.pdf',
      'QSC WideLine-8 specification sheet: passive subwoofer element requiring external amplification.'),
    S('kef-ls60-wireless', 'driverCount', 6,
      'https://assets.kef.com/product-support/ls60-wireless/LS60_Wireless_Info_sheet_EN.pdf',
      'LS60 Wireless information sheet: per speaker, four 135 mm LF drivers plus a 100 mm MF driver and a 19 mm HF driver = 6 drive units.'),
    S('kef-ls60-wireless', 'active', True,
      'https://assets.kef.com/product-support/ls60-wireless/LS60_Wireless_Info_sheet_EN.pdf',
      'LS60 Wireless information sheet: built-in amplification (LF 500 W, MF 100 W, HF 100 W per speaker).'),
    S('klipsch-r51m', 'driverCount', 2,
      'https://assets.klipsch.com/product-specsheets/R-51M_Spec-Sheet_v01.pdf',
      'R-51M specification sheet: one 5.25 in IMG woofer and one 1 in aluminium dome tweeter (2 drive units).'),
]
