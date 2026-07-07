/**
 * 模块：src/apps/web-admin/e2e/shell.spec.ts
 * 作用：Playwright 壳层冒烟 — 路由 · layout · lazy（不测 API 正确性）
 * 怎么用：pnpm e2e（page.route mock · 不依赖 MSW worker）
 * 解决：端到端验证 router/layout；避免 SW 与 Playwright 竞态
 * 上游：router/compose · layout/studio
 * 下游：W-06
 * 关联：playwright.config.ts · ENGINEERING.md §6
 */
import { expect, test } from "@playwright/test";

const FLOWS_FIXTURE = {
  version: "1.0.0",
  title: "Integration Studio 六步向导",
  steps: [
    { id: "connect", order: 1, title: "连通", summary: "凭证 ref、ping" },
    { id: "discover", order: 2, title: "发现", summary: "Blueprint 校验" },
    { id: "map", order: 3, title: "映射", summary: "字段映射" },
    { id: "prove", order: 4, title: "验证", summary: "Shadow 证明" },
    { id: "freeze", order: 5, title: "冻结", summary: "Graph freeze" },
    { id: "export", order: 6, title: "导出", summary: "Package export" },
  ],
};

test.describe("app shell", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/v1/studio/flows", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(FLOWS_FIXTURE),
      });
    });
  });

  test("redirects / to /studio", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL(/\/studio\/?$/, { timeout: 10_000 });
  });

  test("studio layout nav and lazy child render", async ({ page }) => {
    await page.goto("/studio/connect");
    await expect(page.getByRole("navigation", { name: "Studio 六步" })).toBeVisible();
    await expect(page.getByText("Integration Studio 六步向导")).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole("main")).toContainText("Connect · 连通", { timeout: 15_000 });
    await expect(page.getByText("1. 连通")).toBeVisible();
  });

  test("studio home overview shows step count", async ({ page }) => {
    await page.goto("/studio");
    await expect(page.getByText(/已注册 6 个向导步骤/)).toBeVisible({ timeout: 10_000 });
  });

  const stepCases = [
    { path: "/studio/connect", heading: "Connect · 连通" },
    { path: "/studio/discover", heading: "Discover · 发现" },
    { path: "/studio/map", heading: "Map · 映射" },
    { path: "/studio/prove", heading: "Prove · 验证" },
    { path: "/studio/freeze", heading: "Freeze · 冻结" },
    { path: "/studio/export", heading: "Export · 导出" },
  ] as const;

  for (const { path, heading } of stepCases) {
    test(`lazy route ${path} renders shell page`, async ({ page }) => {
      await page.goto(path);
      await expect(page.getByRole("heading", { level: 5, name: heading })).toBeVisible({
        timeout: 15_000,
      });
    });
  }

  test("sidebar navigates connect to discover", async ({ page }) => {
    await page.goto("/studio/connect");
    await page.getByRole("link", { name: /2\.\s*发现/ }).click();
    await expect(page).toHaveURL(/\/studio\/discover/);
    await expect(page.getByRole("heading", { level: 5, name: "Discover · 发现" })).toBeVisible();
  });
});
