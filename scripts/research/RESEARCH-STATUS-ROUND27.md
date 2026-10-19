# Round 27 — disputed records and settlement of the review backlog

**Date:** 2026-10-19 · **Branch:** `arena/cdfc16bd-nnnnnnnnnn`
**Batch 1 of Round 27:** disputed-record adjudication (10 documents, 15 field outcomes, 12 value writes)

## Counts, recomputed from the repository (not carried over from a brief)

| Measure | Before this batch | After this batch |
| --- | --- | --- |
| Live records in `src/data/speakers.json` | 657 | 657 |
| `driverCount` + `active` fields | 1314 | 1314 |
| `MANUFACTURER_VERIFIED` | 696 | **710** |
| `CITED_IN_NOTES_UNCHECKED` | 237 | **221** |
| `UNSOURCED` | 192 | **194** |
| No provenance object | 189 | 189 |
| Provenance queue | 171 URLs / 237 items | **162 URLs / 221 items** |

`UNSOURCED` rose by one because the WL212-sw `active` value was retracted rather than replaced.

## What was opened and read (not a search snippet)

Every document below was retrieved in full or to the end of the relevant section, and the
quoted text is recorded in `scripts/research/round27_disputes_data.py`.

1. **ADAM Audio S3V** product page — one 9-inch ELE woofer, one 4-inch DCH midrange, one S-ART tweeter.
2. **ADAM Audio S3X-V** archived page — Technical Data "Number 1" rows for woofer, midrange and tweeter.
3. **ADAM Audio A8H** product page — one 8-inch MLM woofer, one 3.5-inch DCH midrange, one X-ART tweeter; named "Active Studio Monitor" with internal amplification.
4. **ADAM Audio S3A** archived page **and its linked operation manual** — "a three-way ported active system … a single ART tweeter … two HexaCone-bass/midrange drivers".
5. **MartinLogan Motion 40** brochure — 1 Folded Motion tweeter + 1 midrange + **two** 6.5-inch woofers = 4.
6. **Focal Scala Utopia Evo** data sheet — 1 × 27 cm woofer, 1 × 16.5 cm midrange, 1 × 27 mm tweeter = 3 (the "1/2/3" are feature callouts, not quantities).
7. **JBL JRX225** spec sheet — "JBL M115-8A x 2" plus one 2414H-C compression driver = 3; no passive/active wording.
8. **Yamaha NS-6490** US specification page — 8-inch woofer, 4-inch midrange, 7/8-inch tweeter = 3; 8 Ω for this variant only.
9. **KEF Q750** product page — Uni-Q (MF cone + HF dome), one LF driver, 2 × ABR.
10. **QSC WideLine-8 user manual, TD-000237-00 rev D** — WL3082 "audio power" input, no crossover network; WL212-sw NL8 wiring to transducers, 1100 W continuous, no passive/active statement.

## Outcomes

### Promotions (stored value confirmed by the exact document)

| Record | Field | Value | Source |
| --- | --- | --- | --- |
| `adam-audio-s3v` | driverCount | 3 | S3V product page |
| `adam-s3x` | driverCount | 3 | S3X-V archived page |
| `adam-a8h` | driverCount, active | 3, true | A8H product page |
| `legacy-adam-1` | driverCount | 3 | S3A operation manual (PDF) |
| `martinlogan-motion-40` | driverCount | 4 | Motion 40 brochure |
| `focal-scala-utopia-evo` | driverCount | 3 | Scala Utopia Evo data sheet |
| `jbl-jrx225` | driverCount | 3 | JRX225 spec sheet |
| `yamaha-ns-6490` | driverCount | 3 | Yamaha US specs page |

The earlier `CONFLICT` notes on the three ADAM models and the Motion 40 were arithmetic errors:
the pages list *one of each* driver, and the Motion 40 lists **two** woofers, not three.

### Corrections

- **`kef-q750.driverCount` 5 → 3.** KEF lists a Uni-Q (MF cone + HF dome), one LF driver and two ABRs.
  Passive radiators are not counted, as already recorded for `jbl-charge5`, `jbl-flip6` and
  `klipsch-forte-iv`; the record's own note said so while storing 5.
- **`qsc-wl212-sw.active` false → unknown (retraction).** Neither the WideLine-8 specification sheet nor
  the user manual states passive/active for the subwoofer. The Round 22 manufacturer-verified promotion
  contradicted the record's own Round 8 note ("Active/passive not stated on the sheet; active stays
  null"). The field now carries an `UNSOURCED` provenance with the retraction reason; no value was
  invented in either direction.
