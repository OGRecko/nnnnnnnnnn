/**
 * audioEngine against a recording Web Audio fake. The fake implements just enough of the spec to run the real engine
 * code (node graph, AudioParams, buffers, listener, decodeAudioData), and records every node, connection, start and stop
 * so lifecycle and wiring can be asserted. It is NOT a sound-quality test: no audio is rendered.
 */
import assert from 'node:assert/strict';

// ---------------------------------------------------------------- Web Audio fake
const PARAMS = new Set(['gain', 'frequency', 'detune', 'Q', 'positionX', 'positionY', 'positionZ', 'orientationX', 'orientationY', 'orientationZ', 'threshold', 'knee', 'ratio', 'attack', 'release', 'playbackRate', 'pan', 'delayTime', 'offset']);
class FakeParam { value = 0; targets: Array<[number, number, number]> = [];
  setValueAtTime(v: number) { this.value = v; return this; } linearRampToValueAtTime(v: number) { this.value = v; return this; } exponentialRampToValueAtTime(v: number) { this.value = v; return this; }
  setTargetAtTime(v: number, t: number, k: number) { this.targets.push([v, t, k]); this.value = v; return this; } cancelScheduledValues() { return this; } }
interface Rec { kind: string; connections: unknown[]; started: number; stopped: number; disconnected: number; stopThrows?: Error | null; disconnectThrows?: boolean }
const allNodes: any[] = [];
const STOPPABLE = new Set(['oscillator', 'bufferSource', 'constantSource']);
function makeNode(kind: string): any {
  const rec: Rec = { kind, connections: [], started: 0, stopped: 0, disconnected: 0 };
  const params: Record<string, FakeParam> = {};
  const n: any = new Proxy(rec as any, {
    get(t, p: string) {
      if (p in t) return t[p];
      if (p === 'connect') return (d: unknown) => { t.connections.push(d); return d; };
      if (p === 'disconnect') return () => { if (t.disconnectThrows) throw new Error('already disconnected'); t.disconnected++; };
      if (STOPPABLE.has(kind) && p === 'start') return () => { t.started++; };
      if (STOPPABLE.has(kind) && p === 'stop') return () => { if (t.stopThrows) throw t.stopThrows; t.stopped++; };
      if (PARAMS.has(p)) return (params[p] ||= new FakeParam());
      return undefined;
    },
    set(t, p: string, v) { (t as any)[p] = v; return true; },
  });
  allNodes.push(n); return n;
}
class FakeBuffer { constructor(public numberOfChannels: number, public length: number, public sampleRate: number) { this.data = Array.from({ length: numberOfChannels }, () => new Float32Array(length)); }
  data: Float32Array[]; get duration() { return this.length / this.sampleRate; } getChannelData(i: number) { return this.data[i]; } }
