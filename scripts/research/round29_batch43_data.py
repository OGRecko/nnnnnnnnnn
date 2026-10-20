#!/usr/bin/env python3
"""Round 29 batch 43 (2026-10-19): the six remaining Electro-Voice Tour X listings on Full Compass.

Each page was opened and read. Every one names the exact Tour X model and part number, enumerates its
transducers in the specification list, and prints "Internal Crossover" plus "Nominal Impedance (Passive)".
Five of the six also carry the word "Passive" in the product name; the TX2181 page instead instructs
"Use with processor and dedicated amp channel", which is the external-amplifier evidence the policy
accepts. All are retailer-hosted — Full Compass is a third party — so the tier is THIRD_PARTY_VERIFIED.
"""
DATE = '2026-10-19'
ROUND = 29

WHY = ('The listing is served from fullcompass.com, a retailer, not from an Electro-Voice host; the '
       'manufacturer page for this legacy model was not opened.')


def url(part):
    return 'https://www.fullcompass.com/prod/' + part


TX1152 = url('133350-electro-voice-tx1152-tour-x-15-2-way-60-x-40-500w-passive-loudspeaker-black')
TX2152 = url('133352-electro-voice-tour-x-tx2152-dual-15-2-way-passive-speaker-with-a-60x40-horn')
TX1181 = url('133354-electro-voice-tour-x-tx1181-18-500w-passive-subwoofer-black')
TX2181 = url('133355-electro-voice-tour-x-tx2181-18-subwoofer-with-evs-18s-woofers')
TX1122FM = url('133356-electro-voice-tx1122fm-12-2-way-passive-vertical-floor-monitor-with-90-x-50-horn')
TX1152FM = url('133358-electro-voice-tx1152fm-15-2-way-passive-vertical-floor-monitor-with-90-x-50-horn')

PROMOTIONS = [
    {'record': 'electro-voice-tx1152', 'field': 'driverCount', 'value': 2, 'source': TX1152,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX1152 15\" 2-Way 60x40 500W Passive "
                 "Loudspeaker, Black', MFR # F.01U.302.273",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX1152 listing — "LF Transducer: 15-inch SMX2151" and '
              'the feature list\'s "1.25-inch DH3/2010A titanium HF compression driver". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Full Compass '
                     'TX1152 listing, whose name reads "Passive Loudspeaker" and whose specs print "Internal '
                     'Crossover: Yes".')},
    {'record': 'electro-voice-tx1152', 'field': 'active', 'value': False, 'source': TX1152,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX1152 15\" 2-Way 60x40 500W Passive "
                 "Loudspeaker, Black', MFR # F.01U.302.273",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — the product name is "Electro-Voice Tour X TX1152 15\\" '
              '2-Way 60x40 500W Passive Loudspeaker, Black" and the spec list prints "Internal Crossover: '
              'Yes". Explicit passive wording.'),
     'notesAppend': ''},
    {'record': 'electro-voice-tx2152', 'field': 'driverCount', 'value': 3, 'source': TX2152,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX2152 Dual 15\" 2-Way Passive Speaker with a "
                 "60x40 Horn', MFR # F.01U.302.274",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX2152 listing — "LF Transducer: (2) SMX2151" and "HF '
              'Transducer: ND2". Two woofers plus one HF device.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 3 and active false verified from the Full Compass '
                     'TX2152 listing ("Dual 15\\" 2-Way Passive Speaker", "Nominal Impedance (passive): '
                     '4 ohms").')},
    {'record': 'electro-voice-tx2152', 'field': 'active', 'value': False, 'source': TX2152,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX2152 Dual 15\" 2-Way Passive Speaker with a "
                 "60x40 Horn', MFR # F.01U.302.274",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — the product name is "Electro-Voice Tour X TX2152 Dual '
              '15\\" 2-Way Passive Speaker with a 60x40 Horn", the spec list prints "Internal Crossover: Yes" '
              'and "Nominal Impedance (passive): 4 ohms".'),
     'notesAppend': ''},
    {'record': 'electro-voice-tx1181', 'field': 'driverCount', 'value': 1, 'source': TX1181,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX1181 18\" 500W Passive Subwoofer, Black', "
                 "MFR # F.01U.302.275",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX1181 listing — "LF Transducer: EVS18S" and "Speaker '
              'Type: Subs"; no HF transducer is listed. One transducer.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 1 and active false verified from the Full Compass '
                     'TX1181 listing ("18\\" 500W Passive Subwoofer", "Nominal Impedance (Passive): 8 Ohms").')},
    {'record': 'electro-voice-tx1181', 'field': 'active', 'value': False, 'source': TX1181,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX1181 18\" 500W Passive Subwoofer, Black', "
                 "MFR # F.01U.302.275",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — the product name is "Electro-Voice Tour X TX1181 18\\" '
              '500W Passive Subwoofer, Black" and the spec list prints "Nominal Impedance (Passive): 8 Ohms" '
              'with "Internal Crossover: Yes".'),
     'notesAppend': ''},
    {'record': 'electro-voice-tx2181', 'field': 'driverCount', 'value': 2, 'source': TX2181,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX2181 18\" Subwoofer with EVS-18S Woofers', "
                 "MFR # F.01U.302.276",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX2181 listing — feature "Two high-excursion EVS-18S '
              'woofers" and specification "LF Transducer: (2) EVS18S"; "Speaker Type: Subs", no HF device. '
              'Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Full Compass '
                     'TX2181 listing, whose feature list says "Use with processor and dedicated amp channel" '
                     'and whose specs print "Nominal Impedance (Passive): 4 Ohms".')},
    {'record': 'electro-voice-tx2181', 'field': 'active', 'value': False, 'source': TX2181,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice Tour X TX2181 18\" Subwoofer with EVS-18S Woofers', "
                 "MFR # F.01U.302.276",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — feature list instructs "Use with processor and dedicated '
              'amp channel", and the specification prints "Nominal Impedance (Passive): 4 Ohms" with '
              '"Internal Crossover: No". External processing and amplification.'),
     'notesAppend': ''},
    {'record': 'electro-voice-tx1122fm', 'field': 'driverCount', 'value': 2, 'source': TX1122FM,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice TX1122FM 12\" 2-Way Passive Vertical Floor Monitor "
                 "with 90 x 50 Horn', MFR # F.01U.302.277",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX1122FM listing — "LF Transducer: SMX2121" and "HF '
              'Transducer: DH3"; the overview names the "SMX2121 woofer and 1-1/4\\" DH3/2010A titanium HF '
              'driver". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Full Compass '
                     'TX1122FM listing ("two-way passive floor monitor", "Nominal Impedance (Passive): '
                     '8 Ohms").')},
    {'record': 'electro-voice-tx1122fm', 'field': 'active', 'value': False, 'source': TX1122FM,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice TX1122FM 12\" 2-Way Passive Vertical Floor Monitor "
                 "with 90 x 50 Horn', MFR # F.01U.302.277",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — "The TX1122FM is a 12\", two-way passive floor monitor", '
              'with "Nominal Impedance (Passive): 8 Ohms" and "Internal Crossover: Yes".'),
     'notesAppend': ''},
    {'record': 'electro-voice-tx1152fm', 'field': 'driverCount', 'value': 2, 'source': TX1152FM,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice TX1152FM 15\" 2-Way Passive Vertical Floor Monitor "
                 "with 90 x 50 Horn', MFR # F.01U.302.278",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): Full Compass TX1152FM listing — "LF Transducer: SMX2151" and "HF '
              'Transducer: DH3". Two transducers.'),
     'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active false verified from the Full Compass '
                     'TX1152FM listing ("15\\" 2-Way Passive Vertical Floor Monitor", "Nominal Impedance '
                     '(Passive): 8 Ohms").')},
    {'record': 'electro-voice-tx1152fm', 'field': 'active', 'value': False, 'source': TX1152FM,
     'sourceType': 'THIRD_PARTY', 'status': 'THIRD_PARTY_VERIFIED',
     'document': "Full Compass listing 'Electro-Voice TX1152FM 15\" 2-Way Passive Vertical Floor Monitor "
                 "with 90 x 50 Horn', MFR # F.01U.302.278",
     'whyNotManufacturer': WHY,
     'note': ('Round 29 (2026-10-19): same listing — the product name is "Electro-Voice TX1152FM 15\\" 2-Way '
              'Passive Vertical Floor Monitor with 90 x 50 Horn" and the specs print "Internal Crossover: '
              'Yes".'),
     'notesAppend': ''},
]

