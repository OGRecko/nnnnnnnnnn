import assert from 'node:assert/strict';
import { ReportAbortedError, pdfReportRenderer } from './reportRenderer';
import type { ReportBuildInput } from './reportInput';

let passed = 0;
async function check(name: string, fn: () => void | Promise<void>) { try { await fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== reportRenderer (real PDFKit) ===\n');

const input = (o: Partial<ReportBuildInput> = {}): ReportBuildInput => ({
  projectName: 'Test project', roomName: 'Hall', simulationId: '11111111-1111-4111-8111-111111111111',
  room: { L: 8, W: 5, H: 3, wallMaterial: 'drywall', floorMaterial: 'wood_floor', ceilMaterial: 'stonewool' },
  speakers: [{ brand: 'JBL', model: 'LSR32', x: .2, y: .5 }], receivers: [{ name: 'R1', x: .8, y: .5 }],
  solverResult: { receivers: [{ id: 'r0', metrics: { rt60: 0.6 } }] }, ...o,
});

await check('renders a real, well-formed PDF (header, EOF marker, non-trivial size)', async () => {
  const pdf = await pdfReportRenderer(input());
  assert.ok(Buffer.isBuffer(pdf)); assert.equal(pdf.subarray(0, 5).toString('latin1'), '%PDF-');
  assert.match(pdf.subarray(-32).toString('latin1'), /%%EOF\s*$/); assert.ok(pdf.length > 1500, `${pdf.length} bytes`);
});

await check('a pre-aborted signal rejects ReportAbortedError without rendering', async () => {
  const c = new AbortController(); c.abort();
  await assert.rejects(pdfReportRenderer(input(), c.signal), (e: any) => e instanceof ReportAbortedError && e.name === 'ReportAbortedError');
});

await check('malformed speaker/receiver entries fall back to defaults instead of crashing', async () => {
  const pdf = await pdfReportRenderer(input({ speakers: [{ brand: 5, x: 'a' } as any, {} as any], receivers: [{ name: null, x: NaN } as any, {} as any] }));
  assert.equal(pdf.subarray(0, 5).toString('latin1'), '%PDF-');
});

await check('hostile text (control chars, very long names, markup, unicode) renders without crashing or being treated as markup', async () => {
  const evil = '<script>alert(1)</script>\u0000\u202e' + 'A'.repeat(5000) + ' \u{1F4A5} \u0645\u0631\u062d\u0628\u0627';
  const pdf = await pdfReportRenderer(input({ projectName: evil, roomName: evil, speakers: [{ brand: evil, model: evil, x: 0, y: 0 }] }));
  assert.equal(pdf.subarray(0, 5).toString('latin1'), '%PDF-');
});

await check('concurrent renders do not interfere (each gets its own complete document)', async () => {
  const outs = await Promise.all([1, 2, 3, 4].map((i) => pdfReportRenderer(input({ projectName: `P${i}` }))));
  for (const o of outs) { assert.equal(o.subarray(0, 5).toString('latin1'), '%PDF-'); assert.match(o.subarray(-32).toString('latin1'), /%%EOF/); }
});

await check('a generator failure is surfaced as a rejection, never a hang or a crash', async () => {
  await assert.rejects(pdfReportRenderer(input({ room: null as any, solverResult: null as any })));
});

await check('the renderer leaves no listeners on a long-lived AbortSignal after success', async () => {
  const c = new AbortController(); const before = (c.signal as any)[Object.getOwnPropertySymbols(c.signal).find((s) => String(s).includes('events')) as any];
  void before;
  let added = 0, removed = 0; const sig = c.signal; const a = sig.addEventListener.bind(sig), r = sig.removeEventListener.bind(sig);
  sig.addEventListener = ((...x: any[]) => { added++; return (a as any)(...x); }) as any; sig.removeEventListener = ((...x: any[]) => { removed++; return (r as any)(...x); }) as any;
  await pdfReportRenderer(input(), sig);
  assert.equal(added, removed, `leaked ${added - removed} abort listener(s)`);
});

console.log(`\n=== ${passed} passed ===`);
