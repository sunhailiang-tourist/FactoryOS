/**
 * 模块：src/apps/web-admin/src/router/registry.ts
 * 作用：路由板块 glob 聚合 ROUTE_REGISTRY
 * 怎么用：新增路由只建 router/modules/{id}/registry.ts；勿手改本文件 glob
 * 解决：多模块路由登记可扩展且 harness 可对账
 * 上游：router/modules 各子目录 registry.ts
 * 下游：router/compose.tsx
 * 关联：router/contracts/README.md · ENGINEERING.md §2
 */
import type { RouteModuleEntry } from "@/router/types";
import { canAccessRoute } from "@/rbac/core/evaluate";

type RouteRegistryModule = {
  ROUTE_MODULE_ENTRIES: RouteModuleEntry[];
};

const routeModules = import.meta.glob<RouteRegistryModule>("./modules/*/registry.ts", {
  eager: true,
});

function collectRouteEntries(): RouteModuleEntry[] {
  return Object.values(routeModules).flatMap((mod) => mod.ROUTE_MODULE_ENTRIES ?? []);
}

/** 按 moduleId 稳定排序，便于 diff 与 harness 对账。 */
export const ROUTE_REGISTRY: readonly RouteModuleEntry[] = collectRouteEntries().sort((a, b) =>
  a.moduleId.localeCompare(b.moduleId),
);

export function getRoutesByLayout(layoutId: string, role?: string): RouteModuleEntry[] {
  const routes = ROUTE_REGISTRY.filter((entry) => entry.layoutId === layoutId);
  if (!role) return routes;
  return routes.filter((entry) => canAccessRoute(role, entry.permissions, entry.permissionsMode));
}