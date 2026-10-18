import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DIRECTIVITY_IMPORT_LIMITS, importDirectivityFile, parseDirectivityBytes, parseDirectivityText } from './directivityImport';
import { DIRECTIVITY_LIMITS, validateDirectivity } from './publicLimits';
import { getInterpolatedMagnitude } from '../../server/directivityParser';

let passed = 0;
function check(name: string, fn: () => void | Promise<void>) { return Promise.resolve().then(fn).then(() => { passed++; console.log(`  PASS  ${name}`); }, (e: any) => { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; }); }
console.log('\n=== directivity import (CSV long/wide, JSON; hostile inputs) ===\n');

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'directivity');
const bytes = (n: string) => new Uint8Array(fs.readFileSync(path.join(dir, n)));
const load = (n: string) => parseDirectivityBytes(bytes(n), n);
const ok = (r: ReturnType<typeof load>) => { assert.ok(r.ok, r.ok ? '' : r.error); return r as Extract<typeof r, { ok: true }>; };
const err = (r: ReturnType<typeof load>, re: RegExp) => { assert.equal(r.ok, false, 'should have been rejected'); assert.match((r as { error: string }).error, re); };
const csv = (rows: string[], header = 'azimuth_deg,elevation_deg,frequency_hz,magnitude_db') => [header, ...rows].join('\n');
const ring = (f = 1000, step = 30, el = 0, abs = 90) => Array.from({ length: 360 / step }, (_, i) => `${i * step},${el},${f},${(abs - Math.min(i, 12 - i) * 0.5).toFixed(2)}`);

await check('long-format sphere fixture imports; absolute SPL is normalised to on-axis and the reference is reported', () => {
  const r = ok(load('valid-long-sphere.csv'));
  assert.equal(r.summary.format, 'csv-long'); assert.deepEqual(r.summary.frequenciesHz, [250, 1000, 4000]); assert.equal(r.summary.pointCount, 84);
  assert.deepEqual(r.summary.onAxisReferenceDb, [90, 90, 90]); assert.deepEqual(r.data.points['0,0'], [0, 0, 0]);
  assert.equal(r.data.brand, 'SYNTHETIC'); assert.equal(r.data.model, 'long-format fixture'); assert.equal(r.summary.angularResolutionDeg, 30);
  for (const v of Object.values(r.data.points)) for (const m of v) assert.ok(m <= 1e-9 && m >= -120);
  assert.ok(r.data.points['180,0'][2] < r.data.points['180,0'][0], 'rear is quieter at 4 kHz than at 250 Hz (more directional)');
});

await check('coverage is described honestly: a complete 30-degree sphere is "full-sphere"; bands within half an octave are covered, the rest omnidirectional', () => {
  const r = ok(load('valid-long-sphere.csv')); assert.equal(r.summary.coverage, 'full-sphere');
  assert.deepEqual(r.summary.coveredBandsHz, [250, 1000, 4000]); assert.deepEqual(r.summary.uncoveredBandsHz, [125, 500, 2000, 8000]);
  assert.deepEqual(ok(parseDirectivityText(csv(ring(1000)))).summary.coveredBandsHz, [1000]);
});

await check('wide format with semicolons, decimal commas and unit headers ("250 Hz", "1k", "4 kHz") imports; horizontal-only is labelled as such', () => {
  const r = ok(load('valid-wide-horizontal.csv')); assert.equal(r.summary.format, 'csv-wide'); assert.deepEqual(r.summary.frequenciesHz, [250, 1000, 4000]);
  assert.equal(r.summary.coverage, 'horizontal-plane-only'); assert.equal(r.summary.pointCount, 24); assert.equal(r.summary.angularResolutionDeg, 15);
});

await check('JSON in both shapes (point map and point array) imports through the same pipeline', () => {
  const m = ok(load('valid-map.json')), a = ok(load('valid-array.json'));
  assert.equal(m.summary.format, 'json'); assert.equal(m.data.model, 'json-map fixture'); assert.deepEqual(m.data.points['0,0'], [0, 0, 0]); assert.equal(a.summary.pointCount, 12);
});

