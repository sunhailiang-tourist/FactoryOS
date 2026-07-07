/**
 * 模块：src/apps/web-admin/src/router/modules/studio-prove/registry.ts
 * 作用：Prove 验证 路由子表（ROUTE_MODULE_ENTRIES）
 * 怎么用：登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts
 * 解决：单模块路由与 pages/studio-prove 追踪链一一对应
 * 上游：pages/studio-prove lazy 页
 * 下游：router/registry.ts · router/compose.tsx
 * 关联：pages/studio-prove/contracts/README.md · router/contracts/README.md
 */
import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "studio.prove",
    moduleId: "studio-prove",
    layoutId: "studio",
    path: "prove",
    permissions: ["studio.prove.view"],
    summary: "Prove · Shadow 验证",
    lazy: async () => {
      const m = await import("@/pages/studio-prove/StudioProvePage.lazy");
      return { Component: m.default };
    },
  },
];