- **`qsc-wl3082.active` false retained, re-sourced.** The manual states that "all signal processing must
  be done before connecting audio power to the loudspeaker" and documents only NL8 audio-power inputs,
  with no internal amplification, mains inlet or level control. Value unchanged; source moved from the
  specification sheet to the manual that actually carries the statement.

### JBL LSR32 — the 20 kHz conflict is resolved

The exact owner's manual was re-read end to end. Its **LSR32 Amplitude & Phase** table reads **92 dB at
20 kHz** (28 rows, 20 Hz–20 kHz) and the **LSR32 Acoustic Contribution** fundamental also reads 92 dB.
The 61 dB figure belongs to the **LSR28P** section of the same manual (61 dB at 10 kHz with a blank 20 kHz
row). The "self-conflict" was a mis-read of a different model's table.

The stored 27-row series was also not the LSR32 table: 12 of its 27 values differed (30, 40, 50, 70, 80,
300, 400, 500, 600, 700, 900, 1000 Hz) and it omitted 20 kHz. It has been replaced by the verbatim 28-row
table, now the record's source-backed response series (`pointsStatus: MANUFACTURER_VERIFIED`,
`pointsSourceType: MANUFACTURER`). The previous rows, the exclusion reason and the prior status are
preserved under `frequencyResponse.resolution.priorPoints` and in `round27-value-history.json`.
The manual measures anechoically at 2 m referenced to 1 m; the drive level is not stated, so the series
is normalized shape only and absolute level continues to come from the verified sensitivity field.

### Electro-Voice ELX200-15 — still irreconcilable, still excluded

Both official editions were fetched and their tables transcribed verbatim
(`scripts/research/data/elx200-15-editions-2026-10-19.py`):

| | FR edition | EN edition | Stored series |
| --- | --- | --- | --- |
| Rows | 86 | 87 | 85 |
| 2400 Hz | 93.5 dB | 95 dB | absent |
| 2500 Hz | absent | 95 dB | present |
| 2600 Hz | 94 dB | 95 dB | absent |
| Impedance column | falls to 1.1 Ω | peaks at 110 Ω @ 2500 Hz | — |

The two editions differ at 64 shared frequencies; the stored series matches neither (9 values differ from
FR, 61 from EN). Both sheets state 77 Hz–16 kHz (−3 dB) and 52 Hz–19 kHz (−10 dB), but the tables' own
crossings are 75 Hz–13 kHz / 55 Hz–17 kHz (FR) and 80 Hz–17 kHz / 55 Hz–19 kHz (EN), so the text limits
cannot validate either table. The FR impedance column falls below the 7.0 Ω minimum the same sheet
publishes, which is physically impossible. **No point was written, no alternate series adopted, and
`simulationExcluded` remains `true`.** The comparison is recorded in `disputedPoints.editionComparison`.

### Records left deliberately unchanged

- **Focal Sopra N°2** — the exact sheet states "Sensitivity (2.83V / 1m) 91dB"; the existing
  `MANUFACTURER_VERIFIED` value and reference are correct and were not altered.
- **Focal Scala Utopia Evo `active`**, **JBL JRX225 `active`**, **KEF Q750 `active`** — no explicit
  passive/active wording in the documents; all remain unverified.
- **`legacy-mack-4`** and **`equator-d5`** — held; nothing new was found and no value was invented.
- **Turbosound iP15B** — still no record with that model in the catalogue; the distributor datasheet's
  origin is unresolved, so no reclassification exists to make.
- **Genelec 8331A** — the SOFA/CLF dataset was not obtained, so nothing was imported; the directivity
  lead remains `LEAD_NOT_IMPORTED`.

## Files

| File | Change |
| --- | --- |
| `src/data/speakers.json` | 12 field writes, 2 value changes, LSR32 series replaced, ELX comparison recorded |
| `scripts/research/round27_disputes_data.py` | new — verbatim quotations and every outcome |
| `scripts/research/prepare-round27-batches.py` | new — validates each outcome against the live catalogue |
| `scripts/research/apply-round27-batch.py` | new — applies values, history, queue status and ledger |
| `scripts/research/round27-url-results.json` | new — 10 URLs / 15 field results / 11 value writes |
| `scripts/research/round27-value-history.json` | new — every before/after pair, including the 27 superseded LSR32 rows |
| `scripts/research/round27-field-and-dataset-ledger.json` | new — one row per adjudicated item |
| `scripts/research/queue-url-status.json` | 10 entries rewritten; earlier snapshots preserved |
| `scripts/research/provenance-source-ledger.json` | 2 documents added |
| `scripts/research/provenance-queue.json` | regenerated: 165 URLs / 227 items |
| `RESEARCH-QUEUE.md`, `SPEAKER-DATA-STATUS.md`, `SPEAKER-SOURCES.md`, `AUDIT.md`, `FINAL_VERIFICATION.md` | regenerated by the existing generators |

