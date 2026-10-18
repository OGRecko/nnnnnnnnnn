import assert from "node:assert/strict";
import { calibrateRelativeLevel } from "./splCalibration";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== splCalibration (direct) ===\n");

check("calibrated level equals the measurement and the offset is measured - simulated", () => {
  const r = calibrateRelativeLevel(-12.5, 83);
  assert.equal(r.offsetDb, 95.5); assert.equal(r.calibratedDb, 83);
  assert.equal(r.measuredDb, 83); assert.equal(r.simulatedRelativeDb, -12.5);
});
check("the reference states the level is user-supplied, never a standard", () => {
  assert.match(calibrateRelativeLevel(0, 70).reference, /user-supplied/);
});
check("zero and negative levels are valid", () => {
  assert.equal(calibrateRelativeLevel(0, 0).offsetDb, 0);
  assert.equal(calibrateRelativeLevel(5, -3).offsetDb, -8);
});
check("non-finite inputs throw instead of producing NaN", () => {
  for (const [s, m] of [[NaN, 80], [0, NaN], [Infinity, 80], [0, -Infinity]]) assert.throws(() => calibrateRelativeLevel(s, m), /finite/);
});

console.log(`\n=== ${passed} passed ===`);
