"""Round 23 evidence table.

Every check below was performed by opening the listed URL during Round 23
(2026-10-19) and reading the model-specific specification text. Outcomes:
  PROMOTED / SUPPORTED_NOT_PROMOTED / NOT_STATED / NOT_EXTRACTED / INACCESSIBLE / CONFLICT

Promotion rules applied here (unchanged from Round 22):
  * a field is PROMOTED only when the opened document states it explicitly for the
    exact model named by the catalogue record, and the host is the manufacturer's
    own site (or an owner-approved distributor copy);
  * `active` is never inferred from a recommended-amplifier-power range or from a
    cabinet's power-handling figure: the document must say powered/active, show a
    built-in amplifier, or say passive/unpowered. Otherwise the outcome is NOT_STATED;
  * third-party hosts (Stereophile specification sidebars) can support a value but
    never promote it: those fields are SUPPORTED_NOT_PROMOTED.

Values are filled from the live catalogue at build time, never hard-coded here.
"""
CHECKED_DATE = '2026-10-19'

NOT_STATED_NOTE = ('The opened document gives no explicit passive/active, powered/unpowered '
                   'or built-in-amplifier wording for this model (only enclosure power '
                   'handling or a recommended amplifier-power range), so `active` stays '
                   'unverified.')

PROMOTED_PASSIVE_NOTE = None  # reserved; passive promotion needs explicit wording

THIRD_PARTY_NOTE = ('Specification sidebar of a third-party review (Stereophile) reproduces '
                    'the model\'s drive-unit count, but a third-party host cannot promote a '
                    'field to MANUFACTURER_VERIFIED; recorded for the audit trail only.')


def C(url, document, evidence, results, status='CHECKED', total=None, chunks=(0,),
      source_class='MANUFACTURER'):
    return {
        'url': url,
        'document': document,
        'chunksOpened': list(chunks),
        'chunksTotal': total,
        'status': status,
        'evidence': evidence,
        'results': results,
        'sourceClass': source_class,
    }


def R(record, field, outcome='PROMOTED', note=None):
    # Hashable 3-tuple so the literals below can stay compact; the builder converts
    # them into ordered dicts deterministically.
    return (record + '.' + field, outcome, note)


