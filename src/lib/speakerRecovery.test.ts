import assert from 'node:assert/strict';
import archived from '../data/archivedSpeakers.json';
import live from '../data/speakers.json';
import { validateProjectData } from './projectValidation';
import { MAX_SPEAKER_REPLACEMENT_RECORDS, applySpeakerReplacements, archivedSpeakerCount, classifySpeakerId, findUnresolvedSpeakerRefs, getLiveSpeaker, isLiveSpeakerId, sanitizeSpeakerReplacements, searchLiveSpeakers, sourceFieldsFromSpeaker } from './speakerRecovery';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== speaker recovery (archived vs unknown, explicit replacement) ===\n');

const LIVE_IDS = new Set((live as Array<{ id: string }>).map((s) => s.id));
const entries = (archived as { entries: Record<string, any> }).entries;
const ARCH = Object.keys(entries);
const A1 = 'legacy-jbl-5'; // archived, with a redirect suggestion (jbl-4311)
const A2 = ARCH.find((id) => !entries[id].redirectTo)!; // archived, no suggestion
const LIVE1 = 'jbl-4311', LIVE2 = (live as any[]).find((s) => s.id !== LIVE1 && s.sensitivity?.value != null)!.id as string;

const project = (sources: any[]) => ({
  schemaVersion: 3, appVersion: '1.0.0', projectName: 'P', roomName: 'R', L: 10, W: 8, H: 3, fmax: 500, accuracyMode: 'balanced', confirmReducedResolution: false,
  poly: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], wallMaterial: 'drywall', wallSegMats: [null, null, null, null], wallOpenings: [null, null, null, null],
  floorMaterial: 'wood_floor', ceilMaterial: 'stonewool', scatter: { walls: 0.15, floor: 0.15, ceiling: 0.15 },
  sources, receivers: [{ id: 'r1', name: 'R1', x: .5, y: .5, z: 1.5 }], simulations: [], uxMode: 'beginner', primaryReceiverId: 'r1', receiverGrid: null,
});
const src = (id: string, o: any = {}) => ({ id, x: .3, y: .5, z: 1.5, gainDb: 0, delayMs: 0, ...o });

check('the generated archive index matches the owner archives: 120 IDs, none live, redirect targets are live', () => {
  assert.equal(archivedSpeakerCount(), 120); assert.equal((archived as any).count, 120);
  for (const id of ARCH) { assert.ok(!LIVE_IDS.has(id), `${id} is archived AND live`); const t = entries[id].redirectTo; if (t) assert.ok(LIVE_IDS.has(t), `${id} -> ${t} is not live`); }
});

check('archived IDs are told apart from unknown IDs, and inherited property names are never "archived"', () => {
  assert.equal(classifySpeakerId(A1), 'archived'); assert.equal(classifySpeakerId('never-existed'), 'unknown');
  for (const k of ['__proto__', 'constructor', 'toString', 'hasOwnProperty', '']) assert.equal(classifySpeakerId(k), 'unknown', k);
});

check('findUnresolvedSpeakerRefs: live, empty, null and absent IDs are not references; archived/unknown are, with reason and position', () => {
  const refs = findUnresolvedSpeakerRefs(project([src('a', { speakerId: LIVE1 }), src('b', { speakerId: '' }), src('c', { speakerId: null }), src('d'), src('e', { speakerId: A1, brand: 'JBL', model: 'old' }), src('f', { speakerId: 'typo-speaker' })]));
  assert.deepEqual(refs.map((r) => [r.sourceId, r.sourceNumber, r.status]), [['e', 5, 'archived'], ['f', 6, 'unknown']]);
  assert.match(refs[0].archived!.reason, /Duplicate of jbl-4311/); assert.equal(refs[0].savedBrand, 'JBL');
  assert.equal(refs[0].suggestedReplacementId, 'jbl-4311'); assert.equal(refs[1].suggestedReplacementId, undefined); assert.equal(refs[1].archived, undefined);
});

