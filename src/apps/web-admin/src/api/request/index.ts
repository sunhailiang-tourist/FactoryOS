/**
 * 模块：src/apps/web-admin/src/api/request/index.ts
 * 作用：api/request barrel 导出
 * 怎么用：import { http, ApiError, setActorContext } from '@/api/request'
 * 解决：request 层唯一公共出口
 * 上游：client/errors/interceptors/types
 * 下游：api/functions 与 pages（仅类型/headers）
 * 关联：ENGINEERING.md §3
 */
export { http } from "./client";
export { ApiError, NetworkError } from "./errors";
export { ERROR_CODES, ERROR_MESSAGES_ZH, getErrorMessageZh, formatErrorLabel } from "./error-codes";
export type { ErrorCodeValue } from "./error-codes";
export { setActorContext, getActorContext, buildDefaultHeaders } from "./interceptors";
export type { ActorContext, HttpMethod, RequestConfig } from "./types";