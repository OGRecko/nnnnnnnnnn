/**
 * Recovery for saved projects that reference a speaker ID which is no longer in the live catalog.
 *
 * Rules (see SAVED-PROJECT-SPEAKER-REFERENCES.md):
 *  - Archived and never-existed IDs are told apart using the generated archive index (src/data/archivedSpeakers.json).
 *  - A replacement is ALWAYS an explicit per-source choice by the person. Nothing is auto-remapped. An archive entry's
 *    `redirectTo` is only a SUGGESTION shown to the person.
 *  - Only sources whose ID is unresolved can be replaced; a resolved source can never be silently re-pointed.
 *  - Archived records are never restored to make an old project open.
 *  - Every replacement is recorded in the project (`speakerReplacements`) so the history is visible and survives re-saves.
 *  - The original file is never modified: replacements apply to an in-memory copy.
 */
import speakerData from '../data/speakers.json';
import archivedIndex from '../data/archivedSpeakers.json';
import { speakerTypeLabel } from './speakers';

export interface ArchivedSpeakerEntry { brand: string; model: string; reason: string; archivedDate: string | null; source: string; redirectTo?: string }
export type UnresolvedStatus = 'archived' | 'unknown';

export interface UnresolvedSpeakerRef {
  sourceId: string;
  /** 1-based position of the source in the project, for display. */
  sourceNumber: number;
  speakerId: string;
  status: UnresolvedStatus;
  /** The brand/model the source was saved with, if present in the file. Display only. */
  savedBrand?: string;
  savedModel?: string;
  archived?: Pick<ArchivedSpeakerEntry, 'brand' | 'model' | 'reason' | 'archivedDate'>;
  /** A live speaker the archive notes point to. A suggestion only; it is never applied automatically. */
  suggestedReplacementId?: string;
}

export interface SpeakerReplacementRecord {
  sourceId: string;
  originalSpeakerId: string;
  originalStatus: UnresolvedStatus;
  originalBrand?: string;
  originalModel?: string;
  replacementSpeakerId: string;
  replacementBrand: string;
  replacementModel: string;
}

export const MAX_SPEAKER_REPLACEMENT_RECORDS = 200;
const MAX_ID_CHARS = 100;

interface LiveSpec { id: string; brand: string; model: string; category: string; sensitivity?: { value?: number | null; status?: string; reference?: string | null } | null; impedance?: { value?: number | null } | null }
const LIVE: ReadonlyMap<string, LiveSpec> = new Map((speakerData as unknown as LiveSpec[]).map((s) => [s.id, s]));
const ARCHIVED: Readonly<Record<string, ArchivedSpeakerEntry>> = (archivedIndex as { entries: Record<string, ArchivedSpeakerEntry> }).entries;
const hasOwn = (o: object, k: string) => Object.prototype.hasOwnProperty.call(o, k);
const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v);
const text = (v: unknown, max = 100): string | undefined => (typeof v === 'string' && v.length > 0 ? v.replace(/[\u0000-\u001f\u007f]/g, '').slice(0, max) : undefined);

export const isLiveSpeakerId = (id: unknown): id is string => typeof id === 'string' && LIVE.has(id);
export const getLiveSpeaker = (id: string): LiveSpec | undefined => (typeof id === 'string' && LIVE.has(id) ? LIVE.get(id) : undefined);
export const archivedSpeakerCount = (): number => Object.keys(ARCHIVED).length;

/** Classify an ID that is not live. Own-property lookup only: '__proto__' / 'constructor' are 'unknown', not archived. */
export function classifySpeakerId(id: string): UnresolvedStatus {
  return hasOwn(ARCHIVED, id) ? 'archived' : 'unknown';
}

/**
 * Every source whose `speakerId` is set but not live. Empty/absent IDs are not references. Non-string IDs are reported
 * as 'unknown' with their string form so the person can still repair the project. Sources without a string `id` cannot be
 * addressed individually and are reported with an empty sourceId (the caller must reject the project).
 */