const fakeCtl = { sampleRate: 48000, state: 'running' as string, resumed: 0, decodeFails: false, listenerVariant: 'params' as 'params' | 'legacy', ctxCount: 0, setPositionCalls: [] as number[][] };
class FakeAudioContext {
  sampleRate = fakeCtl.sampleRate; state = fakeCtl.state; currentTime = 1.5; destination = makeNode('destination'); listener: any;
  constructor() { fakeCtl.ctxCount++; this.listener = fakeCtl.listenerVariant === 'params'
    ? { positionX: new FakeParam(), positionY: new FakeParam(), positionZ: new FakeParam() }
    : { setPosition: (...a: number[]) => { fakeCtl.setPositionCalls.push(a); } }; }
  resume() { fakeCtl.resumed++; this.state = 'running'; return Promise.resolve(); }
  createBuffer(ch: number, len: number, sr: number) { if (!(len >= 1) || !(ch >= 1)) throw new RangeError('createBuffer: invalid length'); return new FakeBuffer(ch, len, sr); }
  createGain() { const n = makeNode('gain'); n.gain.value = 1; return n; } createPanner() { return makeNode('panner'); } createBiquadFilter() { return makeNode('biquad'); }
  createDynamicsCompressor() { return makeNode('compressor'); } createConvolver() { return makeNode('convolver'); } createOscillator() { return makeNode('oscillator'); }
  createBufferSource() { return makeNode('bufferSource'); } createConstantSource() { return makeNode('constantSource'); } createMediaStreamSource() { return makeNode('mediaStreamSource'); }
  createWaveShaper() { return makeNode('waveShaper'); } createDelay() { return makeNode('delay'); } createStereoPanner() { return makeNode('stereoPanner'); } createChannelSplitter() { return makeNode('splitter'); } createChannelMerger() { return makeNode('merger'); } createAnalyser() { return makeNode('analyser'); }
  async decodeAudioData(ab: ArrayBuffer) { if (fakeCtl.decodeFails) throw new DOMException('Unable to decode audio data', 'EncodingError'); return new FakeBuffer(2, Math.max(1, ab.byteLength), 48000); }
}
const g: any = globalThis;
const alerts: string[] = []; const speech = { cancelled: 0 };
g.window = { AudioContext: FakeAudioContext, speechSynthesis: { cancel() { speech.cancelled++; }, speak() {} } };
g.AudioBuffer = FakeBuffer; g.SpeechSynthesisUtterance = class { rate = 1; pitch = 1; volume = 1; onend: (() => void) | null = null; constructor(public text: string) {} }; g.alert = (m: string) => { alerts.push(String(m)); };
const nav: any = { mediaDevices: undefined }; Object.defineProperty(g, 'navigator', { value: nav, configurable: true });
console.warn = () => {}; // the engine logs expected degraded-mode warnings; keep test output readable
const origLog = console.log; const origError = console.error; console.log = () => {}; console.error = () => {};