check('findUnresolvedSpeakerRefs is safe on garbage: non-objects, non-arrays, non-string IDs, control characters, huge strings', () => {
  for (const bad of [null, undefined, 5, 'x', [], {}, { sources: 'no' }, { sources: [null, 1, 'x', []] }]) assert.deepEqual(findUnresolvedSpeakerRefs(bad), []);
  const refs = findUnresolvedSpeakerRefs({ sources: [{ id: 'a', speakerId: 42 }, { id: 'b', speakerId: { x: 1 } }, { id: 'c', speakerId: 'a\u0000b\nc'.repeat(100) }, { id: 'd', speakerId: '__proto__' }] });
  assert.equal(refs.length, 4); assert.ok(refs.every((r) => r.status === 'unknown')); assert.ok(refs[2].speakerId.length <= 100 && !/[\u0000-\u001f]/.test(refs[2].speakerId));
});

check('the validator reports ALL unresolved sources, structured, while keeping the readable message', () => {
  const r = validateProjectData(project([src('a', { speakerId: A1 }), src('b', { speakerId: 'nope' }), src('c', { speakerId: LIVE1 })]));
  assert.equal(r.ok, false); if (r.ok) return;
  assert.match(r.error, /not in the current catalog/); assert.match(r.error, /and 1 more source/); assert.match(r.error, /project was not opened/);
  assert.deepEqual(r.unresolvedSpeakers!.map((u) => u.sourceId), ['a', 'b']);
  assert.equal(validateProjectData(project([src('a', { speakerId: 'x' })])).ok, false);
});

check('other validation errors do NOT carry unresolvedSpeakers (the picker is offered only when speakers are the only blocker)', () => {
  const r = validateProjectData({ ...project([src('a', { speakerId: A1 })]), L: -5 }); assert.equal(r.ok, false); if (!r.ok) assert.equal(r.unresolvedSpeakers, undefined);
});

check('applySpeakerReplacements: an explicit choice per unresolved source produces a project that validates, with the history recorded', () => {
  const raw = project([src('a', { speakerId: A1, brand: 'JBL', model: 'old', gainDb: -3 }), src('b', { speakerId: A2 }), src('c', { speakerId: LIVE1 })]);
  const r = applySpeakerReplacements(raw, { a: LIVE1, b: LIVE2 }); assert.ok(r.ok); if (!r.ok) return;
  const v = validateProjectData(r.project); assert.ok(v.ok, v.ok ? '' : v.error); if (!v.ok) return;
  const byId = Object.fromEntries(v.data.sources.map((s: any) => [s.id, s]));
  assert.equal(byId.a.speakerId, LIVE1); assert.equal(byId.a.model, getLiveSpeaker(LIVE1)!.model); assert.equal(byId.a.gainDb, -3, 'user settings survive'); assert.equal(byId.b.speakerId, LIVE2); assert.equal(byId.c.speakerId, LIVE1);
  assert.equal(v.data.speakerReplacements.length, 2);
  assert.deepEqual(v.data.speakerReplacements[0], { sourceId: 'a', originalSpeakerId: A1, originalStatus: 'archived', originalBrand: 'JBL', originalModel: 'old', replacementSpeakerId: LIVE1, replacementBrand: getLiveSpeaker(LIVE1)!.brand, replacementModel: getLiveSpeaker(LIVE1)!.model });
});

