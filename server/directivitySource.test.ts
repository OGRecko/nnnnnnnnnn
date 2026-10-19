/**
 * Analytic tests for the equivalent-source directivity model.
 *
 * These verify the MATHEMATICS of the fit (does the weighted node set radiate the supplied pattern?), not the FDTD
 * realisation. `npm run validate:directivity` measures the realisation in a room and is the release gate.
 */
import assert from 'node:assert/strict';
import { synthesizeDirectionalNodes, gridResolvesPattern } from './directivitySource';

let passed = 0;
function check(name: string, fn: () => void) {
  try { fn(); passed++; console.log(`  PASS  ${name}`); }
  catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; }
}
console.log('\n=== directivity equivalent-source synthesis (analytic) ===\n');

const rad = (d: number) => (d * Math.PI) / 180;
const FREQS = [125, 250, 500, 1000, 2000];
const REAR_DB = -30;
const points: Record<string, number[]> = {};
for (let el = -90; el <= 90; el += 30) for (let az = 0; az < 360; az += 30) {
  const c = Math.cos(rad(az)) * Math.cos(rad(el));
  points[`${az},${el}`] = FREQS.map(() => (REAR_DB * (1 - c)) / 2);
}
const data = { frequencies: FREQS, angularResolution: 30, points };
const identity = (x: number, y: number, z: number) => ({ x, y, z });
const DX = 0.137;

function farField(nodes: ReturnType<typeof synthesizeDirectionalNodes>, freq: number, s: [number, number, number]): number {
  const k = (2 * Math.PI * freq) / 343;
  let re = 0, im = 0;
  for (const n of nodes) {
    const phase = -k * (s[0] * n.offset[0] + s[1] * n.offset[1] + s[2] * n.offset[2]) * DX;
    const c = Math.cos(phase), sn = Math.sin(phase);
    re += n.re * c - n.im * sn;
    im += n.re * sn + n.im * c;
  }
  return Math.hypot(re, im);
}

check('a supplied 30 dB pattern is radiated with the specified front-to-rear difference (analytic far field)', () => {
  for (const f of [250, 500]) {
    const nodes = synthesizeDirectionalNodes(data as any, f, DX, identity);
    assert.ok(nodes.length > 20, `expected a node cluster, got ${nodes.length}`);
    const ratio = 20 * Math.log10(farField(nodes, f, [0, 1, 0]) / farField(nodes, f, [0, -1, 0]));
    assert.ok(ratio > 25, `${f} Hz front/rear ${ratio.toFixed(1)} dB should be within a few dB of 30`);
  }
});

check('the fitted pattern is accurate across the sphere, not just on the two measured directions', () => {
  const f = 500;
  const nodes = synthesizeDirectionalNodes(data as any, f, DX, identity);
  let sum = 0, count = 0;
  for (let el = -60; el <= 60; el += 30) for (let az = 0; az < 360; az += 30) {
    const c = Math.cos(rad(az)) * Math.cos(rad(el));
    const target = Math.pow(10, (REAR_DB * (1 - c)) / 2 / 20);
    const got = farField(nodes, f, [Math.sin(rad(az)) * Math.cos(rad(el)), Math.cos(rad(az)) * Math.cos(rad(el)), Math.sin(rad(el))]);
    sum += Math.pow(20 * Math.log10(got / target), 2); count++;
  }
  const rms = Math.sqrt(sum / count);
  assert.ok(rms < 2.5, `rms pattern error ${rms.toFixed(2)} dB`);
});

check('rotating the source rotates the radiated pattern', () => {
  const f = 500;
  const nodes = synthesizeDirectionalNodes(data as any, f, DX, identity);
  const forward = farField(nodes, f, [0, 1, 0]);
  assert.ok(forward > farField(nodes, f, [1, 0, 0]) && forward > farField(nodes, f, [0, 0, 1]), 'forward is the loudest axis');
  // A yaw of 90 degrees maps the speaker's forward axis onto world -X; the fit uses the rotated local directions.
  const yaw = rad(90);
  const toLocal = (x: number, y: number, z: number) => ({ x: Math.cos(yaw) * x + Math.sin(yaw) * y, y: -Math.sin(yaw) * x + Math.cos(yaw) * y, z });
  const rotated = synthesizeDirectionalNodes(data as any, f, DX, toLocal);
  const toMinusX = farField(rotated, f, [-1, 0, 0]);
  assert.ok(toMinusX > 0.8 * forward, `rotated on-axis gain ${toMinusX.toFixed(3)} vs ${forward.toFixed(3)}`);
});

check('the grid-resolution guard refuses to claim a pattern it cannot carry', () => {
  assert.equal(gridResolvesPattern(500, 0.137), true, '500 Hz at 13.7 cm cells is 5 cells per wavelength');
  assert.equal(gridResolvesPattern(2000, 0.137), false, '2 kHz at 13.7 cm cells is unresolved');
  assert.equal(gridResolvesPattern(0, 0.1), false);
});

check('weights are finite and the on-axis gain is normalised to the dataset value', () => {
  const nodes = synthesizeDirectionalNodes(data as any, 500, DX, identity);
  for (const n of nodes) assert.ok(Number.isFinite(n.re) && Number.isFinite(n.im), 'finite weights');
  const onAxis = farField(nodes, 500, [0, 1, 0]);
  assert.ok(Math.abs(onAxis - 1) < 1e-6, `on-axis ${onAxis}`);
});

console.log(`\n=== ${passed} passed ===`);
