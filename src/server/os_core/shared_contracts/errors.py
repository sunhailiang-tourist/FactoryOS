"""平台统一错误码常量。

作用：HTTP/API 与内核异常共用的机器可读错误码与中文默认文案。
业务关联：对齐 OpenAPI 响应与 AC 负向断言（如 GRAPH_NOT_FROZEN）。
上游：contracts/error-registry.yaml（SSOT）· mirror_python 真源
下游：server/api 异常处理器、os_core 各 service、web-admin error-codes.ts
关联文档：docs/文档/规格说明/状态码与错误约定.md
"""
from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
  """FactoryOS 业务错误码 — mirror contracts/error-registry.yaml (mirror_python)。

  禁止手改漂移；变更须先改 SSOT 再 sync --apply。
  """

  AUTH_STUDIO_FORBIDDEN = "AUTH_STUDIO_FORBIDDEN"
  BLUEPRINT_INVALID = "BLUEPRINT_INVALID"
  CONNECTOR_NOT_CONFIGURED = "CONNECTOR_NOT_CONFIGURED"
  DSL_NOT_IN_GRAPH = "DSL_NOT_IN_GRAPH"
  DSL_UNKNOWN = "DSL_UNKNOWN"
  GRAPH_NOT_FROZEN = "GRAPH_NOT_FROZEN"
  IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
  INTERNAL_ERROR = "INTERNAL_ERROR"
  MAPPING_ERROR = "MAPPING_ERROR"
  MODULE_NOT_LICENSED = "MODULE_NOT_LICENSED"
  REG_CHANGE_NOT_FOUND = "REG_CHANGE_NOT_FOUND"
  REG_CHANGE_REJECTED = "REG_CHANGE_REJECTED"
  REG_NO_ACTIVE_CONTRACT = "REG_NO_ACTIVE_CONTRACT"
  REG_PACK_NOT_FOUND = "REG_PACK_NOT_FOUND"
  REG_RESOURCE_NOT_FOUND = "REG_RESOURCE_NOT_FOUND"
  REG_TENANT_NOT_FOUND = "REG_TENANT_NOT_FOUND"
  REG_UNSUPPORTED_KIND = "REG_UNSUPPORTED_KIND"
  REVERT_NOT_ALLOWED = "REVERT_NOT_ALLOWED"
  RULE_DENIED = "RULE_DENIED"
  TENANT_FORBIDDEN = "TENANT_FORBIDDEN"
  UNKNOWN_ERROR = "UNKNOWN_ERROR"
  VAL_BAD_REQUEST = "VAL_BAD_REQUEST"
  VAL_SCHEMA_FAILED = "VAL_SCHEMA_FAILED"


ERROR_MESSAGE_ZH: dict[str, str] = {
  "AUTH_STUDIO_FORBIDDEN": "Studio 访问被拒绝：当前角色无权限",
  "BLUEPRINT_INVALID": "Blueprint 结构或 L2 声明无效",
  "CONNECTOR_NOT_CONFIGURED": "Connector 或 Pack 未注册或未配置",
  "DSL_NOT_IN_GRAPH": "Graph 白名单不含该 DSL",
  "DSL_UNKNOWN": "DSL 动词未注册或参数非法",
  "GRAPH_NOT_FROZEN": "Graph 未冻结或状态不允许该操作",
  "IDEMPOTENCY_CONFLICT": "幂等键冲突，重复提交",
  "INTERNAL_ERROR": "服务器内部错误",
  "MAPPING_ERROR": "字段映射或参数校验失败",
  "MODULE_NOT_LICENSED": "模块或 Pack 未授权",
  "REG_CHANGE_NOT_FOUND": "变更请求不存在",
  "REG_CHANGE_REJECTED": "变更请求已被拒绝或状态冲突",
  "REG_NO_ACTIVE_CONTRACT": "无生效 Contract Set",
  "REG_PACK_NOT_FOUND": "Pack 不存在",
  "REG_RESOURCE_NOT_FOUND": "Registry 资源不存在",
  "REG_TENANT_NOT_FOUND": "Tenant 不存在",
  "REG_UNSUPPORTED_KIND": "不支持的 Registry 变更类型",
  "REVERT_NOT_ALLOWED": "不允许回滚（含 simulated/dry_run）",
  "RULE_DENIED": "规则拒绝或 RuleSet 状态不允许",
  "TENANT_FORBIDDEN": "租户隔离拒绝",
  "UNKNOWN_ERROR": "未知错误",
  "VAL_BAD_REQUEST": "请求无法解析或参数类型错误",
  "VAL_SCHEMA_FAILED": "请求体验证失败",
}


def default_message(code: ErrorCode | str) -> str:
  """返回错误码默认中文文案。

  功能：查 ERROR_MESSAGE_ZH 表。
  业务含义：API 响应与日志统一中文描述；SSOT 为 error-registry.yaml。
  参数 code：ErrorCode 或字符串 code。
  返回：message_zh；未知码回退 UNKNOWN_ERROR。
  """
  key = code.value if isinstance(code, ErrorCode) else code
  return ERROR_MESSAGE_ZH.get(key, ERROR_MESSAGE_ZH["UNKNOWN_ERROR"])


def format_error_label(code: ErrorCode | str) -> str:
  """格式化「code · 中文」调试标签。

  功能：拼接英文 code 与 default_message。
  业务含义：日志与 pytest 断言一眼读懂业务错误。
  参数 code：ErrorCode 或字符串。
  返回：如 RULE_DENIED · 规则拒绝…
  """
  key = code.value if isinstance(code, ErrorCode) else code
  return f"{key} · {default_message(key)}"
