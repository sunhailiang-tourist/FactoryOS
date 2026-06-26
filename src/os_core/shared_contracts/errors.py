"""平台统一错误码常量。

作用：HTTP/API 与内核异常共用的机器可读错误码。
业务关联：对齐 OpenAPI 响应与 AC 负向断言（如 GRAPH_NOT_FROZEN）。
上游：contracts/acceptance · OpenAPI
下游：apps/api 异常处理器、os_core 各 service
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
  """FactoryOS 核心错误码枚举。

  业务含义：客户端与审计可稳定识别失败原因；禁止散落魔法字符串。
  """

  GRAPH_NOT_FROZEN = "GRAPH_NOT_FROZEN"
  RULE_DENIED = "RULE_DENIED"
  DSL_UNKNOWN = "DSL_UNKNOWN"
  DSL_NOT_IN_GRAPH = "DSL_NOT_IN_GRAPH"
  MODULE_NOT_LICENSED = "MODULE_NOT_LICENSED"
  TENANT_FORBIDDEN = "TENANT_FORBIDDEN"
  IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
  REVERT_NOT_ALLOWED = "REVERT_NOT_ALLOWED"
  BLUEPRINT_INVALID = "BLUEPRINT_INVALID"
  MAPPING_ERROR = "MAPPING_ERROR"
  CONNECTOR_NOT_CONFIGURED = "CONNECTOR_NOT_CONFIGURED"
