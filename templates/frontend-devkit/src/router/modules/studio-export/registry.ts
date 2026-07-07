/**
 * 模块：src/apps/web-admin/src/router/modules/studio-export/registry.ts
 * 作用：Export 导出 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-export 追踪链一一对应
 * 上游：pages/studio-export lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-export/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.export",
    moduleId: "studio-export",
    layoutId: "studio",
    path: "export",
    permissions: ["studio.export.view"],
    summary: "Export · Package 导出",
    lazy: async () => {
      const m = await import("@/pages/studio-export/StudioExportPage.lazy");
      return { Component: m.default };
    },
  },
];