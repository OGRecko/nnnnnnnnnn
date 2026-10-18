import assert from "node:assert/strict";
import { BRANDS, SPEAKERS, SPEAKER_SPECS, TYPES, getSpeakerById } from "./speakers";
import { resolveSensitivity } from "./speakerResponse";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== speakers adapter (derived from speakers.json, nothing hardcoded) ===\n");

const KNOWN_CATEGORIES = new Set(["studio-monitor", "bookshelf", "floor-standing", "pa", "ceiling", "in-wall", "subwoofer", "portable", "soundbar", "car-audio", "guitar-cab", "smart-speaker"]);

check("adapter is 1:1 with the raw catalog and ids are unique", () => {
  assert.equal(SPEAKERS.length, SPEAKER_SPECS.length);
  assert.ok(SPEAKERS.length > 0);
  assert.equal(new Set(SPEAKERS.map((s) => s.id)).size, SPEAKERS.length);
  SPEAKERS.forEach((s, i) => { assert.equal(s.id, SPEAKER_SPECS[i].id); assert.equal(s.brand, SPEAKER_SPECS[i].brand); assert.equal(s.model, SPEAKER_SPECS[i].model); });
});

check("every record uses a known category and no raw slug leaks into the displayed type (regression: hifi/cinema/custom)", () => {
  const known = new Set([...KNOWN_CATEGORIES, "hifi", "cinema", "custom"]);
  assert.deepEqual(SPEAKER_SPECS.filter((s) => !known.has(s.category)).map((s) => `${s.id}:${s.category}`), []);
  for (const [i, s] of SPEAKERS.entries()) assert.notEqual(s.type, SPEAKER_SPECS[i].category, `${s.id} shows raw category "${s.type}"`);
});

check("third-party / reputable-database sensitivities are labelled third-party, never 'unavailable' (regression)", () => {
  const tp = SPEAKER_SPECS.filter((s) => s.sensitivity?.value && ["THIRD_PARTY", "REPUTABLE_DATABASE"].includes((s.sensitivity as any).sourceType) && s.sensitivity.status !== "LEGACY");
  assert.ok(tp.length > 0);
  for (const s of tp) { assert.equal(SPEAKERS.find((x) => x.id === s.id)!.sensitivitySource, "third-party", s.id); assert.equal(resolveSensitivity(s).source === "third-party" || resolveSensitivity(s).isFallback, true, s.id); }
});

check("no speaker is shown as verified unless its overall status is FULLY_VERIFIED", () => {
  for (const [i, s] of SPEAKERS.entries()) assert.equal(s.verified, SPEAKER_SPECS[i].overallStatus === "FULLY_VERIFIED", s.id);
});

check("sensitivity fields are mutually consistent: no value <=> 'unavailable' + fallback", () => {
  for (const s of SPEAKERS) {
    if (s.manufacturerSensitivityDb === null) { assert.equal(s.sensitivitySource, "unavailable", s.id); assert.equal(s.sensitivityIsFallback, true, s.id); }
    else assert.notEqual(s.sensitivitySource, "unavailable", `${s.id} has a value but no source`);
    assert.equal(s.estimatedSensitivityDb, null, `${s.id}: estimates must never be synthesised by the adapter`);
  }
});

check("the fallback flag always agrees with resolveSensitivity (single source of truth)", () => {
  for (const [i, s] of SPEAKERS.entries()) assert.equal(s.sensitivityIsFallback, resolveSensitivity(SPEAKER_SPECS[i]).isFallback, s.id);
});

check("a 2.83 V/1 m sensitivity without a known impedance is flagged as fallback, not silently normalised", () => {
  const bad = SPEAKERS.filter((s) => s.manufacturerSensitivityDb !== null && /^2\.83/i.test(s.sensitivityReference ?? "") && !(typeof s.impedanceOhm === "number" && s.impedanceOhm > 0));
  for (const s of bad) assert.equal(s.sensitivityIsFallback, true, s.id);
});

check("every populated sensitivity has a plausible dB value and an auditable source URL", () => {
  for (const [i, s] of SPEAKERS.entries()) {
    if (s.manufacturerSensitivityDb === null) continue;
    assert.ok(s.manufacturerSensitivityDb > 40 && s.manufacturerSensitivityDb < 140, `${s.id}: ${s.manufacturerSensitivityDb} dB`);
    const src = (SPEAKER_SPECS[i].sensitivity as any)?.source;
    assert.ok(typeof src === "string" && /^https?:\/\//.test(src), `${s.id}: sensitivity has no source URL (${String(src)})`);
  }
});

check("impedance, when present, is a positive finite number", () => {
  for (const s of SPEAKERS) if (s.impedanceOhm !== null) assert.ok(Number.isFinite(s.impedanceOhm) && s.impedanceOhm > 0 && s.impedanceOhm <= 64, `${s.id}: ${s.impedanceOhm}`);
});

check("BRANDS and TYPES are sorted, unique, and cover every record", () => {
  assert.deepEqual([...BRANDS], [...new Set(BRANDS)].sort());
  assert.deepEqual([...TYPES], [...new Set(TYPES)].sort());
  for (const s of SPEAKERS) { assert.ok(BRANDS.includes(s.brand)); assert.ok(TYPES.includes(s.type)); }
});

check("getSpeakerById: hit, miss, and inherited-property ids never resolve", () => {
  const first = SPEAKER_SPECS[0];
  assert.equal(getSpeakerById(first.id), first);
  for (const bad of ["", "nope", "__proto__", "constructor", "toString", "JBL-LSR32"]) assert.equal(getSpeakerById(bad), undefined, bad);
});

check("brand+model pairs are unique (case-insensitive)", () => {
  assert.equal(new Set(SPEAKERS.map((s) => `${s.brand}::${s.model}`.toLowerCase())).size, SPEAKERS.length);
});

console.log(`\n=== ${passed} passed ===`);
