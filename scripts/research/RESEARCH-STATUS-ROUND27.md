# Round 27 — disputed records and settlement of the review backlog

**Date:** 2026-10-19 · **Branch:** `arena/cdfc16bd-nnnnnnnnnn`
**Batch 1 of Round 27:** disputed-record adjudication (10 documents, 15 field outcomes, 12 value writes)

## Counts, recomputed from the repository (not carried over from a brief)

> This table records batch 1 only. The current figures are in "Counts after batch 7" below
> (728 / 221 / 177 / 188; backlog 400 of 657).

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

## Batch 6 — first promotions out of the UNSOURCED bucket

Both fields were UNSOURCED on three Yamaha monitors, so nothing was being replaced: the record held no
claim at all. The HS Series specifications table names each model and states the system type itself.

| Record | Field | Outcome | Evidence |
| --- | --- | --- | --- |
| `yamaha-hs5` | `driverCount` | PROMOTED to 2 | LF 5" cone + HF 1" dome |
| `yamaha-hs5` | `active` | PROMOTED to true | "2-way bi-amp powered studio monitor", 70 W output |
| `yamaha-hs7` | `driverCount` | PROMOTED to 2 | LF 6.5" cone + HF 1" dome |
| `yamaha-hs7` | `active` | PROMOTED to true | "2-way bi-amp powered studio monitor", 95 W output |
| `yamaha-hs8` | `driverCount` | PROMOTED to 2 | LF 8" cone + HF 1" dome |
| `yamaha-hs8` | `active` | PROMOTED to true | "2-way bi-amp powered studio monitor", 120 W output |

Source: `https://usa.yamaha.com/products/proaudio/speakers/hs_series/specs.html`.

### A defect in the applier, found and fixed here

The first run of this batch wrote nothing. `apply-round27-batch.py` only writes a row whose `outcome` is
`PROMOTED`/`CORRECTED` (or whose action is `RESOURCE`/`RETRACT`); this batch arrived with `outcome:
PROMOTE`, so all six rows fell through to the "value kept" branch and were logged without being applied.
The outcome strings were normalised to `PROMOTED` in both the batch module and `round27-url-results.json`,
after which the applier wrote exactly six fields and six values. Re-running the applier is safe: the
LSR32 series block and the ELX200-15 edition block both short-circuit when already recorded.

## Batch 7 — Genelec active monitors and the PreSonus Eris E8 XT

Six records, twelve fields, all previously empty. Each value comes from the exact model's own datasheet;
the active/monitoring-system wording is quoted rather than inferred from the presence of a mains inlet.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `genelec-8050a` | `driverCount` / `active` | 2 / true | "8050A Active Monitoring System", "bi-amplified active monitor system"; 25 mm tweeter + 205 mm bass |
| `genelec-8030a` | `driverCount` / `active` | 2 / true | "8030A Active Monitoring System", "bi-amplified active monitor system"; 19 mm + 130 mm |
| `genelec-1030a` | `driverCount` / `active` | 2 / true | "bi-amplified active monitoring system"; 19 mm metal dome + 170 mm polymer cone |
| `genelec-1032a` | `driverCount` / `active` | 2 / true | "Bi-amplified Active Monitoring System"; specifications list Bass 250 mm + Treble 25 mm |
| `genelec-1029a` | `driverCount` / `active` | 2 / true | "1029A Active Monitoring System"; 19 mm tweeter + 130 mm woofer |
| `presonus-eris-e8` | `driverCount` / `active` | 2 / true | "2-Way Active Studio Monitor"; 8" woven-composite LF + 1.25" silk-dome HF; 140 W Class AB bi-amp |

`genelec-1030a.driverCount` carried no provenance object at all (it was in the no-provenance bucket, not the
UNSOURCED bucket); the applier was extended only in the batch preparation step to accept that case when the
value is `null`, and the write still required the datasheet to state the driver complement explicitly.

## Counts after batch 7

Recomputed from `src/data/speakers.json` (1,314 field slots over 657 records):

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 728 |
| `CITED_IN_NOTES_UNCHECKED` | 221 |
| `UNSOURCED` | 177 |
| no provenance at all | 188 |

Research backlog: 400 of 657 records. Queue: 221 cited-but-unchecked items across 162 URLs, all assessed
(`assessed=221, unassessed=0`), zero consistency warnings.


### Host-policy note

`audio-database.com` is `NOT_MANUFACTURER` in `source-host-allowlist.json` and `cdn.shopify.com` is
likewise `NOT_MANUFACTURER`, so the ten queue items carried by audio-database.com pages and the KRK
Shopify PDFs cannot be promoted to manufacturer-verified even if the value is stated there. They need
either an owner ruling on third-party sources or a manufacturer-hosted copy. `www.genelec.com` is
`ESTABLISHED` and `assets.ctfassets.net` is `ESTABLISHED_FOR_LINKED_DOCUMENTS`, which is why the Genelec
datasheets above were usable.

## Batch 8 — DALI OBERON driver counts and five Genelec monitors

