/**
 * 模块：src/apps/web-admin/src/api/registry.types.ts
 * 作用：ApiRegistryEntry 类型
 * 怎么用：api/functions 各子目录 registry.ts 引用
 * 解决：API 登记 id/fn/path 形状 SSOT
 * 上游：ARCHITECTURE 注册制
 * 下游：api/functions 子表 · api/registry.ts
 * 关联：api/contracts/README.md
 */
export type ApiRegistryEntry = {
  id: string;
  module: string;
  routeName: string;
  method: string;
  path: string;
  fn: string;
  summary: string;
  problem: string;
  usage: string;
  acIds: string[];
};