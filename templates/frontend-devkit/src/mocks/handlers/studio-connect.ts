/**
 * 模块：src/apps/web-admin/src/mocks/handlers/studio-connect.ts
 * 作用：studio-connect MSW — POST connect/test
 * 怎么用：handlers/index.ts 聚合
 * 解决：零后端 Connect 步可演示
 * 上游：api/functions/studio-connect/connect.fn.ts
 * 下游：mocks/server.ts
 * 关联：pages/studio-connect/contracts/README.md
 */
import { http, HttpResponse } from "msw";

export const studioConnectHandlers = [
  http.post("/v1/integration/connect/test", async () => {
    return HttpResponse.json({ ok: true, message: "MSW: connect ping ok" });
  }),
];
