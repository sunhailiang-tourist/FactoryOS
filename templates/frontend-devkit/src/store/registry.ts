/**
 * 模块：src/apps/web-admin/src/store/registry.ts
 * 作用：store 板块 glob 聚合 STORE_REGISTRY
 * 怎么用：新增 store 建 store/modules/{id}/；common 走 store/common/
 * 解决：模块级 zustand 登记与 pages 追踪链对齐
 * 上游：store/modules 子目录 · store/common
 * 下游：pages 与 store hooks
 * 关联：store/contracts/README.md
 */
import { STORE_COMMON_ENTRIES } from "@/store/common/registry";
import type { StoreModuleEntry } from "@/store/types";

type StoreRegistryModule = {
  STORE_MODULE_ENTRIES: StoreModuleEntry[];
};

const storeModules = import.meta.glob<StoreRegistryModule>("./modules/*/registry.ts", {
  eager: true,
});

function collectStoreEntries(): StoreModuleEntry[] {
  return Object.values(storeModules).flatMap((mod) => mod.STORE_MODULE_ENTRIES ?? []);
}

export const STORE_REGISTRY: readonly StoreModuleEntry[] = [
  ...STORE_COMMON_ENTRIES,
  ...collectStoreEntries().sort((a, b) => a.moduleId.localeCompare(b.moduleId)),
] as const;

export function getStoreByModuleId(moduleId: string): StoreModuleEntry | undefined {
  return STORE_REGISTRY.find((entry) => entry.moduleId === moduleId);
}