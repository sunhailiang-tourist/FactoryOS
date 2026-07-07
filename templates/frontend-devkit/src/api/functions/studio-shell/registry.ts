/**
 * 模块：src/apps/web-admin/src/api/functions/studio-shell/registry.ts
 * 作用：studio-shell API 子表（API_MODULE_ENTRIES）
 * 怎么用：登记 id/method/path/fn；fn 须在 .fn.ts 导出
 * 解决：端点与实现文件 harness 可追踪
 * 上游：pages/studio-shell
 * 下游：api/functions/studio-shell fn 文件 · server/api
 * 关联：pages/studio-shell/contracts/README.md · api/contracts/README.md
 */
import type { ApiRegistryEntry } from "@/api/registry.types";

export const API_MODULE_ENTRIES: ApiRegistryEntry[] = [
  {
    id: "studio.flows.list",
    module: "studio-shell",
    routeName: "studio.home",
    method: "GET",
    path: "/v1/studio/flows",
    fn: "getStudioFlows",
    summary: "Studio 六步向导元数据",
    problem: "侧栏导航须从服务端拉取 connect→export 步骤",
    usage: "StudioShellLayout · studio-shell store · AC STU-09",
    acIds: ["STU-09"],
  },
];