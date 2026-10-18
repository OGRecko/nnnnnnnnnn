import { LIMITS } from './publicLimits';
import type { SpatialSummary, ReceiverResult, ReceiverGridDef, ReceiverInput, HeatmapData, HeatmapPoint } from './sharedTypes';

/**
 * Compute spatial summary statistics for a given metric across receivers.
 * Ignores null/undefined/NaN values. Returns null if fewer than 2 valid values.
 */
export function computeSpatialSummary(
  metric: string,
  values: (number | null | undefined)[]
): SpatialSummary | null {
  const valid = values.filter((v): v is number => v != null && Number.isFinite(v));
  if (valid.length < 2) return null;

  const sorted = [...valid].sort((a, b) => a - b);
  const min = sorted[0];
  const max = sorted[sorted.length - 1];
  const sum = valid.reduce((a, b) => a + b, 0);
  const mean = sum / valid.length;
  
  // Median
  const mid = Math.floor(sorted.length / 2);
  const median = sorted.length % 2 === 0
    ? (sorted[mid - 1] + sorted[mid]) / 2
    : sorted[mid];

  // Standard deviation (population)
  const sqDiffs = valid.map(v => (v - mean) ** 2);
  const stdDev = Math.sqrt(sqDiffs.reduce((a, b) => a + b, 0) / valid.length);

  return { metric, min, max, mean, median, stdDev, validCount: valid.length };
}

/**
 * Compute spatial summaries for all available metrics across receiver results.
 */
export function computeAllSpatialSummaries(
  receiverResults: ReceiverResult[]
): SpatialSummary[] {
  const metricKeys: (keyof import('./sharedTypes').ReceiverMetrics)[] = 
    ['rt60', 'edt', 't20', 't30', 'c50', 'c80', 'd50', 'spl'];
  
  const summaries: SpatialSummary[] = [];
  for (const key of metricKeys) {
    const values = receiverResults.map(r => (r.metrics[key] ?? null) as number | null);
    const summary = computeSpatialSummary(key.toUpperCase(), values);
    if (summary) summaries.push(summary);
  }
  return summaries;
}

/** Index-based axis count with a 1%-of-spacing tolerance so an exact-fit grid keeps its last row/column. */
function axisCount(min: number, max: number, spacing: number): number {
  if (!Number.isFinite(min) || !Number.isFinite(max) || max < min) return 0;
  const n = Math.floor((max - min) / spacing + 0.01) + 1;
  return Number.isFinite(n) && n > 0 ? n : 0;
}

function normalizedSpacing(def: ReceiverGridDef, roomL: number, roomW: number): { spacingX: number; spacingY: number } | null {
  const spacingX = def.spacing / roomL;
  const spacingY = def.spacing / roomW;
  if (!(spacingX > 0) || !(spacingY > 0) || !Number.isFinite(spacingX) || !Number.isFinite(spacingY)) return null;
  return { spacingX, spacingY };
}

/**
 * Generate receiver grid points from a grid definition.
 * Normalizes positions to 0..1 coordinates.
 * Enforces the public LIMITS.MAX_RECEIVERS limit BEFORE allocating anything, and rejects non-finite bounds
 * (an infinite bound or a tiny spacing previously produced an unbounded loop).
 */
export function generateReceiverGrid(
  def: ReceiverGridDef,
  roomL: number,
  roomW: number
): ReceiverInput[] {
  // def coordinates are normalized 0..1; spacing is in meters
  const sp = normalizedSpacing(def, roomL, roomW);
  if (!sp) throw new Error('Grid spacing must be a positive finite number.');
  if (![def.xMin, def.xMax, def.yMin, def.yMax].every(Number.isFinite)) throw new Error('Grid bounds must be finite numbers.');

  const countX = axisCount(def.xMin, def.xMax, sp.spacingX);
  const countY = axisCount(def.yMin, def.yMax, sp.spacingY);
  const total = countX * countY;
  if (total > LIMITS.MAX_RECEIVERS) {
    throw new Error(`This grid would create ${total.toLocaleString('en-US')} receivers; the limit is ${LIMITS.MAX_RECEIVERS}. Increase the spacing or shrink the grid area.`);
  }

  const receivers: ReceiverInput[] = [];
  let id = 1;
  for (let ix = 0; ix < countX; ix++) {
    const x = def.xMin + ix * sp.spacingX;
    for (let iy = 0; iy < countY; iy++) {
      const y = def.yMin + iy * sp.spacingY;
      const clampedX = Math.max(0.02, Math.min(0.98, x));
      const clampedY = Math.max(0.02, Math.min(0.98, y));
      receivers.push({
        id: `grid-${id}`,
        name: `Grid ${id}`,
        x: Math.round(clampedX * 1000) / 1000,
        y: Math.round(clampedY * 1000) / 1000,
        z: def.zHeight,
      });
      id++;
    }
  }

  return receivers;
}

/**
 * Number of receivers a grid definition would produce (0 for an invalid definition). Matches generateReceiverGrid
 * exactly, and is NOT clamped to the limit, so a UI can show "N receivers (limit 64)".
 */
export function estimateGridReceiverCount(
  def: ReceiverGridDef,
  roomL: number,
  roomW: number
): number {
  const sp = normalizedSpacing(def, roomL, roomW);
  if (!sp) return 0;
  return axisCount(def.xMin, def.xMax, sp.spacingX) * axisCount(def.yMin, def.yMax, sp.spacingY);
}

/**
 * Build a heatmap data structure from receiver results for a specific metric.
 */
export function buildHeatmapData(
  metric: string,
  receiverResults: ReceiverResult[],
  roomL: number,
  roomW: number
): HeatmapData {
  const metricKey = metric.toLowerCase() as keyof import('./sharedTypes').ReceiverMetrics;
  const points: HeatmapPoint[] = [];

  for (const r of receiverResults) {
    const value = r.metrics[metricKey] as number;
    if (value != null && Number.isFinite(value)) {
      points.push({
        x: r.position.x * roomL,
        y: r.position.y * roomW,
        z: r.position.z ?? null, // unknown stays unknown; an explicit 0 is kept
        value,
        receiverId: r.id,
      });
    }
  }

  return {
    metric,
    points,
    interpolated: false, // Direct measurement points only
  };
}

/**
 * Check if receiver spacing is coarse relative to room dimensions.
 * Returns a warning if spacing > roomMinDim / 4.
 */
export function checkSpatialResolution(
  spacingM: number,
  roomL: number,
  roomW: number
): import('./sharedTypes').StructuredWarning | null {
  const minDim = Math.min(roomL, roomW);
  if (spacingM > minDim / 4) {
    return {
      code: 'LOW_SPATIAL_RESOLUTION',
      severity: 'warning',
      message: `Receiver spacing (${spacingM.toFixed(2)} m) is coarse relative to the room dimensions (${roomL.toFixed(1)}×${roomW.toFixed(1)} m). Fine spatial variations may not be captured.`,
    };
  }
  return null;
}
