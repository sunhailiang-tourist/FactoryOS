/**
 * 模块：src/apps/web-admin/src/router/modules/studio-freeze/registry.ts
 * 作用：Freeze 冻结 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-freeze 追踪链一一对应
 * 上游：pages/studio-freeze lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-freeze/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.freeze",
    moduleId: "studio-freeze",
    layoutId: "studio",
    path: "freeze",
    permissions: ["studio.freeze.view"],
    summary: "Freeze · Graph 冻结",
    lazy: async () => {
      const m = await import("@/pages/studio-freeze/StudioFreezePage.lazy");
      return { Component: m.default };
    },
  },
];