import { useId } from 'react';
import { MUSCLE_BY_ID, type MuscleId } from '../content/muscles';

// Original front and back body diagram with separately addressable regions.
// Drawn for PeakForm. Regions are defined for one half and mirrored.
// Primary = solid fill, secondary = hatched, activity exposure = dotted outline.
// Meaning never depends on colour alone.

export const MAP_W = 100;
export const MAP_H = 220;

const SILHOUETTE_HALF =
  'M50,28 L55,28 L56,33 L66,36 L74,38 L79,44 L80,56 L79,80 L81,88 L80,110 L78,124 L79,134 L74,138 L71,126 L70,112 L70,90 L71,62 L68,64 L67,82 L65,96 L69,108 L70,124 L68,150 L66,160 L67,172 L66,190 L63,204 L66,212 L56,214 L57,204 L56,190 L55,166 L54,160 L53,140 L51,120 L50,120 Z';

type Region = { m: MuscleId; d: string };

const FRONT: Region[] = [
  { m: 'traps_upper', d: 'M54,30 L67,36 L56,37 Z' },
  { m: 'pec_clavicular', d: 'M51,39 L62,38 Q64,41 64,45 L51,47 Z' },
  { m: 'pec_sternal', d: 'M51,48 L64,46 Q68,50 70,56 Q64,63 52,62 L51,60 Z' },
  { m: 'delt_anterior', d: 'M63,37 Q70,36 73,40 L72,54 Q67,50 64,44 Z' },
  { m: 'delt_lateral', d: 'M74,38 Q79,41 79,50 L76,56 L73,54 L74,43 Z' },
  { m: 'serratus_anterior', d: 'M65,63 L70,59 L70.5,70 L66,71 Z' },
  { m: 'biceps', d: 'M72,58 Q77,61 77,72 L74,82 Q71,72 71.5,60 Z' },
  { m: 'brachialis', d: 'M77.5,70 L79,75 L79,85 L75.5,84 Z' },
  { m: 'brachioradialis', d: 'M76,87 L80,90 L78,104 L75,100 Z' },
  { m: 'forearm_flexors', d: 'M71,89 L75.5,88 L74.5,114 L71,113 Z' },
  { m: 'rectus_abdominis', d: 'M51,64 L58.5,64 L59,100 L51,103 Z' },
  { m: 'obliques_core', d: 'M60,64 L67,70 L66,92 L60,99 Z' },
  { m: 'hip_flexors', d: 'M56,104 L63,100 L62,112 L57,114 Z' },
  { m: 'glute_med', d: 'M64,99 L68.5,103 L69,114 L64.5,111 Z' },
  { m: 'adductors', d: 'M51,120 L57,117 Q55.5,134 57,150 L53,141 Z' },
  { m: 'quads', d: 'M58,116 L66,112 Q70,126 68,150 L62,160 L57.5,158 Q55.5,136 58,116 Z' },
  { m: 'gastrocnemius', d: 'M55.5,167 L59,166 L59.5,184 L56.5,183 Z' },
  { m: 'tibialis_anterior', d: 'M60.5,166 L65,165 L63,196 L60.5,196 Z' },
  { m: 'soleus', d: 'M65.2,176 L66.5,180 L64.5,198 L63.5,196 Z' },
];

const BACK: Region[] = [
  { m: 'traps_upper', d: 'M54,30 L69,37 L56,40 Z' },
  { m: 'traps_middle', d: 'M51,39 L63,40 L62,47 L51,48 Z' },
  { m: 'rhomboids', d: 'M51,48.5 L61.5,47.5 L59.5,58 L51,60 Z' },
  { m: 'traps_lower', d: 'M51,60.5 L59.5,58.5 L56,71 L51,75 Z' },
  { m: 'delt_posterior', d: 'M64,37 Q71,36 74,40 L73,53 Q68,47 64,43 Z' },
  { m: 'delt_lateral', d: 'M74.5,38.5 Q79,41 79,50 L76,56 L73.5,53 L75,43 Z' },
  { m: 'rotator_cuff', d: 'M62.5,44 L70,46.5 L68.5,56 L61,56.5 Z' },
  { m: 'teres_major', d: 'M65,57.5 L71,57 L70,62.5 L64,62 Z' },
  { m: 'lats', d: 'M60,59 L63.5,63 L71,63.5 Q70,78 64,92 L57,94 L56,74 Z' },
  { m: 'triceps', d: 'M72,57 Q78,61 78,74 L74,84 Q70.5,72 71.5,58 Z' },
  { m: 'brachioradialis', d: 'M76,87 L80,90 L78,100 L75,97 Z' },
  { m: 'forearm_extensors', d: 'M71,89 L75.5,90 L74.5,114 L71,113 Z' },
  { m: 'erectors', d: 'M51,76 L55.5,73 L57,100 L51,103 Z' },
  { m: 'obliques_core', d: 'M64.5,92 L67.5,86 L68,101 L62,102 Z' },
  { m: 'glute_med', d: 'M58,101 L67.5,99 L68.5,109 L60,108.5 Z' },
  { m: 'glute_max', d: 'M51,106 L60,106.5 Q69,110 68.5,120 Q62,128 51,126 Z' },
  { m: 'adductors', d: 'M51,127.5 L54,128.5 Q53,140 55,150 L51,141 Z' },
  { m: 'hamstrings', d: 'M54.5,128.5 L66.5,124.5 Q69,141 65,158 L58.5,158.5 Q54.5,142 54.5,128.5 Z' },
  { m: 'gastrocnemius', d: 'M56,164 Q62,160 66,166 Q66.5,178 62,184 L58,184 Q55,176 56,164 Z' },
  { m: 'soleus', d: 'M57.5,185.5 L62,185.5 L64.5,182.5 L63,198 L59,198 Z' },
];