const { audioEngine, getAudioContextCtor } = await import('./audioEngine');
const { useStore } = await import('../store/useStore');
const { MATERIALS } = await import('./materials');
console.log = origLog;
// The engine's own console.error output is silenced above, but test failures MUST stay visible.
const reportFail = (msg: string) => origError(msg);

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) { try { reset(); await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { reportFail(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
function reset() {
  const e: any = audioEngine; e.stop?.();
  Object.assign(e, { ctx: null, masterGain: null, limiter: null, convolver: null, micSourceNode: null, isPlaying: false, micStatus: 'idle', onMicStatusChange: null });
  e.sourceNodes.clear(); e.customBuffers.clear();
  allNodes.length = 0; alerts.length = 0; speech.cancelled = 0; nav.mediaDevices = undefined;
  Object.assign(fakeCtl, { sampleRate: 48000, state: 'running', resumed: 0, decodeFails: false, listenerVariant: 'params', ctxCount: 0, setPositionCalls: [] });
}
console.log('\n=== audioEngine (recording Web Audio fake) ===\n');

const SQUARE = [{ x: .1, y: .1 }, { x: .9, y: .1 }, { x: .9, y: .9 }, { x: .1, y: .9 }];
const src = (o: any = {}) => ({ id: 's1', brand: 'X', model: 'Y', x: .5, y: .5, soundType: 'noise_white', ...o });
const rcv = { id: 'r1', name: 'R', x: .5, y: .6 };
const play = (sources: any[], o: { receiver?: any; type?: string; walls?: string[] } = {}) =>
  audioEngine.play(sources as any, o.receiver === undefined ? rcv : o.receiver, 10, 10, o.type ?? 'noise_white', SQUARE as any, o.walls ?? [null, null, null, null], 'drywall');
const nodesOf = (kind: string) => allNodes.filter((n) => n.kind === kind);
const peak = (a: Float32Array) => { let m = 0; for (let i = 0; i < a.length; i++) { const v = Math.abs(a[i]); if (v > m) m = v; } return m; };
const rms = (a: Float32Array) => Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length);

await check('getAudioContextCtor: standard, prefixed (old Safari) and missing', () => {
  assert.equal(getAudioContextCtor(), FakeAudioContext);
  const w = g.window; g.window = { webkitAudioContext: class Old {} }; assert.equal(getAudioContextCtor().name, 'Old');
  g.window = {}; assert.throws(() => getAudioContextCtor(), /not supported/); g.window = w;
});

await check('init(): one context, idempotent, master -> limiter -> destination, limiter configured, convolver feeds the wet bus', () => {
  audioEngine.init(); audioEngine.init(); audioEngine.init();
  assert.equal(fakeCtl.ctxCount, 1);
  const e: any = audioEngine;
  assert.equal(e.masterGain.gain.value, 0.9);
  assert.ok(e.masterGain.connections.includes(e.limiter)); assert.ok(e.limiter.connections.includes(e.ctx.destination));
  assert.deepEqual([e.limiter.threshold.value, e.limiter.ratio.value], [-6, 20]);
  const wet = e.convolver.connections[0]; assert.equal(wet.gain.value, 0.4); assert.ok(wet.connections.includes(e.masterGain));
  assert.ok(e.convolver.buffer, 'a convolver buffer (reverb or dry impulse) must always exist after init');
});

await check('init() with no Web Audio support throws a clear error and leaves the engine uninitialised', () => {
  g.window = {}; try { assert.throws(() => audioEngine.init(), /not supported/); assert.equal(audioEngine.ctx, null); } finally { g.window = { AudioContext: FakeAudioContext, speechSynthesis: { cancel() { speech.cancelled++; }, speak() {} } }; }
});

await check('updateFdtdIR before init is a safe no-op; with a buffer it is used verbatim; with null it falls back to a non-empty IR', () => {
  assert.doesNotThrow(() => audioEngine.updateFdtdIR(null));
  audioEngine.init(); const b: any = new FakeBuffer(1, 10, 48000);
  audioEngine.updateFdtdIR(b); assert.equal((audioEngine.convolver as any).buffer, b);
  audioEngine.updateFdtdIR(null); const fb: any = (audioEngine.convolver as any).buffer; assert.ok(fb !== b && fb.length >= 1);
});

await check('generateImpulseResponse: stereo, ceil(sr*rt60) samples, deterministic, channels decorrelated, finite', () => {
  audioEngine.init(); const ctx: any = audioEngine.ctx;
  const a: any = audioEngine.generateImpulseResponse(ctx, 0.8), b: any = audioEngine.generateImpulseResponse(ctx, 0.8);
  assert.equal(a.numberOfChannels, 2); assert.equal(a.length, Math.ceil(48000 * 0.8));
  assert.deepEqual([...a.getChannelData(0).slice(0, 500)], [...b.getChannelData(0).slice(0, 500)], 'same RT60 must give the same tail');
  assert.notDeepEqual([...a.getChannelData(0).slice(0, 50)], [...a.getChannelData(1).slice(0, 50)]);
  for (const c of [0, 1]) assert.ok(a.getChannelData(c).every(Number.isFinite));
  const c: any = audioEngine.generateImpulseResponse(ctx, 0.81); assert.notDeepEqual([...c.getChannelData(0).slice(0, 50)], [...a.getChannelData(0).slice(0, 50)]);
});

await check('generateImpulseResponse: the envelope reaches -60 dB at t = RT60 (the definition of RT60), and never exceeds the decay curve', () => {
  audioEngine.init(); const ctx: any = audioEngine.ctx; const rt = 1.2;
  const ch: Float32Array = (audioEngine.generateImpulseResponse(ctx, rt) as any).getChannelData(0);
  const tau = rt * 20 / (60 * Math.log(10));
  for (let i = 0; i < ch.length; i += 97) assert.ok(Math.abs(ch[i]) <= Math.exp(-(i / 48000) / tau) + 1e-9, `sample ${i} above envelope`);
  const lastAmp = Math.exp(-(ch.length / 48000) / tau); assert.ok(Math.abs(20 * Math.log10(lastAmp) + 60) < 0.1, `end level ${20 * Math.log10(lastAmp)} dB`);
  const early = rms(ch.slice(0, 2000)), late = rms(ch.slice(ch.length - 2000)); assert.ok(20 * Math.log10(late / early) < -45, 'tail must be far quieter than the onset');
});

await check('generateImpulseResponse rejects 0, negative, NaN and Infinity RT60 instead of inventing a value', () => {
  audioEngine.init(); for (const bad of [0, -1, NaN, Infinity, -Infinity]) assert.throws(() => audioEngine.generateImpulseResponse(audioEngine.ctx as any, bad), RangeError, String(bad));
});

await check('generateImpulseResponse scales with the sample rate', () => {
  fakeCtl.sampleRate = 44100; audioEngine.init(); assert.equal((audioEngine.generateImpulseResponse(audioEngine.ctx as any, 0.5) as any).length, 22050);
});

await check('createNoiseBuffer: 2 s mono; white is zero-mean/bounded/uncorrelated; pink and brown are progressively more low-frequency (lag-1 autocorrelation)', () => {
  audioEngine.init(); const ctx: any = audioEngine.ctx;
  const ac = (x: Float32Array) => { let n = 0, d = 0; for (let i = 1; i < x.length; i++) { n += x[i] * x[i - 1]; d += x[i] * x[i]; } return n / d; };
  const get = (t: any) => { const b: any = audioEngine.createNoiseBuffer(ctx, t); assert.equal(b.numberOfChannels, 1); assert.equal(b.length, 96000); const x: Float32Array = b.getChannelData(0); assert.ok(x.every(Number.isFinite)); return x; };
  const w = get('white'), p = get('pink'), br = get('brown');
  const mean = w.reduce((s, v) => s + v, 0) / w.length; assert.ok(Math.abs(mean) < 0.02, `white mean ${mean}`); assert.ok(w.every((v) => v >= -1 && v <= 1));
  assert.ok(Math.abs(ac(w)) < 0.02, `white autocorrelation ${ac(w)}`);
  assert.ok(ac(p) > 0.3 && ac(p) < ac(br), `pink ${ac(p)} brown ${ac(br)}`); assert.ok(ac(br) > 0.95, `brown ${ac(br)}`);
  assert.ok(peak(p) < 2 && peak(br) < 3, 'noise must not blow up');
});

await check('every synthesised instrument loop is finite, non-silent, mono/stereo-valid, and of sensible length and level', () => {
  audioEngine.init(); const ctx: any = audioEngine.ctx; const e: any = audioEngine;
  const makers = Object.getOwnPropertyNames(Object.getPrototypeOf(e)).filter((n) => /^create.*(LoopBuffer|BeatBuffer)$/.test(n));
  assert.ok(makers.length >= 14, `found only ${makers.length} loop makers`);
  for (const m of makers) {
    const b: FakeBuffer = e[m](ctx); assert.ok(b.length > 4800 && b.length < 48000 * 90, `${m} length ${b.length}`);
    for (let c = 0; c < b.numberOfChannels; c++) { const x = b.getChannelData(c); assert.ok(x.every(Number.isFinite), `${m} has NaN/Infinity`); assert.ok(rms(x) > 1e-4, `${m} is silent`); assert.ok(peak(x) < 4, `${m} peaks absurdly high`); }
  }
});

await check('lineIntersect: crossing returns the position along the wall; parallel, collinear and non-crossing return null; endpoints count', () => {
  const e: any = audioEngine;
  assert.equal(e.lineIntersect(0, .5, 1, .5, .5, 0, .5, 1), .5); assert.equal(e.lineIntersect(0, .5, 1, .5, .25, 0, .25, 1), .5);
  assert.equal(e.lineIntersect(0, 0, 1, 0, 0, 1, 1, 1), null, 'parallel'); assert.equal(e.lineIntersect(0, 0, 1, 0, .2, 0, .8, 0), null, 'collinear');
  assert.equal(e.lineIntersect(0, .5, .4, .5, .5, 0, .5, 1), null, 'stops short'); assert.equal(e.lineIntersect(0, .5, .5, .5, .5, 0, .5, 1), .5, 'touching an endpoint');
  assert.equal(e.lineIntersect(0, 0, 0, 0, 0, 0, 1, 1), null, 'zero-length ray');
});

await check('checkWallIntersections: both inside = 0 dB; receiver outside crosses exactly one wall and pays its transmission loss', () => {
  const e: any = audioEngine; const tl = (id: string) => MATERIALS.walls.find((m) => m.id === id)!.tl;
  assert.equal(e.checkWallIntersections(0, 0, 2, 2, SQUARE, [null, null, null, null], 'drywall', 10, 10), 0);
  assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, null, null, null], 'drywall', 10, 10), tl('drywall'));
  assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, ['concrete', 'concrete', 'concrete', 'concrete'], 'drywall', 10, 10), tl('concrete'));
  assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, 'glass', null, null], 'drywall', 10, 10), tl('glass'), 'per-wall override applies to that wall only (wall 1 is x = 0.9)');
});

