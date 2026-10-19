# Research status — Round 26 (2026-10-19)

Round 26 finished the `driverCount` / `active` provenance queue. **Every outstanding item in
`scripts/research/provenance-queue.json` has now been assessed at least once** — the queue reports
zero `UNASSESSED` items for the first time. What remains is evidence that is real but not
promotable (support-only hosts) or explicit non-statements, not unopened work.

## Method

* 46 URLs opened: 3 manufacturer/distributor documents that could promote, 43 dealer, archive,
  review or database pages recorded as supporting only.
* 79 field results: **18 PROMOTED**, 61 recorded without a write (SUPPORTED_NOT_PROMOTED 33,
  NOT_STATED 24, NOT_EXTRACTED 2, INACCESSIBLE 2).
* The same rules as Rounds 22–25 applied: promotion only from the manufacturer's own host, or from
  an owner-approved copy of the exact-model manufacturer manual (Owner Decision 1). Dealer,
  review, museum and enthusiast-database pages corroborate a value but never promote it.
* `active` was promoted only where the document said powered/active, showed a built-in amplifier
  power rating, or stated that the loudspeaker is driven from an external amplifier/controller.
  A recommended-amplifier-power range or a cabinet power-handling figure alone was recorded as
  NOT_STATED.

## Promotions (18)

| Record | Field | Value | Source and exact evidence |
| --- | --- | --- | --- |
| lacoustics-arcs-ii | driverCount | 2 | Sisme (L-Acoustics distributor) ARCS II data sheet: "one 15'' neodymium LF driver … and one 3'' neodymium diaphragm compression driver" |
| lacoustics-arcs-ii | active | true | Same sheet: "based on an active 2-way design", "exclusively driven and bi-amplified by the LA8 amplified controller" |
| legacy-la-3 (KARA) | driverCount | 3 | Pro Music (L-Acoustics distributor) KARA manual App. C: "LF: 2 × 8"", "HF: 1 × 3"" compression driver |
| revel-ultima-salon2 | active | false | Revel owner's manual: input terminals take "connections from the associated power amplifier(s)"; single-wired, bi-wired or bi-amplified only |
| jl-audio-10w3v3 | driverCount / active | 1 / false | JL Audio 10W3v3 manual: one subwoofer driver per impedance variant; bi-amplified with external amplifiers |
| jl-audio-12w7 | driverCount / active | 1 / false | JL Audio W7AE manual: "RECOMMENDED CONTINUOUS (RMS) POWER RANGE FOR ONE SUBWOOFER DRIVER" |
| jl-audio-12w3v3 | driverCount / active | 1 / false | JL Audio 12W3v3 manual: single 12-inch driver, 500 W continuous, bi-amplified system |
| jl-audio-c1-650 | driverCount / active | 2 / false | JL Audio C1-650 manual: one 6.5" woofer + one 19 mm tweeter per channel, passive in-line high-pass |
| jl-audio-c2-650 | driverCount / active | 2 / false | JL Audio C2-650 manual: one 6.5" woofer + one 19 mm tweeter, passive C2 crossover fed from amplifier output |
| jl-audio-c3-650 | driverCount / active | 2 / false | JL Audio C3-650 manual: one 6.5" woofer + one 25 mm tweeter, passive LC crossover |
| jl-audio-c5-650 | driverCount / active | 2 / false | JL Audio C5-650 manual: one 6.5" woofer + one 19 mm tweeter, passive C5 crossover |

All seven JL Audio promotions use the manufacturer's own owner's manual, served verbatim by an
authorized JL Audio dealer and recorded under the DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL class with
Owner Decision 1. The two L-Acoustics promotions use the manufacturer's data sheet/manual served by
L-Acoustics distributors.

## Recorded without a write (61)

