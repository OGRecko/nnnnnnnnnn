#!/usr/bin/env python3
"""Round 28 (2026-10-19): Round 18 consistency review of the EV Zx3 and PreSonus R records.

WHAT THIS DOES
  Reopens the Round 18 field checks and re-reads the exact documents they cite. Every value in the
  four records is supported by the document; what was wrong was the *notes*:

   * both Zx3 records cited "p. 3" for a specification table that is on page 10;
   * both sensitivity notes claimed "95 dB full-space" language that the manual does not contain (its
     only footnote is "Half Space Measurement");
   * both active notes quoted a "System Configuration" row that is not in the manual, and a connector
     string that is not the manual's wording;
   * the power note labelled the row "Full-Range" where the manual says "Power Handling (Passive)".

  A stale copy of the same unsupported 95 dB claim in RESEARCH-STATUS-ROUND22.md is annotated.

  The PreSonus R80 woofer provenance now records WHY 8 in is kept: the accepted manual and the tech
  sheet's own feature bullet say 8-inch, while the tech sheet's technical table row says 6.5-inch.

WHAT THIS DOES NOT DO
  No value changes. No status promotions or demotions: each field's status already matched the
  evidence, and this batch only makes the recorded evidence exact. The owner-confirmed fmicassets.com
  host decision is untouched. Old notes are preserved in round28-value-history.json.
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
HISTORY = os.path.join(ROOT, 'scripts', 'research', 'round28-value-history.json')
LEDGER = os.path.join(ROOT, 'scripts', 'research', 'round28-round18-review.json')
ROUND = 28
DATE = '2026-10-19'
ZX3 = 'https://www.eviaudio.fr/wp-content/uploads/2020/04/ev_zx3_manuel.pdf'
PRESONUS_MANUAL = 'https://www.fmicassets.com/Damroot/Original/10001/OM_2777500201_R65_EN.pdf'
PRESONUS_R80_SHEET = 'https://www.fmicassets.com/Damroot/Original/10001/OM_2777500203_R80_Tech-Sheet_EN.pdf'

ZX3_NOTES = {
    'driverCount': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Electro-Voice Zx3 Owner's Manual "
        "DOC38110265 Rev B, Specifications (p. 10): LF Transducer \"DVX3121, 12 in (305mm) Driver\"; "
        "HF Transducer \"ND2, 1 in (25.4mm) exit Neodymium Compression Driver\". Two driven "
        "transducers, in both passive and biamp modes."
    ),
    'active': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: the manual states \"Passive and biamp "
        "selectable\", lists \"Power Handling (Passive): 600W Continuous, 2400W Peak\" and prints a "
        "\"Block Diagram - Passive Mode\"; it gives no amplifier power rating and the system is driven "
        "by an external amplifier, so it is not self-powered. The earlier note quoted a \"System "
        "Configuration\" row that this document does not contain."
    ),
    'sensitivity': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Specifications (p. 10) \"Axial "
        "Sensitivity: 97 dB (1W/1m)\", footnote 1 \"Half Space Measurement\". The manual publishes no "
        "separate full-space figure; the earlier note's \"95 dB full-space\" clause was not in the "
        "document and has been removed rather than repeated."
    ),
    'impedance': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Specifications (p. 10) \"Nominal "
        "Impedance: 8 Ohms\" and \"Minimum Impedance: 6.2 Ohms\"."
    ),
    'power': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Specifications (p. 10) \"Power Handling "
        "(Passive): 600W Continuous, 2400W Peak\". The stored scalar is the continuous rating for "
        "passive operation; the peak figure is context only. The earlier note called this row "
        "\"Full-Range\", which is not the manual's wording."
    ),
    'frequencyResponse': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Specifications (p. 10) \"Freq. Response "
        "(-3 dB): 58 Hz - 15 kHz\" under footnote 1 \"Half Space Measurement\". The -10 dB range "
        "(48 Hz - 20 kHz) stays context and is not substituted for the -3 dB limits."
    ),
    'woofer': (
        "Round 28 (2026-10-19) recheck of the Round 18 check: Specifications (p. 10), LF Transducer "
        "\"DVX3121, 12 in (305mm) Driver\". Origin and hosting remain recorded separately."
    ),
}

R80_WOOFER_NOTE = (
    "Round 28 (2026-10-19) recheck: the accepted owner's manual, Technical Specifications (p. 12), "
    "lists \"R80 | 8\\\" Woven composite\" and the R80 tech sheet's Key Features say \"8-inch woven "
    "composite LF drivers\", while that sheet's technical table prints \"LF Driver | 6.5\\\" Woven "
    "Composite\" for the R80. The 8-inch value is kept on the model-specific manual row and the "
    "sheet's feature bullet; the contradictory table row is recorded here rather than followed."
)


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def record(history, rid, field, before_value, before_note, after_note, source, reason):
    entry = {
        'id': rid,
        'field': field,
        'value': before_value,
        'before': {'value': before_value, 'provenanceNote': before_note},
        'after': {'value': before_value, 'provenanceNote': after_note},
        'round': ROUND,
        'action': 'CORRECT_PROVENANCE_NOTE',
        'source': source,
        'reason': reason,
    }
    key = (rid, field, source, entry['action'])
    seen = {(h['id'], h['field'], h.get('source'), h.get('action')) for h in history['entries']}
    if key not in seen:
        history['entries'].append(entry)
    return entry


def main():
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    history = json.load(open(HISTORY, encoding='utf-8')) if os.path.exists(HISTORY) else {
        'round': ROUND, 'entries': []
    }
    changes = []

    # ---- Electro-Voice Zx3-60 / Zx3-90: notes only, no value or status change
    for rid in ('electro-voice-zx3-60', 'electro-voice-zx3-90'):
        rec = by_id[rid]
        for field, new_note in ZX3_NOTES.items():
            prov = rec.get(field + 'Provenance') if field in ('driverCount', 'active') else rec[field]
            assert prov is not None, (rid, field)
            assert prov.get('source') == ZX3, (rid, field, prov.get('source'))
            old_note = prov.get('note', '')
            assert old_note != new_note, (rid, field, 'already applied')
            record(history, rid, field, rec.get(field), old_note, new_note, ZX3,
                   'Round 18 note rechecked against the opened manual; value and status unchanged.')
            prov['note'] = new_note
            changes.append({'record': rid, 'field': field, 'outcome': 'NOTE_CORRECTED',
                            'value': rec.get(field), 'status': prov.get('status')})

        # Field-level facts this review established, recorded in the ledger (not in the record notes).
        changes.append({'record': rid, 'field': 'driverCount/active/woofer/sensitivity', 'outcome': 'EVIDENCE_CONFIRMED'})

    # ---- PreSonus R80: explain the kept 8-inch value at field level
    r80 = by_id['presonus-r80']
    own = r80['woofer']
    assert own.get('value') == 8 and own.get('source') == PRESONUS_MANUAL, own
    old_note = own.get('note', '')
    assert old_note != R80_WOOFER_NOTE
    record(history, 'presonus-r80', 'woofer', 8, old_note, R80_WOOFER_NOTE, PRESONUS_MANUAL,
           'Round 18 value rechecked; the conflicting tech-sheet row is now recorded at field level.')
    own['note'] = R80_WOOFER_NOTE
    changes.append({'record': 'presonus-r80', 'field': 'woofer', 'outcome': 'NOTE_CORRECTED',
                    'value': 8, 'status': own.get('status')})

    # Sanity check the PreSonus fields this review re-read (no writes expected).
    checks = []
    for rid, woof, low in (('presonus-r65', 6.5, 45), ('presonus-r80', 8, 40)):
        rec = by_id[rid]
        assert rec['driverCount'] == 2, rec['id']
        assert rec['active'] is True, rec['id']
        assert rec['woofer']['value'] == woof, (rec['id'], rec['woofer']['value'])
        assert rec['frequencyResponse']['low_hz'] == low, (rec['id'], rec['frequencyResponse'])
        assert rec['sensitivity']['status'] == 'UNAVAILABLE', rec['id']
        assert rec['impedance']['status'] == 'UNAVAILABLE', rec['id']
        checks.append({
            'record': rid,
            'driverCount': [2, '2-way active AMT; LF driver + AMT HF driver'],
            'active': [True, 'manual: "2-way active AMT studio monitor", "self-powered"'],
            'woofer': [woof, 'manual Technical Specifications row'],
            'frequencyResponse': [f'{low}-22000 Hz (-3 dB)', 'manual Technical Specifications row'],
            'power': [rec['power']['value'], 'tech sheet: "150 watt, Class D biamplification"'],
            'sensitivity': ['UNAVAILABLE', 'manual publishes max/peak SPL, not acoustic sensitivity'],
            'impedance': ['UNAVAILABLE', 'manual publishes line INPUT impedance (20k/10k ohm), not load impedance'],
        })

    dump(DATA, db)
    history['round'] = ROUND
    dump(HISTORY, history)

    ledger = {
        'schema': 'round28-round18-review/v1',
        'round': ROUND,
        'checkedDate': DATE,
        'purpose': 'Recheck the Round 18 field checks against the exact documents they cite.',
        'documents': {
            'zx3Manual': {
                'url': ZX3,
                'documentOrigin': "Electro-Voice Zx3 Owner's Manual DOC38110265 Rev B",
                'hostingLocation': 'www.eviaudio.fr (EVI Audio France distributor copy, owner decision 1)',
                'chunksOpened': [0, 1, 2, 3, 5],
                'chunksTotal': 6,
            },
            'presonusManual': {'url': PRESONUS_MANUAL, 'chunksOpened': [0, 1, 2, 3], 'chunksTotal': 4},
            'presonusR80Sheet': {'url': PRESONUS_R80_SHEET, 'chunksOpened': [0], 'chunksTotal': 1},
        },
        'zx3Verdict': {
            'values': 'All seven stored fields are stated verbatim in the manual specification table (p. 10).',
            'statuses': 'Unchanged. Every field already had MANUFACTURER_VERIFIED and the document supports each one independently; no field was promoted because a sibling field was verified.',
            'defectsFound': [
                'Page reference said p. 3; the specification table is on p. 10.',
                'Sensitivity note claimed "95 dB full-space", which the manual does not state.',
                'Active note quoted a "System Configuration" row not present in the manual, and misquoted the connector row.',
                'Power note called the row "Full-Range" instead of "Power Handling (Passive)".',
            ],
            'unresolved': 'none',
        },
        'presonusVerdict': {
            'values': 'R65 and R80 driverCount, active, woofer and frequency response match the manual; power matches the tech sheets; sensitivity and load impedance remain UNAVAILABLE with reasons recorded.',
            'host': 'www.fmicassets.com stays ESTABLISHED under the owner confirmation of 2026-10-13; unchanged.',
            'defectsFound': [
                'R80 woofer provenance did not record why 8 in is kept against the tech sheet table row that says 6.5 in.',
            ],
            'unresolved': 'none',
        },
        'fieldChecks': changes,
        'presonusFieldMatrix': checks,
        'valueChanges': 0,
    }
    dump(LEDGER, ledger)
    print(f'round28 review: note corrections={len(changes)} value_changes=0 ledger={os.path.basename(LEDGER)}')


if __name__ == '__main__':
    main()