check('the replacement fills the SAME speaker-derived fields as picking a speaker by hand (sensitivity, status, reference, impedance, type)', () => {
  const spec: any = getLiveSpeaker(LIVE2)!; const f = sourceFieldsFromSpeaker(spec);
  assert.equal(f.sens, spec.sensitivity.value); assert.equal(f.manufacturerSensitivityDb, spec.sensitivity.value); assert.equal(f.sensitivityStatus, spec.sensitivity.status ?? 'UNAVAILABLE');
  assert.equal(f.speakerImpedanceOhm, spec.impedance?.value ?? null); assert.notEqual(f.type, spec.category === 'hifi' ? 'hifi' : '', 'type is the display label, not the raw slug');
  const r = applySpeakerReplacements(project([src('a', { speakerId: A1, sens: 99, manufacturerSensitivityDb: 99 })]), { a: LIVE2 }) as any;
  assert.equal(r.project.sources[0].sens, f.sens); assert.notEqual(r.project.sources[0].sens, 99, 'the old speaker\'s sensitivity must not linger');
});

check('NEVER auto-remapped: an archive redirect is a suggestion only; applying with no choice fails and changes nothing', () => {
  const raw = project([src('a', { speakerId: A1 })]); const before = JSON.stringify(raw);
  for (const choices of [{}, { a: '' }, { a: undefined as any }] as Array<Record<string, string>>) { const r = applySpeakerReplacements(raw, choices); assert.equal(r.ok, false); }
  assert.equal(JSON.stringify(raw), before, 'the input is never mutated'); assert.equal(findUnresolvedSpeakerRefs(raw)[0].suggestedReplacementId, 'jbl-4311');
});

check('replacement must be LIVE: archived, unknown, inherited-name and non-string choices are refused', () => {
  const raw = project([src('a', { speakerId: A1 })]);
  for (const pick of [A2, 'nope', '__proto__', 'constructor', 123 as any, null as any, {} as any]) assert.equal(applySpeakerReplacements(raw, { a: pick }).ok, false, String(pick));
});

check('only unresolved sources can be replaced: a choice for a resolved or non-existent source is refused (no silent re-pointing)', () => {
  const raw = project([src('a', { speakerId: A1 }), src('c', { speakerId: LIVE1 })]);
  assert.equal(applySpeakerReplacements(raw, { a: LIVE1, c: LIVE2 }).ok, false, 'c is a live speaker and must not be changed');
  assert.equal(applySpeakerReplacements(raw, { a: LIVE1, ghost: LIVE2 }).ok, false);
  const ok = applySpeakerReplacements(raw, { a: LIVE1 }) as any; assert.equal(ok.project.sources[1].speakerId, LIVE1);
  const all = project([src('c', { speakerId: LIVE1 })]); assert.equal(applySpeakerReplacements(all, {}).ok, true, 'a project with nothing to repair is a no-op');
});

check('prototype-pollution style keys in choices are rejected, and Object.prototype stays clean', () => {
  const raw = project([src('a', { speakerId: A1 })]);
  const evil = JSON.parse('{"__proto__":{"polluted":true},"a":"' + LIVE1 + '"}');
  applySpeakerReplacements(raw, evil); assert.equal(({} as any).polluted, undefined);
  assert.equal(applySpeakerReplacements(raw, JSON.parse('{"constructor":"' + LIVE1 + '"}')).ok, false);
});

check('sources without a string ID or with duplicate IDs cannot be repaired unambiguously', () => {
  assert.equal(applySpeakerReplacements({ sources: [{ speakerId: A1 }] }, {}).ok, false);
  assert.equal(applySpeakerReplacements(project([src('a', { speakerId: A1 }), src('a', { speakerId: A2 })]), { a: LIVE1 }).ok, false);
  for (const bad of [null, 5, 'x', {}, { sources: 3 }]) assert.equal(applySpeakerReplacements(bad, {}).ok, false);
});

check('polar data supplied for the ORIGINAL speaker is dropped and reported, not silently applied to the replacement', () => {
  const r = applySpeakerReplacements(project([src('a', { speakerId: A1, isDirectional: true, directivityData: { frequencies: [1000], points: {} } }), src('b', { speakerId: A2 })]), { a: LIVE1, b: LIVE2 }) as any;
  assert.deepEqual(r.droppedDirectivitySourceIds, ['a']); assert.equal('directivityData' in r.project.sources[0], false); assert.equal('isDirectional' in r.project.sources[0], false);
});

