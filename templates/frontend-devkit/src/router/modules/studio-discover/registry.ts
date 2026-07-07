/**
 * 模块：src/apps/web-admin/src/router/modules/studio-discover/registry.ts
 * 作用：Discover 发现 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-discover 追踪链一一对应
 * 上游：pages/studio-discover lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-discover/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.discover",
    moduleId: "studio-discover",
    layoutId: "studio",
    path: "discover",
    permissions: ["studio.discover.view"],
    summary: "Discover · OpenAPI/Blueprint 发现",
    lazy: async () => {
      const m = await import("@/pages/studio-discover/StudioDiscoverPage.lazy");
      return { Component: m.default };
    },
  },
];