/**
 * 模块：src/apps/web-admin/src/api/functions/studio-connect/registry.ts
 * 作用：studio-connect API 子表（API_MODULE_ENTRIES）
 * 怎么用：登记 id/method/path/fn；fn 须在 .fn.ts 导出
 * 解决：端点与实现文件 harness 可追踪
 * 上游：pages/studio-connect
 * 下游：api/functions/studio-connect fn 文件 · server/api
 * 关联：pages/studio-connect/contracts/README.md · api/contracts/README.md
 */
import type { ApiRegistryEntry } from "@/api/registry.types";

export const API_MODULE_ENTRIES: ApiRegistryEntry[] = [
  {
    id: "studio.connect.test",
    module: "studio-connect",
    routeName: "studio.connect",
    method: "POST",
    path: "/v1/integration/connect/test",
    fn: "postConnectTest",
    summary: "凭证连通 ping",
    problem: "顾问录入 secrets_ref 后验证 ERP 可达",
    usage: "Studio Connect 页 · AC STU-01",
    acIds: ["STU-01"],
  },
];