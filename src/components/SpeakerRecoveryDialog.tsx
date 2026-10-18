import React, { useEffect, useId, useMemo, useRef, useState } from 'react';
import { useStore } from '../store/useStore';
import { getLiveSpeaker, searchLiveSpeakers, type UnresolvedSpeakerRef } from '../lib/speakerRecovery';

type Theme = 'dark' | 'light';

const palette = (t: Theme) => t === 'dark'
  ? { panel: 'bg-[#16181c] text-[#e6e8eb] border-[#2a2d33]', muted: 'text-[#a7adb7]', field: 'bg-[#0f1114] border-[#3a3e46] text-[#e6e8eb]', row: 'border-[#2a2d33]', hover: 'hover:bg-[#202226]', sel: 'bg-[#1f3a5f]', warn: 'bg-[#3b2f12] text-[#ffd98a]', info: 'bg-[#1c2733] text-[#b9d4f0]', btn: 'bg-[#2d6cdf] text-white hover:bg-[#3b7af0]', btn2: 'bg-[#2a2d33] text-[#e6e8eb] hover:bg-[#343841]', err: 'bg-[#3d1a1a] text-[#ffb4b4]' }
  : { panel: 'bg-white text-[#1b1f24] border-[#d0d5dd]', muted: 'text-[#4b5563]', field: 'bg-white border-[#9aa3af] text-[#1b1f24]', row: 'border-[#e5e7eb]', hover: 'hover:bg-[#f3f4f6]', sel: 'bg-[#dbeafe]', warn: 'bg-[#fff4d6] text-[#6b4a00]', info: 'bg-[#e8f1fb] text-[#18416b]', btn: 'bg-[#1d4ed8] text-white hover:bg-[#1e40af]', btn2: 'bg-[#e5e7eb] text-[#1b1f24] hover:bg-[#d1d5db]', err: 'bg-[#fde8e8] text-[#8a1c1c]' };

