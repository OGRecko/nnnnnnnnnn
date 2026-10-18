/**
 * Orientation of imported directivity data inside the solver. Frame (see worldToLocalDirection):
 *   world x = room LENGTH axis, world y = room WIDTH axis, world z = UP (the grid's vertical axis is ny).
 *   speaker local: +Y forward (on-axis), +X right, +Z up. yaw about up, then pitch (nose up +) about X, then roll about Y.
 */
import assert from 'node:assert/strict';
import { computeInjectionNodes, worldToLocalDirection } from './solverWorker';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== solver directivity orientation (analytic) ===\n');

const near = (a: number, b: number, tol = 1e-9) => Math.abs(a - b) <= tol;
const vec = (v: { x: number; y: number; z: number }, x: number, y: number, z: number, msg: string) => assert.ok(near(v.x, x) && near(v.y, y) && near(v.z, z), `${msg}: got (${v.x.toFixed(4)}, ${v.y.toFixed(4)}, ${v.z.toFixed(4)}) expected (${x}, ${y}, ${z})`);
const rad = (d: number) => (d * Math.PI) / 180;

check('unrotated: world +width is forward (+Y), world +length is right (+X), world up is up (+Z)', () => {
  const s = { yawDeg: 0, pitchDeg: 0, rollDeg: 0 };
  vec(worldToLocalDirection(0, 1, 0, s), 0, 1, 0, 'forward'); vec(worldToLocalDirection(1, 0, 0, s), 1, 0, 0, 'right'); vec(worldToLocalDirection(0, 0, 1, s), 0, 0, 1, 'up');
});

check('yaw turns the speaker about the vertical axis: the speaker\'s forward in the world is (-sin yaw, cos yaw, 0)', () => {
  for (const yaw of [0, 30, 90, 180, 270, -45]) {
    const f = { x: -Math.sin(rad(yaw)), y: Math.cos(rad(yaw)), z: 0 };
    vec(worldToLocalDirection(f.x, f.y, f.z, { yawDeg: yaw }), 0, 1, 0, `yaw ${yaw}`);
    vec(worldToLocalDirection(0, 0, 1, { yawDeg: yaw }), 0, 0, 1, `up stays up at yaw ${yaw}`);
  }
});

check('pitch tilts the speaker up/down (positive = nose up): its forward becomes (0, cos p, sin p)', () => {
  for (const p of [0, 15, 45, 90, -30]) vec(worldToLocalDirection(0, Math.cos(rad(p)), Math.sin(rad(p)), { pitchDeg: p }), 0, 1, 0, `pitch ${p}`);
});

check('roll spins the speaker about its own forward axis: forward is unchanged, and +X rotates into the vertical plane', () => {
  for (const r of [0, 20, 90, 180]) vec(worldToLocalDirection(0, 1, 0, { rollDeg: r }), 0, 1, 0, `forward unaffected by roll ${r}`);
  const side = worldToLocalDirection(1, 0, 0, { rollDeg: 90 }); assert.ok(near(side.x, 0) && near(Math.abs(side.z), 1) && near(side.y, 0), `roll 90 moves right into up/down: ${JSON.stringify(side)}`);
});

check('the transform is a pure rotation: it preserves length for every yaw/pitch/roll combination, and missing angles mean 0', () => {
  for (const yaw of [0, 33, 120, -77]) for (const pitch of [0, 25, -60]) for (const roll of [0, 40, 170]) {
    const v = worldToLocalDirection(0.3, -0.5, 0.8, { yawDeg: yaw, pitchDeg: pitch, rollDeg: roll }); assert.ok(near(Math.hypot(v.x, v.y, v.z), Math.hypot(0.3, 0.5, 0.8), 1e-12));
  }
  vec(worldToLocalDirection(0.2, 0.5, 0.1, {}), 0.2, 0.5, 0.1, 'no angles'); vec(worldToLocalDirection(0.2, 0.5, 0.1, { yawDeg: NaN, pitchDeg: 'x', rollDeg: null }), 0.2, 0.5, 0.1, 'junk angles are 0');
});