await check('every accepted result passes the app\'s own validator (the single authority) and is usable by the solver\'s interpolation', () => {
  for (const f of ['valid-long-sphere.csv', 'valid-wide-horizontal.csv', 'valid-map.json', 'valid-array.json']) {
    const r = ok(load(f)); assert.ok(!('error' in validateDirectivity(r.data)), f);
    const d = { ...r.data, brand: 'x', model: 'y' } as any;
    for (const [freq, az, el] of [[1000, 0, 0], [1000, 45, 10], [3000, 200, -20], [100, -90, 0], [20000, 400, 0]]) assert.ok(Number.isFinite(getInterpolatedMagnitude(d, freq, az, el)), `${f} ${freq}/${az}/${el}`);
    assert.ok(Math.abs(getInterpolatedMagnitude(d, 1000, 0, 0)) < 1e-9, 'on-axis is 0 dB');
  }
});

await check('azimuth is wrapped: -30 equals 330, and a repeated 360 row that matches 0 is merged (not a conflict)', () => {
  const rows = ['0,0,1000,90', '90,0,1000,87', '180,0,1000,84', '-90,0,1000,87', '360,0,1000,90'];
  const r = ok(parseDirectivityText(csv(rows))); assert.deepEqual(Object.keys(r.data.points).sort(), ['0,0', '180,0', '270,0', '90,0']);
});

await check('BOM, CRLF, CR-only line endings, blank lines, tabs and "#" comments are tolerated', () => {
  const body = csv(ring()); for (const t of ['\uFEFF' + body, body.replace(/\n/g, '\r\n'), body.replace(/\n/g, '\r'), '\n\n# note\n' + body + '\n\n', csv(ring().map((l) => l.replace(/,/g, '\t')), 'azimuth_deg\televation_deg\tfrequency_hz\tmagnitude_db')]) assert.ok(parseDirectivityText(t).ok);
});

await check('header aliases work (az/el/freq/spl) and column order does not matter', () => {
  assert.ok(parseDirectivityText(csv(ring().map((l) => { const [a, e, f, m] = l.split(','); return `${m},${f},${e},${a}`; }), 'SPL,Freq,El,Az')).ok);
});

// ------------------------------------------------------------------ refusal of unsupported / binary formats
await check('CLF2, GLL, ULF and friends are REFUSED by name or signature with an actionable message, never guessed at', () => {
  for (const ext of ['.gll', '.cf2', '.cf1', '.clf', '.ulf', '.sofa', '.xhn']) err(parseDirectivityBytes(new TextEncoder().encode(csv(ring())), `speaker${ext}`), /cannot be read|not supported/);
  err(parseDirectivityBytes(new Uint8Array([0x41, 0xbd, 0x0a, 0x00, 0x01, 0, 0, 0, 0]), 'renamed.csv'), /CLF2 binary/);
  err(parseDirectivityBytes(new Uint8Array([0x50, 0x4b, 0x03, 0x04, 1, 2, 3]), 'x.csv'), /compressed archive/);
  err(parseDirectivityBytes(new Uint8Array([65, 66, 0, 67]), 'x.csv'), /binary file/);
  err(parseDirectivityBytes(new Uint8Array([0xff, 0xfe, 0xfd, 0x80]), 'x.csv'), /UTF-8/);
  err(parseDirectivityBytes(new Uint8Array(0), 'x.csv'), /empty/);
  assert.match((parseDirectivityBytes(new Uint8Array(1), 'a.gll') as { error: string }).error, /Export the polar data as CSV/);
});

await check('size limits: files over the cap are refused before reading (browser entry point), and over-long or over-many lines are refused', async () => {
  let read = 0; const big = { name: 'a.csv', size: DIRECTIVITY_IMPORT_LIMITS.MAX_FILE_BYTES + 1, arrayBuffer: async () => { read++; return new ArrayBuffer(1); } };
  const r = await importDirectivityFile(big); assert.equal(r.ok, false); assert.equal(read, 0, 'a too-large file must never be read into memory');
  assert.equal((await importDirectivityFile({ name: 'a.gll', size: 10, arrayBuffer: async () => { read++; return new ArrayBuffer(1); } })).ok, false); assert.equal(read, 0);
  assert.equal((await importDirectivityFile({ name: 'a.csv', size: 5, arrayBuffer: async () => { throw new Error('disk'); } })).ok, false);
  err(parseDirectivityText('azimuth_deg,elevation_deg,frequency_hz,magnitude_db\n' + '1'.repeat(DIRECTIVITY_IMPORT_LIMITS.MAX_LINE_CHARS + 5)), /longer than/);
  err(parseDirectivityText('a,b,c\n'.repeat(DIRECTIVITY_IMPORT_LIMITS.MAX_LINES + 5)), /more than .* lines/);
});

