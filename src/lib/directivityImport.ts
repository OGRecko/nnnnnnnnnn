/**
 * Import of user-supplied loudspeaker polar (directivity) data: CSV (long or wide) and JSON.
 *
 * What this is NOT: it does not read CLF/CF2, GLL or ULF. CLF2 is a binary, access-controlled format and GLL is
 * proprietary; neither is implemented, and files that look like them are REFUSED with a clear message rather than
 * guessed at. Export to CSV from the tool that produced the file.
 *
 * Everything accepted here is passed through validateDirectivity() (src/lib/publicLimits.ts), the same validator the
 * project loader and the solver API use, so an imported file can never be accepted here and rejected later.
 *
 * Conventions (identical to what the solver uses):
 *  - azimuth 0 deg is the speaker's forward (on-axis) direction; positive azimuth rotates toward the speaker's local +X axis
 *    (+Y forward, +Z up). Azimuth is wrapped to [0, 360). Elevation is positive upward, -90..+90.
 *  - magnitudes are dB. They are normalised per frequency to the on-axis sample (0 deg, 0 deg) so the stored data is
 *    RELATIVE directivity; absolute SPL and sensitivity are not read from the file.
 *  - the data is the user's own and is labelled as imported; it is not catalog data and is not verified by Cavity Audio.
 */
import { DIRECTIVITY_LIMITS, validateDirectivity, type DirectivityDataInput } from './publicLimits';

export const DIRECTIVITY_IMPORT_LIMITS = { MAX_FILE_BYTES: 5 * 1024 * 1024, MAX_LINES: 200_000, MAX_LINE_CHARS: 4000, DUPLICATE_TOLERANCE_DB: 0.1 } as const;
export const OCTAVE_BANDS_HZ = [125, 250, 500, 1000, 2000, 4000, 8000] as const;

export interface DirectivityImportSummary {
  fileName: string;
  format: 'csv-long' | 'csv-wide' | 'json';
  pointCount: number;
  frequenciesHz: number[];
  azimuthCount: number;
  elevationCount: number;
  coverage: 'horizontal-plane-only' | 'partial' | 'full-sphere';
  angularResolutionDeg: number;
  /** Octave bands within half an octave of a supplied frequency (the solver's rule). The rest stay omnidirectional. */
  coveredBandsHz: number[];
  uncoveredBandsHz: number[];
  /** The on-axis level that was subtracted at each frequency (informational). */
  onAxisReferenceDb: number[];
}
export type DirectivityImportResult = { ok: true; data: DirectivityDataInput; summary: DirectivityImportSummary } | { ok: false; error: string };
const tooManyDirections = (n?: number) => `The file has ${n === undefined ? 'more than ' + DIRECTIVITY_LIMITS.MAX_POINTS.toLocaleString('en-US') : n.toLocaleString('en-US')} directions; the limit is ${DIRECTIVITY_LIMITS.MAX_POINTS.toLocaleString('en-US')}. Resample to a coarser grid (5° steps over the full sphere is 2,664 directions).`;
const fail = (error: string): { ok: false; error: string } => ({ ok: false, error });

const REFUSED_EXTENSIONS: Record<string, string> = {
  '.gll': 'GLL files are proprietary and cannot be read here.',
  '.cf1': 'CLF files (.cf1/.cf2) are a binary, access-controlled format and cannot be read here.',
  '.cf2': 'CLF files (.cf1/.cf2) are a binary, access-controlled format and cannot be read here.',
  '.clf': 'CLF files are a binary, access-controlled format and cannot be read here.',
  '.ulf': 'ULF files are not supported yet.',
  '.sofa': 'SOFA files are not supported.',
  '.xhn': 'XHN files are not supported.',
};
const EXPORT_HINT = ' Export the polar data as CSV (azimuth_deg, elevation_deg, frequency_hz, magnitude_db) or JSON and import that instead.';

const NUMBER_RE = /^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i;
const AZ_NAMES = new Set(['azimuth', 'az', 'azimuthdeg', 'azdeg', 'azimuthdegrees', 'horizontalangle', 'horizontalangledeg']);
const EL_NAMES = new Set(['elevation', 'el', 'elevationdeg', 'eldeg', 'elevationdegrees', 'verticalangle', 'verticalangledeg']);
const FREQ_NAMES = new Set(['frequency', 'freq', 'f', 'frequencyhz', 'freqhz', 'fhz']);
const MAG_NAMES = new Set(['magnitude', 'mag', 'level', 'spl', 'db', 'magnitudedb', 'magdb', 'leveldb', 'spldb', 'gain', 'gaindb']);
const AMBIGUOUS = new Set(['theta', 'phi', 'polar', 'polarangle', 'azimuthal']);
const keyOf = (h: string) => h.toLowerCase().replace(/[\s_\-()[\]°]/g, '');
const cleanNum = (n: number) => { const r = Math.round(n * 1e6) / 1e6; return Object.is(r, -0) ? 0 : r; };
const wrapAz = (az: number) => cleanNum(((az % 360) + 360) % 360);