## Verification

- `npm run typecheck` — clean.
- `npm test` — 82/82 suites.
- `audit:speaker`, `audit:provenance`, `audit:final`, `audit:third-party` — `problems: []`.
- `docs:consistency` — `issues: []`.
- `make-provenance-queue.py` — `records=657 unchecked_items=227 unique_urls=165 warnings=0`.

## Batch 2 — three more queue documents

| URL | Tied fields | Outcome |
| --- | --- | --- |
| Klipsch RF-7 III spec sheet v01 | `legacy-klip-6.driverCount`, `legacy-klip-6.active` | driverCount **promoted** (two 10" woofers + one 1.75" compression driver = 3); `active` NOT_STATED |
| JBL 4430/4435 information sheet | `jbl-4430.active`, `legacy-jbl-6.active` | NOT_STATED — the sheet describes single-amplification and bi-amplification wiring and a recommended amplifier power, never a passive/active classification |
| DALI OBERON owner manual | `dali-oberon-3/5/7.driverCount` | NOT_EXTRACTED — the manual points to "Table 2" for technical specifications, but that table is not present in the retrieved text |

The three DALI driver counts remain unchanged and unverified; nothing was inferred from the carton
contents table or from another Oberon model.

### History-integrity note

The first applier rewrote `round27-value-history.json` from a fresh list on every run, so its own
idempotent re-run (0 writes) emptied the file. Both artifacts were rebuilt from
`round27-url-results.json`, the `queue-url-status.json` snapshots, the live records and the LSR32
`resolution.priorPoints` block by `scripts/research/rebuild-round27-history.py` (14 history entries,
24 ledger rows). The applier now merges into the existing files and de-duplicates instead of
truncating them.

## Batch 3 — one promotion, one documented blocker

- **Triangle Borea BR02** — the exact product page states "2 Drivers: 1 x 25mm silk dome tweeter; 1 x 13 cm
  midwoofer", so `driverCount` 2 is promoted. The same page gives "Sensitivity (dB/W/m): 89dB", i.e. a
  1 W / 1 m reference (not 2.83 V); `active` stays NOT_STATED — the page gives amplifier power and power
  handling but never a passive/active classification.
- **KEF Reference Series Model 103 (1976-77)** — the `assets.kef.com` archive URL serves no document, only
  "redirecting to [kef.com]"; both `driverCount` and `active` are recorded INACCESSIBLE and left unchanged.

### Note on the figures supplied with this brief

The brief quoted 675 CITED fields across 396 URLs, 252 UNSOURCED, ~394 cited URLs and 70 restored
structural values. Those figures are **not present in this repository**: `git fetch` shows the branch tip
is `ef482e9` and `origin/main` contains only a source zip, with no `src/data/speakers.json`. Recounted from
the live file, the backlog is **225 cited fields across 165 URLs**, 193 UNSOURCED and 189 with no
provenance. The work below uses the repository numbers.

## Batch 4 — four more documents, three promotions and one retraction

| Record | Field | Result | Evidence |
| --- | --- | --- | --- |
| `legacy-dyn-4` (Evidence Platinum) | driverCount 8 | **promoted** | Spec block: "Tweeter 2x 28mm Esotar2 / Midrange 2x15 cm MSP / Woofer 4x18 cm MSP" = 8 |
| `dali-opticon-8-mk2` | driverCount 5 | **promoted** | "two 8-inch bass drivers and dedicated 6.5-inch midrange" + hybrid tweeter "marries a 29 mm soft dome tweeter with a custom 17 x 45 mm planar element. Both drivers…" = 5 |
| `martinlogan-esl-x` | driverCount 3 | **promoted** | "XStat electrostatic transducer" + "Twin 8-inch high-excursion woofers" = 3; `active` NOT_STATED |
| `sony-sony-ht-a7000` | driverCount 11 → **null** | **retracted** | The Sony spec page states "Amplifier Channels 11ch" and "Speaker Structure 7.1.2ch" but never enumerates drive units; the stored 11 was the amplifier channel count, not a documented driver complement |

## Batch 5 — the complete Klipsch spec-sheet cluster (13 URLs)

Twelve sheets were retrieved in full; one URL serves no document.

