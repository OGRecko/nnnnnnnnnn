#!/usr/bin/env python3
"""Round 29 batch 37 (2026-10-19): KRK documents on a Shopify CDN (third-party host).

1. KRK Model 7000B/BS spec sheet.
   "The components are comprised of a 7-inch Kevlar woofer and a 1-inch Kevlar dome tweeter."
   "Crossover: Passive 2-way"; "The system is crossed over at 3 kHz with a proprietary passive crossover
   network."

2. KRK ROKIT Powered Generation 1 user guide (RP5 column).
   "High Frequency Driver 1\" Soft Dome"; "Low Frequency Driver 5\" Aramid Glass Fiber";
   "AMPLIFIER Power Rating (HF/LF) 15 watts / 30 watts"; IEC mains connector.

3. KRK ROKIT Powered Generation 3 info sheet (ROKIT 8 column).
   "Configuration 2-Way"; "System type Active Studio Monitor"; "HF Transducer 1\" Soft-dome tweeter";
   "LF Transducer 8\" Aramid glass composite woofer".

All three documents are KRK publications served from cdn.shopify.com, which is not a KRK-owned host, so the
values are THIRD_PARTY_VERIFIED and never MANUFACTURER_VERIFIED.
"""
DATE = '2026-10-19'
ROUND = 29

KRK_7000 = ('https://cdn.shopify.com/s/files/1/0566/0809/6342/files/KRK-7000b_spec_sheet.pdf'
            '?v=1708102022')
KRK_G1 = ('https://cdn.shopify.com/s/files/1/0566/0809/6342/files/KRK_ROKIT_Powered_G1_Series_Manual.pdf'
          '?v=1708102022')
KRK_G3 = ('https://cdn.shopify.com/s/files/1/0566/0809/6342/files/'
          'KRK-ROKIT-Powered-Generation-3-Series-Info-Sheet.pdf?v=1708102022')

_7000_WHY = ('The document is a KRK publication, but the retained copy is served from cdn.shopify.com, not '
             'from a KRK-owned host.')

PROMOTIONS = [
    {'record': 'krk-7000', 'field': 'driverCount', 'value': 2, 'source': KRK_7000,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK Model 7000B/BS close-field monitor specification sheet',
     'whyNotManufacturer': _7000_WHY,
     'note': ('Round 29 (2026-10-19): KRK 7000B spec sheet — "The components are comprised of a 7-inch '
              'Kevlar woofer and a 1-inch Kevlar dome tweeter"; "Drivers: 7\\" kevlar/1\\" kevlar". Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified against the KRK '
                     '7000B spec sheet ("Passive 2-way").')},
    {'record': 'krk-7000', 'field': 'active', 'value': False, 'source': KRK_7000,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK Model 7000B/BS close-field monitor specification sheet',
     'whyNotManufacturer': _7000_WHY,
     'note': ('Round 29 (2026-10-19): same sheet — "Crossover: Passive 2-way"; "The system is crossed over '
              'at 3 kHz with a proprietary passive crossover network." No amplifier or mains input is '
              'specified.'),
     'notesAppend': ''},
    {'record': 'krk-rokit-5', 'field': 'driverCount', 'value': 2, 'source': KRK_G1,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK ROKIT Powered Series (Generation 1) user guide, RP5 column',
     'whyNotManufacturer': ('KRK publication served from cdn.shopify.com, not from a KRK-owned host.'),
     'note': ('Round 29 (2026-10-19): ROKIT G1 manual, RP5 column — "High Frequency Driver 1\\" Soft Dome"; '
              '"Low Frequency Driver 5\\" Aramid Glass Fiber". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true verified against the ROKIT '
                     'Powered Generation 1 user guide (RP5).')},
    {'record': 'krk-rokit-5', 'field': 'active', 'value': True, 'source': KRK_G1,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK ROKIT Powered Series (Generation 1) user guide, RP5 column',
     'whyNotManufacturer': ('KRK publication served from cdn.shopify.com, not from a KRK-owned host.'),
     'note': ('Round 29 (2026-10-19): same table — "AMPLIFIER Power Rating (HF/LF) 15 watts / 30 watts"; '
              '"IEC Mains Connector"; fuse ratings and a power switch are listed. Built-in amplification.'),
     'notesAppend': ''},
    {'record': 'krk-rokit-8', 'field': 'driverCount', 'value': 2, 'source': KRK_G3,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK ROKIT Powered Generation 3 info sheet, ROKIT 8 column',
     'whyNotManufacturer': ('KRK publication served from cdn.shopify.com, not from a KRK-owned host.'),
     'note': ('Round 29 (2026-10-19): ROKIT G3 info sheet, ROKIT 8 column — "Configuration 2-Way"; "HF '
              'Transducer 1\\" Soft-dome tweeter"; "LF Transducer 8\\" Aramid glass composite woofer". Two '
              'transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true verified against the ROKIT '
                     'Generation 3 info sheet (ROKIT 8).')},
    {'record': 'krk-rokit-8', 'field': 'active', 'value': True, 'source': KRK_G3,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': 'KRK ROKIT Powered Generation 3 info sheet, ROKIT 8 column',
     'whyNotManufacturer': ('KRK publication served from cdn.shopify.com, not from a KRK-owned host.'),
     'note': ('Round 29 (2026-10-19): same sheet — "System type Active Studio Monitor"; per-model amplifier '
              'power (ROKIT 8: 25 W HF / 75 W LF) and "Auto-Standby". Built-in amplification.'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': KRK_7000, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('KRK 7000B: "7-inch Kevlar woofer and a 1-inch Kevlar dome tweeter"; "Crossover: Passive '
                  '2-way"; "proprietary passive crossover network"; 8 ohms; 150 W.'),
     'fieldResults': [
         {'record': 'krk-7000', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two named transducers; third-party copy of the KRK sheet.'},
         {'record': 'krk-7000', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: "Passive 2-way" and passive crossover network.'},
     ]},
    {'url': KRK_G1, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0, 4, 5], 'chunksTotal': 6,
     'evidence': ('ROKIT G1 manual: RP5 "High Frequency Driver 1\\" Soft Dome", "Low Frequency Driver 5\\" '
                  'Aramid Glass Fiber", "AMPLIFIER Power Rating (HF/LF) 15 watts / 30 watts", IEC mains '
                  'connector.'),
     'fieldResults': [
         {'record': 'krk-rokit-5', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two drivers in the RP5 column.'},
         {'record': 'krk-rokit-5', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: built-in HF/LF amplifiers, IEC mains inlet.'},
     ]},
    {'url': KRK_G3, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
     'evidence': ('ROKIT G3 info sheet: "Configuration 2-Way", "System type Active Studio Monitor", HF 1\\" '
                  'soft dome, LF 8\\" aramid glass composite (ROKIT 8), amplifier power per model.'),
     'fieldResults': [
         {'record': 'krk-rokit-8', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: 2-way with one HF and one LF transducer.'},
         {'record': 'krk-rokit-8', 'field': 'active', 'value': True, 'outcome': 'PROMOTED',
          'note': 'Round 29: "System type Active Studio Monitor".'},
     ]},
]
