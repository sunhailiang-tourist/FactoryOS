/**
 * 模块：src/apps/web-admin/src/router/modules/studio-connect/registry.ts
 * 作用：Connect 连通 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-connect 追踪链一一对应
 * 上游：pages/studio-connect lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-connect/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.connect",
    moduleId: "studio-connect",
    layoutId: "studio",
    path: "connect",
    permissions: ["studio.connect.view"],
    summary: "Connect · 凭证连通",
    lazy: async () => {
      const m = await import("@/pages/studio-connect/StudioConnectPage.lazy");
      return { Component: m.default };
    },
  },
];