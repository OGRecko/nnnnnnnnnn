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

## MV host audit — 23 mislabelled fields corrected

The 2026-10-19 instruction restricts `MANUFACTURER_VERIFIED` to manufacturer-owned hosts or explicitly
approved manufacturer copies. Cross-checking every MV `driverCount`/`active` source against
`source-host-allowlist.json` found 23 fields whose host is `NOT_MANUFACTURER`:

| Host | Fields | Records |
| --- | --- | --- |
| manualslib.com (document aggregator, now in the allowlist as NOT_MANUFACTURER) | 17 | jbl-vrx932, legacy-kef-5, legacy-kef-7, legacy-mack-2, Sonus faber Olympica Nova I/II/III/V, Homage Tradition Amati/Guarneri/Serafino |
| tacotunes.com (retailer) | 4 | jl-audio-c3-650, jl-audio-c5-650 |
| onlinecarstereo.blob.core.windows.net (retailer storage) | 2 | jl-audio-12w3v3 |

Every value is kept (none was contradicted); the status becomes `CITED_IN_NOTES_UNCHECKED`, the original
evidence note is preserved with a policy sentence appended, and each change has a `DEMOTE_POLICY` history
entry. The queue rows move from `PROMOTED` to `SUPPORTED_NOT_PROMOTED`. Report:
`round29-mv-host-audit.json`. This is a correction, not a loss of data — the MV count drops by 23 and the
cited backlog grows by the same amount.

## Policy clarification: what proves `active: false`

The tier's condition 2 only said what cannot prove a loudspeaker *is* powered. Batches 39–40 needed the
mirror rule, which is now written into `PROVENANCE-POLICY.md`:

* accepted: the document calls the product passive; or it instructs the user to drive the loudspeaker from
  an external power amplifier (including bi-wiring/bi-amping instructions) and describes no mains inlet; or
  it places the active electronics in a separate unit and says so;
* **not** accepted on their own: impedance, power-handling ratings, binding posts/terminals, "recommended /
  suggested amplifier power" or "amplifier requirements" figures, product category, pictures, or the mere
  absence of an amplifier mention.

Consequences applied consistently: ATC SCM19, Wilson WATT/Puppy, KEF Q150/Q350, JBL 4312/L16/D130 and KEF
Model 104 keep `active` unresolved (`NOT_STATED`) even though the value is obviously false, because those
documents only give a recommended amplifier power or a power-handling rating.

## Batch 39 — Audio Database (JBL 4312, JBL L16, JBL D130, KEF Model 104)

| Record | driverCount | Quote | active |
| --- | --- | --- | --- |
| jbl-4312 | 3 | "Method: 3-Way, 3-Speaker" | NOT_STATED (only "Allowable input 80W") |
| jbl-l16 | 2 | "Method: 2-Way, 2-Speaker" | NOT_STATED (only "Allowable input 35W") |
| legacy-jbl-1 | 1 | "Type: 38 cm cone type full range unit" | NOT_STATED (category is not evidence) |
| legacy-kef-2 | 2 | "2-way, 2-speaker, passive radiator system" | NOT_STATED ("passive radiator" is cabinet loading) |

## Batch 40 — Sonus faber manuals (manualslib copy)

These are the fields demoted earlier today by the MV host audit. The pages were opened and the evidence
re-read, so they now hold the third-party tier instead of a mislabelled MV:

| Record | driverCount | Quote | active |
| --- | --- | --- | --- |
| homage-tradition-amati | 4 | "3.5 way"; H28 28 mm + M15 150 mm + 2 × W22XTR-08 220 mm | false — "Homage tradition passive loudspeakers" |
| homage-tradition-guarneri | 2 | "2 way stand mount"; H28 + W15 150 mm | false — same header |
| homage-tradition-serafino | 4 | "3.5 way"; H28 + M15 + 2 × W18XTR-08 180 mm | false — same header |
| olympica-nova-i | 2 | "2 way ... stand mount"; H28 XTR3 + MW15 XTR2-04 | false — "Use a single stereo amplifier or two mono amplifiers" |
| olympica-nova-ii | 3 | "3 way"; H28 + M15 + W18XTR2-04 | false — same connection chapter |
| olympica-nova-iii | 4 | "3 way"; H28 + M15 + 2 × W18XTR2-08 | false — same connection chapter |
| olympica-nova-v | 5 | "3 way"; H28 + M15 + 3 × W18XTR2-12 | false — same connection chapter |

