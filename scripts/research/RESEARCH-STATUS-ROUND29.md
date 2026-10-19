# Research status — Round 29 (2026-10-19)

Continuation of the backlog brief started in `RESEARCH-STATUS-ROUND28.md`. Round 29 introduces a documented
third-party tier for `driverCount`/`active`, then processes the only fields where an exact-model document
states the value explicitly. **The backlog is not complete**; the counts below are the honest state after
this round's batches.

## Policy: `THIRD_PARTY_VERIFIED` (new tier)

`PROVENANCE-POLICY.md` defines the tier and its six conditions (exact model/revision, explicit field-level
statement, retained https URL, allowed source type, quoted evidence in the note, auditable ledger entry).
Conflicting sources leave the field unresolved; the tier is legal only for `driverCount` and `active`, the
two fields whose provenance objects support it. `MANUFACTURER_VERIFIED` remains exclusive to manufacturer
hosts or owner-approved manufacturer copies.

Round 29 applied the tier once, to the four records whose held evidence was already documented:

| Record | Field | Value | Source type | Note |
| --- | --- | --- | --- | --- |
| legacy-mack-4 | driverCount / active | 2 / true | THIRD_PARTY | pdf-manuals Mackie CR manual copy |
| legacy-mack-5 | driverCount / active | 2 / true | THIRD_PARTY | proacousticsusa Thump15 sheet |
| equator-d5 | driverCount / active | 2 / true | THIRD_PARTY | gear4music "Active Studio Monitors with Internal DSP" |
| beolab-5 | driverCount / active | 4 / true | REPUTABLE_DATABASE | B&O brochure hosted on abt.com |

Eight fields left `UNSOURCED`; each note quotes the document and explains why an MV source was not
available. History: `round29-value-history.json`.

## Batch 30 — manufacturer hosts, explicit evidence only

Documents opened this round: Yamaha NS-690/NS-5000 history, KEF Q150/Q350 product pages, Marshall 1936
(retry), Yamaha studio-monitor history (retry), ELAC Uni-Fi sell sheet.

| Record | Field | Outcome | Evidence |
| --- | --- | --- | --- |
| legacy-yam-3 | driverCount | **PROMOTED 3** (MV) | "30 cm (12") 3-way bookshelf design" with soft-dome tweeter and midrange |
| kef-q150 | active | NOT_STATED | "Amplifier Requirements 10-100W" only; no passive/powered wording |
| kef-q350 | active | NOT_STATED | same template |
| marshall-marshall-1936 | driverCount / active | INACCESSIBLE | marshall.com product page still 404 |
| legacy-yam-2 (NS-10M) | driverCount | INACCESSIBLE | hub.yamaha.com article 404 |
| elac-uni-fi-ub5 | driverCount | CONFLICT | concentric tweeter/midrange makes 2 vs 3 transducers ambiguous |

## Batch 31 — no-provenance nulls, explicit evidence only

| Record | Field | Outcome | Evidence |
| --- | --- | --- | --- |
| electro-voice-ekx-15p | driverCount / active | **PROMOTED 2 / true** (MV) | "Powered 15" 2-Way Loudspeaker"; EVS-15M woofer + DH-1M compression driver |
| atc-scm19 | active | NOT_STATED | "Recommended Power Amplifier" and binding posts only |
| wilson-watt-puppy | active | NOT_STATED | "Minimum Amplifier Power 7 Watts" only |
| polk-rti-a7 | active | INACCESSIBLE | archive page renders "wires crossed" |
| dutch-and-dutch-8c | driverCount | NO_SPEC_TABLE | storefront page has no driver table; /8c/ is 404 |
| eV-sx300, eV-eliminator | driverCount / active | INACCESSIBLE | electrovoice.com product pages return an empty shell |

Outcome ledger (no provenance objects for unresolved fields): `round29-unsourced-ledger.json`.

## Batch 32 — JBL 4310 manual re-read (loc.gov)

Round 12 recorded "passive/active not stated". The same PDF page says: "The loudspeaker system shall consist
of three direct-radiator transducers and frequency dividing network installed in a tube-ported enclosure",
"driven by a 50 Watt sine wave signal", "rated capacity of 50 watts program material". That is a passive
system, and it confirms the three transducers.

Both `jbl-4310` fields remain `CITED_IN_NOTES_UNCHECKED` because tile.loc.gov is not a manufacturer host
(Round 14 host policy). The queue rows move from NOT_STATED to `SUPPORTED_NOT_PROMOTED`; the previous
round-12 evidence string is snapshotted in the URL's history. The two `legacy-jbl-3` rows are marked
`RECORD_ARCHIVED` (that record exists only in `removed-owner-2026-10-13-decisions.json`).

## Batch 33 — JBL 4430/4435 (jblpro.com, manufacturer)

"The frequency dividing network ... has a crossover frequency of 1 kHz"; "Maximum Power Input / Single
Amplification / Continuous Program: 300 W (4430), 375 W (4435)"; "Recommended Amplifier Power"; "A switch ...
allows the monitor to be biamplified." → passive.

`jbl-4430.active` **promoted false** (MV). `legacy-jbl-6` (duplicate 4430 record) **promoted false** in
batch 34 from the same page.

KEF archive PDFs (Model 105.2, Model 103) still answer with "redirecting to kef.com" and serve nothing:
`kef-105` and `legacy-kef-3` stay `INACCESSIBLE`.

## Tool fixes in this round

- `make-provenance-queue.py`: accepts `RECORD_ARCHIVED` outcomes and verifies the record really is retired.
- `build-field-provenance-inventory.py`: no longer double-counts ids that exist both in `speakers.json` and
  in an older `removed-*.json` snapshot (e.g. `legacy-jbl-6`); live rows are the only writable ones.
- `build-field-provenance-inventory.py`: archive rows keep their own `location` so the work list can be
  sorted by live fields.

## Counts after this round

| Status | Before (Round 28 tip) | Now |
| --- | --- | --- |
| `MANUFACTURER_VERIFIED` | 2422 | **2426** |
| `CITED_IN_NOTES_UNCHECKED` | 247 | **245** |
| `UNSOURCED` | 81 (73 after policy) | **71** |
| `THIRD_PARTY_VERIFIED` | 24 | **28** |
| `NO_PROVENANCE` | 363 | 363 |
| queue items | 212 / 157 URLs | **210 / 156 URLs** |
| records with backlog | 336 of 657 | **333 of 657** |

`npm test`, typecheck, both audit scripts and the release-docs generators are run after every batch; no
values were written by an audit script and no test was relaxed.

## Still open

- 71 `UNSOURCED` fields and 168 no-provenance nulls remain; this round assessed 14 of them with documented
  outcomes, not values.
- 51 directivity leads (0 imported), the 9 archive ZIPs, Genelec 8331A SOFA (MD5 confirmed on the source).
- 27 response-dataset blocks (24 active series, 25 records) and the ELX200-15 exclusion.
- The ~2,4xx MV fields have not been re-audited field-by-field; the queue above only covers
  `driverCount`/`active`.
