#!/usr/bin/env python3
"""Round 29 batch 44 (2026-10-19): two manufacturer PDFs served by distributors/retailers.

  lacoustics-arcs — L-Acoustics ARCS WIDE product information sheet, version 5.0 (03/17), hosted whole by
    ProMusic: "The ARCS WIDE loudspeaker enclosure is based on a 2-way passive design with a nominal
    impedance of 8 ohms"; "Transducers LF: 1 × 12\", weather-resistant, bass-reflex HF: 1 × 3\", diaphragm
    compression driver, DOSC waveguide"; and "The ARCS WIDE is driven and amplified by the LA4X or the LA8
    controller". Two transducers, passive enclosure with external amplification.

  nexo-ps15 — NEXO PS Series brochure (v1.3) PS15 pages, hosted by Full Compass: "one 15\" 6Ω cone
    transducer and a 2\"-exit compression driver" (architect spec), "Connectors 3x NL4MP 4-pole SPEAKON;
    Passive In Passive Loop Thru, Active In", "Crossover Frequencies 900Hz Passive or Active (internally
    switchable)", "Nominal Impedance Passive 8 Ω Active; LF 6 Ω, HF 8 Ω", and "Recommended Amplifiers 550
    to 1200Watts into 8 Ωs for 1x PS15". Two transducers; the recommended external amplifier and the
    passive input connector are the accepted passive evidence (bi-amp-capable designs are still passive).
"""
DATE = '2026-10-19'
ROUND = 29

ARCS = 'https://www.promusic.cz/sites/default/files/product/field_files/arcswide_sp_en_5.0.pdf'
PS15 = 'https://www.fullcompass.com/common/files/9194-PSSeriesBrochure.pdf'

ARCS_WHY = ('The PDF is the manufacturer-published ARCS WIDE sheet but it is served by promusic.cz, a '
            'distributor, not by an L-Acoustics host.')
PS15_WHY = ('The brochure is NEXO-authored but is served by fullcompass.com, a retailer, not by a NEXO host.')

PROMOTIONS = [
    {'record': 'lacoustics-arcs', 'field': 'driverCount', 'value': 2, 'source': ARCS,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'L-Acoustics ARCS WIDE product information sheet, ARCSWIDE_SP_EN_5.0 (03/17)',
     'whyNotManufacturer': ARCS_WHY,
     'note': ('Round 29 (2026-10-19): ARCS WIDE sheet — "Transducers LF: 1 × 12\\", weather-resistant, '
              'bass-reflex HF: 1 × 3\\", diaphragm compression driver, DOSC waveguide". One LF transducer '
              'plus one HF compression driver.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the ARCS WIDE '
                     'sheet ("2-way passive design", "driven and amplified by the LA4X or the LA8 '
                     'controller").')},
    {'record': 'lacoustics-arcs', 'field': 'active', 'value': False, 'source': ARCS,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'L-Acoustics ARCS WIDE product information sheet, ARCSWIDE_SP_EN_5.0 (03/17)',
     'whyNotManufacturer': ARCS_WHY,
     'note': ('Round 29 (2026-10-19): same sheet — "The ARCS WIDE loudspeaker enclosure is based on a 2-way '
              'passive design with a nominal impedance of 8 ohms"; "The ARCS WIDE is driven and amplified by '
              'the LA4X or the LA8 controller". Explicit passive wording with external amplification.'),
     'notesAppend': ''},
    {'record': 'nexo-ps15', 'field': 'driverCount', 'value': 2, 'source': PS15,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'NEXO PS Series brochure v1.3, PS15 loudspeaker and architect/engineering pages',
     'whyNotManufacturer': PS15_WHY,
     'note': ('Round 29 (2026-10-19): NEXO PS15 brochure — architect spec: "The 2-way full range loudspeaker '
              'system shall have one 15\\" 6Ω cone transducer and a 2\\"-exit compression driver"; product '
              'features list "LF 1x 15\\" (38cm) 6 Ω driver HF 1x 2\\" throat, 3\\" titanium diaphragm". Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the NEXO PS15 '
                     'brochure pages ("Passive In Passive Loop Thru, Active In", "Recommended Amplifiers 550 '
                     'to 1200Watts into 8 Ωs for 1x PS15").')},
    {'record': 'nexo-ps15', 'field': 'active', 'value': False, 'source': PS15,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'NEXO PS Series brochure v1.3, PS15 loudspeaker and architect/engineering pages',
     'whyNotManufacturer': PS15_WHY,
     'note': ('Round 29 (2026-10-19): same brochure — "Connectors 3x NL4MP 4-pole SPEAKON; Passive In Passive '
              'Loop Thru, Active In"; "Crossover Frequencies 900Hz Passive or Active (internally '
              'switchable)"; "Recommended Amplifiers 550 to 1200Watts into 8 Ωs for 1x PS15". Passive '
              'enclosure driven by external amplifiers; the active mode is bi-amplification, not an internal '
              'amplifier.'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': ARCS, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('"based on a 2-way passive design with a nominal impedance of 8 ohms"; "Transducers LF: 1 × '
                  '12\\" ... HF: 1 × 3\\" ... compression driver"; "driven and amplified by the LA4X or the '
                  'LA8 controller".'),
     'fieldResults': [
         {'record': 'lacoustics-arcs', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: 1 × 12 in LF + 1 × 3 in HF.'},
         {'record': 'lacoustics-arcs', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: "2-way passive design"; amplified by external LA4X/LA8.'},
     ]},
    {'url': PS15, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0, 10], 'chunksTotal': 14,
     'evidence': ('"one 15\\" 6Ω cone transducer and a 2\\"-exit compression driver"; "Passive In Passive '
                  'Loop Thru, Active In"; "Passive 8 Ω"; "Recommended Amplifiers 550 to 1200Watts into 8 Ωs".'),
     'fieldResults': [
         {'record': 'nexo-ps15', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: 15 in LF + 2 in exit HF.'},
         {'record': 'nexo-ps15', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: passive input connector and recommended external amplifier.'},
     ]},
]
