/**
 * 模块：src/apps/web-admin/src/api/functions/studio-connect/index.ts
 * 作用：studio-connect API barrel 导出
 * 怎么用：import from '@/api/functions/{mid}'
 * 解决：模块 API 公共出口
 * 上游：api/functions/studio-connect/registry.ts · fn 文件
 * 下游：pages/studio-connect
 * 关联：pages/studio-connect/contracts/README.md
 */
export { postConnectTest } from "./connect.fn";
export { API_MODULE_ENTRIES } from "./registry";