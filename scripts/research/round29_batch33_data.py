#!/usr/bin/env python3
"""Round 29 batch 33 data (2026-10-19): JBL 4430/4435 manufacturer document; KEF archive retry.

JBL 4430/4435 (jblpro.com, manufacturer host):
  * "The frequency dividing network of the Bi-Radial monitors has a crossover frequency of 1 kHz ..."
  * "Maximum Power Input / Single Amplification / Continuous Program: 300 W (4430), 375 W (4435)"
  * "A switch located adjacent to the connection terminals allows the monitor to be biamplified."
  * "Recommended Amplifier Power ..."
  A dividing network inside the cabinet, single amplification from an external amplifier and an optional
  biamp switch = passive loudspeaker. jbl-4430.active false is therefore promoted to MANUFACTURER_VERIFIED.

KEF archive PDFs (assets.kef.com): both URLs answer with "redirecting to kef.com" and no document, so the
KEF 105 and 103 fields stay unresolved (INACCESSIBLE).

legacy-jbl-6 and legacy-kef-3 are archived; their rows are marked RECORD_ARCHIVED.
"""
DATE = '2026-10-19'
ROUND = 29
JBL_4430 = 'https://jblpro.com/en-US/site_elements/4430-and-4435-information'
KEF_105 = ('https://assets.kef.com/pdf_doc/product-archive/1970s/'
           'REFERENCE+SERIES+MODEL+105.2+(1979-87).pdf')
KEF_103 = ('https://assets.kef.com/pdf_doc/product-archive/1970s/'
           'REFERENCE+SERIES+MODEL+103+(1976-77).pdf')

PROMOTION = {
    'record': 'jbl-4430', 'field': 'active', 'value': False, 'source': JBL_4430,
    'note': ('Round 29 (2026-10-19): JBL 4430/4435 information — "The frequency dividing network of the '
             'Bi-Radial monitors has a crossover frequency of 1 kHz"; "Maximum Power Input / Single '
             'Amplification / Continuous Program: 300 W"; "Recommended Amplifier Power"; "A switch located '
             'adjacent to the connection terminals allows the monitor to be biamplified." A passive '
             'dividing network driven by an external amplifier.'),
    'notesAppend': (' Round 29 (2026-10-19): active false promoted from the JBL 4430/4435 information page '
                    '(single amplification through the internal 1 kHz frequency dividing network; biamp '
                    'switch optional).'),
}

URL_RESULTS = [
    {'url': JBL_4430, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('JBL 4430/4435: "single 380 mm (15 in) low frequency driver" plus Bi-Radial compression '
                  'driver (4430 = 2 transducers); "The frequency dividing network ... has a crossover '
                  'frequency of 1 kHz"; "Maximum Power Input / Single Amplification / Continuous Program: '
                  '300 W (4430), 375 W (4435)"; "Recommended Amplifier Power"; optional biamp switch.'),
     'fieldResults': [
         {'record': 'jbl-4430', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: passive system established by the dividing network and single-amplification power input.'},
         {'record': 'legacy-jbl-6', 'field': 'active', 'value': False, 'outcome': 'RECORD_ARCHIVED',
          'note': 'Round 29 (2026-10-19): record retired; nothing can be written.'},
         {'record': 'legacy-jbl-6', 'field': 'driverCount', 'value': None, 'outcome': 'RECORD_ARCHIVED',
          'note': 'Round 29 (2026-10-19): record retired; nothing can be written.'},
     ]},
    {'url': KEF_105, 'status': 'INACCESSIBLE', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('The archive PDF answers with "redirecting to kef.com" and no content; the product '
                  'archive document is still not served.'),
     'fieldResults': [
         {'record': 'kef-105', 'field': 'driverCount', 'value': 3, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: redirect stub, no datasheet.'},
         {'record': 'kef-105', 'field': 'active', 'value': False, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: redirect stub, no datasheet.'},
     ]},
    {'url': KEF_103, 'status': 'INACCESSIBLE', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': 'Same KEF archive redirect stub; no document.',
     'fieldResults': [
         {'record': 'legacy-kef-3', 'field': 'driverCount', 'value': 2, 'outcome': 'RECORD_ARCHIVED',
          'note': 'Record retired; the URL is also inaccessible.'},
         {'record': 'legacy-kef-3', 'field': 'active', 'value': False, 'outcome': 'RECORD_ARCHIVED',
          'note': 'Record retired; the URL is also inaccessible.'},
     ]},
]
