/**
 * 模块：src/apps/web-admin/src/api/functions/studio-shell/flows.fn.ts
 * 作用：Studio 六步 flows 列表 HTTP 实体函数
 * 怎么用：import { getStudioFlows } from '@/api/functions/studio-shell/flows.fn'
 * 解决：导航步骤与后端 /v1/studio/flows 对齐
 * 上游：StudioShellLayout · pages/studio-shell
 * 下游：api/request/client.ts · GET /v1/studio/flows
 * 关联：pages/studio-shell/contracts/README.md · AC-STU-09
 */
import { http } from "@/api/request";
import type { StudioFlowsResult } from "./flows.types";

/** 获取 Studio 六步向导定义。 */
export async function getStudioFlows(): Promise<StudioFlowsResult> {
  return http.get<StudioFlowsResult>("/v1/studio/flows");
}