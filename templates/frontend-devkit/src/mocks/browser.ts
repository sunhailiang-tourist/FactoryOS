/**
 * 模块：src/apps/web-admin/src/mocks/browser.ts
 * 作用：浏览器 dev MSW worker（VITE_MSW=1）
 * 怎么用：main.tsx 条件 dynamic import
 * 解决：本地无 API 时前端独立开发
 * 上游：handlers/index.ts
 * 下游：vite dev（可选）
 * 关联：ENGINEERING.md §6
 */
import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";

export const worker = setupWorker(...handlers);
