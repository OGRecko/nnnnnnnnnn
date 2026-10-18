import assert from 'node:assert/strict';
import { runGPUBenchmark } from './gpu-solver';

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) { try { await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== gpu-solver (WebGL2 capability benchmark, fake GL) ===\n');

type Opts = { noContext?: boolean; lost?: boolean; noFloatExt?: boolean; maxTex?: number; compileFail?: boolean; linkFail?: boolean; incompleteFb?: boolean; glErrorAfterAlloc?: boolean; glErrorAtEnd?: boolean; throwOnDraw?: boolean; lostAtEnd?: boolean; nullTexture?: boolean; deleteThrows?: boolean };
function makeGL(o: Opts = {}) {
  const live = { texture: 0, framebuffer: 0, shader: 0, buffer: 0, program: 0 }; const created = { ...live };
  let allocDone = false, drew = 0, lostNow = !!o.lost;
  const mk = (k: keyof typeof live) => () => { if (k === 'texture' && o.nullTexture) return null; live[k]++; created[k]++; return { k }; };
  const del = (k: keyof typeof live) => () => { if (o.deleteThrows) throw new Error('context lost'); live[k]--; };
  const gl: any = {
    VERTEX_SHADER: 1, FRAGMENT_SHADER: 2, COMPILE_STATUS: 3, LINK_STATUS: 4, ARRAY_BUFFER: 5, STATIC_DRAW: 6, FLOAT: 7, TEXTURE_2D: 8, RGBA32F: 9, RGBA: 10, NEAREST: 11, CLAMP_TO_EDGE: 12,
    TEXTURE_MIN_FILTER: 13, TEXTURE_MAG_FILTER: 14, TEXTURE_WRAP_S: 15, TEXTURE_WRAP_T: 16, FRAMEBUFFER: 17, COLOR_ATTACHMENT0: 18, FRAMEBUFFER_COMPLETE: 19, TEXTURE0: 20, TEXTURE1: 21, TRIANGLES: 22, MAX_TEXTURE_SIZE: 23, NO_ERROR: 0,
    isContextLost: () => lostNow, getExtension: (n: string) => (n === 'EXT_color_buffer_float' && !o.noFloatExt ? {} : null), getParameter: () => o.maxTex ?? 16384,
    viewport() {}, createShader: mk('shader'), shaderSource() {}, compileShader() {}, getShaderParameter: () => !o.compileFail, getShaderInfoLog: () => 'ERROR: 0:1: \n  /driver/secret/path.glsl line 9\n bad token', deleteShader: del('shader'),
    createProgram: mk('program'), attachShader() {}, linkProgram() {}, getProgramParameter: () => !o.linkFail, getProgramInfoLog: () => 'link bad', deleteProgram: del('program'),
    createBuffer: mk('buffer'), bindBuffer() {}, bufferData() {}, deleteBuffer: del('buffer'), getAttribLocation: () => 0, enableVertexAttribArray() {}, vertexAttribPointer() {},
    createTexture: mk('texture'), bindTexture() {}, texImage2D() { allocDone = true; }, texParameteri() {}, deleteTexture: del('texture'),
    createFramebuffer: mk('framebuffer'), bindFramebuffer() {}, framebufferTexture2D() {}, checkFramebufferStatus: () => (o.incompleteFb ? 0 : 19), deleteFramebuffer: del('framebuffer'),
    useProgram() {}, getUniformLocation: () => ({}), uniform1i() {}, uniform1f() {}, uniform2f() {}, activeTexture() {},
    drawArrays() { if (o.throwOnDraw) throw new Error('GPU hang'); drew++; }, readPixels() { if (o.lostAtEnd) lostNow = true; },
    getError: () => (o.glErrorAfterAlloc && allocDone && drew === 0 ? 1285 : o.glErrorAtEnd && drew > 0 ? 1282 : 0),
  };
  return { gl, live, created, drawCalls: () => drew };
}
function install(o: Opts | 'no-dom' = {}) {
  const g: any = globalThis; const saved = { doc: g.document, perf: g.performance };
  let made: ReturnType<typeof makeGL> | null = null; let t = 0;
  if (o === 'no-dom') delete g.document;
  else { made = makeGL(o); g.document = { createElement: () => ({ width: 0, height: 0, getContext: () => (o.noContext ? null : made!.gl) }) }; }
  Object.defineProperty(g, 'performance', { value: { now: () => (t += 7) }, configurable: true });
  return { made, restore() { if (saved.doc === undefined) delete g.document; else g.document = saved.doc; Object.defineProperty(g, 'performance', { value: saved.perf, configurable: true }); } };
}
async function run(o: Opts | 'no-dom', n = 1_000_000) { const e = install(o); try { return { res: await runGPUBenchmark(n), made: e.made }; } finally { e.restore(); } }
const noLeak = (m: ReturnType<typeof makeGL> | null) => { if (m) assert.deepEqual(m.live, { texture: 0, framebuffer: 0, shader: 0, buffer: 0, program: 0 }, `leaked GL objects: ${JSON.stringify(m.live)}`); };

await check('success: supported, measured time (never fabricated), 10 steps drawn, all GL objects released', async () => {
  const { res, made } = await run({});
  assert.equal(res.supported, true); assert.equal(res.reason, undefined);
  assert.equal(res.timeMs, 7, 'time must come from performance.now() deltas');
  assert.equal(made!.drawCalls(), 10); assert.equal(made!.created.texture, 3); noLeak(made);
});

await check('graceful: no DOM (server/worker) resolves unsupported instead of throwing', async () => {
  const { res } = await run('no-dom'); assert.deepEqual([res.supported, res.timeMs], [false, 0]); assert.match(res.reason!, /DOM|browser/i);
});

await check('graceful: WebGL2 unavailable, lost context, missing float extension each resolve unsupported with a clear reason', async () => {
  for (const [o, re] of [[{ noContext: true }, /WebGL2 is not supported/], [{ lost: true }, /lost/i], [{ noFloatExt: true }, /EXT_color_buffer_float/]] as const) {
    const { res, made } = await run(o); assert.equal(res.supported, false); assert.match(res.reason!, re); noLeak(made);
  }
});

await check('graceful: a texture larger than the GPU limit resolves unsupported (and allocates nothing)', async () => {
  const { res, made } = await run({ maxTex: 512 }, 10_000_000); assert.equal(res.supported, false); assert.match(res.reason!, /3163.*512/); assert.equal(made!.created.texture, 0);
  const ok = await run({ maxTex: 1000 }, 1_000_000); assert.equal(ok.res.supported, true, 'exactly-fitting size must work');
});

await check('invalid element counts never reach the GPU: NaN, Infinity, 0, negative, -0', async () => {
  for (const n of [NaN, Infinity, -Infinity, 0, -5, -0]) { const { res, made } = await run({}, n); assert.equal(res.supported, false, String(n)); assert.equal(made!.created.texture, 0, String(n)); }
  assert.equal((await run({}, 1)).res.supported, true, '1 element is a valid 1x1 texture');
});

await check('shader compile/link failures resolve unsupported with a single-line reason (<= 200 chars), and nothing leaks', async () => {
  const c = await run({ compileFail: true }); assert.equal(c.res.supported, false); assert.ok(!c.res.reason!.includes('\n') && c.res.reason!.length <= 200); noLeak(c.made);
  const l = await run({ linkFail: true }); assert.equal(l.res.supported, false); assert.match(l.res.reason!, /link/i); noLeak(l.made);
});

await check('an incomplete framebuffer is detected: no timing is reported for a pipeline that renders nothing (regression)', async () => {
  const { res, made } = await run({ incompleteFb: true }); assert.deepEqual([res.supported, res.timeMs], [false, 0]); assert.equal(made!.drawCalls(), 0); noLeak(made);
});

await check('GPU errors after allocation or after the run (OUT_OF_MEMORY / INVALID_OPERATION) invalidate the result', async () => {
  for (const o of [{ glErrorAfterAlloc: true }, { glErrorAtEnd: true }, { lostAtEnd: true }] as Opts[]) { const { res, made } = await run(o); assert.equal(res.supported, false, JSON.stringify(o)); noLeak(made); }
});

await check('an exception mid-run (GPU hang, null texture allocation) is converted to unsupported and cleans up', async () => {
  for (const o of [{ throwOnDraw: true }, { nullTexture: true }] as Opts[]) { const { res, made } = await run(o); assert.equal(res.supported, false); assert.ok(res.reason); noLeak(made); }
});

await check('cleanup errors from a lost context never escape', async () => {
  const { res } = await run({ deleteThrows: true }); assert.equal(res.supported, true);
});

await check('the promise never rejects and never logs console.error for expected unavailability', async () => {
  const orig = console.error; let logged = 0; console.error = () => { logged++; };
  try { for (const o of [{ noContext: true }, { noFloatExt: true }, { compileFail: true }, { throwOnDraw: true }] as Opts[]) await run(o); await run('no-dom'); } finally { console.error = orig; }
  assert.equal(logged, 0);
});

await check('the reference kernel is CFL-stable for 3D (Courant <= 1/sqrt(3)) and damped (<1)', async () => {
  const fs = await import('node:fs'); const src = fs.readFileSync(new URL('./gpu-solver.ts', import.meta.url), 'utf8');
  const courant = Number(/uniform1f\(gl\.getUniformLocation\(program, "uCourant"\), ([0-9.]+)\)/.exec(src)![1]);
  const damp = Number(/"uDamping"\), ([0-9.]+)\)/.exec(src)![1]);
  assert.ok(courant <= 1 / Math.sqrt(3) && courant > 0.5, `Courant ${courant}`); assert.ok(damp < 1 && damp > 0.9);
});

console.log(`\n=== ${passed} passed ===`);