function ReplacementPicker({ refItem, value, onChoose, theme, labelId }: { refItem: UnresolvedSpeakerRef; value: string | undefined; onChoose: (id: string | null) => void; theme: Theme; labelId: string }) {
  const c = palette(theme);
  const [query, setQuery] = useState('');
  const [active, setActive] = useState(0);
  const listId = useId();
  const results = useMemo(() => searchLiveSpeakers(query, 30), [query]);
  const chosen = value ? getLiveSpeaker(value) : undefined;
  const suggested = refItem.suggestedReplacementId ? getLiveSpeaker(refItem.suggestedReplacementId) : undefined;

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive((i) => Math.min(results.length - 1, i + 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive((i) => Math.max(0, i - 1)); }
    else if (e.key === 'Enter' && results[active]) { e.preventDefault(); e.stopPropagation(); onChoose(results[active].id); }
  };

  if (chosen) {
    return (
      <div className="flex items-center gap-2 flex-wrap" data-testid={`chosen-${refItem.sourceId}`}>
        <span className={`px-2 py-1 rounded text-sm ${c.sel}`}>Replacement: <strong>{chosen.brand} {chosen.model}</strong></span>
        <button type="button" className={`px-2 py-1 rounded text-sm ${c.btn2}`} onClick={() => onChoose(null)}>Change</button>
      </div>
    );
  }
  return (
    <div>
      {suggested && (
        <div className={`mb-2 p-2 rounded text-sm ${c.info}`}>
          The archive notes point to <strong>{suggested.brand} {suggested.model}</strong> for this speaker. It is only a suggestion; nothing is replaced until you choose it.{' '}
          <button type="button" className={`ml-1 px-2 py-0.5 rounded ${c.btn2}`} onClick={() => onChoose(suggested.id)}>Use {suggested.brand} {suggested.model}</button>
        </div>
      )}
      <input
        type="search" value={query} onChange={(e) => { setQuery(e.target.value); setActive(0); }} onKeyDown={onKeyDown}
        placeholder="Search brand or model" autoComplete="off" spellCheck={false} maxLength={100}
        aria-labelledby={labelId} aria-controls={listId} aria-autocomplete="list" role="combobox" aria-expanded="true"
        aria-activedescendant={results[active] ? `${listId}-${results[active].id}` : undefined}
        className={`w-full px-3 py-2 rounded border text-sm ${c.field}`}
      />
      <ul id={listId} role="listbox" aria-label="Replacement speakers" className={`mt-1 max-h-44 overflow-y-auto rounded border ${c.row}`}>
        {results.length === 0 && <li role="presentation" className={`px-3 py-2 text-sm ${c.muted}`}>No speakers match "{query.slice(0, 40)}".</li>}
        {results.map((r, i) => (
          <li key={r.id} id={`${listId}-${r.id}`} role="option" aria-selected={i === active} onMouseEnter={() => setActive(i)} onClick={() => onChoose(r.id)}
              className={`px-3 py-1.5 text-sm cursor-pointer flex justify-between gap-2 ${c.hover} ${i === active ? c.sel : ''}`}>
            <span>{r.brand} {r.model}</span>
            <span className={c.muted}>{r.type}{r.unavailable ? ' · limited data' : ''}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export interface SpeakerRecoveryViewProps {
  unresolved: UnresolvedSpeakerRef[];
  choices: Record<string, string>;
  onChoose: (sourceId: string, speakerId: string | null) => void;
  onSubmit: () => void;
  onCancel: () => void;
  error?: string | null;
  theme?: Theme;
}

/** Presentational dialog: no store access, so it can be rendered and tested on its own. */
export function SpeakerRecoveryView({ unresolved, choices, onChoose, onSubmit, onCancel, error = null, theme = 'dark' }: SpeakerRecoveryViewProps) {
  const c = palette(theme);
  const titleId = useId(); const descId = useId();
  const ref = useRef<HTMLDivElement>(null);
  const missing = unresolved.filter((u) => !choices[u.sourceId]).length;
  const ready = missing === 0;

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    ref.current?.querySelector<HTMLElement>('[data-autofocus]')?.focus();
    return () => { previous?.focus?.(); };
  }, []);

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') { e.stopPropagation(); onCancel(); return; }
    if (e.key !== 'Tab' || !ref.current) return;
    const f = [...ref.current.querySelectorAll<HTMLElement>('button:not([disabled]), input, [tabindex]:not([tabindex="-1"])')];
    if (f.length === 0) return;
    const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center bg-black/60 p-4" onKeyDown={onKeyDown}>
      <div ref={ref} role="dialog" aria-modal="true" aria-labelledby={titleId} aria-describedby={descId} className={`w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-lg border shadow-xl p-5 ${c.panel}`}>
        <h2 id={titleId} tabIndex={-1} data-autofocus className="text-lg font-semibold outline-none">Some speakers in this project are no longer available</h2>
        <p id={descId} className={`mt-1 text-sm ${c.muted}`}>
          Choose a replacement for each affected source to open the project. Your file is not changed. Nothing is replaced automatically, and the replacements are recorded in the project once you save it.
        </p>
        <div className="mt-4 space-y-4">
          {unresolved.map((u) => {
            const labelId = `${titleId}-${u.sourceId}`;
            return (
              <fieldset key={u.sourceId} className={`border rounded p-3 ${c.row}`}>
                <legend id={labelId} className="px-1 text-sm font-medium">Source {u.sourceNumber}: {u.savedBrand || u.archived?.brand || 'Unknown speaker'} {u.savedModel || u.archived?.model || ''}</legend>
                {u.status === 'archived' ? (
                  <p className={`mb-2 p-2 rounded text-sm ${c.warn}`}><strong>Archived.</strong> This speaker was removed from the catalog{u.archived?.archivedDate ? ` on ${u.archived.archivedDate}` : ''}. {u.archived?.reason}</p>
                ) : (
                  <p className={`mb-2 p-2 rounded text-sm ${c.warn}`}><strong>Not in the catalog.</strong> The ID "{u.speakerId}" was never a catalog speaker, so the file may have been edited or damaged.</p>
                )}
                <ReplacementPicker refItem={u} value={choices[u.sourceId]} onChoose={(id) => onChoose(u.sourceId, id)} theme={theme} labelId={labelId} />
              </fieldset>
            );
          })}
        </div>
        <div role="alert" aria-live="assertive" className={error ? `mt-4 p-2 rounded text-sm ${c.err}` : 'sr-only'}>{error ?? ''}</div>
        <div className="mt-5 flex items-center justify-end gap-2 flex-wrap">
          <span className={`text-sm ${c.muted}`} aria-live="polite">{ready ? `${unresolved.length} replacement${unresolved.length === 1 ? '' : 's'} chosen` : `Choose a replacement for ${missing} more source${missing === 1 ? '' : 's'}`}</span>
          <button type="button" className={`px-3 py-2 rounded text-sm ${c.btn2}`} onClick={onCancel}>Cancel, don't open</button>
          <button type="button" disabled={!ready} aria-disabled={!ready} className={`px-3 py-2 rounded text-sm font-medium ${c.btn} disabled:opacity-50 disabled:cursor-not-allowed`} onClick={onSubmit}>Open with replacements</button>
        </div>
      </div>
    </div>
  );
}

/** Connected dialog: shown whenever a project was refused only because of missing speakers. */
export default function SpeakerRecoveryDialog() {
  const pending = useStore((s) => s.pendingSpeakerRecovery);
  const resolve = useStore((s) => s.resolveSpeakerRecovery);
  const cancel = useStore((s) => s.cancelSpeakerRecovery);
  const theme = useStore((s) => s.theme);
  const [choices, setChoices] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);

  // A different pending project starts with a clean slate.
  useEffect(() => { setChoices({}); setError(null); }, [pending?.rawProject]);
  if (!pending) return null;

  return (
    <SpeakerRecoveryView
      unresolved={pending.unresolved} choices={choices} error={error} theme={theme}
      onChoose={(sourceId, speakerId) => { setError(null); setChoices((prev) => { const next = { ...prev }; if (speakerId) next[sourceId] = speakerId; else delete next[sourceId]; return next; }); }}
      onCancel={() => { setError(null); cancel(); }}
      onSubmit={() => { const r = resolve(choices); if (r.ok) alert(r.message); else setError(r.error); }}
    />
  );
}