## Batch 41 — aggregator-hosted manufacturer documents

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| tannoy-system-600 | 2 / false | "Dual Concentric 6.5\" driver"; HF and LF units serviced separately; terminals "must be connected to ... the power amplifier" | both promoted |
| spendor-sp100 | 3 / false | "Low Frequency unit ... 300mm Bextrene", "Mid Frequency unit ... 160mm", "High Frequency unit 19mm Soft Dome"; amplifier wiring and tri-wiring instructions | both promoted |
| kef-ls3-5a | 2 | "B110 bass/midrange unit (SP1228), and T27 tweeter (SP1032)" | driverCount promoted; active NOT_STATED ("Amplifier requirements 25-75W" only) |
| meyer-mjf212 | 3 / true | "self-powered stage monitor"; 4 in compression driver + "a pair of ... 12in." cone drivers; "3-channel class AB/H amplifier" | both promoted |
| eV-sentry-500 | 2 / false | "12-inch direct radiator woofer" + "Super-Dome tweeter"; integral crossover; bi-amp access panel; external amplifiers | both promoted |
| electro-voice-sx100 | 2 | "LF Transducer: 12\" (300mm)", "HF Transducer: 1\" ... DH3" | driverCount promoted; active NOT_STATED |
| dbtechnologies-opera-405 | — | specification table columns not recoverable; series heading says "professional active speaker" | NOT_EXTRACTED for both; values untouched |

Ten fields promoted, seven URL outcomes recorded. Note the deliberate differences: KEF LS3/5A and EV Sx100+
keep `active` unresolved because their sheets only print an amplifier-requirements figure, while the Tannoy
and Spendor manuals give wiring instructions to an external amplifier.

## Batch 42 — two Electro-Voice documents on a retailer host, one archive copy

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| electro-voice-tx1122 | 2 / false | title "… 500W Passive Loudspeaker, Black"; "LF Transducer: SMX2120", "HF Transducer: DH3"; "Internal Crossover: Yes" | both promoted |
| electro-voice-zx4 | 2 | "LF Transducer: EVS15-SF, 15 in (381mm) Driver", "HF Transducer: DH3, 1 in (25.4mm) exit Compression Driver" | driverCount promoted; active NOT_STATED (only power handling, Speakon connectors and an "HPF PASSIVE LIMITER" block) |
| jbl-4310 | 3 | "The loudspeaker system shall consist of three direct-radiator transducers and frequency dividing network installed in a tube-ported enclosure" | driverCount promoted (`REPUTABLE_DATABASE`, Library of Congress copy); active NOT_STATED ("Power capacity 50 watts program" only) |
| jbl-4311 | — | "300-mm (12-in) … low frequency loudspeaker; 130-mm (5-in) midrange loudspeaker; 36-mm (1.4-in) high frequency direct radiator" | driverCount already `MANUFACTURER_VERIFIED`; active NOT_STATED, unchanged |

Four fields promoted, four URL outcomes recorded. The contrast is deliberate: the TX1122 listing prints the
word "Passive", so `active: false` is promotable, while the Zx4 sheet and the two JBL documents only print
power-handling and crossover data, which the policy excludes.

## Batch 43 — the rest of the Electro-Voice Tour X listings

Six Full Compass listings, each opened and read; twelve fields promoted.

| Record | driverCount | Passive evidence |
| --- | --- | --- |
| electro-voice-tx1152 | 2 (SMX2151 + DH3/2010A) | name reads "… 500W Passive Loudspeaker" |
| electro-voice-tx2152 | 3 ((2) SMX2151 + ND2) | name reads "Dual 15\" 2-Way Passive Speaker" |
| electro-voice-tx1181 | 1 (EVS18S) | name reads "18\" 500W Passive Subwoofer" |
| electro-voice-tx2181 | 2 ((2) EVS18S) | "Use with processor and dedicated amp channel" |
| electro-voice-tx1122fm | 2 (SMX2121 + DH3) | "The TX1122FM is a 12\", two-way passive floor monitor" |
| electro-voice-tx1152fm | 2 (SMX2151 + DH3) | name reads "15\" 2-Way Passive Vertical Floor Monitor" |

Every page also prints "Nominal Impedance (Passive)" and most print "Internal Crossover: Yes". The TX2181 has
no "passive" in its name, so it rests on its own instruction to use an external processor and a dedicated
amplifier channel; `Internal Crossover: No` is consistent with that.