function parseFrequencyHeader(h: string): number | null {
  const m = /^(\d+(?:\.\d+)?)\s*(k)?\s*(?:hz)?$/i.exec(h.trim());
  if (!m) return null;
  const v = Number(m[1]) * (m[2] ? 1000 : 1);
  return Number.isFinite(v) && v > 0 ? cleanNum(v) : null;
}

interface Sample { az: number; el: number; mags: number[] }

/** Shared back end for every input format: merge duplicates, require on-axis, normalise, derive resolution, validate. */
function assemble(samplesIn: Sample[], freqsIn: number[], format: DirectivityImportSummary['format'], fileName: string, meta: { brand?: string; model?: string }): DirectivityImportResult {
  const freqs = freqsIn;
  const merged = new Map<string, Sample>();
  for (const s of samplesIn) {
    const az = wrapAz(s.az), el = cleanNum(s.el), key = `${az},${el}`;
    const prev = merged.get(key);
    if (!prev) { merged.set(key, { az, el, mags: s.mags.slice() }); continue; }
    for (let i = 0; i < freqs.length; i++) {
      if (Math.abs(prev.mags[i] - s.mags[i]) > DIRECTIVITY_IMPORT_LIMITS.DUPLICATE_TOLERANCE_DB) {
        return fail(`Conflicting values for azimuth ${az}°, elevation ${el}° at ${freqs[i]} Hz (${prev.mags[i]} dB vs ${s.mags[i]} dB). Each direction must appear once (a repeated 360° row must match 0°).`);
      }
    }
  }
  const samples = [...merged.values()];
  if (samples.length < 3) return fail('The file has fewer than 3 distinct directions, which cannot describe a radiation pattern.');
  if (samples.length > DIRECTIVITY_LIMITS.MAX_POINTS) {
    return fail(tooManyDirections(samples.length));
  }
  const onAxis = merged.get('0,0');
  if (!onAxis) return fail('The file has no on-axis sample (azimuth 0°, elevation 0°). Add it, or rotate the angles so 0°/0° is the speaker\'s forward axis.');

  const azs = [...new Set(samples.map((s) => s.az))].sort((a, b) => a - b);
  const els = [...new Set(samples.map((s) => s.el))].sort((a, b) => a - b);
  let resolution = DIRECTIVITY_LIMITS.MAX_ANGULAR_RESOLUTION_DEG as number;
  for (let i = 1; i < azs.length; i++) resolution = Math.min(resolution, azs[i] - azs[i - 1]);
  if (azs.length > 1) resolution = Math.min(resolution, 360 - azs[azs.length - 1] + azs[0]);
  for (let i = 1; i < els.length; i++) resolution = Math.min(resolution, els[i] - els[i - 1]);
  resolution = cleanNum(resolution);

  const points: Record<string, number[]> = Object.create(null);
  for (const s of samples) points[`${s.az},${s.el}`] = s.mags.map((m, i) => cleanNum(m - onAxis.mags[i]));
  const checked = validateDirectivity({ frequencies: freqs, points: { ...points }, angularResolution: resolution, brand: meta.brand, model: meta.model });
  if ('error' in checked) return fail(checked.error + ' (Magnitudes are normalised to the on-axis sample; a pattern that falls more than 120 dB below on-axis is rejected.)');

  const maxAzGap = azs.length > 1 ? Math.max(...azs.slice(1).map((a, i) => a - azs[i]), 360 - azs[azs.length - 1] + azs[0]) : 360;
  const complete = samples.length === azs.length * els.length;
  const coverage: DirectivityImportSummary['coverage'] = els.length === 1 && els[0] === 0 ? 'horizontal-plane-only'
    : complete && maxAzGap <= 90 && els[0] <= -60 && els[els.length - 1] >= 60 ? 'full-sphere' : 'partial';
  const covered = OCTAVE_BANDS_HZ.filter((b) => freqs.some((f) => Math.abs(Math.log2(f / b)) <= 0.5));
  return {
    ok: true, data: checked.directivityData,
    summary: {
      fileName: fileName.slice(0, 100), format, pointCount: samples.length, frequenciesHz: freqs.slice(), azimuthCount: azs.length, elevationCount: els.length, coverage,
      angularResolutionDeg: resolution, coveredBandsHz: [...covered], uncoveredBandsHz: OCTAVE_BANDS_HZ.filter((b) => !covered.includes(b)), onAxisReferenceDb: onAxis.mags.map(cleanNum),
    },
  };
}

