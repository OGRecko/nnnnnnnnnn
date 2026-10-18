import assert from 'node:assert/strict';
import { validateProjectData } from './projectValidation';
import { sourceSensitivityDb } from './sourceSensitivity';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== project load keeps project-level source fields (regression: data loss on reopen) ===\n');

const full = { id: 's1', x: .5, y: .5, z: 1.5, brand: 'JBL', model: '4311 Studio Monitor', speakerId: 'jbl-4311', type: 'Studio Monitor', sens: 91, manufacturerSensitivityDb: 91,
  sensitivityStatus: 'MANUFACTURER_VERIFIED', manufacturerSensitivityReference: '2.83V/1m', speakerImpedanceOhm: 6, soundType: 'noise_pink', customFileName: 'a.wav', gainDb: -2, delayMs: 3, muted: true, yawDeg: 30 };
const proj = (sources: any[]) => ({ schemaVersion: 3, projectName: 'P', roomName: 'R', L: 10, W: 8, H: 3, fmax: 500, accuracyMode: 'balanced',
  poly: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], wallMaterial: 'drywall', wallSegMats: [null, null, null, null], wallOpenings: [null, null, null, null],
  floorMaterial: 'wood_floor', ceilMaterial: 'stonewool', scatter: { walls: .15, floor: .15, ceiling: .15 }, sources, receivers: [{ id: 'r1', name: 'R', x: .5, y: .5, z: 1.5 }], simulations: [], uxMode: 'beginner', primaryReceiverId: 'r1', receiverGrid: null });
const load = (s: any) => validateProjectData(proj([s]));
const out = (s: any) => { const r = load(s); assert.ok(r.ok, r.ok ? '' : r.error); return (r as any).data.sources[0]; };

check('every project-level source field survives a load (speaker, sound, sensitivity, reference, impedance, status, type, file label)', () => {
  const o = out(full);
  for (const k of ['speakerId', 'type', 'sens', 'manufacturerSensitivityDb', 'sensitivityStatus', 'manufacturerSensitivityReference', 'speakerImpedanceOhm', 'soundType', 'customFileName', 'gainDb', 'delayMs', 'muted', 'yawDeg', 'brand', 'model'])
    assert.deepEqual(o[k], (full as any)[k], `${k} was lost or changed on load`);
});

check('speaker loudness survives reopening: the 2.83 V/1 m reference is still normalised with the saved impedance (was silently lost)', () => {
  const o = out(full);
  const expected = 91 - 10 * Math.log10((2.83 * 2.83) / 6);
  assert.ok(Math.abs(sourceSensitivityDb(o)! - expected) < 1e-9, `got ${sourceSensitivityDb(o)}`);
  assert.equal(sourceSensitivityDb(out({ ...full, speakerImpedanceOhm: undefined })), null, 'without impedance a 2.83 V value must still be flagged, not assumed');
});

check('null is preserved for unknown sensitivity/impedance/reference (so "unavailable" stays unavailable)', () => {
  const o = out({ ...full, sens: null, manufacturerSensitivityDb: null, speakerImpedanceOhm: null, manufacturerSensitivityReference: null });
  for (const k of ['sens', 'manufacturerSensitivityDb', 'speakerImpedanceOhm', 'manufacturerSensitivityReference']) assert.equal(o[k], null, k);
  assert.equal(sourceSensitivityDb(o), null);
});

check('absent fields stay absent (nothing is invented for a source that never had them)', () => {
  const o = out({ id: 's1', x: .5, y: .5, z: 1.5 });
  for (const k of ['speakerId', 'soundType', 'sens', 'manufacturerSensitivityDb', 'speakerImpedanceOhm', 'sensitivityStatus', 'type', 'customFileName']) assert.equal(k in o, false, k);
});

check('hostile or malformed values are REJECTED, never copied through', () => {
  const bad: Array<[string, any]> = [
    ['soundType', 'a b'], ['soundType', '<script>'], ['soundType', 'x'.repeat(41)], ['soundType', 5],
    ['sensitivityStatus', 'lower_case'], ['sensitivityStatus', 'X'.repeat(41)], ['sensitivityStatus', {}],
    ['sens', 'loud'], ['sens', 1e9], ['sens', 5], ['sens', NaN], ['manufacturerSensitivityDb', -90], ['manufacturerSensitivityDb', {}],
    ['speakerImpedanceOhm', 0], ['speakerImpedanceOhm', -8], ['speakerImpedanceOhm', 65], ['speakerImpedanceOhm', '8'], ['speakerImpedanceOhm', Infinity],
    ['type', 'a\u0000b'], ['type', 'x'.repeat(101)], ['type', 7], ['customFileName', 'a\nb'], ['customFileName', 'x'.repeat(101)],
    ['manufacturerSensitivityReference', 'x'.repeat(101)], ['manufacturerSensitivityReference', 5], ['speakerId', 'a\u0000b'], ['speakerId', 'x'.repeat(101)],
  ];
  for (const [k, v] of bad) { const r = load({ ...full, [k]: v }); assert.equal(r.ok, false, `${k}=${JSON.stringify(v)?.slice(0, 30)} was accepted`); }
});

check('unknown extra source fields are still dropped (only the explicit allow-list survives)', () => {
  const o = out({ ...full, evil: 'x', __proto__: { polluted: 1 }, constructor: 'c', isAdmin: true });
  assert.equal('evil' in o, false); assert.equal('isAdmin' in o, false); assert.equal(({} as any).polluted, undefined); assert.equal(Object.getPrototypeOf(o), Object.prototype);
});

check('a full save -> load -> save -> load cycle is stable (idempotent)', () => {
  const a = validateProjectData(proj([full])) as any; assert.ok(a.ok);
  const b = validateProjectData(JSON.parse(JSON.stringify(a.data))) as any; assert.ok(b.ok);
  assert.deepEqual(b.data.sources, a.data.sources); assert.deepEqual(b.data.speakerReplacements, a.data.speakerReplacements);
});

check('multiple sources keep their OWN fields (no cross-contamination by index)', () => {
  const r = validateProjectData(proj([{ ...full, id: 'a', soundType: 'bass', speakerImpedanceOhm: 4 }, { id: 'b', x: .2, y: .2, z: 1.5 }, { ...full, id: 'c', soundType: 'piano', speakerImpedanceOhm: 8 }])) as any;
  assert.ok(r.ok); const s = r.data.sources;
  assert.deepEqual([s[0].soundType, s[1].soundType, s[2].soundType], ['bass', undefined, 'piano']); assert.deepEqual([s[0].speakerImpedanceOhm, s[1].speakerImpedanceOhm, s[2].speakerImpedanceOhm], [4, undefined, 8]);
});

console.log(`\n=== ${passed} passed ===`);
