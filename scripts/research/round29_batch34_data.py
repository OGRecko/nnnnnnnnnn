#!/usr/bin/env python3
"""Round 29 batch 34 data: legacy-jbl-6 (duplicate 4430 record) active promotion; queue-row corrections.

legacy-jbl-6 is the archived-id duplicate of jbl-4430 that lives in speakers.json (the inventory used to
double-count it as ARCHIVED). Its note says it is synchronized with jbl-4430 from the same combined JBL
4430/4435 page, so the passive evidence on that page applies and `active` false is promoted.

Queue corrections:
  * 4430/4435 URL: legacy-jbl-6 rows become PROMOTED (active) or are dropped (driverCount already MV).
  * KEF Model 103 URL: legacy-kef-3 is a live record; its rows were mislabelled RECORD_ARCHIVED and are
    corrected to INACCESSIBLE (the archive PDF is still a redirect stub).
"""
DATE = '2026-10-19'
ROUND = 29
JBL_4430 = 'https://jblpro.com/en-US/site_elements/4430-and-4435-information'
KEF_103 = ('https://assets.kef.com/pdf_doc/product-archive/1970s/'
           'REFERENCE+SERIES+MODEL+103+(1976-77).pdf')

PROMOTIONS = [
    {'record': 'legacy-jbl-6', 'field': 'active', 'value': False, 'source': JBL_4430,
     'note': ('Round 29 (2026-10-19): duplicate record of the JBL 4430; the combined 4430/4435 page '
              'specifies an internal frequency dividing network at 1 kHz, single-amplification power input '
              'and an optional biamp switch, so the system is passive.'),
     'notesAppend': (' Round 29 (2026-10-19): active false promoted from the same combined 4430/4435 page '
                     '(single amplification through the internal dividing network).')},
]

URL_RESULTS = [
    {'url': JBL_4430, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 3,
     'evidence': ('JBL 4430/4435: passive frequency dividing network (1 kHz), single-amplification power '
                  'input 300 W (4430) / 375 W (4435), optional biamp switch; 4430 uses one 15 in LF driver '
                  'plus the Bi-Radial compression driver.'),
     'fieldResults': [
         {'record': 'legacy-jbl-6', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: same passive evidence as jbl-4430; duplicate record synchronized.'},
     ],
     'dropRows': [['legacy-jbl-6', 'driverCount']]},
    {'url': KEF_103, 'status': 'INACCESSIBLE', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('KEF archive PDF answers with "redirecting to kef.com" and serves no document.'),
     'fieldResults': [
         {'record': 'legacy-kef-3', 'field': 'driverCount', 'value': 2, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: redirect stub, no datasheet.'},
         {'record': 'legacy-kef-3', 'field': 'active', 'value': False, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: redirect stub, no datasheet.'},
     ]},
]