function parseCell(raw: string, decimalComma: boolean, line: number, col: number, what: string): number | { error: string } {
  let t = raw.trim().replace(/^"(.*)"$/, '$1').trim();
  if (decimalComma) t = t.replace(',', '.');
  if (!NUMBER_RE.test(t)) return { error: `Line ${line}, column ${col}: ${what} "${raw.trim().slice(0, 20)}" is not a number.` };
  const n = Number(t);
  return Number.isFinite(n) ? n : { error: `Line ${line}, column ${col}: ${what} "${raw.trim().slice(0, 20)}" is out of range.` };
}

function parseCsv(text: string, fileName: string): DirectivityImportResult {
  const lines = text.split(/\r\n|\n|\r/);
  if (lines.length > DIRECTIVITY_IMPORT_LIMITS.MAX_LINES) return fail(`The file has more than ${DIRECTIVITY_IMPORT_LIMITS.MAX_LINES.toLocaleString('en-US')} lines.`);
  const meta: { brand?: string; model?: string } = {};
  const rows: Array<{ n: number; text: string }> = [];
  lines.forEach((l, i) => {
    const t = l.trim();
    if (!t) return;
    if (t.length > DIRECTIVITY_IMPORT_LIMITS.MAX_LINE_CHARS) { rows.push({ n: i + 1, text: '\u0000TOO_LONG' }); return; }
    if (t.startsWith('#')) {
      const m = /^#\s*(brand|model)\s*[:=]\s*(.+)$/i.exec(t);
      if (m) (meta as Record<string, string>)[m[1].toLowerCase()] = m[2].trim().replace(/[\u0000-\u001f\u007f]/g, '').slice(0, 100);
      return;
    }
    rows.push({ n: i + 1, text: t });
  });
  const tooLong = rows.find((r) => r.text === '\u0000TOO_LONG');
  if (tooLong) return fail(`Line ${tooLong.n} is longer than ${DIRECTIVITY_IMPORT_LIMITS.MAX_LINE_CHARS} characters; this does not look like a CSV file.`);
  if (rows.length < 2) return fail('The file needs a header row and at least one data row.');

  const header = rows[0].text;
  const delim = [',', ';', '\t'].map((d) => ({ d, c: header.split(d).length - 1 })).sort((a, b) => b.c - a.c)[0];
  if (delim.c < 2) return fail('The header row needs at least 3 columns separated by commas, semicolons or tabs.');
  const d = delim.d, decimalComma = d !== ',';
  const names = header.split(d).map((h) => h.trim().replace(/^"(.*)"$/, '$1'));

  let azCol = -1, elCol = -1, fCol = -1, mCol = -1;
  const wide: Array<{ col: number; hz: number }> = [];
  for (let c = 0; c < names.length; c++) {
    const k = keyOf(names[c]);
    if (AMBIGUOUS.has(k)) return fail(`Column "${names[c]}" is ambiguous: theta/phi conventions differ between tools. Rename and convert it to azimuth (0° = on-axis) and elevation (0° = horizon).`);
    const assign = (cur: number, label: string) => { if (cur !== -1) throw new Error(`Column "${names[c]}" duplicates the ${label} column.`); return c; };
    try {
      if (AZ_NAMES.has(k)) azCol = assign(azCol, 'azimuth');
      else if (EL_NAMES.has(k)) elCol = assign(elCol, 'elevation');
      else if (FREQ_NAMES.has(k)) fCol = assign(fCol, 'frequency');
      else if (MAG_NAMES.has(k)) mCol = assign(mCol, 'magnitude');
      else { const hz = parseFrequencyHeader(names[c]); if (hz === null) return fail(`Column "${names[c].slice(0, 30)}" is not recognised. Expected azimuth_deg, elevation_deg, and either frequency_hz + magnitude_db (long format) or one numeric column per frequency such as 125, 250, 1000 (wide format).`); wide.push({ col: c, hz }); }
    } catch (e) { return fail((e as Error).message); }
  }
  if (azCol === -1 || elCol === -1) return fail('The header must include azimuth and elevation columns (for example azimuth_deg and elevation_deg).');
  const isLong = fCol !== -1 || mCol !== -1;
  if (isLong && (fCol === -1 || mCol === -1 || wide.length > 0)) return fail('Long format needs both a frequency and a magnitude column and no per-frequency columns; wide format needs only numeric frequency columns.');
  if (!isLong && wide.length === 0) return fail('No frequency data found: add frequency_hz + magnitude_db columns, or one numeric column per frequency.');

  const num = (r: { n: number; text: string }, parts: string[], col: number, what: string) => parseCell(parts[col] ?? '', decimalComma, r.n, col + 1, what);
  const body = rows.slice(1);
  if (isLong) {
    const byDir = new Map<string, { az: number; el: number; f: Map<number, number> }>();
    const freqSet = new Set<number>();
    for (const r of body) {
      const parts = r.text.split(d);
      if (parts.length !== names.length) return fail(`Line ${r.n} has ${parts.length} columns; the header has ${names.length}.`);
      const az = num(r, parts, azCol, 'azimuth'), el = num(r, parts, elCol, 'elevation'), f = num(r, parts, fCol, 'frequency'), m = num(r, parts, mCol, 'magnitude');
      for (const v of [az, el, f, m]) if (typeof v !== 'number') return fail((v as { error: string }).error);
      const fz = cleanNum(f as number);
      if (!(fz > 0 && fz <= DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ)) return fail(`Line ${r.n}: frequency ${fz} Hz must be between 0 and ${DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ} Hz.`);
      if (Math.abs(el as number) > DIRECTIVITY_LIMITS.MAX_ABS_ELEVATION_DEG) return fail(`Line ${r.n}: elevation ${el} must be between -90° and +90°.`);
      freqSet.add(fz);
      if (freqSet.size > DIRECTIVITY_LIMITS.MAX_FREQUENCIES) return fail(`The file has more than ${DIRECTIVITY_LIMITS.MAX_FREQUENCIES} distinct frequencies. Resample to octave or 1/3-octave bands (at most ${DIRECTIVITY_LIMITS.MAX_FREQUENCIES}).`);
      const key = `${wrapAz(az as number)},${cleanNum(el as number)}`;
      let e = byDir.get(key); if (!e) { e = { az: az as number, el: el as number, f: new Map() }; byDir.set(key, e); }
      const prev = e.f.get(fz);
      if (prev !== undefined && Math.abs(prev - (m as number)) > DIRECTIVITY_IMPORT_LIMITS.DUPLICATE_TOLERANCE_DB) return fail(`Line ${r.n}: conflicting duplicate for azimuth ${az}°, elevation ${el}° at ${fz} Hz.`);
      e.f.set(fz, m as number);
      if (byDir.size > DIRECTIVITY_LIMITS.MAX_POINTS) return fail(tooManyDirections());
    }
    const freqs = [...freqSet].sort((a, b) => a - b);
    const samples: Sample[] = [];
    for (const e of byDir.values()) {
      const mags: number[] = [];
      for (const f of freqs) { const v = e.f.get(f); if (v === undefined) return fail(`Azimuth ${e.az}°, elevation ${e.el}° has no value at ${f} Hz. Every direction needs a value at every frequency.`); mags.push(v); }
      samples.push({ az: e.az, el: e.el, mags });
    }
    return assemble(samples, freqs, 'csv-long', fileName, meta);
  }

  const sortedWide = [...wide].sort((a, b) => a.hz - b.hz);
  if (new Set(sortedWide.map((w) => w.hz)).size !== sortedWide.length) return fail('Two columns have the same frequency.');
  if (sortedWide.length > DIRECTIVITY_LIMITS.MAX_FREQUENCIES) return fail(`The file has ${sortedWide.length} frequency columns; the limit is ${DIRECTIVITY_LIMITS.MAX_FREQUENCIES}.`);
  if (sortedWide.some((w) => w.hz > DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ)) return fail(`Frequencies must be at most ${DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ} Hz.`);
  const samples: Sample[] = [];
  for (const r of body) {
    const parts = r.text.split(d);
    if (parts.length !== names.length) return fail(`Line ${r.n} has ${parts.length} columns; the header has ${names.length}.`);
    const az = num(r, parts, azCol, 'azimuth'), el = num(r, parts, elCol, 'elevation');
    if (typeof az !== 'number') return fail(az.error);
    if (typeof el !== 'number') return fail(el.error);
    if (Math.abs(el) > DIRECTIVITY_LIMITS.MAX_ABS_ELEVATION_DEG) return fail(`Line ${r.n}: elevation ${el} must be between -90° and +90°.`);
    const mags: number[] = [];
    for (const w of sortedWide) { const v = num(r, parts, w.col, `${w.hz} Hz value`); if (typeof v !== 'number') return fail(v.error); mags.push(v); }
    samples.push({ az, el, mags });
    if (samples.length > DIRECTIVITY_LIMITS.MAX_POINTS) return fail(tooManyDirections());
  }
  return assemble(samples, sortedWide.map((w) => w.hz), 'csv-wide', fileName, meta);
}

