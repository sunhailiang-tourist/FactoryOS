/**
 * 模块：src/apps/web-admin/src/config/modules/studio/registry.ts
 * 作用：studio domain 功能开关子表
 * 怎么用：enabled 控制 Studio 向导是否注册；glob 聚合
 * 解决：Studio 模块可整体灰度
 * 上游：config/registry.ts
 * 下游：router/bootstrap 消费方
 * 关联：config/contracts/README.md
 */
import type { ConfigModuleEntry } from "@/config/types";

export const CONFIG_MODULE_ENTRIES: ConfigModuleEntry[] = [
  {
    id: "studio.wizard",
    enabled: true,
    summary: "Integration Studio 六步向导",
  },
];