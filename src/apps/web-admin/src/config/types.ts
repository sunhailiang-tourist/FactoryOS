/**
 * 模块：src/apps/web-admin/src/config/types.ts
 * 作用：ConfigModuleEntry 类型
 * 怎么用：config/modules 各子目录 registry.ts 引用
 * 解决：配置登记结构 SSOT
 * 上游：ARCHITECTURE 注册制
 * 下游：config/modules 子表 · config/registry.ts
 * 关联：config/contracts/README.md
 */
export type ConfigModuleEntry = {
  id: string;
  enabled: boolean;
  summary: string;
};