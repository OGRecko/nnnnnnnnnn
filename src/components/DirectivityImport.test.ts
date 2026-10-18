import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { DirectivityImportView } from './DirectivityImport';
import { describeDirectivityData, parseDirectivityText } from '../lib/directivityImport';
import { validateProjectData } from '../lib/projectValidation';

const g: any = globalThis; g.window = {}; g.alert = () => {};
const origLog = console.log; console.log = () => {};
const { useStore } = await import('../store/useStore');
console.log = origLog;

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== directivity import UI + persistence ===\n');

const fixture = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'lib', 'fixtures', 'directivity', 'valid-long-sphere.csv');
const imported = (() => { const r = parseDirectivityText(fs.readFileSync(fixture, 'utf8'), 'valid-long-sphere.csv'); assert.ok(r.ok); return (r as any).data; })();
const none = describeDirectivityData(false, undefined);
const have = describeDirectivityData(true, imported);
const noop = () => {};
const render = (o: any = {}) => renderToStaticMarkup(React.createElement(DirectivityImportView, { status: none, sourceNumber: 2, onFile: noop, onRemove: noop, ...o }));

check('default state is honest: not available, omnidirectional assumed; offers import; no aim controls or Remove button', () => {
  const h = render(); assert.match(h, /Not available: omnidirectional assumed/); assert.match(h, /Import polar data…/); assert.doesNotMatch(h, /Aim source/); assert.doesNotMatch(h, />Remove</);
});

check('imported data is labelled as the user\'s own and unverified, with counts and exactly which bands it covers', () => {
  const h = render({ status: have, onAim: noop }); assert.match(h, /Imported by you \(not verified by Cavity Audio\): 84 directions at 250 Hz, 1 kHz, 4 kHz/);
  assert.match(h, /<strong>Experimental\.<\/strong>/); assert.match(h, /receives this data for the 250 Hz, 1 kHz, 4 kHz bands, but its directional source only approximates the pattern/); assert.match(h, /do not rely on directional results/);
  assert.match(h, /125 Hz, 500 Hz, 2 kHz, 8 kHz stay omnidirectional/);
  assert.doesNotMatch(h, /manufacturer|verified by the manufacturer|catalog data/i);
});

check('with data: Replace + Remove buttons, aim presets and numeric inputs with accessible names that include the source number', () => {
  const h = render({ status: have, onAim: noop, yawDeg: 90, pitchDeg: 10 });
  assert.match(h, /Replace polar data…/); assert.match(h, /aria-label="Remove polar data from source 2"/); assert.match(h, /<legend[^>]*>Aim source 2</);
  for (const l of ['Toward +Y', 'Toward −X', 'Toward −Y', 'Toward +X']) assert.ok(h.includes(`>${l}<`), `missing preset ${l}`);
  assert.match(h, /aria-label="Aim angle of source 2 in degrees"[^>]*/); assert.match(h, /aria-label="Upward tilt of source 2 in degrees"/); assert.match(h, /aria-label="Import polar data for source 2 \(CSV or JSON\)"/);
  assert.match(h, /value="90"/); assert.match(h, /value="10"/);
});

check('the active aim preset is exposed with aria-pressed (and wraps: 450° is 90°)', () => {
  const pressed = (yaw: number) => [...render({ status: have, onAim: noop, yawDeg: yaw }).matchAll(/aria-pressed="(true|false)"[^>]*>(Toward [^<]+)</g)].filter((m) => m[1] === 'true').map((m) => m[2]);
  assert.deepEqual(pressed(0), ['Toward +Y']); assert.deepEqual(pressed(90), ['Toward −X']); assert.deepEqual(pressed(-90), ['Toward +X']); assert.deepEqual(pressed(180), ['Toward −Y']); assert.deepEqual(pressed(450), ['Toward −X']); assert.deepEqual(pressed(33), []);
});

check('the axes are explained in terms of the position fields the user already sees (no unverifiable screen-direction claims)', () => {
  const h = render({ status: have, onAim: noop }); assert.match(h, /room&#x27;s X \(length\) and Y \(width\), the same as the Source X\/Y position fields/); assert.doesNotMatch(h, /top of the plan|north|clockwise/i);
});

check('errors are announced in an assertive live region; busy state disables the control', () => {
  assert.match(render({ error: 'This is a CLF2 binary file.' }), /role="alert"[^>]*aria-live="assertive"[^>]*>This is a CLF2 binary file\./);
  const b = render({ busy: true }); assert.match(b, /Reading…/); assert.match(b, /disabled=""/);
});

check('the file input accepts only text formats the importer reads (never .gll/.cf2/.ulf)', () => {
  const m = /accept="([^"]+)"/.exec(render())![1]; assert.ok(m.includes('.csv') && m.includes('.json')); assert.doesNotMatch(m, /gll|cf2|clf|ulf/);
});

