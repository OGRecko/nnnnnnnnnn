#!/usr/bin/env python3
"""Round 29 batch 52 (2026-10-19): alternate sources for dead URLs (workstream 5).

The ten INACCESSIBLE URLs in `queue-url-status.json` carry sixteen live fields. This batch replaces the
dead address for six of those records with a document that actually serves the same model:

* KEF's product archive keeps a per-model PDF at `.../1970s/<MODEL>/Reference_Series_<MODEL>_r.pdf`. The
  stored URLs pointed at the bare directory with a truncated filename, which is why they 404'd. The 103 and
  the 105.2 PDFs both print a drive-unit table.
* Polk's current site serves the Signature S60 from its archive section. The dead URL used a retired
  `/106513.html` product id.
* Yamaha's corporate "Innovation Road" collection page describes the 1978 NS-10M itself, not the later
  NS-10M STUDIO revision.
* Marshall's product page answers once the stale `?pid=1007263` tracking parameter is dropped.
* audio-database serves the Paragon D44000 with a per-revision unit table.

Rejected candidates are recorded too, so they are not re-tried:

* The Yamaha NS-10M STUDIO owner's manual (`yamaha.com/.../ns10ms.pdf`) is the STUDIO revision; the record
  is the 1978 NS-10M, so its "18 cm woofer / 3.5 cm soft dome" pair was not used.
* The cieri.net JBL L19 brochure scan (1977) does enumerate "a 200-mm low frequency loudspeaker" and "a
  36-mm high frequency direct radiator", but cieri.net serves no HTTPS endpoint (TLS handshake fails and
  the HTTP copy returns an empty reply to a direct request), so the policy's retained-https-source rule is
  not met. Recorded SUPPORTED_NOT_PROMOTED.
"""
DATE = '2026-10-19'
ROUND = 29

KEF103 = ('https://assets.kef.com/pdf_doc/product-archive/1970s/'
          'REFERENCE+SERIES+MODEL+103+(1976-77)/Reference_Series_Model_103_r.pdf')
KEF105 = ('https://assets.kef.com/pdf_doc/product-archive/1970s/'
          'REFERENCE+SERIES+MODEL+105.2+(1979-87)/Reference_Series_Model_105_2_r.pdf')
POLK = ('https://www.polkaudio.com/en-us/product/archive/archive-floor-standing-speakers/'
        'signature-s60/112702.html')
YAMAHA = 'https://www.yamaha.com/en/about/experience/innovation-road/collection/detail/7008/'
MARSHALL = 'https://www.marshall.com/us/en/product/1936-2x12-cabinet'
PARAGON = 'https://audio-database.com/JBL/speaker/paragon.html'
DALI = 'https://www.dali-speakers.com/en/products/discontinued/oberon/oberon-1/'

