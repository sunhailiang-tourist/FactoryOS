/**
 * 模块：src/apps/web-admin/src/router/compose.tsx
 * 作用：路由组装兼容导出（真源 browser-router.tsx）
 * 怎么用：新代码用 createAppRouter + RouterProvider
 * 解决：保留 harness/文档引用路径；compose 不再直接挂 Routes
 * 上游：router/browser-router.tsx
 * 下游：ARCHITECTURE.md 追踪链
 * 关联：router/contracts/README.md
 */
export { createAppRouter } from "@/router/browser-router";
