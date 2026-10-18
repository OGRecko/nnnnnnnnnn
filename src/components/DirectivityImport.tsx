import React, { useId, useState } from 'react';
import { useStore, type Source } from '../store/useStore';
import { describeDirectivityData, importDirectivityFile, type DirectivityStatus } from '../lib/directivityImport';

type Theme = 'dark' | 'light';
const hz = (n: number) => (n >= 1000 ? `${n / 1000} kHz` : `${n} Hz`);

export interface DirectivityImportViewProps {
  status: DirectivityStatus;
  yawDeg?: number;
  pitchDeg?: number;
  onAim?: (aim: { yawDeg?: number; pitchDeg?: number }) => void;
  error?: string | null;
  busy?: boolean;
  theme?: Theme;
  /** Source number for labels, 1-based. */
  sourceNumber: number;
  onFile: (file: File) => void;
  onRemove: () => void;
}

/** Presentational part, free of store access so it can be rendered and tested on its own. */
export function DirectivityImportView({ status, yawDeg = 0, pitchDeg = 0, onAim, error = null, busy = false, theme = 'dark', sourceNumber, onFile, onRemove }: DirectivityImportViewProps) {
  const inputId = useId(); const descId = useId();
  const muted = theme === 'dark' ? 'text-[#a7adb7]' : 'text-[#4b5563]';
  const btn = theme === 'dark' ? 'bg-[#2a2d33] text-[#e6e8eb] hover:bg-[#343841]' : 'bg-[#e5e7eb] text-[#1b1f24] hover:bg-[#d1d5db]';
  const warn = theme === 'dark' ? 'bg-[#3d1a1a] text-[#ffb4b4]' : 'bg-[#fde8e8] text-[#8a1c1c]';
  return (
    <div className="mt-2 text-[10px] leading-snug" data-testid="directivity-import">
      <div className="font-semibold">Directivity</div>
      <p id={descId} className={muted}>
        {status.available ? (
          <>Imported by you (not verified by Cavity Audio): {status.pointCount.toLocaleString('en-US')} directions at {status.frequenciesHz.map(hz).join(', ')}.{' '}
            <strong>Experimental.</strong> {status.coveredBandsHz.length > 0 ? `The room simulation receives this data for the ${status.coveredBandsHz.map(hz).join(', ')} band${status.coveredBandsHz.length === 1 ? '' : 's'}, but its directional source only approximates the pattern (in testing it reproduced a small fraction of it), so do not rely on directional results. ` : 'No simulated octave band is within half an octave of this data, so it has no effect. '}
            {status.uncoveredBandsHz.length > 0 ? `${status.uncoveredBandsHz.map(hz).join(', ')} stay omnidirectional.` : 'All simulated bands receive the data.'}</>
        ) : (
          <>Not available: omnidirectional assumed. No polar data is built in for this speaker. Import your own CSV or JSON to use directional behavior.</>
        )}
      </p>
      <div className="mt-1 flex items-center gap-2 flex-wrap">
        <label htmlFor={inputId} className={`px-2 py-1 rounded cursor-pointer focus-within:outline focus-within:outline-2 ${btn} ${busy ? 'opacity-50 pointer-events-none' : ''}`}>
          {busy ? 'Reading…' : status.available ? 'Replace polar data…' : 'Import polar data…'}
          <input id={inputId} type="file" accept=".csv,.json,.txt,text/csv,application/json,text/plain" className="sr-only" disabled={busy}
            aria-label={`Import polar data for source ${sourceNumber} (CSV or JSON)`} aria-describedby={descId}
            onChange={(e) => { const f = e.target.files?.[0]; e.target.value = ''; if (f) onFile(f); }} />
        </label>
        {status.available && <button type="button" className={`px-2 py-1 rounded ${btn}`} onClick={onRemove} aria-label={`Remove polar data from source ${sourceNumber}`}>Remove</button>}
      </div>
      {status.available && onAim && (
        <fieldset className="mt-2 border rounded p-1.5" style={{ borderColor: theme === 'dark' ? '#2a2d33' : '#d0d5dd' }}>
          <legend className="px-1 font-semibold">Aim source {sourceNumber}</legend>
          <p className={muted}>Axes are the room's X (length) and Y (width), the same as the Source X/Y position fields. 0° faces toward higher Y; positive angles turn toward lower X.</p>
          <div className="mt-1 flex gap-1 flex-wrap" role="group" aria-label={`Aim source ${sourceNumber} toward a wall`}>
            {([['Toward +Y', 0], ['Toward −X', 90], ['Toward −Y', 180], ['Toward +X', 270]] as const).map(([label, yaw]) => (
              <button key={label} type="button" aria-pressed={Math.round(((yawDeg % 360) + 360) % 360) === yaw} className={`px-2 py-1 rounded ${btn} aria-pressed:outline aria-pressed:outline-2`} onClick={() => onAim({ yawDeg: yaw })}>{label}</button>
            ))}
          </div>
          <div className="mt-1 flex gap-3 flex-wrap">
            <label className="flex items-center gap-1">Aim (°)
              <input type="number" min={-360} max={360} step={5} value={yawDeg} aria-label={`Aim angle of source ${sourceNumber} in degrees`} className={`w-16 px-1 py-0.5 rounded border ${theme === 'dark' ? 'bg-[#0f1114] border-[#3a3e46]' : 'bg-white border-[#9aa3af]'}`}
                onChange={(e) => { const n = e.target.valueAsNumber; if (Number.isFinite(n)) onAim({ yawDeg: Math.max(-360, Math.min(360, n)) }); }} />
            </label>
            <label className="flex items-center gap-1">Tilt up (°)
              <input type="number" min={-90} max={90} step={5} value={pitchDeg} aria-label={`Upward tilt of source ${sourceNumber} in degrees`} className={`w-16 px-1 py-0.5 rounded border ${theme === 'dark' ? 'bg-[#0f1114] border-[#3a3e46]' : 'bg-white border-[#9aa3af]'}`}
                onChange={(e) => { const n = e.target.valueAsNumber; if (Number.isFinite(n)) onAim({ pitchDeg: Math.max(-90, Math.min(90, n)) }); }} />
            </label>
          </div>
        </fieldset>
      )}
      <div role="alert" aria-live="assertive" className={error ? `mt-1 p-1.5 rounded ${warn}` : 'sr-only'}>{error ?? ''}</div>
    </div>
  );
}

/** Connected control for one source. Imported data is the user's own: it is stored on the source and saved with the project. */
export default function DirectivityImport({ source, sourceNumber }: { source: Source; sourceNumber: number }) {
  const theme = useStore((s) => s.theme);
  const updateSource = useStore((s) => s.updateSource);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const status = describeDirectivityData(source.isDirectional, source.directivityData);
  return (
    <DirectivityImportView
      status={status} error={error} busy={busy} theme={theme} sourceNumber={sourceNumber}
      yawDeg={source.yawDeg ?? 0} pitchDeg={source.pitchDeg ?? 0}
      onAim={(aim) => updateSource(source.id, aim)}
      onFile={async (file) => {
        setError(null); setBusy(true);
        try {
          const r = await importDirectivityFile(file);
          if (!r.ok) { setError(r.error); return; }
          updateSource(source.id, { isDirectional: true, directivityData: r.data });
        } finally { setBusy(false); }
      }}
      onRemove={() => { setError(null); updateSource(source.id, { isDirectional: false, directivityData: undefined }); }}
    />
  );
}
