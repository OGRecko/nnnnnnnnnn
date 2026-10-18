/**
 * Geometry/occlusion tests for audioEngine.lineIntersect and audioEngine.checkWallIntersections.
 *
 * These used to test a verbatim COPY of the two methods (audioEngine.ts could not be imported when zustand was not
 * installed) guarded by an eval-based drift check. audioEngine now imports normally, so every assertion here runs
 * against the REAL engine. The old per-edge-sum implementation is kept below ONLY as an independent oracle: for every
 * non-degenerate path (one that does not pass exactly through a polygon vertex) the real engine must agree with it.
 * Vertex paths are the one deliberate difference - see audioEngine.test.ts for the corner-crossing regression.
 */
import assert from 'node:assert/strict';
import { MATERIALS } from './materials';
import { audioEngine } from './audioEngine';

let passed = 0;
const check = (name: string, fn: () => void) => { fn(); passed++; console.log(`  PASS  ${name}`); };
console.log('\n=== audioEngine geometry tests (real engine + independent oracle) ===\n');

// --- Independent ORACLE: the original per-edge sum (counts a vertex hit once per adjoining wall) ---
function oracleLineIntersect(x1: number, y1: number, x2: number, y2: number, x3: number, y3: number, x4: number, y4: number) {
  const denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1);
  if (denom === 0) return null;
  const ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom;
  const ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom;
  if (ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1) return ub;
  return null;
}

function oracleCheck(sx: number, sz: number, rx: number, rz: number, poly: { x: number; y: number }[], wallSegMats: (string | null)[], globalWallMat: string, L: number, W: number, wallOpenings: any[] = []) {
  let lossDb = 0;
  if (!Number.isFinite(L) || !Number.isFinite(W) || L <= 0 || W <= 0) {
    return 0;
  }
  const p1x = (sx / L) + 0.5;
  const p1z = (sz / W) + 0.5;
  const p2x = (rx / L) + 0.5;
  const p2z = (rz / W) + 0.5;

  for (let i = 0; i < poly.length; i++) {
    const nextI = (i + 1) % poly.length;
    const opening = wallOpenings[i];
    if (opening === 'full') continue;
    const hitAt = oracleLineIntersect(p1x, p1z, p2x, p2z, poly[i].x, poly[i].y, poly[nextI].x, poly[nextI].y);
    if (hitAt === null) continue;
    if (opening && typeof opening === 'object' && hitAt >= opening.start && hitAt <= opening.end) {
      continue;
    }
    const matId = wallSegMats[i] || globalWallMat;
    const mat = MATERIALS.walls.find((m) => m.id === matId);
    if (!mat || !Number.isFinite(mat.tl)) {
      throw new Error(`Unknown wall material "${matId}" — cannot compute transmission loss`);
    }
    lossDb += mat.tl;
  }
  return lossDb;
}
// --- end oracle ---

// The functions under test are the engine's own.
const E: any = audioEngine;
const lineIntersect = (...a: number[]): number | null => E.lineIntersect(...a);
const checkWallIntersections = (sx: number, sz: number, rx: number, rz: number, poly: { x: number; y: number }[], mats: (string | null)[], g: string, L: number, W: number, ops: any[] = []): number => E.checkWallIntersections(sx, sz, rx, rz, poly, mats, g, L, W, ops);

check('differential: the real engine equals the independent per-edge oracle on every path that does not pass through a polygon vertex', () => {
  const polys = [
    [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }],
    [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 0.5 }, { x: 0.5, y: 0.5 }, { x: 0.5, y: 1 }, { x: 0, y: 1 }], // L-shaped
  ];
  const coords = [-9, -6, -4, -1, 0, 1, 4, 6, 9];
  const openingSets: any[][] = [[], ['full', null, null, null], [null, { start: 0.2, end: 0.8 }, null, null], [null, null, null, { start: 0, end: 1 }]];
  const dims: [number, number][] = [[10, 10], [8, 5], [0, 5], [10, NaN], [-3, 4]];
  const touchesVertex = (poly: { x: number; y: number }[], sx: number, sz: number, rx: number, rz: number, L: number, W: number) => {
    if (!(L > 0 && W > 0 && Number.isFinite(L) && Number.isFinite(W))) return false;
    const [p1x, p1z, p2x, p2z] = [sx / L + 0.5, sz / W + 0.5, rx / L + 0.5, rz / W + 0.5];
    return poly.some((_, i) => { const h = oracleLineIntersect(p1x, p1z, p2x, p2z, poly[i].x, poly[i].y, poly[(i + 1) % poly.length].x, poly[(i + 1) % poly.length].y); return h !== null && (h <= 1e-9 || h >= 1 - 1e-9); });
  };
  let compared = 0, skippedVertex = 0;
  for (const poly of polys) for (const [L, W] of dims) for (const ops of openingSets)
    for (const globalMat of ['drywall', 'concrete', 'no_such_material'])
    for (const sx of coords) for (const rx of coords) for (const sz of [-3, 0, 3]) for (const rz of [-3, 0, 3]) {
      if (touchesVertex(poly, sx, sz, rx, rz, L, W)) { skippedVertex++; continue; }
      const mats = poly.map((_, i) => (i === 1 ? 'glass' : null));
      const run = (fn: typeof checkWallIntersections) => { try { return fn(sx, sz, rx, rz, poly, mats, globalMat, L, W, ops); } catch (e) { return `THROW:${(e as Error).message}`; } };
      const a = run(oracleCheck as any), b = run(checkWallIntersections);
      assert.equal(a, b, `oracle=${a} real=${b} for (${sx},${sz})->(${rx},${rz}) L=${L} W=${W} mat=${globalMat}`);
      compared++;
    }
  for (const [x1, y1, x2, y2, x3, y3, x4, y4] of [[0,0,10,10,0,10,10,0],[0,0,10,0,0,5,10,5],[0,0,1,1,5,0,5,-1],[-5,0,5,0,0,-5,0,5]]) {
    assert.equal(lineIntersect(x1,y1,x2,y2,x3,y3,x4,y4), oracleLineIntersect(x1,y1,x2,y2,x3,y3,x4,y4)); compared++;
  }
  assert.ok(compared > 1000, `expected a broad comparison grid, only compared ${compared}`);
  assert.ok(skippedVertex > 0, 'the grid must include vertex-touching paths so the exclusion is exercised');
});

