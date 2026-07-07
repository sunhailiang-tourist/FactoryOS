/**
 * 模块：src/apps/web-admin/src/AppShell.tsx
 * 作用：兼容导出 — 路由已迁至 bootstrap（S4）
 * 怎么用：测试/Storybook 可继续 import createAppRouter
 * 解决：避免双 RouterProvider
 * 上游：bootstrap.tsx
 * 下游：browser-router.test
 * 关联：ARCHITECTURE.md §2
 */
export { Bootstrap as AppShell } from "@/bootstrap";
