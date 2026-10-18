import fs from 'node:fs';
import path from 'node:path';
import { countGenericReference, isValidResponsePointTable, parseKnownCurves } from './lib/speakerAuditCore.mjs';

const root = process.cwd();
const data = JSON.parse(fs.readFileSync(path.join(root, 'src/data/speakers.json'), 'utf8'));
const responseSource = fs.readFileSync(path.join(root, 'src/lib/speakerResponse.ts'), 'utf8');
const { ids: knownCurveIds } = parseKnownCurves(responseSource);
const responseModelCounts = countGenericReference(data, knownCurveIds);
const read = (name) => fs.readFileSync(path.join(root, name), 'utf8');
const docs = {
  audit: read('AUDIT.md'),
  final: read('FINAL_VERIFICATION.md'),
  status: read('SPEAKER-DATA-STATUS.md'),
  gaps: read('SPEAKER-DATA-GAPS.md'),
  queue: read('scripts/research/RESEARCH-QUEUE.md'),
};
const issues = [];
const fields = ['sensitivity','power','impedance','resonantFreq','voiceCoil','woofer'];
const count = (f) => data.filter((s) => s?.[f]?.value !== null && s?.[f]?.value !== undefined).length;
const frCount = data.filter((s) => Number.isFinite(s?.frequencyResponse?.low_hz) || Number.isFinite(s?.frequencyResponse?.high_hz)).length;
const responseCurves = data.filter((s) => isValidResponsePointTable(s?.frequencyResponse));
const curveCounts = {
  total: responseCurves.length,
  manufacturer: responseCurves.filter((s) => s.frequencyResponse.pointsSourceType === 'MANUFACTURER').length,
  measurement: responseCurves.filter((s) => s.frequencyResponse.pointsSourceType === 'MEASUREMENT').length,
  reputableDatabase: responseCurves.filter((s) => s.frequencyResponse.pointsSourceType === 'REPUTABLE_DATABASE').length,
};
const modeledFromLimits = responseModelCounts.modeledFromPublishedLimits;
const sourced = (s) => fields.some((f) => s?.[f]?.value !== null && s?.[f]?.value !== undefined) || Number.isFinite(s?.frequencyResponse?.low_hz) || Number.isFinite(s?.frequencyResponse?.high_hz);
const status = {};
for (const s of data) status[s.overallStatus ?? 'UNSPECIFIED'] = (status[s.overallStatus ?? 'UNSPECIFIED'] ?? 0) + 1;
const expected = {
  records: data.length,
  uniqueIds: new Set(data.map((s) => s.id)).size,
  uniqueBrandModels: new Set(data.map((s) => `${s.brand}::${s.model}`.toLowerCase())).size,
  sensitivity: count('sensitivity'), power: count('power'), impedance: count('impedance'),
  resonantFreq: count('resonantFreq'), voiceCoil: count('voiceCoil'), woofer: count('woofer'), frequencyResponse: frCount,
  partial: status.PARTIALLY_VERIFIED ?? 0,
  unverified: status.UNVERIFIED ?? 0,
  unavailable: status.UNAVAILABLE ?? 0,
  anySource: data.filter(sourced).length,
  noSource: data.filter((s) => !sourced(s) && s.overallStatus !== 'UNAVAILABLE').length,
  generic: responseModelCounts.total,
  modeledFromLimits,
  responseCurves: curveCounts,
  physicallyModeledResponseModels: data.length - curveCounts.total,
};
if (expected.uniqueIds !== expected.records) issues.push(`duplicate IDs: ${expected.records - expected.uniqueIds}`);
if (expected.uniqueBrandModels !== expected.records) issues.push(`duplicate brand/model pairs: ${expected.records - expected.uniqueBrandModels}`);
// Queue membership is field-level: a record with any live CITED_IN_NOTES_UNCHECKED,
// UNSOURCED or missing provenance field is still queued even though every record's
// overallStatus is PARTIALLY_VERIFIED. This keeps the summary from printing zero.
const queueInventory = JSON.parse(fs.readFileSync(path.join(root, 'scripts/research/field-provenance-inventory.json'), 'utf8')).entries;
const backlogStates = new Set(['CITED_IN_NOTES_UNCHECKED', 'UNSOURCED', 'NO_PROVENANCE']);
const backlogIds = new Set(queueInventory.filter((e) => e.location === 'LIVE' && backlogStates.has(e.storedStatus)).map((e) => e.speakerId));
const queueRecords = data.filter((s) => backlogIds.has(s.id));
const queueStatusCounts = {
  unverified: data.filter((s) => s.overallStatus === 'UNVERIFIED').length,
  unavailable: data.filter((s) => s.overallStatus === 'UNAVAILABLE').length,
};
const queueBrandCount = new Set(queueRecords.map((s) => s.brand)).size;
const expectedQueueSummary = `Records still needing research: **${queueRecords.length}** of ${data.length} (${queueStatusCounts.unverified} UNVERIFIED, ${queueStatusCounts.unavailable} UNAVAILABLE) across ${queueBrandCount} brands.`;