| Sheet | Record | Outcome |
| --- | --- | --- |
| AWR-650-SM | `klipsch-awr650sm` | `active` NOT_STATED |
| Forte IV | `klipsch-forte-iv` | `active` NOT_STATED |
| Heresy IV | `klipsch-heresy-iv` | `active` NOT_STATED |
| R-41M | `legacy-klip-8` | `active` NOT_STATED |
| RP-5000F II | `klipsch-rp-5000f-ii` | `active` NOT_STATED |
| RP-500M II | `klipsch-rp500m` | `active` NOT_STATED |
| RP-500M | `klipsch-rp-500m` | `active` NOT_STATED |
| RP-6000F II | `klipsch-rp6000f` | `active` NOT_STATED |
| RP-600M II | `klipsch-rp600m` | `active` NOT_STATED |
| RP-600M | `klipsch-rp-600m` | `active` NOT_STATED |
| RP-8000F II | `klipsch-rp-8000f-ii` | `active` NOT_STATED |
| RP-8060FA II | `klipsch-rp8060fa` | `active` NOT_STATED |
| Cornwall IV | `klipsch-cornwall-iv` | INACCESSIBLE — S3 `AccessDenied` XML, no PDF |

Every one of the twelve sheets publishes a peak/continuous power-handling figure and passive input
terminals (binding posts, bi-wire/bi-amp) but none writes "passive", "active", "powered" or "built-in
amplification". Power handling is a rating, not a classification, so the fields stay unverified. The
Forte IV sheet's "PASSIVE RADIATOR" line refers to the KD-15 driver that the same table lists as a
"Passive cone radiator" beside the active woofer — it classifies a driver, not the system.

## Queue reporting fix: assessed vs unassessed

`uncheckedItems` counted every `CITED_IN_NOTES_UNCHECKED` field, including fields whose document had
already been opened and found not to state the value. That made the queue look permanently unconverged.
`make-provenance-queue.py` now also reports `assessedItems` (a recorded outcome exists for that exact
record+field) and `unassessedItems`:

```
records=657 unchecked_items=221 (assessed=221, unassessed=0) unique_urls=162 resolved_urls=291 warnings=0
```

Every remaining cited field has been triaged against its document. What remains is that the evidence
did not support the value, not that nobody looked.

## Remaining in this round

221 cited-but-unchecked fields across 162 URLs, 193 unsourced fields, 189 fields with no provenance,
25 distinct response datasets (27 audit blocks) and 51 directivity leads. None of these are claimed
resolved here; they are the next batches.


## Whole-application verification (2026-10-19)

Run against the tree that contains every change in this round:

| Check | Result |
| --- | --- |
| `npm run build` (vite + server + solver worker bundles) | pass — `dist/index.html`, one JS bundle, `dist/server.cjs`, `dist/solverWorker.cjs` |
| `npm run typecheck` | clean |
| `npm test` | 82/82 suites |
| `audit:speaker` / `audit:provenance` / `audit:final` / `audit:third-party` | `problems: []` |
| `docs:release` / `docs:consistency` | regenerated; `issues: []` |
| `release:source` / `release:source:verify` | 601 files, treeSha256 `1e6a269a8d2bdaad36cd50a58c61527e0334082a6eaf7a64a8885caa74207511`, verification `ok: true` |
| `audit:release` | 657 files checked, 0 duplicate ids, 0 duplicate brand+model, `problems: []`, warningCount 0 |
| `npm audit --audit-level=high` | no high/critical findings (8 moderate in the electron-builder toolchain only) |
| dev server (`npm run dev`) | starts on :3000, `/` 200, `/api/health` `{"status":"ok","desktopStorage":false}` |

Data-to-simulation spot check through the real response builder:

| Record | Model provenance | Points | Band | Sensitivity |
| --- | --- | --- | --- | --- |
| `jbl-lsr32` | manufacturer | 28 | 20–20,000 Hz | 90.0 dB, manufacturer |
| `electro-voice-elx200-15` | physically_modeled (envelope) | 31 band points | 77–16,000 Hz | 95 dB, manufacturer |
| `electro-voice-elx200-10` | manufacturer | 71 | 30–20,000 Hz | 90 dB, manufacturer |
| `sony-sony-ht-a7000` | physically_modeled, generic reference | 31 | 20–20,000 Hz | neutral fallback |

The ELX200-15 result is the important one: the disputed 85-point table is **not** consumed by the
simulator — the record falls back to the published-band envelope — while the LSR32 now consumes its
verified manual table. Production startup without cloud credentials still fails fast with the full
configuration list, which is the intended guard rather than a defect.