function parseJson(text: string, fileName: string): DirectivityImportResult {
  let doc: unknown;
  try { doc = JSON.parse(text); } catch { return fail('The file is not valid JSON.'); }
  if (doc === null || typeof doc !== 'object' || Array.isArray(doc)) return fail('The JSON must be an object with "frequencies" and "points".');
  const o = doc as Record<string, unknown>;
  const freqs = o.frequencies;
  if (!Array.isArray(freqs) || freqs.length < 1 || freqs.length > DIRECTIVITY_LIMITS.MAX_FREQUENCIES || !freqs.every((f) => typeof f === 'number' && Number.isFinite(f) && f > 0 && f <= DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ)) {
    return fail(`"frequencies" must be 1 to ${DIRECTIVITY_LIMITS.MAX_FREQUENCIES} positive numbers up to ${DIRECTIVITY_LIMITS.MAX_FREQUENCY_HZ} Hz.`);
  }
  const order = freqs.map((f, i) => ({ f: cleanNum(f as number), i })).sort((a, b) => a.f - b.f);
  if (new Set(order.map((x) => x.f)).size !== order.length) return fail('"frequencies" contains a duplicate.');
  const sortedFreqs = order.map((x) => x.f);
  const samples: Sample[] = [];
  const push = (az: unknown, el: unknown, mag: unknown): string | null => {
    if (typeof az !== 'number' || typeof el !== 'number' || !Number.isFinite(az) || !Number.isFinite(el)) return 'A point has a non-numeric azimuth or elevation.';
    if (!Array.isArray(mag) || mag.length !== freqs.length || !mag.every((v) => typeof v === 'number' && Number.isFinite(v))) return `The point at azimuth ${az}, elevation ${el} must have ${freqs.length} finite magnitude values (one per frequency).`;
    if (Math.abs(el) > DIRECTIVITY_LIMITS.MAX_ABS_ELEVATION_DEG) return `Elevation ${el} must be between -90 and +90.`;
    samples.push({ az, el, mags: order.map((x) => mag[x.i] as number) });
    return samples.length > DIRECTIVITY_LIMITS.MAX_POINTS ? tooManyDirections() : null;
  };
  if (Array.isArray(o.points)) {
    for (const p of o.points) { if (p === null || typeof p !== 'object') return fail('A point is not an object.'); const q = p as Record<string, unknown>; const e = push(q.azimuth, q.elevation, q.magnitude); if (e) return fail(e); }
  } else if (o.points !== null && typeof o.points === 'object') {
    for (const [k, v] of Object.entries(o.points as Record<string, unknown>)) {
      const parts = k.split(',');
      if (parts.length !== 2 || !parts.every((x) => NUMBER_RE.test(x.trim()))) return fail(`Point key "${k.slice(0, 20)}" must look like "azimuth,elevation".`);
      const e = push(Number(parts[0]), Number(parts[1]), v); if (e) return fail(e);
    }
  } else return fail('"points" must be an object keyed "azimuth,elevation" or an array of {azimuth, elevation, magnitude}.');
  const label = (v: unknown) => (typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f]/g, '').slice(0, 100) : undefined);
  return assemble(samples, sortedFreqs, 'json', fileName, { brand: label(o.brand), model: label(o.model) });
}

