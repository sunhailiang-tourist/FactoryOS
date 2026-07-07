/**
 * 模块：src/apps/web-admin/src/layout/modules/studio/StudioShellLayout.test.tsx
 * 作用：Studio 壳布局 RTL — 侧栏 · MSW flows
 * 怎么用：vitest run StudioShellLayout.test.tsx
 * 解决：layout + query hook 集成可测
 * 上游：useStudioFlows · mocks
 * 下游：e2e shell
 * 关联：layout/modules/studio/contracts
 */
import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Routes, Route } from "react-router-dom";
import { renderWithProviders } from "@/test/render";
import { StudioShellLayout } from "./StudioShellLayout";

function ShellRoute() {
  return (
    <Routes>
      <Route path="/studio/*" element={<StudioShellLayout />}>
        <Route index element={<div>child</div>} />
      </Route>
    </Routes>
  );
}

describe("StudioShellLayout", () => {
  it("renders six-step navigation from MSW flows", async () => {
    renderWithProviders(<ShellRoute />, { route: "/studio" });
    await waitFor(() => {
      expect(screen.getByRole("navigation", { name: "Studio 六步" })).toBeInTheDocument();
      expect(screen.getByText("1. 连通")).toBeInTheDocument();
    });
    expect(screen.getByText("6. 导出")).toBeInTheDocument();
  });
});
