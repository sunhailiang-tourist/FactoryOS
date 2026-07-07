/**
 * 模块：src/apps/web-admin/src/api/request/types.ts
 * 作用：request 层共享类型（RequestConfig/ActorContext）
 * 怎么用：client.ts 与 interceptors 引用
 * 解决：HTTP 层类型 SSOT
 * 上游：ARCHITECTURE api/request
 * 下游：client.ts · interceptors.ts
 * 关联：api/request/README.md（若有）
 */
export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type RequestConfig = {
  headers?: Record<string, string>;
  signal?: AbortSignal;
};

export type ActorContext = {
  role: string;
  userId: string;
};