export const BODY_REGIONS = { front: FRONT, back: BACK };

export interface MapHighlight {
  primary: MuscleId[];
  secondary: MuscleId[];
  exposure?: MuscleId[];
}

function View({ regions, view, h, patternId, dotId }: { regions: Region[]; view: 'front' | 'back'; h: MapHighlight; patternId: string; dotId: string }) {
  const role = (m: MuscleId): 'primary' | 'secondary' | 'exposure' | null =>
    h.primary.includes(m) ? 'primary' : h.secondary.includes(m) ? 'secondary' : h.exposure?.includes(m) ? 'exposure' : null;
  const draw = (mirror: boolean) => (
    <g transform={mirror ? `translate(${MAP_W},0) scale(-1,1)` : undefined}>
      <path d={SILHOUETTE_HALF} fill="var(--map-base)" stroke="var(--map-edge)" strokeWidth={0.6} strokeLinejoin="round" />
      {regions.map((r, i) => {
        const rr = role(r.m);
        const fill = rr === 'primary' ? 'var(--map-primary)' : rr === 'secondary' ? `url(#${patternId})` : 'transparent';
        return (
          <path
            key={i}
            d={r.d}
            fill={fill}
            stroke={rr === 'exposure' ? 'var(--map-exposure)' : 'var(--map-edge)'}
            strokeWidth={rr === 'exposure' ? 1.1 : 0.45}
            strokeDasharray={rr === 'exposure' ? '1.4 1.2' : undefined}
            data-muscle={r.m}
            data-role={rr ?? 'none'}
          >
            <title>{`${MUSCLE_BY_ID[r.m].shortName}${rr ? `, ${rr}` : ''}`}</title>
          </path>
        );
      })}
    </g>
  );
  return (
    <svg viewBox={`0 0 ${MAP_W} ${MAP_H}`} role="img" aria-label={`${view === 'front' ? 'Front' : 'Back'} view`} data-view={view}>
      <defs>
        <pattern id={patternId} width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="3" height="3" fill="var(--map-base)" />
          <line x1="0" y1="0" x2="0" y2="3" stroke="var(--map-secondary)" strokeWidth="2" />
        </pattern>
        <pattern id={dotId} width="3" height="3" patternUnits="userSpaceOnUse">
          <circle cx="1.5" cy="1.5" r="0.6" fill="var(--map-exposure)" />
        </pattern>
      </defs>
      <ellipse cx="50" cy="16" rx="10" ry="12" fill="var(--map-base)" stroke="var(--map-edge)" strokeWidth={0.6} />
      {draw(false)}
      {draw(true)}
    </svg>
  );
}

export function BodyMap({ highlight, caption, compact }: { highlight: MapHighlight; caption?: string; compact?: boolean }) {
  const uid = useId().replace(/:/g, '');
  const names = (ids: MuscleId[]) => ids.map((m) => MUSCLE_BY_ID[m].shortName).join(', ');
  return (
    <div>
      <div className="bodymap" style={compact ? { maxWidth: 300 } : undefined}>
        <figure>
          <View regions={FRONT} view="front" h={highlight} patternId={`hp-${uid}-f`} dotId={`dp-${uid}-f`} />
          <figcaption>Front</figcaption>
        </figure>
        <figure>
          <View regions={BACK} view="back" h={highlight} patternId={`hp-${uid}-b`} dotId={`dp-${uid}-b`} />
          <figcaption>Back</figcaption>
        </figure>
      </div>
      <div className="legend" style={{ marginTop: 8 }}>
        <span>
          <i className="swatch" style={{ background: 'var(--map-primary)' }} aria-hidden="true" /> Primary
        </span>
        <span>
          <svg width="16" height="12" aria-hidden="true">
            <defs>
              <pattern id={`lg-${uid}`} width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <rect width="3" height="3" fill="var(--map-base)" />
                <line x1="0" y1="0" x2="0" y2="3" stroke="var(--map-secondary)" strokeWidth="2" />
              </pattern>
            </defs>
            <rect x="0.5" y="0.5" width="15" height="11" rx="3" fill={`url(#lg-${uid})`} stroke="var(--map-edge)" />
          </svg>
          Secondary
        </span>
        {highlight.exposure && highlight.exposure.length > 0 && (
          <span>
            <svg width="16" height="12" aria-hidden="true">
              <rect x="1" y="1" width="14" height="10" rx="3" fill="none" stroke="var(--map-exposure)" strokeDasharray="2 1.5" strokeWidth="1.5" />
            </svg>
            Activity exposure
          </span>
        )}
      </div>
      <p className="small muted" style={{ marginTop: 6 }}>
        {highlight.primary.length > 0 && (
          <>
            <b>Primary:</b> {names(highlight.primary)}.{' '}
          </>
        )}
        {highlight.secondary.length > 0 && (
          <>
            <b>Secondary:</b> {names(highlight.secondary)}.
          </>
        )}
        {caption && <> {caption}</>}
      </p>
    </div>
  );
}
