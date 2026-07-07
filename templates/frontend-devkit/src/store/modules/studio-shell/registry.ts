/**
 * 模块：src/apps/web-admin/src/store/modules/studio-shell/registry.ts
 * 作用：studio-shell store 子表登记
 * 怎么用：导出 STORE_MODULE_ENTRIES；glob 聚合
 * 解决：模块 UI 状态与 pages/studio-shell 契约一致
 * 上游：pages/studio-shell
 * 下游：store/modules/studio-shell store 实现文件
 * 关联：pages/studio-shell/contracts/README.md
 */
import type { StoreModuleEntry } from "@/store/types";

export const STORE_MODULE_ENTRIES: StoreModuleEntry[] = [
  {
    key: "studio/shell",
    moduleId: "studio-shell",
    summary: "Studio 壳纯 UI 态（侧栏折叠）；flows 走 useStudioFlows",
  },
];