// ------------------------------------------------------------------ hostile / malformed content
await check('ambiguous theta/phi headers are refused (conventions differ between tools; guessing would rotate the pattern wrongly)', () => err(load('hostile-theta-phi.csv'), /ambiguous/));

await check('unknown, duplicate and missing columns are explained', () => {
  err(load('hostile-unknown-column.csv'), /"notes" is not recognised/);
  err(parseDirectivityText('azimuth_deg,azimuth,elevation_deg,frequency_hz,magnitude_db\n0,0,0,1000,0'), /duplicates the azimuth/);
  err(parseDirectivityText('elevation_deg,frequency_hz,magnitude_db\n0,1000,0'), /azimuth and elevation/);
  err(parseDirectivityText('azimuth_deg,elevation_deg,frequency_hz\n0,0,1000'), /both a frequency and a magnitude/);
  err(parseDirectivityText('azimuth_deg,elevation_deg,125,125 Hz\n0,0,1,1'), /same frequency/);
  err(parseDirectivityText('azimuth_deg,elevation_deg\n0,0'), /at least 3 columns/);
  err(parseDirectivityText('only one line'), /header row and at least one data row/);
});

await check('bad cells name the line and column: NaN, Infinity, hex, empty, overflow, formulas, units', () => {
  err(load('hostile-nan-cell.csv'), /Line 3, column 4: magnitude "NaN" is not a number/);
  for (const cell of ['Infinity', '-Infinity', '0x10', '', '1_000', '1e999', '=SUM(A1)', '90dB', '--5', '1.2.3', '١٢٣']) err(parseDirectivityText(csv(['0,0,1000,' + cell, ...ring().slice(1)])), /Line 2, column 4/);
  err(load('hostile-formula-injection.csv'), /Line 2, column 4/);
});

await check('structural problems: wrong column count, out-of-range angles and frequencies', () => {
  err(parseDirectivityText(csv(['0,0,1000', ...ring().slice(1)])), /Line 2 has 3 columns; the header has 4/);
  err(parseDirectivityText(csv(['0,91,1000,0', ...ring().slice(1)])), /elevation 91/); err(parseDirectivityText(csv(['0,-100,1000,0'])), /elevation -100/);
  for (const f of ['0', '-5', '30000', '1e9']) err(parseDirectivityText(csv([`0,0,${f},0`, ...ring().slice(1)])), /Line 2: frequency/);
});

await check('more than 16 frequencies and incomplete matrices are refused with guidance', () => {
  const rows: string[] = []; for (let f = 1; f <= 17; f++) rows.push(`0,0,${f * 100},0`);
  err(parseDirectivityText(csv(rows)), /more than 16 distinct frequencies/);
  err(parseDirectivityText(csv([...ring(250), ...ring(1000).slice(1)])), /has no value at 1000 Hz/);
  err(parseDirectivityText('azimuth_deg,elevation_deg,' + Array.from({ length: 17 }, (_, i) => (i + 1) * 100).join(',') + '\n0,0,' + '0,'.repeat(16) + '0'), /17 frequency columns/);
});

await check('ambiguous data is refused: conflicting duplicates, no on-axis sample, too few directions', () => {
  err(parseDirectivityText(csv(['0,0,1000,90', '0,0,1000,80', '90,0,1000,85', '180,0,1000,80'])), /conflicting duplicate/);
  err(load('hostile-no-onaxis.csv'), /no on-axis sample/);
  err(parseDirectivityText(csv(['0,0,1000,90', '90,0,1000,85'])), /fewer than 3 distinct directions/);
  ok(parseDirectivityText(csv(['0,0,1000,90', '0,0,1000,90.05', '90,0,1000,85', '180,0,1000,80'])));
});

await check('more directions than the shared limit are refused with resampling guidance (the 2.5-degree sphere would be 10,512)', () => {
  const rows: string[] = []; for (let el = -90; el <= 90; el += 2.5) for (let az = 0; az < 360; az += 2.5) rows.push(`${az},${el},1000,${(90 - Math.abs(az - 180) / 90).toFixed(2)}`);
  assert.ok(rows.length > DIRECTIVITY_LIMITS.MAX_POINTS); err(parseDirectivityText(csv(rows)), /limit is 4,096.*5° steps/s);
});