// ----------------------------------------------------------------- the grid mapping (the vertical-axis bug)
const F = [1000];
const sphere = () => { const points: Record<string, number[]> = {}; for (let el = -90; el <= 90; el += 30) for (let az = 0; az < 360; az += 30) { const c = Math.cos(rad(az)) * Math.cos(rad(el)); points[`${az},${el}`] = [-30 * (1 - c) / 2]; } return { frequencies: F, angularResolution: 30, points }; };
const N = 21, nx = N, ny = N, nz = N, nxz = nx * nz, c = 10;
const idxToXYZ = (idx: number) => ({ ix: idx % nx, iz: Math.floor(idx / nx) % nz, iy: Math.floor(idx / nxz) });
/** Fraction of the injected weight that lies in each half-space around the source: [+length, +width, +vertical]. */
function lobes(source: any) {
  const nodes = computeInjectionNodes({ isDirectional: true, directivityData: sphere(), ...source }, c, c, c, nx, ny, nz, nxz, 1000);
  const w = (f: (d: { ix: number; iy: number; iz: number }) => boolean) => nodes.reduce((s, n) => { const p = idxToXYZ(n.idx); return f({ ix: p.ix - c, iy: p.iy - c, iz: p.iz - c }) ? s + n.weight : s; }, 0);
  return { lengthPlus: w((d) => d.ix > 0), lengthMinus: w((d) => d.ix < 0), widthPlus: w((d) => d.iz > 0), widthMinus: w((d) => d.iz < 0), up: w((d) => d.iy > 0), down: w((d) => d.iy < 0), total: nodes.reduce((s, n) => s + n.weight, 0) };
}

check('a horizontally-aimed speaker (yaw 0) radiates toward +width, NOT toward the ceiling (regression: the vertical axis was used as forward)', () => {
  const l = lobes({ yawDeg: 0, pitchDeg: 0, rollDeg: 0 });
  assert.ok(near(l.total, 1, 1e-9), 'injection weights are normalised'); assert.ok(l.widthPlus > 1.5 * l.widthMinus, `forward lobe ${l.widthPlus.toFixed(3)} vs rear ${l.widthMinus.toFixed(3)}`);
  assert.ok(l.widthPlus > l.up, `forward (${l.widthPlus.toFixed(3)}) must beat straight up (${l.up.toFixed(3)})`); assert.ok(near(l.up, l.down, 0.02), `a level speaker is vertically symmetric (${l.up.toFixed(3)} vs ${l.down.toFixed(3)})`);
  assert.ok(near(l.lengthPlus, l.lengthMinus, 0.02), 'and left/right symmetric');
});

check('yaw 180 reverses the lobe; yaw 90 and 270 swing it along the length axis (-length / +length)', () => {
  const a = lobes({ yawDeg: 180 }); assert.ok(a.widthMinus > 1.5 * a.widthPlus, 'yaw 180 faces -width');
  const b = lobes({ yawDeg: 90 }); assert.ok(b.lengthMinus > 1.5 * b.lengthPlus, 'yaw 90 faces -length');
  const d = lobes({ yawDeg: 270 }); assert.ok(d.lengthPlus > 1.5 * d.lengthMinus, 'yaw 270 faces +length');
});

check('pitch +90 aims at the ceiling, pitch -90 at the floor; roll does not move a symmetric lobe', () => {
  const up = lobes({ pitchDeg: 90 }); assert.ok(up.up > 1.5 * up.down, `pitch +90: up ${up.up.toFixed(3)} vs down ${up.down.toFixed(3)}`);
  const dn = lobes({ pitchDeg: -90 }); assert.ok(dn.down > 1.5 * dn.up, 'pitch -90 faces the floor');
  const r = lobes({ rollDeg: 70 }); assert.ok(r.widthPlus > 1.5 * r.widthMinus, 'rolling about the forward axis keeps facing +width');
});

