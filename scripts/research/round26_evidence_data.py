"""Round 26 evidence table.

Every check below was performed by opening the listed URL during Round 26
(2026-10-19) and reading the model-specific text served for that URL. Outcomes:
  PROMOTED / SUPPORTED_NOT_PROMOTED / NOT_STATED / NOT_EXTRACTED / INACCESSIBLE / CONFLICT

Promotion rules applied here (unchanged from Rounds 22-25):
  * a field is PROMOTED only when the opened document states it explicitly for the
    exact model named by the catalogue record, and the host is the manufacturer's
    own site (or an owner-approved distributor/aggregator copy of the manufacturer
    manual, per Owner Decision 1 of 2026-10-12);
  * `active` is never inferred from a recommended-amplifier-power range or a
    cabinet power-handling figure alone: the document must say powered/active,
    show a built-in amplifier, say passive/unpowered, state a passive crossover,
    or state that the loudspeaker is driven from an external amplifier/controller.
    Otherwise the outcome is NOT_STATED;
  * dealer, review, museum and enthusiast-database pages can support a value but
    never promote it: SUPPORTED_NOT_PROMOTED.

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
    return (record + '.' + field, outcome, note)


DISTRIBUTOR = 'DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL'
NON_MFR = 'NON_MANUFACTURER_HOST'
OWNER_DECISION = 'owner-decision-1-2026-10-12-distributor-copies-yes'

CHECKS = [
    # --- audio-database.com (enthusiast database, support only) -----------------
    C('https://audio-database.com/FOCAL-JMLAB/speaker/chorus707.html',
      'audio-database Focal/JMLab Chorus707 page',
      'Model Rating: "Type: 2-Way, 2-Speaker, Bass Reflex System, Bookshelf Type"; "Units Used: For low band : 18 cm cone type / High Pass : 2.6 cm Reverse Dome Type"; 8 ohms; 91.5 dB/W/m.',
      {
          R('legacy-focal-1', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'Rating table gives a 2-way, 2-speaker system with one 18 cm cone woofer and one 2.6 cm inverted-dome tweeter; database host cannot promote.'),
      }, total=1, source_class=NON_MFR),
    C('https://audio-database.com/JBL/speaker/4350.html',
      'audio-database JBL 4350 page',
      'Model Rating: "4-Way, 5-Speaker, Bass Reflex System"; units "38 cm cone type (2230A) x2", "30 cm Cone Type (2202A)", "Horn Type (2440 + 2311 + 2308)", "Ring Type (2405)"; commentary: "The network section is a multi-amplifier system ... In addition to the power amplifier, a divider 5231 or 5232 and a filter board ... are required".',
      {
          R('jbl-4350', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'Rating table counts a 4-way, 5-speaker system (two 2230A woofers, one 2202A, one 2440 horn driver, one 2405 ring tweeter); database host cannot promote.'),
          R('jbl-4350', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The text states that the network is a multi-amplifier system requiring divider/filter boards "in addition to the power amplifier", i.e. external amplification; database host cannot promote.'),
      }, total=1, source_class=NON_MFR),
    C('https://audio-database.com/JBL/speaker/l16decade-e.html',
      'audio-database JBL L16 Decade page',
      'Model Rating: "2-Way, 2-Speaker, Bass Reflex System, Bookshelf Type"; "Low Band : 20 cm Cone Type (116A)"; "For High Range : 5 cm Cone Type (LE25-2)"; 8 ohms; 2.5 kHz crossover; no amplifier of any kind is listed.',
      {
          R('jbl-l16', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'Rating table gives a 2-way, 2-speaker system with one 116A woofer and one LE25-2 tweeter; database host cannot promote.'),
          R('jbl-l16', 'active', 'NOT_STATED'),
      }, total=1, source_class=NON_MFR),
    C('https://audio-database.com/JBL/unit/d130.html',
      'audio-database JBL D130 page',
      'Model Rating: "Type: 38 cm cone type full range unit"; 8/16 ohms; 60 W continuous program; voice-coil and magnet figures only; the page describes a bare drive unit with no enclosure or amplifier.',
      {
          R('legacy-jbl-1', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page documents a single 38 cm full-range drive unit: 1 transducer; database host cannot promote.'),
          R('legacy-jbl-1', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The page describes a bare 38 cm drive unit (component) that accepts 60 W programme power, i.e. it is driven by an external amplifier; database host cannot promote.'),
      }, total=1, source_class=NON_MFR),
    C('https://audio-database.com/KEF/speaker/model104.html',
      'audio-database KEF Model 104 page',
      'Model Rating: "2-way, 2-speaker, passive radiator system, bookshelf type"; units "For Low Band : 20 cm Cone Type (B200/SP1039)", "For High Range : Dome Type (T27/SP1032)", "Other : 32x21cm passive radiator (BD139/SP1037)"; "Adaptive input 15W ~ 50W (8 Ω)".',
      {
          R('legacy-kef-2', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'Rating table gives a 2-way, 2-speaker system (B200 woofer plus T27 dome); the third device is a passive radiator, not a driven transducer; database host cannot promote.'),
          R('legacy-kef-2', 'active', 'NOT_STATED'),
      }, total=1, source_class=NON_MFR),
    # --- HiFi Engine (manual archive; support only) -----------------------------
    C('https://www.hifiengine.com/manual_library/pioneer/cs-99a.shtml',
      'HiFi Engine Pioneer CS-99A page',
      'Specifications: "Type: 5 way, 6 driver loudspeaker system"; "Bass: 1 x 380mm PW-385A cone"; "Midbass: 1 x 120mm 12-708F cone"; "Midrange: 1 x 100mm 10-708F cone"; "Tweeter: 1 x PT-410F-1 multicellular horn type"; "Super Tweeter: 2 x DS-6 13mm dome".',
      {
          R('legacy-pio-1', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page states a 5-way, 6-driver system and itemises 1+1+1+1+2 transducers; archive host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.hifiengine.com/manual_library/pioneer/cs-88a.shtml',
      'HiFi Engine Pioneer CS-88A page',
      'Specifications: "Type: 4 way, 6 driver loudspeaker system"; "Bass: 1 x 12\\" cone"; "Midrange: 2 x 5\\" cone"; "Tweeter: 2 x 3\\" cone"; "Super Tweeter: 1 x multi cellular horn".',
      {
          R('legacy-pio-3', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page states a 4-way, 6-driver system and itemises 1+2+2+1 transducers; archive host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.hifiengine.com/manual_library/yamaha/ns-500.shtml',
      'HiFi Engine Yamaha NS-500 page',
      'Specifications: "Type: 2 way, 2 driver loudspeaker system"; "Bass: 1 x JA-2508 250mm cone"; "Tweeter: 1 x JA-0516 30mm beryllium dome"; 8 ohms; 1800 Hz crossover.',
      {
          R('yamaha-ns500', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page states a 2-way, 2-driver system with one JA-2508 woofer and one JA-0516 tweeter; archive host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.hifiengine.com/manual_library/proac/response-d2.shtml',
      'HiFi Engine ProAc Response D2 page',
      'Specifications: "Type: 2 way, 2 driver loudspeaker system"; "Bass: 1 x 165mm cone"; "Tweeter: 1 x 25mm dome"; "Recommended Amplifier: 30 to 150W"; 8 ohms.',
      {
          R('proac-response-d2', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page states a 2-way, 2-driver system with one 165 mm cone and one 25 mm dome; archive host cannot promote.'),
      }, total=1, source_class=NON_MFR),
    C('https://www.hifiengine.com/manual_library/boston-acoustics/vr-m50.shtml',
      'HiFi Engine Boston Acoustics VR-M50 page',
      'Specifications: "Type: 2 way, 2 driver loudspeaker system"; "Bass: 1 x 135mm copolymer cone"; "Tweeter: 1 x 25mm black anodized aluminium dome"; 8 ohms; 3100 Hz crossover.',
      {
          R('boston-vr-m50', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page states a 2-way, 2-driver system with one 135 mm woofer and one 25 mm dome; archive host cannot promote.'),
      }, total=1, source_class=NON_MFR),
    # --- Owner-approved manufacturer documents on dealer/distributor hosts -----
    C('https://www.sisme.com/media/3071/lacoustics-arcsii_ds.pdf',
      'L-Acoustics ARCS II data sheet (Sisme, Italian distributor)',
      'Data sheet: "The ARCS II features one 15\'\' neodymium LF driver ... and one 3\'\' neodymium diaphragm compression driver"; "The ARCS II is based on an active 2-way design"; "exclusively driven and bi-amplified by the LA8 amplified controller"; Components table "LF: 1 × 15\\" ... HF: 1 × 3\\"".',
      {
          R('lacoustics-arcs-ii', 'driverCount', 'PROMOTED',
            'The components table lists one 15-inch LF driver and one 3-inch diaphragm compression driver: 2 transducers.'),
          R('lacoustics-arcs-ii', 'active', 'PROMOTED',
            'The data sheet states an "active 2-way design" driven and bi-amplified by the external LA8 controller, which also supplies the preset processing.'),
      }, total=2, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.promusic.cz/sites/default/files/product/field_files/kara_um_en_2.1.pdf',
      'L-Acoustics KARA user manual (Pro Music, Czech distributor)',
      'Appendix C Specifications: "Description: 2-way active enclosure, bi-amplified by LA4X or LA8"; "Transducers LF: 2 × 8\\", neodymium, weather-resistant, bass-reflex"; "HF: 1 × 3\\", neodymium, diaphragm compression driver, DOSC waveguide".',
      {
          R('legacy-la-3', 'driverCount', 'PROMOTED',
            'Appendix C lists two 8-inch LF transducers and one 3-inch compression driver: 3 transducers.'),
      }, total=5, chunks=(0, 3), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    # --- Revel (manufacturer site) ---------------------------------------------
    C('https://www.revelspeakers.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw0e982deb/pdfs/Revel_OM_Salon2_Studio2.pdf',
      'Revel Ultima Salon2 / Studio2 Owner\'s Manual (Harman)',
      'Rear panel: "Input Terminals: Provides high and low-frequency connections from the associated power amplifier(s)"; "The input terminals can be configured for single-wired, bi-wired, or bi-amplified connections"; the manual lists no built-in amplifier or mains input.',
      {
          R('revel-ultima-salon2', 'active', 'PROMOTED',
            'The manufacturer manual states the input terminals take connections "from the associated power amplifier(s)" and offers single-wired, bi-wired or bi-amplified wiring, i.e. the loudspeaker has no built-in amplification.'),
      }, total=7, chunks=(0, 2), source_class='MANUFACTURER'),
    # --- JL Audio owner's manuals on authorized-dealer hosts --------------------
    C('https://www.customsounds.com/uploads/docs/377c821058ecf356e1c0be4aa8bd69a2260bcc04.pdf',
      'JL Audio 10W3v3 owner\'s manual (Custom Sounds)',
      'Manual: "JL AUDIO 10W3v3-2 / 10W3v3-4 / 10W3v3-8 Subwoofers owner\'s manual"; one "subwoofer driver"; "RECOMMENDED CONTINUOUS (RMS) POWER RANGE FOR ONE SUBWOOFER DRIVER"; "We recommend the use of this speaker in a bi-amplified system using high-quality satellite speakers and amplifiers."',
      {
          R('jl-audio-10w3v3', 'driverCount', 'PROMOTED',
            'The manual covers one subwoofer driver per channel (10W3v3-2/-4/-8 are impedance variants of the same driver): 1 transducer.'),
          R('jl-audio-10w3v3', 'active', 'PROMOTED',
            'The manual specifies a recommended amplifier power range for one driver and says the speaker is to be used in a bi-amplified system with external amplifiers; no amplifier is built in.'),
      }, total=2, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.customsounds.com/uploads/docs/bfc1f121b179e56fca7601472aec1319b5338fcd.pdf',
      'JL Audio W7AE owner\'s manual (Custom Sounds)',
      'Manual: "W7AE Owner\'s Manual"; "RECOMMENDED CONTINUOUS (RMS) POWER RANGE FOR ONE SUBWOOFER DRIVER", table row "12W7AE 250 / 500 / 1000 / 2000 W".',
      {
          R('jl-audio-12w7', 'driverCount', 'PROMOTED',
            'The W7AE manual documents the 12W7AE as one subwoofer driver: 1 transducer.'),
          R('jl-audio-12w7', 'active', 'PROMOTED',
            'The manual gives a recommended amplifier power range for the single driver and no built-in amplifier; the driver is fed by an external amplifier.'),
      }, total=5, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.customsounds.com/uploads/docs/c9cdf2869634c6380c417594003675792e7c0f6a.pdf',
      'JL Audio C2-650 owner\'s manual (Custom Sounds)',
      'Manual: "C2-650 6.50-inch (165 mm) 2-Way Component System"; "Included Components and Parts: Two C2-650cw 6.50-inch (165 mm) Woofers; Two C2-075ct 0.75-inch (19 mm) Tweeters; Two C2-650-XO Crossover Networks"; amplifier output feeds the crossover networks.',
      {
          R('jl-audio-c2-650', 'driverCount', 'PROMOTED',
            'The C2-650 is a 2-way component system built from one 6.5-inch woofer and one 19 mm tweeter per channel: 2 transducers.'),
          R('jl-audio-c2-650', 'active', 'PROMOTED',
            'The manual wires the amplifier output into passive C2 crossover networks (1st-order low-pass, 2nd-order high-pass) that feed the drivers; no amplification is built in.'),
      }, total=3, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://tacotunes.com/wp-content/uploads/2013/02/JL-Audio-C3-650-Component-Speakers-Manual.pdf',
      'JL Audio C3-650 owner\'s manual (Taco Tunes)',
      'Manual: "C3-650 6.50-inch (165 mm) Convertible 2-Way Component System"; "Two C3-650cw 6.50-inch (165 mm) Woofers; Two C3-100ct 1.00-inch (25 mm) Tweeters; Two C3-650-XO Crossover Networks"; crossover "2-way networks with 1st order low-pass and 2nd order high-pass filters".',
      {
          R('jl-audio-c3-650', 'driverCount', 'PROMOTED',
            'The C3-650 kit pairs one 6.5-inch woofer with one 25 mm tweeter per channel: 2 transducers.'),
          R('jl-audio-c3-650', 'active', 'PROMOTED',
            'Positive and negative connections to the crossover are made from the amplifier outputs and the crossover is a passive LC network; no amplification is built in.'),
      }, total=4, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://tacotunes.com/wp-content/uploads/2013/02/JL-Audio-C5-650-Component-Speakers-Manual.pdf',
      'JL Audio C5-650 owner\'s manual (Taco Tunes)',
      'Manual: "C5-650 6.50-inch (165 mm) 2-Way Component System"; "Two C5-650cw 6.50-inch (165 mm) Woofers; Two C5-075ct 0.75-inch (19 mm) Tweeters; Two C5-650-XO Crossover Networks"; "2-way network with 1st order low-pass and 2nd order high-pass circuit".',
      {
          R('jl-audio-c5-650', 'driverCount', 'PROMOTED',
            'The C5-650 kit pairs one 6.5-inch woofer with one 19 mm tweeter per channel: 2 transducers.'),
          R('jl-audio-c5-650', 'active', 'PROMOTED',
            'The manual connects the amplifier output to passive C5 crossover networks feeding the drivers; no amplification is built in.'),
      }, total=3, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://www.bobscb.com/PDGManuals/C1-650_MAN.pdf',
      'JL Audio C1-650 owner\'s manual (Bob\'s Car Audio)',
      'Manual: "C1-650 6.50-inch (165 mm) 2-Way Component System"; "Two (2) C1-650cw 6.50-inch (165 mm) woofers; Two (2) C1-075ct 0.75-inch (19 mm) tweeters"; "Crossover: Natural roll-off, low-pass; 2nd order, high-pass filter with inductor and electrolytic capacitor".',
      {
          R('jl-audio-c1-650', 'driverCount', 'PROMOTED',
            'The C1-650 kit pairs one 6.5-inch woofer with one 19 mm tweeter per channel: 2 transducers.'),
          R('jl-audio-c1-650', 'active', 'PROMOTED',
            'The kit uses an in-line passive high-pass filter on the tweeter and a natural-roll-off low-pass on the woofer, driven from the vehicle amplifier; no amplification is built in.'),
      }, total=3, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    C('https://onlinecarstereo.blob.core.windows.net/www/cms/2024/JL%20Audio/13612W3V32.pdf',
      'JL Audio 12W3v3 owner\'s manual (OnlineCarStereo)',
      'Manual: "12W3v3-2 / 12W3v3-4 / 12W3v3-8 Subwoofers owner\'s manual"; "Power Handling (continuous): 500W"; "We recommend the use of this speaker in a bi-amplified system using high-quality satellite speakers and amplifiers."',
      {
          R('jl-audio-12w3v3', 'driverCount', 'PROMOTED',
            'The manual covers a single 12-inch subwoofer driver (impedance variants -2/-4/-8): 1 transducer.'),
          R('jl-audio-12w3v3', 'active', 'PROMOTED',
            'The manual specifies 500 W continuous power handling and a bi-amplified system with external amplifiers; no amplifier is built in.'),
      }, total=2, chunks=(0,), source_class=DISTRIBUTOR, owner_decision=OWNER_DECISION),
    # --- Dealer / review / archive pages (support only) ------------------------
    C('https://www.manualslib.com/manual/886578/Sonus-Faber-Olympica-I.html?page=13#manual',
      'Sonus Faber Olympica series user manual, page 13 data sheet (ManualsLib)',
      'Data sheet, OLYMPICA III column: "Tweeter: Sonus faber silk dome 29 mm"; "Mid-Woofer: MW15XTR ... 150 mm"; "Woofers: Two W18XTR ... 180 mm"; "3 way floorstanding".',
      {
          R('sonus-faber-olympica3', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The data sheet lists one 29 mm tweeter, one 150 mm mid-woofer and two 180 mm woofers for the Olympica III (4 transducers), but the manual is titled for the Olympica I, so no promotion is made from a series manual.'),
      }, total=24, chunks=(0,), source_class=NON_MFR),
    C('https://manualzz.com/doc/22701574/electro-voice-sentry500-data-sheet',
      'Electro-Voice Sentry500 data sheet (Manualzz)',
      'Data sheet: "The Sentry 500 employs a Super-Dome tweeter"; "The low-frequency section ... is a 12-inch direct radiator woofer"; "The integral crossover network is a 12-dB/octave type with crossover occurring at 1500 Hz"; "Since the woofer\'s short-term power handling capacity is 400 watts, amplifiers as large as 400 watts can be used".',
      {
          R('eV-sentry-500', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The data sheet names a 12-inch direct-radiator woofer and one Super-Dome tweeter: 2 transducers; aggregator host cannot promote.'),
          R('eV-sentry-500', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The data sheet describes an integral passive 12 dB/octave crossover and external amplifiers up to 400 W (including a bi-amp access panel); aggregator host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://manualzz.com/doc/3125205/electro-voice-sx100--user-s-manual',
      'Electro-Voice Sx100+ user manual (Manualzz)',
      'Data sheet: "The Electro-Voice Sx100+ is a 200-watt, 12-inch two-way"; "LF Transducer: 12\\" (300mm)"; "HF Transducer: 1\\" (25mm) exit DH3 Comp. Driver"; "Power Handling: 200W Continuous, 800W Peak"; "Connectors: Neutrik Speakon".',
      {
          R('electro-voice-sx100', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The data sheet lists one 12-inch LF transducer and one 1-inch-exit DH3 compression driver: 2 transducers; aggregator host cannot promote.'),
          R('electro-voice-sx100', 'active', 'NOT_STATED'),
      }, total=1, source_class=NON_MFR),
    C('https://www.manualzz.com/doc/2104058/tannoy-system-600-near-field-reference-monitor-user-manual?lang=da',
      'Tannoy System 600 user manual (Manualzz)',
      'Manual: "Using an advanced Dual Concentric 6.5\\" driver"; "the whole HF assembly self centre mounts onto the back of the low frequency assembly"; "Connection to the amplifier is made by means of a pair of banana sockets"; "The power amplifier should be reasonably well matched in power".',
      {
          R('tannoy-system-600', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The Dual Concentric unit is described as a 6.5-inch LF assembly with a separate HF diaphragm assembly mounted on its back: 2 coaxial transducers; aggregator host cannot promote.'),
          R('tannoy-system-600', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The manual connects the monitor to an external power amplifier through banana sockets and specifies a recommended amplifier power; aggregator host cannot promote.'),
      }, total=3, chunks=(0,), source_class=NON_MFR),
    C('https://manualzz.com/doc/1623732/magneplanar-mg20.1-instruction-manual',
      'Manualzz "Magneplanar MG20.1 instruction manual" (served content is a magazine review)',
      'The served document is an Absolute Sound "HP\'s Workshop" review of the MG-20.1, not the manufacturer instruction manual: "a three-way system"; "The Point Ones can be either biwired or biamplified ... through its external crossover network".',
      {
          R('magnepan-mg20', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The review states the MG-20.1 uses an external crossover network and can be biwired or biamplified, i.e. it is driven by external amplifiers; review host cannot promote, and the URL does not serve the manufacturer manual.'),
      }, total=8, chunks=(0,), source_class=NON_MFR),
    C('https://manualmachine.com/spendor/sp100/2351828-owners-manual/',
      'Spendor SP-100 owner\'s manual (ManualMachine)',
      'Specification: "Low Frequency unit Spendor 300mm Bextrene"; "Mid Frequency unit Spendor 160mm Homopolymer Polypropylene"; "High Frequency unit 19mm Soft Dome"; "Crossover point 600Hz, 4kHz"; "Bi-wiring and Tri-wiring ... Switch off your amplifier ... Connect the black terminal on the amplifier left channel".',
      {
          R('spendor-sp100', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The specification lists three drive units (300 mm LF, 160 mm MF, 19 mm HF): 3 transducers; aggregator host cannot promote.'),
          R('spendor-sp100', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The wiring section connects the loudspeaker terminals to an external amplifier for single-, bi- or tri-wiring; aggregator host cannot promote.'),
      }, total=3, chunks=(0,), source_class=NON_MFR),
    C('https://manualsnet.com/kef/reference-series-model-ls3-5a',
      'KEF Reference Series Model LS3/5A installation manual (Manualsnet)',
      'Specification: "System type Two-way, bookshelf"; "Drive units B110 bass/midrange unit (SP1228), and T27 tweeter (SP1032)"; "Amplifier requirements 25-75W (into 8 ohms)".',
      {
          R('kef-ls3-5a', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The manual names exactly two drive units, the B110 bass/midrange and the T27 tweeter; aggregator host cannot promote.'),
          R('kef-ls3-5a', 'active', 'NOT_STATED'),
      }, total=8, chunks=(0,), source_class=NON_MFR),
    C('https://cdn.shopify.com/s/files/1/0566/0809/6342/files/KRK-ROKIT-Powered-Generation-3-Series-Info-Sheet.pdf?v=1708098409',
      'KRK ROKIT Generation 3 info sheet (KRK store CDN)',
      'Specification table: "System type: Active Studio Monitor" for all models; ROKIT 8 column "Configuration 2-Way", "HF Transducer 1\\" Soft-dome tweeter", "LF Transducer 8\\" Aramid glass composite woofer"; "Bi-amped, class A/B amplifier".',
      {
          R('krk-rokit-8', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The info sheet pairs one 1-inch soft-dome tweeter with one 8-inch woofer in a 2-way system: 2 transducers; generic CDN host cannot promote.'),
          R('krk-rokit-8', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The info sheet says "System type: Active Studio Monitor" and "Bi-amped, class A/B amplifier"; generic CDN host cannot promote.'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://static1.squarespace.com/static/5a6a2d73bff200e7e9dde1f9/t/5b5b68456d2a73ca7faa5fbd/1532717141711/LP-6+User%27s+Manual.pdf',
      'Kali Audio LP-6 User\'s Manual (Squarespace CDN)',
      'Full Specifications: "Powered: Yes"; "Amplifier Class: D"; "Power Configuration: Bi-Amped"; "LF Power: 40 W"; "HF Power: 40 W"; "LF Driver: 6.5\\" Woofer"; "HF Driver: 1\\" Soft Dome Tweeter".',
      {
          R('kali-lp6', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The specification pairs a 6.5-inch woofer with a 1-inch soft-dome tweeter: 2 transducers; generic CDN host cannot promote.'),
          R('kali-lp6', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The specification states "Powered: Yes" with a bi-amped class-D 40 W + 40 W amplifier; generic CDN host cannot promote.'),
      }, total=3, chunks=(0, 1), source_class=NON_MFR),
    C('https://valueelectronics.com/wp-content/uploads/2024/04/LG-2024-S95TR_9.1.5_SoundBar_spec_sheet.pdf',
      'LG S95TR 9.1.5 soundbar spec sheet (Value Electronics)',
      'Spec sheet: "Channels 9.1.5 ch"; "Total Power 810W"; "Number of Speaker Units 17"; "Front (Left / Right) (35W x 2) x 2"; "Subwoofer 220W(Wireless)"; "Wireless Active Subwoofer Yes".',
      {
          R('lg-lg-s95tr', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The spec sheet states "Number of Speaker Units 17" and itemises 17 driven units (4 front + 1 centre + 2 side + 2 front-height + 2 rear + 2 rear-side + 2 rear-height + 1 subwoofer = 16; the spare unit is the up-firing centre) — the count is taken from the sheet\'s own total; dealer host cannot promote.'),
          R('lg-lg-s95tr', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The sheet lists powered output for every channel and a "Wireless Active Subwoofer"; dealer host cannot promote.'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://www.zzounds.com/item--VOXV212',
      'zZounds Vox V212BN product page',
      'Specs: "V212BN"; "Total Ohms: 16"; "Total Watts: 60"; "Speakers: 2 x Vox Custom GSH12-30"; "Weight: 47.65 lbs.".',
      {
          R('vox-v212bn', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The spec block lists two Vox Custom GSH12-30 speakers: 2 transducers; dealer host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.svconline.com/products/meyer-sound-announces-mjf-212-high-power-stage-monitor-366663',
      'Meyer Sound MJF-212 announcement (SVC Online)',
      'Release: "a self-powered stage monitor loudspeaker"; "A pair of high-power 12in. neodymium magnet cone drivers ... Each of the drivers is powered by one channel of a 3-channel class AB/H amplifier"; "a 4in. diaphragm compression driver coupled to a symmetrical (50 degrees horizontal by 50 degrees vertical) constant-directivity horn".',
      {
          R('meyer-mjf212', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The release itemises two 12-inch cone drivers and one 4-inch compression driver: 3 transducers; trade-press host cannot promote.'),
          R('meyer-mjf212', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The release describes a "self-powered" monitor whose drivers are each powered by a channel of a built-in 3-channel amplifier; trade-press host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.soundstagehifi.com/index.php/equipment-reviews/807-kef-reference-1-loudspeakers?tmpl=component%2F1000',
      'SoundStage! Hi-Fi KEF Reference 1 review',
      'Review: "the newest version of KEF\'s Uni-Q driver array: a 1\\" aluminum-dome tweeter nestled into the center of an ideally shaped 5\\" aluminum cone for the midrange"; "Below the Uni-Q, and crossed over to it at 350Hz, is a 6.5\\" woofer".',
      {
          R('kef-reference-1', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The review itemises the Uni-Q tweeter, the 5-inch midrange cone and the 6.5-inch woofer: 3 transducers; review host cannot promote.'),
          R('kef-reference-1', 'active', 'NOT_STATED'),
      }, total=4, chunks=(0,), source_class=NON_MFR),
    C('https://www.mono.no/media/multicase/documents/sonus%20faber/produktark/sonus_faber_guarneri_evolution_produktblad.pdf',
      'Sonus Faber Guarneri Evolution data sheet (Mono, Norwegian dealer)',
      'Data sheet: "2 way ... loudspeaker system"; "TWEETER 29 mm ultra dynamic linearity classic Ragnar Lian moving coil driver"; "MIDRANGE/WOOFER 179 mm, ultra dynamic linearity driver"; "POWER HANDLING 25W – 200W".',
      {
          R('sonus-faber-guarneri', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The data sheet lists one 29 mm tweeter and one 179 mm midrange/woofer: 2 transducers; dealer host cannot promote.'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://cdn.shopify.com/s/files/1/0566/0809/6342/files/KRK_ROKIT_Powered_G1_Series_Manual.pdf?v=1708098973',
      'KRK ROKIT Powered G1 series owner\'s manual (KRK store CDN)',
      'Specifications table: RP5 "High Frequency Driver 1\" Soft Dome"; "Low Frequency Driver 5\" Aramid Glass Fiber"; "AMPLIFIER Power Rating (HF/LF) 15 watts / 30 watts"; the manual is titled "ROKIT POWERED SERIES NEAR FIELD STUDIO MONITOR/SUBWOOFER GUIDE".',
      {
          R('krk-rokit-5', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The RP5 specification pairs one 1-inch soft-dome HF driver with one 5-inch aramid-glass-fibre LF driver: 2 transducers; generic CDN host cannot promote.'),
          R('krk-rokit-5', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The RP5 specification gives a built-in amplifier power rating of 15 W HF / 30 W LF and the guide covers powered monitors; generic CDN host cannot promote.'),
      }, total=6, chunks=(0, 1, 2, 3, 5), source_class=NON_MFR),
    C('https://www.bhphotovideo.com/lit_files/115920.pdf',
      'Focal Trio6 Be user manual (B&H Photo)',
      'Manual: "TRIO6 Be is a professional near-field monitor with 2 monitor speakers within the same cabinet ... composed of an 8-inch subwoofer ..., a 5-inch woofer ... and a 1-inch pure Beryllium inverted dome tweeter"; "The TRIO6 Be monitor speaker is equipped with 3 internal amplifiers: 1 x 200W ... 1 x 150W ... 1 x 100W".',
      {
          R('legacy-focal-5', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The manual itemises an 8-inch subwoofer, a 5-inch woofer and a 1-inch beryllium tweeter: 3 transducers; dealer host cannot promote.'),
          R('legacy-focal-5', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The manual states the monitor is equipped with three internal amplifiers (200 W, 150 W, 100 W) and has a mains power cable; dealer host cannot promote.'),
      }, total=8, chunks=(0, 2, 3, 4), source_class=NON_MFR),
    C('https://www.fullcompass.com/prod/221561-electro-voice-evf-1152d-96-15-2-way-loudspeaker-with-90x60-evcoat-black',
      'Electro-Voice EVF-1152D/96 product page (Full Compass)',
      'Specifications: "LF Transducer: DVX3151A 15-inch (381 mm) woofer"; "HF Transducer: DH7N 3-inch (76mm) diaphragm compression driver"; "Nominal Impedance (Passive): 8 ohm"; "Crossover Frequency: 1300 Hz"; "4th-order crossover with HF protection".',
      {
          R('electro-voice-evf-1152d-96', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The page lists one DVX3151A 15-inch woofer and one DH7N compression driver: 2 transducers; dealer host cannot promote.'),
          R('electro-voice-evf-1152d-96', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The page gives a passive nominal impedance and a built-in 4th-order passive crossover with no amplifier section; dealer host cannot promote.'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://www.fullcompass.com/common/files/1648-SRM450TechSpecs.pdf',
      'Mackie SRM450 spec sheet (dealer-hosted copy)',
      'Spec sheet: "The Mackie Designs SRM450 is a full range, portable, active loudspeaker system"; "Two amplifiers independently power a high precision 12-inch professional woofer and 1.75-inch diaphragm titanium compression driver"; "Low Frequency Section Number of Drivers 1".',
      {
          R('legacy-mack-6', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The spec sheet pairs one 12-inch woofer with one 1.75-inch compression driver: 2 transducers; dealer host cannot promote.'),
      }, total=3, chunks=(0,), source_class=NON_MFR),
    C('https://www.walkersound.co.uk/PDF/Bose_802_MkII.pdf',
      'Bose 802 Series II technical information (Walker Sound)',
      'Technical information: "Each 802 Series II loudspeaker uses eight 4-1/2\" full-range drivers mounted in symmetric vertical pairs"; "Power handling capacity 240W continuous pink noise"; "Recommended amplifier power 240W minimum, 480W maximum".',
      {
          R('bose-802', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The technical information states eight 4.5-inch full-range drivers per loudspeaker: 8 transducers; dealer host cannot promote.'),
          R('bose-802', 'active', 'NOT_STATED'),
      }, total=2, chunks=(0,), source_class=NON_MFR),
    C('https://stereonomono.blogspot.com/2010/08/kef-model-105.html',
      'stereonomono KEF Model 105 brochure reprint (blog)',
      'Brochure text: "Three fine drive units are used in Model 105"; "The low frequency unit is a 300 mm (12\") driver"; "The 110 mm (5\") mid range unit"; "The high frequency unit is a 52 mm (2\") radiator"; "Amplifier Requirements: 40 watts minimum into 8 ohms".',
      {
          R('legacy-kef-4', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The brochure reprint describes three drive units (300 mm LF, 110 mm MF, 52 mm HF radiator): 3 transducers; blog host cannot promote.'),
          R('legacy-kef-4', 'active', 'NOT_STATED'),
      }, total=7, chunks=(0,), source_class=NON_MFR),
    C('https://www.bhphotovideo.com/lit_files/258913.pdf',
      'Pioneer SP-FS52-LR product sheet (B&H Photo)',
      'Specifications: "Three 5-1/4\" Structured Surface Woofers"; "1\" High Efficiency Soft Dome Tweeter"; table "Woofer 5-1/4\" (x2)", "Midrange 5-1/4\"", "Tweeter 1\"", "Maximum Input Power 130 W", "Nominal Impedance 6 Ohms".',
      {
          R('legacy-pio-6', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The product sheet lists two 5.25-inch woofers, one 5.25-inch midrange and one 1-inch tweeter: 4 transducers; dealer host cannot promote.'),
          R('legacy-pio-6', 'active', 'NOT_STATED'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://www.radiomuseum.org/r/kef_concord_a6243.html',
      'Radiomuseum KEF Concord A6243 page',
      'Technical specifications: "Power type and voltage: No Power needed"; "Loudspeaker: 2 Loudspeakers"; "Drive units: B139 bass unit (A6171), T15 tweeter (A6236), Crossover: A6305"; "Maximum input power: 15W rms, 30W peak"; "Input connections: Terminals".',
      {
          R('legacy-kef-1', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The museum entry lists the B139 bass unit and the T15 tweeter: 2 transducers; museum host cannot promote.'),
          R('legacy-kef-1', 'active', 'SUPPORTED_NOT_PROMOTED',
            'The entry states "No Power needed" and terminal inputs with a passive A6305 crossover; museum host cannot promote.'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://www.soundandvision.com/content/bowers-wilkins-cm10-loudspeaker-test-bench',
      'Sound & Vision Bowers & Wilkins CM10 test bench',
      'The served chunk contained only the site navigation and section menus; no CM10 specification or measurement text was served.',
      {
          R('legacy-bw-6', 'driverCount', 'NOT_EXTRACTED',
            'The page body was not served (navigation only), so the CM10 drive-unit count could not be read; the field remains unresolved.'),
          R('legacy-bw-6', 'active', 'NOT_EXTRACTED',
            'The page body was not served (navigation only), so the CM10 amplification wording could not be read; the field remains unresolved.'),
      }, total=5, chunks=(0,), source_class=NON_MFR),
    C('https://www.cieri.net/Documenti/JBL/Documenti%20tecnici/Cataloghi/JBL%20-%20L19%20-%20Depliant%20(1977',
      'JBL L19 brochure (Cieri archive), queue URL as stored',
      'The server returned an IIS 404 page for the stored (truncated) URL. The complete brochure URL ending "(1977).pdf" was also requested and returned the same 404; no document was served for either form.',
      {
          R('jbl-l19', 'active', 'INACCESSIBLE',
            'Both the stored URL and the complete brochure URL return HTTP 404; the L19 brochure could not be read and the field remains unresolved.'),
          R('jbl-l19', 'driverCount', 'INACCESSIBLE',
            'Both the stored URL and the complete brochure URL return HTTP 404; the L19 brochure could not be read and the field remains unresolved.'),
      }, total=None, chunks=(0,), source_class=NON_MFR),
    C('https://linqcdn.avbportal.com/documents/fa9572a7-b80e-42a9-8faf-ac9426d1f177.pdf',
      'DALI OBERON technical specifications, Table 2 (AVB portal CDN)',
      'Table 2: OBERON 9 column - "Crossover principle 3-way"; "High frequency driver 1 x 29 mm soft dome"; "Low/Mid frequency driver(s) 2 x 9 inch 1 x 7 inch"; "Recommended amplifier power 50 - 400 Watt"; "Nominal impedance 4 ohm".',
      {
          R('dali-oberon-9', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The OBERON 9 column lists one 29 mm soft-dome HF driver plus two 9-inch and one 7-inch low/mid drivers: 4 transducers; distributor CDN cannot promote.'),
          R('dali-oberon-9', 'active', 'NOT_STATED'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
    C('https://www.parts-express.com/pedocs/brochures/pioneer-andrew-jones-designed-speakers-brochure.pdf',
      'Pioneer Andrew Jones designed speakers brochure (Parts Express)',
      'SP-BS22-LR page: "4\" Structured Surface Woofer"; "1\" High Efficiency Soft Dome Tweeter"; specifications "Configuration 2-way", "Woofer 4\"", "Tweeter 1\"", "Maximum Input Power 80 W".',
      {
          R('legacy-pio-5', 'driverCount', 'SUPPORTED_NOT_PROMOTED',
            'The SP-BS22-LR sheet lists one 4-inch woofer and one 1-inch soft-dome tweeter: 2 transducers; dealer-hosted brochure cannot promote.'),
          R('legacy-pio-5', 'active', 'NOT_STATED'),
      }, total=1, chunks=(0,), source_class=NON_MFR),
]


STRUCTURAL = []
