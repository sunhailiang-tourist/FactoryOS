/**
 * 模块：src/apps/web-admin/src/api/request/interceptors.ts
 * 作用：Actor 上下文与默认请求头
 * 怎么用：setActorContext 在登录/bootstrap；buildDefaultHeaders 供 client
 * 解决：X-Actor-Role/User-Id 注入，对齐 STU-09 RBAC
 * 上游：bootstrap/登录流
 * 下游：api/request/client.ts
 * 关联：AC-STU-09 · Integration-Studio规格
 */
import type { ActorContext } from "./types";

let actorContext: ActorContext = {
  role: "integrator",
  userId: "web-admin-dev",
};

/** 设置当前操作者上下文（登录后由壳层注入）。 */
export function setActorContext(ctx: Partial<ActorContext>): void {
  actorContext = { ...actorContext, ...ctx };
}

/**
 * 功能：读取当前操作者（layout/guard 与请求头同源）
 * 业务含义：getActorContext 模块对外 API。
 * 上游：同文件文件头。
 * 下游：调用方见文件头。
 */
export function getActorContext(): Readonly<ActorContext> {
  return actorContext;
}

/**
 * 功能：读取默认请求头
 * 业务含义：buildDefaultHeaders 模块对外 API。
 * 上游：同文件文件头。
 * 下游：调用方见文件头。
 */
export function buildDefaultHeaders(extra?: Record<string, string>): Record<string, string> {
  return {
    "Content-Type": "application/json",
    "X-Actor-Role": actorContext.role,
    "X-Actor-User-Id": actorContext.userId,
    ...extra,
  };
}