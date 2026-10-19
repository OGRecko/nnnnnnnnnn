# Research status — Round 25 (2026-10-19)

Round 25 continued the field-provenance audit of `driverCount` and `active`. Every result below
comes from a document opened in this round; the exact quotes are stored in
`scripts/research/round25_evidence_data.py` and the per-URL outcomes in
`scripts/research/round25-url-results.json`. Promotion history is appended to
`scripts/research/round25-value-history.json`; no earlier value or provenance entry was removed.

## Method

* 64 URLs opened: 36 manufacturer-site URLs, 6 owner-approved manualslib copies of exact-model
  manuals, 22 dealer/review/database pages recorded as supporting only.
* 106 field results: **47 PROMOTED**, 16 NOT_STATED, 32 SUPPORTED_NOT_PROMOTED, 8 NOT_EXTRACTED,
  3 INACCESSIBLE.
* A field was promoted only when the opened document stated it for the exact stored model and the
  host was the manufacturer's own site (or an owner-approved distributor copy under Owner
  Decision 1). Dealer, review, museum and database pages can support a value but never promote it.
* `active` was promoted only on explicit wording ("passive loudspeaker", "active monitors",
  "self-powered", "Powered Subwoofer", a built-in amplifier listing, or an explicit
  "Amplifier: N/A" row). Recommended-amplifier-power ranges alone were recorded as NOT_STATED.
* Values were not hard-coded: the builder reads them from `src/data/speakers.json` and refuses any
  tied field that the evidence table does not declare.

## Promotions (47)

Manufacturer sites (38 promotions):

| Record | Field | Value | Source evidence |
| --- | --- | --- | --- |
| jbl-everest-dd67000 | driverCount | 4 | dual 15″ woofers + 4″ beryllium compression driver + 1″ beryllium UHF driver |
| jbl-k2-s9900 | driverCount | 3 | 15″ 1500AL-1 woofer + 4″ 476Mg + 1″ 045Be-1 |
| legacy-ma-4 (Martin MLA) | driverCount / active | 7 / true | LF 2 + MF 2 + HF 3; "active array element", "Six channel Class D", "self-powered" |
| legacy-bose-7 (Bose 251) | driverCount | 3 | "Two (2) 2½″ … Twiddler drivers … One (1) 5¼″ … woofer per speaker" |
| magnepan-mg1.7 | driverCount | 3 | "3-way … quasi-ribbon bass/midrange, tweeter, and super-tweeter" |
| sennheiser-ambeo-mini | driverCount / active | 6 / true | "Total number of speakers 6"; "6x class D amplifiers" |
| sennheiser-ambeo-soundbar-plus | driverCount / active | 9 / true | "Total number of speakers 9"; "9x class D amplifiers" |
| fender-blues-junior-iv | driverCount / active | 1 / true | "Speakers: One - 12″ Celestion A-Type"; "Amplifier Type Tube", 15 W |
| qsc-e218sw | driverCount / active | 2 / false | "two 18-inch die-cast frame woofers"; E Series "passive loudspeakers" |
| kenwood-excelon-kfc-xp6903c | driverCount | 3 | 6x9″ woofer + 3-1/2″ mid-high + 25 mm tweeter |
| yamaha-dxs12 | driverCount / active | 1 / true | DXS12 "12″ Cone", HF "–"; "Powered Subwoofer … Class-D" |
| lg-lg-sc9s / s80tr / s90tr | driverCount | 9 / 11 / 13 | "Number of Speakers 9 EA" / "Número de Colunas 11 EA" / "13 EA" |
| dandb-t10 | driverCount / active | 3 / false | "dual 6.5″ drivers, a 1.4″ exit compression driver and a passive crossover network" |
| das-audio-aero-12a | driverCount / active | 2 / true | 12″ 12LNC4 + M-75N; "amplificador de 600 W" |
| adamson-e15 | driverCount | 6 | 2× ND15-L + 2× YX7 + 2× NH4TA2 |
| rockford-fosgate-t1650-s | driverCount | 2 | "separate tweeter and a true 6.5″ midrange", 2-way set |
| rockford-fosgate-t1650 | driverCount | 2 | "Speaker Type: 2-Way Coax"; 6.5″ midrange + 1″ tweeter |
| vox-v212hwx | driverCount | 2 | "2 x 12″ 8 Ohm Celestion Alnico Blue" |
| q-acoustics-5020 | driverCount | 2 | "Bass unit: 1 × 125 mm"; "Treble unit: 1 × 25 mm" |
| presonus-eris-e5 | driverCount / active | 2 / true | "2-Way Active"; 5.25″ LF + 1″ HF; 45 W/35 W Class AB |
| legacy-sonos-5 (Move) | driverCount / active | 2 / true | "One tweeter", "One mid-woofer"; "Two Class-D digital amplifiers" |
| alpine-s-s65 / r-s65c / x-s65c | driverCount | 2 / 2 / 2 | 2-way coaxial/component sets with one listed 1″ tweeter |
| morel-elate-carbon-62a | driverCount | 2 | "Elate Carbon 62A \| 6½″ 2-way Active" |
| fender-bassman-410 | active | false | enclosure "designed for use with the Fender Bassman 250 head amplifier" |

Owner-approved manualslib copies (6 URLs, 9 promotions):

