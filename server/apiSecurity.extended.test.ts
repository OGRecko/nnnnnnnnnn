/**
 * Extended black-box API security suite (complements apiSecurity.blackbox.test.ts).
 * Real createApi() over real loopback HTTP; only persistence/admission are in-memory fakes.
 * Covers: Origin/CSRF enforcement, raw path normalisation tricks, prototype-pollution bodies, header abuse,
 * log injection + PII/secret redaction, and per-IP rate limiting including X-Forwarded-For spoofing.
 */
import assert from 'node:assert/strict';
import http from 'node:http';
import net from 'node:net';
import { createApi } from './api';
import { hashCapabilityToken } from './capabilityToken';
import { LIMITS } from '../src/lib/publicLimits';
import { resetLogSinks, setLogSinks } from './observability';
import type { JobRecord } from './jobStore';
import { MemoryArtifactStore } from './testing/memoryArtifactStore';

const ORIGIN = 'https://app.example.test';
const mk = (c: string) => `${c.repeat(8)}-${c.repeat(4)}-4${c.repeat(3)}-8${c.repeat(3)}-${c.repeat(12)}`;
const A = { sim: mk('a'), job: mk('b'), token: 'a1'.repeat(32) };
const records = new Map<string, JobRecord>([[A.sim, {
  simulationId: A.sim, jobId: A.job, type: 'impulse-response', status: 'completed', capabilityTokenHash: hashCapabilityToken(A.token),
  createdAt: Date.now(), updatedAt: Date.now(), leaseOwner: null, leaseEpoch: 1, leaseUntil: 0, recoveryAttempts: 0,
  room: { L: 4, W: 4, H: 3 }, speakers: [{ x: .5, y: .5, z: 1.5 }], receivers: [{ x: .5, y: .5, z: 1.5 }], result: { receivers: [] }, artifacts: [],
} as any]]);
let created = 0;
const store: any = {
  async createQueued(i: any) { if (records.has(i.simulationId)) return false; created++; records.set(i.simulationId, { ...i, status: 'queued', updatedAt: i.createdAt, leaseOwner: null, leaseEpoch: 0, leaseUntil: 0, recoveryAttempts: 0 }); return true; },
  async get(id: string) { return records.get(id) ?? null; },
  async getByJobId(id: string) { return [...records.values()].find((r) => r.jobId === id) ?? null; },
  async cancel(id: string) { const r = records.get(id); if (!r) return { ok: false }; r.status = 'cancelled'; return { ok: true, alreadyFinished: false, status: 'cancelled' }; },
  async forEachCreatedBefore() {}, async deleteIfTerminal() { return 'missing'; }, async recover() { return 'skipped'; },
};
let admissionAllows = true;
const admission: any = {
  async rateLimit() { return { allowed: admissionAllows, retryAfterSeconds: 7 }; }, async acquireSlot() { return { ok: true, slotId: 's' }; },
  async releaseSlot() {}, async isRateLimited() { return false; }, async purgeExpiredRateLimits() { return 0; },
};
const artifacts = new MemoryArtifactStore();
let clockOffsetMs = 0;
const nextWindow = () => { clockOffsetMs += 60_000; };
const mkApi = (config: any) => createApi({
  now: () => Date.now() + clockOffsetMs, store, artifacts, admission, dispatcher: { enqueue() { return true; }, cancelLocal() {} } as any,
  metrics: { inc() {}, snapshot() { return {}; } } as any, renderReport: async () => Buffer.from('%PDF-1.4 x'),
  cleanup: { store, artifacts, admission, metrics: { inc() {} } as any }, cloudTasks: { authorize() { return false; }, async enqueue() { return true; } },
  config: { trustProxy: false, cleanupSecret: 'd'.repeat(32), allowedOrigin: null, ...config },
});
const listen = async (api: ReturnType<typeof createApi>) => {
  const s = http.createServer((q, r) => { void api(q, r).then((h) => { if (!h) { r.statusCode = 404; r.end(); } }).catch(() => { if (!r.headersSent) { r.statusCode = 500; r.end(); } }); });
  await new Promise<void>((ok) => s.listen(0, '127.0.0.1', () => ok()));
  return { s, port: (s.address() as net.AddressInfo).port };
};
const strict = await listen(mkApi({ allowedOrigin: ORIGIN }));
const open = await listen(mkApi({ allowedOrigin: null }));
const proxied = await listen(mkApi({ trustProxy: 1 }));