export function findUnresolvedSpeakerRefs(rawProject: unknown): UnresolvedSpeakerRef[] {
  if (!isRecord(rawProject) || !Array.isArray(rawProject.sources)) return [];
  const out: UnresolvedSpeakerRef[] = [];
  rawProject.sources.forEach((src, index) => {
    if (!isRecord(src)) return;
    const raw = src.speakerId;
    if (raw === undefined || raw === null || raw === '') return;
    if (typeof raw === 'string' && LIVE.has(raw)) return;
    const speakerId = text(typeof raw === 'string' ? raw : String(raw), MAX_ID_CHARS) ?? '(invalid)';
    const status: UnresolvedStatus = typeof raw === 'string' ? classifySpeakerId(raw) : 'unknown';
    const ref: UnresolvedSpeakerRef = {
      sourceId: typeof src.id === 'string' ? src.id : '',
      sourceNumber: index + 1,
      speakerId, status,
      savedBrand: text(src.brand), savedModel: text(src.model),
    };
    if (status === 'archived') {
      const a = ARCHIVED[raw as string];
      ref.archived = { brand: a.brand, model: a.model, reason: a.reason, archivedDate: a.archivedDate };
      if (a.redirectTo && LIVE.has(a.redirectTo)) ref.suggestedReplacementId = a.redirectTo;
    }
    out.push(ref);
  });
  return out;
}

/** The fields of a source that come from its speaker. One definition, used wherever a speaker is assigned to a source. */
export function sourceFieldsFromSpeaker(spec: LiveSpec) {
  const sens = spec.sensitivity?.value ?? null;
  return {
    speakerId: spec.id, brand: spec.brand, model: spec.model, type: speakerTypeLabel(spec.category),
    sens, manufacturerSensitivityDb: sens,
    sensitivityStatus: spec.sensitivity?.status ?? 'UNAVAILABLE',
    manufacturerSensitivityReference: spec.sensitivity?.reference ?? null,
    speakerImpedanceOhm: spec.impedance?.value ?? null,
  };
}

export type ApplyReplacementsResult =
  | { ok: true; project: Record<string, unknown>; replacements: SpeakerReplacementRecord[]; droppedDirectivitySourceIds: string[] }
  | { ok: false; error: string };

/**
 * Apply explicit per-source replacement choices to a COPY of the project.
 * `choices` maps sourceId -> replacement speaker ID. Every unresolved source must have a live choice, and choices for
 * anything else are refused.
 */
export function applySpeakerReplacements(rawProject: unknown, choices: Record<string, string>): ApplyReplacementsResult {
  if (!isRecord(rawProject) || !Array.isArray(rawProject.sources)) return { ok: false, error: 'Project has no sources to repair.' };
  if (!isRecord(choices)) return { ok: false, error: 'Replacement choices must be an object.' };
  const unresolved = findUnresolvedSpeakerRefs(rawProject);
  if (unresolved.some((u) => !u.sourceId)) return { ok: false, error: 'A source with an unknown speaker has no ID, so it cannot be repaired. The project was not changed.' };
  const byId = new Map(unresolved.map((u) => [u.sourceId, u]));
  if (byId.size !== unresolved.length) return { ok: false, error: 'Two sources share an ID, so replacements cannot be applied unambiguously. The project was not changed.' };

  for (const key of Object.keys(choices)) {
    if (!byId.has(key)) return { ok: false, error: 'A replacement was supplied for a source that does not need one. Replacements apply only to sources whose speaker is missing.' };
  }
  for (const u of unresolved) {
    const pick = hasOwn(choices, u.sourceId) ? choices[u.sourceId] : undefined;
    if (typeof pick !== 'string' || pick === '') return { ok: false, error: `Choose a replacement speaker for source ${u.sourceNumber} (${u.speakerId}).` };
    if (!LIVE.has(pick)) return { ok: false, error: `The replacement "${text(pick, MAX_ID_CHARS) ?? ''}" is not a speaker in the current catalog.` };
  }

  const priorRecords = Array.isArray(rawProject.speakerReplacements) ? (rawProject.speakerReplacements as unknown[]) : [];
  const replacements: SpeakerReplacementRecord[] = [];
  const dropped: string[] = [];
  const sources = (rawProject.sources as unknown[]).map((src) => {
    if (!isRecord(src) || typeof src.id !== 'string' || !byId.has(src.id)) return src;
    const u = byId.get(src.id)!;
    const spec = LIVE.get(choices[src.id])!;
    const next: Record<string, unknown> = { ...src, ...sourceFieldsFromSpeaker(spec) };
    // Polar data was supplied for the ORIGINAL speaker; it must not silently apply to a different one.
    if (hasOwn(next, 'directivityData') && next.directivityData != null) dropped.push(src.id);
    delete next.directivityData; delete next.isDirectional;
    replacements.push({
      sourceId: src.id, originalSpeakerId: u.speakerId, originalStatus: u.status,
      originalBrand: u.savedBrand ?? u.archived?.brand, originalModel: u.savedModel ?? u.archived?.model,
      replacementSpeakerId: spec.id, replacementBrand: spec.brand, replacementModel: spec.model,
    });
    return next;
  });

  const history = [...priorRecords, ...replacements].slice(-MAX_SPEAKER_REPLACEMENT_RECORDS);
  return { ok: true, project: { ...rawProject, sources, speakerReplacements: history }, replacements, droppedDirectivitySourceIds: dropped };
}

