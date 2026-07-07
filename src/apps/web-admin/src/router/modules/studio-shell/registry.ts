/**
 * 模块：src/apps/web-admin/src/router/modules/studio-shell/registry.ts
 * 作用：Studio 概览 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-shell 追踪链一一对应
 * 上游：pages/studio-shell lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-shell/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.home",
    moduleId: "studio-shell",
    layoutId: "studio",
    index: true,
    permissions: ["studio.shell.view"],
    summary: "Studio 概览 · flows 导航入口",
    lazy: async () => {
      const m = await import("@/pages/studio-shell/StudioHomePage.lazy");
      return { Component: m.default };
    },
  },
];