/** Drives the REAL store actions (loadProject, resolveSpeakerRecovery, cancel, saveProject) through stubbed browser APIs. */
import assert from 'node:assert/strict';

const g: any = globalThis;
const alerts: string[] = [];
let pickedFile: { size: number; text: string } | null = null;
let savedBlob: Blob | null = null;
g.window = {}; g.alert = (m: string) => { alerts.push(String(m)); };
g.FileReader = class { onload: ((e: any) => void) | null = null; readAsText(f: { text: string }) { queueMicrotask(() => this.onload?.({ target: { result: f.text } })); } };
g.document = { createElement: (tag: string) => tag === 'input' ? { type: '', accept: '', onchange: null as any, click() { this.onchange?.({ target: { files: pickedFile ? [pickedFile] : [] } }); } } : { href: '', download: '', click() {} } };
g.URL.createObjectURL = (b: Blob) => { savedBlob = b; return 'blob:test'; }; g.URL.revokeObjectURL = () => {};
console.log = () => {};
const { useStore } = await import('./useStore');
console.log = (...a: any[]) => process.stdout.write(a.join(' ') + '\n');

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) { try { reset(); await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
const tick = () => new Promise((r) => setTimeout(r, 5));
function reset() { alerts.length = 0; pickedFile = null; savedBlob = null; useStore.setState({ pendingSpeakerRecovery: null, speakerReplacements: [] }); }
console.log('\n=== speaker recovery: store flow (real actions) ===\n');

const proj = (sources: any[]) => ({ schemaVersion: 3, appVersion: '1.0.0', projectName: 'Recovered', roomName: 'R', L: 10, W: 8, H: 3, fmax: 500, accuracyMode: 'balanced', confirmReducedResolution: false,
  poly: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], wallMaterial: 'drywall', wallSegMats: [null, null, null, null], wallOpenings: [null, null, null, null],
  floorMaterial: 'wood_floor', ceilMaterial: 'stonewool', scatter: { walls: .15, floor: .15, ceiling: .15 }, sources, receivers: [{ id: 'r1', name: 'R1', x: .5, y: .5, z: 1.5 }], simulations: [], uxMode: 'beginner', primaryReceiverId: 'r1', receiverGrid: null });
const open = async (p: unknown) => { pickedFile = { size: 100, text: typeof p === 'string' ? p : JSON.stringify(p) }; useStore.getState().loadProject(); await tick(); };
const s = (id: string, o: any = {}) => ({ id, x: .3, y: .5, z: 1.5, gainDb: 0, delayMs: 0, ...o });

await check('opening a project with an ARCHIVED speaker does not dead-end: no alert, the picker data is staged, the live project is untouched', async () => {
  const before = useStore.getState().projectName;
  await open(proj([s('a', { speakerId: 'legacy-jbl-5', brand: 'JBL', model: 'old' })]));
  const st = useStore.getState(); assert.equal(alerts.length, 0, 'no failure alert'); assert.equal(st.projectName, before, 'nothing was applied');
  assert.equal(st.pendingSpeakerRecovery!.unresolved[0].status, 'archived'); assert.equal(st.pendingSpeakerRecovery!.unresolved[0].suggestedReplacementId, 'jbl-4311');
});

await check('an unknown (typo) ID is staged as "unknown", and a MIX of archived + unknown + live sources lists only the unresolved ones', async () => {
  await open(proj([s('a', { speakerId: 'legacy-jbl-5' }), s('b', { speakerId: 'typo' }), s('c', { speakerId: 'jbl-4311' })]));
  assert.deepEqual(useStore.getState().pendingSpeakerRecovery!.unresolved.map((u) => [u.sourceId, u.status]), [['a', 'archived'], ['b', 'unknown']]);
});

await check('other load errors still show the normal failure alert and do NOT open the picker', async () => {
  await open({ ...proj([s('a', { speakerId: 'legacy-jbl-5' })]), L: -1 }); assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.match(alerts[0], /Failed to load project/);
  reset(); await open('{not json'); assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.match(alerts[0], /Failed to load project/);
});

await check('a source with no ID cannot be repaired individually, so the picker is NOT offered (clear error instead)', async () => {
  await open(proj([{ x: .3, y: .5, z: 1.5, speakerId: 'legacy-jbl-5' }])); assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.equal(alerts.length, 1);
});

await check('resolving applies the explicit choices, opens the project, clears the pending state and records the history', async () => {
  await open(proj([s('a', { speakerId: 'legacy-jbl-5', gainDb: -4, soundType: 'noise_pink' }), s('b', { speakerId: 'typo' })]));
  const r = useStore.getState().resolveSpeakerRecovery({ a: 'jbl-4311', b: 'jbl-l100' }); assert.ok(r.ok, r.ok ? '' : r.error); if (!r.ok) return;
  const st = useStore.getState(); assert.equal(st.pendingSpeakerRecovery, null); assert.equal(st.projectName, 'Recovered');
  assert.deepEqual(st.sources.map((x) => x.speakerId), ['jbl-4311', 'jbl-l100']); assert.equal(st.sources[0].gainDb, -4); assert.equal((st.sources[0] as any).soundType, 'noise_pink');
  assert.equal(st.speakerReplacements.length, 2); assert.deepEqual(st.speakerReplacements.map((x) => [x.originalSpeakerId, x.replacementSpeakerId]), [['legacy-jbl-5', 'jbl-4311'], ['typo', 'jbl-l100']]);
  assert.match(r.message, /2 replacement speakers/); assert.match(r.message, /original file was not changed/);
});

await check('incomplete, invalid or archived choices return an error and KEEP the pending state so the person can fix them', async () => {
  await open(proj([s('a', { speakerId: 'legacy-jbl-5' }), s('b', { speakerId: 'typo' })]));
  for (const choices of [{}, { a: 'jbl-4311' }, { a: 'jbl-4311', b: 'legacy-jbl-5' }, { a: 'jbl-4311', b: 'nope' }, { a: 'jbl-4311', b: 'jbl-l100', ghost: 'jbl-l100' }]) {
    const r = useStore.getState().resolveSpeakerRecovery(choices as any); assert.equal(r.ok, false, JSON.stringify(choices)); assert.ok(useStore.getState().pendingSpeakerRecovery, 'still pending');
  }
  assert.equal(useStore.getState().speakerReplacements.length, 0);
});

await check('cancel discards the staged project and changes nothing; resolving with nothing pending is an error, not a crash', async () => {
  const before = useStore.getState().projectName;
  await open(proj([s('a', { speakerId: 'legacy-jbl-5' })])); useStore.getState().cancelSpeakerRecovery();
  assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.equal(useStore.getState().projectName, before);
  assert.equal(useStore.getState().resolveSpeakerRecovery({ a: 'jbl-4311' }).ok, false);
});

await check('the replacement history is written by Save and survives a full reopen (and the reopened project is NOT offered recovery again)', async () => {
  await open(proj([s('a', { speakerId: 'legacy-jbl-5' })])); assert.ok(useStore.getState().resolveSpeakerRecovery({ a: 'jbl-4311' }).ok);
  useStore.getState().saveProject(); assert.ok(savedBlob, 'saveProject produced a file');
  const saved = JSON.parse(await savedBlob!.text()); assert.equal(saved.speakerReplacements.length, 1); assert.equal(saved.sources[0].speakerId, 'jbl-4311');
  reset(); alerts.length = 0; await open(saved);
  assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.match(alerts[0], /loaded successfully/); assert.equal(useStore.getState().speakerReplacements.length, 1, 'history is preserved on reopen');
  assert.equal(useStore.getState().sources[0].speakerId, 'jbl-4311');
});

await check('opening a normal project clears any stale replacement history, and newProject resets recovery state', async () => {
  useStore.setState({ speakerReplacements: [{ sourceId: 'x', originalSpeakerId: 'o', originalStatus: 'unknown', replacementSpeakerId: 'jbl-4311', replacementBrand: 'b', replacementModel: 'm' }], pendingSpeakerRecovery: { rawProject: {}, unresolved: [] } });
  await open(proj([s('a', { speakerId: 'jbl-4311' })])); assert.deepEqual(useStore.getState().speakerReplacements, []); assert.equal(useStore.getState().pendingSpeakerRecovery, null);
  useStore.setState({ pendingSpeakerRecovery: { rawProject: {}, unresolved: [] }, speakerReplacements: [{ sourceId: 'x' } as any] }); useStore.getState().newProject();
  assert.equal(useStore.getState().pendingSpeakerRecovery, null); assert.deepEqual(useStore.getState().speakerReplacements, []);
});

await check('a hostile project file cannot pollute prototypes or smuggle fields through the recovery path', async () => {
  const hostile = JSON.stringify(proj([s('a', { speakerId: 'legacy-jbl-5' })])).replace('"sources":', '"__proto__":{"polluted":true},"sources":');
  await open(hostile); assert.equal(({} as any).polluted, undefined);
  const r = useStore.getState().resolveSpeakerRecovery({ a: 'jbl-4311' }); assert.equal(({} as any).polluted, undefined); void r;
});

console.log(`\n=== ${passed} passed ===`);
