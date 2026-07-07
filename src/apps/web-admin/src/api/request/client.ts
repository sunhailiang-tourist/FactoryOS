/**
 * 模块：src/apps/web-admin/src/api/request/client.ts
 * 作用：HTTP 客户端 — 全站唯一 fetch 封装
 * 怎么用：api/functions 通过 http.get/post 调用
 * 解决：禁止 pages 直接 fetch；统一错误解析与 headers
 * 上游：vite proxy /v1 · buildDefaultHeaders
 * 下游：api/functions 模块
 * 关联：ENGINEERING.md §3 · contracts/error-registry.yaml
 */
import { ApiError, NetworkError, parseApiErrorBody } from "./errors";
import { buildDefaultHeaders } from "./interceptors";
import type { RequestConfig } from "./types";

async function parseBody<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!text) {
    return undefined as T;
  }
  try {
    return JSON.parse(text) as T;
  } catch {
    return text as T;
  }
}

async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  config?: RequestConfig,
): Promise<T> {
  const headers = buildDefaultHeaders(config?.headers);
  let response: Response;

  try {
    response = await fetch(path, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: config?.signal,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "network failed";
    throw new NetworkError(message);
  }

  const data = await parseBody<unknown>(response);
  if (!response.ok) {
    const errorBody = parseApiErrorBody(data, response.status);
    throw new ApiError(response.status, errorBody.message, errorBody);
  }

  return data as T;
}

export const http = {
  get: <T>(path: string, config?: RequestConfig) => request<T>("GET", path, undefined, config),
  post: <T>(path: string, body?: unknown, config?: RequestConfig) =>
    request<T>("POST", path, body, config),
  put: <T>(path: string, body?: unknown, config?: RequestConfig) =>
    request<T>("PUT", path, body, config),
  patch: <T>(path: string, body?: unknown, config?: RequestConfig) =>
    request<T>("PATCH", path, body, config),
  del: <T>(path: string, config?: RequestConfig) => request<T>("DELETE", path, undefined, config),
};