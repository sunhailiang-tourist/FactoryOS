/**
 * 模块：src/apps/web-admin/src/api/query/hooks/useStudioFlows.test.tsx
 * 作用：useStudioFlows + MSW 集成测试
 * 怎么用：vitest run useStudioFlows.test.tsx
 * 解决：Server State hook 与 handlers 对齐
 * 上游：mocks/handlers/studio-shell · test/setup.ts
 * 下游：layout/pages
 * 关联：W-02 · W-04
 */
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { describe, expect, it } from "vitest";
import { createQueryClient } from "@/api/query/client";
import { useStudioFlows } from "./useStudioFlows";

function wrapper({ children }: { children: ReactNode }) {
  const client = createQueryClient();
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

describe("useStudioFlows", () => {
  it("loads six wizard steps from MSW", async () => {
    const { result } = renderHook(() => useStudioFlows(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.steps).toHaveLength(6);
    expect(result.current.data?.title).toMatch(/六步向导/);
  });
});
