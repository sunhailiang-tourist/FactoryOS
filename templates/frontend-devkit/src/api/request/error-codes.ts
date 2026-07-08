/**
 * 模块：src/apps/web-admin/src/api/request/error-codes.ts
 * 作用：业务错误码 + 中文 message_zh mirror（SSOT error-registry.yaml）
 * 怎么用：ERROR_CODES · getErrorMessageZh · formatErrorLabel
 * 解决：英文 code 必带中文描述，开发者一眼懂
 * 上游：contracts/error-registry.yaml · sync_error_registry.py
 * 下游：errors.ts · ApiErrorBanner · 页面分支
 * 关联：docs/文档/规格说明/状态码与错误约定.md
 */
export const ERROR_CODES = {
  /** Studio 访问被拒绝：当前角色无权限 */
  AUTH_STUDIO_FORBIDDEN: "AUTH_STUDIO_FORBIDDEN",
  /** Blueprint 结构或 L2 声明无效 */
  BLUEPRINT_INVALID: "BLUEPRINT_INVALID",
  /** Connector 或 Pack 未注册或未配置 */
  CONNECTOR_NOT_CONFIGURED: "CONNECTOR_NOT_CONFIGURED",
  /** Graph 白名单不含该 DSL */
  DSL_NOT_IN_GRAPH: "DSL_NOT_IN_GRAPH",
  /** DSL 动词未注册或参数非法 */
  DSL_UNKNOWN: "DSL_UNKNOWN",
  /** Graph 未冻结或状态不允许该操作 */
  GRAPH_NOT_FROZEN: "GRAPH_NOT_FROZEN",
  /** 幂等键冲突，重复提交 */
  IDEMPOTENCY_CONFLICT: "IDEMPOTENCY_CONFLICT",
  /** 服务器内部错误 */
  INTERNAL_ERROR: "INTERNAL_ERROR",
  /** 字段映射或参数校验失败 */
  MAPPING_ERROR: "MAPPING_ERROR",
  /** 模块或 Pack 未授权 */
  MODULE_NOT_LICENSED: "MODULE_NOT_LICENSED",
  /** 变更请求不存在 */
  REG_CHANGE_NOT_FOUND: "REG_CHANGE_NOT_FOUND",
  /** 变更请求已被拒绝或状态冲突 */
  REG_CHANGE_REJECTED: "REG_CHANGE_REJECTED",
  /** 无生效 Contract Set */
  REG_NO_ACTIVE_CONTRACT: "REG_NO_ACTIVE_CONTRACT",
  /** Pack 不存在 */
  REG_PACK_NOT_FOUND: "REG_PACK_NOT_FOUND",
  /** Registry 资源不存在 */
  REG_RESOURCE_NOT_FOUND: "REG_RESOURCE_NOT_FOUND",
  /** Tenant 不存在 */
  REG_TENANT_NOT_FOUND: "REG_TENANT_NOT_FOUND",
  /** 不支持的 Registry 变更类型 */
  REG_UNSUPPORTED_KIND: "REG_UNSUPPORTED_KIND",
  /** 不允许回滚（含 simulated/dry_run） */
  REVERT_NOT_ALLOWED: "REVERT_NOT_ALLOWED",
  /** 规则拒绝或 RuleSet 状态不允许 */
  RULE_DENIED: "RULE_DENIED",
  /** 租户隔离拒绝 */
  TENANT_FORBIDDEN: "TENANT_FORBIDDEN",
  /** 未知错误 */
  UNKNOWN_ERROR: "UNKNOWN_ERROR",
  /** 请求无法解析或参数类型错误 */
  VAL_BAD_REQUEST: "VAL_BAD_REQUEST",
  /** 请求体验证失败 */
  VAL_SCHEMA_FAILED: "VAL_SCHEMA_FAILED",
} as const;

export type ErrorCodeValue = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];

export const ERROR_MESSAGES_ZH: Record<ErrorCodeValue, string> = {
  AUTH_STUDIO_FORBIDDEN: "Studio 访问被拒绝：当前角色无权限",
  BLUEPRINT_INVALID: "Blueprint 结构或 L2 声明无效",
  CONNECTOR_NOT_CONFIGURED: "Connector 或 Pack 未注册或未配置",
  DSL_NOT_IN_GRAPH: "Graph 白名单不含该 DSL",
  DSL_UNKNOWN: "DSL 动词未注册或参数非法",
  GRAPH_NOT_FROZEN: "Graph 未冻结或状态不允许该操作",
  IDEMPOTENCY_CONFLICT: "幂等键冲突，重复提交",
  INTERNAL_ERROR: "服务器内部错误",
  MAPPING_ERROR: "字段映射或参数校验失败",
  MODULE_NOT_LICENSED: "模块或 Pack 未授权",
  REG_CHANGE_NOT_FOUND: "变更请求不存在",
  REG_CHANGE_REJECTED: "变更请求已被拒绝或状态冲突",
  REG_NO_ACTIVE_CONTRACT: "无生效 Contract Set",
  REG_PACK_NOT_FOUND: "Pack 不存在",
  REG_RESOURCE_NOT_FOUND: "Registry 资源不存在",
  REG_TENANT_NOT_FOUND: "Tenant 不存在",
  REG_UNSUPPORTED_KIND: "不支持的 Registry 变更类型",
  REVERT_NOT_ALLOWED: "不允许回滚（含 simulated/dry_run）",
  RULE_DENIED: "规则拒绝或 RuleSet 状态不允许",
  TENANT_FORBIDDEN: "租户隔离拒绝",
  UNKNOWN_ERROR: "未知错误",
  VAL_BAD_REQUEST: "请求无法解析或参数类型错误",
  VAL_SCHEMA_FAILED: "请求体验证失败",
} as const;

/** SSOT 默认中文；API 未返回 message 时 fallback。 */
export function getErrorMessageZh(code: ErrorCodeValue | string): string {
  const key = code as ErrorCodeValue;
  return ERROR_MESSAGES_ZH[key] ?? ERROR_MESSAGES_ZH.UNKNOWN_ERROR;
}

/**
 * 功能：日志 / UI 调试：CODE · 中文
 * 业务含义：formatErrorLabel 模块对外 API。
 * 上游：同文件文件头。
 * 下游：调用方见文件头。
 */
export function formatErrorLabel(code: ErrorCodeValue | string): string {
  return `${code} · ${getErrorMessageZh(code)}`;
}