await check('checkWallIntersections: crossing two walls adds both losses; a full-opening wall and a door gap let sound through; outside the gap it does not', () => {
  const e: any = audioEngine; const tl = MATERIALS.walls.find((m) => m.id === 'drywall')!.tl;
  assert.equal(e.checkWallIntersections(-6, 0, 6, 0, SQUARE, [null, null, null, null], 'drywall', 10, 10), 2 * tl);
  assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, null, null, null], 'drywall', 10, 10, [null, 'full', null, null]), 0);
  assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, null, null, null], 'drywall', 10, 10, [null, { start: .4, end: .6 }, null, null]), 0, 'path through the door');
  assert.equal(e.checkWallIntersections(0, 0, 6, -3, SQUARE, [null, null, null, null], 'drywall', 10, 10, [null, { start: .4, end: .6 }, null, null]), tl, 'path outside the door');
});

await check('checkWallIntersections: a path through an exact corner is charged ONE wall, not two; a path that only grazes a corner is charged nothing (regression)', () => {
  const e: any = audioEngine; const tl = MATERIALS.walls.find((m) => m.id === 'drywall')!.tl; const none = [null, null, null, null];
  assert.equal(e.checkWallIntersections(0, 0, 6, 6, SQUARE, none, 'drywall', 10, 10), tl, 'diagonal through the (0.9,0.9) corner leaves the room once');
  assert.equal(e.checkWallIntersections(0, 0, -6, -6, SQUARE, none, 'drywall', 10, 10), tl, 'and the opposite corner');
  assert.equal(e.checkWallIntersections(5, 3, 3, 5, SQUARE, none, 'drywall', 10, 10), 0, 'anti-diagonal outside the room that only touches the corner');
  const conc = MATERIALS.walls.find((m) => m.id === 'concrete')!.tl;
  assert.equal(e.checkWallIntersections(0, 0, 6, 6, SQUARE, [null, 'concrete', 'drywall', null], 'drywall', 10, 10), (conc + tl) / 2, 'a corner between two materials uses their mean');
  assert.equal(e.checkWallIntersections(0, 0, 6, 6, SQUARE, none, 'drywall', 10, 10, [null, 'full', 'full', null]), 0, 'both walls removed');
  assert.equal(e.checkWallIntersections(0, 0, 6, 5.9, SQUARE, none, 'drywall', 10, 10), tl, 'just beside the corner is unchanged');
});

