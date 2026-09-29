import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import { readFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8')) as { version: string };

// Content Security Policy for production builds. Static hosts like GitHub Pages cannot set
// headers, so the policy is delivered as a meta tag. Dev builds skip it because Vite injects
// inline scripts for hot reload.
const CSP = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self'",
  "img-src 'self' data: blob:",
  "font-src 'self'",
  "connect-src 'self' https://world.openfoodfacts.org",
  'frame-src https://www.youtube-nocookie.com',
  "media-src 'self' blob:",
  "worker-src 'self'",
  "manifest-src 'self'",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'none'",
].join('; ');

function csp(): Plugin {
  return {
    name: 'peakform-csp',
    apply: 'build',
    transformIndexHtml(html) {
      return html.replace('<!--CSP-->', `<meta http-equiv="Content-Security-Policy" content="${CSP}" />`);
    },
  };
}

export default defineConfig({
  base: './',
  define: {
    __APP_VERSION__: JSON.stringify(pkg.version),
    __BUILD_DATE__: JSON.stringify(new Date().toISOString().slice(0, 10)),
  },
  build: {
    target: 'es2020',
    sourcemap: false,
    assetsInlineLimit: 0,
  },
  plugins: [
    react(),
    csp(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: null,
      // The private deployment needs its session cookie on the manifest request too.
      useCredentials: true,
      includeAssets: ['icons/*.png', 'icons/*.svg', 'favicon.svg'],
      manifest: {
        id: './',
        name: 'PeakForm',
        short_name: 'PeakForm',
        description: 'Private training, food, and recovery log that works offline.',
        lang: 'en',
        dir: 'ltr',
        start_url: './#/today',
        scope: './',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#f4f3ef',
        theme_color: '#f4f3ef',
        categories: ['health', 'fitness', 'lifestyle'],
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
          { src: 'icons/icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
        shortcuts: [
          { name: 'Start Workout', short_name: 'Workout', url: './#/train/start', icons: [{ src: 'icons/icon-192.png', sizes: '192x192' }] },
          { name: 'Log Meal', short_name: 'Meal', url: './#/eat', icons: [{ src: 'icons/icon-192.png', sizes: '192x192' }] },
          { name: 'Morning Check In', short_name: 'Check in', url: './#/checkin', icons: [{ src: 'icons/icon-192.png', sizes: '192x192' }] },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,webmanifest,ico}'],
        navigateFallback: 'index.html',
        cleanupOutdatedCaches: true,
        clientsClaim: false,
        skipWaiting: false,
        // No runtime caching: nothing from other origins is stored, and no personal data is cached.
        runtimeCaching: [],
      },
      devOptions: { enabled: false },
    }),
  ],
});
