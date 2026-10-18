/**
 * workerRunner: pure helpers + the real runner driven against REAL worker threads running tiny purpose-built scripts.
 * Nothing in worker_threads is mocked; each scenario is a worker that behaves exactly as described.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { buildPublicResult, classifyWorkerError, createWorkerRunner, defaultWorkerPath, extractTraces, toWorkerPayload } from './workerRunner';
import { SolverError } from './jobExecutor';
import { PUBLIC_ERROR_CODES, PUBLIC_ERROR_MESSAGES } from './jobStore';
import { LIMITS } from '../src/lib/publicLimits';

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) {
  try { await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; }
}
console.log('\n=== workerRunner ===\n');

// ---------------------------------------------------------------- pure helpers
await check('classifyWorkerError maps internal text to fixed public codes (text is never exposed)', () => {
  const E = PUBLIC_ERROR_CODES;
  for (const m of ['exceeds available system memory', 'memory budget exceeded', 'grid exceeds the limit', 'too many receivers', 'server safety limit']) assert.equal(classifyWorkerError(m), E.resource_limit, m);
  for (const m of ['invalid room', 'must be positive', 'source outside the room', 'unstable simulation', 'Courant number too high', 'non-finite value', 'steps is required']) assert.equal(classifyWorkerError(m), E.invalid_input, m);
  for (const m of ['boom', '', undefined, null, 42, {}, 'ENOENT /etc/passwd']) assert.equal(classifyWorkerError(m), E.solver_failed, String(m));
  // resource limits win over invalid-input words when both appear
  assert.equal(classifyWorkerError('invalid: grid exceeds the limit'), E.resource_limit);
});

await check('toWorkerPayload: wave takes the FIRST source as `source`; impulse-response is left alone; input is not mutated', () => {
  const payload = { sources: [{ x: 1 }, { x: 2 }], L: 4 };
  const w = toWorkerPayload('wave', payload, 'sim-1');
  assert.deepEqual(w.source, { x: 1 }); assert.equal(w.simulationId, 'sim-1'); assert.deepEqual(w.sources, payload.sources);
  const ir = toWorkerPayload('impulse-response', payload, 'sim-2');
  assert.equal('source' in ir, false); assert.equal(ir.simulationId, 'sim-2');
  assert.equal('simulationId' in payload, false);
  assert.equal('source' in toWorkerPayload('wave', { L: 1 }, 's'), false);
  assert.equal(toWorkerPayload('wave', { sources: [], L: 1 }, 's').source, undefined);
});

await check('toWorkerPayload: a client-supplied simulationId can never override the server-assigned one', () => {
  assert.equal(toWorkerPayload('wave', { simulationId: 'attacker', sources: [{}] }, 'real').simulationId, 'real');
});

await check('defaultWorkerPath: production/desktop use the bundled worker rooted at CAVITY_APP_ROOT; dev uses tsx on the TS source', () => {
  const save = { ...process.env };
  try {
    process.env.NODE_ENV = 'production'; delete process.env.CAVITY_DESKTOP; process.env.CAVITY_APP_ROOT = '/app';
    assert.equal(defaultWorkerPath().workerPath, path.join('/app', 'dist', 'solverWorker.cjs')); assert.equal(defaultWorkerPath().execArgv, undefined);
    process.env.NODE_ENV = 'development'; process.env.CAVITY_DESKTOP = '1';
    assert.equal(defaultWorkerPath().workerPath, path.join('/app', 'dist', 'solverWorker.cjs'));
    delete process.env.CAVITY_DESKTOP; process.env.NODE_ENV = 'test';
    const dev = defaultWorkerPath();
    assert.equal(dev.workerPath, path.join(process.cwd(), 'server', 'solverWorker.ts')); assert.deepEqual(dev.execArgv, ['--import', 'tsx']);
  } finally { for (const k of ['NODE_ENV', 'CAVITY_DESKTOP', 'CAVITY_APP_ROOT']) { if (save[k] === undefined) delete process.env[k]; else process.env[k] = save[k]; } }
});

await check('buildPublicResult strips bulky per-sample data and per-receiver traces, keeps metrics, summarises the wavefield', () => {
  const r = buildPublicResult('impulse-response', {
    rt60: 0.5, receiverTrace: [1, 2], receiverTraces: [[1]], wavefield: { outNx: 4, outNz: 3, dt: 0.001, frames: ['big'] } as any,
    receivers: [{ id: 'a', trace: [1, 2, 3], metrics: { spl: 70 } }, null, { id: 'b' }],
  } as any, 7);
  assert.equal(r.rt60, 0.5); assert.equal('receiverTrace' in r, false); assert.equal('receiverTraces' in r, false);
  assert.deepEqual(r.wavefield, { outNx: 4, outNz: 3, dt: 0.001, frameCount: 7 });
  assert.deepEqual(r.receivers, [{ id: 'a', metrics: { spl: 70 } }, {}, { id: 'b' }]);
  assert.deepEqual(buildPublicResult('wave', null, 0), { receivers: [] });
  assert.deepEqual(buildPublicResult('wave', { receivers: 'nope' } as any, 0), { receivers: [] });
});

await check('extractTraces: IR reads receivers[i].trace, wave reads receiverTraces; empty/missing become null; values become Float32', () => {
  const ir = extractTraces('impulse-response', { receivers: [{ trace: [0.5, 1] }, { trace: [] }, null, {}] } as any);
  assert.ok(ir[0] instanceof Float32Array && ir[0]!.length === 2 && ir[0]![0] === 0.5); assert.deepEqual(ir.slice(1), [null, null, null]);
  const w = extractTraces('wave', { receiverTraces: [new Float64Array([1, 2]), [], 'x'] } as any);
  assert.ok(w[0] instanceof Float32Array); assert.deepEqual(w.slice(1), [null, null]);
  assert.deepEqual(extractTraces('wave', null), []); assert.deepEqual(extractTraces('impulse-response', {} as any), []);
});

// ---------------------------------------------------------------- real worker threads
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'wr-'));
const script = (name: string, body: string) => { const p = path.join(dir, `${name}.cjs`); fs.writeFileSync(p, `const { parentPort, workerData } = require('node:worker_threads');\n${body}`); return p; };
const W = {
  ok: script('ok', `parentPort.postMessage({ success: true, data: { rt60: 0.42, echo: workerData.type, sid: workerData.payload.simulationId, receivers: [{ id: 'r0', trace: [0.25, 0.5], metrics: { spl: 70 } }] } });`),
  fail: script('fail', `parentPort.postMessage({ success: false, error: 'Courant number too high at /secret/path' });`),
  failMem: script('failmem', `parentPort.postMessage({ success: false, error: 'exceeds available system memory' });`),
  throws: script('throws', `throw new Error('kaboom internal detail');`),
  exitNoResult: script('exit', `process.exit(3);`),
  hang: script('hang', `setInterval(() => {}, 1000);`),
  junk: script('junk', `parentPort.postMessage(null); parentPort.postMessage('str'); parentPort.postMessage({ nothing: 1 }); parentPort.postMessage({ success: true, data: { receivers: [{ trace: [1] }] } });`),
  nullData: script('nulldata', `parentPort.postMessage({ success: true, data: null });`),
  frames: script('frames', `parentPort.postMessage({ type: 'expected_frames', count: 3 }); for (let i = 0; i < 3; i++) parentPort.postMessage({ type: 'wavefield_frame', frame: new Float32Array([i, i + 1]) });
    parentPort.postMessage({ success: true, data: { wavefield: { outNx: 2, outNz: 1, dt: 0.01 }, receiverTraces: [[1, 2]] } });`),
  badFrame: script('badframe', `parentPort.postMessage({ type: 'wavefield_frame', frame: [1, 2, 3] });`),
  tooManyExpected: script('tme', `parentPort.postMessage({ type: 'expected_frames', count: 99999 });`),
  expectedMismatch: script('mismatch', `parentPort.postMessage({ type: 'expected_frames', count: 5 }); parentPort.postMessage({ type: 'wavefield_frame', frame: new Float32Array(2) });
    parentPort.postMessage({ success: true, data: { wavefield: { outNx: 1, outNz: 1, dt: 1 } } });`),
};
const run = (worker: string, o: { type?: any; signal?: AbortSignal; timeoutMs?: number; put?: (i: number, f: Float32Array) => Promise<string> } = {}) =>
  createWorkerRunner({ workerPath: worker, execArgv: [], timeoutMs: o.timeoutMs ?? 5000 })({
    type: o.type ?? 'impulse-response', payload: { sources: [{ x: 1 }], L: 4 }, simulationId: 'sim-xyz', signal: o.signal ?? new AbortController().signal,
    putWaveFrame: o.put ?? (async (i) => `obj_${i}`),
  });
const code = async (p: Promise<unknown>) => { try { await p; return 'RESOLVED'; } catch (e: any) { assert.ok(e instanceof SolverError, `non-SolverError rejection: ${e?.stack ?? e}`); return e.code as string; } };

await check('a successful job resolves with the public result and Float32 traces; the worker received the server simulationId', async () => {
  const out = await run(W.ok);
  assert.equal((out.result as any).rt60, 0.42); assert.equal((out.result as any).echo, 'impulse-response'); assert.equal((out.result as any).sid, 'sim-xyz');
  assert.deepEqual((out.result as any).receivers, [{ id: 'r0', metrics: { spl: 70 } }]);
  assert.ok(out.traces[0] instanceof Float32Array && out.traces[0]![1] === 0.5); assert.deepEqual(out.waveObjectIds, []);
});

await check('worker-reported failures become fixed public codes and the internal text never reaches the caller', async () => {
  assert.equal(await code(run(W.fail)), 'invalid_input');
  assert.equal(await code(run(W.failMem)), 'resource_limit');
  // Contract: SolverError.message keeps the internal detail for SERVER logs only (which are redacted); everything a
  // client can see is derived from `code` alone.
  try { await run(W.fail); assert.fail('should reject'); } catch (e: any) {
    assert.ok(e instanceof SolverError && /Courant/.test(e.message), 'internal detail is kept for logs');
    assert.ok(!/secret|path|Courant/.test(PUBLIC_ERROR_MESSAGES[e.code as keyof typeof PUBLIC_ERROR_MESSAGES]), 'the public message must not echo internal text');
  }
  for (const m of Object.values(PUBLIC_ERROR_MESSAGES)) assert.ok(!/\/|\\|Error:|at .*:\d+/.test(m), `public message looks like internals: ${m}`);
});

await check('a worker that throws or exits without a result rejects solver_failed (no hang, no unhandled rejection)', async () => {
  let unhandled = 0; const h = () => { unhandled++; }; process.on('unhandledRejection', h);
  try { assert.equal(await code(run(W.throws)), 'solver_failed'); assert.equal(await code(run(W.exitNoResult)), 'solver_failed'); await new Promise((r) => setTimeout(r, 50)); assert.equal(unhandled, 0); } finally { process.off('unhandledRejection', h); }
});

await check('a missing worker file rejects solver_failed', async () => { assert.equal(await code(run(path.join(dir, 'nope.cjs'))), 'solver_failed'); });

await check('timeout: a hung worker is terminated and rejected as timeout', async () => {
  const t0 = Date.now(); assert.equal(await code(run(W.hang, { timeoutMs: 200 })), 'timeout'); assert.ok(Date.now() - t0 < 4000, 'must not wait for the worker');
});

await check('abort: cancel mid-run => cancelled; an abort whose reason is "timeout" => timeout; a pre-aborted signal never starts work', async () => {
  const c = new AbortController(); const p = run(W.hang, { signal: c.signal }); setTimeout(() => c.abort(), 100); assert.equal(await code(p), 'cancelled');
  const t = new AbortController(); const p2 = run(W.hang, { signal: t.signal }); setTimeout(() => t.abort(PUBLIC_ERROR_CODES.timeout), 100); assert.equal(await code(p2), 'timeout');
  const pre = new AbortController(); pre.abort(); assert.equal(await code(run(W.hang, { signal: pre.signal })), 'cancelled');
});

await check('malformed worker messages (null, string, no `success`) are ignored; the later valid result still resolves', async () => {
  const out = await run(W.junk); assert.ok(out.traces[0] instanceof Float32Array);
});

await check('success with null/non-object data is rejected, not resolved', async () => { assert.equal(await code(run(W.nullData)), 'solver_failed'); });

await check('wavefield: frames are persisted in order and listed; expected_frames is verified', async () => {
  const stored: Array<[number, number[]]> = [];
  const out = await run(W.frames, { type: 'wave', put: async (i, f) => { stored.push([i, [...f]]); return `wave_${i}`; } });
  assert.deepEqual(stored.sort((a, b) => a[0] - b[0]), [[0, [0, 1]], [1, [1, 2]], [2, [2, 3]]]);
  assert.deepEqual(out.waveObjectIds, ['wave_0', 'wave_1', 'wave_2']);
  assert.deepEqual((out.result as any).wavefield, { outNx: 2, outNz: 1, dt: 0.01, frameCount: 3 });
});

await check('wavefield: a non-Float32Array frame, an absurd expected_frames, and a frame-count mismatch are all rejected', async () => {
  assert.equal(await code(run(W.badFrame, { type: 'wave' })), 'solver_failed');
  assert.equal(await code(run(W.tooManyExpected, { type: 'wave' })), 'resource_limit');
  assert.equal(await code(run(W.expectedMismatch, { type: 'wave' })), 'storage_failed');
  assert.ok(99999 > LIMITS.MAX_WAVEFIELD_FRAMES);
});

await check('wavefield: a failing frame upload surfaces as storage_failed, and a quota SolverError keeps its own code', async () => {
  assert.equal(await code(run(W.frames, { type: 'wave', put: async () => { throw new Error('gcs down'); } })), 'storage_failed');
  assert.equal(await code(run(W.frames, { type: 'wave', put: async () => { throw new SolverError(PUBLIC_ERROR_CODES.resource_limit); } })), 'resource_limit');
});

await check('abort during in-flight uploads waits for them to settle before rejecting (no orphaned artifact after cleanup)', async () => {
  let finished = 0; const c = new AbortController();
  const frames = script('slowframes', `parentPort.postMessage({ type: 'wavefield_frame', frame: new Float32Array(2) }); setInterval(() => {}, 1000);`);
  const p = run(frames, { type: 'wave', signal: c.signal, put: () => new Promise((r) => setTimeout(() => { finished++; r('late'); }, 300)) });
  setTimeout(() => c.abort(), 80);
  assert.equal(await code(p), 'cancelled'); assert.equal(finished, 1, 'the in-flight upload must complete before the rejection is delivered');
});

fs.rmSync(dir, { recursive: true, force: true });
console.log(`\n=== ${passed} passed ===`);