## Batch 44 — two manufacturer PDFs served by a distributor and a retailer

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| lacoustics-arcs | 2 / false | "based on a 2-way passive design with a nominal impedance of 8 ohms"; "Transducers LF: 1 × 12\" … HF: 1 × 3\" … compression driver"; "driven and amplified by the LA4X or the LA8 controller" | both promoted |
| nexo-ps15 | 2 / false | "one 15\" 6Ω cone transducer and a 2\"-exit compression driver"; "Passive In Passive Loop Thru, Active In"; "Recommended Amplifiers 550 to 1200Watts into 8 Ωs" | both promoted |

The PS15 needs the policy's second accepted form rather than the first: its brochure never calls the product
"passive" outright, but it prints passive input connectors and a recommended external amplifier, and its
"active" mode is bi-amplification with external amplifiers.

## Batch 45 — two powered monitors

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| fostex-6301b | 1 / true | "PERSONAL MONITOR Self-Powered"; "Speaker section Type 10cm full range single cone"; "Amplifier section (EXT SP jack) Output Higher than 10W RMS"; "Mains power 120VAC 60Hz" | both promoted |
| kali-lp6 | 2 / true | "Powered: Yes"; "Amplifier Class: D"; "LF Driver: 6.5\" Woofer"; "HF Driver: 1\" Soft Dome Tweeter" | both promoted |

