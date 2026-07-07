/**
 * 模块：src/apps/web-admin/src/components/index.ts
 * 作用：components barrel 导出
 * 怎么用：import from '@/components'
 * 解决：全局复用组件公共出口
 * 上游：各组件文件
 * 下游：AppShell · layout · pages
 * 关联：components/README.md
 */
export { ApiErrorBanner } from "./ApiErrorBanner";
export { AppThemeProvider } from "./AppThemeProvider";
export { PageLoading } from "./PageLoading";
export { appTheme } from "./theme";
export * from "./forms";