check('history accumulates across repairs, is bounded, and survives validate -> save -> reload', () => {
  const first = applySpeakerReplacements(project([src('a', { speakerId: A1 })]), { a: LIVE1 }) as any;
  const v1 = validateProjectData(first.project) as any; assert.ok(v1.ok);
  const raw2 = { ...v1.data, sources: [...v1.data.sources, src('z', { speakerId: A2 })] };
  const second = applySpeakerReplacements(raw2, { z: LIVE2 }) as any; assert.equal(second.project.speakerReplacements.length, 2);
  const many = { ...project([src('a', { speakerId: A1 })]), speakerReplacements: Array.from({ length: MAX_SPEAKER_REPLACEMENT_RECORDS }, (_, i) => ({ sourceId: `s${i}`, originalSpeakerId: 'x', originalStatus: 'unknown', replacementSpeakerId: LIVE1, replacementBrand: 'b', replacementModel: 'm' })) };
  assert.equal((applySpeakerReplacements(many, { a: LIVE1 }) as any).project.speakerReplacements.length, MAX_SPEAKER_REPLACEMENT_RECORDS);
});

check('sanitizeSpeakerReplacements accepts good history and rejects malformed or oversized history (a bad field fails validation, never crashes)', () => {
  assert.deepEqual(sanitizeSpeakerReplacements(undefined), []); assert.deepEqual(sanitizeSpeakerReplacements(null), []);
  for (const bad of ['x', 5, {}, [null], [{}], [{ sourceId: 'a', originalSpeakerId: 'b', originalStatus: 'weird', replacementSpeakerId: 'c' }], Array(MAX_SPEAKER_REPLACEMENT_RECORDS + 1).fill({})]) assert.equal(sanitizeSpeakerReplacements(bad), undefined);
  const clean = sanitizeSpeakerReplacements([{ sourceId: 'a\u0000', originalSpeakerId: 'b', originalStatus: 'archived', replacementSpeakerId: 'c', replacementBrand: 'x'.repeat(500) }])!;
  assert.equal(clean[0].sourceId, 'a'); assert.equal(clean[0].replacementBrand.length, 100);
  assert.equal(validateProjectData({ ...project([src('a')]), speakerReplacements: 'junk' }).ok, false);
});

check('searchLiveSpeakers: finds live speakers only, ranks exact/prefix first, is bounded, and tolerates hostile queries', () => {
  const r = searchLiveSpeakers('jbl 4311'); assert.ok(r.some((x) => x.id === 'jbl-4311')); assert.ok(r.every((x) => LIVE_IDS.has(x.id)));
  assert.ok(!searchLiveSpeakers(A1.replace('legacy-', '')).some((x) => ARCH.includes(x.id)), 'archived IDs are never offered');
  assert.equal(searchLiveSpeakers('jbl-4311')[0].id, 'jbl-4311', 'an exact ID ranks first');
  assert.ok(searchLiveSpeakers('', 1000).length <= 100); assert.equal(searchLiveSpeakers('', 5).length, 5); assert.deepEqual(searchLiveSpeakers('zzzzqqqq'), []);
  for (const q of ['<script>', '.*', '(((', '\\', 'a'.repeat(100000), null as any, undefined as any, 5 as any]) assert.doesNotThrow(() => searchLiveSpeakers(q));
  assert.ok(searchLiveSpeakers('a b c d e f g h i j k l m n o p').length >= 0);
});

check('isLiveSpeakerId / getLiveSpeaker use own-key lookup', () => {
  assert.equal(isLiveSpeakerId(LIVE1), true); for (const k of [A1, '__proto__', 'constructor', 5, null]) assert.equal(isLiveSpeakerId(k), false);
  assert.equal(getLiveSpeaker('__proto__'), undefined); assert.equal(getLiveSpeaker('toString'), undefined);
});

console.log(`\n=== ${passed} passed ===`);
