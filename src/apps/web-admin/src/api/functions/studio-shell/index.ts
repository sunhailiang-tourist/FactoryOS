/**
 * 模块：src/apps/web-admin/src/api/functions/studio-shell/index.ts
 * 作用：studio-shell API barrel 导出
 * 怎么用：import from '@/api/functions/{mid}'
 * 解决：模块 API 公共出口
 * 上游：api/functions/studio-shell/registry.ts · fn 文件
 * 下游：pages/studio-shell
 * 关联：pages/studio-shell/contracts/README.md
 */
export { getStudioFlows } from "./flows.fn";
export type { StudioFlowsResult, WizardStep } from "./flows.types";
export { API_MODULE_ENTRIES } from "./registry";