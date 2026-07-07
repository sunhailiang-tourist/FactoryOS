/**
 * 模块：src/apps/web-admin/src/router/loaders.ts
 * 作用：RR loader 工厂 — QueryClient ensureQueryData
 * 怎么用：browser-router studio layout loader
 * 解决：进壳前预取 flows，减少侧栏 spinner
 * 上游：QueryClient · getStudioFlows
 * 下游：StudioShellLayout
 * 关联：ENGINEERING.md §10 S4
 */
import type { QueryClient } from "@tanstack/react-query";
import { getStudioFlows } from "@/api/functions/studio-shell";
import { studioKeys } from "@/api/query/keys";

export function createStudioFlowsLoader(queryClient: QueryClient) {
  return async () => {
    await queryClient.ensureQueryData({
      queryKey: studioKeys.flows(),
      queryFn: getStudioFlows,
    });
    return null;
  };
}
