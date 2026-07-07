/**
 * 模块：src/apps/web-admin/src/api/request/errors.ts
 * 作用：ApiError/NetworkError 与响应体解析
 * 怎么用：client.ts 抛出；页面 catch ApiError.code
 * 解决：业务码与 HTTP 状态解耦，对齐 error-registry
 * 上游：client.ts · 后端 JSON 错误体
 * 下游：pages 与全局 error boundary（可选）
 * 关联：docs/文档/规格说明/状态码与错误约定.md
 */
import { ERROR_CODES, getErrorMessageZh } from "./error-codes";

export type ApiErrorBody = {
  code: string;
  message: string;
  detail?: string;
  details?: unknown;
  trace_id?: string;
  upstream?: { code: string; message: string };
};

export class ApiError extends Error {
  readonly httpStatus: number;
  readonly code: string;
  readonly body: ApiErrorBody;

  constructor(httpStatus: number, message: string, body: ApiErrorBody) {
    super(message);
    this.name = "ApiError";
    this.httpStatus = httpStatus;
    this.code = body.code || ERROR_CODES.UNKNOWN_ERROR;
    this.body = body;
  }
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NetworkError";
  }
}

/** 从非 2xx JSON 体解析标准错误字段。 */
export function parseApiErrorBody(data: unknown, httpStatus: number): ApiErrorBody {
  if (typeof data !== "object" || data === null) {
    return {
      code: ERROR_CODES.UNKNOWN_ERROR,
      message: typeof data === "string" ? data : `HTTP ${httpStatus}`,
    };
  }
  const obj = data as Record<string, unknown>;
  const rawMessage = String(obj.message ?? obj.detail ?? "").trim();
  const code = typeof obj.code === "string" ? obj.code : ERROR_CODES.UNKNOWN_ERROR;
  const message = rawMessage || getErrorMessageZh(code);
  return {
    code,
    message,
    detail: typeof obj.detail === "string" ? obj.detail : message,
    details: obj.details,
    trace_id: typeof obj.trace_id === "string" ? obj.trace_id : undefined,
    upstream:
      typeof obj.upstream === "object" && obj.upstream !== null
        ? (obj.upstream as { code: string; message: string })
        : undefined,
  };
}