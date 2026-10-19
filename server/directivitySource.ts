/**
 * Equivalent-source synthesis for an imported directivity pattern.
 *
 * The solver cannot radiate a direction-dependent pattern from a single in-phase node: a compact cluster of in-phase
 * monopoles is, to first order, a monopole.  This module fits a *complex-weighted* set of monopole nodes (an
 * equivalent-source / multipole expansion) to the pattern the user supplied, at one octave-band centre frequency.
 *
 *   p_far(s) ~ sum_n w_n * exp(-j k s.r_n)          (r_n in metres, s a unit world direction, k = 2*pi*f/c)
 *
 * The complex weight w_n = re_n + j*im_n is realised in the time domain by injecting re_n * excitation(t) plus
 * im_n * Hilbert(excitation)(t); the Hilbert transform implements the +90 degrees that a complex weight implies.
 * This is a genuine phase-differenced source, unlike the earlier amplitude-only cluster.
 *
 * Limits, stated rather than hidden:
 *  - The fit is a regularised least-squares fit at the band centre. Away from the centre the same weights are used,
 *    so a pattern that changes quickly with frequency is approximated rather than followed inside the band.
 *  - The node spacing is one FDTD cell. Above roughly c/(3*dx) the grid cannot represent the pattern (spatial
 *    aliasing); the caller keeps the previous amplitude-cluster model for those bands instead of fabricating one.
 *  - The fitted pattern is sampled on a 15-degree world sphere; detail finer than that is not represented.
 */
import { getInterpolatedMagnitude } from './directivityParser';

export type ComplexNode = { offset: [number, number, number]; re: number; im: number };

const SPEED_OF_SOUND = 343;
const SAMPLE_STEP_DEG = 15;
const MAX_NODES = 72;
const SHELL_RADIUS_CELLS = 2.6;  // a compact shell: wide enough for a real lobe, small enough to stay broadband
const RIDGE = 1e-4;

/** The grid cannot carry a direction pattern when a cell is a large fraction of a wavelength. */
export function gridResolvesPattern(frequencyHz: number, dxMeters: number): boolean {
  if (!(frequencyHz > 0) || !(dxMeters > 0)) return false;
  return dxMeters * frequencyHz <= SPEED_OF_SOUND / 3;
}

type PatternSampler = (azDeg: number, elDeg: number) => number;

/**
 * Bilinear sampler over a regular (azimuth, elevation) grid.
 *
 * The app's own `getInterpolatedMagnitude` is an inverse-distance weighting over ALL supplied points, which is fine for
 * a single source weight but pulls distant directions into every value. Fitting a 30 dB pattern against that smoothed
 * target leaves the rear lobe more than 10 dB wrong, so the synthesis resamples the same data locally. Irregular grids
 * fall back to the parser's interpolation rather than inventing a lattice.
 */
