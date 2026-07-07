/**
 * 模块：src/apps/web-admin/playwright.config.ts
 * 作用：Playwright 配置 — e2e 禁用 MSW（page.route mock）
 * 怎么用：pnpm e2e
 * 解决：E2E 无 live API · 避免 MSW worker 竞态
 * 上游：e2e/shell.spec.ts
 * 下游：pnpm check · W-06
 * 关联：ENGINEERING.md §10 S4
 */
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "on-first-retry",
    channel: process.env.PW_CHANNEL || "chrome",
  },
  webServer: {
    command: "pnpm dev --host 127.0.0.1 --port 5173",
    url: "http://127.0.0.1:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    env: {
      ...process.env,
      VITE_MSW: "0",
    },
  },
});
