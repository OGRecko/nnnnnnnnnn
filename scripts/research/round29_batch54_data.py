#!/usr/bin/env python3
"""Round 29 batch 54 (2026-10-19): Meyer Sound UPA-1P and UPJ-1P from their own datasheets.

Both records were `UNSOURCED` nulls. Meyer Sound's own datasheets state the drive complement and the
built-in amplification explicitly, which settles `driverCount` and `active` (true) together.

Host note: meyersound.com retired both product pages (`/product/upa-1p/` now serves the product index,
`/product/upj-1p/` returns "Page not found"), and the surviving Meyer documentation site only offers the
discontinued series as ZIP archives. The datasheets below are Meyer Sound's own PDFs, served by a pro-audio
dealer and a distributor respectively, so they are recorded as `THIRD_PARTY_VERIFIED` with sourceType
`THIRD_PARTY` — the evidence is manufacturer-authored, the host is not the manufacturer's.
"""
DATE = '2026-10-19'
ROUND = 29

UPA = ('https://prg-proshop.com/themes/prg/assets/files/product/'
       '087a9d79e530f24051cf9f19ef0fe1ef.pdf')
UPJ = 'https://www.imlight.ru/files/PDF/ZVUK/MEYER/AS/ULTRA/upj-1p.pdf'

WHY_UPA = ('meyersound.com/product/upa-1p/ no longer serves a product page (it returns the product index), '
           'and the Meyer documentation site publishes discontinued products only as ZIP archives; this is '
           'Meyer Sound\'s own datasheet PDF, mirrored by a pro-audio dealer.')
WHY_UPJ = ('meyersound.com/product/upj-1p/ returns "Page not found", and the Meyer documentation site '
           'publishes discontinued products only as ZIP archives; this is Meyer Sound\'s own datasheet PDF, '
           'mirrored by a distributor.')

UPA_DOC = 'Meyer Sound "UPA-1P Compact Wide Coverage Loudspeaker" datasheet'
UPJ_DOC = 'Meyer Sound "UPJ-1P Compact VariO Loudspeaker" datasheet'

PROMOTIONS = [
    {'record': 'meyer-ups1p', 'field': 'driverCount', 'value': 2, 'source': UPA, 'sourceType': 'THIRD_PARTY',
     'document': UPA_DOC, 'whyNotManufacturer': WHY_UPA,
     'note': ('Round 29 (2026-10-19): Meyer Sound UPA-1P datasheet, TRANSDUCERS table — "Low Frequency | '
              'One 12-inch cone driver; 2 Ω nominal impedance" and "High Frequency | One 3-inch compression '
              'driver; 16 Ω nominal impedance". Two transducers, and the model is named in the title.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the Meyer Sound UPA-1P datasheet '
                '("One 12-inch cone driver" and "One 3-inch compression driver").')},
    {'record': 'meyer-ups1p', 'field': 'active', 'value': True, 'source': UPA, 'sourceType': 'THIRD_PARTY',
     'document': UPA_DOC, 'whyNotManufacturer': WHY_UPA,
     'note': ('Round 29 (2026-10-19): Meyer Sound UPA-1P datasheet — "A proprietary two-channel, class '
              'AB/bridged power amplifier with complementary MOSFET output stages drives the UPA-1P. Total '
              'peak power output is 1000 watts"; the AC POWER table lists "Connector | PowerCON20 input". '
              'Built-in amplification with a mains inlet, so the loudspeaker is powered.'),
     'append': (' Round 29 (2026-10-19): active true verified from the Meyer Sound UPA-1P datasheet, which '
                'describes a built-in two-channel power amplifier (1000 W peak) and a PowerCON20 mains '
                'inlet.')},
    {'record': 'meyer-sound-upj-1p', 'field': 'driverCount', 'value': 2, 'source': UPJ,
     'sourceType': 'THIRD_PARTY', 'document': UPJ_DOC, 'whyNotManufacturer': WHY_UPJ,
     'note': ('Round 29 (2026-10-19): Meyer Sound UPJ-1P datasheet — "a 10-inch low-frequency neodymium '
              'magnet cone driver and 3-inch diaphragm compression driver in the high-frequency section"; '
              'TRANSDUCERS table "Low Frequency | One 10-inch cone driver with neodymium magnet" and '
              '"High Frequency | One 3-inch diaphragm compression driver". Two transducers.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the Meyer Sound UPJ-1P datasheet '
                '("One 10-inch cone driver" and "One 3-inch diaphragm compression driver").')},
    {'record': 'meyer-sound-upj-1p', 'field': 'active', 'value': True, 'source': UPJ,
     'sourceType': 'THIRD_PARTY', 'document': UPJ_DOC, 'whyNotManufacturer': WHY_UPJ,
     'note': ('Round 29 (2026-10-19): Meyer Sound UPJ-1P datasheet — "The UPJ-1P combines the advantages of '
              'self-powered systems"; "A proprietary Meyer Sound two-channel, class AB/bridged power '
              'amplifier with complementary MOSFET output stages provides a total output of 550 watts"; AC '
              'POWER "Connector | powerCON 20 input with loop output". Self-powered with a mains inlet.'),
     'append': (' Round 29 (2026-10-19): active true verified from the Meyer Sound UPJ-1P datasheet, which '
                'states "self-powered systems" and describes a built-in 550 W two-channel amplifier with a '
                'powerCON mains inlet.')},
]