PROMOTIONS = [
    {'record': 'legacy-kef-3', 'field': 'driverCount', 'value': 2, 'source': KEF103,
     'tier': 'MANUFACTURER',
     'note': ('Round 29 (2026-10-19): KEF product archive sheet "REFERENCE SERIES MODEL 103 (1976-77)" — '
              '"An 8 inch two way closed box design, it used the same low distortion B200 bass driver as the '
              'Model 104 with the new T52 tweeter"; drive-unit table "Drive units | B200 bass unit (SP1039), '
              'T52 tweeter (SP1049)". Two transducers.'),
     'fieldNote': 'Round 29: KEF archive sheet lists B200 bass unit (SP1039) and T52 tweeter (SP1049).',
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the KEF archive sheet for the exact '
                'model, which prints "Drive units | B200 bass unit (SP1039), T52 tweeter (SP1049)".')},
    {'record': 'kef-105', 'field': 'driverCount', 'value': 3, 'source': KEF105,
     'tier': 'MANUFACTURER',
     'note': ('Round 29 (2026-10-19): KEF product archive sheet "REFERENCE SERIES MODEL 105.2 (1979-87)" — '
              '"Three-way, floor standing"; drive-unit rows "Drive units | B300 bass unit (SPI071), B110 '
              'midrange unit (SPI057), T52 tweeter (SPI049)" repeated for each serial-number break (SPI072 '
              'tweeter from SN 2966). Three transducers in every revision listed.'),
     'fieldNote': 'Round 29: KEF archive sheet lists B300 bass, B110 midrange and T52 tweeter.',
     'append': (' Round 29 (2026-10-19): driverCount 3 verified from the KEF archive sheet for the exact '
                'model; every serial-number break lists the same three units.')},
    {'record': 'polk-signature-s60', 'field': 'driverCount', 'value': 4, 'source': POLK,
     'tier': 'MANUFACTURER',
     'note': ('Round 29 (2026-10-19): Polk Audio archive page for the Signature S60 — "Front Array Driver '
              'Complement • (3) 6.5\" (16.51 cm) d (Round) - Mid/Woofer • (1) 1\" (2.54 cm) d (Round) - '
              'Tweeter". Three mid/woofers plus one tweeter.'),
     'fieldNote': 'Round 29: Polk archive page lists three 6.5-inch mid/woofers and one 1-inch tweeter.',
     'append': (' Round 29 (2026-10-19): driverCount 4 verified from the Polk Audio archive page for the '
                'exact model ("(3) 6.5\" ... Mid/Woofer" and "(1) 1\" ... Tweeter").')},
    {'record': 'legacy-yam-2', 'field': 'driverCount', 'value': 2, 'source': YAMAHA,
     'tier': 'MANUFACTURER',
     'note': ('Round 29 (2026-10-19): Yamaha corporate "Innovation Road" collection entry headed "NS-10M / '
              'Speaker System／1978" — "The two-way construction features an 18-cm white cone woofer and '
              '3.5-cm soft dome tweeter, along with an encapsulated enclosure." Two transducers, and the '
              'year identifies this page as the 1978 NS-10M rather than the later NS-10M STUDIO.'),
     'fieldNote': 'Round 29: Yamaha NS-10M (1978) page lists an 18-cm cone woofer and a 3.5-cm soft dome.',
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from Yamaha\'s own 1978 NS-10M entry '
                '("18-cm white cone woofer and 3.5-cm soft dome tweeter").')},
    {'record': 'marshall-marshall-1936', 'field': 'driverCount', 'value': 2, 'source': MARSHALL,
     'tier': 'MANUFACTURER',
     'note': ('Round 29 (2026-10-19): Marshall 1936 2x12 cabinet product page — "Two 12\" Celestion G12T-75 '
              'speakers" and the specification block "Speaker configuration | 2x12\"". Two transducers. The '
              'recorded URL with "?pid=1007263" returns the site 404; the page itself answers without the '
              'stale tracking parameter.'),
     'fieldNote': 'Round 29: Marshall page states two 12-inch Celestion G12T-75 speakers.',
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the Marshall 1936 page; the earlier '
                'INACCESSIBLE result came from a stale "?pid=" parameter, not from a missing page.')},
    {'record': 'jbl-paragon', 'field': 'driverCount', 'value': 6, 'source': PARAGON,
     'tier': 'REPUTABLE_DATABASE',
     'note': ('Round 29 (2026-10-19): audio-database JBL Paragon (D44000 / D44000WXA) entry — "Method | '
              'Integrated stereo speaker system, 3-way, 6-speaker, front loading horn system, floor type", '
              'with a per-revision unit table giving 2x bass, 2x midrange ("375 + H5038P") and 2x high '
              '("075") in the initial and medium-term D44000 and 2x bass, 2x "376 + H5038P" and 2x "075" in '
              'the D44000WXA. The complement is six in every revision the page lists, so the revision '
              'difference does not affect the count.'),
     'fieldNote': 'Round 29: audio-database lists a 6-speaker 3-way system, 2+2+2 in every revision.',
     'append': (' Round 29 (2026-10-19): driverCount 6 verified from the audio-database Paragon entry, '
                'which states a 6-speaker system and lists two bass, two midrange and two high units in '
                'each revision.')},
]

# Outcomes that deliberately write nothing to speakers.json.
NOT_PROMOTED = [
    {'record': 'jbl-l19', 'field': 'driverCount', 'value': 2, 'outcome': 'SUPPORTED_NOT_PROMOTED',
     'source': ('http://www.cieri.net/Documenti/JBL/Documenti%20tecnici/Cataloghi/'
                'JBL%20-%20L19%20-%20Depliant%20(1977)%20(English).pdf'),
     'note': ('Round 29 (2026-10-19): the 1977 JBL L19 brochure scan on cieri.net enumerates "a 200-mm low '
              'frequency loudspeaker, a 36-mm high frequency direct radiator", i.e. two transducers, but '
              'cieri.net offers no HTTPS endpoint (TLS handshake fails; the HTTP copy returns an empty '
              'reply), so the retained-https rule is unmet and the value stays CITED.')},
    {'record': 'kef-105', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED', 'source': KEF105,
     'note': ('Round 29 (2026-10-19): the KEF 105.2 sheet gives "Amplifier Requirements | 40-200 watts per '
              'channel into 8 ohms" and "Rated maximum power | 200W programme"; amplifier-requirement '
              'figures are excluded evidence, and the sheet never calls the system passive.')},
    {'record': 'legacy-kef-3', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED', 'source': KEF103,
     'note': ('Round 29 (2026-10-19): the KEF 103 sheet gives "Amplifier Requirements | 25-100 watts per '
              'channel into 8 ohms" and the prose "Model 103 will handle the output from 100 watt '
              'amplifiers on musical programme"; power-handling wording is excluded evidence, so active '
              'stays unresolved.')},
    {'record': 'dali-oberon-1', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED', 'source': DALI,
     'note': ('Round 29 (2026-10-19): the DALI OBERON 1 page rows "Recommended Amp. Power [watts] 25 - 100" '
              'and "Connection Input | Single Wire", both excluded evidence; the page never calls the '
              'loudspeaker passive.')},
]

