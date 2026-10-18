# Research status — Round 22 (2026-10-19)

Generated for the field-level provenance audit. This round continued from Round 21 without
repeating earlier work; every promotion below was made only after opening the exact-model
manufacturer document named in the entry.

## What changed

| Area | Before Round 22 | After Round 22 |
|---|---:|---:|
| Live `CITED_IN_NOTES_UNCHECKED` fields | 672 | **444** |
| — `driverCount` | 378 | **237** |
| — `active` | 294 | **207** |
| Distinct source URLs with outstanding fields | 396 | **290** |
| Live `UNSOURCED` fields | 246 | **192** |
| — `driverCount` | 117 | **87** |
| — `active` | 129 | **105** |
| Live `NO_PROVENANCE` fields | 189 | **189** |
| Live records with at least one outstanding field | 574 | **468** of 657 |

Promotions this round: **228** fields from opened source documents
(`round22-url-results.json` → `round22-value-history.json`) and **54** null values restored from
exact-model manufacturer pages (`round22-structural-batch.json` → `round22-structural-history.json`).
All previous values and provenance objects are preserved in the per-round history files.

## Electro-Voice ZX3 reconciliation

`electro-voice-zx3-60` and `electro-voice-zx3-90` were rechecked against the Electro-Voice Zx3
Owner's Manual, DOC38110265 Rev B (EVI Audio France distributor copy, permitted under owner
decision 1):

- `driverCount = 2` — LF Transducer DVX3121 12 in (305 mm) plus HF Transducer ND2 compression driver.
- `active = false` — System Configuration "Passive or Biamp 2-Way", Speakon connectors, external amplifier.
- `woofer = 12 in`, `sensitivity = 97 dB` (1 W / 1 m, half space; 95 dB full space for the 90 x 50 model), `power = 600 W`, `impedance = 8 ohm`, frequency response 58 Hz – 15 kHz.

All six fields now carry the same `documentOrigin` and `hostingLocation`, and the notes contain a
single `Round 18:` prefix (no duplicated prefixes anywhere in the catalogue). The reconciliation is
recorded in `round18-value-history.json` under `acousticFieldProvenanceReconciliation`; existing
`before` objects are preserved.

## Queue documentation

`RESEARCH-QUEUE.md`, `make-research-queue.mjs`, `make-queue.mjs` and `check-doc-consistency.mjs`
previously filtered records by `overallStatus !== 'PARTIALLY_VERIFIED'`. Because every live record is
`PARTIALLY_VERIFIED`, that produced "0 records, 0 brands" while 468 records still had field-level
work. Queue membership is now derived from the field provenance inventory, and the consistency gate
asserts the same derivation. A zero can no longer be printed while any live field remains
`CITED_IN_NOTES_UNCHECKED`, `UNSOURCED`, or without provenance.

## Sources opened this round

162 URLs were checked; 156 were added to `provenance-source-ledger.json`. Hosts include
KEF, Klipsch, ATC, PMC, Electro-Voice, JBL Professional, QSC, Mackie, Bose Professional,
Dynaudio, Focal, Genelec, L-Acoustics, MartinLogan, Wharfedale, DALI, ADAM Audio and
Bowers & Wilkins. `source-host-allowlist.json` now records 30 established hosts with the
operator evidence for each.

Confirmed limitations, recorded rather than worked around:

- KEF Reference Series 103 and 105.2 archive URLs return HTTP 404 (`INACCESSIBLE`).
- DALI OBERON manual: the specification table is beyond the PDF extractor's 30-page limit
  (`NOT_EXTRACTED`); no OBERON field was changed.
- Genelec 8331A SOFA file: the Zenodo record page is reachable, but the 410.5 MB file download
  endpoint previously returned HTTP 500. No directivity data was imported.
- Mackie CR3 product page returns only a cart overlay; Equator D5 product URL returns HTTP 404.
  Both held records remain on hold.

## Conflicts left unresolved (values not changed)

| Record | Field | Stored | Source reading |
|---|---|---:|---|
| `legacy-klip-6` | driverCount | 3 | RF-7 III sheet lists 2 woofers + 2 compression drivers = 4 |
| `legacy-focal-2` | driverCount | 4 | Electra SW 1000 Be manual describes a single 13 in woofer |
| `focal-scala-utopia-evo` | driverCount | 3 | Sheet lists tweeter + midrange + 2 woofers = 4 |
| `martinlogan-motion-40` | driverCount | 4 | Brochure lists 5 drive units |
| `adam-a8h`, `legacy-adam-1`, `adam-audio-s3v`, `adam-s3x` | driverCount | 3 | Manufacturer pages list 4 drive units |

`atc-scm45a-pro.driverCount` stays 3 and remains pinned by `src/data/speakers.test.ts`; its
specification table lists three driver sizes while the overview and datasheet describe dual
woofers. `jbl-jrx225` and `kef-q750` were verified but left `SUPPORTED_NOT_PROMOTED` because the
counting convention (compression drivers, ABR passive radiators) needs an owner decision.

## Still open

- 444 cited-but-unchecked fields across 290 URLs (225 URLs never opened, 65 opened but still
  carrying open fields).
- 192 null fields (87 `driverCount`, 105 `active`) with no source.
- 189 fields with no provenance object at all (47 `driverCount`, 142 `active`).
- ELX200-15 response row-count reconciliation: still unresolved; the stored 85-point curve remains
  excluded from simulation.
- JBL LSR32 20 kHz self-conflict: still unresolved; response series unchanged.
- 51 directivity leads: 0 imported; Genelec 8331A SOFA remains inaccessible.
