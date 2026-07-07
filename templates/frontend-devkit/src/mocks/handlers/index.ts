/**
 * 模块：src/apps/web-admin/src/mocks/handlers/index.ts
 * 作用：MSW handlers 聚合入口
 * 怎么用：mocks/server.ts import handlers
 * 解决：按 module-id 扩展 handler 文件
 * 上游：handlers/studio-*.ts
 * 下游：mocks/server.ts · mocks/browser.ts
 * 关联：ENGINEERING.md §10 S4
 */
import { studioConnectHandlers } from "./studio-connect";
import { studioShellHandlers } from "./studio-shell";
import { studioStubHandlers } from "./studio-stubs";

export const handlers = [
  ...studioShellHandlers,
  ...studioConnectHandlers,
  ...studioStubHandlers,
];