* **SUPPORTED_NOT_PROMOTED (33)** — the document states the value but the host cannot promote:
  audio-database Focal Chorus 707 (2), JBL 4350 (5, plus "multi-amplifier system" for `active`),
  L16 (2), D130 (1), KEF Model 104 (2); HiFi Engine Pioneer CS-99A (6), CS-88A (6), Yamaha NS-500
  (2), ProAc Response D2 (2), Boston VR-M50 (2); ManualsLib Olympica III (4, series manual);
  Manualzz EV Sentry 500 (2), Tannoy System 600 (2), Magneplanar MG-20.1 (`active`, review copy);
  ManualMachine Spendor SP-100 (3); Manualsnet KEF LS3/5A (2); KRK ROKIT 5 G1 (2) and ROKIT 8 G3
  (2); Kali LP-6 (2); LG S95TR (17 units); Vox V212BN (2); Meyer MJF-212 (3, self-powered);
  KEF Reference 1 (3); Sonus Faber Guarneri Evolution (2); Electro-Voice EVF-1152D/96 (2, passive);
  Mackie SRM450 (2, active); KEF Model 105 (3); Pioneer SP-FS52-LR (4); KEF Concord (2, "No Power
  needed"); Bose 802 Series II (8); Focal Trio6 Be (3, three internal amplifiers).
* **NOT_STATED (24)** — explicit silence on `active` after a full read: audio-database JBL L16,
  KEF Model 104; Manualzz EV Sx100+; Manualsnet KEF LS3/5A; SoundStage! KEF Reference 1; Bose 802;
  KEF Model 105; Pioneer SP-FS52-LR; DALI Oberon 9; Pioneer SP-BS22-LR; plus the LG S95TR and
  others whose `active` was supported but not promoted.
* **NOT_EXTRACTED (2)** — Sound & Vision's B&W CM10 page served navigation only.
* **INACCESSIBLE (2)** — the Cieri JBL L19 brochure URL, in both the stored truncated form and the
  complete `(1977).pdf` form, returns HTTP 404.

## Counts after Round 26

| Metric | Before | After |
| --- | --- | --- |
| `driverCount`+`active` MANUFACTURER_VERIFIED | 678 | **696** |
| CITED_IN_NOTES_UNCHECKED | 255 | **237** |
| UNSOURCED | 192 | 192 |
| NO_PROVENANCE | 189 | 189 |
| Queue items never assessed | 79 | **0** |
| Provenance-queue URLs / items | 181 / 255 | 171 / 237 |

Residual queue: SUPPORTED_NOT_PROMOTED 97, NOT_STATED 103, INACCESSIBLE 16, NOT_EXTRACTED 13,
CONFLICT 8. No item is unopened.

## Remaining limitations (honest state)

* 237 fields stay `CITED_IN_NOTES_UNCHECKED`: each now has a named, opened document that either
  states the value on a host that cannot promote it, states nothing about it, or was not served.
  They cannot be promoted without a manufacturer-hosted copy of the same document.
* Eight conflicts remain untouched (ELX200-15 response points stay excluded from simulation;
  LSR32 20 kHz; `jbl-jrx225`; `kef-q750`; Adam; focal-scala-utopia-evo; martinlogan-motion-40).
* `legacy-mack-4` and `equator-d5` values remain held; Genelec 8331A SOFA retrieval still fails
  upstream; 0 of 51 directivity leads imported.

## Verification

```
python3 scripts/research/prepare-round26-batches.py   # 121 hosts / 85 established
python3 scripts/research/apply-queue-batch.py 26      # promoted=18 recorded=61
python3 scripts/research/build-field-provenance-inventory.py
node scripts/research/make-research-queue.mjs
python3 scripts/research/make-provenance-queue.py     # 237 items / 171 URLs, 0 unassessed
npm run docs:release && npm run docs:consistency      # issues: []
npm run typecheck && npm test                         # 82/82 suites
npm run audit:final / audit:third-party / audit:speaker / audit:provenance   # problems: []
npm run release:source && npm run audit:release       # problems: [], warningCount 0
```