await check('checkWallIntersections: zero/negative/NaN room sizes return 0 (never NaN); an unknown wall material throws instead of guessing', () => {
  const e: any = audioEngine;
  for (const [L, W] of [[0, 10], [10, 0], [-5, 10], [NaN, 10], [10, Infinity]]) assert.equal(e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, null, null, null], 'drywall', L, W), 0);
  assert.throws(() => e.checkWallIntersections(0, 0, 6, 0, SQUARE, [null, null, null, null], 'unobtainium', 10, 10), /Unknown wall material/);
});

await check('play(): one panner/gain chain per UNMUTED source, registered by id; muted sources create nothing; isPlaying is set', async () => {
  await play([src({ id: 'a' }), src({ id: 'b', muted: true }), src({ id: 'c', soundType: 'pulse' })]);
  const e: any = audioEngine; assert.deepEqual([...e.sourceNodes.keys()].sort(), ['a', 'c']); assert.equal(nodesOf('panner').length, 2); assert.equal(e.isPlaying, true);
  assert.equal(nodesOf('bufferSource').filter((n) => n.started === 1).length, 1);
  assert.equal(nodesOf('oscillator').filter((n) => n.started === 1).length, 2, 'pulse = carrier + LFO');
});

await check('play(): every source gain feeds BOTH the dry master bus and the convolver (reverb) bus', async () => {
  await play([src()]); const e: any = audioEngine; const { gain } = e.sourceNodes.get('s1');
  assert.ok(gain.connections.includes(e.masterGain)); assert.ok(gain.connections.includes(e.convolver));
});

