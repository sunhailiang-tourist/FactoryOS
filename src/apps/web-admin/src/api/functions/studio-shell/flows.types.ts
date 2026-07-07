/**
 * 模块：src/apps/web-admin/src/api/functions/studio-shell/flows.types.ts
 * 作用：Studio flows 响应 TypeScript 类型
 * 怎么用：flows.fn.ts 与 store/页面共用
 * 解决：前后端 flows JSON 形状对齐
 * 上游：server/api studio 模块 OpenAPI
 * 下游：flows.fn.ts · studio-shell store/页面
 * 关联：pages/studio-shell/contracts/README.md
 */
export type WizardStep = {
  id: string;
  order: number;
  title: string;
  summary: string;
  /** 前端路由 path（缺省 `/studio/{id}`） */
  path?: string;
};

export type StudioFlowsResult = {
  title?: string;
  steps?: WizardStep[];
};