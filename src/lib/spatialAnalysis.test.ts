import assert from "node:assert/strict";
import { LIMITS } from "./publicLimits";
import { buildHeatmapData, checkSpatialResolution, computeAllSpatialSummaries, computeSpatialSummary, estimateGridReceiverCount, generateReceiverGrid } from "./spatialAnalysis";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== spatialAnalysis (direct) ===\n");

const grid = (o: Partial<{ xMin: number; xMax: number; yMin: number; yMax: number; spacing: number; zHeight: number }> = {}) =>
  ({ xMin: 0.1, xMax: 0.9, yMin: 0.1, yMax: 0.9, spacing: 1, zHeight: 1.2, ...o }) as any;

check("summary: known statistics, ignoring null/undefined/NaN/Infinity", () => {
  const s = computeSpatialSummary("RT60", [1, 2, 3, 4, null, undefined, NaN, Infinity])!;
  assert.equal(s.validCount, 4); assert.equal(s.min, 1); assert.equal(s.max, 4);
  assert.equal(s.mean, 2.5); assert.equal(s.median, 2.5);
  assert.ok(Math.abs(s.stdDev - Math.sqrt(1.25)) < 1e-12);
  assert.equal(s.metric, "RT60");
});
check("summary: odd-count median; fewer than two valid values -> null (no fake spread)", () => {
  assert.equal(computeSpatialSummary("x", [5, 1, 3])!.median, 3);
  assert.equal(computeSpatialSummary("x", [1]), null);
  assert.equal(computeSpatialSummary("x", [NaN, null, 2]), null);
  assert.equal(computeSpatialSummary("x", []), null);
});
check("summary does not mutate its input", () => {
  const v = [3, 1, 2]; computeSpatialSummary("x", v); assert.deepEqual(v, [3, 1, 2]);
});
check("computeAll: only metrics with >=2 valid receivers are summarised", () => {
  const mk = (id: string, rt60: number | null, spl: number | null) => ({ id, position: { x: 0.5, y: 0.5, z: 1.2 }, metrics: { rt60, spl } }) as any;
  const out = computeAllSpatialSummaries([mk("a", 0.5, 70), mk("b", 0.7, null), mk("c", null, null)]);
  assert.deepEqual(out.map((s) => s.metric), ["RT60"]);
  assert.equal(out[0].validCount, 2);
});

check("grid: count matches the estimator and every receiver is inside the room", () => {
  const def = grid({ spacing: 1.5 });
  const r = generateReceiverGrid(def, 10, 10);
  assert.equal(r.length, estimateGridReceiverCount(def, 10, 10));
  for (const p of r) { assert.ok(p.x >= 0.02 && p.x <= 0.98 && p.y >= 0.02 && p.y <= 0.98); assert.equal(p.z, 1.2); }
  assert.equal(new Set(r.map((p) => p.id)).size, r.length);
});
check("grid: an exact-fit axis keeps its last row (no floating-point drift)", () => {
  // 0.1 .. 0.7 in 0.1 steps is 7 points; naive accumulation drops the last one.
  const def = grid({ xMin: 0.1, xMax: 0.7, yMin: 0.5, yMax: 0.5, spacing: 1 });
  assert.equal(generateReceiverGrid(def, 10, 10).length, 7);
});
check("grid: more than the receiver limit is rejected BEFORE allocation (regression: 1 mm spacing)", () => {
  assert.throws(() => generateReceiverGrid(grid({ spacing: 0.001 }), 10, 10), /limit is 64/);
  assert.equal(estimateGridReceiverCount(grid({ spacing: 0.001 }), 10, 10) > LIMITS.MAX_RECEIVERS, true);
  assert.equal(generateReceiverGrid(grid({ xMin: 0.1, xMax: 0.8, yMin: 0.1, yMax: 0.8, spacing: 1 }), 10, 10).length, 64);
  assert.throws(() => generateReceiverGrid(grid({ xMin: 0.1, xMax: 0.9, yMin: 0.1, yMax: 0.8, spacing: 1 }), 10, 10), /limit is 64/); // 9 x 8 = 72
});
check("grid: an infinite or NaN bound terminates with an error (regression: infinite loop)", () => {
  for (const bad of [{ xMax: Infinity }, { yMax: Infinity }, { xMin: -Infinity }, { xMin: NaN }, { yMax: NaN }]) {
    assert.throws(() => generateReceiverGrid(grid(bad), 10, 10), /finite/, JSON.stringify(bad));
  }
});
check("grid: invalid spacing or room size throws; the estimator returns 0", () => {
  for (const [sp, L, W] of [[0, 10, 10], [-1, 10, 10], [NaN, 10, 10], [1, 0, 10], [1, 10, -3], [1, NaN, 10], [Infinity, 10, 10]] as const) {
    assert.throws(() => generateReceiverGrid(grid({ spacing: sp }), L, W), /spacing/, `${sp},${L},${W}`);
    assert.equal(estimateGridReceiverCount(grid({ spacing: sp }), L, W), 0);
  }
});
check("grid: min > max yields no receivers, not a crash", () => {
  assert.equal(generateReceiverGrid(grid({ xMin: 0.9, xMax: 0.1 }), 10, 10).length, 0);
  assert.equal(estimateGridReceiverCount(grid({ xMin: 0.9, xMax: 0.1 }), 10, 10), 0);
});

check("heatmap: converts to metres, skips missing/NaN values, keeps an explicit z of 0 and null for unknown z", () => {
  const rs = [
    { id: "a", position: { x: 0.5, y: 0.25, z: 0 }, metrics: { rt60: 0.6 } },
    { id: "b", position: { x: 1, y: 1 }, metrics: { rt60: 0.8 } },
    { id: "c", position: { x: 0.1, y: 0.1, z: 1 }, metrics: { rt60: NaN } },
    { id: "d", position: { x: 0.1, y: 0.1, z: 1 }, metrics: {} },
  ] as any;
  const h = buildHeatmapData("RT60", rs, 8, 4);
  assert.equal(h.interpolated, false);
  assert.deepEqual(h.points.map((p) => [p.receiverId, p.x, p.y, p.z, p.value]), [["a", 4, 1, 0, 0.6], ["b", 8, 4, null, 0.8]]);
});

check("resolution warning triggers only above room-min/4", () => {
  assert.equal(checkSpatialResolution(1, 8, 4), null);
  assert.equal(checkSpatialResolution(1.0001, 8, 4)?.code, "LOW_SPATIAL_RESOLUTION");
  assert.match(checkSpatialResolution(3, 8, 4)!.message, /3\.00 m/);
});

console.log(`\n=== ${passed} passed ===`);
