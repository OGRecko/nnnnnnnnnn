# Research status — Round 24 (2026-10-19)

Scope: keep driving the open field-level provenance backlog (`driverCount` / `active`)
towards closure in one pass, opening each recorded URL and recording exactly what the
document says. No owner decision, archived record, response dataset or held value was
changed.

## Method

Every URL below was opened during this round and read for the exact model's own
specification text; the quoted strings are stored in `round24_evidence_data.py` and the
per-field notes in `round24-url-results.json`. The rules from Rounds 22–23 were applied
unchanged:

* a field becomes `MANUFACTURER_VERIFIED` only when the opened **manufacturer** document
  states that field for the exact model and the stored value already matches
  (`apply-queue-batch.py` asserts `stored == recorded` before writing);
* `active` is never inferred from a power-handling figure, an impedance, a recommended
  amplifier-power range or an amplifier-channel count. The document must say
  powered/active, show a built-in amplifier, or say passive/unpowered — otherwise the
  outcome is `NOT_STATED` and the stored value is left untouched;
* multi-tenant and third-party hosts (`cdn.shopify.com`, a rental firm's document mirror,
  an unestablished Azure blob account) can support a value but never promote it; those
  results are `SUPPORTED_NOT_PROMOTED`;
* a document that no longer serves the recorded content is `INACCESSIBLE`, with the
  limitation named.

## Totals

| Item | Count |
| --- | --- |
| URLs opened | 70 |
| Field results recorded | 111 |
| Fields promoted to `MANUFACTURER_VERIFIED` | 88 |
| `NOT_STATED` (no explicit support in the opened text) | 14 |
| `SUPPORTED_NOT_PROMOTED` (non-manufacturer host) | 6 |
| `INACCESSIBLE` (2 URLs) | 3 |
| Sources added to `provenance-source-ledger.json` | 69 |
| Null-value restorations | 0 (no field opened this round was null) |
| Hosts added to `source-host-allowlist.json` | 33 (86 hosts total, 75 established) |

## Effect on the live catalogue (657 records, 1314 `driverCount`+`active` fields)

| Metric | Before Round 24 | After Round 24 |
| --- | --- | --- |
| `MANUFACTURER_VERIFIED` (driverCount+active) | 543 | **631** |
| `CITED_IN_NOTES_UNCHECKED` | 390 | **302** |
| — of which `driverCount` | 194 | **132** |
| — of which `active` | 196 | **170** |
| Distinct unchecked source URLs | 255 | **204** |
| `UNSOURCED` | 192 | 192 (unchanged) |
| `NO_PROVENANCE` | 189 | 189 (unchanged) |
| Field-provenance inventory (`driverCount`+`active` entries) | 3336 | 3336 |
| Research queue records | 460 of 657 | **435 of 657** |
| Resolved source URLs in the research queue | 196 | **247** |

Queue status after this round: 105 `OPEN`, 92 `CHECKED_PARTIAL`, 7 `INACCESSIBLE`
(204 URLs, 302 outstanding fields).

## Fields promoted (88)

Values are the stored catalogue values confirmed by the quoted source text; `*` marks an
`active` result.

* **SVS (12)** — `pb-3000`, `pb-4000`, `pb16-ultra`, `sb-2000-pro`, `sb-3000`, `sb4000`:
  `driverCount=1` (single named 12"/13"/13.5"/16" driver) and `active=True*` (Sledge
  amplifier, 550 W RMS on the 2000 Pro).
