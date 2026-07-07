/**
 * 模块：src/apps/web-admin/src/mocks/handlers/studio-stubs.ts
 * 作用：Studio 其余步骤占位 MSW（待业务 API 落地替换）
 * 怎么用：handlers/index.ts 聚合
 * 解决：dev 未实现端点 bypass 前占位 501
 * 上游：pages studio-discover..export
 * 下游：mocks/server.ts
 * 关联：ENGINEERING.md §10
 */
import { http, HttpResponse } from "msw";

const STUB_PATHS = [
  "/v1/integration/discover/validate",
  "/v1/integration/map/preview",
  "/v1/integration/prove/run",
  "/v1/integration/freeze/submit",
  "/v1/integration/export/package",
];

export const studioStubHandlers = STUB_PATHS.map((path) =>
  http.all(path, () =>
    HttpResponse.json(
      { ok: true, stub: true, message: `MSW stub for ${path}` },
      { status: 200 },
    ),
  ),
);