/** Parse already-decoded text. Chooses JSON when the first character is { or [, otherwise CSV. */
export function parseDirectivityText(text: string, fileName = 'directivity'): DirectivityImportResult {
  const t = text.replace(/^\uFEFF/, '');
  const first = t.trimStart()[0];
  // A .json name wins over sniffing, so a bare `null` or `5` is reported as bad JSON rather than misread as a CSV.
  return first === '{' || first === '[' || /\.json$/i.test(fileName) ? parseJson(t, fileName) : parseCsv(t, fileName);
}

/** Parse raw file bytes. Refuses binary and known-unsupported formats before touching the content. */
export function parseDirectivityBytes(bytes: Uint8Array, fileName: string): DirectivityImportResult {
  const ext = /\.[A-Za-z0-9]+$/.exec(fileName)?.[0]?.toLowerCase() ?? '';
  if (REFUSED_EXTENSIONS[ext]) return fail(REFUSED_EXTENSIONS[ext] + EXPORT_HINT);
  if (bytes.length === 0) return fail('The file is empty.');
  if (bytes.length > DIRECTIVITY_IMPORT_LIMITS.MAX_FILE_BYTES) return fail(`The file is larger than ${DIRECTIVITY_IMPORT_LIMITS.MAX_FILE_BYTES / (1024 * 1024)} MB.`);
  // CLF2 signature (41 BD 0A 00 01), ZIP/GLL-style containers (PK\x03\x04), then any NUL byte = binary.
  if (bytes[0] === 0x41 && bytes[1] === 0xbd && bytes[2] === 0x0a && bytes[3] === 0x00 && bytes[4] === 0x01) return fail('This is a CLF2 binary file, which cannot be read here.' + EXPORT_HINT);
  if (bytes[0] === 0x50 && bytes[1] === 0x4b && bytes[2] === 0x03 && bytes[3] === 0x04) return fail('This is a compressed archive, not a CSV or JSON file.' + EXPORT_HINT);
  const probe = Math.min(bytes.length, 8192);
  for (let i = 0; i < probe; i++) if (bytes[i] === 0) return fail('This is a binary file, not a CSV or JSON text file.' + EXPORT_HINT);
  let text: string;
  try { text = new TextDecoder('utf-8', { fatal: true }).decode(bytes); } catch { return fail('The file is not valid UTF-8 text.'); }
  return parseDirectivityText(text, fileName);
}

