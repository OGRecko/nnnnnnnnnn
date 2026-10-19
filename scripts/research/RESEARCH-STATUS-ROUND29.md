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

The inventory also counted ids that exist both in `speakers.json` and in an old `removed-*.json` snapshot
(`legacy-jbl-6`). Those rows are now live-only; `legacy-jbl-6.active` was promoted from the same 4430 page
in batch 34, and the mislabelled `legacy-kef-3` rows are `INACCESSIBLE` (it is a live record).

## Batch 35 — Bose 802 Series II (distributor-hosted Bose document)

`https://www.walkersound.co.uk/PDF/Bose_802_MkII.pdf` is a Bose technical information sheet hosted by a UK
distributor. Because the host is not Bose, the new third-party tier applies:

* "Each 802 Series II loudspeaker uses eight 4-1/2" full-range drivers mounted in symmetric vertical pairs"
  → `driverCount` 8, **THIRD_PARTY_VERIFIED**.
* "Recommended amplifier power 240W minimum, 480W maximum", 240 W continuous pink-noise rating, 1/4-inch
  phone and XLR inputs, and active equalization performed by the separate 802C Series II controller
  → `active` false, **THIRD_PARTY_VERIFIED**.

Neither field was labelled MANUFACTURER_VERIFIED: the host is a distributor, exactly the case the policy is
meant to separate. Ledger: `round29-third-party-ledger.json`; history: `round29-value-history.json`.

## Batch 36 — three explicit third-party documents

| Record | Fields | Value | Source (host class) | Quote |
| --- | --- | --- | --- | --- |
| jbl-4350 | driverCount / active | 5 / false | audio-database.com (REPUTABLE_DATABASE) | "Method: 4-Way, 5-Speaker"; "In addition to the power amplifier, a divider 5231 or 5232 ... [is] required" |
| mackie-hr824 | driverCount / active | 2 / true | soundonsound.com review (THIRD_PARTY) | "a compact, two-way active nearfield monitor"; 8.75" woofer + 1" dome |
| jbl-eon15 | driverCount / active | 2 / false | warehousesound.com copy of the JBL sheet (THIRD_PARTY) | "The EON 15 is a 15 inch two-way passive speaker system" |

## Batch 37 — KRK documents on a Shopify CDN

All three are KRK publications served from `cdn.shopify.com` (not a KRK host), so the third-party tier
applies: `krk-7000` 2 / false ("Crossover: Passive 2-way"); `krk-rokit-5` 2 / true ("AMPLIFIER Power
Rating (HF/LF) 15 watts / 30 watts", IEC mains); `krk-rokit-8` 2 / true ("System type Active Studio
Monitor"). Six fields promoted.

## Batch 38 — KEF LS50 specification page; two dead pages

* `kef-ls50.driverCount` 2 — Stereophile sidebar ("Two-way ... 1-inch vented aluminium-dome tweeter,
  5.25-inch alloy-cone woofer"). Promoted to THIRD_PARTY_VERIFIED.
* `kef-ls50.active` — only "Amplifier requirements: 25-100W"; no passive/powered wording → NOT_STATED.
* `polk-signature-s60` — polkaudio.com still renders "Sorry, we've got our wires crossed."; both fields
  INACCESSIBLE.
* `elac-uni-fi-ub5.active` — the sell sheet has no passive/powered statement → NOT_STATED; the
  driverCount ambiguity (2 vs 3 transducers) stands.

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
| `CITED_IN_NOTES_UNCHECKED` | 247 | **230** |
| `UNSOURCED` | 81 (73 after policy) | **71** |
| `THIRD_PARTY_VERIFIED` | 24 | **43** |
| `NO_PROVENANCE` | 363 | 363 |
| queue items | 212 / 157 URLs | **195 / 149 URLs** |
| records with backlog | 336 of 657 | **326 of 657** |

`npm test`, typecheck, both audit scripts and the release-docs generators are run after every batch; no
values were written by an audit script and no test was relaxed.

## Still open

- 71 `UNSOURCED` fields and 168 no-provenance nulls remain. This round recorded 12 documented outcomes for
  that pool: 8 assessments (ATC, Wilson, Polk, Dutch & Dutch, EV SX300 ×2, EV Eliminator ×2) that stay null,
  and 4 promotions on explicit evidence (EV EKX-15P driverCount/active with MANUFACTURER_VERIFIED; Bose 802
  Series II driverCount/active with THIRD_PARTY_VERIFIED).
- 51 directivity leads (0 imported), the 9 archive ZIPs, Genelec 8331A SOFA (MD5 confirmed on the source).
- 27 response-dataset blocks (24 active series, 25 records) and the ELX200-15 exclusion.
- The ~2,4xx MV fields have not been re-audited field-by-field; the queue above only covers
  `driverCount`/`active`.