function buildPatternSampler(data: any, frequencyHz: number): PatternSampler {
  const keys = Object.keys(data?.points ?? {});
  const freqs: number[] = Array.isArray(data?.frequencies) ? data.frequencies : [];
  const valuesAt = (mags: number[]): number | null => {
    if (!Array.isArray(mags) || !mags.length) return null;
    if (freqs.length <= 1) return Number.isFinite(mags[0]) ? mags[0] : null;
    let lo = 0, hi = freqs.length - 1;
    if (frequencyHz <= freqs[0]) { lo = hi = 0; }
    else if (frequencyHz >= freqs[freqs.length - 1]) { lo = hi = freqs.length - 1; }
    else { for (let i = 0; i < freqs.length - 1; i++) if (freqs[i] <= frequencyHz && frequencyHz <= freqs[i + 1]) { lo = i; hi = i + 1; break; } }
    const a = mags[lo], b = mags[hi];
    if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
    if (lo === hi) return a;
    const t = (frequencyHz - freqs[lo]) / (freqs[hi] - freqs[lo]);
    return a + (b - a) * t;
  };
  if (!keys.length) return () => 0;

  const azSet = new Set<number>(), elSet = new Set<number>();
  const table = new Map<string, number>();
  for (const key of keys) {
    const [azStr, elStr] = key.split(',');
    const az = parseFloat(azStr), el = parseFloat(elStr);
    if (!Number.isFinite(az) || !Number.isFinite(el)) return (a, e) => getInterpolatedMagnitude(data, frequencyHz, a, e);
    const v = valuesAt(data.points[key]);
    if (v === null) continue;
    azSet.add(az); elSet.add(el); table.set(`${az},${el}`, v);
  }
  if (!table.size) return () => 0;
  const azList = [...azSet].sort((a, b) => a - b);
  const elList = [...elSet].sort((a, b) => a - b);
  // 0.5-degree tolerance: the importer normalises angles to integers, so a regular grid is exactly regular.
  const regular = (() => {
    if (azList.length < 2 || elList.length < 2) return false;
    const dAz = azList[1] - azList[0], dEl = elList[1] - elList[0];
    for (let i = 1; i < azList.length; i++) if (Math.abs((azList[i] - azList[i - 1]) - dAz) > 0.5) return false;
    for (let i = 1; i < elList.length; i++) if (Math.abs((elList[i] - elList[i - 1]) - dEl) > 0.5) return false;
    for (const az of azList) for (const el of elList) if (!table.has(`${az},${el}`)) return false;
    return true;
  })();
  if (!regular) return (a, e) => getInterpolatedMagnitude(data, frequencyHz, a, e);

  const azValues = azList.slice().sort((a, b) => a - b);
  const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
  return (azDeg: number, elDeg: number) => {
    const az = ((azDeg % 360) + 360) % 360;
    const el = Math.max(elList[0], Math.min(elList[elList.length - 1], elDeg));
    const azI = Math.min(azValues.length - 1, Math.floor((az / 360) * azValues.length));
    const az0 = azValues[azI];
    const az1 = azI + 1 < azValues.length ? azValues[azI + 1] : azValues[0] + 360;
    const azT = az1 > az0 ? (az - az0) / (az1 - az0) : 0;
    let elI = 0;
    for (let i = 0; i < elList.length - 1; i++) if (elList[i] <= el && el <= elList[i + 1]) { elI = i; break; }
    if (el >= elList[elList.length - 1]) elI = elList.length - 2;
    const el0 = elList[elI], el1 = elList[elI + 1];
    const elT = el1 > el0 ? (el - el0) / (el1 - el0) : 0;
    const at = (a: number, e: number) => table.get(`${a},${e}`) ?? 0;
    const az0w = az0 % 360;
    const az1w = az1 % 360;
    const v00 = at(az0w, el0), v10 = at(az1w, el0), v01 = at(az0w, el1), v11 = at(az1w, el1);
    const v0 = lerp(v00, v10, azT);
    const v1 = lerp(v01, v11, azT);
    return lerp(v0, v1, elT);
  };
}

function unitSphereDirections(stepDeg: number): Array<[number, number, number]> {
  const out: Array<[number, number, number]> = [];
  for (let el = -90; el <= 90; el += stepDeg) {
    // At the poles every azimuth is the same direction; one sample avoids weighting the pole 24 times.
    if (Math.abs(el) === 90) { out.push([0, 0, Math.sign(el)]); continue; }
    for (let az = 0; az < 360; az += stepDeg) {
      const c = Math.cos((el * Math.PI) / 180);
      out.push([Math.sin((az * Math.PI) / 180) * c, Math.cos((az * Math.PI) / 180) * c, Math.sin((el * Math.PI) / 180)]);
    }
  }
  return out;
}

/**
 * Evenly spread candidate injection cells on a shell around SHELL_RADIUS_CELLS from the source. A Fibonacci sphere snapped to the
 * nearest integer cell gives near-uniform angular coverage with a bounded node count, which keeps the normal
 * equations well conditioned.
 */
function shellCells(): Array<[number, number, number]> {
  const radiusCells = SHELL_RADIUS_CELLS;
  const cells: Array<[number, number, number]> = [];
  const seen = new Set<string>();
  const golden = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < MAX_NODES * 3 && cells.length < MAX_NODES; i++) {
    const z = 1 - (2 * (i + 0.5)) / (MAX_NODES * 3);
    const r = Math.sqrt(Math.max(0, 1 - z * z));
    const theta = golden * i;
    const dir: [number, number, number] = [Math.cos(theta) * r, Math.sin(theta) * r, z];
    const cell: [number, number, number] = [
      Math.round(dir[0] * radiusCells),
      Math.round(dir[1] * radiusCells),
      Math.round(dir[2] * radiusCells),
    ];
    const radius = Math.hypot(cell[0], cell[1], cell[2]);
    if (radius < radiusCells * 0.6 || radius > radiusCells * 1.3) continue;
    const key = cell.join(',');
    if (seen.has(key)) continue;
    seen.add(key);
    cells.push(cell);
  }
  return cells;
}

type Vec3 = { x: number; y: number; z: number };

