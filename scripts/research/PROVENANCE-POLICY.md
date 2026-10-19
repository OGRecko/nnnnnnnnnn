# Provenance policy for `driverCount` and `active`

Status: owner instruction of 2026-10-19 ("Improve provenance policy safely"). This document defines the
`THIRD_PARTY_VERIFIED` tier for the two structural fields and the exact conditions under which it may be
used. It does not change any other field's policy and it does not promote anything by itself.

## Tiers

| Status | Meaning for `driverCount` / `active` |
| --- | --- |
| `MANUFACTURER_VERIFIED` | The value is stated by the manufacturer's own document served from the manufacturer's host, or by an exact-model manufacturer document on a host the owner has explicitly approved (`eviaudio.fr`, `fmicassets.com`, Owner Decision 1 / 2026-10-13). |
| `THIRD_PARTY_VERIFIED` | The value is explicitly stated in a third-party document that passes every condition below. It never implies manufacturer endorsement. |
| `CITED_IN_NOTES_UNCHECKED` | The value is attached to a URL in the record notes that has not been checked for that field. |
| `UNSOURCED` | No usable source is recorded. The value must be null. |

## Conditions for `THIRD_PARTY_VERIFIED`

All six must hold; failing any one keeps the field unresolved.

1. **Exact model and revision.** The document names the exact model in the catalogue. Where the product
   has revisions or variants (e.g. CR3 vs CR3-X, Thump15 vs Thump15A/THUMP15BST), the document must
   identify the same revision or the field must be independent of the difference and the note must say why.
2. **Explicit field-level evidence.** The document states the fact in words: an enumerated driver
   complement, or "powered"/"active"/built-in amplifier/AC power with internal amplification. The
   following are **not** evidence: nominal impedance, power-handling ratings, binding posts, absence of a
   crossover or amplifier mention, product category, a picture, or a related model's sheet.
3. **Retained source.** `source` is an `https://` URL that was opened in the session; `sourceType` is
   `THIRD_PARTY` (retailer, manual mirror) or `REPUTABLE_DATABASE` (documented archives/databases).
4. **Quoted evidence.** The provenance `note` contains a short verbatim quote and the document's identity
   (title, revision or date where printed).
5. **Auditable decision.** The batch ledger records: record id, field, prior state, new value, source,
   sourceType, outcome, the quote, and why `MANUFACTURER_VERIFIED` is unavailable. Value history keeps
   the before/after pair.
6. **No conflict suppression.** If another opened source contradicts the value, or the revision is
   ambiguous, the field stays unresolved (`CITED_IN_NOTES_UNCHECKED` / `UNSOURCED`) and the conflict is
   recorded.

## Rules for batches

* One record at a time; no bulk promotion and no inference from a sibling field.
* A successful HTTP response is not evidence; the statement must be read.
* Missing values stay null; do not create provenance objects for unknown fields.
* Third-party values feed the simulator only through the same field-level checks as before. A change of
  provenance tier does not change simulation behaviour by itself; any simulation exclusion rule stays in
  force.
* Counts are generated from the data by the existing scripts; never hand-edited.

## Enforcement

* `src/data/speakers.round3.test.ts` — allowed statuses and the extra requirements for
  `THIRD_PARTY_VERIFIED`.
* `scripts/lib/speakerAuditCore.mjs` (`auditWithdrawalAndExclusionRules`) — URL, `sourceType`, and evidence
  note required for the third-party tier; `UNSOURCED` must stay null.
* `scripts/speakerAuditCore.test.ts` — negative tests proving the audit rejects a bare third-party
  status.
* `scripts/research/apply-round29-policy.py` — the only script that writes this tier; it reads a data
  module with the evidence and refuses incomplete entries.
