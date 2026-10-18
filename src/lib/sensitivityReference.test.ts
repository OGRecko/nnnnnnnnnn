import assert from 'node:assert/strict';
import specs from '../data/speakers.json';
import { normalizeSensitivityTo1W1m, parseSensitivityReference } from './sensitivityReference';
import { resolveSensitivity, SENSITIVITY_REFERENCE_DB } from './speakerResponse';
import { sourceSensitivityDb } from './sourceSensitivity';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== sensitivity reference normalisation ===\n');
const near = (a: number | null, b: number, tol = 0.01) => assert.ok(a !== null && Math.abs(a - b) <= tol, `${a} vs ${b}`);

check('1 W / 1 m is used as published; blank is treated as 1 W / 1 m', () => {
  for (const ref of ['1W/1m', '1 W / 1 m', '1w/1M', '', '   ', null, undefined]) assert.equal(normalizeSensitivityTo1W1m(90, ref as any, undefined), 90, String(ref));
});

check('explicit 1 W / 1 m inside descriptive text (the Electro-Voice ZX wording) is recognised; look-alikes are not', () => {
  for (const ref of ['Axial, half-space measurement, 1 W/1 m (manual footnote 1)', 'Axial, half-space measurement, 1 W/1 m (datasheet footnote 1)']) assert.equal(normalizeSensitivityTo1W1m(97, ref, undefined), 97);
  for (const ref of ['2.83V/1m, 1 W/1 m equivalent', 'at 1 W/2 m', '10 W/1 m', 'about 1 W/1 mile', '1W/1m 2.83V/2m', 'noise at 1 W/1 m is 50 dB (see 2 W/1 m)']) assert.equal(normalizeSensitivityTo1W1m(97, ref, 8), null, ref);
});

check('2.83 V / 1 m needs a KNOWN impedance (never an assumed 8 ohm), and converts power exactly: 4 ohm +3.0 dB, 8 ohm 0 dB, 16 ohm -3.0 dB', () => {
  for (const ref of ['2.83V/1m', '2.83Vrms/1m', '2.83 V / 1 m']) {
    assert.equal(normalizeSensitivityTo1W1m(90, ref, undefined), null); assert.equal(normalizeSensitivityTo1W1m(90, ref, null), null);
    for (const bad of [0, -8, NaN, Infinity, '8', {}]) assert.equal(normalizeSensitivityTo1W1m(90, ref, bad), null, String(bad));
    near(normalizeSensitivityTo1W1m(90, ref, 8), 90 - 10 * Math.log10(2.83 * 2.83 / 8)); near(normalizeSensitivityTo1W1m(90, ref, 4), 87.0, 0.02); near(normalizeSensitivityTo1W1m(90, ref, 16), 93.0, 0.02);
  }
});

check('distance/power conversions and the bare unit W/m are deliberately NOT performed (they would rest on an unverified model)', () => {
  for (const ref of ['1W/10ft', '1W/2m', '1 W / 1 ft', 'EIA: 1mW/30ft, averaged 500–2500Hz', 'EIA: 1 mW/1 m', 'W/m']) assert.equal(normalizeSensitivityTo1W1m(86, ref, 8), null, ref);
});

check('references that cannot be normalised without guessing are rejected', () => {
  for (const ref of ['unspecified by source', '2.83V/m', '2.83V/1m (RMS not stated)', '2.83V; measurement distance not stated', '2.83Vrms on-axis; measurement distance not stated', 'New JIS SPL; drive and distance reference not stated', '218mVrms (-11dBu) input, 0dB gain, 1m',
    'at 1m; input reference unspecified', 'Measurement reference/distance not stated', '2.83V/2m', '1W/0ft', '1W/ft', 'EIA: 1mW/', '1W/1e3m', '1W/-5m', '1W/10 furlongs']) assert.equal(normalizeSensitivityTo1W1m(90, ref, 8), null, ref);
});

check('invalid raw values never normalise', () => { for (const v of [0, -1, NaN, Infinity, '90' as any, null as any, undefined as any]) assert.equal(normalizeSensitivityTo1W1m(v, '1W/1m', 8), null, String(v)); });

check('hostile reference strings cannot cause catastrophic backtracking or throw', () => {
  const t = Date.now();
  for (const ref of ['A'.repeat(100000), 'a b '.repeat(20000) + '1 W/1 m', '1W/' + '9'.repeat(50000) + 'ft', 'EIA: 1mW/' + '1'.repeat(50000), ' '.repeat(100000), '2.83' + 'V'.repeat(50000)]) assert.doesNotThrow(() => normalizeSensitivityTo1W1m(90, ref, 8));
  assert.ok(Date.now() - t < 1500, `${Date.now() - t} ms`);
  assert.equal(parseSensitivityReference('1W/' + '9'.repeat(400) + 'ft'), null, 'an infinite distance is rejected');
});