const needles = [
  ['AUDIT speaker-quality gate', `- ` + '`node scripts/speaker-quality-audit.mjs`' + ` — **PASS**, ${expected.records} records, ${expected.records - expected.uniqueIds} duplicate IDs, ${expected.records - expected.uniqueBrandModels} duplicate brand/model pairs, ${expected.responseCurves.total} embedded response-point datasets (${expected.responseCurves.manufacturer} manufacturer, ${expected.responseCurves.measurement} measurement), no category-based response synthesis.`, docs.audit],
  ['AUDIT records', `- ${expected.records} records`, docs.audit],
  ['AUDIT sensitivity', `sensitivity ${expected.sensitivity}`, docs.audit],
  ['AUDIT power', `power ${expected.power}`, docs.audit],
  ['AUDIT impedance', `impedance ${expected.impedance}`, docs.audit],
  ['AUDIT resonant', `resonant frequency ${expected.resonantFreq}`, docs.audit],
  ['AUDIT voice', `voice-coil size ${expected.voiceCoil}`, docs.audit],
  ['AUDIT woofer', `woofer size ${expected.woofer}`, docs.audit],
  ['AUDIT fr', `frequency-response limits ${expected.frequencyResponse}`, docs.audit],
  ['AUDIT partial', `\`PARTIALLY_VERIFIED\`: ${expected.partial}`, docs.audit],
  ['AUDIT unverified', `\`UNVERIFIED\`: ${expected.unverified}`, docs.audit],
  ['AUDIT unavailable', `\`UNAVAILABLE\`: ${expected.unavailable}`, docs.audit],
  ['STATUS partial', `- PARTIALLY_VERIFIED: ${expected.partial}`, docs.status],
  ['STATUS unverified', `- UNVERIFIED: ${expected.unverified}`, docs.status],
  ['STATUS unavailable', `- UNAVAILABLE: ${expected.unavailable}`, docs.status],
  ['STATUS sensitivity', `- Sensitivity: ${expected.sensitivity}`, docs.status],
  ['STATUS power', `- Power: ${expected.power}`, docs.status],
  ['STATUS impedance', `- Impedance: ${expected.impedance}`, docs.status],
  ['STATUS resonant', `- Resonant frequency: ${expected.resonantFreq}`, docs.status],
  ['STATUS voice', `- Voice-coil size: ${expected.voiceCoil}`, docs.status],
  ['STATUS woofer', `- Woofer size: ${expected.woofer}`, docs.status],
  ['STATUS fr', `- Frequency-response limits: ${expected.frequencyResponse}`, docs.status],
  ['STATUS generic', `- Generic reference models with missing published bounds: ${expected.generic}`, docs.status],
  ['STATUS response points', `- Embedded source-backed response-point datasets: ${expected.responseCurves.total} (measurement ${expected.responseCurves.measurement}, manufacturer ${expected.responseCurves.manufacturer}, reputable database ${expected.responseCurves.reputableDatabase})`, docs.status],
  ['STATUS modeled limits', `- Models derived from published frequency limits: ${expected.modeledFromLimits}`, docs.status],
  ['AUDIT embedded response points', `- embedded JSON response-point datasets: ${expected.responseCurves.total}`, docs.audit],
  ['AUDIT modeled response models', `- physically modeled response models: ${expected.physicallyModeledResponseModels}`, docs.audit],
  ['FINAL partial', `- PARTIALLY_VERIFIED: ${expected.partial}`, docs.final],
  ['FINAL unverified', `- UNVERIFIED: ${expected.unverified}`, docs.final],
  ['FINAL unavailable', `- UNAVAILABLE: ${expected.unavailable}`, docs.final],
  ['FINAL sensitivity', `sensitivity ${expected.sensitivity}`, docs.final],
  ['FINAL power', `power ${expected.power}`, docs.final],
  ['FINAL impedance', `impedance ${expected.impedance}`, docs.final],
  ['FINAL resonant', `resonant frequency ${expected.resonantFreq}`, docs.final],
  ['FINAL voice', `voice-coil size ${expected.voiceCoil}`, docs.final],
  ['FINAL woofer', `woofer size ${expected.woofer}`, docs.final],
  ['FINAL fr', `frequency-response limits ${expected.frequencyResponse}`, docs.final],
  ['FINAL response points', `- Source-backed response-point datasets: ${expected.responseCurves.total} (measurement ${expected.responseCurves.measurement}, manufacturer ${expected.responseCurves.manufacturer}, reputable database ${expected.responseCurves.reputableDatabase}).`, docs.final],
  ['FINAL response model composition', `- Response models: ${expected.records}; ${expected.modeledFromLimits} are modeled from published response limits, ${expected.generic} use the generic reference path, and ${expected.responseCurves.total} use source-backed response-point datasets.`, docs.final],
];
for (const [name, needle, body] of needles) if (!body.includes(needle)) issues.push(`${name}: missing ${needle}`);
if (!docs.queue.includes(expectedQueueSummary)) issues.push(`research queue summary is stale: expected ${expectedQueueSummary}`);
const queueIds = new Set([...docs.queue.matchAll(/\(`([^`]+)`\)/g)].map((m) => m[1]));
const expectedQueueIds = new Set(queueRecords.map((s) => s.id));
for (const id of expectedQueueIds) if (!queueIds.has(id)) issues.push(`research queue is missing ${id}`);
for (const id of queueIds) if (!expectedQueueIds.has(id)) issues.push(`research queue has unexpected ${id}`);
const old = ['Sensitivity: 39','Power: 64','Impedance: 43','Voice-coil size: 4','Woofer size: 64','Frequency-response limits: 71','PARTIALLY_VERIFIED: 772','embedded JSON response curves: 0','Embedded measured/manufacturer response curves: 0','physically modeled response models: 774'];
for (const stale of old) {
  // Stale counts require a numeric-token boundary so a valid newer count (e.g. 40) does not match 4.
  const stalePattern = new RegExp(`${stale}(?![0-9])`);
  if (Object.values(docs).some((body) => stalePattern.test(body))) issues.push(`stale documentation token: ${stale}`);
}
if (!docs.gaps.includes(`**Records with no source-backed acoustic field:** ${expected.noSource}`)) issues.push('speaker gap inventory total is stale');
const rowCount = (docs.gaps.match(/^\| [^|]+ \|/gm) || []).length - 1;
if (rowCount !== expected.records) issues.push(`speaker gap inventory rows: expected ${expected.records}, found ${rowCount}`);

// Release-version and Node-pin consistency (single source of truth: package.json).
{
  const pkg = JSON.parse(read('package.json'));
  const lock = JSON.parse(read('package-lock.json'));
  const manifest = JSON.parse(read('source-release/manifest.json'));
  const versionTs = /APP_VERSION\s*=\s*["']([^"']+)["']/.exec(read('src/lib/version.ts'))?.[1];
  if (lock.version !== pkg.version || lock.packages?.['']?.version !== pkg.version) issues.push(`package-lock version ${lock.version} != package.json ${pkg.version}`);
  if (manifest.version !== pkg.version) issues.push(`source-release manifest version ${manifest.version} != ${pkg.version}`);
  if (versionTs !== pkg.version) issues.push(`src/lib/version.ts APP_VERSION ${versionTs} != ${pkg.version}`);
  if (!docs.final.includes(`**Product:** Cavity Audio ${pkg.version}`)) issues.push('FINAL_VERIFICATION product version is stale');
  const minor = pkg.version.split('.').slice(0, 2).join('.');
  if (!read('SECURITY.md').includes(`\`${minor}.x\` release line`)) issues.push(`SECURITY.md supported release line is not ${minor}.x`);
  const pin = read('.nvmrc').trim();
  if (pkg.engines?.node !== `>=${pin} <23`) issues.push(`engines.node ${pkg.engines?.node} does not match .nvmrc ${pin}`);
  for (const f of fs.readdirSync(path.join(root, '.github/workflows'))) {
    for (const m of read(`.github/workflows/${f}`).matchAll(/node-version:\s*([0-9.]+)/g)) if (m[1] !== pin) issues.push(`${f} node-version ${m[1]} != .nvmrc ${pin}`);
  }
  // Live speaker count must never be hardcoded to a stale number in prose docs.
  for (const [n, body] of Object.entries({README: read('README.md'), metadata: read('metadata.json')})) {
    for (const m of body.matchAll(/\b(\d{3})[- ]speaker/gi)) if (Number(m[1]) !== data.length) issues.push(`${n} states ${m[1]} speakers; live DB has ${data.length}`);
  }
}

