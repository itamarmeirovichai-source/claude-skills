import { defineConfig, devices } from '@playwright/test';

// WebKit cannot be installed in this build environment, so tests run on Chromium with
// iPhone sized viewports, touch, and an iOS user agent. The app avoids Chromium only APIs.
const iphone = {
  ...devices['iPhone 13'],
  browserName: 'chromium' as const,
  defaultBrowserType: 'chromium' as const,
};

export default defineConfig({
  testDir: 'e2e',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 2,
  reporter: [['list'], ['json', { outputFile: 'test-results/e2e.json' }]],
  use: {
    baseURL: 'http://localhost:4173/',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    acceptDownloads: true,
    serviceWorkers: 'allow',
    timezoneId: 'Asia/Jerusalem',
    locale: 'en-US',
  },
  projects: [
    { name: 'iphone-390', use: { ...iphone, viewport: { width: 390, height: 844 } } },
    { name: 'iphone-375', use: { ...iphone, viewport: { width: 375, height: 667 } }, grep: /@layout/ },
    { name: 'iphone-393', use: { ...iphone, viewport: { width: 393, height: 852 } }, grep: /@layout/ },
    { name: 'iphone-430', use: { ...iphone, viewport: { width: 430, height: 932 } }, grep: /@layout/ },
  ],
  webServer: {
    command: 'npm run build && npx vite preview --port 4173 --strictPort',
    url: 'http://localhost:4173/',
    reuseExistingServer: true,
    timeout: 180_000,
  },
});
