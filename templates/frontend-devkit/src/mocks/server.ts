/**
 * 模块：src/apps/web-admin/src/mocks/server.ts
 * 作用：Vitest / Node 环境 MSW server
 * 怎么用：test/setup.ts beforeAll server.listen()
 * 解决：单元/组件测试拦截 fetch
 * 上游：handlers/index.ts
 * 下游：test/setup.ts
 * 关联：ENGINEERING.md §6
 */
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);