| Record | Field | Value | Evidence |
| --- | --- | --- | --- |
| legacy-kef-7 (Blade) | driverCount | 6 | MF 125 mm + HF 25 mm + 4 × 225 mm bass units |
| legacy-kef-5 (Q100) | driverCount / active | 2 / false | Uni-Q 130 mm + 25 mm HF; "Amplifier N/A", 10–100 W requirement |
| jbl-vrx932 | driverCount / active | 4 / false | 1 × 2262H + 3 × 2407J; "Bi-amp / passive, externally switchable" |
| legacy-mack-2 (HR624) | driverCount / active | 2 / true | 1″ HF + 6.7″ LF; "bi-amplified, active monitors", 100 W/40 W |
| sonus-faber-homage-tradition-amati | driverCount / active | 4 / false | AMATI column: 28 mm + 150 mm + 2 × 220 mm; "passive loudspeakers" |

No value changed in this round: all 47 promotions confirmed the value already stored.

## Recorded without promotion

* **NOT_STATED (16)**: KEF R11 Meta, JBL 4311, JBL 4412 `active`; JBL DD67000, K2 S9900,
  Bose 251, Magnepan 1.7, Adamson E15, LG SC9S/S80TR/S90TR `active`; KEF Blade, Snell Type A/III,
  Vandersteen 2Ce `active`; audio-database JBL 4312 `active`. Every one gives only power handling,
  impedance or a recommended amplifier-power range.
* **SUPPORTED_NOT_PROMOTED (32)**: dealer pages (Full Compass Electro-Voice TX1122/TX1152/TX2152/
  TX1181/TX2181/TX1122FM/TX1152FM, ZX4 data sheet, NEXO PS15 brochure), JBL EON15 and L-Acoustics
  ARCS WIDE dealer documents, and third-party pages (Stereophile KEF Reference 5, Snell Type A/III,
  Totem Model 1, Sound On Sound HR824, hifi-guide 801 Matrix/KG 4.5, Radiomuseum KLH Six,
  audio-database 4312, HiFi Engine HPM-100). They confirm the stored values but their hosts cannot
  promote them.
* **NOT_EXTRACTED (8)**: KEF Q150/Q350 (only the navigation chunk was served), dB Technologies
  Opera Live page (manual covers 202/205/402, not Opera 405), Sound & Vision Pioneer EX page
  (no specification table served), both Yamaha history pages (no NS-690 / NS-10M driver count in
  the served chunk).
* **INACCESSIBLE (3)**: `jp.jbl.com/jamaica.html` (jazz-bar profile, not Paragon data),
  `dali-speakers.com/…/oberon-1/` (404 template), and the JBL Paragon driver count through that URL.

## Counts after Round 25

| Metric | Before | After |
| --- | --- | --- |
| Live `driverCount`+`active` fields | 1314 | 1314 |
| MANUFACTURER_VERIFIED | 631 | **678** |
| CITED_IN_NOTES_UNCHECKED | 302 | **255** |
| UNSOURCED | 192 | 192 |
| NO_PROVENANCE | 189 | 189 |
| Provenance-queue URLs / items | 204 / 302 | **181 / 255** |
| Queue items never assessed | 180 | **79** |

Provenance-queue residual: NOT_STATED 93, SUPPORTED_NOT_PROMOTED 50, INACCESSIBLE 14,
NOT_EXTRACTED 11, CONFLICT 8, UNASSESSED 79 (46 OPEN URL groups). Research queue: 421 of 657
records still carry a backlog; cited 255 fields across 181 URLs, 192 unsourced, 189 without
provenance.

Largest remaining unassessed groups: `walkersound.co.uk` Bose 802 MkII, `svconline.com` Meyer
MJF-212, `soundstagehifi.com` KEF Reference 1, `soundandvision.com` B&W CM10, `sisme.com`
L-Acoustics ARCS II (URL still missing from `queue-url-status.json`), `radiomuseum.org` KEF
Concord, `parts-express.com` Pioneer brochure, `manualzz.com` Tannoy System 600 / EV Sx100 /
Magneplanar MG20.1, the five `audio-database.com` pages, five `hifiengine.com` pages, three
`customsounds.com` JL Audio PDFs, two `tacotunes.com` JL Audio PDFs, and the remaining
`fullcompass.com` PDFs (EVF-1152D/96, SRM450).

`manualzz.com/doc/22701574/electro-voice-sentry500-data-sheet` was opened and read (12″ woofer +
Super-Dome tweeter, 2 transducers) but could not be recorded: the URL is absent from
`queue-url-status.json`, and the apply step requires an existing status entry. It stays on the
list above as a registry gap, not as a missing source.

## Unresolved (unchanged)

* ELX200-15 85-vs-86-point reading remains excluded from simulation; the disputed curve was not
  reintroduced.
* LSR32 20 kHz discrepancy remains a recorded CONFLICT.
* `legacy-mack-4` and `equator-d5` values remain held.
* Genelec 8331A SOFA retrieval still fails upstream (Zenodo HTTP 500); 0 of 51 directivity leads
  imported.
* `jbl-jrx225`, `kef-q750`, Adam, focal-scala-utopia-evo and martinlogan-motion-40 conflicts remain
  open.

## Verification

```
python3 scripts/research/prepare-round25-batches.py     # 107 hosts / 85 ESTABLISHED
python3 scripts/research/apply-queue-batch.py 25        # cumulative promoted=47, recorded=59
python3 scripts/research/build-field-provenance-inventory.py
node scripts/research/make-research-queue.mjs
python3 scripts/research/make-provenance-queue.py       # 255 items / 181 URLs, warnings 0
npm run docs:release && npm run docs:consistency        # issues: []
npm run typecheck && npm test                           # 82/82 suites
npm run audit:final / audit:third-party / audit:speaker / audit:provenance   # problems: []
npm run release:source && npm run audit:release         # problems: [], duplicateIds 0
```