Both manuals are hosted by third parties (a rental house and the site's asset CDN), so neither reaches
`MANUFACTURER_VERIFIED`; the wording is explicit enough for `THIRD_PARTY_VERIFIED`.

## Batch 46 — two ManualsLib copies

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| legacy-mack-2 | 2 / true | "two-way, bi-amplified, active monitors"; 1 in HF transducer + 6.7 in LF transducer + "elliptical flat piston passive radiator"; "built-in control and amplifier electronics" | both promoted |
| jbl-vrx932 | 4 / false | "1 x JBL 2262H 305 mm (12 in)" and "3 x JBL 2407J, 25.4 mm (1 in)"; "Crossover Modes: Bi-amp / passive, externally switchable"; NL4 inputs, no mains | both promoted |

The Mackie passive radiator is deliberately not counted as a driver: it is not electrically driven, and the
record note already made that distinction.

## Batch 47 — driver counts from two Stereophile sidebars

| Record | Field | Quote | Outcome |
| --- | --- | --- | --- |
| harbeth-shl5 | driverCount 3 | "0.78\" (20mm) titanium-dome and 1\" (25mm) aluminum-dome tweeters; 7.8\" (200mm) polymeric composite-cone mid/woofer" | promoted; active NOT_STATED |
| snell-typeAIII | driverCount 4 | "10\" cone-woofer, 4\" midrange, 1\" soft-dome tweeter, rear-firing supertweeter (A/III)" | promoted; active NOT_STATED |

Both sidebars print only impedance and sensitivity, so `active` remains unresolved in both records; the
attempt is recorded as NOT_STATED rather than converted into an inference.

## Batch 48 — three KEF documents re-read

| Record | Fields | Quote | Outcome |
| --- | --- | --- | --- |
| legacy-kef-5 (Q100) | driverCount 2 | Q100 column: "Two-way bass reflex"; "130mm (5.25in.) aluminium Uni-Q"; "25mm (1in.) vented aluminium dome HF" | promoted; active NOT_STATED ("Amplifier N/A" + requirements figure only) |
| legacy-kef-7 (Blade) | driverCount 6 / false | "Uni-Q driver array: MF: 125mm (5in.) … HF: 25mm (1in.) Al dome; Bass units: LF: 4 x 225mm (9in.)"; "Single, Bi-Wire and Bi-Amp Connections"; "KEF recommends that high quality speaker cable be used" | both promoted |
| kef-reference-5 | driverCount 6 | "Uni-Q driver array with 1\" … tweeter, 5\" … midrange unit, four 6.5\" … woofers" | promoted; active NOT_STATED (recommended amplifier power only) |

Two counts are convention-dependent and were checked against existing records before promotion: a Uni-Q array
is counted as its two transducers (mid/bass cone plus concentric HF dome), matching the already-promoted KEF
LS50 record, and a passive radiator is not counted, matching the Mackie HR624 record. The Blade's `active`
rests on its connection chapter, which the policy's second accepted form covers; the Q100's wiring pages
extract as images, so that record stays unresolved rather than inferred.

## Batch 49 — four driver complements, no `active` changes

| Record | Field | Quote | Outcome |
| --- | --- | --- | --- |
| elac-uni-fi-ub5 | driverCount 3 | UB5 column: "3-way bass reflex", "Tweeter ... 1-inch soft dome", "Mid-Range ... 4-inch aluminum", "Woofer ... 5.25-inch aluminum" | promoted; supersedes the round-29 CONFLICT row (counting question, not a contradicting source) |
| kef-reference-1 | driverCount 3 | "a 1\" aluminum-dome tweeter nestled into the center of an ideally shaped 5\" aluminum cone"; "Below the Uni-Q ... is a 6.5\" woofer"; "the outputs of the Reference 1's three drivers" | promoted; active NOT_STATED |
| legacy-kef-4 | driverCount 3 | "Three fine drive units are used in Model 105"; 300 mm LF, 110 mm midrange, 52 mm HF radiator | promoted; active NOT_STATED |
| legacy-kef-1 | driverCount 2 | "Drive units: B139 bass unit (A6171), T15 tweeter (A6236)"; "Two-way, floor standing" | promoted; active left as a candidate |

### One counting convention, applied consistently

A concentric tweeter/midrange assembly counts as **two** transducers (two voice coils, two drive units), never
as one. That rule is what the KEF LS50 record already used, and it is repeated here for the KEF Uni-Q (Q100,
Reference 1) and ELAC Uni-Fi records. A passive radiator is not counted (Mackie HR624). Both conventions are
recorded in the notes so a later reader can re-check them without guessing.

### Candidate evidence left unpromoted

The Radiomuseum page for the KEF Concord prints `Power type and voltage: No Power needed` — an explicit
statement that the loudspeaker takes no electrical supply. It is not one of the three accepted forms in
`PROVENANCE-POLICY.md` (passive wording, amplifier-connection instructions, separate active electronics), so
`legacy-kef-1.active` was recorded as SUPPORTED_NOT_PROMOTED rather than promoted. Widening the standard is an
owner decision, not a batch decision.

## Batch 50 — one explicit passive statement

| Record | Field | Quote | Outcome |
| --- | --- | --- | --- |
| legacy-bw-6 (B&W CM10) | active false | "The passive loudspeaker was measured with the grille at a distance of 1 meter with a 2.83-volt input." | promoted; driverCount NOT_STATED (the Test Bench never lists the drive units) |

This is the cleanest form of the policy's first accepted case: the reviewing publication names the product
"the passive loudspeaker" in the same sentence that documents a speaker-level 2.83 V measurement.

## Batch 51 — Klipsch owner's manuals, not spec sheets

The Klipsch spec sheets are exhausted: all fourteen were read (Cornwall-2019 was `INACCESSIBLE` in round 27
and is now readable), and none calls the loudspeaker passive or tells the user to drive it from an external
amplifier, so each recorded `NOT_STATED`. The owner's manuals are a different document class and do satisfy
the policy's second accepted form. Three manuals name every target model on their cover model list:

| Document | Models named on the cover | Records settled |
| --- | --- | --- |
| Reference Premiere Speakers 2021 Manual v02 | RP-8060FA II, RP-8000F II, RP-6000F II, RP-5000F II, RP-600M II, RP-500M II (plus RP-502S II / RP-500SA II / RP-504C II / RP-404C II / RP-500C II) | `klipsch-rp8060fa`, `klipsch-rp-8000f-ii`, `klipsch-rp6000f`, `klipsch-rp-5000f-ii`, `klipsch-rp600m`, `klipsch-rp500m` |
| Reference Premiere Speakers Manual v03 (2018 generation) | RP-600M, RP-500M, RP-400M (plus RP-8060FA / RP-8000F / RP-6000F / RP-5000F / RP-4000F and the centres/surrounds) | `klipsch-rp-600m`, `klipsch-rp-500m` |
| Reference Speakers 2018 Manual v02 | R-51M, R-41M, R-52C, R-625FA, R-820F, R-620F, R-610F, R-34C, R-41SA | `legacy-klip-8` |

Each connection chapter reads: "Using 16-12 gauge speaker wire, connect the RED "positive" (+) terminal of
the LEFT speaker to the RED "positive" (+) terminal of your amplifier's LEFT channel. Connect the BLACK
"negative" (–) terminal of the LEFT speaker to the BLACK "negative" (–) terminal of your amplifier's LEFT
channel." No mains inlet, power cord or built-in amplifier is described anywhere in the manuals, so the
external-amplifier form applies and `active` is `false` at `MANUFACTURER_VERIFIED`.

Also checked and deliberately **not** used:

- `Heritage-Manual-2005_…rccj.pdf` covers Klipschorn, La Scala II, **Cornwall III** and **Heresy III**. The
  records are the IV revisions, so substituting it would be a related-model promotion.
- `Cornwall-2019_Manual_v02.pdf` and `Heresy-2019_Manual_v01_…egqp.pdf` have the same amplifier wiring
  chapters, but the documents name only "Cornwall" and "Heresy" — no IV suffix anywhere. They stay
  unrecorded until the revision can be tied to the document.
- The Forte IV and RF-7 III owner's manuals were not found on a manufacturer host (the RF-7 III manual is
  only on third-party manual sites), so those two records keep `NOT_STATED`.

