/**
 * 模块：src/apps/web-admin/src/layout/types.ts
 * 作用：LayoutModuleEntry 类型
 * 怎么用：layout/modules 各子目录 registry.ts 引用
 * 解决：layout 登记结构 SSOT
 * 上游：ARCHITECTURE 注册制
 * 下游：layout/modules 子表 · layout/registry.ts
 * 关联：layout/contracts/README.md
 */
import type { ComponentType } from "react";

export type LayoutModuleEntry = {
  id: string;
  pathPrefix: string;
  summary: string;
  component: ComponentType;
};