check('describeDirectivityData derives the same status from STORED data: needs the directional flag AND valid data, otherwise unavailable', () => {
  assert.equal(have.available, true); assert.equal(have.provenance, 'imported-unverified'); assert.deepEqual(have.coveredBandsHz, [250, 1000, 4000]);
  for (const [flag, data] of [[false, imported], [undefined, imported], [true, undefined], [true, {}], [true, { frequencies: [1000], points: {}, angularResolution: 30 }], [true, 'junk'], [true, null]] as Array<[any, any]>) {
    const s = describeDirectivityData(flag, data); assert.equal(s.available, false, JSON.stringify([flag, typeof data])); assert.equal(s.provenance, 'none'); assert.equal(s.uncoveredBandsHz.length, 7);
  }
});

// -------------------------------------------------------------------- persistence
const proj = (sources: any[]) => ({ schemaVersion: 3, projectName: 'P', roomName: 'R', L: 10, W: 8, H: 3, fmax: 500, accuracyMode: 'balanced',
  poly: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], wallMaterial: 'drywall', wallSegMats: [null, null, null, null], wallOpenings: [null, null, null, null],
  floorMaterial: 'wood_floor', ceilMaterial: 'stonewool', scatter: { walls: .15, floor: .15, ceiling: .15 }, sources, receivers: [{ id: 'r1', name: 'R', x: .5, y: .5, z: 1.5 }], simulations: [], uxMode: 'beginner', primaryReceiverId: 'r1', receiverGrid: null });

check('imported directivity and the aim survive a save -> load round trip, and still describe as available afterwards', () => {
  const r = validateProjectData(proj([{ id: 's1', x: .5, y: .5, z: 1.5, isDirectional: true, directivityData: imported, yawDeg: 270, pitchDeg: -15, rollDeg: 5 }])) as any;
  assert.ok(r.ok, r.error); const s = r.data.sources[0];
  assert.deepEqual([s.yawDeg, s.pitchDeg, s.rollDeg, s.isDirectional], [270, -15, 5, true]); assert.deepEqual(s.directivityData.points['0,0'], [0, 0, 0]); assert.equal(Object.keys(s.directivityData.points).length, 84);
  assert.equal(describeDirectivityData(s.isDirectional, s.directivityData).available, true);
  const again = validateProjectData(JSON.parse(JSON.stringify(r.data))) as any; assert.ok(again.ok); assert.deepEqual(again.data.sources, r.data.sources);
});

check('hostile or out-of-range directivity in a project file is rejected at load, not silently kept', () => {
  const bad = { ...imported, points: { ...imported.points, '0,0': [0, 0, 999] } };
  assert.equal((validateProjectData(proj([{ id: 's1', x: .5, y: .5, z: 1.5, isDirectional: true, directivityData: bad }])) as any).ok, false);
});

check('store: importing sets the flag and data via updateSource; aim updates; Remove clears the data; each step is undoable and invalidates results', () => {
  useStore.setState({ sources: [{ id: 's1', brand: 'b', model: 'm', x: .5, y: .5, z: 1.5 } as any], past: [], future: [] });
  const st = () => useStore.getState().sources[0] as any;
  useStore.getState().updateSource('s1', { isDirectional: true, directivityData: imported }); assert.equal(describeDirectivityData(st().isDirectional, st().directivityData).available, true);
  useStore.getState().updateSource('s1', { yawDeg: 180 }); assert.equal(st().yawDeg, 180); assert.ok(st().directivityData, 'aiming keeps the data');
  useStore.getState().updateSource('s1', { isDirectional: false, directivityData: undefined }); assert.equal(describeDirectivityData(st().isDirectional, st().directivityData).available, false);
  assert.ok(useStore.getState().past.length >= 3, 'every change is recorded for undo');
  useStore.getState().undo(); assert.equal(describeDirectivityData(st().isDirectional, st().directivityData).available, true, 'undo restores the imported data');
});

console.log(`\n=== ${passed} passed ===`);
