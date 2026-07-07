/**
 * 模块：src/apps/web-admin/src/router/types.ts
 * 作用：RouteModuleEntry 类型 — 子目录 registry 条目形状
 * 怎么用：router/modules 各子目录 registry.ts 引用；扩展字段先改类型再改 harness
 * 解决：路由登记结构 SSOT，避免散落 inline 类型
 * 上游：ARCHITECTURE 注册制
 * 下游：router/modules 子表 · router/registry.ts
 * 关联：router/contracts/README.md
 */
import type { ComponentType } from "react";

export type RouteModuleEntry = {
  name: string;
  moduleId: string;
  layoutId: string;
  summary: string;
  path?: string;
  index?: boolean;
  /** 路由级 view 权限（rbac/modules 登记须一致）。 */
  permissions?: readonly string[];
  permissionsMode?: "all" | "any";
  lazy: () => Promise<{ Component: ComponentType }>;
};