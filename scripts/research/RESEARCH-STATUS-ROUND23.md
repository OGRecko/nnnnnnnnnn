# Research status — Round 23 (2026-10-19)

Scope: close as much of the open field-level provenance backlog as can be verified from
exact-model sources, without touching owner decisions, archived records, or unresolved
response data.

## Method

Each URL was opened in this round and read for the exact model's own specification text.
The rules from Round 22 were applied unchanged:

* a field becomes `MANUFACTURER_VERIFIED` only when the opened manufacturer document states
  that field for that exact model, and the stored value already matches (`apply-queue-batch.py`
  asserts `stored == recorded` before writing);
* `active` is never inferred from a cabinet's power-handling figure or from a "recommended
  amplifier power" range. The document must say powered/active, list a built-in amplifier, or
  say passive/unpowered. Otherwise the outcome is `NOT_STATED`;
* third-party hosts can support a value but never promote it. The two Stereophile
  specification sidebars opened this round are recorded as `SUPPORTED_NOT_PROMOTED`;
* unreadable documents are `INACCESSIBLE` with the precise limitation; no value is changed.

## Totals

| Item | Count |
| --- | --- |
| URLs opened | 50 |
| Field results recorded | 73 |
| Fields promoted to `MANUFACTURER_VERIFIED` | 54 |
| `NOT_STATED` (explicit support absent) | 13 |
| `SUPPORTED_NOT_PROMOTED` (third-party host) | 2 |
| `INACCESSIBLE` (2 URLs, 4 fields) | 4 |
| Sources added to `provenance-source-ledger.json` | 50 |
| Null-value restorations | 0 (no field opened this round was null) |

## Effect on the live catalogue (657 records, 3082 live fields)

| Metric | Before Round 23 | After Round 23 |
| --- | --- | --- |
| `MANUFACTURER_VERIFIED` | 2034 | **2088** |
| `CITED_IN_NOTES_UNCHECKED` | 444 | **390** |
| — of which `driverCount` | 237 | **194** |
| — of which `active` | 207 | **196** |
| Distinct unchecked source URLs | 290 | **255** |
| `UNSOURCED` | 192 | 192 (unchanged) |
| `NO_PROVENANCE` | 189 | 189 (unchanged) |
| Research queue records | 468 of 657 | **460 of 657** |
| Resolved source URLs in the queue | 161 | **196** |

Queue status after this round: 175 `OPEN`, 75 `CHECKED_PARTIAL`, 5 `INACCESSIBLE`
(255 URLs, 390 outstanding fields).

## Fields promoted (54)

Values below are the stored catalogue values, confirmed by the quoted source text. The full
per-field evidence strings are in `round23_evidence_data.py` and `round23-url-results.json`.