URL_RESULTS = [
    {'url': TX1152, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"Passive Loudspeaker"; "LF Transducer: 15-inch SMX2151"; "1.25-inch DH3/2010A"; '
                 '"Internal Crossover: Yes".',
     'fieldResults': [
         {'record': 'electro-voice-tx1152', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: SMX2151 + DH3/2010A.'},
         {'record': 'electro-voice-tx1152', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: product name says "Passive".'},
     ]},
    {'url': TX2152, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"Dual 15\\" 2-Way Passive Speaker"; "LF Transducer: (2) SMX2151"; "HF Transducer: ND2"; '
                 '"Nominal Impedance (passive): 4 ohms".',
     'fieldResults': [
         {'record': 'electro-voice-tx2152', 'field': 'driverCount', 'value': 3, 'outcome': 'PROMOTED',
          'note': 'Round 29: two SMX2151 + ND2.'},
         {'record': 'electro-voice-tx2152', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: product name says "Passive".'},
     ]},
    {'url': TX1181, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"18\\" 500W Passive Subwoofer"; "LF Transducer: EVS18S"; "Speaker Type: Subs"; '
                 '"Nominal Impedance (Passive): 8 Ohms".',
     'fieldResults': [
         {'record': 'electro-voice-tx1181', 'field': 'driverCount', 'value': 1, 'outcome': 'PROMOTED',
          'note': 'Round 29: one EVS18S, no HF device.'},
         {'record': 'electro-voice-tx1181', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: product name says "Passive Subwoofer".'},
     ]},
    {'url': TX2181, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"Two high-excursion EVS-18S woofers"; "LF Transducer: (2) EVS18S"; "Use with processor and '
                 'dedicated amp channel"; "Nominal Impedance (Passive): 4 Ohms"; "Internal Crossover: No".',
     'fieldResults': [
         {'record': 'electro-voice-tx2181', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: two EVS18S.'},
         {'record': 'electro-voice-tx2181', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: "Use with processor and dedicated amp channel".'},
     ]},
    {'url': TX1122FM, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"two-way passive floor monitor"; "LF Transducer: SMX2121"; "HF Transducer: DH3"; "Nominal '
                 'Impedance (Passive): 8 Ohms".',
     'fieldResults': [
         {'record': 'electro-voice-tx1122fm', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: SMX2121 + DH3.'},
         {'record': 'electro-voice-tx1122fm', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: "two-way passive floor monitor".'},
     ]},
    {'url': TX1152FM, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 2,
     'evidence': '"15\\" 2-Way Passive Vertical Floor Monitor"; "LF Transducer: SMX2151"; "HF Transducer: '
                 'DH3"; "Internal Crossover: Yes".',
     'fieldResults': [
         {'record': 'electro-voice-tx1152fm', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
          'note': 'Round 29: SMX2151 + DH3.'},
         {'record': 'electro-voice-tx1152fm', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
          'note': 'Round 29: product name says "Passive".'},
     ]},
]
