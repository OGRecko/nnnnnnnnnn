#!/usr/bin/env python3
"""Round 29 batch 35 data: Bose 802 Series II — distributor-hosted manufacturer manual.

Document: https://www.walkersound.co.uk/PDF/Bose_802_MkII.pdf (Bose technical information sheet, hosted by a
UK distributor; the document is a Bose publication but the host is not Bose, so the third-party tier applies
and never MANUFACTURER_VERIFIED).

Evidence:
  * "Each 802 Series II loudspeaker uses eight 4-1/2" full-range drivers mounted in symmetric vertical pairs"
  * "Recommended amplifier power 240W minimum, 480W maximum"; "Power handling capacity 240W continuous pink
    noise"; connectors are 1/4" phone jacks and XLR; the active equalization is performed by the separate
    802C Series II systems controller (a rack unit with its own AC input), not inside the loudspeaker.
"""
DATE = '2026-10-19'
ROUND = 29
URL = 'https://www.walkersound.co.uk/PDF/Bose_802_MkII.pdf'

PROMOTIONS = [
    {'record': 'bose-802', 'field': 'driverCount', 'value': 8, 'source': URL, 'sourceType': 'THIRD_PARTY',
     'status': 'THIRD_PARTY_VERIFIED',
     'note': ('Round 29 (2026-10-19): Bose 802 Series II technical information (distributor-hosted Bose '
              'document) — "Each 802 Series II loudspeaker uses eight 4-1/2\\" full-range drivers mounted in '
              'symmetric vertical pairs on a faceted Articulated Array baffle assembly."'),
     'notesAppend': ''},
    {'record': 'bose-802', 'field': 'active', 'value': False, 'source': URL, 'sourceType': 'THIRD_PARTY',
     'status': 'THIRD_PARTY_VERIFIED',
     'note': ('Round 29 (2026-10-19): same document — "Recommended amplifier power 240W minimum, 480W '
              'maximum", 240 W continuous pink-noise power handling, 1/4-inch phone and XLR input connectors; '
              'the active equalization is provided by the separate 802C Series II systems controller, not by '
              'the loudspeaker. Passive loudspeaker.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 8 and active false promoted to THIRD_PARTY_VERIFIED '
                     'from the Bose 802 Series II technical sheet hosted at walkersound.co.uk (distributor '
                     'copy; not a manufacturer host).')},
]

URL_RESULTS = [
    {'url': URL, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': ('"Each 802 Series II loudspeaker uses eight 4-1/2" full-range drivers"; "Recommended '
                  'amplifier power 240W minimum, 480W maximum"; 240 W continuous pink noise; phone/XLR '
                  'connectors; active equalization is in the separate 802C Series II controller.'),
     'fieldResults': [
         {'record': 'bose-802', 'field': 'driverCount', 'value': 8, 'outcome': 'PROMOTED',
          'note': 'Round 29: eight full-range drivers; third-party copy of the Bose sheet.'},
         {'record': 'bose-802', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: external amplifier and separate controller; passive loudspeaker.'},
     ]},
]