await check('a pattern more than 120 dB below on-axis is refused (it would silence the source), with the reason', () => {
  err(parseDirectivityText(csv(['0,0,1000,90', '90,0,1000,-60', '180,0,1000,80'])), /between -120 and 30/);
});

await check('JSON: invalid / wrong shape / bad keys / mismatched magnitudes / duplicate frequencies are all rejected cleanly', () => {
  for (const [t, re] of [['{"a":', /not valid JSON/], ['[1,2]', /object with/], ['null', /object with/], ['{"frequencies":[],"points":{}}', /frequencies/], ['{"frequencies":[1000]}', /"points" must be/],
    ['{"frequencies":[1000,1000],"points":{"0,0":[0,0]}}', /duplicate/], ['{"frequencies":[1000],"points":{"x":[0]}}', /must look like/], ['{"frequencies":[1000],"points":{"0,0":[0,1]}}', /one per frequency/],
    ['{"frequencies":[1000],"points":[null]}', /not an object/], ['{"frequencies":[1000],"points":[{"azimuth":"0","elevation":0,"magnitude":[0]}]}', /non-numeric/], ['{"frequencies":["1000"],"points":{}}', /frequencies/],
    ['{"frequencies":[1000],"points":{"0,0":[0],"30,95":[0]}}', /Elevation 95/]] as Array<[string, RegExp]>) err(parseDirectivityText(t, 'x.json'), re);
  err(load('hostile-script.json'), /must look like/);
});

await check('prototype pollution via JSON keys is refused or ignored, and Object.prototype stays clean', () => {
  const r = load('hostile-proto.json'); assert.equal(r.ok, false); assert.equal(({} as any).polluted, undefined);
  const ok2 = parseDirectivityText('{"__proto__":{"polluted":true},"frequencies":[1000],"points":{"0,0":[0],"90,0":[-1],"180,0":[-2]}}'); assert.equal(({} as any).polluted, undefined); if (ok2.ok) assert.equal(Object.getPrototypeOf(ok2.data.points) === Object.prototype || Object.getPrototypeOf(ok2.data.points) === null, true);
});

await check('performance: a 100,000-line hostile file is rejected quickly, and a maximal valid file (4,096 directions x 16 bands) parses in well under a second', () => {
  let t = Date.now(); parseDirectivityText('azimuth_deg,elevation_deg,frequency_hz,magnitude_db\n' + '1,1,1000,x\n'.repeat(100_000)); assert.ok(Date.now() - t < 2000, `${Date.now() - t} ms`);
  const header = 'azimuth_deg,elevation_deg,' + Array.from({ length: 16 }, (_, i) => 125 * (i + 1)).join(','); const rows: string[] = []; let n = 0;
  for (let el = -90; el <= 90 && n < 4096; el += 3) for (let az = 0; az < 360 && n < 4096; az += 3) { rows.push(`${az},${el},` + Array.from({ length: 16 }, (_, i) => (90 - Math.abs(az - 180) / 90 - i * 0.1).toFixed(2)).join(',')); n++; }
  t = Date.now(); const r = parseDirectivityText([header, ...rows].join('\n')); assert.ok(Date.now() - t < 1000, `${Date.now() - t} ms`); assert.ok(r.ok, r.ok ? '' : r.error);
});

await check('hostile labels are sanitised and truncated; control characters never survive', () => {
  const r = ok(parseDirectivityText('# brand: ' + 'B'.repeat(500) + '\n# model: M\u0001od\n' + csv(ring()))); assert.equal(r.data.brand!.length, 100); assert.equal(r.data.model, 'Mod');
  assert.equal(ok(parseDirectivityText('{"brand":{"x":1},"model":"\\u0000x","frequencies":[1000],"points":{"0,0":[0],"90,0":[-1],"180,0":[-2]}}')).data.brand, undefined);
});

await check('the file name in the summary is truncated and the data never claims to be verified', () => {
  const r = ok(parseDirectivityText(csv(ring()), 'f'.repeat(300) + '.csv')); assert.equal(r.summary.fileName.length, 100); assert.ok(!JSON.stringify(r).match(/verified/i));
});

console.log(`\n=== ${passed} passed ===`);
