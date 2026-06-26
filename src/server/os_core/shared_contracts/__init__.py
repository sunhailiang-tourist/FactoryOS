"""shared_contracts · 全平台契约真源包。

作用：Pydantic 模型、错误码、JSON Schema 加载。
业务关联：L0 契约代码化；对齐 contracts/schemas。
上游：contracts/ 机器真源
下游：os_core 各 service、server/api
关联文档：src/server/os_core/shared_contracts/README.md
"""
from __future__ import annotations

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.models import (
  AuditEvent,
  BusinessGraph,
  DomainEvent,
  DslPlan,
  ExecutionEvidence,
  ExecutionRecord,
  RuleSet,
)
from os_core.shared_contracts.schema_loader import load_schema, schemas_dir

__all__ = [
  "AuditEvent",
  "BusinessGraph",
  "DomainEvent",
  "DslPlan",
  "ErrorCode",
  "ExecutionEvidence",
  "ExecutionRecord",
  "RuleSet",
  "load_schema",
  "schemas_dir",
]