/** Validate a stored replacement history. Returns a sanitized copy, or undefined when the field is invalid. */
export function sanitizeSpeakerReplacements(value: unknown): SpeakerReplacementRecord[] | undefined {
  if (value === undefined || value === null) return [];
  if (!Array.isArray(value) || value.length > MAX_SPEAKER_REPLACEMENT_RECORDS) return undefined;
  const out: SpeakerReplacementRecord[] = [];
  for (const r of value) {
    if (!isRecord(r)) return undefined;
    const sourceId = text(r.sourceId, MAX_ID_CHARS), original = text(r.originalSpeakerId, MAX_ID_CHARS), repl = text(r.replacementSpeakerId, MAX_ID_CHARS);
    if (!sourceId || !original || !repl) return undefined;
    if (r.originalStatus !== 'archived' && r.originalStatus !== 'unknown') return undefined;
    out.push({
      sourceId, originalSpeakerId: original, originalStatus: r.originalStatus,
      originalBrand: text(r.originalBrand), originalModel: text(r.originalModel),
      replacementSpeakerId: repl, replacementBrand: text(r.replacementBrand) ?? '', replacementModel: text(r.replacementModel) ?? '',
    });
  }
  return out;
}

/** Search the LIVE catalog for the replacement picker. Pure and bounded. */
export function searchLiveSpeakers(query: string, limit = 40): Array<{ id: string; brand: string; model: string; type: string; unavailable: boolean }> {
  const q = String(query ?? '').toLowerCase().replace(/[^a-z0-9.\s-]/g, ' ').trim().slice(0, 100);
  const tokens = q.split(/\s+/).filter(Boolean).slice(0, 6);
  const max = Number.isFinite(limit) ? Math.max(1, Math.min(100, Math.floor(limit))) : 40;
  const rows: Array<{ s: LiveSpec; score: number }> = [];
  for (const s of LIVE.values()) {
    const hay = `${s.brand} ${s.model} ${s.id}`.toLowerCase();
    if (!tokens.every((t) => hay.includes(t))) continue;
    const name = `${s.brand} ${s.model}`.toLowerCase();
    const score = tokens.length === 0 ? 0 : (s.id === q ? 0 : name === q ? 1 : name.startsWith(q) ? 2 : s.brand.toLowerCase().startsWith(tokens[0]) ? 3 : 4);
    rows.push({ s, score });
  }
  rows.sort((a, b) => a.score - b.score || a.s.brand.localeCompare(b.s.brand) || a.s.model.localeCompare(b.s.model));
  return rows.slice(0, max).map(({ s }) => ({ id: s.id, brand: s.brand, model: s.model, type: speakerTypeLabel(s.category), unavailable: (s as { overallStatus?: string }).overallStatus === 'UNAVAILABLE' }));
}