await check('play(): every built-in sound type produces a running source without throwing', async () => {
  const types = ['noise_white', 'noise_pink', 'noise_brown', 'bass', 'piano', 'violin', 'guitar', 'drumbeat', 'synthlead', 'cello', 'flute', 'organ', 'marimba', 'synthpad', 'hiphopbeat', 'bells', 'oceanwaves', 'song', 'pulse', 'testing123', 'something-unknown'];
  for (const t of types) { reset(); await play([src({ soundType: t })]); assert.ok((audioEngine as any).sourceNodes.has('s1'), t); assert.ok(allNodes.some((n) => (n.kind === 'bufferSource' || n.kind === 'oscillator') && n.started > 0), `${t}: nothing started`); audioEngine.stop(); }
});

await check('play(): gain staging - 0 dB vs -6 dB differ by 6 dB; a wall in the path attenuates by its TL and low-passes at 500 Hz; non-finite gainDb is treated as 0 dB', async () => {
  await play([src({ id: 'a', gainDb: 0 }), src({ id: 'b', gainDb: -6, x: .5 })]); const e: any = audioEngine;
  const ga = e.sourceNodes.get('a').gain.gain.value, gb = e.sourceNodes.get('b').gain.gain.value; assert.ok(Math.abs(20 * Math.log10(gb / ga) + 6) < 1e-9);
  reset(); await play([src({ id: 'a' })], { receiver: { id: 'r', name: 'r', x: 1.1, y: .5 } }); const walled = (audioEngine as any).sourceNodes.get('a').gain.gain.value;
  reset(); await play([src({ id: 'a' })]); const open = (audioEngine as any).sourceNodes.get('a').gain.gain.value;
  assert.ok(Math.abs(20 * Math.log10(walled / open) + 35) < 1e-9, `wall loss ${20 * Math.log10(walled / open)} dB`);
  assert.equal(nodesOf('biquad').filter((n) => n.type === 'lowpass').length >= 1, true);
  reset(); await play([src({ id: 'a', gainDb: NaN }), src({ id: 'b', gainDb: Infinity })]);
  const ge = (audioEngine as any).sourceNodes; assert.ok(Number.isFinite(ge.get('a').gain.gain.value) && Number.isFinite(ge.get('b').gain.gain.value));
});

await check('play(): the listener is placed at the receiver (AudioParam listeners and legacy setPosition listeners)', async () => {
  await play([src()], { receiver: { id: 'r', name: 'r', x: .75, y: .25 } }); const l: any = (audioEngine.ctx as any).listener; assert.deepEqual([l.positionX.value, l.positionZ.value], [2.5, -2.5]);
  reset(); fakeCtl.listenerVariant = 'legacy'; await play([src()], { receiver: { id: 'r', name: 'r', x: .75, y: .25 } }); assert.deepEqual(fakeCtl.setPositionCalls[0], [2.5, 1.6, -2.5]);
  reset(); await play([src()], { receiver: null }); assert.equal(audioEngine.isPlaying, true);
});

