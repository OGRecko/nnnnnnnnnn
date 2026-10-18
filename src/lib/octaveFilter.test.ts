import assert from "node:assert/strict";
import { OCTAVE_BANDS_HZ, OCTAVE_BAND_LABELS, applyBiquad, bandpassBiquad, filterIntoBands } from "./octaveFilter";

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log("\n=== octaveFilter (direct) ===\n");

const FS = 48000;
const sine = (hz: number, n = 24000) => Array.from({ length: n }, (_, i) => Math.sin((2 * Math.PI * hz * i) / FS));
const rms = (x: number[], skip = 4000) => { let s = 0; for (let i = skip; i < x.length; i++) s += x[i] * x[i]; return Math.sqrt(s / (x.length - skip)); };

check("band table is 125 Hz-8 kHz in octaves with matching labels", () => {
  assert.deepEqual(OCTAVE_BANDS_HZ, [125, 250, 500, 1000, 2000, 4000, 8000]);
  assert.deepEqual(OCTAVE_BAND_LABELS, OCTAVE_BANDS_HZ.map((h) => `${h} Hz`));
});

check("bandpass biquad: DC-blocking numerator, stable poles, unity-ish gain at centre", () => {
  for (const c of OCTAVE_BANDS_HZ) {
    const f = bandpassBiquad(c, FS, Math.SQRT1_2);
    assert.equal(f.b1, 0); assert.ok(Math.abs(f.b0 + f.b2) < 1e-15);
    assert.ok(Math.abs(f.a2) < 1, `|a2|<1 for stability at ${c}`);
    assert.ok(Math.abs(f.a1) < 1 + f.a2, `triangle stability at ${c}`);
    const g = rms(applyBiquad(sine(c), f)) / rms(sine(c));
    assert.ok(g > 0.95 && g < 1.05, `centre gain ${g} at ${c} Hz`);
  }
});

check("band selectivity: a tone one decade away is attenuated by >12 dB", () => {
  const f = bandpassBiquad(1000, FS, Math.SQRT1_2);
  for (const hz of [100, 10000]) {
    const db = 20 * Math.log10(rms(applyBiquad(sine(hz), f)) / rms(sine(hz)));
    assert.ok(db < -12, `${hz} Hz leaked at ${db.toFixed(1)} dB`);
  }
});

check("filtering is linear and zero in = zero out; empty trace is empty", () => {
  const f = bandpassBiquad(500, FS, Math.SQRT1_2);
  assert.deepEqual(applyBiquad([], f), []);
  assert.ok(applyBiquad(new Array(100).fill(0), f).every((v) => v === 0));
  const a = sine(500, 2000), b = sine(700, 2000);
  const sum = applyBiquad(a.map((v, i) => v + b[i]), f);
  const sep = applyBiquad(a, f).map((v, i) => v + applyBiquad(b, f)[i]);
  sum.forEach((v, i) => assert.ok(Math.abs(v - sep[i]) < 1e-12));
});

check("filterIntoBands skips bands at/above Nyquist and never fabricates them", () => {
  const trace = sine(1000, 4000);
  assert.deepEqual(Object.keys(filterIntoBands(trace, 48000)).map(Number), OCTAVE_BANDS_HZ);
  assert.deepEqual(Object.keys(filterIntoBands(trace, 16000)).map(Number), [125, 250, 500, 1000, 2000, 4000]);
  assert.deepEqual(Object.keys(filterIntoBands(trace, 8000)).map(Number), [125, 250, 500, 1000, 2000]);
  assert.deepEqual(filterIntoBands(trace, 100), {});
});

check("filterIntoBands honours a custom band list and preserves trace length", () => {
  const r = filterIntoBands(sine(250, 1234), FS, [250, 500]);
  assert.deepEqual(Object.keys(r).map(Number), [250, 500]);
  assert.equal(r[250].length, 1234);
});

check("an impulse produces a finite, decaying band response (no blow-up)", () => {
  const imp = new Array(8000).fill(0); imp[0] = 1;
  for (const [, out] of Object.entries(filterIntoBands(imp, FS))) {
    assert.ok(out.every(Number.isFinite));
    assert.ok(rms(out.slice(4000), 0) < 1e-3, "tail must decay");
  }
});

console.log(`\n=== ${passed} passed ===`);