check('without directional data the source is a single omnidirectional node (nothing fabricated)', () => {
  const n = computeInjectionNodes({ isDirectional: false }, c, c, c, nx, ny, nz, nxz, 1000); assert.equal(n.length, 1); assert.equal(n[0].weight, 1);
  const m = computeInjectionNodes({ isDirectional: true, directivityData: { frequencies: [100], angularResolution: 30, points: { '0,0': [0] } } }, c, c, c, nx, ny, nz, nxz, 8000);
  assert.equal(m.length, 1, 'data more than half an octave away is not reused');
});

console.log(`\n=== ${passed} passed ===`);

// ----------------------------------------------------------------- end to end through the real FDTD solver
// IMPORTANT: these tests establish that orientation REACHES the solver and changes its result consistently. They deliberately do
// NOT assert that the radiated pattern matches the supplied data, because it does not: the solver's directional source (a
// weighted cluster of in-phase injection nodes) reproduces well under 1 dB of a pattern specified as 30 dB. That shortfall is
// measured by scripts/validate-directivity-fidelity.mjs and is a documented, open FAIL in FINAL_VERIFICATION, not a passing test.
import { runWave } from './solverWorker';
{
  const quiet = <T>(fn: () => T): T => { const l = console.log, w = console.warn; console.log = () => {}; console.warn = () => {}; try { return fn(); } finally { console.log = l; console.warn = w; } };
  const peak = (t: ArrayLike<number>) => { let m = 0; for (let i = 0; i < t.length; i++) m = Math.max(m, Math.abs(t[i])); return m; };
  const sphere2 = () => { const points: Record<string, number[]> = {}; for (let el = -90; el <= 90; el += 30) for (let az = 0; az < 360; az += 30) { const cc = Math.cos(rad(az)) * Math.cos(rad(el)); const m = -30 * (1 - cc) / 2; points[`${az},${el}`] = [m, m]; } return { frequencies: [250, 500], angularResolution: 30, points }; };
  const run = (src: any) => {
    const r: any = quiet(() => runWave({ L: 14, W: 14, H: 4, steps: 260, fmax: 500, accuracyMode: 'fast', poly: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], wallMaterial: 'drywall', floorMaterial: 'wood_floor', ceilMaterial: 'drywall',
      source: { x: .5, y: .5, z: 2, ...src }, receivers: [{ x: .5, y: .85, z: 2 }, { x: .5, y: .15, z: 2 }] })); // outside the injection cluster; front = +width
    return { status: r.speaker.status, bands: r.speaker.directivityCoveredBands, db: 20 * Math.log10(peak(r.receiverTraces[0]) / peak(r.receiverTraces[1])) };
  };
  const directional = { isDirectional: true, directivityData: sphere2() };

  check('end to end: with no directivity data the room is front/rear symmetric (the baseline for every comparison)', () => { assert.ok(Math.abs(run({}).db) < 0.1); });

  check('end to end: imported data is accepted, reported as covering the simulated bands, and labelled as a representative (not verified) model', () => {
    const r = run({ ...directional, yawDeg: 0 }); assert.equal(r.status, 'MODELED_REPRESENTATIVE'); assert.equal(r.bands, 2);
  });

  check('end to end: orientation reaches the solver - aiming the source 180 degrees mirrors the front/rear difference (sign flips, size similar)', () => {
    const a = run({ ...directional, yawDeg: 0 }), b = run({ ...directional, yawDeg: 180 });
    assert.ok(Math.abs(a.db) > 0.05 && Math.abs(b.db) > 0.05, `aim must change the result (${a.db.toFixed(2)} dB, ${b.db.toFixed(2)} dB)`);
    assert.ok(Math.sign(a.db) === -Math.sign(b.db), 'turning the source around flips the sign'); assert.ok(Math.abs(a.db + b.db) < 0.6 * Math.max(Math.abs(a.db), Math.abs(b.db)) + 0.3, 'and the magnitudes are comparable');
  });

  console.log(`\n=== ${passed} passed (including end-to-end) ===`);
}
