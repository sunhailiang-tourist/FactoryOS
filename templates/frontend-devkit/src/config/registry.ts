/**
 * 模块：src/apps/web-admin/src/config/registry.ts
 * 作用：config 板块 glob 聚合 + isConfigEnabled
 * 怎么用：功能开关登记在 config/modules/{domain}/registry.ts
 * 解决：按 domain 启停模块而不改路由代码
 * 上游：config/modules 子目录
 * 下游：bootstrap/路由/feature flag 消费方
 * 关联：config/contracts/README.md
 */
import type { ConfigModuleEntry } from "@/config/types";

type ConfigRegistryModule = {
  CONFIG_MODULE_ENTRIES: ConfigModuleEntry[];
};

const configModules = import.meta.glob<ConfigRegistryModule>("./modules/*/registry.ts", {
  eager: true,
});

export const CONFIG_REGISTRY: readonly ConfigModuleEntry[] = Object.values(configModules)
  .flatMap((mod) => mod.CONFIG_MODULE_ENTRIES ?? [])
  .sort((a, b) => a.id.localeCompare(b.id));

/** 运行时 feature flag：id 未登记视为 disabled。 */
export function isConfigEnabled(configId: string): boolean {
  const entry = CONFIG_REGISTRY.find((item) => item.id === configId);
  return entry?.enabled ?? false;
}