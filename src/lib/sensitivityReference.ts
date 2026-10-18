/**
 * Normalisation of a published sensitivity to the DSP reference, dB SPL @ 1 W / 1 m. The ONE place this rule lives:
 * resolveSensitivity() (catalog records) and sourceSensitivityDb() (project sources) both call it, so they cannot drift.
 *
 * Deliberately conservative. Only these are normalised:
 *  - 1 W / 1 m, including descriptive text that STATES it ("Axial, half-space measurement, 1 W/1 m (footnote 1)"): used as published.
 *  - 2.83 V / 1 m: converted using the nominal impedance, and ONLY when it is known (never an assumed 8 ohm).
 * Everything else returns null and the caller reports a flagged fallback; nothing is reinterpreted as 1 W / 1 m. In particular
 * distance and power conversions (1 W / 10 ft, EIA 1 mW / 30 ft) and the bare unit "W/m" are NOT converted: they would rest on a
 * free-field inverse-distance model or an unverified reading of an old manual. Those records stay flagged until someone confirms
 * the conversion from the source document.
 */
export type SensitivityReferenceKind = 'one-watt-one-metre' | 'voltage';

export interface ParsedSensitivityReference { kind: SensitivityReferenceKind; volts?: number }

/** Classifies a reference string. Empty/blank is treated as 1 W / 1 m by the callers, not here. */
export function parseSensitivityReference(reference: string): ParsedSensitivityReference | null {
  const r = reference.trim();
  if (/^1\s*W\s*\/\s*1\s*m$/i.test(r)) return { kind: 'one-watt-one-metre' };
  // An explicit 1 W/1 m with descriptive text around it, e.g. the Electro-Voice ZX footnote wording.
  if (/^[A-Za-z][A-Za-z ,\-]*\b1\s*W\s*\/\s*1\s*m\b(?:\s*\([^)]*\))?$/.test(r)) return { kind: 'one-watt-one-metre' };
  if (/^2\.83\s*(?:V|Vrms)\s*\/\s*1\s*m$/i.test(r)) return { kind: 'voltage', volts: 2.83 };
  return null;
}

/**
 * dB SPL @ 1 W / 1 m for a published value and its reference, or null when it cannot be normalised without guessing.
 * `impedanceOhm` is used only for voltage references.
 */
export function normalizeSensitivityTo1W1m(rawDb: number, reference: string | null | undefined, impedanceOhm: unknown): number | null {
  if (typeof rawDb !== 'number' || !Number.isFinite(rawDb) || rawDb <= 0) return null;
  const ref = typeof reference === 'string' ? reference.trim() : '';
  if (ref === '') return rawDb;
  const p = parseSensitivityReference(ref);
  if (!p) return null;
  if (p.kind === 'one-watt-one-metre') return rawDb;
  if (typeof impedanceOhm !== 'number' || !Number.isFinite(impedanceOhm) || impedanceOhm <= 0) return null;
  const watts = (p.volts! * p.volts!) / impedanceOhm;
  return Number.isFinite(watts) && watts > 0 ? rawDb - 10 * Math.log10(watts) : null;
}