The DALI manual genuinely omits its Table 2, so those three fields had been left `NOT_EXTRACTED` since
Round 12. DALI's own technical-information PDF prints the table for every OBERON model, so the values are
now verified from a different DALI document. The manual URL keeps its outcome, changed to
`RESOLVED_ELSEWHERE` with the resolving source named — the queue checks that outcome explicitly instead
of warning about it.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `dali-oberon-3` | `driverCount` | 2 | 1 x 29 mm dome + 1 x 180 mm (7") mid/bass, 2-way |
| `dali-oberon-5` | `driverCount` | 3 | 1 x 29 mm dome + 2 x 130 mm (5¼") mid/bass, 2-way |
| `dali-oberon7` | `driverCount` | 3 | 1 x 29 mm dome + 2 x 180 mm (7") mid/bass, 2-way |
| `genelec-8040b` | `driverCount` / `active` | 2 / true | "8040B Active Monitoring System"; 19 mm dome + 165 mm cone; 90 W + 90 W |
| `legacy-gen-5` (8050B) | `driverCount` / `active` | 2 / true | manual title "8040B and 8050B Active Monitoring Systems"; 205 mm + 25 mm |
| `genelec-8351a` | `driverCount` / `active` | 4 / true | dual 100 x 215 mm racetrack bass + 120 mm coax mid + 19 mm coax treble; 150/120/90 W |
| `genelec-8260a` | `driverCount` / `active` | 3 / true | 255 mm bass + 120 mm coax mid + 19 mm coax treble; "DSP TRI-AMPLIFIED" |
| `genelec-1032c` | `driverCount` / `active` | 2 / true | ⌀ 250 mm bass + ⌀ 25 mm treble; 250 W + 150 W Class D |

Two documents carried the same 8351A rows; the duplicate rows were collapsed before the applier ran, and
after the first aborted run the results file had to be corrected because the dedupe had also removed the
DALI rows (they legitimately appeared in an earlier round against a different URL). The applier is
idempotent, so re-running after the correction wrote exactly the thirteen missing fields.

## Counts after batch 8

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 741 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 167 |
| no provenance at all | 188 |

Research backlog: 392 of 657 records. Queue: 218 items across 161 URLs, all assessed
(`assessed=218, unassessed=0`), zero consistency warnings. Typecheck clean; `npm test` 82/82 (the first
run failed 15 suites only because the dependency tree had not been reinstalled in this sandbox —
`npm ci` restored `tsc` and the suites passed unchanged).

## Final whole-application pass (2026-10-19, after batch 8)

| Check | Result |
| --- | --- |
| `npm ci` | 743 packages installed; the earlier `tsc: not found` and 15 red suites were a missing toolchain in a fresh sandbox, not a regression |
| `npm run typecheck` | clean |
| `npm test` | 83/83 suites |
| `npm run build` | Vite client bundle, `dist/server.cjs`, `dist/solverWorker.cjs` |
| dev server | `:3000`, `/` 200, `/api/health` `{"status":"ok","desktopStorage":false}` |
| `audit:speaker` / `audit:provenance` / `audit:final` / `audit:third-party` | `problems: []` |
| `docs:release` / `docs:consistency` | regenerated; `issues: []` |
| `release:source` / `release:source:verify` | 602 files, treeSha256 `597848e5d52ebe1cae0a9269ba573f2c626edd3333156e14c9c90d4fdd472105`, verification `ok: true` |
| `audit:release` | 657 records, 0 duplicate ids, 0 duplicate brand+model, `problems: []` |
| `npm audit --audit-level=high` | exit 0; 8 moderate findings, all in the electron-builder toolchain |

### What is still open, stated plainly

* 218 cited fields remain `CITED_IN_NOTES_UNCHECKED` because the documents that carry the citation do
  not state the value (typically `active` on a passive home loudspeaker, where the manual only describes
  connecting to an amplifier). All 218 have a recorded outcome; none is unexamined.
* 167 fields are `UNSOURCED` and 188 carry no provenance at all — 250 records with a data gap. These are
  research backlog, not software defects: the application builds, runs and reports them as unknown
  rather than inventing a value.
* Blocked by host policy: `audio-database.com` and `cdn.shopify.com` are `NOT_MANUFACTURER`, so the JBL
  and KRK pages hosted there cannot be promoted without an owner ruling or a manufacturer copy.
* Unchanged owner rulings: ELX200-15 response series excluded; QSC WL3082/WL212-sw `active` unknown;
  Yamaha NS-6490 8 Ω US-only; Focal Sopra N°2 sensitivity; Genelec 8331A `LEAD_NOT_IMPORTED`.

## Batch 9 — Genelec 8020D/8030C and the QSC specification sheets

Two Genelec records that carried no provenance at all. Both values come from the model's own technical
specification block; the driver dimensions enumerate exactly two transducers and the amplifier line
states the built-in power per band.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `genelec-8020d` | `driverCount` / `active` | 2 / true | ⌀ 105 mm bass + ⌀ 19 mm treble; 50 W + 50 W Class D |
| `genelec-8030c` | `driverCount` / `active` | 2 / true | ⌀ 130 mm bass + ⌀ 19 mm treble; 50 W + 50 W Class D |

### QSC

The QSC product-tree URLs changed: `/solutions-products/.../kla-series/kla12/` and
`/products-solutions/.../kla12/` both redirect to the home page, and `.../spk/e/e110/q_spk_e_110_specs.pdf`
is a 404. The stable locators are the specification PDFs under `/resource-files/productresources/`, which
is what was opened and cited.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `qsc-ks112` | `driverCount` / `active` | 1 / true | "single 12-inch bandpass design subwoofer, powered by a 2000 Watt peak power Class D amplifier module"; "LF Transducer 305 mm (12 in), Cone" |
| `qsc-kla12` | `driverCount` / `active` | 2 / true | "12\" cone transducer" + "1.75\" diaphragm compression driver"; "500 W x 500 W power module", powerCON AC In/Out |
| `qsc-kla181` | `driverCount` / `active` | 1 / true | "18\" cone transducer", HF "—"; "1000 W power module", powerCON AC In/Out |
| `qsc-e110` | `driverCount` / `active` | 2 / false | "1 x 10-inch, 2-way, non-powered"; 254 mm LF driver + 25 mm exit compression driver |
| `qsc-e115` | `driverCount` / `active` | 2 / false | "1 x 15-inch, 2-way, passive"; 381 mm LF driver + 38 mm exit compression driver |
| `qsc-e215` | `driverCount` / `active` | 3 / false | "2 x 15-inch, 2-way, non-powered"; 2 × 381 mm LF + 38 mm exit compression driver |
| `qsc-ad-c820` | `driverCount` / `active` | 2 / false | "Configuration | Passive"; 8" ferrite woofer + 1.4" neodymium compression driver |

### Left unresolved on purpose

* `qsc-gp118-sw`, `qsc-gp212-sw`, `qsc-gp218-sw` and `qsc-wl218-sw` still show `active: null`. Their
  sheets list NL4 inputs and a "recommended power" figure, but none of the text opened prints "passive"
  or "non-powered". Absence of a mains inlet was treated as insufficient to state the field.
* `qsc-wl3082` and `qsc-wl212-sw` were not touched — the owner ruling keeps `active` unknown for them.
* `qsc-e112` and `qsc-e218sw` already carried verified values and were not rewritten.

### Documents checked and deliberately not used

* `focal.com/en/solo6-be-40th` now redirects to the current ST6 **Solo6**, a different product from the
  catalogue's `focal-solo6` "Solo6 Be". Its 6.5" W woofer + 1" beryllium tweeter and 80 W/50 W
  amplification were **not** applied to the Solo6 Be record.
* `mackie.com`'s SRM450 page is the current V-Class 1000 W revision, while `legacy-mack-6` is the
  original SRM450 documented from its own "Active 2-Way" sheet. The page was not used to confirm the
  legacy record's driver count, even though both revisions are two-way.
* `mackie.com/.../cr3.html` and `.../thump15.html` both return the site error page; the CR3 and Thump15
  records stay unsourced.

## Counts after batch 9

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 759 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 157 |
| no provenance at all | 180 |

Batch 9 wrote 18 field values across nine records; no earlier value or provenance entry was replaced.
Research backlog: 383 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
313 source URLs resolved in total. `npm test` 82/82.

## Batch 10 — Yamaha DXR / DXR mkII / DBR

Nine records that had neither a value nor a provenance entry. Two Yamaha USA specification tables
carry every one of them; each model's own row states the power topology and enumerates the drivers.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `yamaha-dxr8`, `dxr10`, `dxr12`, `dxr15` | `driverCount` / `active` | 2 / true | "8/10/12/15\" 2-way, Bi-amp powered speaker, Bass-reflex type"; one cone LF driver + "Diaphragm:1.4\", Type: 1\" throat compression driver" |
| `yamaha-dxr10mkii`, `dxr12mkii`, `dxr15mkii` | `driverCount` / `active` | 2 / true | same "Bi-amp powered speaker" row; LF cone + "Diaphragm:1.75\", Type: 1\" throat compression driver" |
| `yamaha-dbr12`, `dbr15` | `driverCount` / `active` | 2 / true | "2-way, Bi-amp powered speaker, Bass-reflex type"; 12"/15" cone LF driver + 1.4" diaphragm / 1" throat compression driver |

Both pages were read in full (DXR 2/2 chunks, DBR 1/1). No value was inferred from the model number:
the "Bi-amp powered speaker" wording and the built-in dynamic power split (LF 950 W / HF 150 W) are
printed in the tables.

## Counts after batch 10

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 777 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 139 |
| no provenance at all | 180 |

Research backlog: 374 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
315 source URLs resolved in total. `npm test` 82/82.

## Batch 11 — Mackie CR-X and JBL 3 Series MkII

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `mackie-cr3-x`, `cr4-x`, `cr5-x` | `driverCount` | 2 | Owner's manual Appendix B: 3.0 / 4.0 / 5.0 in polypropylene woofer + shared 0.75 in (19 mm) silk-dome tweeter |
| `jbl-305p-mkii` | `driverCount` / `active` | 2 / true | "Powered 5\" Two-Way Studio Monitor"; 5" woofer + 1" neodymium tweeter; "Dual integrated, custom Class-D amplifiers ... 82 watts" |
| `jbl-306p-mkii` | `driverCount` / `active` | 2 / true | "Powered 6\" Two-Way Studio Monitor"; dual Class-D amplifiers, 112 W |
| `jbl-308p-mkii` | `driverCount` / `active` | 2 / true | "Powered 8\" Two-Way Studio Monitor"; dual Class-D amplifiers, 112 W |

### A source defect recorded rather than smoothed over

The JBL 306P and 308P pages reuse the 305P body paragraph verbatim, so both still read
"long-throw 5\" woofer" even though the same pages are headed "Powered 6\"…" and "Powered 8\"…".
The contradictory sentence was **not** used. The driver count rests on the model's own headline
plus "Dual integrated, custom Class-D amplifiers ... custom designed by JBL for each transducer".
Anyone re-checking these records should expect that sentence and not treat it as a second woofer.

### Test updated with the evidence, not around it

`src/data/speakers.test.ts` previously pinned `driverCount: null` for CR3-X / CR4-X / CR5-X, which was
correct while only the quick-start guide had been read. The owner's manual now prints the complement,
so the expectation is 2 and carries a comment naming the manual and the reason `woofer`/`voiceCoil`
remain `UNAVAILABLE` (the response fields still come from the quick-start guide).

## Counts after batch 11

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 786 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 133 |
| no provenance at all | 177 |

Research backlog: 368 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
319 source URLs resolved in total. `npm test` 82/82.

## Batch 12 — Mackie Thump 2022 series and JBL SRX800P

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `mackie-thump212` | `driverCount` / `active` | 2 / true | 12 in / 305 mm ferrite woofer + 1.0 in / 25 mm polymer compression driver; 1400 W Class D (1200 W LF + 200 W HF) |
| `mackie-thump215` | `driverCount` / `active` | 2 / true | 15 in / 381 mm ferrite woofer + 1.0 in / 25 mm polymer compression driver; 1400 W Class D |
| `mackie-thump118s` | `driverCount` / `active` | 1 / true | single 18 in / 457 mm ferrite transducer, no HF device listed; 1400 W Class D |
| `jbl-srx815p` | `driverCount` / `active` | 2 / true | "Self powered 15\", two-way"; 1 × 2275F 15" + 1 × 2432H compression driver; "amplification is integrated" |
| `jbl-srx835p` | `driverCount` / `active` | 3 / true | "Self powered 15\", three-way"; 1 × 2275F + 1 × 2107H + 1 × 2432H |

Both Mackie sheets were read in a single chunk each and the JBL pages in two of three chunks; the
specification tables themselves were in the chunks read. `legacy-mack-5` (the original Thump15) was
**not** touched: the 2022 sheet describes the current Thump212/215, not that earlier product.

## Counts after batch 12

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 796 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 123 |
| no provenance at all | 177 |

Research backlog: 363 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
323 source URLs resolved in total. `npm test` 82/82.

## Batch 13 — JBL M2 and 708P

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `jbl-m2` | `driverCount` / `active` | 2 / **false** | "2-Way Floor Standing or Soffit Mountable"; D2430K dual-diaphragm compression driver + 2216Nd 15" woofer; "The System Requires One Crown® iTech 5000HD power amp for each speaker"; spring-terminal inputs |
| `jbl-708p` | `driverCount` / `active` | 2 / true | HF 2409H + LF 728G 8 in (203 mm); "200W/250W Class D" amplifier power rating; XLR analog and AES3 inputs |

The M2 is the counter-example to the "premium monitor therefore active" assumption: JBL's own page
lists the external Crown amplifier the system requires, so `active` is recorded as **false**.

## Counts after batch 13

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 800 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 119 |
| no provenance at all | 177 |

Research backlog: 361 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
325 source URLs resolved in total.

## Batch 14 — the Neumann KH monitor line

`www.neumann.com` was not in the source-host allowlist. It was added in this round as **ESTABLISHED**
with the operator evidence taken from the site itself ("newsletters from Georg Neumann GmbH") and the
two product pages used as sources. The policy rule — a host may support `MANUFACTURER_VERIFIED` only
when `ESTABLISHED` and that link is recorded — is therefore satisfied before any value was written.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `neumann-kh120` | `driverCount` / `active` | 2 / true | KH 120 A G: 130 mm (5.25") woofer + 25 mm (1") tweeter; 80 W + 80 W amplifiers; "Analog; active" |
| `neumann-kh310` | `driverCount` / `active` | 3 / true | KH 310 A: three-way, crossovers 650 Hz / 2.0 kHz, limiters "for woofer, midrange dome and tweeter"; 210 W / 90 W |
| `neumann-kh-80-dsp` | `driverCount` / `active` | 2 / true | 100 mm (4") woofer + 25 mm (1") tweeter; 120 W / 70 W; "Digital; active" |
| `neumann-kh-120-ii` | `driverCount` / `active` | 2 / true | 130 mm (5.25") woofer + 25 mm (1") tweeter; 145 W / 100 W; page titled "Active Studio Monitor" |
| `neumann-kh-150` | `driverCount` / `active` | 2 / true | 165 mm (6.5") woofer + 25 mm (1") tweeter; built-in woofer/tweeter amplifiers |
| `neumann-kh-420` | `driverCount` / `active` | 3 / true | KH 420: three-way, crossovers 570 Hz / 2.0 kHz, limiters naming midrange dome; 330 W / 140 W |
| `neumann-kh-750-dsp` | `driverCount` / `active` | 1 / true | single 10" long-throw driver; 256 W amplifier; "Digital; active" |

The KH 310 and KH 420 `driverCount` values rest on the three-way designation plus the protection
clause that enumerates woofer, midrange dome and tweeter and the two printed crossover frequencies —
not on a midrange dimension row, which those tables do not print.

## Counts after batch 14

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 814 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 106 |
| no provenance at all | 176 |

Research backlog: 354 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
332 source URLs resolved in total.

## Batch 15 — Bowers & Wilkins 800 Series Diamond (D3 and D4): checked, nothing promotable

Three manufacturer documents were opened in full:

| Document | Models covered | Rows printed |
| --- | --- | --- |
| 800 Series Diamond D4 brochure | 801 D4, 802 D4, 803 D4, 804 D4, 805 D4 | drive units, 8 Ω (min 3.0–4.6 Ω), recommended amplifier power 50–1000 W into 8 Ω |
| 802 D3 information sheet | 802 D3 | drive units, 8 Ω (min 3.0 Ω), 50–500 W into 8 Ω |
| 800 D3 information sheet | 800 D3 | drive units, 8 Ω (min 3.0 Ω), 50–1000 W into 8 Ω |

All seven `active` gaps looked closeable here — a nominal load plus a recommended amplifier power
is what a passive loudspeaker prints — but **the repository forbids that step**:
`src/data/speakers.test.ts` asserts `active === null` for `bw-802d3` and `legacy-bw-7` with the
message *"do not infer passive/active classification from a recommended-amplifier range"*. The
same reasoning covers the five D4 models, so none of the seven fields was written. The
information is real but the classification is not printed anywhere in these documents, so the
gaps stay open and are recorded here rather than converted into a value.

`driverCount` was already resolved for all seven records, so no count was written either.

**Consequence for planning:** Bowers & Wilkins accounts for 19 of the 354 records with an
outstanding field, and almost all of those are `active`. That column cannot be closed for this
brand without a document that prints a passive/active classification (no such row exists in the
D3/D4 literature examined), so future rounds should not re-spend effort here.

## Counts after batch 15

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 814 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 106 |
| no provenance at all | 176 |

Research backlog: 354 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
333 source URLs resolved in total.

## Batch 16 — Focal Shape 40 / 50 / 65

Focal's product sheets print an **"Electronic section" that belongs to the loudspeaker**: a
mid/bass amplifier, a high-frequency amplifier, an IEC mains inlet and a standby circuit. That is
a statement that the cabinet contains its amplifiers — unlike a recommended external amplifier
range, which the repository forbids converting into a passive/active verdict. The same table lists
the transducers, so the driver count is a direct read.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `ath-focal-shape40` | `driverCount` / `active` | 2 / true | 4" (10 cm) Flax woofer + 1" tweeter; 25 W + 25 W Class AB, IEC inlet, standby |
| `focal-shape-50` | `active` | true | 5" (13 cm) woofer; 60 W + 25 W Class AB, IEC inlet, standby (count already 2) |
| `ath-focal-shape65` | `driverCount` / `active` | 2 / true | 6.5" (16.5 cm) Flax woofer + 1" tweeter; 80 W + 25 W Class AB, IEC inlet, standby |

The "double passive radiator" printed for each model is not a driven transducer and is not counted.

## Counts after batch 16

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 819 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 101 |
| no provenance at all | 176 |

Research backlog: 351 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
336 source URLs resolved in total.

## Batch 17 — KEF KC62 and JBL Control 25-1

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `kef-kc62` | `driverCount` / `active` | 2 / true | "two 6.5inch force cancelling drive units powered by 1,000W RMS of specially designed Class D amplification" |
| `jbl-control-25` | `driverCount` | 2 | "Drivers | LF: 135 mm (5.25 in) ... HF: 19 mm (0.75 in)" |

KC62 is self-amplified in KEF's own sentence, so no inference was needed. Control 25-1's table
prints impedance and a power rating but no passive/active row — only the count was written, for
the same reason as batch 15.

## Counts after batch 17

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 822 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 100 |
| no provenance at all | 174 |

Research backlog: 350 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
338 source URLs resolved in total.

## Batch 18 — JBL Control 1 (vintage)

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `jbl-control-1` | `driverCount` | 2 | "Components: 135 mm (5 1/4 in) low frequency loudspeaker, 19 mm (3/4 in) polycarbonate dome tweeter" |

The archive specification sheet states the complement twice (feature list and architectural
specification). It also prints 4 ohms nominal impedance and 150 W power capacity but no
passive/active classification, so `active` stays open under the batch 15 rule.

## Counts after batch 18

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 823 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 100 |
| no provenance at all | 173 |

Research backlog: 350 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
339 source URLs resolved in total.

## Batch 19 — Dynaudio LYD 5 / LYD 7 / LYD 48

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `dynaudio-lyd-5` | `driverCount` | 2 | "Tweeter 1.1in soft dome" + "Midrange/Woofer 5in MSP"; 2-way DSP crossover |
| `dynaudio-lyd-7` | `driverCount` | 2 | "Tweeter 1.1in soft dome" + "Midrange/Woofer 7in MSP"; 2-way DSP crossover |
| `dynaudio-lyd-48` | `driverCount` / `active` | 3 / true | 8in woofer + 4in midrange + 1.1in tweeter; 80 W / 50 W / 50 W amplifier rows and 100–240 V AC input |

The LYD tables print one row per transducer, so the counts are read directly. `active` was
already verified for the LYD 5 and LYD 7; for the LYD 48 the per-band amplifier rows plus an AC
mains input establish that the amplification is inside the cabinet.

## Counts after batch 19

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 827 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 98 |
| no provenance at all | 171 |

Research backlog: 347 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
342 source URLs resolved in total.

## Batch 20 — Meyer Sound LINA and LEOPARD

`docs.meyersound.com` was added to the source-host allowlist in this batch (123 hosts) with the
manufacturer's own documentation portal as operator evidence. Both datasheets state the design in
words — *"The loudspeaker shall be a compact, self-powered, linear, low-distortion, line array
loudspeaker"* — and then enumerate the transducers and the internal amplifier.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `meyer-sound-lina` | `driverCount` / `active` | 3 / true | Two 6.5-inch cone drivers + one 3-inch compression driver; "self-powered"; 3-channel class-D, 1950 W peak |
| `meyer-sound-leopard` | `driverCount` / `active` | 3 / true | Two 9-inch cone drivers + one 3-inch compression driver; "self-powered"; 3-channel class-D, 3900 W peak |

The legacy UPA-1P and UPJ-1P remain open: their documentation on the same site is distributed only
as ZIP archives, which this environment cannot open.

## Counts after batch 20

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 831 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 94 |
| no provenance at all | 171 |

Research backlog: 345 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
344 source URLs resolved in total.

## Batch 21 — Marshall Acton III / Stanmore III / Woburn III: checked, nothing promotable

Marshall's product pages print a POWER AMPLIFIERS block that names the amplifier feeding each
transducer group:

| Model | POWER AMPLIFIERS rows |
| --- | --- |
| Acton III | One 30 W amplifier for the woofer; two 15 W amplifiers for the tweeters |
| Stanmore III | One 50 W amplifier for the woofer; two 15 W amplifiers for the tweeters |
| Woburn III | One 90 W woofer amplifier; two 15 W midrange amplifiers; two 15 W tweeter amplifiers |

Reading a driver complement out of that block would be a guess about how many drive units each
channel group feeds, and **the repository forbids it**: `src/data/speakers.test.ts` asserts
`driverCount === null` for all three models with the message *"do not infer driver count from
amplifier channels"*. No value was written; the three URLs are recorded as checked so they close.

## Counts after batch 21

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 831 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 94 |
| no provenance at all | 171 |

Research backlog: 345 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
347 source URLs resolved in total.

## Batch 22 — Celestion and Jensen guitar loudspeakers

A guitar speaker sold as a component is one loudspeaker chassis, not a multi-way system. Each page
below prints a single-chassis specification block (one nominal diameter, one magnet, one voice coil,
one basket, mounting holes for that one chassis), so the count is read off the page rather than
inferred from a cabinet.

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `celestion-v30` | `driverCount` | 1 | "12 inch 60W Guitar Speaker"; one 305 mm chassis, one 50 oz ceramic magnet, one 1.75 in voice coil |
| `celestion-greenback` | `driverCount` | 1 | "12 inch 25W Guitar Speaker"; one 305 mm chassis, 35 oz magnet, 1.75 in voice coil |
| `celestion-g12h30` | `driverCount` | 1 | "G12H Anniversary - 12 inch 30W Guitar Speaker"; same single-chassis block already used for its other fields |
| `jensen-p12n` | `driverCount` | 1 | "12" - 50 W Vintage Alnico Loudspeaker"; one 307 mm chassis, one 38 mm voice coil |
| `jensen-p10r` | `driverCount` | 1 | "10" - 25 W Vintage Alnico Loudspeaker"; one 259 mm chassis, one 25 mm voice coil |

`eminence-legend` could not be advanced: the recorded collection URL
(`eminence.com/collections/legend-series`) now returns the store's 404 page, so it is recorded as
inaccessible rather than re-sourced from a reseller.

## Counts after batch 22

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 836 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 89 |
| no provenance at all | 171 |

Research backlog: 345 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
353 source URLs resolved in total.

## Batch 23 — JBL 4429, JBL L112, Klipsch RP-8000F

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `jbl-4429` | `driverCount` | 3 | General Specifications rows: 300 mm woofer 1200FE-8, 50 mm HF 175Nd-3, 19 mm UHF 138Nd |
| `jbl-l112` | `driverCount` | 3 | Manual COMPONENTS: 300 mm low frequency, 130 mm midrange, 25 mm high-frequency dome |
| `klipsch-rp8000f` | `driverCount` | 3 | Spec sheet: "1\" Titanium LTS Vented Tweeter" + "Dual 8\" Cerametalic Cone Woofers" |

Two documents needed a caveat rather than a value:

- The **JBL 4429 page carries two contradictory specification blocks** — the General Specifications
  give 40 Hz–45 kHz, 91 dB and crossovers at 800 Hz / 7 kHz, while a second "Audio Specifications"
  block gives 40 Hz–40 kHz, 93 dB and 2 kHz / 5 kHz. The driver list is identical in both, so the
  count is safe; the conflicting rows were not used for anything.
- The **recorded source for `jbl-l100` no longer resolves**: the exact `L100_Century_Owners_Manual.pdf`
  URL now returns JBL's "404 - URL Error" page. Its existing verified fields are left untouched —
  they were read from that document while it was served — but the driver complement cannot be
  re-read from it, so `jbl-l100.driverCount` stays open rather than being filled from a reseller
  summary of the same manual.

## Counts after batch 23

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 839 |
| `CITED_IN_NOTES_UNCHECKED` | 218 |
| `UNSOURCED` | 86 |
| no provenance at all | 171 |

Research backlog: 345 of 657 records. Queue: 218 items across 161 URLs, all assessed, zero warnings,
357 source URLs resolved in total.

## Batch 24 — Bose 901 Series VI, REL S/812, JL Audio Fathom f113v2

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `bose-901-series-vi` | `driverCount` | 9 | Owner guide, "Technical information → Transducer complement": "Nine (9) 4½" (11.4 cm) full-range Helical Voice Coil drivers in each cabinet" |
| `rel-s812` | `driverCount` | 1 | Brochure: one front-firing 12 in. active driver; the 12 in. down-firing passive radiator is not a driven transducer and is not counted |
| `rel-s812` | `active` | true (provenance upgraded) | Brochure "TYPE: Front-firing active woofer, down-firing passive radiator" plus NextGen5 Class D amplifier at 800 W RMS |

Caveats and limits:

- **Bose**: the Technical information page was re-read in full (chunk 4 of 9) and the transducer row is
  unambiguous: nine full-range drivers per cabinet. The same page states 8 Ω nominal, "Rated 250 watts
  IEC" and compatibility with 10–450 W RMS amplifiers; the 901 is driven by an external amplifier and
  its "active equalizer" is a separate outboard unit. `active` was left alone: amplifier compatibility
  is not treated as a statement that the speaker is passive, and no promotion was made for that field.
- **REL**: the recorded `rel.net` brochure URL was opened again and redirects to REL's Shopify CDN
  copy (`cdn.shopify.com/.../S812-brochure.pdf`); the final URL and the full specification table were
  observed. The promotion is recorded against the manufacturer URL already used for `rel-s812.power`.
  Driver count follows the passive-radiator convention already applied to `jbl-charge5`, `jbl-flip6`,
  `klipsch-forte-iv`, the KEF R3 and the Mackie HR624.
- **JL Audio**: the recorded Fathom f113v2 product URL now redirects to Garmin's JL Audio category
  page, which lists ranges rather than the product. No specification was read and no field was
  written; the URL is recorded INACCESSIBLE rather than replaced with a reseller copy.
- **Test updated with the evidence, not around it**: `src/data/speakers.test.ts` previously asserted
  `rel-s812.driverCount === null` with the comment "retain uncertainty between the active woofer and
  passive radiator count". The repository now has a settled convention (driven transducers only,
  recorded on `jbl-charge5`, `jbl-flip6`, `klipsch-forte-iv` and the KEF R3), so the assertion is now
  `1`, and the test additionally asserts the new note's passive-radiator sentence. Its other checks
  (active, 800 W amplifier-output role and source, 12-inch woofer, 19 Hz extension with no upper
  limit, no response points, null sensitivity and impedance) are unchanged.

The queue status history was also repaired: repeated apply runs had appended 1,871 byte-identical
adjacent snapshots (the file had grown to 4.4 MB). Those duplicates were removed while every distinct
prior entry was retained (now 187 snapshots, 960 KB), and `apply-round27-batch.py` now snapshots only
when the previous entry belongs to an earlier round, matching `apply-queue-batch.py`.

## Counts after batch 24

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 842 |
| `CITED_IN_NOTES_UNCHECKED` | 217 |
| `UNSOURCED` | 85 |
| no provenance at all | 170 |

Research backlog: 344 of 657 records. Queue: 217 items across 160 URLs, all assessed, zero warnings,
361 source URLs resolved in total. Counts cover the two audited scalar fields (`active`,
`driverCount`) across all 657 records.

## Batch 25 — DALI OBERON 1 and OBERON 9; Sonetto and Tour X dead ends

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| `dali-oberon-1` | `driverCount` | 2 | Discontinued-product page: "2-way", "1 x 29 mm soft dome" HF and "1 x 5¼ inch" low/mid |
| `dali-oberon-9` | `driverCount` | 4 | Discontinued-product page: "3-way", "2 x 9 inch / 1 x 7 inch" LF/MF and "1 x 29 mm soft dome" HF |

`active` was not promoted for either model. Both pages give a nominal impedance and a recommended
amplifier-power range but never use passive, active, powered or built-in-amplification wording, and
the repository rule forbids inferring active status from a recommended-amplifier range.

Two dead ends were recorded rather than converted into values:

- **Sonus faber Sonetto first generation**: the official owner manual was located on the product-guides
  page and opened. Its declaration covers the "passive loudspeaker system" models VIII, V, III, II and
  I, but the section 6 technical-information table on page 34 is absent from the extracted text of the
  six opened chunks, so no driver row could be read. The PDF is served from `a.storyblok.com`, a
  multi-tenant CMS host that the source-host policy does not treat as a manufacturer host, so even a
  readable table would not have been promotion-grade. No field was written.
- **Electro-Voice Tour X**: the recorded `products.electrovoice.com/na/en/tx1122` URL now redirects to
  the current electrovoice.com homepage, and the `la/en` path returns an Application Gateway 404. The
  fullcompass copies remain the only opened support for those counts and stay SUPPORTED_NOT_PROMOTED;
  no value was taken from a reseller or from a search-result snippet.

## Batch 26 (2026-10-19)

One field promoted, four URLs recorded.

| Record | Field | Result | Source |
| --- | --- | --- | --- |
| `atc-scm45a-pro` | `driverCount` | 3, `MANUFACTURER_VERIFIED` | ATC SCM45A Pro product page |

- **ATC SCM45A Pro**: the exact-model page lists `Drivers: HF 1"/25mm Dual-Suspension 'S-Spec', Mid
  3"/75mm Soft Dome, LF 6.5"/164mm short-coil carbon paper cone` and describes the model as an
  "active 3-way studio monitor" with a 150 W/60 W/25 W tri-amp pack. One HF, one mid and one LF
  transducer: three driven transducers. The value matched the count already recorded, so this changed
  provenance only.
- **KEF legacy product paths**: `international.kef.com/products/ls50` redirects to the JavaScript
  product-archive selector page, and `us.kef.com/products/{ls50,reference-1,reference-5}` return KEF's
  404. The product-archive PDFs (`assets.kef.com/pdf_doc/product-archive/1970s/...`) answer with an
  HTML "redirecting to kef.com" stub instead of the document. No KEF value was written.
- **Marshall 1936 2x12**, **Polk Signature S60**, **IK Multimedia iLoud MTM** (original): re-checked
  because their queue items are still open. Marshall returns "Page not found", Polk returns its
  "wires crossed" error page, and the original iLoud MTM route now redirects to the **MKII** product
  page. The MKII page does state a three-transducer MTM complement, but it is a different model, so no
  value was inferred for the original from it.

## Batch 27 (2026-10-19)

Four fields promoted from three manufacturer pages.

| Record | Field | Result | Source |
| --- | --- | --- | --- |
| `barefoot-micromain27` | `active` | true, `MANUFACTURER_VERIFIED` | Barefoot Sound product page |
| `barefoot-micromain27` | `driverCount` | 5, `MANUFACTURER_VERIFIED` | Barefoot Sound product page |
| `sonus-faber-sonetto-i` | `active` | false, `MANUFACTURER_VERIFIED` | Sonus faber Sonetto collection |
| `sonus-faber-sonetto-ii` | `active` | false, `MANUFACTURER_VERIFIED` | Sonus faber Sonetto collection |

- **Barefoot MicroMain27**: "3.5-way active monitor"; the TECH SPECS table lists a 1" tweeter, two 5.25"
  midbass units and two 10" subwoofers, each with its own amplifier (180/250/250/500 W), and the page
  states "5 drive units" in its own words. Both `active` and `driverCount` were empty before this batch.
- **Sonus faber Sonetto I / II**: the collection page describes Sonetto I as "A compact passive
  bookshelf speaker" and Sonetto II as "A passive bookshelf speaker". The records carry no generation
  suffix; the first-generation manual declares the same family passive and this page is the second
  generation, so both possible generations agree and no value is transferred between products.
- **Olympica III**: the product page now serves the "Olympica G3 III" generation while the record is
  the earlier Olympica III. Its four-transducer table was read but not used; there is no G3 record to
  attach it to.

Searched and rejected in the same batch (no value taken):
- KEF legacy product paths (`ls50`, `reference-1`, `reference-5`) and the product-archive PDFs still
  serve the 404/redirect stubs recorded in batch 26.
- The KRK product slugs `rokit-5-g4` and `rokit-8-g4` return 404; the records are G1/G3 and the current
  site only carries later generations.
- Wharfedale Linton / Diamond 12.1, Triangle Borea BR02/BR03, Paradigm Monitor SE 6000F, MartinLogan
  Motion 60XT, Danley SH96 and Funktion-One RES 2 never use the words passive/active/powered in their
  served pages, so their `active` fields stay open.

## Counts after batch 27

| Status | Fields |
| --- | ---: |
| `MANUFACTURER_VERIFIED` | 849 |
| `CITED_IN_NOTES_UNCHECKED` | 214 |
| `UNSOURCED` | 83 |
| no provenance at all | 168 |

Research backlog: 342 of 657 records. Queue: 214 items across 159 URLs, all assessed, zero warnings,
373 source URLs resolved in total. URL result file: 114 entries.

## Remaining in this round

214 cited-but-unchecked fields across 159 URLs (all assessed, 0 unassessed; see batch 8), 83 unsourced fields, 168 fields with no provenance,
25 distinct response datasets (27 audit blocks) and 51 directivity leads. None of these are claimed
resolved here; they are the next batches.


## Whole-application verification (2026-10-19)

Run against the tree that contains every change in this round:

| Check | Result |
| --- | --- |
| `npm run build` (vite + server + solver worker bundles) | pass — `dist/index.html`, one JS bundle, `dist/server.cjs`, `dist/solverWorker.cjs` |
| `npm run validate:directivity` | **FAIL** (open gate): forward 20.02 dB / backward -21.17 dB against a specified 30 dB; up from -0.67/+0.87 before the equivalent-source rewrite |
| `npm run typecheck` | clean |
| `npm test` | 83/83 suites |
| `audit:speaker` / `audit:provenance` / `audit:final` / `audit:third-party` | `problems: []` |
| `docs:release` / `docs:consistency` | regenerated; `issues: []` |
| `release:source` / `release:source:verify` | 624 files, treeSha256 `8f40f6874ebc8af1cb0a12b6a9f4ffb2d0992d332eb81a5feb67f4242cd02162`, verification `ok: true` |
| `audit:release` | 657 files checked, 0 duplicate ids, 0 duplicate brand+model, `problems: []`, warningCount 0 |
| `npm audit --audit-level=high` | no high/critical findings (8 moderate in the electron-builder toolchain only) |
| dev server (`npm run dev`) | starts on :3000, `/` 200, `/api/health` `{"status":"ok","desktopStorage":false}` |
| `APP_URL=… node scripts/production-smoke.mjs` | PASS health, public validation, Cloud Tasks 403 |
| `APP_URL=… SMOKE_RUN_SOLVER=true node scripts/production-smoke.mjs` | PASS end to end: anonymous submission, capability authorization, solver completion, artifact retrieval, report export |

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
