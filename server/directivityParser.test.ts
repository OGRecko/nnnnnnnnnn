import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { DIRECTIVITY_LIMITS, getInterpolatedMagnitude, parseDirectivityFile } from "./directivityParser";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== directivityParser (fixtures, hostile inputs) ===\n");

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "fixtures", "directivity");
const fx = (n: string) => path.join(dir, n);

check("valid synthetic fixture parses with sorted frequencies and per-bin rows", () => {
  const d = parseDirectivityFile(fx("valid-synthetic.json"));
  assert.deepEqual(d.frequencies, [250, 1000, 4000]);
  assert.equal(Object.keys(d.points).length, 12);
  for (const row of Object.values(d.points)) assert.equal(row.length, 3);
  assert.equal(d.angularResolution, 90);
});

check("unsorted frequencies are re-indexed so each magnitude stays with its frequency", () => {
  const d = parseDirectivityFile(fx("valid-unsorted-frequencies.json"));
  assert.deepEqual(d.frequencies, [250, 1000, 4000]);
  // file order is [4000, 250, 1000] -> magnitudes [-3, 0, -1.5]; sorted order [250, 1000, 4000] -> [0, -1.5, -3]
  assert.deepEqual(d.points["0,0"], [0, -1.5, -3]);
  assert.deepEqual(d.points["90,0"], [-6, -7.5, -9]);
});

const HOSTILE: Array<[string, RegExp]> = [
  ["hostile-not-json.json", /not valid JSON/],
  ["hostile-top-level-array.json", /top level must be an object/],
  ["hostile-null.json", /top level must be an object/],
  ["hostile-missing-frequencies.json", /missing frequencies/],
  ["hostile-points-not-array.json", /missing points array/],
  ["hostile-null-point.json", /Malformed angular point/],
  ["hostile-string-angle.json", /Malformed angular point/],
  ["hostile-angle-out-of-range.json", /azimuth must be within/],
  ["hostile-elevation-out-of-range.json", /elevation within/],
  ["hostile-magnitude-huge.json", /Invalid directivity magnitude row/],
  ["hostile-magnitude-string.json", /Invalid directivity magnitude row/],
  ["hostile-magnitude-length-mismatch.json", /Invalid directivity magnitude row/],
  ["hostile-duplicate-frequencies.json", /duplicate frequency/],
  ["hostile-frequency-negative.json", /frequency must be finite, positive/],
  ["hostile-frequency-above-limit.json", /<= 24000/],
  ["hostile-too-many-frequencies.json", /1 to 16/],
  ["hostile-empty-points.json", /points array is empty/],
  ["hostile-bad-resolution.json", /angularResolution/],
  ["hostile-resolution-huge.json", /angularResolution/],
];
for (const [file, re] of HOSTILE) check(`rejects ${file}`, () => assert.throws(() => parseDirectivityFile(fx(file)), (e: any) => e instanceof Error && re.test(e.message) && !(e instanceof TypeError)));

check("prototype-pollution keys in the file do not pollute Object.prototype or the result", () => {
  const d = parseDirectivityFile(fx("hostile-proto-keys.json"));
  assert.equal(({} as any).polluted, undefined);
  assert.equal(Object.getPrototypeOf(d.points), null);
  assert.equal(d.brand, "__proto__");
  assert.deepEqual(d.frequencies, [1000]);
});

check("unsupported and proprietary extensions are refused with a clear message", () => {
  assert.throws(() => parseDirectivityFile("x.gll"), /proprietary/);
  for (const ext of [".clf", ".ulf", ".csv", ".txt", ""]) assert.throws(() => parseDirectivityFile(`x${ext}`), /Unsupported directivity file format/);
});

check("a missing file or a directory is a clean error, not a crash", () => {
  assert.throws(() => parseDirectivityFile(fx("does-not-exist.json")), /ENOENT/);
  const d = fs.mkdtempSync(path.join(os.tmpdir(), "dir-"));
  const asJson = path.join(d, "folder.json"); fs.mkdirSync(asJson);
  assert.throws(() => parseDirectivityFile(asJson), /regular file/);
  fs.rmSync(d, { recursive: true, force: true });
});

check("oversized point count and oversized files are rejected before processing", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "dir-"));
  const many = Array.from({ length: DIRECTIVITY_LIMITS.MAX_POINTS + 1 }, (_, i) => ({ azimuth: i % 360, elevation: 0, magnitude: [0] }));
  fs.writeFileSync(path.join(tmp, "many.json"), JSON.stringify({ frequencies: [1000], angularResolution: 10, points: many }));
  assert.throws(() => parseDirectivityFile(path.join(tmp, "many.json")), /too many angular points/);
  fs.writeFileSync(path.join(tmp, "big.json"), Buffer.alloc(DIRECTIVITY_LIMITS.MAX_FILE_BYTES + 1, 32));
  assert.throws(() => parseDirectivityFile(path.join(tmp, "big.json")), /too large/);
  fs.rmSync(tmp, { recursive: true, force: true });
});

const D = parseDirectivityFile(fx("valid-synthetic.json"));

check("on-axis returns the stored value; interpolation stays inside the data range", () => {
  assert.equal(getInterpolatedMagnitude(D, 1000, 0, 0), 0);
  for (let az = -180; az <= 540; az += 37) for (let el = -120; el <= 120; el += 41) {
    const v = getInterpolatedMagnitude(D, 1000, az, el);
    assert.ok(Number.isFinite(v) && v <= 1e-9 && v >= -7.5 - 1e-9, `${az},${el} -> ${v}`);
  }
});

check("azimuth wraps modulo 360 and elevation is clamped to +/-90", () => {
  assert.equal(getInterpolatedMagnitude(D, 1000, 360, 0), getInterpolatedMagnitude(D, 1000, 0, 0));
  assert.ok(Math.abs(getInterpolatedMagnitude(D, 1000, -90, 0) - getInterpolatedMagnitude(D, 1000, 270, 0)) < 1e-12);
  assert.equal(getInterpolatedMagnitude(D, 1000, 33, 500), getInterpolatedMagnitude(D, 1000, 33, 90));
});

check("frequency is linearly interpolated between bins and clamped outside them", () => {
  const at250 = getInterpolatedMagnitude(D, 250, 180, 0), at1k = getInterpolatedMagnitude(D, 1000, 180, 0);
  const mid = getInterpolatedMagnitude(D, 625, 180, 0);
  assert.ok(Math.abs(mid - (at250 + at1k) / 2) < 1e-9);
  assert.equal(getInterpolatedMagnitude(D, 10, 180, 0), at250);
  assert.equal(getInterpolatedMagnitude(D, 20000, 180, 0), getInterpolatedMagnitude(D, 4000, 180, 0));
});

check("NaN / Infinity inputs throw RangeError instead of returning NaN (regression)", () => {
  for (const [f, a, e] of [[1000, NaN, 0], [1000, 0, NaN], [NaN, 0, 0], [1000, Infinity, 0], [1000, 0, -Infinity]] as const)
    assert.throws(() => getInterpolatedMagnitude(D, f, a, e), RangeError, `${f},${a},${e}`);
});

console.log(`\n=== ${passed} passed ===`);
