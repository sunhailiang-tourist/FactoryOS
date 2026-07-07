/**
 * 模块：src/apps/web-admin/src/api/registry.ts
 * 作用：API 板块 glob 聚合 API_REGISTRY
 * 怎么用：新增端点建 api/functions/{module}/；勿手改 glob
 * 解决：实体函数登记与 harness fn 对账
 * 上游：api/functions 各子目录 registry.ts
 * 下游：pages 与 store 模块
 * 关联：api/contracts/README.md · server/api/router/v1
 */
import type { ApiRegistryEntry } from "@/api/registry.types";

type ApiRegistryModule = {
  API_MODULE_ENTRIES: ApiRegistryEntry[];
};

const apiModules = import.meta.glob<ApiRegistryModule>("./functions/*/registry.ts", {
  eager: true,
});

export const API_REGISTRY: readonly ApiRegistryEntry[] = Object.values(apiModules)
  .flatMap((mod) => mod.API_MODULE_ENTRIES ?? [])
  .sort((a, b) => a.id.localeCompare(b.id));

export type { ApiRegistryEntry } from "@/api/registry.types";