// ------------------------------------------------------------------ the catalog
const all = specs as any[];
const toSource = (s: any) => ({ manufacturerSensitivityDb: s.sensitivity?.value ?? null, sens: s.sensitivity?.value ?? null, manufacturerSensitivityReference: s.sensitivity?.reference ?? null, speakerImpedanceOhm: s.impedance?.value ?? null });

check('PROPERTY over every catalog record: the catalog resolver and the project-source resolver agree exactly (value, and fallback <=> null)', () => {
  let populated = 0, converted = 0, fallbacks = 0;
  for (const s of all) {
    const r = resolveSensitivity(s), src = sourceSensitivityDb(toSource(s));
    if (s.sensitivity?.value == null) { assert.equal(r.isFallback, true, s.id); assert.equal(src, null, s.id); continue; }
    populated++;
    if (r.isFallback) { fallbacks++; assert.equal(src, null, `${s.id}: resolver falls back but the source path returned ${src}`); assert.equal(r.valueDb, SENSITIVITY_REFERENCE_DB, s.id); }
    else { assert.ok(src !== null && Math.abs(src - r.valueDb) < 1e-9, `${s.id}: ${src} vs ${r.valueDb}`); if (Math.abs(r.valueDb - s.sensitivity.value) > 1e-9) converted++; }
    assert.ok(Number.isFinite(r.valueDb) && r.valueDb > 40 && r.valueDb < 140, `${s.id}: normalised ${r.valueDb} dB is implausible`);
  }
  assert.ok(populated > 250 && converted > 100 && fallbacks > 0, `populated ${populated}, converted ${converted}, fallbacks ${fallbacks}`);
});

check('the three Electro-Voice ZX records that STATE 1 W/1 m now use their real value; the three conversion-dependent records stay flagged fallbacks', () => {
  const by = (id: string) => resolveSensitivity(all.find((s) => s.id === id));
  for (const [id, v] of [['electro-voice-zx3-60', 97], ['electro-voice-zx3-90', 97], ['electro-voice-zx4', 100]] as const) { near(by(id).valueDb, v); assert.equal(by(id).isFallback, false, id); }
  for (const id of ['jbl-4310', 'jbl-4350', 'fostex-6301b']) { assert.equal(by(id).isFallback, true, id); assert.equal(by(id).valueDb, SENSITIVITY_REFERENCE_DB, id); }
});

check('references still NOT normalisable remain flagged fallbacks (nothing is guessed): count and examples', () => {
  const fb = all.filter((s) => s.sensitivity?.value != null && resolveSensitivity(s).isFallback);
  for (const s of fb) assert.ok(normalizeSensitivityTo1W1m(s.sensitivity.value, s.sensitivity.reference, s.impedance?.value) === null, s.id);
  assert.ok(fb.some((s) => s.id === 'legacy-pio-1'), 'a "distance not stated" record stays a fallback');
});

check('every distinct reference string in the catalog is classified deterministically (a new, unrecognised wording shows up here)', () => {
  const classified = new Map<string, string>();
  for (const s of all) { const ref = s.sensitivity?.reference; if (s.sensitivity?.value == null || typeof ref !== 'string' || ref.trim() === '') continue; const p = parseSensitivityReference(ref); classified.set(ref, p ? p.kind : 'UNRECOGNISED'); }
  const unrecognised = [...classified].filter(([, k]) => k === 'UNRECOGNISED').map(([r]) => r).sort();
  const EXPECTED_UNRECOGNISED = ['1W/10ft', 'EIA: 1mW/30ft, averaged 500–2500Hz', 'W/m', '2.83V/1m (RMS not stated)', '2.83V/1m at 500Hz', '2.83V/m', '2.83V; measurement distance not stated', '2.83Vrms on-axis; measurement distance not stated', '2.8 V; measurement distance not stated', '218mVrms (-11dBu) input, 0dB gain, 1m',
    'Measurement reference/distance not stated', 'New JIS SPL at 1 kHz; drive and distance not stated', 'New JIS SPL; drive and distance reference not stated', 'at 1m; input reference unspecified', 'unspecified by source'].sort();
  assert.deepEqual(unrecognised, EXPECTED_UNRECOGNISED, 'the set of references the app cannot normalise changed: review each new one for a safe, explicit conversion or leave it a flagged fallback');
});

console.log(`\n=== ${passed} passed ===`);
