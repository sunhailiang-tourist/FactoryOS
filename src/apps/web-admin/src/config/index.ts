/**
 * 模块：src/apps/web-admin/src/config/index.ts
 * 作用：config 板块 barrel 导出
 * 怎么用：import from '@/config' 取 registry/types/env
 * 解决：统一 config 公共出口
 * 上游：config/registry.ts · config/env.ts
 * 下游：应用各层
 * 关联：config/contracts/README.md
 */
export { env } from "./env";
export { CONFIG_REGISTRY } from "./registry";
export type { ConfigModuleEntry } from "./types";