// Crash-reporting opt-out must be documented wherever the privacy policy is published, and match the client code.
{
  const optKey = /localStorage\.getItem\('([^']+)'\) === 'off'/.exec(read('public/error-reporter.js'))?.[1];
  if (!optKey) issues.push('public/error-reporter.js has no localStorage opt-out');
  for (const f of ['PRIVACY.md', 'public/privacy.html']) {
    if (optKey && !read(f).includes(optKey)) issues.push(`${f} does not document the error-report opt-out key ${optKey}`);
    if (!/Do Not Track/i.test(read(f))) issues.push(`${f} does not document the Do Not Track opt-out`);
  }
}

// Archived-speaker index and the saved-project doc are generated; stale or contradictory copies must fail CI.
{
  const { spawnSync } = await import('node:child_process');
  for (const script of ['scripts/generate-archived-speaker-index.mjs', 'scripts/generate-speaker-reference-doc.mjs']) {
    const r = spawnSync(process.execPath, [script, '--check'], { cwd: root, encoding: 'utf8' });
    if (r.status !== 0) issues.push(`${script} --check failed: ${(r.stderr || r.stdout).trim().split('\n')[0]}`);
  }
}

// DIRECTIVITY-IMPORT.md must state the shared limits exactly as defined in publicLimits.ts, and the known limitation.
{
  const lim = read('src/lib/publicLimits.ts');
  const get = (k) => (new RegExp('\\b' + k + ':\\s*(-?[0-9_]+)').exec(lim) || [])[1]?.replace(/_/g, '');
  const text = read('DIRECTIVITY-IMPORT.md');
  const m = /At most (\d+) frequencies, (\d+) directions .*? frequencies up to (\d+) Hz, and normalised magnitudes between (-?\d+) and (-?\d+) dB/.exec(text);
  if (!m) issues.push('DIRECTIVITY-IMPORT.md limits sentence not found');
  else {
    const want = [get('MAX_FREQUENCIES'), get('MAX_POINTS'), get('MAX_FREQUENCY_HZ'), get('MIN_MAGNITUDE_DB'), get('MAX_MAGNITUDE_DB')];
    const names = ['max frequencies', 'max directions', 'max frequency Hz', 'min magnitude dB', 'max magnitude dB'];
    names.forEach((n, i) => { if (want[i] === undefined) issues.push(`could not read ${n} from publicLimits.ts`); else if (m[i + 1] !== want[i]) issues.push(`DIRECTIVITY-IMPORT.md says ${n} = ${m[i + 1]}, publicLimits.ts says ${want[i]}`); });
  }
  if (!/Known limitation/.test(text) || !/Experimental/i.test(text)) issues.push('DIRECTIVITY-IMPORT.md must state the known limitation and the experimental status');
  if (!/validate:directivity/.test(text) || !read('package.json').includes('"validate:directivity"')) issues.push('validate:directivity must exist and be documented');
}

