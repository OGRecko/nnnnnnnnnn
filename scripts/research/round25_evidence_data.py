"""Round 25 evidence table.

Every check below was performed by opening the listed URL during Round 25
(2026-10-19) and reading the model-specific specification text. Outcomes:
  PROMOTED / SUPPORTED_NOT_PROMOTED / NOT_STATED / NOT_EXTRACTED / INACCESSIBLE / CONFLICT

Promotion rules applied here (unchanged from Rounds 22-24):
  * a field is PROMOTED only when the opened document states it explicitly for the
    exact model named by the catalogue record, and the host is the manufacturer's
    own site (or an owner-approved distributor/aggregator copy of the manufacturer
    manual, per Owner Decision 1 of 2026-10-12);
  * `active` is never inferred from a recommended-amplifier-power range or a
    cabinet power-handling figure alone: the document must say powered/active,
    show a built-in amplifier, say passive/unpowered, or mark the built-in
    amplifier row "N/A"/state a passive crossover. Otherwise the outcome is
    NOT_STATED;
  * third-party review sites, enthusiast databases and museum catalogues can
    support a value but never promote it: SUPPORTED_NOT_PROMOTED.

Values are filled from the live catalogue at build time, never hard-coded here.
"""
CHECKED_DATE = '2026-10-19'

NOT_STATED_NOTE = ('The opened document gives no explicit passive/active, powered/unpowered '
                   'or built-in-amplifier wording for this model (only enclosure power '
                   'handling, impedance or a recommended amplifier-power range), so `active` '
                   'stays `unverified`.')

THIRD_PARTY_NOTE = ('The document reproduces the model\'s drive-unit complement, but it is '
                    'served from a host that cannot be established as a manufacturer origin, '
                    'so the field is recorded as supported and not promoted.')


def C(url, document, evidence, results, status='CHECKED', total=None, chunks=(0,),
      source_class='MANUFACTURER', owner_decision=None):
    entry = {
        'url': url,
        'document': document,
        'chunksOpened': list(chunks),
        'chunksTotal': total,
        'status': status,
        'evidence': evidence,
        'results': results,
        'sourceClass': source_class,
    }
    if owner_decision:
        entry['ownerDecision'] = owner_decision
    return entry


def R(record, field, outcome='PROMOTED', note=None):
    # Hashable 3-tuple so the literals below stay compact; the builder turns them
    # into ordered dicts deterministically.
    return (record + '.' + field, outcome, note)


DISTRIBUTOR = 'DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL'
OWNER_DECISION = 'owner-decision-1-2026-10-12-distributor-copies-yes'