## Batch 52 — alternate sources for the dead URLs (workstream 5)

Target 5 of the brief: replace the ten `INACCESSIBLE` URLs with a document that actually serves the same
model. Six of the sixteen live fields behind them were settled on a source that answers.

| Record | Field | Value | New source | Tier |
| --- | --- | --- | --- | --- |
| `legacy-kef-3` (Model 103) | driverCount | 2 | KEF archive `.../REFERENCE SERIES MODEL 103 (1976-77)/Reference_Series_Model_103_r.pdf` | manufacturer |
| `kef-105` (Reference 105.2) | driverCount | 3 | KEF archive `.../REFERENCE SERIES MODEL 105.2 (1979-87)/Reference_Series_Model_105_2_r.pdf` | manufacturer |
| `polk-signature-s60` | driverCount | 4 | polkaudio.com archive product page `/112702.html` | manufacturer |
| `legacy-yam-2` (NS-10M) | driverCount | 2 | yamaha.com Innovation Road collection, "NS-10M / Speaker System／1978" | manufacturer |
| `marshall-marshall-1936` | driverCount | 2 | marshall.com 1936 page without the stale `?pid=` parameter | manufacturer |
| `jbl-paragon` (D44000) | driverCount | 6 | audio-database Paragon entry | reputable database |

Why the old addresses failed, in each case:

* **KEF archive** — the stored URLs were the *directory* plus a truncated filename; KEF serves
  `Reference_Series_<MODEL>_r.pdf` inside that directory. Both sheets print a drive-unit table.
* **Polk** — a retired product id (`/106513.html`); the same model is served from the archive section.
* **Marshall** — the page exists; the recorded `?pid=1007263` tracking parameter is what 404s.
* **Yamaha** — the history article (`hub.yamaha.com`) is gone, but the corporate collection entry for the
  1978 NS-10M survives and states the drive complement directly.
* **JBL Paragon** — `jp.jbl.com/jamaica.html` was never a Paragon page (it is a Jamaica jazz-bar profile).

Rejected, and recorded so they are not retried:

* **Yamaha `ns10ms.pdf`** — this is the **NS-10M STUDIO** owner's manual, not the 1978 NS-10M. Its
  "18 cm woofer / 3.5 cm soft dome" pair is the same *sizes* but a different revision, so it was not used;
  the manufacturer collection page covers the exact model instead.
* **cieri.net JBL L19 brochure (1977)** — opened and it does enumerate "a 200-mm low frequency loudspeaker,
  a 36-mm high frequency direct radiator" (two transducers), but cieri.net serves no HTTPS endpoint: the TLS
  handshake fails and a direct HTTP request returns an empty reply. With no `https://` URL that can be
  retained, the policy's source rule is unmet, so `jbl-l19.driverCount` is recorded
  `SUPPORTED_NOT_PROMOTED` and stays `CITED`.
* **DALI Oberon 1** — the live page is the discontinued-section URL and carries the spec table, but it only
  offers "Recommended Amp. Power [watts] 25 - 100" and "Connection Input | Single Wire", both excluded
  evidence, so `active` stays `NOT_STATED`.
* **KEF 103 / 105.2 `active`** — both sheets give "Amplifier Requirements | 25-100 watts per channel into
  8 ohms" (and 103: "will handle the output from 100 watt amplifiers"). Amplifier-requirement figures are
  explicitly excluded, so both stay `NOT_STATED`.

Still dead and unresolved (four records, six live fields): `kef-105.active`, `legacy-kef-3.active`,
`polk-signature-s60.active`, `marshall-marshall-1936.active`, `jbl-l19.active`, plus the IK iLoud MTM
news id, the Pioneer Elite S-1EX Sound & Vision page, and the `jp.jbl.com` Paragon URL.

