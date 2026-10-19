#!/usr/bin/env python3
"""Round 29 batch 38 (2026-10-19): KEF LS50 specification page (Stereophile), Polk S60 retry, ELAC active.

KEF LS50 Anniversary — Stereophile specification sidebar:
  "Two-way, reflex-loaded, stand-mounted loudspeaker. Drive-units: Uni-Q driver array with 1" (25mm)
   vented aluminum-dome tweeter, 5.25" (130mm) magnesium/aluminum alloy-cone woofer."
  Two transducers. The same page gives only "Amplifier requirements: 25-100W" for amplification and never
  says passive or powered, so `active` stays unresolved (NOT_STATED).

Polk Signature S60 — the polkaudio.com product URL renders "Sorry, we've got our wires crossed." again; no
specification text. Both fields INACCESSIBLE.

ELAC Uni-Fi UB5 — the sell sheet gives "3-way bass reflex" and the driver sizes but no passive/active
statement; `active` is NOT_STATED (the driverCount conflict from batch 30 stands).
"""
DATE = '2026-10-19'
ROUND = 29

STEREO_LS50 = ('https://www.stereophile.com/content/'
               'kef-ls50-anniversary-model-loudspeaker-specifications')
POLK_S60 = 'https://www.polkaudio.com/en-us/product/home-speakers/signature/s60/106513.html'
ELAC_UB5 = 'https://cdn.elac.com/uploads/2016/08/29132944/Uni-Fi-Sell-Sheet.pdf'

PROMOTIONS = [
    {'record': 'kef-ls50', 'field': 'driverCount', 'value': 2, 'source': STEREO_LS50,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'Stereophile, "KEF LS50 Anniversary Model loudspeaker Specifications" sidebar',
     'whyNotManufacturer': ('stereophile.com is a magazine; no KEF-hosted LS50 specification page was served '
                            'in this session (the KEF archive PDFs are redirect stubs).'),
     'note': ('Round 29 (2026-10-19): Stereophile LS50 specifications — "Two-way, reflex-loaded, '
              'stand-mounted loudspeaker. Drive-units: Uni-Q driver array with 1\\" (25mm) vented '
              'aluminum-dome tweeter, 5.25\\" (130mm) magnesium/aluminum alloy-cone woofer." Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 verified against the Stereophile LS50 '
                     'specification sidebar; active remains unresolved (the page gives only amplifier '
                     'requirements).')},
]

URL_RESULTS = [
    {'url': STEREO_LS50, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('Stereophile LS50 sidebar: "Two-way, reflex-loaded, stand-mounted loudspeaker"; 1" vented '
                  'aluminium-dome tweeter plus 5.25" alloy-cone woofer; "Amplifier requirements: 25-100W"; '
                  'no passive/active statement.'),
     'fieldResults': [
         {'record': 'kef-ls50', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two named drive units; third-party magazine specification.'},
         {'record': 'kef-ls50', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: only "Amplifier requirements: 25-100W" is printed; no passive/powered wording.'},
     ]},
    {'url': POLK_S60, 'status': 'INACCESSIBLE', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('polkaudio.com product page renders "Sorry, we\'ve got our wires crossed." and no '
                  'specification text.'),
     'fieldResults': [
         {'record': 'polk-signature-s60', 'field': 'driverCount', 'value': 4, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: dead product page.'},
         {'record': 'polk-signature-s60', 'field': 'active', 'value': False, 'outcome': 'INACCESSIBLE',
          'note': 'Round 29 retry: dead product page.'},
     ]},
    {'url': ELAC_UB5, 'status': 'CHECKED_PARTIAL', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('ELAC Uni-Fi sell sheet: "3-way bass reflex"; 1 in soft-dome tweeter, 4 in aluminium '
                  'midrange, 5.25 in aluminium woofer (tweeter and midrange concentric). No passive/active '
                  'statement; driver count remains ambiguous.'),
     'fieldResults': [
         {'record': 'elac-uni-fi-ub5', 'field': 'active', 'value': False, 'outcome': 'NOT_STATED',
          'note': 'Round 29: no passive/powered wording on the sell sheet.'},
     ]},
]