await check('play(): a suspended context is resumed (autoplay policy)', async () => { fakeCtl.state = 'suspended'; await play([src()]); assert.equal(fakeCtl.resumed, 1); });

await check('play() twice replaces the first graph: the old sources are stopped and nothing accumulates', async () => {
  await play([src({ id: 'a' })]); const first = nodesOf('bufferSource'); assert.equal(first.length, 1);
  await play([src({ id: 'a' })]); assert.equal(first[0].stopped, 1, 'the previous noise source must be stopped'); assert.equal((audioEngine as any).sourceNodes.size, 1);
});

await check('stop(): stops every stoppable node, disconnects the chain, clears the registry, cancels speech and bumps the generation', async () => {
  await play([src({ id: 'a' }), src({ id: 'b', soundType: 'pulse' })]); const gen = audioEngine.playGeneration;
  audioEngine.stop(); assert.equal(audioEngine.isPlaying, false); assert.equal((audioEngine as any).sourceNodes.size, 0); assert.ok(audioEngine.playGeneration > gen); assert.ok(speech.cancelled >= 1);
  for (const n of allNodes.filter((x) => (x.kind === 'bufferSource' || x.kind === 'oscillator') && x.started > 0)) assert.equal(n.stopped, 1, `${n.kind} not stopped`);
  for (const n of nodesOf('panner')) assert.ok(n.disconnected >= 1);
});

await check('stop(): one node throwing (already ended / already disconnected) does not leave the rest playing; stop() is idempotent', async () => {
  await play([src({ id: 'a' }), src({ id: 'b' })]); const srcs = nodesOf('bufferSource');
  srcs[0].stopThrows = new DOMException('already stopped', 'InvalidStateError'); srcs[0].disconnectThrows = true; nodesOf('panner')[0].disconnectThrows = true;
  assert.doesNotThrow(() => audioEngine.stop()); assert.equal(srcs[1].stopped, 1, 'the second source must still be stopped'); assert.doesNotThrow(() => { audioEngine.stop(); audioEngine.stop(); });
  reset(); assert.doesNotThrow(() => audioEngine.stop());
});

await check('microphone: unsupported browser -> status "unsupported", user is told, playback falls back instead of failing', async () => {
  const seen: string[] = []; audioEngine.onMicStatusChange = (s) => seen.push(s);
  nav.mediaDevices = undefined; await play([src({ soundType: 'mic' })], { type: 'mic' });
  assert.equal(audioEngine.micStatus, 'unsupported'); assert.equal(alerts.length, 1); assert.ok(seen.includes('unsupported')); assert.equal((audioEngine as any).sourceNodes.size, 1);
});

await check('microphone: permission denied -> "denied" + alert + fallback; granted -> "active", mic wired through a boost stage, tracks released on stop()', async () => {
  nav.mediaDevices = { getUserMedia: async () => { throw new DOMException('denied', 'NotAllowedError'); } };
  await play([src({ soundType: 'mic' })], { type: 'song' }); assert.equal(audioEngine.micStatus, 'denied'); assert.equal(alerts.length, 1);
  reset(); const tracks = [{ stopped: 0, stop() { this.stopped++; } }]; const stream = { getTracks: () => tracks };
  nav.mediaDevices = { getUserMedia: async (c: any) => { assert.equal(c.audio.echoCancellation, false, 'raw capture, no processing'); return stream; } };
  await play([src({ soundType: 'mic' })]); assert.equal(audioEngine.micStatus, 'active');
  const boost = nodesOf('gain').find((n) => n.gain.value === 6); assert.ok(boost, 'mic boost stage'); assert.ok(nodesOf('mediaStreamSource').length === 1);
  audioEngine.stop(); assert.equal(tracks[0].stopped, 1, 'the microphone must be released'); assert.equal(audioEngine.micStatus, 'idle');
});

