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

/**
 * 功能：prefetchStudioFlows 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function prefetchStudioFlows(queryClient: QueryClient): void {
  void queryClient.prefetchQuery({
    queryKey: studioKeys.flows(),
    queryFn: getStudioFlows,
  });
}

/**
 * 功能：prefetchRouteChunk 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function prefetchRouteChunk(moduleId: string): void {
  // 业务：prefetchRouteChunk 主体编排（见文件头上下游）
  const entry = ROUTE_/**
 * 功能：prefetchStudioNavigation 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
REGISTRY.find((r) => r.moduleId === moduleId);
  if (entry) {
    void entry.lazy();
  }
}

/**
 * 功能：prefetchStudioNavigation 导出函数。
 * 业务含义：见同文件模块文件头。
 * 上游：见文件头上游。
 * 下游：见文件头下游。
 */
export function prefetchStudioNavigation(
  queryClient: QueryClient,
  moduleId?: string,
): void {
  prefetchStudioFlows(queryClient);
  if (moduleId) {
    prefetchRouteChunk(moduleId);
  }
}