/** Gaussian elimination with partial pivoting on an n x (n+1) system; returns null if it is singular. */
function solveLinearSystem(matrix: Float64Array[], rhs: Float64Array): Float64Array | null {
  const n = rhs.length;
  const a: Float64Array[] = matrix.map((row, i) => {
    const copy = new Float64Array(n + 1);
    copy.set(row.subarray(0, n));
    copy[n] = rhs[i];
    return copy;
  });
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let row = col + 1; row < n; row++) if (Math.abs(a[row][col]) > Math.abs(a[pivot][col])) pivot = row;
    if (Math.abs(a[pivot][col]) < 1e-12) return null;
    if (pivot !== col) { const t = a[col]; a[col] = a[pivot]; a[pivot] = t; }
    const p = a[col][col];
    for (let j = col; j <= n; j++) a[col][j] /= p;
    for (let row = 0; row < n; row++) {
      if (row === col) continue;
      const f = a[row][col];
      if (f === 0) continue;
      for (let j = col; j <= n; j++) a[row][j] -= f * a[col][j];
    }
  }
  const out = new Float64Array(n);
  for (let i = 0; i < n; i++) out[i] = a[i][n];
  return out;
}

/**
 * Fit complex monopole weights that reproduce the supplied pattern at `frequencyHz`.
 *
 * `toLocal` maps a world direction to the speaker's local frame (the same transform the solver uses for aiming), so
 * the pattern is fitted in the user's coordinate convention and then radiated along the world axes.
 */
export function synthesizeDirectionalNodes(
  data: any,
  frequencyHz: number,
  dxMeters: number,
  toLocal: (x: number, y: number, z: number) => Vec3,
): ComplexNode[] {
  const cells = shellCells();
  if (!cells.length) return [];
  const k = (2 * Math.PI * frequencyHz) / SPEED_OF_SOUND;
  const dirs = unitSphereDirections(SAMPLE_STEP_DEG);
  const sampler = buildPatternSampler(data, frequencyHz);
  const targets = new Float64Array(dirs.length);
  for (let m = 0; m < dirs.length; m++) {
    const [sx, sy, sz] = dirs[m];
    const local = toLocal(sx, sy, sz);
    const az = (Math.atan2(local.x, local.y) * 180) / Math.PI;
    const el = (Math.asin(Math.max(-1, Math.min(1, local.z))) * 180) / Math.PI;
    targets[m] = Math.pow(10, sampler(az, el) / 20);
  }

  const N = cells.length;
  const M = dirs.length;
  // Real and imaginary parts of A[m][n] = exp(-j k s_m . r_n)
  const ar: Float64Array[] = [];
  const ai: Float64Array[] = [];
  for (let m = 0; m < M; m++) {
    const rowR = new Float64Array(N);
    const rowI = new Float64Array(N);
    const [sx, sy, sz] = dirs[m];
    // Fit relative (dB) error, not absolute pressure: a linear least-squares fit spends all its freedom on the loud
    // front hemisphere and leaves the rear lobe tens of dB wrong. Dividing each row by its target value makes the fit
    // minimise the same relative error in every direction.
    const rowScale = 1 / Math.max(targets[m], 1e-3);
    for (let n = 0; n < N; n++) {
      const [cx, cy, cz] = cells[n];
      const phase = -k * (sx * cx + sy * cy + sz * cz) * dxMeters;
      rowR[n] = Math.cos(phase) * rowScale;
      rowI[n] = Math.sin(phase) * rowScale;
    }
    ar.push(rowR);
    ai.push(rowI);
  }

  // Normal equations (A^H A + ridge I) w = A^H d, expanded into real form:
  //   [P1 -P2][wr]   [br]
  //   [P2  P1][wi] = [bi]
  const P1: Float64Array[] = Array.from({ length: N }, () => new Float64Array(N));
  const P2: Float64Array[] = Array.from({ length: N }, () => new Float64Array(N));
  const br = new Float64Array(N);
  const bi = new Float64Array(N);
  for (let m = 0; m < M; m++) {
    const rowR = ar[m];
    const rowI = ai[m];
    const d = 1;
    for (let i = 0; i < N; i++) {
      const rri = rowR[i];
      const rii = rowI[i];
      br[i] += rri * d;
      bi[i] -= rii * d;
      for (let j = i; j < N; j++) {
        P1[i][j] += rri * rowR[j] + rii * rowI[j];
        P2[i][j] += rri * rowI[j] - rii * rowR[j];
      }
    }
  }
  // P1 = Ar^T Ar + Ai^T Ai is symmetric; P2 = Ar^T Ai - Ai^T Ar is ANTIsymmetric. Mirroring P2 as if it were
  // symmetric silently solves a different system and collapses the fitted pattern towards a cardioid.
  for (let i = 0; i < N; i++) for (let j = 0; j < i; j++) { P1[i][j] = P1[j][i]; P2[i][j] = -P2[j][i]; }

  let meanDiagonal = 0;
  for (let i = 0; i < N; i++) meanDiagonal += P1[i][i];
  meanDiagonal = meanDiagonal / N;
  if (!Number.isFinite(meanDiagonal) || meanDiagonal <= 0) meanDiagonal = 1;
  const lambda = RIDGE * meanDiagonal;

  const n2 = 2 * N;
  const system: Float64Array[] = Array.from({ length: n2 }, () => new Float64Array(n2));
  const rhs = new Float64Array(n2);
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      system[i][j] = P1[i][j];
      system[i][j + N] = -P2[i][j];
      system[i + N][j] = P2[i][j];
      system[i + N][j + N] = P1[i][j];
    }
    system[i][i] += lambda;
    system[i + N][i + N] += lambda;
    rhs[i] = br[i];
    rhs[i + N] = bi[i];
  }
  const solution = solveLinearSystem(system, rhs);
  if (!solution) return [];
  for (let i = 0; i < solution.length; i++) if (!Number.isFinite(solution[i])) return [];

  // Scale so the on-axis direction radiates the dataset's on-axis value (the parser normalises it to 0 dB = 1).
  const axis = onAxisWorldDirection(toLocal);
  let onAxisRe = 0;
  let onAxisIm = 0;
  {
    const [sx, sy, sz] = axis;
    for (let n = 0; n < N; n++) {
      const [cx, cy, cz] = cells[n];
      const phase = -k * (sx * cx + sy * cy + sz * cz) * dxMeters;
      const c = Math.cos(phase);
      const s = Math.sin(phase);
      const wr = solution[n];
      const wi = solution[n + N];
      onAxisRe += wr * c - wi * s;
      onAxisIm += wr * s + wi * c;
    }
  }
  const achieved = Math.hypot(onAxisRe, onAxisIm);
  const scale = achieved > 1e-9 ? 1 / achieved : 1;

  const nodes: ComplexNode[] = [];
  for (let n = 0; n < N; n++) {
    nodes.push({
      offset: cells[n],
      re: solution[n] * scale,
      im: solution[n + N] * scale,
    });
  }
  return nodes;
}

