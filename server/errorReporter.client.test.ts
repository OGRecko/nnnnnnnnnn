import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const src = fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'public', 'error-reporter.js'), 'utf8');
let passed = 0;
function check(name: string, fn: () => void | Promise<void>) { return Promise.resolve().then(fn).then(() => { passed++; console.log(`  PASS  ${name}`); }, (e: any) => { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; }); }
console.log('\n=== client error reporter (sandboxed) ===\n');

/** Loads the real script into a fresh VM context with a fake browser. */
function load(opts: { dnt?: string; gpc?: boolean; storage?: Record<string, string> | 'throws'; fetchImpl?: (u: string, i: any) => any } = {}) {
  const listeners: Record<string, Array<(e: any) => void>> = {};
  const calls: Array<{ url: string; body: any; init: any }> = [];
  const win: any = {
    addEventListener: (t: string, f: any) => { (listeners[t] ||= []).push(f); },
    localStorage: opts.storage === 'throws' ? { getItem() { throw new Error('denied'); } } : { getItem: (k: string) => (opts.storage as any)?.[k] ?? null },
    doNotTrack: opts.dnt,
  };
  const ctx: any = {
    window: win, navigator: { doNotTrack: opts.dnt, globalPrivacyControl: opts.gpc }, JSON, Object, String, Error, Promise,
    fetch: (url: string, init: any) => { calls.push({ url, init, body: JSON.parse(init.body) }); return opts.fetchImpl ? opts.fetchImpl(url, init) : Promise.resolve({ ok: true }); },
  };
  vm.runInNewContext(src, ctx);
  return { calls, fire: (t: string, e: any) => (listeners[t] || []).forEach((f) => f(e)) };
}

await check('window errors are reported with message, location and stack mapped to the fields the server reads (regression)', () => {
  const r = load();
  r.fire('error', { message: 'boom', filename: 'https://app.test/assets/a.js', lineno: 10, colno: 5, error: { stack: 'Error: boom\n at f (https://app.test/assets/a.js:10:5)' } });
  assert.equal(r.calls.length, 1);
  assert.equal(r.calls[0].url, '/api/log-error');
  assert.deepEqual(Object.keys(r.calls[0].body).sort(), ['location', 'message', 'stack']);
  assert.equal(r.calls[0].body.message, 'boom');
  assert.equal(r.calls[0].body.location, 'https://app.test/assets/a.js:10:5');
  assert.match(r.calls[0].body.stack, /at f/);
  assert.equal(r.calls[0].init.method, 'POST');
});

await check('unhandled rejections report message and stack', () => {
  const r = load();
  r.fire('unhandledrejection', { reason: { message: 'nope', stack: 'Error: nope\n at g' } });
  assert.equal(r.calls[0].body.message, 'nope'); assert.match(r.calls[0].body.stack, /at g/);
  const r2 = load(); r2.fire('unhandledrejection', { reason: 'plain string' }); assert.equal(r2.calls[0].body.message, 'plain string');
  const r3 = load(); r3.fire('unhandledrejection', { reason: null }); assert.equal(r3.calls[0].body.message, 'Unhandled Rejection');
});

await check('URL query strings and fragments (which can carry tokens or ids) are stripped from message, location and stack', () => {
  const r = load();
  r.fire('error', { message: 'fail https://app.test/p?token=SECRET#frag', filename: 'https://app.test/a.js?v=1&k=SECRET', lineno: 1, colno: 1, error: { stack: 'at https://app.test/a.js?cap=SECRET:1:1' } });
  const b = JSON.stringify(r.calls[0].body);
  assert.ok(!b.includes('SECRET') && !b.includes('frag'), b);
  assert.ok(b.includes('https://app.test/p') && b.includes('https://app.test/a.js'));
});

await check('opt-out: Do Not Track, Global Privacy Control and the localStorage switch each stop all reports', () => {
  for (const o of [{ dnt: '1' }, { gpc: true }, { storage: { 'cavity.errorReporting': 'off' } }]) {
    const r = load(o as any); r.fire('error', { message: 'x', filename: '', error: null }); r.fire('unhandledrejection', { reason: new Error('y') });
    assert.equal(r.calls.length, 0, JSON.stringify(o));
  }
  const on = load({ dnt: '0', gpc: false, storage: { 'cavity.errorReporting': 'on' } }); on.fire('error', { message: 'x' }); assert.equal(on.calls.length, 1);
});

await check('blocked localStorage (private mode) does not break reporting or throw', () => {
  const r = load({ storage: 'throws' }); r.fire('error', { message: 'x' }); assert.equal(r.calls.length, 1);
});

await check('at most 5 reports per page load, and identical errors are sent once (flood protection)', () => {
  const r = load();
  for (let i = 0; i < 50; i++) r.fire('error', { message: `distinct ${i}`, filename: 'a.js', lineno: 1, colno: 1 });
  assert.equal(r.calls.length, 5);
  const d = load(); for (let i = 0; i < 20; i++) d.fire('error', { message: 'same', filename: 'a.js', lineno: 1, colno: 1 }); assert.equal(d.calls.length, 1);
});

await check('offline: a rejecting fetch is swallowed, so no unhandled rejection and no re-entrant loop (regression)', async () => {
  let unhandled = 0; const h = () => { unhandled++; }; process.on('unhandledRejection', h);
  try {
    const r = load({ fetchImpl: () => Promise.reject(new TypeError('Failed to fetch')) });
    for (let i = 0; i < 3; i++) r.fire('error', { message: `offline ${i}`, filename: 'a.js' });
    await new Promise((res) => setTimeout(res, 50));
    assert.equal(unhandled, 0, 'the failed report surfaced as an unhandled rejection');
    const sync = load({ fetchImpl: () => { throw new Error('sync fail'); } });
    assert.doesNotThrow(() => sync.fire('error', { message: 'x' }));
  } finally { process.off('unhandledRejection', h); }
});

await check('noise is ignored: empty, cross-origin "Script error.", WebSocket and vite dev errors', () => {
  const r = load();
  for (const m of ['', 'Script error.', 'WebSocket closed', 'vite hmr failed']) r.fire('error', { message: m });
  r.fire('unhandledrejection', { reason: { message: 'x', stack: 'at vite/client' } });
  assert.equal(r.calls.length, 0);
});

await check('oversized messages and stacks are truncated client-side so they cannot trip the 10 KB server limit', () => {
  const r = load(); r.fire('error', { message: 'm'.repeat(100_000), filename: 'f'.repeat(100_000), error: { stack: 's'.repeat(100_000) } });
  assert.ok(JSON.stringify(r.calls[0].body).length < 4000);
});

await check('malformed events never make the reporter throw', () => {
  const r = load();
  for (const e of [undefined, null, {}, { message: 5 }, { error: 7 }, { message: { a: 1 }, error: { stack: 3 } }]) assert.doesNotThrow(() => r.fire('error', e));
  for (const e of [undefined, null, {}, { reason: { stack: 1 } }]) assert.doesNotThrow(() => r.fire('unhandledrejection', e));
});

console.log(`\n=== ${passed} passed ===`);
