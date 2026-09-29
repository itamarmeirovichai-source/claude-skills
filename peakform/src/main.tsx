import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './ui/styles.css';
import { App } from './App';
import { ensureInitialized } from './db/repo';

async function boot() {
  const root = createRoot(document.getElementById('root')!);
  try {
    await ensureInitialized();
  } catch (e) {
    root.render(
      <div style={{ padding: 24, fontFamily: 'system-ui' }}>
        <h1>PeakForm cannot open its storage</h1>
        <p>This browser blocked local storage, for example in a private window. Open PeakForm in normal Safari or from the Home Screen.</p>
        <p style={{ color: '#666' }}>{String((e as Error)?.message ?? e)}</p>
      </div>,
    );
    return;
  }
  root.render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
}

void boot();
