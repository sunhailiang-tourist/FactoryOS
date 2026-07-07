/**
 * 模块：src/apps/web-admin/src/store/types.ts
 * 作用：StoreModuleEntry 类型
 * 怎么用：store/modules 各子目录 registry.ts 引用
 * 解决：store 子表条目形状 SSOT
 * 上游：ARCHITECTURE 注册制
 * 下游：store/modules 子表 · store/registry.ts
 * 关联：store/contracts/README.md
 */
export type StoreModuleEntry = {
  key: string;
  moduleId: string;
  summary: string;
};