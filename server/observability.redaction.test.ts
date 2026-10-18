import assert from 'node:assert/strict';
import { redactString, redactValue } from './observability';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== observability redaction ===\n');

check('IPv6 forms are redacted: full, compressed, loopback, leading/trailing ::, v4-mapped', () => {
  for (const ip of ['2001:0db8:85a3:0000:0000:8a2e:0370:7334', '2001:db8:85a3::8a2e:370:7334', '2001:db8::1', '::1', 'fe80::1', '::', '2001:db8::', '::ffff:192.0.2.128']) {
    const out = redactString(`client ${ip} failed`);
    assert.ok(!/db8|fe80|::1\b|192\.0\.2/.test(out) || ip === '::', `${ip} -> ${out}`);
  }
  assert.ok(!redactString('x 2001:db8:85a3::8a2e:370:7334 y').includes('8a2e'));
});

check('ordinary text is NOT mangled by the IPv6 rule (code scopes, clock times, hex words, ratios)', () => {
  for (const t of ['std::add failed', 'Foo::bar::baz', 'at 12:34:56 today', 'ratio 3:2', 'ab:cd', 'time 09:15', 'cafe:babe is not an address', 'a.b::c', 'key:value']) {
    assert.equal(redactString(t), t, t);
  }
});

check('e-mail addresses are redacted; plain @ text is not', () => {
  assert.ok(!redactString('mail george.p+tag@sub.example.co.uk now').includes('george'));
  assert.equal(redactString('mail me @ noon'), 'mail me @ noon');
  assert.equal(redactString('@mention only'), '@mention only');
});

check('OS account names in paths are redacted on Windows, macOS and Linux; the rest of the path survives', () => {
  const win = redactString('C:\\Users\\GeorgeP\\AppData\\Roaming\\Cavity\\x.js:10:5');
  assert.ok(!win.includes('GeorgeP') && win.includes('AppData\\Roaming\\Cavity\\x.js'), win);
  const fileUrl = redactString('file:///C:/Users/GeorgeP/app/main.js');
  assert.ok(!fileUrl.includes('GeorgeP') && fileUrl.endsWith('/app/main.js'), fileUrl);
  const mac = redactString('/Users/georgep/Library/x.js'); assert.ok(!mac.includes('georgep') && mac.endsWith('/Library/x.js'), mac);
  const lin = redactString('at f (/home/georgep/app/y.js:1:1)'); assert.ok(!lin.includes('georgep') && lin.includes('/app/y.js'), lin);
  assert.equal(redactString('/usr/lib/node_modules/x.js'), '/usr/lib/node_modules/x.js');
});

check('tokens, bearer values, keys, private keys and 64-hex strings are redacted', () => {
  const hex = 'ab'.repeat(32);
  const out = redactString(`t=${hex} Bearer abc.DEF-123 AIza${'q'.repeat(35)} ya29.${'w'.repeat(30)} password=hunter2 -----BEGIN PRIVATE KEY-----\nMIIE\n-----END PRIVATE KEY-----`);
  for (const leak of [hex, 'abc.DEF-123', 'AIzaqqqq', 'ya29.www', 'hunter2', 'MIIE']) assert.ok(!out.includes(leak), `${leak} leaked: ${out}`);
});

check('sensitive KEYS are redacted whatever their value; nesting is depth- and size-bounded', () => {
  const v: any = redactValue({ authToken: 'x', Authorization: 'y', cookie: 'z', api_key: 'k', client_email: 'e', safe: 'ok', deep: { a: { b: { c: { d: { e: { f: { g: 'deep' } } } } } } } });
  for (const k of ['authToken', 'Authorization', 'cookie', 'api_key', 'client_email']) assert.equal(v[k], '[REDACTED]', k);
  assert.equal(v.safe, 'ok');
  assert.equal(JSON.stringify(v).includes('"deep":"deep"'), false);
  assert.equal((redactValue(Array.from({ length: 500 }, (_, i) => i)) as unknown[]).length, 50);
  assert.equal((redactValue('x'.repeat(9999)) as string).length, 2000);
});

check('redaction is idempotent and never throws on odd input', () => {
  const once = redactString('mail a@b.co from 2001:db8::1 at 10.0.0.1');
  assert.equal(redactString(once), once);
  for (const x of [null, undefined, 0, NaN, {}, [], Symbol.iterator.toString(), '\u0000', 'a'.repeat(200_000)]) assert.doesNotThrow(() => redactValue(x));
});

check('worst-case input does not cause catastrophic regex backtracking', () => {
  const t = Date.now();
  redactString(('a1:'.repeat(20_000)) + ':' + 'f'.repeat(50_000));
  redactString('a@' + 'b'.repeat(50_000));
  redactString('C:\\Users\\' + 'x'.repeat(100_000));
  assert.ok(Date.now() - t < 2000, `took ${Date.now() - t} ms`);
});

console.log(`\n=== ${passed} passed ===`);