check('lineIntersect finds the crossing point of two segments that cross in the middle', () => {
  const r = lineIntersect(0, 0, 10, 10, 0, 10, 10, 0); // X shape, crosses at (5,5)
  assert.equal(r, 0.5);
});

check('lineIntersect returns null for parallel, non-intersecting segments', () => {
  assert.equal(lineIntersect(0, 0, 10, 0, 0, 5, 10, 5), null);
});

check('lineIntersect returns null when segments would only cross if extended beyond their bounds', () => {
  assert.equal(lineIntersect(0, 0, 1, 1, 5, 0, 5, -1), null);
});

check('checkWallIntersections returns 0 (not NaN/Infinity) for a non-positive or non-finite L or W', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  assert.equal(checkWallIntersections(-4, 0, 4, 0, poly, [null, null, null, null], 'drywall', 0, 10), 0);
  assert.equal(checkWallIntersections(-4, 0, 4, 0, poly, [null, null, null, null], 'drywall', -5, 10), 0);
  assert.equal(checkWallIntersections(-4, 0, 4, 0, poly, [null, null, null, null], 'drywall', NaN, 10), 0);
});

check('checkWallIntersections sums material transmission loss for each wall segment crossed', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  const L = 10, W = 10;
  const loss = checkWallIntersections(-6, 0, 6, 0, poly, [null, null, null, null], 'drywall', L, W);
  const tl = MATERIALS.walls.find((m) => m.id === 'drywall')!.tl;
  assert.equal(loss, 2 * tl, `expected 2 crossed drywall segments at ${tl}dB each = ${2 * tl}, got ${loss}`);
});

check('an unknown material id throws instead of being replaced by an invented 30 dB loss', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  assert.throws(
    () => checkWallIntersections(-6, 0, 6, 0, poly, [null, null, null, null], 'no_such_material', 10, 10),
    /Unknown wall material "no_such_material"/,
  );
});

check('a per-segment material overrides the global wall material for that segment only', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  // Line crosses segment 1 (x=1 wall) and segment 3 (x=0 wall). Override only segment 1 with concrete.
  const drywallTl = MATERIALS.walls.find((m) => m.id === 'drywall')!.tl;
  const concreteTl = MATERIALS.walls.find((m) => m.id === 'concrete')!.tl;
  const loss = checkWallIntersections(-6, 0, 6, 0, poly, [null, 'concrete', null, null], 'drywall', 10, 10);
  assert.equal(loss, drywallTl + concreteTl, `expected one drywall + one concrete crossing = ${drywallTl + concreteTl}, got ${loss}`);
});

check('a fully-open wall segment contributes zero loss even when geometrically crossed', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  const L = 10, W = 10;
  const loss = checkWallIntersections(-6, 0, 6, 0, poly, [null, null, null, null], 'drywall', L, W, ['full', 'full', 'full', 'full']);
  assert.equal(loss, 0);
});

check('a partial opening (doorway) lets the sound path through only when it crosses within the gap range', () => {
  const poly = [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }];
  const L = 10, W = 10;
  const loss = checkWallIntersections(-6, 0, 6, 0, poly, [null, null, null, null], 'drywall', L, W, [null, null, null, { start: 0, end: 1 }]);
  const tl = MATERIALS.walls.find((m) => m.id === 'drywall')!.tl;
  assert.equal(loss, tl, `expected only the other (non-doorway) wall's ${tl}dB, got ${loss}`);
});

console.log(`\n=== ${passed} passed ===`);
