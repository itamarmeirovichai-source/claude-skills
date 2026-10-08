import { defineConfig, devices } from '@playwright/test';
import { existsSync } from 'node:fs';

// Use a preinstalled Chromium when present (no `playwright install` needed); override with PW_CHROMIUM.
const candidates = [process.env['PW_CHROMIUM'], '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium'];
const executablePath = candidates.find((p): p is string => !!p && existsSync(p));
const launchOptions = {
  ...(executablePath ? { executablePath } : {}),
  args: ['--autoplay-policy=no-user-gesture-required', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
};

export default defineConfig({
  testDir: './e2e',
  timeout: 45_000,
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: { baseURL: 'http://localhost:4321', trace: 'off' },
  webServer: { command: 'npx astro preview --port 4321', url: 'http://localhost:4321', reuseExistingServer: true, timeout: 60_000 },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 }, launchOptions } },
    { name: 'mobile', use: { ...devices['Pixel 7'], launchOptions } },
  ],
});
