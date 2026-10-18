import assert from "node:assert/strict";
import * as mat from "./materials";
import { ABSORPTION, UnknownMaterialError, getAbsorption, getAbsorptionOrNull, getOctaveAbsorption, isKnownMaterial, nrc } from "./absorption";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== absorption (direct) ===\n");

const BANDS = ["hz125", "hz250", "hz500", "hz1000", "hz2000", "hz4000"] as const;

check("every material has finite coefficients in [0,1] for 125 Hz-4 kHz and 8 kHz is a number in [0,1] or null", () => {
  const ids = Object.keys(ABSORPTION);
  assert.ok(ids.length > 10, "material table must not be trivially small");
  for (const id of ids) {
    for (const b of BANDS) { const v = ABSORPTION[id][b]; assert.ok(Number.isFinite(v) && v >= 0 && v <= 1, `${id}.${b}=${v}`); }
    const v8 = ABSORPTION[id].hz8000;
    assert.ok(v8 === null || (Number.isFinite(v8) && v8 >= 0 && v8 <= 1), `${id}.hz8000=${v8}`);
  }
});

check("unknown / null / undefined / empty ids throw UnknownMaterialError and never substitute a default", () => {
  for (const bad of ["nope", "", null, undefined, " drywall"]) {
    assert.throws(() => getAbsorption(bad as any), (e: any) => e instanceof UnknownMaterialError && e.name === "UnknownMaterialError");
    assert.equal(isKnownMaterial(bad as any), false);
  }
});

check("prototype keys are not materials (no inherited-property lookup)", () => {
  for (const bad of ["__proto__", "constructor", "toString", "hasOwnProperty"]) {
    assert.equal(isKnownMaterial(bad), false, bad);
    assert.throws(() => getAbsorption(bad), UnknownMaterialError);
    assert.equal(getOctaveAbsorption(bad, 500), "N/A", bad);
    assert.deepEqual(Object.values(getAbsorptionOrNull(bad)), [null, null, null, null, null, null, null], bad);
  }
});

check("getAbsorptionOrNull: known id returns real coefficients, unknown returns all-null", () => {
  const id = Object.keys(ABSORPTION)[0];
  assert.equal(getAbsorptionOrNull(id), ABSORPTION[id]);
  assert.equal(getAbsorptionOrNull("nope").hz500, null);
});

check("getOctaveAbsorption: exact octave centres only; off-centre and non-numeric frequencies are N/A", () => {
  const id = Object.keys(ABSORPTION)[0];
  assert.equal(getOctaveAbsorption(id, 1000), ABSORPTION[id].hz1000);
  for (const f of [0, 100, 126, 1001, -1000, NaN, Infinity]) assert.equal(getOctaveAbsorption(id, f), "N/A", String(f));
});

check("a missing 8 kHz coefficient is reported N/A, never copied from 4 kHz", () => {
  const missing = Object.keys(ABSORPTION).filter((k) => ABSORPTION[k].hz8000 === null);
  for (const id of missing) assert.equal(getOctaveAbsorption(id, 8000), "N/A", id);
  const present = Object.keys(ABSORPTION).filter((k) => ABSORPTION[k].hz8000 !== null);
  for (const id of present) assert.equal(getOctaveAbsorption(id, 8000), ABSORPTION[id].hz8000, id);
});

check("nrc is the 250-2000 Hz mean rounded to 2 dp", () => {
  assert.equal(nrc({ hz125: 0, hz250: 0.1, hz500: 0.2, hz1000: 0.3, hz2000: 0.4, hz4000: 0, hz8000: null }), 0.25);
  assert.equal(nrc({ hz125: 0.9, hz250: 0, hz500: 0, hz1000: 0, hz2000: 0, hz4000: 0.9, hz8000: 0.9 }), 0);
});

check("materials.ts lookups also ignore inherited keys (regression)", () => {
  const m = mat;
  for (const bad of ["__proto__", "constructor", "toString"]) {
    assert.equal(m.getAbsorption(bad, 0.42), 0.42, bad);
    assert.equal(m.getOctaveAbsorption(bad, 500), "N/A", bad);
  }
});

console.log(`\n=== ${passed} passed ===`);
