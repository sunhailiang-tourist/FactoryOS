/**
 * 模块：src/apps/web-admin/src/layout/modules/studio/registry.ts
 * 作用：studio domain layout 子表（pathPrefix /studio）
 * 怎么用：登记 StudioShellLayout；router layoutId=studio
 * 解决：Studio 六步共享导航壳
 * 上游：layout/modules/studio/StudioShellLayout.tsx
 * 下游：router/modules studio 系列路由子表
 * 关联：layout/contracts/README.md · pages/studio-shell/contracts/README.md
 */
import { StudioShellLayout } from "@/layout/modules/studio/StudioShellLayout";
import type { LayoutModuleEntry } from "@/layout/types";

export const LAYOUT_MODULE_ENTRIES: LayoutModuleEntry[] = [
  {
    id: "studio",
    pathPrefix: "/studio",
    summary: "Integration Studio 六步向导壳",
    component: StudioShellLayout,
  },
];