/** Browser entry point: reads a File (size is checked BEFORE reading it into memory). */
export async function importDirectivityFile(file: { name: string; size: number; arrayBuffer: () => Promise<ArrayBuffer> }): Promise<DirectivityImportResult> {
  const ext = /\.[A-Za-z0-9]+$/.exec(file.name)?.[0]?.toLowerCase() ?? '';
  if (REFUSED_EXTENSIONS[ext]) return fail(REFUSED_EXTENSIONS[ext] + EXPORT_HINT);
  if (file.size > DIRECTIVITY_IMPORT_LIMITS.MAX_FILE_BYTES) return fail(`The file is larger than ${DIRECTIVITY_IMPORT_LIMITS.MAX_FILE_BYTES / (1024 * 1024)} MB.`);
  try { return parseDirectivityBytes(new Uint8Array(await file.arrayBuffer()), file.name); } catch { return fail('The file could not be read.'); }
}

export interface DirectivityStatus {
  available: boolean;
  pointCount: number;
  frequenciesHz: number[];
  coveredBandsHz: number[];
  uncoveredBandsHz: number[];
  /** Always 'imported-unverified': user data is never presented as catalog or manufacturer data. */
  provenance: 'imported-unverified' | 'none';
}

/**
 * What a source's stored directivity data actually does, derived from the data itself (so a re-opened project shows the same
 * status as a fresh import). Absent or unusable data is reported as unavailable: the room simulation then treats the
 * source as omnidirectional, and says so.
 */
export function describeDirectivityData(isDirectional: unknown, data: unknown): DirectivityStatus {
  const none: DirectivityStatus = { available: false, pointCount: 0, frequenciesHz: [], coveredBandsHz: [], uncoveredBandsHz: [...OCTAVE_BANDS_HZ], provenance: 'none' };
  if (isDirectional !== true) return none;
  const v = validateDirectivity(data);
  if ('error' in v) return none;
  const d = v.directivityData;
  const covered = OCTAVE_BANDS_HZ.filter((b) => d.frequencies.some((f) => Math.abs(Math.log2(f / b)) <= 0.5));
  return { available: true, pointCount: Object.keys(d.points).length, frequenciesHz: [...d.frequencies].sort((a, b) => a - b), coveredBandsHz: [...covered], uncoveredBandsHz: OCTAVE_BANDS_HZ.filter((b) => !covered.includes(b)), provenance: 'imported-unverified' };
}
