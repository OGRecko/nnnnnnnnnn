#!/usr/bin/env python3
"""Round 29 batch 32 (2026-10-19): locate.gov JBL 4310 manual re-read.

Round 12 recorded "Passive/active not stated" for this document. Re-reading the same PDF page shows the
architectural specification does state the system is a passive loudspeaker:

  "The loudspeaker system shall consist of three direct-radiator transducers and frequency dividing
   network installed in a tube-ported enclosure."
  "This unretouched photo shows the acoustic output of the system when driven by a 50 Watt sine wave
   signal at 35 Hz."
  "... its rated capacity of 50 watts program material ..."

A dividing network inside the enclosure driven by an amplified sine-wave signal and a 50 W program rating
is a passive loudspeaker; no amplifier, mains input or powered stage is described anywhere in the manual.

Promotion is still blocked by the Round 14 host policy: tile.loc.gov is NOT_MANUFACTURER, so both fields
stay CITED_IN_NOTES_UNCHECKED. The queue rows become SUPPORTED_NOT_PROMOTED (they were NOT_STATED for
active), which records what the document now supports without changing the dataset.

`legacy-jbl-3` no longer exists in src/data/speakers.json (archived record). Its two queue rows are marked
RECORD_ARCHIVED so the queue stops counting fields that cannot be written.
"""
DATE = '2026-10-19'
ROUND = 29
URL = ('https://tile.loc.gov/storage-services/master/mbrs/recording_preservation/manuals/'
       'JBL%20Prof.%20Series%20Model%204310%20Control%20Room%20Monitor.pdf')

EVIDENCE = (
    'Architectural specification: "The loudspeaker system shall consist of three direct-radiator '
    'transducers and frequency dividing network installed in a tube-ported enclosure." Components: 12" '
    'woofer (1500 Hz crossover), 5" midrange, 1-3/4" ultra-high transducer. Passive wording: the system is '
    '"driven by a 50 Watt sine wave signal", rated "50 watts program material", and the dividing network '
    'sits inside the enclosure; no amplifier or mains input is described. Round 12\'s "passive/active not '
    'stated" reading is superseded by this quote.')

FIELD_RESULTS = [
    {'record': 'jbl-4310', 'field': 'driverCount', 'value': 3, 'outcome': 'SUPPORTED_NOT_PROMOTED',
     'note': ('Round 29 (2026-10-19): manual states three direct-radiator transducers (12" LF, 5" MF, '
              '1-3/4" UHF). Host policy (tile.loc.gov is NOT_MANUFACTURER) still blocks promotion; status '
              'stays CITED_IN_NOTES_UNCHECKED.')},
    {'record': 'jbl-4310', 'field': 'active', 'value': False, 'outcome': 'SUPPORTED_NOT_PROMOTED',
     'note': ('Round 29 (2026-10-19): dividing network inside the enclosure plus "driven by a 50 Watt sine '
              'wave signal" and "50 watts program material" establish a passive system; no amplifier is '
              'described. Promotion blocked by the same host policy.')},
    {'record': 'legacy-jbl-3', 'field': 'driverCount', 'value': 3, 'outcome': 'RECORD_ARCHIVED',
     'note': 'Round 29 (2026-10-19): record is no longer in speakers.json; nothing can be written.'},
    {'record': 'legacy-jbl-3', 'field': 'active', 'value': False, 'outcome': 'RECORD_ARCHIVED',
     'note': 'Round 29 (2026-10-19): record is no longer in speakers.json; nothing can be written.'},
]

LEDGER_ROWS = [
    {'record': 'jbl-4310', 'field': 'active', 'value': False, 'outcome': 'SUPPORTED_HOST_POLICY_BLOCKED',
     'url': URL,
     'note': ('Manual establishes a passive system ("frequency dividing network installed in a tube-ported '
              'enclosure"; driven by a 50 W sine wave; 50 W program rating). Kept CITED_IN_NOTES_UNCHECKED '
              'because tile.loc.gov is not a manufacturer host.'),
     'supersedes': 'queue-url-status round 12 evidence ("Passive/active not stated")'},
]
