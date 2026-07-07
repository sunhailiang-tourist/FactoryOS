/**
 * 模块：src/apps/web-admin/src/router/modules/studio-map/registry.ts
 * 作用：Map 映射 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-map 追踪链一一对应
 * 上游：pages/studio-map lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-map/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.map",
    moduleId: "studio-map",
    layoutId: "studio",
    path: "map",
    permissions: ["studio.map.view"],
    summary: "Map · 字段映射",
    lazy: async () => {
      const m = await import("@/pages/studio-map/StudioMapPage.lazy");
      return { Component: m.default };
    },
  },
];