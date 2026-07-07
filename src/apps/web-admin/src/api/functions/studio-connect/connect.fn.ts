/**
 * 模块：src/apps/web-admin/src/api/functions/studio-connect/connect.fn.ts
 * 作用：Studio Connect 连通测试 HTTP 实体函数
 * 怎么用：import { postConnectTest } from '@/api/functions/studio-connect/connect.fn'
 * 解决：pages 禁 fetch；POST /v1/integration/connect/test 唯一出口
 * 上游：pages/studio-connect · store
 * 下游：api/request/client.ts · server/api integration
 * 关联：pages/studio-connect/contracts/README.md · Playbook G-CONNECT
 */
import { http } from "@/api/request";

export type ConnectTestPayload = {
  tenant_id: string;
  relation_id: string;
};

export type ConnectTestResult = {
  ok: boolean;
  message?: string;
};

/** 凭证连通 ping（占位实现，Step 4 补全 payload 校验）。 */
export async function postConnectTest(body: ConnectTestPayload): Promise<ConnectTestResult> {
  return http.post<ConnectTestResult>("/v1/integration/connect/test", body);
}