URL_RESULTS = [
    {'url': KEF103, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'sourceClass': 'MANUFACTURER', 'document': 'KEF Reference Series Model 103 (1976-77) archive sheet',
     'evidence': ('"An 8 inch two way closed box design, it used the same low distortion B200 bass driver as '
                  'the Model 104 with the new T52 tweeter"; "Drive units | B200 bass unit (SP1039), T52 '
                  'tweeter (SP1049)"; "Amplifier Requirements | 25-100 watts per channel into 8 ohms".'),
     'fieldResults': ['legacy-kef-3']},
    {'url': KEF105, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'sourceClass': 'MANUFACTURER', 'document': 'KEF Reference Series Model 105.2 (1979-87) archive sheet',
     'evidence': ('"Three-way, floor standing"; "Drive units | B300 bass unit (SPI071), B110 midrange unit '
                  '(SPI057), T52 tweeter (SPI049)"; "Amplifier Requirements | 40-200 watts per channel into '
                  '8 ohms".'),
     'fieldResults': ['kef-105']},
    {'url': POLK, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'sourceClass': 'MANUFACTURER', 'document': 'Polk Audio Signature S60 archived product page',
     'evidence': ('"Front Array Driver Complement • (3) 6.5\" (16.51 cm) d (Round) - Mid/Woofer • (1) 1\" '
                  '(2.54 cm) d (Round) - Tweeter"; "Recommended Amplifier Power Per Channel 20 watts → 300 '
                  'watts"; "(2) Pair of Dual 5-way Binding Posts".'),
     'fieldResults': ['polk-signature-s60']},
    {'url': YAMAHA, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'sourceClass': 'MANUFACTURER',
     'document': 'Yamaha Innovation Road display collection, NS-10M (1978)',
     'evidence': ('Page heading "NS-10M / Speaker System／1978"; "The two-way construction features an 18-cm '
                  'white cone woofer and 3.5-cm soft dome tweeter, along with an encapsulated enclosure."'),
     'fieldResults': ['legacy-yam-2']},
    {'url': MARSHALL, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'sourceClass': 'MANUFACTURER', 'document': 'Marshall 1936 2x12 Cabinet product page',
     'evidence': ('"Two 12\" Celestion G12T-75 speakers"; "Speaker configuration | 2x12\""; "power handling '
                  '| 150W MONO, 75W STEREO"; "Unit impedance | 8Ω Mono, 16Ω Stereo".'),
     'fieldResults': ['marshall-marshall-1936']},
    {'url': PARAGON, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'sourceClass': 'NON_MANUFACTURER_HOST',
     'document': 'audio-database JBL Paragon (D44000 / D44000WXA) entry',
     'evidence': ('"Method | Integrated stereo speaker system, 3-way, 6-speaker, front loading horn system, '
                  'floor type"; unit table per revision: "For low band : 38 cm cone type (150-4C) x2", "For '
                  'Medium Range : Horn Type (375 + H5038P) x2", "For High Pass : Horn Type (075) x2".'),
     'fieldResults': ['jbl-paragon']},
    {'url': DALI, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0, 1], 'chunksTotal': 3,
     'sourceClass': 'MANUFACTURER',
     'document': 'DALI OBERON 1 product page (discontinued section)',
     'evidence': ('"High Frequency Driver(s) | 1 x 29 mm soft dome"; "Low/Mid Frequency Driver(s) | 1 x 5¼ '
                  'inch"; "Recommended Amp. Power [watts] 25 - 100"; "Connection Input | Single Wire". No '
                  'passive/powered wording.'),
     'fieldResults': ['dali-oberon-1']},
]

HOSTS = {u: u.split('/')[2] for u in (KEF103, KEF105, POLK, YAMAHA, MARSHALL, PARAGON, DALI)}