YAM = 'https://www.yamaha.com/catalogs/PDFs/brochures/pac/DMI/HS.pdf'
FOC = 'https://www.sounddd.shop/download/Specification/FOCAL/Focal_Solo6_BE_Spec.pdf'

WHY_FOC = ('focal.com/products/solo-6 now serves the current-generation Solo6 (1.5" tweeter), not the '
           'Solo6 Be (1" Beryllium, 150 W BASH + 100 W class AB); this is Focal\'s own Solo6 Be data sheet, '
           'mirrored by a reseller.')

PROMOTIONS += [
    {'record': 'yamaha-hs80m', 'field': 'driverCount', 'value': 2, 'source': YAM,
     'sourceType': 'MANUFACTURER', 'document': 'Yamaha "HS series" brochure (HS80M / HS50M / HS10W)',
     'note': ('Round 29 (2026-10-19): Yamaha HS series brochure, Speaker Components — HS80M is listed with '
              '"LF: 8-in cone (Magnetic shielding Type)" and "HF: 1-in Dome (Magnetic shielding Type)", and '
              'the product bullet reads "2-way bass-reflex bi-amplified near-field studio monitor with 8-in '
              'cone woofer and 1-in dome high-frequency unit". Two transducers.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the Yamaha HS series brochure '
                '("LF: 8-in cone" and "HF: 1-in Dome" for the HS80M).')},
    {'record': 'yamaha-hs80m', 'field': 'active', 'value': True, 'source': YAM,
     'sourceType': 'MANUFACTURER', 'document': 'Yamaha "HS series" brochure (HS80M / HS50M / HS10W)',
     'note': ('Round 29 (2026-10-19): Yamaha HS series brochure, General Specifications — HS80M "Type | '
              'Biamp 2-way Powered speaker", and the section heading "The Benefits Of Built-in Power And '
              'Bi-amplification"; the HS80M bullet quotes "120 watts dynamic bi-amplified power". Built-in '
              'amplification, so the loudspeaker is powered.'),
     'append': (' Round 29 (2026-10-19): active true verified from the Yamaha HS series brochure, which '
                'lists the HS80M type as "Biamp 2-way Powered speaker" with built-in bi-amplification.')},
    {'record': 'focal-solo6', 'field': 'driverCount', 'value': 2, 'source': FOC,
     'sourceType': 'THIRD_PARTY', 'document': 'Focal "Solo6 Be" product data sheet',
     'whyNotManufacturer': WHY_FOC,
     'note': ('Round 29 (2026-10-19): Focal Solo6 Be data sheet — "Solo6 Be is a 2-way monitor"; '
              'Transducers: "Woofer | 6W4370B, 6-1/2 in (16.5cm) Focal W composite sandwich cone drivers" and '
              '"High frequency | TB871, Focal Beryllium inverted dome tweeter with protective grille". '
              'Two transducers.'),
     'append': (' Round 29 (2026-10-19): driverCount 2 verified from the Focal Solo6 Be data sheet '
                '(6W4370B 6.5-inch woofer plus TB871 Beryllium tweeter).')},
    {'record': 'focal-solo6', 'field': 'active', 'value': True, 'source': FOC,
     'sourceType': 'THIRD_PARTY', 'document': 'Focal "Solo6 Be" product data sheet',
     'whyNotManufacturer': WHY_FOC,
     'note': ('Round 29 (2026-10-19): Focal Solo6 Be data sheet, Electronic section — "Bass - Midrange | '
              '150W rms, BASH technology" and "Treble | 100W rms, class AB"; Power supply "Connection | ... '
              'IEC inlet and detachable power cord"; user controls include "On/off switch, voltage selector" '
              'and a "Power On LED". Built-in amplification with a mains inlet.'),
     'append': (' Round 29 (2026-10-19): active true verified from the Focal Solo6 Be data sheet, which '
                'lists built-in 150 W BASH bass/midrange and 100 W class AB treble amplifiers and an IEC '
                'mains inlet.')},
]

HOSTS = {UPA: 'prg-proshop.com', UPJ: 'www.imlight.ru', FOC: 'www.sounddd.shop'}
