import assert from 'node:assert/strict';
import { ReportNotReadyError, buildReportInput } from './reportInput';
import { receiverObjectId } from './storage';
import { MemoryArtifactStore } from './testing/memoryArtifactStore';
import type { JobRecord } from './jobStore';
import { setLogSinks } from './observability';
// Several checks deliberately trigger the report_trace_load_failed log path; keep the output readable.
setLogSinks(() => {}, () => {});

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) { try { await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== reportInput (ownership boundary) ===\n');

const SIM = '11111111-1111-4111-8111-111111111111';
const FOREIGN = '22222222-2222-4222-8222-222222222222';
const f32 = (...v: number[]) => Buffer.from(new Float32Array(v).buffer);
const rec = (o: Partial<JobRecord> & Record<string, unknown> = {}): JobRecord => ({
  simulationId: SIM, jobId: 'j', type: 'impulse-response', status: 'completed',
  room: { projectName: 'Proj', roomName: 'Hall', L: 8, W: 5, H: 3, wallMaterial: 'drywall' },
  speakers: [{ brand: 'JBL', model: 'LSR32', x: .2, y: .5 }], receivers: [{ name: 'R1', x: .8, y: .5 }],
  result: { rt60: 0.6, traceObjectIds: [receiverObjectId(SIM, 0)], receivers: [{ id: 'r0', metrics: { spl: 70 } }] },
  artifacts: [receiverObjectId(SIM, 0)], ...o,
} as any);
const store = async (entries: Record<string, Buffer> = { [receiverObjectId(SIM, 0)]: f32(0.25, 0.5, -1) }) => { const s = new MemoryArtifactStore(); for (const [k, v] of Object.entries(entries)) await s.put(k, v); return s; };
const notReady = async (r: JobRecord) => { try { await buildReportInput(r, await store()); assert.fail('should throw'); } catch (e) { assert.ok(e instanceof ReportNotReadyError, String(e)); } };

await check('only completed jobs with a stored result and room are reportable', async () => {
  for (const status of ['queued', 'running', 'failed', 'cancelled']) await notReady(rec({ status } as any));
  await notReady(rec({ result: null } as any)); await notReady(rec({ result: 'str' } as any)); await notReady(rec({ room: null } as any)); await notReady(rec({ room: 5 } as any));
});

await check('happy path: server-stored room/speakers/receivers are used, the trace is loaded from the artifact store and attached', async () => {
  const out = await buildReportInput(rec(), await store(), 12);
  assert.equal(out.projectName, 'Proj'); assert.equal(out.roomName, 'Hall'); assert.equal(out.simulationId, SIM); assert.equal(out.assumedSnrDb, 12);
  assert.deepEqual([out.room.L, out.room.W, out.room.H, out.room.wallMaterial], [8, 5, 3, 'drywall']);
  assert.deepEqual((out.solverResult.receivers as any)[0].receiverTrace, [0.25, 0.5, -1]);
  assert.deepEqual(out.solverResult.receiverTrace, [0.25, 0.5, -1]);
  assert.equal('traceObjectIds' in out.solverResult, false); assert.equal(out.solverResult.rt60, 0.6);
  assert.equal(out.speakers[0].brand, 'JBL'); assert.equal(out.receivers[0].name, 'R1');
});

await check('OWNERSHIP: an object ID that is not in the simulation\'s own artifact list is never loaded', async () => {
  const other = receiverObjectId(SIM, 1);
  const r = rec({ result: { traceObjectIds: [other], receivers: [{ id: 'r0' }] }, artifacts: [receiverObjectId(SIM, 0)] } as any);
  const out = await buildReportInput(r, await store({ [other]: f32(9, 9) }));
  assert.equal('receiverTrace' in (out.solverResult.receivers as any)[0], false); assert.equal('receiverTrace' in out.solverResult, false);
});

await check('OWNERSHIP: a tampered result pointing at ANOTHER simulation\'s artifact is ignored even if listed as owned', async () => {
  const foreign = receiverObjectId(FOREIGN, 0);
  const r = rec({ result: { traceObjectIds: [foreign], receivers: [{ id: 'r0' }] }, artifacts: [foreign] } as any);
  const out = await buildReportInput(r, await store({ [foreign]: f32(666) }));
  assert.equal('receiverTrace' in (out.solverResult.receivers as any)[0], false, 'foreign trace must not be followed');
  assert.ok(!JSON.stringify(out).includes('666'));
});

await check('hostile trace ids (traversal, wrong type, empty, huge, non-string) are skipped without throwing', async () => {
  const ids = ['../../etc/passwd', '', 5, null, {}, [], 'x'.repeat(5000), `${SIM}_receiver_0.bin/../x`, `${SIM}_receiver_-1.bin`, `${SIM}_receiver_0.BIN\u0000`];
  const r = rec({ result: { traceObjectIds: ids, receivers: ids.map(() => ({ id: 'r' })) }, artifacts: ids as any } as any);
  const out = await buildReportInput(r, await store());
  for (const x of out.solverResult.receivers as any[]) assert.equal('receiverTrace' in x, false);
});

await check('index alignment: a missing/failed trace for receiver 1 does not shift receiver 2\'s trace onto receiver 1', async () => {
  const a = receiverObjectId(SIM, 0), c = receiverObjectId(SIM, 2), missing = receiverObjectId(SIM, 1);
  const r = rec({ result: { traceObjectIds: [a, missing, c], receivers: [{ id: 'a' }, { id: 'b' }, { id: 'c' }] }, artifacts: [a, missing, c] } as any);
  const out = await buildReportInput(r, await store({ [a]: f32(1), [c]: f32(3) }));
  const rs = out.solverResult.receivers as any[];
  assert.deepEqual([rs[0].receiverTrace, rs[1].receiverTrace, rs[2].receiverTrace], [[1], undefined, [3]]);
  assert.deepEqual(rs.map((x) => x.id), ['a', 'b', 'c']);
});

await check('a storage failure degrades to "trace unavailable" (report still produced) instead of failing the whole report', async () => {
  const s = await store(); const real = s.get.bind(s); s.get = async () => { throw new Error('gcs down'); }; void real;
  const out = await buildReportInput(rec(), s);
  assert.equal('receiverTrace' in (out.solverResult.receivers as any)[0], false); assert.equal(out.solverResult.rt60, 0.6);
});

await check('a trace whose byte length is not a multiple of 4 is truncated safely, and an unaligned Buffer view decodes correctly', async () => {
  const id = receiverObjectId(SIM, 0);
  const odd = Buffer.concat([f32(1.5, 2.5), Buffer.from([1, 2, 3])]);
  assert.deepEqual(((await buildReportInput(rec(), await store({ [id]: odd }))).solverResult.receiverTrace), [1.5, 2.5]);
  // Force a non-4-aligned byteOffset on the buffer the store returns.
  const backing = Buffer.concat([Buffer.from([0]), f32(7, 8)]); const view = backing.subarray(1);
  assert.notEqual(view.byteOffset % 4, 0);
  const s = await store(); s.get = async () => view as any;
  assert.deepEqual((await buildReportInput(rec(), s)).solverResult.receiverTrace, [7, 8]);
});

await check('fewer stored receivers than traces, and non-object receiver entries, become {} without dropping alignment', async () => {
  const a = receiverObjectId(SIM, 0), b = receiverObjectId(SIM, 1);
  const r = rec({ result: { traceObjectIds: [a, b], receivers: ['junk', null, 7] }, artifacts: [a, b] } as any);
  const rs = (await buildReportInput(r, await store({ [a]: f32(1), [b]: f32(2) }))).solverResult.receivers as any[];
  assert.equal(rs.length, 3); assert.deepEqual(rs[0], { receiverTrace: [1] }); assert.deepEqual(rs[1], { receiverTrace: [2] }); assert.deepEqual(rs[2], {});
});

await check('missing/blank/non-string names and materials fall back to safe defaults; non-array room parts are dropped', async () => {
  const out = await buildReportInput(rec({ room: { projectName: '', roomName: 5, L: 1, W: 1, H: 1, poly: 'x', wallSegMats: {}, wallOpenings: 1 } } as any), await store());
  assert.equal(out.projectName, 'Cavity simulation'); assert.equal(out.roomName, 'Room');
  assert.deepEqual([out.room.wallMaterial, out.room.floorMaterial, out.room.ceilMaterial], ['smooth_concrete', 'concrete', 'concrete']);
  assert.deepEqual([out.room.poly, out.room.wallSegMats, out.room.wallOpenings], [undefined, undefined, undefined]);
});

await check('non-array speakers/receivers/artifacts/traceObjectIds are tolerated', async () => {
  const out = await buildReportInput(rec({ speakers: 'x', receivers: null, artifacts: 'y', result: { traceObjectIds: 'z', receivers: 'w' } } as any), await store());
  assert.deepEqual([out.speakers, out.receivers, out.solverResult.receivers], [[], [], []]);
});

await check('client-controlled data cannot enter: only the explicit assumedSnrDb parameter is passed through, and the record is not mutated', async () => {
  const r = rec(); const before = JSON.stringify(r);
  const out = await buildReportInput(r, await store(), undefined);
  assert.equal(out.assumedSnrDb, undefined); assert.equal(JSON.stringify(r), before);
});

console.log(`\n=== ${passed} passed ===`);