await check('microphone: a play() superseded while the permission prompt is open releases the mic and builds no graph (race)', async () => {
  const tracks = [{ stopped: 0, stop() { this.stopped++; } }]; let release!: (s: any) => void;
  nav.mediaDevices = { getUserMedia: () => new Promise((r) => { release = r; }) };
  const p = play([src({ soundType: 'mic' })]); await new Promise((r) => setTimeout(r, 10)); audioEngine.stop(); release({ getTracks: () => tracks }); await p;
  assert.equal(tracks[0].stopped, 1, 'the late stream must be released'); assert.equal((audioEngine as any).sourceNodes.size, 0); assert.equal(nodesOf('mediaStreamSource').length, 0);
});

await check('custom audio: decode stores the buffer and reports its duration; a decode failure rejects and stores nothing; a custom source plays it', async () => {
  const file = { arrayBuffer: async () => new ArrayBuffer(96000) } as any;
  assert.deepEqual(await audioEngine.loadCustomAudioFile('s1', file), { durationSec: 2 }); assert.ok(audioEngine.customBuffers.has('s1'));
  await play([src({ soundType: 'custom' })]); const bs = nodesOf('bufferSource'); assert.equal(bs.length, 1); assert.equal(bs[0].buffer, audioEngine.customBuffers.get('s1')); assert.equal(bs[0].loop, true);
  fakeCtl.decodeFails = true; await assert.rejects(audioEngine.loadCustomAudioFile('bad', file), /decode/i); assert.equal(audioEngine.customBuffers.has('bad'), false);
  audioEngine.clearCustomAudioFile('s1'); assert.equal(audioEngine.customBuffers.has('s1'), false); assert.doesNotThrow(() => audioEngine.clearCustomAudioFile('never-existed'));
});

await check('a custom source with no uploaded file does not crash playback', async () => { await play([src({ soundType: 'custom' })]); assert.equal(audioEngine.isPlaying, true); });

await check('live updates: position/listener/volume use smooth AudioParam targets; unknown ids and a missing context are safe no-ops; bad gain throws', async () => {
  assert.doesNotThrow(() => { audioEngine.updateSourcePosition('x', 1, 2, 3); audioEngine.updateSourceVolume('x', 0); audioEngine.updateListener(rcv as any, 10, 10); });
  await play([src()]); const n: any = (audioEngine as any).sourceNodes.get('s1');
  audioEngine.updateSourcePosition('s1', 1, 2, 3); assert.deepEqual([n.panner.positionX.targets.at(-1)![0], n.panner.positionZ.targets.at(-1)![0]], [1, 3]);
  audioEngine.updateSourceVolume('s1', -6); assert.ok(Math.abs(n.gain.gain.targets.at(-1)![0] - Math.pow(10, -6 / 20) * 0.7) < 1e-9);
  assert.throws(() => audioEngine.updateSourceVolume('s1', NaN), RangeError); assert.throws(() => audioEngine.updateSourceVolume('s1', Infinity), RangeError);
  audioEngine.updateListener({ ...rcv, x: 1, y: 0 } as any, 10, 10); assert.equal((audioEngine.ctx as any).listener.positionX.targets.at(-1)[0], 5);
  audioEngine.updateSourceVolume('nope', NaN); // unknown id: nothing to update, nothing thrown
});

await check('bad room input degrades to a dry (reverb-free) result rather than crashing play(): zero-size room and an unknown floor material', async () => {
  await audioEngine.play([src()] as any, rcv as any, 0, 0, 'noise_white', SQUARE as any, [null, null, null, null], 'drywall', [], 3, 'no-such-floor', 'stonewool');
  assert.equal(audioEngine.isPlaying, true); assert.ok((audioEngine.convolver as any).buffer);
});

console.log(`\n=== ${passed} passed ===`);
