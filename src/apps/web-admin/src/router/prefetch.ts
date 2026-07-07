/**
 * 模块：src/apps/web-admin/src/router/prefetch.ts
 * 作用：导航意图预取 — Query + route chunk
 * 怎么用：StudioNavLink onMouseEnter / onFocus
 * 解决：切页 P95 感知延迟
 * 上游：ROUTE_REGISTRY · QueryClient
 * 下游：侧栏 Link
 * 关联：ENGINEERING.md §10 S4
 */
import type { QueryClient } from "@tanstack/react-query";
import { getStudioFlows } from "@/api/functions/studio-shell";
import { studioKeys } from "@/api/query/keys";
import { ROUTE_REGISTRY } from "@/router/registry";

export function prefetchStudioFlows(queryClient: QueryClient): void {
  void queryClient.prefetchQuery({
    queryKey: studioKeys.flows(),
    queryFn: getStudioFlows,
  });
}

export function prefetchRouteChunk(moduleId: string): void {
  const entry = ROUTE_REGISTRY.find((r) => r.moduleId === moduleId);
  if (entry) {
    void entry.lazy();
  }
}

export function prefetchStudioNavigation(
  queryClient: QueryClient,
  moduleId?: string,
): void {
  prefetchStudioFlows(queryClient);
  if (moduleId) {
    prefetchRouteChunk(moduleId);
  }
}