/** Raw HTTP so the client cannot normalise or reject hostile request lines. */
function raw(port: number, reqLine: string, headers: string[] = [], body = ''): Promise<{ status: number; head: string; body: string }> {
  return new Promise((resolve, reject) => {
    const sock = net.connect(port, '127.0.0.1');
    let buf = '';
    sock.setTimeout(5000, () => { sock.destroy(); reject(new Error('timeout')); });
    sock.on('data', (d) => { buf += d.toString('latin1'); });
    sock.on('error', reject);
    sock.on('close', () => { const [head, ...rest] = buf.split('\r\n\r\n'); resolve({ status: Number(/^HTTP\/1\.1 (\d+)/.exec(head)?.[1] ?? 0), head, body: rest.join('\r\n\r\n') }); });
    sock.write([reqLine, 'Host: 127.0.0.1', 'Connection: close', ...headers, ...(body ? [`Content-Length: ${Buffer.byteLength(body)}`] : []), '', body].join('\r\n'));
  });
}
const goodWave = () => ({ L: 4, W: 4, H: 3, steps: 1, wallMaterial: 'drywall', floorMaterial: 'wood_floor', ceilMaterial: 'stonewool', sources: [{ x: .5, y: .5, z: 1.5 }], receivers: [{ x: 1, y: 1, z: 1.5 }] });
const J = 'Content-Type: application/json';

let passed = 0;
async function check(name: string, fn: () => Promise<void>) {
  try { await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; }
}
console.log('\n=== Extended API security (black-box) ===\n');
// The API logs every queued job / client error as JSON; keep the test output readable. Checks that assert on logs install their own sinks.
setLogSinks(() => {}, () => {});

