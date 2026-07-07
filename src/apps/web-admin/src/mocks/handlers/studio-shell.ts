/**
 * 模块：src/apps/web-admin/src/mocks/handlers/studio-shell.ts
 * 作用：studio-shell MSW handlers — GET /v1/studio/flows
 * 怎么用：handlers/index.ts 聚合；Vitest server 启动
 * 解决：无后端时 layout/pages 联调与 RTL 冒烟
 * 上游：api/functions/studio-shell/flows.fn.ts
 * 下游：mocks/server.ts · test/setup.ts
 * 关联：pages/studio-shell/contracts/README.md · W-04
 */
import { http, HttpResponse } from "msw";

const FLOWS_FIXTURE = {
  version: "1.0.0",
  title: "Integration Studio 六步向导",
  steps: [
    { id: "connect", order: 1, title: "连通", summary: "凭证 ref、ping" },
    { id: "discover", order: 2, title: "发现", summary: "Blueprint 校验" },
    { id: "map", order: 3, title: "映射", summary: "字段映射" },
    { id: "prove", order: 4, title: "验证", summary: "Shadow 证明" },
    { id: "freeze", order: 5, title: "冻结", summary: "Graph freeze" },
    { id: "export", order: 6, title: "导出", summary: "Package export" },
  ],
};

export const studioShellHandlers = [
  http.get("/v1/studio/flows", () => HttpResponse.json(FLOWS_FIXTURE)),
];