## Batch 53 — UNSOURCED nulls from documents already in hand

Workstream 3 of the brief (the unsourced / no-provenance pool) opened with the 71 `UNSOURCED` fields.
Three records had exact-model manufacturer documents that were **already opened this session** for other
work, so no new fetching was needed — the earlier passes had simply never pointed at these records:

| Record | Field | Value | Document | Why it fits |
| --- | --- | --- | --- | --- |
| `yamaha-ns10m` (NS-10M **Studio**) | driverCount | 2 | Yamaha `ns10ms.pdf` | "Components \| LF: JA1801 (18 cm cone)  HF: JA0518A (3.5 cm soft dome)" |
| `yamaha-ns10m` (NS-10M **Studio**) | active | false | Yamaha `ns10ms.pdf` | "BEFORE MAKING SPEAKER CONNECTIONS, MAKE SURE YOUR POWER AMPLIFIER IS TURNED OFF!" |
| `klipsch-rp8000f` (RP-8000F) | active | false | Reference Premiere manual v03 | RP-8000F is on the cover model list; connection chapter wires it to an external amplifier |
| `klipsch-r51m` (R-51M) | active | false | Reference Speakers 2018 v02 | R-51M is on the cover model list; same connection chapter |

The Yamaha case is a revision catch worth recording. In batch 52 the `ns10ms.pdf` manual was **rejected**
for `legacy-yam-2`, because that record is the **1978 NS-10M** and the manual covers the **NS-10M STUDIO**.
That rejection was correct for `legacy-yam-2` — but `yamaha-ns10m` is a *separate catalogue record* for the
Studio variant, and this manual is exactly its document. Same evidence, opposite verdicts, because the two
records are different products. Rejecting a source for one record is not a judgement on the source.

Written through `apply-structural-batch.py 29` (the sanctioned path for `UNSOURCED` nulls: it asserts the
value is `None`, the status is `UNSOURCED`, and the source is an `https://` manufacturer URL), with
`apply-round29-batch53.py` recording the same four decisions against the source URLs and the ledger.

## Tool fixes in this round

- `make-provenance-queue.py`: accepts `RECORD_ARCHIVED` outcomes and verifies the record really is retired.
- `build-field-provenance-inventory.py`: no longer double-counts ids that exist both in `speakers.json` and
  in an older `removed-*.json` snapshot (e.g. `legacy-jbl-6`); live rows are the only writable ones.
- `build-field-provenance-inventory.py`: archive rows keep their own `location` so the work list can be
  sorted by live fields.

## Counts after this round

| Status | Before (Round 28 tip) | Now |
| --- | --- | --- |
| `MANUFACTURER_VERIFIED` | 2422 | **2421** |
| `CITED_IN_NOTES_UNCHECKED` | 247 | **136 live** (171 stored, 35 archived) |
| `UNSOURCED` | 81 (73 after policy) | **67** |
| `THIRD_PARTY_VERIFIED` | 24 | **111** |
| `NO_PROVENANCE` | 363 | 363 |
| queue items | 212 / 157 URLs | **136 / 124 URLs** |
| records with backlog | 336 of 657 | **298 of 657** |

`npm test`, typecheck, both audit scripts and the release-docs generators are run after every batch; no
values were written by an audit script and no test was relaxed.

## Still open

- 136 live `CITED_IN_NOTES_UNCHECKED` fields on 124 URLs remain. Batch 51 closed nine Klipsch `active`
  fields and batch 52 closed six `driverCount` fields behind dead URLs; what is left is dominated by
  `active`, which the great majority of these documents never state at all.
- 71 `UNSOURCED` fields and 168 no-provenance nulls remain. This round recorded 12 documented outcomes for
  that pool: 8 assessments (ATC, Wilson, Polk, Dutch & Dutch, EV SX300 ×2, EV Eliminator ×2) that stay null,
  and 4 promotions on explicit evidence (EV EKX-15P driverCount/active with MANUFACTURER_VERIFIED; Bose 802
  Series II driverCount/active with THIRD_PARTY_VERIFIED).
- 51 directivity leads (0 imported), the 9 archive ZIPs, Genelec 8331A SOFA (MD5 confirmed on the source).
- 27 response-dataset blocks (24 active series, 25 records) and the ELX200-15 exclusion.
- The MV fields have been host-audited only for `driverCount`/`active` on non-manufacturer hosts (23
  corrections); the remaining 2,403 MV fields, including the large non-structural set, have not been
  re-audited field-by-field.
