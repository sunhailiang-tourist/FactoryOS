/**
 * 模块：src/apps/web-admin/src/test/setup.ts
 * 作用：Vitest 全局 setup — MSW + jest-dom
 * 怎么用：vitest.config.ts setupFiles
 * 解决：RTL 与 API mock 统一初始化
 * 上游：mocks/server.ts
 * 下游：*.test.tsx
 * 关联：ENGINEERING.md §6 · W-04
 */
import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "@/mocks/server";

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