// The measured directivity numbers quoted in DIRECTIVITY-IMPORT.md and FINAL_VERIFICATION.md must match the latest measurement file.
{
  if (!fs.existsSync(path.join(root, 'directivity-fidelity-results.json'))) issues.push('directivity-fidelity-results.json is missing; run npm run validate:directivity');
  else {
    const f = JSON.parse(read('directivity-fidelity-results.json'));
    const doc = read('DIRECTIVITY-IMPORT.md');
    const row = (label) => new RegExp('\\| ' + label + ' \\| ([+-]?\\d+\\.\\d+) dB \\|').exec(doc)?.[1];
    for (const [label, key] of [['Omnidirectional baseline', 'omniDb'], ['Aimed forward', 'forwardDb'], ['Aimed backward', 'backwardDb']]) {
      const v = row(label);
      if (v === undefined) issues.push(`DIRECTIVITY-IMPORT.md table row "${label}" not found`);
      else if (Math.abs(Number(v) - f[key]) > 0.011) issues.push(`DIRECTIVITY-IMPORT.md says ${label} = ${v} dB; latest measurement is ${f[key]} dB`);
    }
    if (!f.pass && !/Open gates[\s\S]*Directivity fidelity: \*\*FAIL\*\*/.test(read('FINAL_VERIFICATION.md'))) issues.push('FINAL_VERIFICATION.md must list the failing directivity fidelity gate under Open gates');
    if (f.pass && /Directivity fidelity: \*\*FAIL\*\*/.test(read('FINAL_VERIFICATION.md'))) issues.push('FINAL_VERIFICATION.md still reports directivity fidelity as FAIL');
  }
}
console.log(JSON.stringify({ok: issues.length === 0, expected, issues}, null, 2));
process.exitCode = issues.length ? 1 : 0;
