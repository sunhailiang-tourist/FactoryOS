/**
 * 模块：src/apps/web-admin/src/pages/studio-steps.smoke.test.tsx
 * 作用：六步 Studio lazy 页 RTL 冒烟（参数化）
 * 怎么用：vitest run studio-steps.smoke.test.tsx
 * 解决：每 module-id 至少 1 条渲染断言，提升测试密度
 * 上游：pages studio 各步 lazy.tsx
 * 下游：pnpm check
 * 关联：WEB-PROFILE 基座 · 联调前壳层
 */
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

const STEP_PAGES = [
  { moduleId: "studio-connect", importPath: "./studio-connect/StudioConnectPage.lazy", heading: "Connect · 连通" },
  { moduleId: "studio-discover", importPath: "./studio-discover/StudioDiscoverPage.lazy", heading: "Discover · 发现" },
  { moduleId: "studio-map", importPath: "./studio-map/StudioMapPage.lazy", heading: "Map · 映射" },
  { moduleId: "studio-prove", importPath: "./studio-prove/StudioProvePage.lazy", heading: "Prove · 验证" },
  { moduleId: "studio-freeze", importPath: "./studio-freeze/StudioFreezePage.lazy", heading: "Freeze · 冻结" },
  { moduleId: "studio-export", importPath: "./studio-export/StudioExportPage.lazy", heading: "Export · 导出" },
] as const;

describe("studio step lazy pages", () => {
  it.each(STEP_PAGES)("$moduleId renders shell heading", async ({ importPath, heading }) => {
    const mod = await import(importPath);
    const Page = mod.default;
    render(<Page />);
    expect(screen.getByRole("heading", { level: 5, name: heading })).toBeInTheDocument();
  });
});
