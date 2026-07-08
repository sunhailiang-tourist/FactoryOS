/**
 * 模块：src/apps/web-admin/src/layout/registry.ts
 * 作用：layout 板块 glob 聚合 LAYOUT_REGISTRY
 * 怎么用：新 domain 建 layout/modules/{domain}/registry.ts + 组件
 * 解决：pathPrefix 与 shell 布局复用
 * 上游：layout/modules 子目录
 * 下游：router/compose.tsx
 * 关联：layout/contracts/README.md
 */
import type { LayoutModuleEntry } from "@/layout/types";

type LayoutRegistryModule = {
  LAYOUT_MODULE_ENTRIES: LayoutModuleEntry[];
};

const layoutModules = import.meta.glob<LayoutRegistryModule>("./modules/*/registry.ts", {
  eager: true,
});

export const LAYOUT_REGISTRY: readonly LayoutModuleEntry[] = Object.values(layoutModules)
  .flatMap((mod) => mod.LAYOUT_MODULE_ENTRIES ?? [])
  .sort((a, b) => a.id.localeCompare(b.id));

/**
 * 功能：getLayoutById 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function getLayoutById(id: string): LayoutModuleEntry | undefined {
  return LAYOUT_REGISTRY.find((entry) => entry.id === id);
}