CHECKS = [
    # ---------------- MARSHALL (cabinets and home speakers) ----------------
    C('https://www.marshall.com/us/en/product/1960a-4x12-angled-cabinet?pid=1007269',
      'Marshall 1960A 4x12 angled cabinet product page',
      'Specification block: Speaker configuration "4x12\\""; Speaker model "4 x Celestion '
      'G12T-75 (16Ω, 75W)"; power handling 300W mono / 150W stereo; unit impedance 16Ω mono, '
      '8Ω stereo. Four discrete 12-inch drivers are named.',
      {R('marshall-marshall-1960a', 'driverCount',
         note='Specification lists four Celestion G12T-75 12-inch drivers (4x12 configuration).'),
       R('marshall-marshall-1960a', 'active', 'NOT_STATED')}),

    C('https://www.marshall.com/us/en/product/mx112-1x12-cabinet?pid=1007173',
      'Marshall MX112 1x12 cabinet product page',
      'Specification block: Speaker configuration "1x12\\""; one Celestion Seventy-80 (80W, '
      '16Ω); power handling 80W; unit impedance 16Ω mono.',
      {R('marshall-marshall-mx112', 'driverCount',
         note='Specification lists a single 12-inch Celestion Seventy-80 (1x12 configuration).'),
       R('marshall-marshall-mx112', 'active', 'NOT_STATED')}),

    C('https://www.marshall.com/us/en/product/middleton?pid=1006034',
      'Marshall Middleton portable speaker product page',
      'Specification block: two 3" 15W woofers, two 3/5" 10W tweeters and two passive radiators; '
      'POWER AMPLIFIERS list two 15W Class D amplifiers for the woofers and two 10W Class D '
      'amplifiers for the tweeters.',
      {R('marshall-marshall-middleton', 'driverCount',
         note='Two 3-inch woofers plus two 3/5-inch tweeters are driven; the two passive '
              'radiators are not driven drivers and are excluded.'),
       R('marshall-marshall-middleton', 'active',
         note='Built-in Class D amplifiers are listed for both woofer and tweeter pairs.')}),

    C('https://www.marshall.com/us/en/product/acton-iii?pid=1006008',
      'Marshall Acton III home speaker product page',
      'Specification block lists the built-in power amplifiers (one 30W Class D amplifier for '
      'the woofer, two 15W Class D amplifiers for the tweeters) and a bass-reflex cabinet.',
      {R('marshall-marshall-acton-iii', 'active',
         note='Built-in Class D amplifiers are listed for woofer and tweeters; self-powered.')}),

    C('https://www.marshall.com/us/en/product/stanmore-iii?pid=1009642',
      'Marshall Stanmore III home speaker product page',
      'Specification block lists the built-in power amplifiers (one 50W Class D amplifier for '
      'the woofer, two 15W Class D amplifiers for the tweeters).',
      {R('marshall-marshall-stanmore-iii', 'active',
         note='Built-in Class D amplifiers are listed for woofer and tweeters; self-powered.')}),

    C('https://www.marshall.com/us/en/product/1936v-2x12-cabinet?pid=1007266',
      'Marshall 1936V 2x12 cabinet product page',
      'Specification block: Speaker configuration "2x12\\""; Speaker model "2 x Celestion G12 '
      'Vintage (16Ω, 70W)"; power handling 140W mono, 70W stereo.',
      {R('marshall-marshall-1936v', 'driverCount',
         note='Specification lists two 12-inch Celestion G12 Vintage speakers (2x12 configuration).'),
       R('marshall-marshall-1936v', 'active', 'NOT_STATED')}),

    C('https://www.marshall.com/us/en/product/mx212-2x12-cabinet?pid=1007176',
      'Marshall MX212 2x12 cabinet product page',
      'Specification block: Speaker configuration "2x12\\""; two Celestion Seventy-80 speakers '
      '(80W, 16Ω each); power handling 160W.',
      {R('marshall-marshall-mx212', 'driverCount',
         note='Specification lists two 12-inch Celestion Seventy-80 speakers (2x12 configuration).'),
       R('marshall-marshall-mx212', 'active', 'NOT_STATED')}),

    C('https://www.marshall.com/us/en/product/woburn-iii?pid=1006020',
      'Marshall Woburn III home speaker product page',
      'POWER AMPLIFIERS block: one 90W Class D amplifier for the woofer, two 15W Class D '
      'amplifiers for the mids and two 15W Class D amplifiers for the tweeters.',
      {R('marshall-marshall-woburn-iii', 'active',
         note='Built-in Class D amplifier bank is listed for woofer, mids and tweeters.')}),

    C('https://www.marshall.com/us/en/support/amps/support-for-1960av-4x12-angled-cabinet',
      'Marshall 1960AV 4x12 angled cabinet support page (product details)',
      'Support page product details: "The 1960AV 280W 4x12 Angled Cabinet features four Celestion '
      'G12 Vintage speakers"; power handling 280W mono, 140W stereo; impedance 16/4Ω mono, '
      '8Ω stereo.',
      {R('marshall-marshall-1960av', 'driverCount',
         note='Support page states the 4x12 cabinet "features four Celestion G12 Vintage speakers".'),
       R('marshall-marshall-1960av', 'active', 'NOT_STATED')}),

    C('https://www.marshall.com/us/en/product/1936-2x12-cabinet?pid=1007263',
      'Marshall 1936 2x12 cabinet product page (queued URL)',
      'HTTP 404: the listed product URL returns "Page not found" for the 1936 2x12 cabinet, so no '
      'specification text could be read. No field evidence was obtained; values were not changed.',
      {R('marshall-marshall-1936', 'driverCount', 'INACCESSIBLE',
         'Queued product URL returns HTTP 404; no document to read.'),
       R('marshall-marshall-1936', 'active', 'INACCESSIBLE',
         'Queued product URL returns HTTP 404; no document to read.')},
      status='INACCESSIBLE'),

    # ---------------- SVS (subwoofers: built-in amplification) ----------------
    C('https://www.svsound.com/products/pb-1000-pro-subwoofer',
      'SVS PB-1000 Pro subwoofer product page',
      'Product description: "12-inch high-excursion driver, 325-watt RMS amplifier, 20Hz '
      'extension"; dual-port cabinet.',
      {R('svs-pb-1000-pro', 'driverCount',
         note='Description names a single 12-inch high-excursion driver.'),
       R('svs-pb-1000-pro', 'active',
         note='Description states a 325-watt RMS amplifier is built in.')}),

    C('https://www.svsound.com/products/sb16-ultra',
      'SVS SB16-Ultra subwoofer product page',
      'Overview copy: "Massive New 16-inch SVS Ultra Driver with Unprecedented 8-inch Edge Wound '
      'Voice Coil" and "The SB16-Ultra Sledge STA-1500D amplifier’s 64 Amp 200-Volt MOSFETs"; '
      'sealed cabinet.',
      {R('svs-sb16-ultra', 'driverCount',
         note='Overview names a single 16-inch SVS Ultra driver.'),
       R('svs-sb16-ultra', 'active',
         note='Overview describes the built-in Sledge STA-1500D amplifier driving the driver; '
              'self-powered.')},
      chunks=(0, 1), total=9),

    C('https://www.svsound.com/products/sb-1000-pro-subwoofer',
      'SVS SB-1000 Pro subwoofer product page',
      'Product description: "A 12-inch high-excursion driver, 325-watt RMS amplifier, 20Hz '
      'extension"; sealed cabinet.',
      {R('svs-sb-1000-pro', 'driverCount',
         note='Description names a single 12-inch high-excursion driver.'),
       R('svs-sb-1000-pro', 'active',
         note='Description states a 325-watt RMS amplifier is built in.')}),

    C('https://www.svsound.com/products/pb-2000-pro',
      'SVS PB-2000 Pro subwoofer product page',
      'Product description: "Its 12-inch high-excursion driver, 550-watt RMS amplifier, dual-port '
      'cabinet, extension to 16Hz".',
      {R('svs-pb-2000-pro', 'driverCount',
         note='Description names a single 12-inch high-excursion driver.'),
       R('svs-pb-2000-pro', 'active',
         note='Description states a 550-watt RMS amplifier is built in.')}),

    # ---------------- POLK AUDIO ----------------
    C('https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/reserve-r100/300028.html',
      'Polk Reserve R100 bookshelf speaker product page',
      'Product copy and specification list: 1" Pinnacle Ring Radiator tweeter plus one 5¼" '
      'Turbine Cone woofer in a rear X-Port cabinet.',
      {R('polk-audio-reserve-r100', 'driverCount',
         note='Two drive units are stated: 1-inch Pinnacle Ring Radiator tweeter + 5¼-inch '
              'Turbine Cone woofer.')}),

    C('https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/reserve-r200/300029.html',
      'Polk Reserve R200 bookshelf speaker product page',
      'Product copy: "6.5\\" turbine cone woofer" with the Pinnacle Ring Radiator tweeter and a '
      'rear X-Port cabinet.',
      {R('polk-audio-reserve-r200', 'driverCount',
         note='Two drive units are stated: Pinnacle Ring Radiator tweeter + 6.5-inch Turbine '
              'Cone woofer.')}),

    C('https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/signature-elite-es15/300363.html',
      'Polk Signature Elite ES15 bookshelf speaker product page',
      'Product copy: 1" Terylene dome tweeter and a 5.25" Dynamic Balance polypropylene woofer.',
      {R('polk-audio-signature-elite-es15', 'driverCount',
         note='Two drive units are stated: 1-inch Terylene dome tweeter + 5.25-inch Dynamic '
              'Balance woofer.')}),

    C('https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/signature-elite-es20/300364.html',
      'Polk Signature Elite ES20 bookshelf speaker product page',
      'Product bullet list: "6.5\\" Dynamic Balance® polypropylene woofers" and "1\\" Terylene '
      'Dome tweeters"; Power Port cabinet.',
      {R('polk-audio-signature-elite-es20', 'driverCount',
         note='Two drive units are stated: 1-inch Terylene dome tweeter + 6.5-inch Dynamic '
              'Balance woofer.')}),

    C('https://www.polkaudio.com/en-us/product/home-speakers/signature/s60/106513.html',
      'Polk Signature S60 tower product page (queued URL)',
      'The queued archive URL no longer resolves: the page returns the site error message "Sorry, '
      'we\'ve got our wires crossed." (product removed from the current catalogue). No '
      'specification text could be read; values were not changed.',
      {R('polk-signature-s60', 'driverCount', 'INACCESSIBLE',
         'Queued archive URL returns the Polk error page; no document to read.'),
       R('polk-signature-s60', 'active', 'INACCESSIBLE',
         'Queued archive URL returns the Polk error page; no document to read.')},
      status='INACCESSIBLE'),

    # ---------------- KRK ----------------
    C('https://www.krkmusic.com/products/rokit-8-generation-4-powered-studio-monitor-black',
      'KRK ROKIT 8 Generation 4 powered studio monitor product page',
      'Product page: "8\\" Powered Studio Monitor", LF Driver 8", HF Driver 1", 203W total '
      '(bi-amped Class D), front-firing port.',
      {R('krk-rokit-8-g4', 'driverCount',
         note='Two drive units are stated: 8-inch LF driver + 1-inch HF driver.'),
       R('krk-rokit-8-g4', 'active',
         note='Product is a powered monitor with built-in bi-amplification (203W).')}),

    C('https://www.krkmusic.com/products/rokit-10-3-generation-4-powered-studio-monitor',
      'KRK ROKIT 10-3 Generation 4 powered studio monitor product page',
      'Product page: "10\\" 3-way Powered Mid-Field Studio Monitor"; LF Driver 10"; HF Driver '
      '4.5\\" MF and 1\\" HF; matching 10", 4.5" and 1" Kevlar drivers; 300W tri-amp.',
      {R('krk-rokit-10-3-g4', 'driverCount',
         note='Three drive units are stated: 10-inch LF, 4.5-inch MF and 1-inch HF.'),
       R('krk-rokit-10-3-g4', 'active',
         note='Product is a powered tri-amp monitor (300W).')}),

    C('https://www.krkmusic.com/products/v8-series-4-powered-studio-monitor',
      'KRK V8 Series 4 powered studio monitor product page',
      'Specification list: Configuration "2-Way"; System type "Active Studio Monitor"; '
      'Low-Frequency Transducer 8" Kevlar woofer; High-Frequency Transducer 1" Kevlar dome; '
      'LF 200W + HF 30W.',
      {R('krk-v8-s4', 'driverCount',
         note='Specification lists two transducers: 8-inch LF woofer + 1-inch HF tweeter.'),
       R('krk-v8-s4', 'active',
         note='Specification states "System type: Active Studio Monitor" with bi-amped Class D '
              'power (200W LF + 30W HF).')}),

    # ---------------- Q ACOUSTICS ----------------
    C('https://www.qacoustics.com/products/3010i-compact-bookshelf-speaker-pair',
      'Q Acoustics 3010i compact bookshelf speaker product page',
      'Product copy: "Boasting room-filling sound with its 100mm (4 in) and 22mm (0.9 in) '
      'precision drivers".',
      {R('q-acoustics-3010i', 'driverCount',
         note='Copy names exactly two precision drivers: 100 mm (4 in) and 22 mm (0.9 in).')}),

    C('https://www.qacoustics.com/products/3020i-bookshelf-speaker-pair',
      'Q Acoustics 3020i bookshelf speaker product page',
      'Product copy: 22 mm decoupled high-frequency driver together with the mid/bass driver in '
      'a P2P-braced cabinet.',
      {R('q-acoustics-3020i', 'driverCount',
         note='Copy names exactly two drivers: 22 mm decoupled HF driver + mid/bass driver.')}),

    # ---------------- MONITOR AUDIO ----------------
    C('https://www.monitoraudio.com/en/deu/product-ranges/platinum-series-3g/platinum-100-3g/',
      'Monitor Audio Platinum 100 3G product page (specification summary)',
      'Product page: "compact 2-way speaker that features an MPD III transducer and a 6" RDT III '
      'mid-bass driver cone".',
      {R('monitor-audio-platinum-100-3g', 'driverCount',
         note='Two drive units are stated: MPD III transducer + 6-inch RDT III mid-bass driver.')}),

    C('https://www.monitoraudio.com/en/deu/product-ranges/platinum-series-3g/platinum-200-3g/',
      'Monitor Audio Platinum 200 3G product page (specification summary)',
      'Product page: "boasts an MPD III transducer, a 4” RDT III mid-range driver, and twin 6” '
      'RDT III bass drivers" in a three-way floorstander.',
      {R('monitor-audio-platinum-200-3g', 'driverCount',
         note='Four drive units are stated: MPD III transducer + 4-inch mid-range + two 6-inch '
              'bass drivers.')}),

    C('https://www.monitoraudio.com/en/us/product-ranges/creator-series/c1m/',
      'Monitor Audio Creator C1M in-ceiling speaker product page',
      'Feature list: "1 x 1\\" C-CAM tweeter with UD Waveguide | 1 x 7\\" C-CAM mid-bass driver"; '
      'two-way design.',
      {R('monitor-audio-creator-c1m', 'driverCount',
         note='Feature list enumerates exactly two drivers: 1-inch C-CAM tweeter + 7-inch C-CAM '
              'mid-bass driver.')}),

    C('https://www.monitoraudio.com/en/us/product-ranges/creator-series/c2m/',
      'Monitor Audio Creator C2M in-ceiling speaker product page',
      'Feature list: "1 x 1\\" C-CAM tweeter with UD Waveguide II | 1 x 7\\" RST II mid-bass '
      'driver"; two-way design.',
      {R('monitor-audio-creator-c2m', 'driverCount',
         note='Feature list enumerates exactly two drivers: 1-inch C-CAM tweeter + 7-inch RST II '
              'mid-bass driver.')}),

    C('https://www.monitoraudio.com/en/us/product-ranges/creator-series/c3m/',
      'Monitor Audio Creator C3M in-ceiling speaker product page',
      'Feature list: "1 x 1\\" IDC II tweeter with UD Waveguide II | 1 x 7\\" RDT III bass driver '
      '| 1 x 4\\" IDC II midrange driver"; three-way design.',
      {R('monitor-audio-creator-c3m', 'driverCount',
         note='Feature list enumerates exactly three drivers: 1-inch IDC II tweeter + 7-inch RDT '
              'III bass driver + 4-inch IDC II midrange.')}),

    # ---------------- ORANGE ----------------
    C('https://orangeamps.com/en-us/products/ppc108',
      'Orange PPC108 1x8 speaker cabinet product page',
      'Full Specification: "1 x 8″ micro terror/micro dark speaker cabinet"; Speaker "8″ voice '
      'of the world"; power handling 20W; impedance 8 ohms.',
      {R('orange-orange-ppc108', 'driverCount',
         note='Specification states a single 8-inch Voice of the World driver (1x8 cabinet).')}),

    C('https://orangeamps.com/en-us/products/ppc112',
      'Orange PPC112 1x12 speaker cabinet product page',
      'Product copy and specification: "1×12 cabinet" with a single Celestion Vintage 30 '
      'speaker; power handling 60W; impedance 16 ohms.',
      {R('orange-orange-ppc112', 'driverCount',
         note='Specification states one Celestion Vintage 30 12-inch speaker (1x12 cabinet).')}),

    C('https://orangeamps.com/en-us/products/ppc212',
      'Orange PPC212 2x12 speaker cabinet product page',
      'Full Specification: Speakers "2 x 12″ celestion vintage 30"; power handling 120W mono; '
      'impedance 16 ohms.',
      {R('orange-ppc212', 'driverCount',
         note='Specification states two 12-inch Celestion Vintage 30 speakers.')}),

    C('https://orangeamps.com/en-us/products/ppc212v',
      'Orange PPC212V vertical 2x12 speaker cabinet product page',
      'Product copy: "Orange’s first vertical 2×12 cabinet ... With two Celestion Neo Creamback '
      'speakers".',
      {R('orange-ppc212v', 'driverCount',
         note='Copy states two Celestion Neo Creamback 12-inch speakers in a 2×12 cabinet.')}),

    C('https://orangeamps.com/en-us/products/ppc412',
      'Orange PPC412 4x12 speaker cabinet product page',
      'Full Specification: Speakers "4 x Celestion Vintage 30"; power handling 240W mono; '
      'impedance 16 ohms.',
      {R('orange-ppc412', 'driverCount',
         note='Specification states four Celestion Vintage 30 speakers.')}),

    # ---------------- MESA/BOOGIE ----------------
    C('https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/fillmore-series/2x12-fillmore.html',
      'MESA/Boogie Fillmore 2x12 cabinet product page (features and specifications)',
      'Features and Specifications table: Style/Type "Open Back"; Speaker(s) & Mounting Position '
      '"Celestion C90s / Rear Mounted"; Wattage 180 Watts; cabinet impedance 8 Ohm.',
      {R('mesa-boogie-fillmore-2x12', 'driverCount',
         note='2x12 cabinet with two Celestion C90 speakers (180 W total, 90 W each).')}),

    C('https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/lone-star-series/2x12-lone-star.html',
      'MESA/Boogie Lone Star 2x12 cabinet product page (features and specifications)',
      'Features and Specifications table: Speaker(s) "Choice of Celestion C90s (std) or Vintage '
      '30s / Rear Mounted"; Wattage "2 x C90 = 180 Watts (std) / 2 x Vintage 30 = 120 Watts".',
      {R('mesa-boogie-lone-star-2x12', 'driverCount',
         note='Wattage row states the cabinet carries two speakers ("2 x C90" / "2 x Vintage 30").')}),

    C('https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/rectifier-series/2x12-recto-horizontal.html',
      'MESA/Boogie 2x12 Recto Horizontal cabinet product page (features and specifications)',
      'Features and Specifications table: Speaker(s) & Mounting Position "Celestion Vintage 30s / '
      'Rear Mounted"; Wattage 120 Watts; the copy describes it as a sealed 2x12 built from "the '
      'bottom two speakers in a Standard Oversized Rectifier 4x12".',
      {R('mesa-boogie-2x12-rectifier', 'driverCount',
         note='2x12 cabinet with two Celestion Vintage 30 speakers (120 W total, 60 W each).')}),

    C('https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/rectifier-series/4x12-recto-standard-oversized-slant.html',
      'MESA/Boogie 4x12 Recto Standard Oversized Slant cabinet product page (features and '
      'specifications)',
      'Features and Specifications table: Speaker(s) & Mounting Position "Celestion Vintage 30s / '
      'Rear Mounted"; Wattage 240 Watts; the copy calls it an "oversized 4x12" and one of the '
      '"quad boxes" (240 W / 60 W per driver = four drivers).',
      {R('mesa-boogie-rectifier-4x12', 'driverCount',
         note='4x12 "quad box" with four Celestion Vintage 30 speakers (240 W total, 60 W each).')},
      chunks=(0, 1), total=2),

    # ---------------- VOX ----------------
    C('https://voxamps.com/product/v212c-extension-cabinet/',
      'VOX V212C extension cabinet product page',
      'Specifications: Max input power 50W RMS, 8 or 16 ohms; Speaker "2 x 12″ Celestion G12M '
      'Greenback".',
      {R('vox-v212c', 'driverCount',
         note='Specification states two 12-inch Celestion G12M Greenback speakers.')}),

    # ---------------- SONUS FABER ----------------
    C('https://www.sonusfaber.com/en/products/lumina-ii/tech-specs',
      'Sonus faber Lumina II technical specifications page',
      'System: "2-way shelf loudspeaker system. Vented box design". Loudspeakers: Tw Ø 29 mm DAD '
      'driver; Mw Ø 150 mm cone driver. Recommended power amplifier 30W-150W.',
      {R('sonus-faber-lumina-ii', 'driverCount',
         note='Specification lists two drive units: 29 mm DAD tweeter + 150 mm cone midwoofer.'),
       R('sonus-faber-lumina-ii', 'active', 'NOT_STATED')}),

    C('https://www.sonusfaber.com/en/products/lumina-iii/tech-specs',
      'Sonus faber Lumina III technical specifications page',
      'System: "3-way floorstanding loudspeaker system. Vented box design". Loudspeakers: Tw Ø '
      '29 mm DAD driver; Md Ø 150 mm paper cone driver; W Ø 2x150 mm paper cone drivers.',
      {R('sonus-faber-lumina-iii', 'driverCount',
         note='Specification lists four drive units: 29 mm DAD tweeter + 150 mm midrange + two '
              '150 mm woofers.'),
       R('sonus-faber-lumina-iii', 'active', 'NOT_STATED')}),

    C('https://www.sonusfaber.com/it/prodotti/lumina-i/specifiche-tecniche',
      'Sonus faber Lumina I technical specifications page (Italian site)',
      'System: "2-way shelf loudspeaker system. Vented box design". Loudspeakers: Tw Ø 29 mm DAD '
      'driver; Mw Ø 120 mm paper cone driver.',
      {R('sonus-faber-lumina-i', 'driverCount',
         note='Specification lists two drive units: 29 mm DAD tweeter + 120 mm paper cone '
              'midwoofer.'),
       R('sonus-faber-lumina-i', 'active', 'NOT_STATED')}),

    # ---------------- WILSON AUDIO ----------------
    C('https://www.wilsonaudio.com/products/watt-puppy/watt-puppy-series-8',
      'Wilson Audio WATT / Puppy Series 8 technical specifications page',
      'Drivers: Woofers "Two - 8 inch {20.32 cm}"; Midrange "One - 7 inch {17.78 cm}"; Tweeter '
      '"One - 1 inch Inverted titanium dome".',
      {R('wilson-watt-puppy', 'driverCount',
         note='Driver table states two 8-inch woofers + one 7-inch midrange + one 1-inch tweeter.')}),

    # ---------------- REVEL ----------------
    C('https://www.revelspeakers.com/products/in-room-loudspeakers/F206-.html',
      'Revel Performa3 F206 floorstanding loudspeaker product page',
      'General Specifications: Low-frequency Driver Components "Dual 6.5” (16.5 cm) Aluminum Cone, '
      'Cast-frame Woofers"; Mid-frequency "5.25” (13.3 cm) Aluminum Cone, Cast-frame Midrange"; '
      'High-frequency "1” (2.5 cm) Aluminum Tweeter".',
      {R('revel-f206', 'driverCount',
         note='Specification table states two 6.5-inch woofers + one 5.25-inch midrange + one '
              '1-inch tweeter.')}),

    # ---------------- JBL (home audio) ----------------
    C('https://www.jbl.com/HDI-3800.html',
      'JBL HDI-3800 floorstanding loudspeaker product page (specs)',
      'Specification table: High Frequency Transducer "1-inch (25mm) Teonex compression driver"; '
      'Low / Mid Frequency Transducers "Three 8-inch (200mm) ... woofers"; description calls it a '
      '2½-way design with "triple 8-inch" woofers.',
      {R('jbl-hdi-3800', 'driverCount',
         note='Specification table states three 8-inch woofers + one 1-inch compression driver.'),
       R('jbl-hdi-3800', 'active', 'NOT_STATED')}),

    C('https://global.jbl.com/JBLL100CLASSICUAM.html',
      'JBL L100 Classic bookshelf loudspeaker product page (specs)',
      'Feature list and copy: 12-inch (300mm) pure pulp cone woofer (JW300PW-8), 5.25-inch '
      '(130mm) polymer-coated pure-pulp cone midrange driver, 1-inch (25mm) titanium dome '
      'tweeter; 3-way bookshelf loudspeaker.',
      {R('jbl-l100-classic', 'driverCount',
         note='Three drive units are stated: 12-inch woofer + 5.25-inch midrange + 1-inch tweeter.'),
       R('jbl-l100-classic', 'active', 'NOT_STATED')}),

    C('https://global.jbl.com/JBLL82CLASSICORGAM.html',
      'JBL L82 Classic bookshelf loudspeaker product page (specs)',
      'General Specifications: Speaker Type "2-way bookshelf loudspeaker"; Low Frequency Driver '
      '"8\\" (200mm) Pure Pulp cone woofer (JW200PW-6)"; High Frequency Driver "1\\" (25mm) '
      'Titanium dome tweeter (JT025TI1-4)".',
      {R('jbl-l82-classic', 'driverCount',
         note='Specification states two drive units: 8-inch woofer + 1-inch tweeter.'),
       R('jbl-l82-classic', 'active', 'NOT_STATED')}),

    # ---------------- PSB ----------------
    C('https://www.psbspeakers.com/products/synchrony-t600-tower',
      'PSB Synchrony T600 tower loudspeaker product page (specifications)',
      'Specifications: Tweeter "1\\" (25mm) Titanium Dome"; Midrange "5 1/4\\" (133mm) ... Carbon '
      'Fibre Cone"; Woofer "3 x 6 1/2\\" (165mm) ... Carbon Fibre Cone"; Design Type "Transitional '
      '3-way system".',
      {R('psb-synchrony-t600', 'driverCount',
         note='Specification table states one tweeter + one midrange + three 6.5-inch woofers.')},
      chunks=(0, 1), total=3),

    # ---------------- THIRD-PARTY SPECIFICATION SIDEBARS ----------------
    C('https://www.stereophile.com/content/kef-ls50-anniversary-model-loudspeaker-specifications',
      'Stereophile KEF LS50 Anniversary Model loudspeaker specifications sidebar',
      'Specifications: "Two-way, reflex-loaded, stand-mounted loudspeaker. Drive-units: Uni-Q '
      'driver array with 1\\" (25mm) vented aluminum-dome tweeter, 5.25\\" (130mm) '
      'magnesium/aluminum alloy-cone woofer."',
      {R('kef-ls50', 'driverCount', 'SUPPORTED_NOT_PROMOTED', THIRD_PARTY_NOTE),
       R('kef-ls50', 'active', 'NOT_STATED',
         'Sidebar describes a passive stand-mounted loudspeaker but uses no explicit passive/'
         'powered wording; third-party host could not promote in any case.')},
      source_class='NON_MANUFACTURER_HOST'),

    C('https://www.stereophile.com/content/harbeth-super-hl5plus-loudspeaker-specifications',
      'Stereophile Harbeth Super HL5 plus loudspeaker specifications sidebar',
      'Specifications: "Three-way, reflex-loaded, stand-mounted loudspeaker. Drive-units: 0.78\\" '
      '(20mm) titanium-dome and 1\\" (25mm) aluminum-dome tweeters; 7.8\\" (200mm) polymeric '
      'composite-cone mid/woofer."',
      {R('harbeth-shl5', 'driverCount', 'SUPPORTED_NOT_PROMOTED', THIRD_PARTY_NOTE),
       R('harbeth-shl5', 'active', 'NOT_STATED',
         'Sidebar describes a passive stand-mounted loudspeaker but uses no explicit passive/'
         'powered wording; third-party host could not promote in any case.')},
      source_class='NON_MANUFACTURER_HOST'),
]

# No null-value restorations were attempted in Round 23: every field opened this round
# already carried a stored value tied to the checked URL.
STRUCTURAL = []