* **KRK (8)** — `rokit-5-g4`, `rokit-7-g4`, `v4-s4`, `v6-s4`: `driverCount=2` (LF + 1"
  HF) and `active=True*` ("Powered Near-Field Studio Monitor", "System type: Active
  Studio Monitor", wattage listed).
* **JBL (6)** — `flip6` (`driverCount=2`, `active*`: 45×80 mm woofer + 16 mm tweeter,
  20 W + 10 W), `charge5` (2; 52×90 mm + 20 mm, 30 W + 10 W), `partybox-1000`
  (4; 12" sub + 2×7" + compression driver, mains-powered).
* **Polk (4)** — `rti-a7=4` (6.5" mid + 2×7" sub + 1" tweeter), `signature-s50=3`,
  `signature-s15=2`, `rc85i=2`.
* **Kicker (4)** — `47ksc6504`, `46csc654`, `46css674`, `43dsc6504`: `driverCount=2`
  (two-way coaxial/component pairs).
* **Rockford Fosgate (3)** — `r165x3=3` ("3-Way Coax"), `r1675x2=2`, `p3=1`
  (single 12" Punch P3 DVC subwoofer).
* **Hertz (3)** — `dieci-dsk-165-3`, `mille-pro-mpk-165-3`, `cento-ck-165`: 2
  (two-way systems, 165 mm + tweeter).
* **Bose (3)** — `legacy-bose-2` (501: ten-inch woofer + two three-inch tweeters),
  `bose-301` (8" + 3" + 2"), `virtually-invisible-791` (2×1" + 7").
* **Audison (3)** — `prima-apk-165`, `voce-av-k6`, `thesis-th-k2-ii-a`: 2.
* **Triangle (3)** — `comete-ez` (`driverCount=2`, `active=False*`: "High-Fidelity
  Passive Speaker"), `borea-br03=2` ("2 Drivers: 1 x 25mm silk dome tweeter; 1 x 16 cm
  midwoofer").
* **Behringer (3)** — `b215xl=2` (15" + 1.75" driver), `truth-b2031` (`driverCount=2`,
  `active*`: "Active 2-Way Reference Studio Monitor", bi-amped 265 W).
* **Marshall (2)** — `1960b=4`, `1960bv=4` ("Four 12-inch Celestion G12T-75 / G12
  Vintage").
* **Yamaha (2)** — `ns-5000=3`, `ns-777=4` (both "3-way" with itemised units).
* **Pioneer (2)** — `ts-d65c=2`, `ts-z65f=2` ("17 cm 2-Way", 26 mm tweeter).
* **PreSonus (2)** — `eris-4-5` (`driverCount=2`, `active*`: 4.5" LF + 1" dome,
  50 W Class AB).
* **Auratone (2)** — `5c` (`driverCount=1`, `active=False*`: "Type Passive reference
  monitor", single 4.5" full-range cone).
* **Void (2)** — `air-8` (2; `active=False*`: "Passive 8 inch two-way coaxial").
* **Sonos (2)** — `sub-mini` (2; `active*`: two 6" force-cancelling woofers, two
  Class-D amplifiers).
* **Sennheiser (2)** — `ambeo-soundbar-max` (13; `active*`: "Total number of speakers
  13", "13x class D Amplifiers").
* **Avantone (2)** — `mixcube` (1; `active=False*`: "Mixcube Passive", 8 Ω nominal,
  10–200 W recommended).
* **RCF (2)** — `nx45a` (2; `active*`: "ACTIVE TWO WAY", 1400 W class-D).
* **Devialet (2)** — `dione` (17; `active*`: 9 full-range + 8 subwoofers, 950 W RMS).
* **Martin Audio (2)** — `legacy-ma-3` (4; `active=False*`: "Three-way, active/passive",
  external iK81 amplifier recommended).
* **Barefoot (2)** — `footprint03` (3; `active*`: "A TRUE 3-WAY ACTIVE PORTED DESIGN").
* **Single-field promotions** — `revel-m106=2`, `apple-homepod=6` (4" woofer + array of
  five tweeters), `sonos-play1=2`, `dutch-and-dutch-8c` (`active*`: "amplification,
  streaming, DACs, DSP … built in"), `eaw-kf760=6` (2 LF + 2 MF + 2 HF), `kenwood-kfc-1666s=2`,
  `paradigm-monitor-11=5` ("5-driver, 3-way"), `q-acoustics-3030i=2` (165 mm + 22 mm),
  `danley-sh96=11` ("four 15-inch … six 4-inch … a 1.4-inch", "11 Drivers, 1 Horn!"),
  `funktion-one-res2=3`.

## `NOT_STATED` — value kept, field left unverified (14)

Documents that never use explicit passive/powered wording (they give only impedance,
power handling, binding posts or a recommended amplifier-power range): Marshall
`1960b.active`, `1960bv.active`; Bose `legacy-bose-2.active`, `bose-301.active`,
`virtually-invisible-791.active`; Audison `prima-apk-165.active`; KRK `7000.active`;
Behringer `b215xl.active`; Triangle `borea-br03.active`; Danley `sh96.active`;
Funktion-One `res2.active`; EAW `kf760.active` ("tri-amplified" describes external
drive, not the absence of a built-in amplifier); Paradigm `monitor-11.active`; and Sony
`ht-a7000.driverCount` — the support page lists 11 amplifier channels and a 7.1.2
speaker structure but never a transducer count, so `driverCount` stays unverified.

Klipsch spec sheets for RF-7 III, Heresy IV, Cornwall IV, RP-8000F II, RP-600M II and
RP-8060FA II were opened and their driver complements read, but the results were **not**
applied in this round (they are still `OPEN` in the queue); the `active` question on
those passive Heritage/Reference models remains unproven by explicit wording.

## `SUPPORTED_NOT_PROMOTED` — correct but unestablishable host (6)

`krk-7000.driverCount` (brand spec-sheet PDF served from `cdn.shopify.com`),
`rel-s812.active` (REL brochure on the same CDN), `fostex-6301b.driverCount` and
`.active` (owner's manual mirrored by a rental firm), `bang-olufsen-beosound-balance`
`driverCount`/`active` (unestablished Azure blob account). Documents are model-exact but
the hosts cannot be attributed to the manufacturer, so nothing was promoted.

## `INACCESSIBLE` (2 URLs)

* `https://trianglehifi.com/products/enceinte-bibliotheque-hi-fi-borea-br02` — dead
  slug, redirects to the distributor home page; `borea-br02` fields stay unverified.
* `https://www.ikmultimedia.com/news/?id=iloudmtm` — the recorded news id is gone; the
  URL now lands on the blog index ("No articles found"), so `iloud-mtm.driverCount`
  stays unverified.

## Backlog remaining (204 URLs, 302 fields)

105 `OPEN`, 92 `CHECKED_PARTIAL`, 7 `INACCESSIBLE`. The largest surviving clusters are
`assets.klipsch.com` (14 URLs / 15 fields — sheets opened but not yet applied),
`www.manualslib.com` (9), `www.fullcompass.com` (8), `media.focal-naim.com` /
`dam.focal-naim.com` (11), `audio-database.com` (6), `www.hifiengine.com` (6),
`www.stereophile.com` (6, third-party — can never promote), `jblpro.com` (4),
`www.adam-audio.com` (3), `international.kef.com` (4), `www.martinlogan.com` (3) and
`www.lg.com` (3 soundbars with no transducer table on the PDP).

## Unresolved research items (unchanged)

* `legacy-mack-4` — the CR3 cartridge overlay still blocks the manual page.
* `equator-d5` — 404 on every recorded URL.
* ELX200-15 85-vs-86 dB response-point conflict — disputed curve stays out of simulation.
* LSR32 20 kHz self-conflict — no new evidence; value untouched.
* 51 directivity leads — 0 imported (Genelec 8331A SOFA still HTTP 500).
* `jbl-jrx225` / `kef-q750` — counting-convention questions; values untouched.
* `atc-scm45a-pro.driverCount` remains 3.

## Reproduce

```
python3 scripts/research/prepare-round24-batches.py     # allowlist + url results
python3 scripts/research/apply-queue-batch.py 24        # write promotions + history
python3 scripts/research/build-field-provenance-inventory.py
node scripts/research/make-research-queue.mjs
python3 scripts/research/make-provenance-queue.py
npm run docs:release && npm run docs:consistency
```