CHECKS = [
    # ---------------------------------------------------------------- manufacturer
    C('https://global.jbl.com/DD67000RW-.html',
      'JBL Project Everest DD67000 product page (specifications)',
      'PDP specification copy: "three-way speaker features dual 15-inch (380mm) ... woofers, a 4-inch (100mm) pure beryllium compression driver and a 1-inch (25mm) pure-beryllium ultra high-frequency driver"; "Recommended Amplifier Power 500 watts"; 96 dB sensitivity; 8 ohms. No passive/active or built-in-amplifier wording.',
      {
          R('jbl-everest-dd67000', 'driverCount',
            'PROMOTED', 'Specification copy names two 15-inch woofers, one 4-inch beryllium compression driver and one 1-inch beryllium UHF driver: 4 transducers.'),
          R('jbl-everest-dd67000', 'active',
            'NOT_STATED', 'Only "Recommended Amplifier Power 500 watts" is given; the page never says passive, powered or built-in amplifier.'),
      }, total=1),
    C('https://global.jbl.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw168a89f9/pdfs/JBL%20Project%20K2%209900%20Data%20Sheet.pdf',
      'JBL Project K2 S9900 data sheet (PDF)',
      'Data-sheet driver list: "Low-Frequency Driver: 15" (380mm) Pulp-cone woofer (1500AL-1)"; "High-Frequency Driver: 4" (100mm) Magnesium compression driver (476Mg)"; "Ultrahigh-Frequency Driver: 1" (25mm) Magnesium compression driver (045Be-1)"; "Maximum Recommended Amplifier Power: 500 Watts"; "LF/HF Drive Mode Switch: Normal, bi amp"; 93 dB.',
      {
          R('jbl-k2-s9900', 'driverCount',
            'PROMOTED', 'Data sheet lists a 15-inch woofer, a 4-inch compression driver and a 1-inch UHF compression driver: 3 transducers.'),
          R('jbl-k2-s9900', 'active',
            'NOT_STATED', 'Only "Maximum Recommended Amplifier Power" and a bi-amp switch are given; no passive/active or built-in-amplifier statement.'),
      }, total=1),
    C('https://jp.jbl.com/jamaica.html',
      'jp.jbl.com "jamaica" page (opened expecting JBL Paragon material)',
      'The page is a Jamaica jazz-bar/shop profile with no JBL Paragon specification text at all; it does not mention the Paragon driver complement.',
      {
          R('jbl-paragon', 'driverCount', 'INACCESSIBLE',
            'The recorded URL is not a Paragon specification page; no model-specific drive-unit text exists there. The stored value of 6 remains unverified.'),
      }, status='INACCESSIBLE', total=1),
    C('https://martin-audio.com/products/loudspeakers/mla',
      'Martin Audio MLA product page (specifications)',
      'PDP: "TYPE Three-way cellular drive, active array element"; LF "2 x 12\\" (300mm)/3\\" voice coil ... Hybrid bass horn loaded"; MF "2 x 6.5\\" (165mm)/2\\" coil"; HF "3 x 1\\" (25mm) exit neodymium magnet compression drivers"; "Six channel Class D ... 6000W peak"; architectural description "self-powered, vertically-arrayable three-way system".',
      {
          R('legacy-ma-4', 'driverCount',
            'PROMOTED', 'LF 2 + MF 2 + HF 3 = 7 transducers, each listed explicitly for the MLA.'),
          R('legacy-ma-4', 'active',
            'PROMOTED', 'Page states "active array element", "Six channel Class D" amplification and "self-powered".'),
      }, total=1),
    C('https://products.bose.com/pdf/customer_service/owners/251_guide.pdf',
      'Bose 251 environmental speakers owner\'s guide (Technical Information)',
      'Owner\'s guide technical information: "Two (2) 2½\\" environmental Twiddler™ drivers per speaker"; "One (1) 5¼\\" environmental woofer per speaker"; "Compatible with amplifiers or receivers rated 10-200 watts".',
      {
          R('legacy-bose-7', 'driverCount',
            'PROMOTED', 'Two Twiddler drivers plus one 5¼-inch woofer per speaker = 3 transducers.'),
          R('legacy-bose-7', 'active',
            'NOT_STATED', 'The guide only gives amplifier/receiver compatibility (10-200 W); it never calls the speaker passive or shows a built-in amplifier.'),
      }, total=2, chunks=(1, 2)),
    C('https://magnepan.com/pages/manual-controller',
      'Magnepan 1.7 owner\'s manual',
      'Manual text: "The 1.7 is a 3-way, full-range, quasi-ribbon design with a quasi-ribbon bass/midrange, tweeter, and super-tweeter." No amplifier or passive/active wording in the opened manual.',
      {
          R('magnepan-mg1.7', 'driverCount',
            'PROMOTED', 'Manual names a quasi-ribbon bass/midrange, a tweeter and a super-tweeter in a 3-way design: 3 transducers.'),
          R('magnepan-mg1.7', 'active',
            'NOT_STATED', 'Manual describes the 3-way quasi-ribbon design but never states passive/active or a built-in amplifier.'),
      }, total=1),
    C('https://us.sennheiser-hearing.com/products/ambeo-soundbar-mini',
      'Sennheiser AMBEO Soundbar Mini product page (Specifications)',
      'Specification table: "Total number of speakers 6"; "Fullrange 4x 1.6\\" (40mm) Cellulose Cone Fullrange Driver"; "Woofers 2x 4\\" Cellulose Cone Driver"; "Amplifier 6x class D amplifiers"; "Total amplification power 250W (RMS)".',
      {
          R('sennheiser-ambeo-mini', 'driverCount',
            'PROMOTED', 'Specification table states "Total number of speakers 6" (4 full-range + 2 woofers).'),
          R('sennheiser-ambeo-mini', 'active',
            'PROMOTED', 'Table lists "6x class D amplifiers" and 250 W total amplification built into the soundbar.'),
      }, total=5, chunks=(3,)),
    C('https://us.sennheiser-hearing.com/products/ambeo-soundbar-plus',
      'Sennheiser AMBEO Soundbar Plus product page (Specifications)',
      'Specification table: "Total number of speakers 9"; "Full range 7x 2\\" Aluminum Cone Fullrange Driver"; "Woofers 2x 4\\" Cellulose Cone Driver"; "Amplifier 9x class D amplifiers"; "Total audio power 400W (RMS)".',
      {
          R('sennheiser-ambeo-soundbar-plus', 'driverCount',
            'PROMOTED', 'Specification table states "Total number of speakers 9" (7 full-range + 2 woofers).'),
          R('sennheiser-ambeo-soundbar-plus', 'active',
            'PROMOTED', 'Table lists "9x class D amplifiers" and 400 W total audio power built into the soundbar.'),
      }, total=5, chunks=(3,)),
    C('https://www.fender.com/products/blues-junior-iv',
      'Fender Blues Junior IV product page (specifications)',
      'PDP specification block: "Speakers: One - 12\\" Celestion® A-Type"; "Total Impedance 8 ohms"; "Amplifier Type Tube"; "Output Power / Output 15 Watts"; tube complement "2 x EL84 / 3 x 12AX7".',
      {
          R('fender-blues-junior-iv', 'driverCount',
            'PROMOTED', 'PDP states "Speakers: One - 12\\" Celestion A-Type": 1 transducer.'),
          R('fender-blues-junior-iv', 'active',
            'PROMOTED', 'PDP states "Amplifier Type Tube" and "15 Watts" output for this combo, i.e. the amplifier is built into the cabinet.'),
      }, total=2, chunks=(0, 1)),
    C('https://www.qscaudio.com/news/news/detail/qsc-expands-e-series-lineup-with-two-new-models/',
      'QSC news release: E Series expands with two new models',
      'News release: "E218SW dual 18-inch subwoofer ... features two 18-inch die-cast frame woofers with 4-inch voice coils"; the release groups both new models under the E Series "passive loudspeakers" heading, and no built-in amplifier is described.',
      {
          R('qsc-e218sw', 'driverCount',
            'PROMOTED', 'Release states the E218SW "features two 18-inch die-cast frame woofers": 2 transducers.'),
          R('qsc-e218sw', 'active',
            'PROMOTED', 'The E218SW is announced within the E Series "passive loudspeakers" range and no amplifier is described.'),
      }, total=1),
    C('https://www.kenwood.com/usa/car/excelon/kfc-xp6903c/',
      'Kenwood Excelon KFC-XP6903C product page',
      'PDP component list: "Shallow 6x9\\" PP Cone Woofer"; "3-1/2\\" 2way Mid-High Speaker"; "Silk Balanced-dome Tweeter Size 25mm / 1 inch"; power handling 300 W peak / 100 W RMS (amplifier power, no built-in amplifier).',
      {
          R('kenwood-excelon-kfc-xp6903c', 'driverCount',
            'PROMOTED', 'The set comprises a 6x9-inch woofer, a 3-1/2-inch mid-high speaker and a 25 mm tweeter: 3 transducers.'),
      }, total=2, chunks=(0, 1)),
    C('https://data.yamaha.com/files/download/other_assets/3/325553/dxr-dxs_en_om_c0.pdf',
      'Yamaha DXR/DXS series owner\'s manual (Specifications)',
      'Owner\'s manual specification tables: DXS12 "System Type: Powered Subwoofer, Band-pass Type"; LF "Diameter 12\\" Cone", HF "-"; "Amplifier Type Class-D"; power rating 950 W dynamic / 600 W continuous; frequency range 47 Hz-160 Hz (-10 dB); 131 dB peak. DXR12 is the 12-inch two-way powered speaker with a 1.4-inch diaphragm / 1-inch throat compression driver.',
      {
          R('yamaha-dxs12', 'driverCount',
            'PROMOTED', 'DXS12 spec row lists one 12-inch cone LF driver and no HF device: 1 transducer.'),
          R('yamaha-dxs12', 'active',
            'PROMOTED', 'Specification table calls the DXS12 a "Powered Subwoofer" with a built-in Class-D amplifier (950 W dynamic / 600 W continuous).'),
      }, total=9, chunks=(4,)),
    C('https://www.lg.com/africa/audio/lg-sc9s',
      'LG SC9S soundbar product page (specifications)',
      'PDP specification block: "Number of Speakers 9 EA"; 3.1.3 channels; 400 W output. The page gives no amplifier-device count or passive/active wording.',
      {
          R('lg-lg-sc9s', 'driverCount',
            'PROMOTED', 'LG specification row states "Number of Speakers 9 EA".'),
          R('lg-lg-sc9s', 'active',
            'NOT_STATED', 'The specification lists output power and speaker count only; it never states built-in amplification or a passive design.'),
      }, total=6, chunks=(4, 5)),
    C('https://www.lg.com/pt/audio/soundbars/s80tr/',
      'LG S80TR soundbar product page (specifications)',
      'PDP specification block: "Número de Colunas 11 EA"; 5.1.3 channels; 580 W output. No amplifier-device count or passive/active wording.',
      {
          R('lg-lg-s80tr', 'driverCount',
            'PROMOTED', 'LG specification row states "Número de Colunas 11 EA" (number of speakers).'),
          R('lg-lg-s80tr', 'active',
            'NOT_STATED', 'The specification lists output power and speaker count only; it never states built-in amplification or a passive design.'),
      }, total=5, chunks=(4,)),
    C('https://www.lg.com/ca_en/speakers/soundbars/s90tr/',
      'LG S90TR soundbar product page (All Spec)',
      'PDP "All Spec" panel: "Number of Speakers 13 EA"; "Number of Channels 7.1.3"; "Output Power 670 W". No amplifier-device count or passive/active wording.',
      {
          R('lg-lg-s90tr', 'driverCount',
            'PROMOTED', 'LG "All Spec" row states "Number of Speakers 13 EA".'),
          R('lg-lg-s90tr', 'active',
            'NOT_STATED', 'The specification lists output power and speaker count only; it never states built-in amplification or a passive design.'),
      }, total=7, chunks=(4, 5)),
    C('https://www.dbaudio.com/assets/products/downloads/manuals-documentation/t-series/dbaudio-datasheet-t10-1.1-en.pdf',
      'd&b audiotechnik T10 data sheet',
      'Data sheet text: "The T10 is a two way design, employing dual 6.5\\" drivers, a 1.4\\" exit compression driver and a passive crossover network."',
      {
          R('dandb-t10', 'driverCount',
            'PROMOTED', 'Data sheet names dual 6.5-inch drivers plus a 1.4-inch exit compression driver: 3 transducers.'),
          R('dandb-t10', 'active',
            'PROMOTED', 'Data sheet states the T10 uses a "passive crossover network" and describes no built-in amplifier.'),
      }, total=1),
    C('https://www.dasaudio.com/wp-content/uploads/2011/11/TECNOLOGIAS_AERO_12A_V1.pdf',
      'DAS Audio Aero 12A technical report (Spanish)',
      'Technical report: "el Aero 12A incorpora un nuevo altavoz de graves de 12\\", el 12LNC4"; "El nuevo motor de compresión, M-75N"; "El amplificador de 600 W de potencia" for the self-powered Aero 12A array element.',
      {
          R('das-audio-aero-12a', 'driverCount',
            'PROMOTED', 'Report names a 12-inch 12LNC4 woofer and an M-75N compression driver: 2 transducers.'),
          R('das-audio-aero-12a', 'active',
            'PROMOTED', 'Report describes the Aero 12A as incorporating its own 600 W amplifier.'),
      }, total=1),
    C('https://legacy.adamson.ai/support/downloads-directory/e-series/e15/1-e15-technicaldata/file',
      'Adamson E15 technical data sheet (legacy archive)',
      'Technical data: "Components LF 2x ND15-L 15\\" Kevlar Neodymium Driver"; "Components MF 2x YX7 7\\""; "Components HF 2x NH4TA2 4\\" Diaphragm / 1.5\\" Exit Compression Driver"; "3 way, true line source enclosure".',
      {
          R('adamson-e15', 'driverCount',
            'PROMOTED', '2 LF + 2 MF + 2 HF devices listed = 6 transducers.'),
          R('adamson-e15', 'active',
            'NOT_STATED', 'The technical data lists the drive units and "3 way" design but no built-in amplifier or passive/active statement.'),
      }, total=1),
    C('https://rockfordfosgate.com/products/details/t1650-s/',
      'Rockford Fosgate T1650-S Power 6.50" 2-Way Euro Fit Component System page',
      'PDP description: "The Power T1650-S is a T1 component system with a separate tweeter and a true 6.5\\" midrange"; page title "Power 6.50\\" 2-Way Euro Fit Component System"; sold in pairs.',
      {
          R('rockford-fosgate-t1650-s', 'driverCount',
            'PROMOTED', 'A 2-way component system with a separate tweeter and one 6.5-inch midrange = 2 transducers per system.'),
      }, total=3),
    C('https://voxamps.com/wp-content/uploads/support/AC15_30HW_V212HWX_OM_EFGS2.pdf',
      'VOX AC30HW2X/AC30HW2/AC15HW1X/AC15HW1/AC30HWH/V212HWX owner\'s manual (Specification)',
      'Manual specification section: "V212HWX: ... Speakers 2 x 12\\" 8 Ohm Celestion Alnico Blue / 30 Watts RMS into 16 Ohms".',
      {
          R('vox-v212hwx', 'driverCount',
            'PROMOTED', 'V212HWX speaker specification line reads "2 x 12\\" 8 Ohm Celestion Alnico Blue": 2 transducers.'),
      }, total=10, chunks=(1, 2)),
    C('https://www.qacoustics.com/products/5020-bookshelf-speaker',
      'Q Acoustics 5020 bookshelf speaker product page (specifications)',
      'PDP specification block: "Bass unit: 1 × 125 mm (5.0 in.)"; "Treble unit: 1 × 25 mm (1.0 in.)"; 25-100 W recommended amplifier power; 6 Ω; 87.9 dB.',
      {
          R('q-acoustics-5020', 'driverCount',
            'PROMOTED', 'Specification lists one 125 mm bass unit and one 25 mm treble unit: 2 transducers.'),
      }, total=4, chunks=(1, 2)),
    C('https://www.fmicassets.com/Damroot/Original/10001/OM_2777500107_Eris-E5_Tech-Sheet_EN.pdf',
      'PreSonus Eris E5 studio monitor tech sheet (PDF)',
      'Tech sheet: "ERIS E5 — 2-Way Active Studio Monitors"; "5.25-inch woven composite low-frequency transducer"; "1-inch (25 mm) ... high-frequency transducer"; "80 watt, Class AB biamplification"; technical table "LF Amplifier Power 45W Class AB", "HF Amplifier Power 35W Class AB".',
      {
          R('presonus-eris-e5', 'driverCount',
            'PROMOTED', 'Tech sheet lists a 5.25-inch LF transducer and a 1-inch HF transducer: 2 transducers.'),
          R('presonus-eris-e5', 'active',
            'PROMOTED', 'Tech sheet heads the model "2-Way Active Studio Monitors" and gives 45 W LF / 35 W HF Class AB amplifier power.'),
      }, total=1),
    C('https://www.sonos.com/en-us/guides/move',
      'Sonos Move user guide (Specifications)',
      'Guide specification table: "Amplifier: Two Class-D digital amplifiers."; "Tweeter: One tweeter..."; "Mid-woofer: One mid-woofer...".',
      {
          R('legacy-sonos-5', 'driverCount',
            'PROMOTED', 'Specification lists one tweeter and one mid-woofer: 2 transducers.'),
          R('legacy-sonos-5', 'active',
            'PROMOTED', 'Specification lists "Two Class-D digital amplifiers" built into the speaker.'),
      }, total=3, chunks=(1,)),
    C('https://www.alpine-usa.com/company/press/2018/new-s-series-speakers-subwoofers-and-tough-power-pack-amplifiers-from-alpine-electronics',
      'Alpine Electronics press release, 8 January 2018 (S-Series / R-Series speakers)',
      'Press release product list: "S-S65 6.5-inch Coaxial 2-Way Speaker ... 1-inch Silk Tweeter"; "R-S65C 6.5-inch Component 2-Way Speakers ... 1-inch Silk Tweeter"; "S-S65C 6.5-inch Component 2-Way Speaker ... 1-inch Silk Tweeter" (S-S65C is an S-Series component set, not the S-S65 coaxial).',
      {
          R('alpine-s-s65', 'driverCount',
            'PROMOTED', 'S-S65 is listed as a "6.5-inch Coaxial 2-Way Speaker" with a 1-inch silk tweeter: 2 transducers.'),
          R('alpine-r-s65c', 'driverCount',
            'PROMOTED', 'R-S65C is listed as a "6.5-inch Component 2-Way Speakers" set with a 1-inch silk tweeter: 2 transducers.'),
      }, total=3, chunks=(0,)),
    C('https://www.alpine-usa.com/company/press/2017/alpine-electronics-now-shipping-x-series-speakers',
      'Alpine Electronics press release, 7 May 2017 (X-Series speakers)',
      'Press release: "the X-S65C 6.5-inch Component 2-Way Speakers"; "1-inch Carbon Graphite Tweeter"; the set pairs one 6.5-inch woofer with one tweeter.',
      {
          R('alpine-x-s65c', 'driverCount',
            'PROMOTED', 'X-S65C is described as a 6.5-inch component 2-way speaker set with a 1-inch carbon-graphite tweeter: 2 transducers.'),
      }, total=1),
    C('https://www.morelhifi.com/en/products/car-audio/reference-9/elate-carbon-16/elate-carbon-62-6-2-way-158',
      'Morel Elate Carbon 2-Way product page (specifications table)',
      'Specification table: "Elate Carbon 62 | 6½\\" 2-way | 180 / 1000 | 87 | 30-25000 | MXT280C"; "Elate Carbon 62A | 6½\\" 2-way Active".',
      {
          R('morel-elate-carbon-62a', 'driverCount',
            'PROMOTED', 'The Elate Carbon 62A is a 6½-inch 2-way system: 2 transducers (woofer plus tweeter).'),
      }, total=4),
    # ---------------------------------------------------------------- distributor manual
    C('https://www.manualslib.com/manual/1412330/Kef-Blade.html?page=10',
      'KEF Blade owner\'s manual, page 10 "Specifications" (aggregator copy)',
      'Specification table: "Design Three-way bass reflex"; "MF: 125mm (5in.) Li-Mg-Al/LCP hybrid cone"; "HF: 25mm (1in.) Al dome"; "Bass units: LF: 4 x 225mm (9in.) with force cancelling"; "Amplifier requirements 50 - 400W". Page 8 (amplifier requirements) never uses the word passive.',
      {
          R('legacy-kef-7', 'driverCount',
            'PROMOTED', 'Specification names one 125 mm MF unit, one 25 mm HF unit and four 225 mm bass units: 6 transducers.'),
          R('legacy-kef-7', 'active',
            'NOT_STATED', 'The manual gives "Amplifier requirements 50 - 400W" but never says passive/unpowered or shows a built-in amplifier.'),
      }, total=13, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.manualslib.com/manual/286175/Kef-Q100.html?page=12',
      'KEF Q Series brochure & specs, page 12 (aggregator copy)',
      'Specification table, Q100 column: "Two-way bass reflex"; "130mm (5.25in.) aluminium Uni-Q"; "25mm (1in.) vented aluminium dome HF"; "Amplifier N/A"; "Amplifier requirements 10 - 100W"; 86 dB; 8Ω.',
      {
          R('legacy-kef-5', 'driverCount',
            'PROMOTED', 'Q100 column lists a 130 mm aluminium Uni-Q unit and a 25 mm vented dome HF unit: 2 transducers.'),
          R('legacy-kef-5', 'active',
            'PROMOTED', 'The Q100 column marks "Amplifier N/A" and gives a separate "Amplifier requirements 10 - 100W" figure, i.e. no built-in amplifier.'),
      }, total=13, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.manualslib.com/manual/79243/Jbl-Vrx932la.html?page=4',
      'JBL VRX932LA user guide, page 4 "Specifications" (aggregator copy)',
      'Specifications: "12\\" two-way, line array loudspeaker system"; "LF Driver: 1 x JBL 2262H 305 mm (12 in) Differential Drive woofer"; "HF Driver: 3 x JBL 2407J, 25.4 mm (1 in) voice-coil ... compression driver"; "Crossover Modes: Bi-amp / passive, externally switchable"; "Power Rating ... Passive: 800 W".',
      {
          R('jbl-vrx932', 'driverCount',
            'PROMOTED', 'One 12-inch 2262H LF driver plus three 2407J HF compression drivers = 4 transducers.'),
          R('jbl-vrx932', 'active',
            'PROMOTED', 'Specifications give a "passive" crossover mode and "Passive" power rating; the cabinet is driven by external amplifiers.'),
      }, total=13, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.manualslib.com/manual/293781/Mackie-Hr624.html',
      'Mackie HR624 specifications sheet (aggregator copy)',
      'Specification sheet: "The HR624 studio monitors are high-resolution, two-way, bi-amplified, active monitors"; "a 1-inch aluminum-alloy high-frequency transducer, a high-precision 6.7-inch die-cast magnesium frame low-frequency transducer, and a 6-inch x 9-inch elliptical flat piston passive radiator"; "The low-frequency amplifier is rated at 100 watts rms ... the high-frequency amplifier is rated at 40 watts rms".',
      {
          R('legacy-mack-2', 'driverCount',
            'PROMOTED', 'One 1-inch HF transducer plus one 6.7-inch LF transducer = 2 transducers; the passive radiator is not a driven transducer.'),
          R('legacy-mack-2', 'active',
            'PROMOTED', 'Sheet calls the HR624 "bi-amplified, active monitors" and gives built-in 100 W LF / 40 W HF amplifiers.'),
      }, total=2, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.manualslib.com/manual/759581/Db-Technologies-Opera-Live.html?page=6',
      'dB Technologies Opera Live user manual, page 6 "Technical Specification" (aggregator copy)',
      'The technical table covers Opera Live 202, 205 and 402 only ("1 woofer 12\\" ... 1 driver 1\\"", "bi-amp", built-in amplifiers); the document contains no Opera 405 column.',
      {
          R('dbtechnologies-opera-405', 'driverCount', 'NOT_EXTRACTED',
            'Opened page is the Opera Live 202/205/402 specification table; it has no Opera 405 column, so no value is asserted for this record.'),
          R('dbtechnologies-opera-405', 'active', 'NOT_EXTRACTED',
            'Opened page is the Opera Live 202/205/402 specification table; it has no Opera 405 column.'),
      }, total=14, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.manualslib.com/manual/1290952/Sonus-Faber-Serafino-Tradition.html?page=29#manual',
      'Sonus Faber Homage Tradition owner\'s manual, page 29 "Technical Specifications" (aggregator copy)',
      'Header: "Homage tradition passive loudspeakers". AMATI column: "3.5 way floorstanding loudspeaker system"; "H28 XTR-04 Sonus faber silk dome 28 mm"; "M15 XTR-04 ... 150 mm ... midrange"; "2 x W22XTR-08 Sonus faber designed 220 mm ... woofers"; 4 Ω; "100 – 500 W".',
      {
          R('sonus-faber-homage-tradition-amati', 'driverCount',
            'PROMOTED', 'AMATI column lists one 28 mm tweeter, one 150 mm midrange and two 220 mm woofers: 4 transducers.'),
          R('sonus-faber-homage-tradition-amati', 'active',
            'PROMOTED', 'The manual is headed "Homage tradition passive loudspeakers"; only a suggested amplifier power is given.'),
      }, total=46, chunks=(0, 1), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    # ---------------------------------------------------------------- partial / nav-only manufacturer pages
    C('https://international.kef.com/products/q150-bookshelf-speaker',
      'KEF Q150 bookshelf speaker product page',
      'Only the opening navigation/hero chunk could be read during this round; it contains no drive-unit count or amplifier statement.',
      {
          R('kef-q150', 'active', 'NOT_EXTRACTED',
            'The opened chunk is navigation/marketing copy without the specification table; the field remains unresolved.'),
      }, total=4, chunks=(0,)),
    C('https://international.kef.com/products/q350-bookshelf-speaker',
      'KEF Q350 bookshelf speaker product page',
      'Only the opening navigation/hero chunk could be read during this round; it contains no drive-unit count or amplifier statement.',
      {
          R('kef-q350', 'active', 'NOT_EXTRACTED',
            'The opened chunk is navigation/marketing copy without the specification table; the field remains unresolved.'),
      }, total=4, chunks=(0,)),
    C('https://international.kef.com/products/r11-meta',
      'KEF R11 Meta floorstanding speaker product page',
      'PDP specification block: "DESIGN Three-way bass reflex"; HF "25 mm (1 in.) vented aluminium dome with MAT"; MF "125 mm (5 in.) aluminium cone"; "LF: 4 x 165 mm (6.5 in.) hybrid aluminium cone"; crossover 330 Hz / 2.5 kHz; "AMPLIFIER REQUIREMENTS 15 - 300W"; 4 Ω; 90 dB.',
      {
          R('kef-r11-meta', 'active',
            'NOT_STATED', 'The page gives "AMPLIFIER REQUIREMENTS 15 - 300W" but never states passive/active or a built-in amplifier.'),
      }, total=6, chunks=(0,)),
    C('https://jblpro.com/en-US/site_elements/4311-information',
      'JBL 4311 information page (JBL Professional)',
      'Page specification text: "Components: 300-mm (12-in) LF loudspeaker; 130-mm (5-in) midrange; 36-mm (1.4-in) HF direct radiator"; 75 W continuous program; 8 Ω; 45 Hz-15 kHz ±3 dB.',
      {
          R('jbl-4311', 'active',
            'NOT_STATED', 'The page lists components and power handling but never states passive/active or a built-in amplifier.'),
      }, total=1),
    C('https://jblpro.com/en-US/site_elements/4412-information',
      'JBL 4412 information page (JBL Professional)',
      'Page specification text: "Transducer Complement: 300 mm (12 in) LF, 125 mm (5 in) midrange, 25 mm (1 in) HF"; 150 W pink noise; 8 ohms; 90 dB.',
      {
          R('jbl-4412', 'active',
            'NOT_STATED', 'The page lists the transducer complement but never states passive/active or a built-in amplifier.'),
      }, total=1),
    C('https://dali-speakers.com/en-us/products/oberon/oberon-1/',
      'DALI Oberon 1 product page (recorded URL)',
      'The URL returns the DALI "Page not found" template; no Oberon 1 specification content is served at this address.',
      {
          R('dali-oberon-1', 'driverCount', 'INACCESSIBLE',
            'Recorded URL returns a 404 page-not-found template; the stored value stays unverified.'),
          R('dali-oberon-1', 'active', 'INACCESSIBLE',
            'Recorded URL returns a 404 page-not-found template; no amplifier statement is available.'),
      }, status='INACCESSIBLE', total=1),
    # ---------------------------------------------------------------- third-party reviews / databases
    C('https://www.stereophile.com/content/kef-reference-5-loudspeaker-specifications',
      'Stereophile KEF Reference 5 loudspeaker specifications',
      'Specifications sidebar: "Three-way, reflex-loaded, floorstanding loudspeaker. Drive-units: Uni-Q driver array with 1\\" (25mm) vented aluminum-dome tweeter, 5\\" (125mm) aluminum-cone midrange unit, four 6.5\\" (165mm) aluminum-cone woofers"; 90 dB/2.83V/m; 8 ohms; 50-400 W recommended.',
      {
          R('kef-reference-5', 'driverCount',
            'SUPPORTED_NOT_PROMOTED', 'One tweeter, one midrange and four woofers are listed (6 transducers), but the page is a third-party review.'),
          R('kef-reference-5', 'active', 'NOT_STATED',
            'The sidebar gives recommended amplifier power only; no passive/active statement.'),
      }, total=2, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.stereophile.com/content/snell-type-loudspeaker-specifications',
      'Stereophile Snell Type A loudspeaker specifications',
      'Specifications sidebar: "Drive-units: 10\\" cone-woofer, 4\\" midrange, 1\\" soft-dome tweeter, rear-firing supertweeter (A/III)"; 86 dB/W/m; 4 ohms; three-way acoustic-suspension.',
      {
          R('snell-typeAIII', 'driverCount',
            'SUPPORTED_NOT_PROMOTED', 'Woofer, midrange, tweeter and rear-firing supertweeter = 4 transducers; third-party review page.'),
          R('snell-typeAIII', 'active', 'NOT_STATED',
            'The sidebar gives sensitivity and impedance but no passive/active statement.'),
      }, total=2, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.stereophile.com/content/totem-acoustic-model-1-loudspeaker-specifications',
      'Stereophile Totem Acoustic Model 1 loudspeaker specifications',
      'Specifications sidebar: "Drive-units: 1.2\\" (28mm) metal-dome SEAS tweeter, 125mm Dynaudio 15W75 ... woofer"; 87 dB/W/m; 4 ohms; "Amplifier requirements: 15W minimum, 120W maximum".',
      {
          R('totem-model1', 'driverCount',
            'SUPPORTED_NOT_PROMOTED', 'One 28 mm tweeter and one 125 mm woofer are listed (2 transducers); third-party review page.'),
      }, total=2, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.stereophile.com/content/vandersteen-2ce-signature-loudspeaker-specifications',
      'Stereophile Vandersteen 2Ce Signature loudspeaker specifications',
      'Specifications sidebar: "1\\" dual-chamber ScanSpeak metal-alloy-dome tweeter ... 4½\\" ScanSpeak polycone midrange ... 8\\" Vifa polycone woofer ... 10\\" ... Active Acoustic Coupler"; "Recommended amplification: 40-160Wpc into 8 ohms"; no passive/active wording.',
      {
          R('vandersteen-2ce', 'active', 'NOT_STATED',
            'Only "Recommended amplification" is given; the page never states passive/active.'),
      }, total=2, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.soundandvision.com/content/pioneer-ex-series-surround-speaker-system-specifications',
      'Sound & Vision Pioneer EX Series surround speaker system specifications',
      'The fetched page returned site navigation and review index content only; the measured-specifications table was not present in the served text.',
      {
          R('legacy-pio-4', 'driverCount', 'NOT_EXTRACTED',
            'No specification table was served in the fetched page; nothing can be asserted for the Elite S-1EX.'),
          R('legacy-pio-4', 'active', 'NOT_EXTRACTED',
            'No specification table was served in the fetched page.'),
      }, total=6, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.soundonsound.com/reviews/mackie-hr824',
      'Sound On Sound review: Mackie HR824',
      'Review: "a compact, two-way active nearfield monitor"; "the HR824 uses a substantial 8.75-inch woofer ... complemented by a 1-inch, ferrofluid-cooled aluminium domed tweeter"; "an active crossover ... at 2kHz"; bass/mid amplifier 150 W, tweeter 100 W.',
      {
          R('mackie-hr824', 'driverCount',
            'SUPPORTED_NOT_PROMOTED', 'Review names an 8.75-inch woofer and a 1-inch tweeter (2 transducers); third-party review.'),
          R('mackie-hr824', 'active',
            'SUPPORTED_NOT_PROMOTED', 'Review calls the HR824 a "two-way active nearfield monitor" with built-in 150 W/100 W amplifiers; third-party review.'),
      }, total=3, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.hifi-guide.com/loudspeaker/bowers-wilkins-801-matrix/',
      'hifi-guide Bowers & Wilkins 801 Matrix entry',
      'Database entry: "Type: Passive"; "Way system: 3"; "Nominal Impedance: 8 Ohm"; "Frequency Response: 35 - 20000 Hz"; "Sensitivity: 87 dB"; "Produced since: 1987".',
      {
          R('b&w-801', 'active', 'SUPPORTED_NOT_PROMOTED',
            'Entry states "Type: Passive", but hifi-guide is an enthusiast database and cannot promote the field.'),
      }, total=1, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.hifi-guide.com/loudspeaker/klipsch-kg-4-5/',
      'hifi-guide Klipsch KG 4.5 entry',
      'Database entry: "Type: Passive"; "Way system: 2"; "Nominal Impedance: 8 Ohm"; "Sensitivity: 95 dB"; "Crossover Frequency: 1600 Hz"; "Power Handling 100 Watts (500 Watts peak)".',
      {
          R('klipsch-kg4', 'active', 'SUPPORTED_NOT_PROMOTED',
            'Entry states "Type: Passive", but hifi-guide is an enthusiast database and cannot promote the field.'),
      }, total=1, source_class='NON_MANUFACTURER_HOST'),
    C('https://www.radiomuseum.org/r/klh_compact_bookshelf_speaker_system_model_six_6.html?language_id=2',
      'Radiomuseum KLH Compact Bookshelf Speaker System Model Six entry',
      'Radiomuseum technical specifications: "Loudspeaker: 2 Loudspeakers"; "Power type and voltage: No Power needed"; year 1958; dimensions 322 x 597 x 302 mm.',
      {
          R('klh-model-6', 'driverCount',
            'SUPPORTED_NOT_PROMOTED', 'Entry lists "2 Loudspeakers", but Radiomuseum is a third-party catalogue and cannot promote the field.'),
      }, total=1, source_class='NON_MANUFACTURER_HOST'),
]

STRUCTURAL = []
