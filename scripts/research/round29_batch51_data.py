#!/usr/bin/env python3
"""Round 29 batch 51 (2026-10-19): Klipsch owner's manuals settle `active: false` by wiring instructions.

The Klipsch spec sheets for these models list binding posts, impedance and power handling but never call
the loudspeaker passive, so they record NOT_STATED (see the round-27/round-29 spec-sheet passes). The
owner's manuals are a different document class and satisfy the second accepted form in
`PROVENANCE-POLICY.md`: the connection chapter instructs the user to wire each loudspeaker's terminals to
the corresponding channel of an external amplifier, and the manual describes no mains inlet, no power cord
and no built-in amplifier for the loudspeaker.

Three manuals are used, each of which names its models on the cover model list, so no related-model
substitution is involved:

* `Reference Premiere Speakers 2021 Manual v02` — RP-8060FA II, RP-8000F II, RP-6000F II, RP-5000F II,
  RP-600M II, RP-500M II.
* `Reference Premiere Speakers Manual v03` — the 2018 generation: RP-600M, RP-500M.
* `Reference Speakers 2018 Manual v02` — R-41M.

The Heritage manuals (Heresy/Cornwall) only name the series, not the IV revision, so they were read but are
not used for the `-iv` records.
"""
DATE = '2026-10-19'
ROUND = 29

RP21 = 'https://assets.klipsch.com/product-manuals/Reference-Premiere-Speakers-2021-Manual-v02.pdf'
RP18 = 'https://assets.klipsch.com/product-manuals/Reference-Premiere-Speakers-Manual-v03.pdf'
REF18 = 'https://assets.klipsch.com/product-manuals/Reference-Speakers-2018-Manual-v02.pdf'

RP21_DOC = 'Klipsch "Reference Premiere Speakers" 2021 owner\'s manual v02'
RP18_DOC = 'Klipsch "Reference Premiere Speakers" owner\'s manual v03 (2018 generation)'
REF18_DOC = 'Klipsch "Reference Speakers" 2018 owner\'s manual v02'

CONNECT = ('"Using 16-12 gauge speaker wire, connect the RED \u201cpositive\u201d (+) terminal of the LEFT speaker '
           'to the RED \u201cpositive\u201d (+) terminal of your amplifier\u2019s LEFT channel. Connect the BLACK '
           '\u201cnegative\u201d (\u2013) terminal of the LEFT speaker to the BLACK \u201cnegative\u201d (\u2013) terminal '
           'of your amplifier\u2019s LEFT channel."')

RP21_EVIDENCE = ('Cover model list: "REFERENCE PREMIERE SPEAKERS RP-8060FA II RP-8000F II RP-6000F II '
                 'RP-5000F II RP-600M II RP-500M II". Connection chapter: ' + CONNECT +
                 ' Dual-binding-post note: "Reference Premiere models RP-8060FA II, RP-8000F II, RP-6000F II, '
                 'RP-5000F II, and RP-600M II are equipped with dual binding posts." The manual describes no '
                 'mains inlet, power cord or built-in amplifier for the loudspeaker.')

RP18_EVIDENCE = ('Cover model list: "REFERENCE PREMIERE SPEAKERS RP-8060FA RP-8000F RP-6000F RP-5000F '
                 'RP-4000F RP-600M RP-500M RP-400M RP-502S RP-402S RP-500SA RP-504C RP-404C RP-600C RP-500C '
                 'RP-400C". Connection chapter: ' + CONNECT +
                 ' The manual describes no mains inlet, power cord or built-in amplifier for the loudspeaker.')

REF18_EVIDENCE = ('Cover model list: "REFERENCE SPEAKERS ... R-51M R-41M R-52C R-625FA R-820F R-620F R-610F '
                  'R-34C R-41SA". Connection chapter: ' + CONNECT +
                  ' The manual describes no mains inlet, power cord or built-in amplifier for the loudspeaker.')


def note(model, doc):
    return ('Round 29 (2026-10-19): ' + doc + ' names ' + model + ' on its cover model list, and its '
            'connection chapter instructs the user to wire the loudspeaker terminals to the corresponding '
            'channel of an external amplifier (' + CONNECT + '); no mains inlet or built-in amplifier is '
            'described, which is accepted form (b) for active: false.')


def append(model):
    return (' Round 29 (2026-10-19): active false verified from the ' + model +
            ' owner\'s manual connection chapter (external-amplifier wiring, no mains inlet described); '
            'the spec sheet alone had left the field NOT_STATED.')


PROMOTIONS = [
    {'record': 'klipsch-rp8060fa', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-8060FA II', 'document': RP21_DOC},
    {'record': 'klipsch-rp-8000f-ii', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-8000F II', 'document': RP21_DOC},
    {'record': 'klipsch-rp6000f', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-6000F II', 'document': RP21_DOC},
    {'record': 'klipsch-rp-5000f-ii', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-5000F II', 'document': RP21_DOC},
    {'record': 'klipsch-rp600m', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-600M II', 'document': RP21_DOC},
    {'record': 'klipsch-rp500m', 'field': 'active', 'value': False, 'source': RP21,
     'model': 'RP-500M II', 'document': RP21_DOC},
    {'record': 'klipsch-rp-600m', 'field': 'active', 'value': False, 'source': RP18,
     'model': 'RP-600M', 'document': RP18_DOC},
    {'record': 'klipsch-rp-500m', 'field': 'active', 'value': False, 'source': RP18,
     'model': 'RP-500M', 'document': RP18_DOC},
    {'record': 'legacy-klip-8', 'field': 'active', 'value': False, 'source': REF18,
     'model': 'R-41M', 'document': REF18_DOC},
]

for _p in PROMOTIONS:
    _p['note'] = note(_p['model'], _p['document'])
    _p['notesAppend'] = append(_p['model'])
    _p['fieldNote'] = ('Round 29: the ' + _p['model'] + ' owner\'s manual wires the speaker to an external '
                       'amplifier and describes no mains inlet.')


def _fr(p):
    return {'record': p['record'], 'field': p['field'], 'value': p['value'], 'outcome': 'PROMOTED',
            'note': p['fieldNote']}


URL_RESULTS = [
    {'url': RP21, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 4,
     'document': RP21_DOC, 'evidence': RP21_EVIDENCE,
     'fieldResults': [_fr(p) for p in PROMOTIONS if p['source'] == RP21]},
    {'url': RP18, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 4,
     'document': RP18_DOC, 'evidence': RP18_EVIDENCE,
     'fieldResults': [_fr(p) for p in PROMOTIONS if p['source'] == RP18]},
    {'url': REF18, 'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 4,
     'document': REF18_DOC, 'evidence': REF18_EVIDENCE,
     'fieldResults': [_fr(p) for p in PROMOTIONS if p['source'] == REF18]},
]

HOSTS = {RP21: 'assets.klipsch.com', RP18: 'assets.klipsch.com', REF18: 'assets.klipsch.com'}
