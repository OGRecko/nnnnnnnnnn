import assert from "node:assert/strict";
import { generateInterpolationGrid, interpolateIDW } from "./interpolation";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== interpolation (direct) ===\n");

const P = [{ x: 0, y: 0, value: 10 }, { x: 1, y: 0, value: 20 }, { x: 0, y: 1, value: 30 }, { x: 1, y: 1, value: 40 }];

check("no points -> null; exact hit returns the measured value", () => {
  assert.equal(interpolateIDW(0.5, 0.5, []), null);
  assert.equal(interpolateIDW(1, 1, P), 40);
});

check("symmetric point is the mean; result stays within the data range", () => {
  assert.ok(Math.abs(interpolateIDW(0.5, 0.5, P)! - 25) < 1e-12);
  for (let i = 0; i <= 10; i++) for (let j = 0; j <= 10; j++) { const v = interpolateIDW(i / 10, j / 10, P)!; assert.ok(v >= 10 - 1e-9 && v <= 40 + 1e-9); }
});

check("maxRadius excludes far points and yields null (not 0) when none are in range", () => {
  assert.equal(interpolateIDW(0.1, 0.0, P, 2, 0.5), 10);
  assert.equal(interpolateIDW(0.5, 0.5, P, 2, 0.1), null);
});

check("a single point fills the whole domain with its value", () => {
  assert.equal(interpolateIDW(0.3, 0.9, [{ x: 0.5, y: 0.5, value: 7 }]), 7);
});

check("NaN/Infinity query coordinates never produce a fabricated number", () => {
  for (const [x, y] of [[NaN, 0.5], [0.5, NaN], [Infinity, 0], [-Infinity, 0]]) {
    const v = interpolateIDW(x, y, P);
    assert.ok(v === null || Number.isNaN(v) === false && Number.isFinite(v), `(${x},${y}) -> ${v}`);
  }
});

check("grid: size, null on empty input, corners equal the nearest sample", () => {
  assert.equal(generateInterpolationGrid(P, 8).length, 64);
  assert.ok(generateInterpolationGrid([], 8).every((v) => v === null));
  const g = generateInterpolationGrid(P, 9);
  assert.equal(g[0], 10); assert.equal(g[8], 20); assert.equal(g[72], 30); assert.equal(g[80], 40);
});

check("grid resolution 1 does not emit NaN", () => {
  const g = generateInterpolationGrid(P, 1);
  assert.equal(g.length, 1);
  assert.ok(g[0] === null || Number.isFinite(g[0] as number), `got ${g[0]}`);
});

console.log(`\n=== ${passed} passed ===`);
