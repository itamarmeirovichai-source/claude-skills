import { useState } from 'react';
import { shareFiles, type PreparedExport } from '../services/exporter';
import { canShareFiles } from '../lib/device';
import { IconShare } from './icons';

// Two tap export: prepare the files, then share or save them. iOS requires the share
// sheet to open straight from a tap, so nothing slow happens between the tap and the sheet.

export function ExportAction({ label, prepare, testId, primary, onDone }: { label: string; prepare: () => Promise<PreparedExport>; testId?: string; primary?: boolean; onDone?: (r: string) => void }) {
  const [state, setState] = useState<'idle' | 'busy' | 'ready' | 'done' | 'error'>('idle');
  const [prep, setPrep] = useState<PreparedExport | null>(null);
  const [msg, setMsg] = useState('');
  if (state === 'ready' && prep) {
    const share = canShareFiles(prep.files);
    return (
      <div className="stack" style={{ gap: 6 }}>
        <p className="small muted">Ready: {prep.files.map((f) => f.name).join(', ')}</p>
        <button
          type="button"
          className="btn btn-primary btn-block"
          data-testid={testId ? `${testId}-share` : undefined}
          onClick={async () => {
            const r = await shareFiles(prep.files, prep.title, prep.record);
            setState('done');
            setMsg(r === 'shared' ? 'Shared.' : r === 'downloaded' ? 'Saved. On iPhone, find it in Files, Downloads.' : 'Cancelled. Nothing was shared.');
            onDone?.(r);
          }}
        >
          <IconShare /> {share ? 'Share or save' : 'Save file'}
        </button>
      </div>
    );
  }
  return (
    <div className="stack" style={{ gap: 6 }}>
      <button
        type="button"
        className={`btn btn-block ${primary ? 'btn-primary' : 'btn-outline'}`}
        disabled={state === 'busy'}
        data-testid={testId}
        onClick={async () => {
          setState('busy');
          try {
            setPrep(await prepare());
            setState('ready');
          } catch (e) {
            setState('error');
            setMsg((e as Error).message);
          }
        }}
      >
        {state === 'busy' ? 'Preparing…' : label}
      </button>
      {msg && <p className={`small ${state === 'error' ? '' : 'muted'}`} role="status">{msg}</p>}
    </div>
  );
}
