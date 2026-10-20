#!/usr/bin/env python3
"""Round 29 batch 39 (2026-10-19): Audio Database specification entries.

All four pages enumerate the drive units; none states passive/active, and "allowable input" is a
power-handling rating, which the policy excludes as evidence for `active`. So `driverCount` is promoted and
`active` is recorded NOT_STATED in the queue, leaving the stored value untouched.

  JBL 4312  — "Method: 3-Way, 3-Speaker, Bass reflex system, Bookshelf Type"; units 2213H, LE5-12, LE25-2.
  JBL L16   — "Method: 2-Way, 2-Speaker, Bass Reflex System, Bookshelf Type"; 116A and LE25-2.
  JBL D130  — "Type: 38 cm cone type full range unit" (a single raw drive unit).
  KEF 104   — "Method: 2-way, 2-speaker, passive radiator system, bookshelf type"; B200/SP1039 and
              T27/SP1032 (the BD139/SP1037 passive radiator is not a driven unit).
"""
DATE = '2026-10-19'
ROUND = 29

AD = 'https://audio-database.com'

PROMOTIONS = [
    {'record': 'jbl-4312', 'field': 'driverCount', 'value': 3, 'source': AD + '/JBL/speaker/4312-e.html',
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — JBL 4312 specification entry',
     'whyNotManufacturer': ('audio-database.com is a specification archive; no JBL-hosted 4312 datasheet '
                            'was opened in this session.'),
     'note': ('Round 29 (2026-10-19): Audio Database JBL 4312 entry — "Method: 3-Way, 3-Speaker, Bass '
              'reflex system, Bookshelf Type"; units: 30 cm cone (2213H), 13 cm cone (LE5-12), 3.6 cm cone '
              '(LE25-2). Three transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 verified against the Audio Database 4312 entry; '
                     'active stays unresolved because the page gives only "Allowable input 80W (continuous '
                     'program)", which the policy excludes as evidence.')},
    {'record': 'jbl-l16', 'field': 'driverCount', 'value': 2, 'source': AD + '/JBL/speaker/l16decade-e.html',
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — JBL L16 Decade specification entry',
     'whyNotManufacturer': ('audio-database.com is a specification archive; no JBL-hosted L16 datasheet was '
                            'opened in this session.'),
     'note': ('Round 29 (2026-10-19): Audio Database JBL L16 Decade entry — "Method: 2-Way, 2-Speaker, Bass '
              'Reflex System, Bookshelf Type"; units: 20 cm cone (116A), 5 cm cone (LE25-2). Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified against the Audio Database L16 entry; '
                     'active stays unresolved (only an "Allowable input 35W" figure is given).')},
    {'record': 'legacy-jbl-1', 'field': 'driverCount', 'value': 1, 'source': AD + '/JBL/unit/d130.html',
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — JBL D130 specification entry',
     'whyNotManufacturer': ('audio-database.com is a specification archive; no JBL-hosted D130 sheet was '
                            'opened in this session.'),
     'note': ('Round 29 (2026-10-19): Audio Database JBL D130 entry — "Type: 38 cm cone type full range '
              'unit"; voice coil 10.2 cm. A single transducer.'), 
     'notesAppend': (' Round 29 (2026-10-19): driverCount 1 verified against the Audio Database D130 entry '
                     '(a single 38 cm full-range unit); active stays unresolved because "product category" '
                     'is not accepted as evidence.')},
    {'record': 'legacy-kef-2', 'field': 'driverCount', 'value': 2, 'source': AD + '/KEF/speaker/model104.html',
     'sourceType': 'REPUTABLE_DATABASE', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Audio Database — KEF Model 104 specification entry',
     'whyNotManufacturer': ('audio-database.com is a specification archive; the KEF archive PDFs are '
                            'redirect stubs and no KEF-hosted Model 104 sheet was opened.'),
     'note': ('Round 29 (2026-10-19): Audio Database KEF Model 104 entry — "Method: 2-way, 2-speaker, '
              'passive radiator system, bookshelf type"; units: 20 cm cone (B200/SP1039) and dome '
              '(T27/SP1032); the BD139/SP1037 passive radiator is not a driven unit. Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified against the Audio Database Model 104 '
                     'entry; active stays unresolved ("passive radiator" describes the cabinet loading, not '
                     'the amplification).')},
]

URL_RESULTS = [
    {'url': AD + '/JBL/speaker/4312-e.html', 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0],
     'chunksTotal': 1,
     'evidence': ('"Method: 3-Way, 3-Speaker, Bass reflex system, Bookshelf Type"; 2213H / LE5-12 / LE25-2; '
                  '"Allowable input 80W (continuous program)"; no passive/active statement.'),
     'fieldResults': [
         {'record': 'jbl-4312', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: three enumerated units.'},
         {'record': 'jbl-4312', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: power-handling rating only; policy excludes it as passive evidence.'},
     ]},
    {'url': AD + '/JBL/speaker/l16decade-e.html', 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0],
     'chunksTotal': 1,
     'evidence': ('"Method: 2-Way, 2-Speaker, Bass Reflex System, Bookshelf Type"; 116A / LE25-2; '
                  '"Allowable input 35W (continuous program)".'),
     'fieldResults': [
         {'record': 'jbl-l16', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two enumerated units.'},
         {'record': 'jbl-l16', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: no passive/active statement.'},
     ]},
    {'url': AD + '/JBL/unit/d130.html', 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('"Type: 38 cm cone type full range unit"; 8/16 ohm; 60 W continuous program; no '
                  'passive/active statement.'),
     'fieldResults': [
         {'record': 'legacy-jbl-1', 'field': 'driverCount', 'value': 1, 'outcome': 'PROMOTED',
          'note': 'Round 29: a single drive unit.'},
         {'record': 'legacy-jbl-1', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: product category is not accepted as evidence.'},
     ]},
    {'url': AD + '/KEF/speaker/model104.html', 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0],
     'chunksTotal': 1,
     'evidence': ('"Method: 2-way, 2-speaker, passive radiator system, bookshelf type"; B200/SP1039, '
                  'T27/SP1032, BD139/SP1037 passive radiator; maximum allowable input 50 W music power.'),
     'fieldResults': [
         {'record': 'legacy-kef-2', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two driven units; the passive radiator is not driven.'},
         {'record': 'legacy-kef-2', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: "passive radiator" is not a passive-amplification statement.'},
     ]},
]