/**
 * The world direction the speaker's local forward (+Y) points along. `toLocal` is a rotation R (local = R * world),
 * so the world image of local +Y is R^T e2, i.e. the second ROW of R. Its columns are the images of the world axes.
 */
export function onAxisWorldDirection(toLocal: (x: number, y: number, z: number) => Vec3): [number, number, number] {
  const colX = toLocal(1, 0, 0);
  const colY = toLocal(0, 1, 0);
  const colZ = toLocal(0, 0, 1);
  return [colX.y, colY.y, colZ.y];
}

/**
 * Hilbert transform with a 90-degree phase ADVANCE (q = +j*x in the Fourier convention used for the complex weights).
 *
 * The nodes carry complex weights; multiplying a real, band-limited excitation by j is exactly a 90-degree advance,
 * which a real-valued time-domain solver cannot express with amplitudes alone. The FIR is the windowed ideal Hilbert
 * kernel (whose transform lags by 90 degrees) with its sign flipped. It is applied off-line to the complete excitation,
 * so no causality or latency is introduced into the run.
 */
export function quadratureSignal(signal: ArrayLike<number>, taps = 127): Float64Array {
  const n = signal.length;
  const out = new Float64Array(n);
  if (!n) return out;
  const half = Math.floor((taps - 1) / 2);
  const kernel = new Float64Array(2 * half + 1);
  for (let k = -half; k <= half; k++) {
    if (k === 0 || k % 2 === 0) continue;
    const w = 0.42 + 0.5 * Math.cos((Math.PI * k) / half) + 0.08 * Math.cos((2 * Math.PI * k) / half);
    kernel[k + half] = (2 / (Math.PI * k)) * w;
  }
  for (let t = 0; t < n; t++) {
    let acc = 0;
    for (let k = -half; k <= half; k++) {
      const idx = t - k;
      if (idx < 0 || idx >= n) continue;
      const h = kernel[k + half];
      if (h !== 0) acc += h * signal[idx];
    }
    out[t] = acc;
  }
  return out;
}