try {
  await check('Origin enforcement: a foreign, "null", trailing-slash or scheme-variant Origin on POST/DELETE => 403 and nothing is created', async () => {
    const before = created;
    for (const o of ['https://evil.example', 'null', `${ORIGIN}/`, 'http://app.example.test', 'https://app.example.test.evil.example', ORIGIN.toUpperCase(), '']) {
      for (const [m, p] of [['POST', '/api/solver/impulse-response'], ['POST', '/api/report/export'], ['DELETE', `/api/jobs/${A.job}`]] as const) {
        const r = await raw(strict.port, `${m} ${p} HTTP/1.1`, [`Origin: ${o}`, J, `Authorization: Bearer ${A.token}`], m === 'POST' ? JSON.stringify(goodWave()) : '');
        assert.equal(r.status, 403, `${m} ${p} with Origin "${o}" got ${r.status}`);
      }
    }
    assert.equal(created, before, 'a refused cross-origin request must not create a job');
    assert.notEqual(records.get(A.sim)!.status, 'cancelled', 'a refused cross-origin DELETE must not cancel');
  });

  await check('Origin enforcement: the exact allowed origin and requests with no Origin (non-browser clients) are not blocked by the origin gate', async () => {
    nextWindow();
    const ok = await raw(strict.port, 'POST /api/solver/impulse-response HTTP/1.1', [`Origin: ${ORIGIN}`, J], JSON.stringify(goodWave()));
    assert.ok(ok.status !== 403, `allowed origin rejected: ${ok.status}`);
    const none = await raw(strict.port, 'POST /api/log-error HTTP/1.1', [J], JSON.stringify({ message: 'x' }));
    assert.equal(none.status, 200);
  });

  await check('path normalisation tricks never reach a route or leak files', async () => {
    const paths = ['/api/../package.json', '/api/%2e%2e/package.json', '/api/..%2fpackage.json', '/api//health', '/api/health/', '/API/health', '/api/health%00', '/api/health%2f..%2f..%2fetc%2fpasswd',
      '/api/jobs/%2e%2e%2fhealth', '/api/jobs/..%5chealth', '/api/jobs/%00', '/api/jobs/' + 'a'.repeat(5000), '/api/' + 'x/'.repeat(2000), '/api/storage?key=../../etc/passwd', '/api/storage?key=%2e%2e%2f%2e%2e%2fetc%2fpasswd'];
    for (const p of paths) {
      const r = await raw(open.port, `GET ${p} HTTP/1.1`);
      assert.ok(r.status >= 400 && r.status < 500 || p === '/api/health/' && r.status < 500, `${p} -> ${r.status}`);
      assert.ok(!/root:|"dependencies"|"scripts"/.test(r.body), `leaked file content via ${p}`);
    }
    const ok = await raw(open.port, 'GET /api/health HTTP/1.1');
    assert.equal(ok.status, 200);
  });

  await check('prototype-pollution bodies never pollute Object.prototype and never cause a 5xx', async () => {
    nextWindow();
    const polluted = (s: string) => assert.equal(({} as any).polluted, undefined, s);
    const bodies = [
      `{"__proto__":{"polluted":true},${JSON.stringify(goodWave()).slice(1)}`,
      `{"constructor":{"prototype":{"polluted":true}},${JSON.stringify(goodWave()).slice(1)}`,
      JSON.stringify({ ...goodWave(), sources: [{ x: .5, y: .5, z: 1.5, '__proto__': { polluted: true } }] }),
      `{"sources":[{"__proto__":{"polluted":true},"x":0.5,"y":0.5,"z":1.5}],"receivers":[{"x":1,"y":1,"z":1.5}],"L":4,"W":4,"H":3}`,
    ];
    for (const b of bodies) {
      for (const p of ['/api/solver/impulse-response', '/api/solver/wave', '/api/report/export', '/api/log-error']) {
        const r = await raw(open.port, `POST ${p} HTTP/1.1`, [J], b);
        assert.ok(r.status < 500, `${p} 5xx on pollution body: ${r.status}`);
        polluted(p);
      }
    }
  });

  await check('method override / smuggling headers are ignored', async () => {
    const r = await raw(open.port, `POST /api/jobs/${A.job} HTTP/1.1`, ['X-HTTP-Method-Override: DELETE', 'X-Method-Override: DELETE', `Authorization: Bearer ${A.token}`]);
    assert.equal(r.status, 405);
    assert.notEqual(records.get(A.sim)!.status, 'cancelled');
    const both = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J, 'Transfer-Encoding: chunked'], '0\r\n\r\n');
    assert.ok(both.status < 500, `chunked+length confusion -> ${both.status}`);
  });

  await check('responses are never cacheable and never sniffable', async () => {
    for (const p of ['/api/health', '/api/nope', `/api/jobs/${A.job}`]) {
      const r = await raw(open.port, `GET ${p} HTTP/1.1`);
      assert.match(r.head, /cache-control: no-store/i, p);
      assert.match(r.head, /x-content-type-options: nosniff/i, p);
    }
  });

  await check('log-error: log-line injection is impossible (one JSON line per report, control chars escaped)', async () => {
    nextWindow();
    const lines: string[] = [];
    setLogSinks((l) => lines.push(l), (l) => lines.push(l));
    try {
      const evil = 'boom\n{"severity":"CRITICAL","event":"forged"}\r\n\u2028second';
      const r = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], JSON.stringify({ message: evil, location: 'a\nb', stack: 'c\nd' }));
      assert.equal(r.status, 200);
      assert.equal(lines.length, 1, 'exactly one log line per report');
      assert.ok(!/[\r\n]/.test(lines[0]), 'raw newline in a log line');
      const parsed = JSON.parse(lines[0]);
      assert.equal(parsed.event, 'client_error', 'the client must not be able to forge the event name');
      assert.ok(!('forged' in parsed) && parsed.severity === 'INFO');
    } finally { setLogSinks(() => {}, () => {}); }
  });

  await check('log-error: secrets and PII in a report are redacted (tokens, bearer, keys, IPv4, IPv6, e-mail, OS user names in paths)', async () => {
    nextWindow();
    const lines: string[] = [];
    setLogSinks((l) => lines.push(l), (l) => lines.push(l));
    try {
      const secrets = {
        hex64: 'ab'.repeat(32), bearer: 'Bearer abc.def.ghi', gkey: 'AIza' + 'x'.repeat(35), ip4: '203.0.113.9', ip6: '2001:db8:85a3::8a2e:370:7334',
        email: 'george.private@example.com', winUser: 'C:\\Users\\GeorgePrivate\\AppData\\app.js', macUser: '/Users/georgeprivate/app/x.js', linuxUser: '/home/georgeprivate/app/x.js',
      };
      const msg = `crash ${Object.values(secrets).join(' | ')}`;
      const r = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], JSON.stringify({ message: msg, stack: msg, location: msg }));
      assert.equal(r.status, 200);
      const out = lines.join('\n');
      for (const [k, v] of Object.entries(secrets)) {
        const needle = k === 'bearer' ? 'abc.def.ghi' : k === 'winUser' ? 'GeorgePrivate' : k === 'macUser' || k === 'linuxUser' ? 'georgeprivate' : v;
        assert.ok(!out.includes(needle), `${k} leaked into logs: ${needle}`);
      }
    } finally { setLogSinks(() => {}, () => {}); }
  });

  await check('log-error: oversized body => 413, missing/non-string message => 400, never 5xx', async () => {
    nextWindow();
    assert.equal((await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], JSON.stringify({ message: 'x'.repeat(LIMITS.MAX_CLIENT_ERROR_BODY_BYTES + 1) }))).status, 413);
    for (const b of ['{}', '[]', 'null', '"x"', '{"message":123}', '{"message":""}', '{"message":{"a":1}}', '{bad']) {
      const r = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], b);
      assert.ok(r.status === 400, `${b} -> ${r.status}`);
    }
  });

  await check('rate limit: log-error is capped per IP per minute (429 + Retry-After) and recovers next window', async () => {
    nextWindow();
    let first429 = -1;
    for (let i = 0; i < LIMITS.CLIENT_ERROR_REPORTS_PER_IP_PER_MINUTE + 5; i++) {
      const r = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], JSON.stringify({ message: `m${i}` }));
      if (r.status === 429 && first429 < 0) { first429 = i; assert.match(r.head, /retry-after: \d+/i); }
    }
    assert.equal(first429, LIMITS.CLIENT_ERROR_REPORTS_PER_IP_PER_MINUTE, 'limit must trip exactly after the configured number');
    nextWindow();
    assert.equal((await raw(open.port, 'POST /api/log-error HTTP/1.1', [J], '{"message":"again"}')).status, 200);
  });

  await check('rate limit: spoofed X-Forwarded-For does NOT mint new buckets when no proxy is trusted', async () => {
    nextWindow();
    let blocked = 0;
    for (let i = 0; i < LIMITS.CLIENT_ERROR_REPORTS_PER_IP_PER_MINUTE + 8; i++) {
      const r = await raw(open.port, 'POST /api/log-error HTTP/1.1', [J, `X-Forwarded-For: 10.0.${i}.${i}`, `X-Real-IP: 10.1.${i}.${i}`, `Forwarded: for=10.2.${i}.${i}`], '{"message":"spoof"}');
      if (r.status === 429) blocked++;
    }
    assert.ok(blocked >= 8, `spoofed headers bypassed the limiter (only ${blocked} blocked)`);
  });

  await check('rate limit: behind one trusted proxy only the proxy-appended hop counts (client-prepended entries are ignored)', async () => {
    nextWindow();
    let blocked = 0;
    for (let i = 0; i < LIMITS.CLIENT_ERROR_REPORTS_PER_IP_PER_MINUTE + 8; i++) {
      // The real client is 198.51.100.7 (appended by the trusted proxy); everything before it is attacker-controlled.
      const r = await raw(proxied.port, 'POST /api/log-error HTTP/1.1', [J, `X-Forwarded-For: 10.9.${i}.${i}, 198.51.100.7`], '{"message":"p"}');
      if (r.status === 429) blocked++;
    }
    assert.ok(blocked >= 8, `prepended X-Forwarded-For entries minted new buckets (only ${blocked} blocked)`);
    nextWindow();
    const otherClient = await raw(proxied.port, 'POST /api/log-error HTTP/1.1', [J, 'X-Forwarded-For: 198.51.100.8'], '{"message":"p"}');
    assert.equal(otherClient.status, 200, 'a different real client must have its own bucket');
  });

  await check('rate limit: an exhausted submission quota returns 429 with Retry-After and creates no job', async () => {
    nextWindow();
    admissionAllows = false;
    const before = created;
    try {
      const r = await raw(open.port, 'POST /api/solver/impulse-response HTTP/1.1', [J], JSON.stringify(goodWave()));
      assert.equal(r.status, 429);
      assert.match(r.head, /retry-after: \d+/i);
      assert.equal(created, before);
    } finally { admissionAllows = true; }
  });

  await check('internal endpoints: wrong, empty, oversized and duplicated secrets are refused; a job token is not a secret', async () => {
    for (const h of ['X-Cleanup-Secret: ', 'X-Cleanup-Secret: ' + 'd'.repeat(31), 'X-Cleanup-Secret: ' + 'd'.repeat(300), `X-Cleanup-Secret: ${'d'.repeat(32)}x`, `Authorization: Bearer ${A.token}`, 'X-Cleanup-Secret: wrong\r\nX-Cleanup-Secret: ' + 'd'.repeat(32)]) {
      for (const [m, p] of [['POST', '/api/internal/cleanup'], ['GET', '/api/internal/metrics']] as const) {
        const r = await raw(open.port, `${m} ${p} HTTP/1.1`, [h, J], m === 'POST' ? '{}' : '');
        assert.equal(r.status, 403, `${m} ${p} with "${h.slice(0, 40)}" -> ${r.status}`);
      }
    }
  });

  await check('huge or malformed headers and request lines do not crash the server (it stays healthy afterwards)', async () => {
    for (const [line, hs] of [
      ['GET /api/health HTTP/1.1', ['X-Big: ' + 'a'.repeat(40_000)]],
      ['GET /api/health HTTP/1.1', Array.from({ length: 300 }, (_, i) => `X-H${i}: v`)],
      ['GET /api/health HTTP/1.1', ['Authorization: Bearer ' + 'z'.repeat(20_000)]],
      ['GE\u0000T /api/health HTTP/1.1', []],
      ['GET /api/health HTTP/9.9', []],
    ] as Array<[string, string[]]>) {
      try { const r = await raw(open.port, line, hs); assert.ok(r.status === 0 || r.status >= 200 && r.status < 500 || r.status === 431, `${line.slice(0, 30)} -> ${r.status}`); } catch { /* connection reset is an acceptable refusal */ }
    }
    assert.equal((await raw(open.port, 'GET /api/health HTTP/1.1')).status, 200);
  });
} finally {
  for (const x of [strict, open, proxied]) x.s.close();
  console.log(`\n=== ${passed} passed ===`);
}
