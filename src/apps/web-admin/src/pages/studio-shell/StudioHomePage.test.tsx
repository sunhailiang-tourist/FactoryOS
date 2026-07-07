/**
 * 模块：src/apps/web-admin/src/pages/studio-shell/StudioHomePage.test.tsx
 * 作用：Studio 概览 RTL 冒烟 — MSW + useStudioFlows
 * 怎么用：vitest run StudioHomePage.test.tsx
 * 解决：W-04 基座测试链验证
 * 上游：mocks/handlers/studio-shell · test/render.tsx
 * 下游：pnpm check
 * 关联：验收用例-WEB-S1 · W-04
 */
import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { renderWithProviders } from "@/test/render";
import StudioHomePage from "./StudioHomePage.lazy";

describe("StudioHomePage", () => {
  it("W-04 · 展示 MSW flows 步骤数", async () => {
    renderWithProviders(<StudioHomePage />);
    await waitFor(() => {
      expect(screen.getByText(/已注册 6 个向导步骤/)).toBeInTheDocument();
    });
  });
});