**Marshall (10)** — `1960a.driverCount=4` ("4 x Celestion G12T-75 (16Ω, 75W)");
`mx112.driverCount=1` ("1x12"; one Celestion Seventy-80); `middleton.driverCount=4` and
`middleton.active=true` (two 3" woofers + two 3/5" tweeters, four Class D amplifiers);
`acton-iii.active=true`, `stanmore-iii.active=true`, `woburn-iii.active=true` (built-in
amplifier banks listed); `1936v.driverCount=2` and `mx212.driverCount=2` ("2x12"; two named
12" speakers); `1960av.driverCount=4` ("features four Celestion G12 Vintage speakers").

**SVS (8)** — `pb-1000-pro`, `sb-1000-pro`, `pb-2000-pro`, `sb16-ultra`: each
`driverCount=1` (single named 12"/16" driver) and `active=true` (325 W / 325 W / 550 W RMS
amplifier; Sledge STA-1500D).

**KRK (6)** — `rokit-8-g4.driverCount=2`, `active=true`; `rokit-10-3-g4.driverCount=3`,
`active=true` (10" + 4.5" + 1", tri-amp); `v8-s4.driverCount=2`, `active=true`
("System type: Active Studio Monitor", 8" + 1").

**Polk (4)** — `reserve-r100`, `reserve-r200`, `signature-elite-es15`,
`signature-elite-es20`: `driverCount=2` each (one tweeter + one woofer named in the product copy).

**Monitor Audio (5)** — `platinum-100-3g=2`, `platinum-200-3g=4`, `creator-c1m=2`,
`creator-c2m=2`, `creator-c3m=3` (each feature list enumerates the drivers: MPD III + 6" / MPD III
+ 4" + twin 6" / 1" + 7" / 1" + 7" / 1" + 7" + 4").

**Orange (5)** — `ppc108=1`, `ppc112=1`, `ppc212=2`, `ppc212v=2`, `ppc412=4`
("1 x 8″" … "4 x Celestion Vintage 30").

**MESA/Boogie (4)** — `fillmore-2x12=2`, `lone-star-2x12=2` ("2 x C90" wattage row),
`2x12-rectifier=2`, `rectifier-4x12=4` (2x12 / "quad box" 4x12 with Celestion Vintage 30s).

**Sonus faber (3)** — `lumina-i=2`, `lumina-ii=2`, `lumina-iii=4` (Tw + Mw; Tw + Md + 2x W).

**JBL (3)** — `hdi-3800=4` (three 8" woofers + 1" compression driver), `l100-classic=3`
(12" + 5.25" + 1"), `l82-classic=2` (8" + 1").

**Single-record promotions (6)** — `q-acoustics-3010i=2`, `q-acoustics-3020i=2`,
`vox-v212c=2`, `wilson-watt-puppy=4`, `revel-f206=4`, `psb-synchrony-t600=5`.

## Not promoted, and why

* **13 `NOT_STATED`** (values left unverified): the passive/active field of the five Marshall
  cabinets, the three Sonus faber Lumina models, the three JBL home models, and the two
  Stereophile records. Each page gives enclosure power handling or a recommended amplifier
  range but no explicit powered/passive wording, which the Round 22 rule does not accept.
* **2 `SUPPORTED_NOT_PROMOTED`**: `kef-ls50.driverCount=2` and `harbeth-shl5.driverCount=3`
  are explicitly supported by Stereophile specification sidebars, but a third-party host
  cannot promote a field. They remain `CITED_IN_NOTES_UNCHECKED` by design.
* **4 `INACCESSIBLE`**: `marshall.com/.../1936-2x12-cabinet` returns HTTP 404 (the 1936 stays
  unresolved), and the Polk Signature S60 archive URL now returns the site error page.

## Host ledger

`source-host-allowlist.json` gained 15 Decision-8 operator checks and 1 upgrade
(53 hosts, 45 established):

* newly `ESTABLISHED`: marshall.com, svsound.com, polkaudio.com, revelspeakers.com,
  krkmusic.com, qacoustics.com, monitoraudio.com, orangeamps.com, legacy.mesaboogie.com,
  voxamps.com, sonusfaber.com, wilsonaudio.com, psbspeakers.com, global.jbl.com;
* `www.jbl.com` upgraded from `BRAND_DOMAIN_UNVERIFIED` after the HDI-3800 page was shown to be
  served from HARMAN's `Sites-masterCatalog_Harman` catalogue path (previous status retained);
* `www.stereophile.com` recorded as `NOT_MANUFACTURER` (review publication).

## Unresolved items carried forward (unchanged, documented in the reconciliation files)

* `legacy-mack-4` and `equator-d5` stay on hold; neither was re-opened this round (see
  `held-records-round18.json` → `round23Review`).
* ELX200-15 response-point row count (85 vs 86) is still unresolved; the disputed curve stays
  excluded from simulation (`elx200-15-reconciliation-round18.json` → `round23Review`).
* LSR32 20 kHz self-conflict unchanged (`lsr32-20khz-reconciliation-round18.json`).
* Directivity: 0 of 51 leads imported; the 410.5 MB Genelec 8331A SOFA file remains
  unretrievable in this environment, so no data was imported or fabricated
  (`directivity-lead-review-round21.json`).
* Counting-convention cases (`jbl-jrx225`, `kef-q750`) remain `SUPPORTED_NOT_PROMOTED`
  pending an owner ruling.

## Backlog remaining (390 fields / 255 URLs)

Largest `OPEN` groups after this round: fullcompass.com 11, manualslib.com 7,
audio-database.com 6, svsound.com 6 (other SVS models), hifiengine.com 6,
rockfordfosgate.com 5, cdn.shopify.com 4, products.bose.com 4, krkmusic.com 4,
stereophile.com 4, kicker.com 4, polkaudio.com 4.

## Gates run

`npm run docs:release` (sources 633), `npm run docs:consistency` → `issues: []`,
`npm run typecheck` clean, `npm test` 82/82, `npm run audit:speaker` → `problems: []`,
`npm run audit:provenance` → `problems: []`, `npm run audit:final`,
`npm run audit:release`, `npm run release:source` + `release:source:verify`.

## Artifacts

* `scripts/research/round23_evidence_data.py` — 50 checks, evidence quotes, non-promotion reasons.
* `scripts/research/round23-url-results.json` — per-URL status and per-field outcomes (73).
* `scripts/research/round23-value-history.json` — 54 before/after provenance entries.
* `scripts/research/prepare-round23-batches.py` — host-ledger checks + results builder (idempotent).
* `scripts/research/provenance-queue.json`, `field-provenance-inventory.json`,
  `queue-url-status.json`, `provenance-source-ledger.json` — rebuilt.
