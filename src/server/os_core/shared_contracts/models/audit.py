"""审计事件模型。

作用：对齐 AuditEvent.schema.json。
业务关联：append-only 审计链；每次写须落审计（R-06）。
上游：audit_service
下游：ExecutionEvidence、OpenAPI /v1/audit/events
关联文档：contracts/schemas/AuditEvent.schema.json
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from os_core.shared_contracts.models.common import Actor


class AuditEventType(StrEnum):
  """审计事件类型（与 Schema enum 一致）。"""

  GRAPH_CREATED = "graph.created"
  GRAPH_SUBMITTED = "graph.submitted"
  GRAPH_FROZEN = "graph.frozen"
  RULESET_FROZEN = "ruleset.frozen"
  EXECUTE_STARTED = "execute.started"
  EXECUTE_COMPLETED = "execute.completed"
  EXECUTE_FAILED = "execute.failed"
  EXECUTE_SIMULATED = "execute.simulated"
  EXECUTE_REVERTED = "execute.reverted"
  RECONCILE_COMPLETED = "reconcile.completed"
  RECONCILE_DRIFT = "reconcile.drift_detected"
  RULE_DENIED = "rule.denied"
  LICENSE_DENIED = "license.denied"
  INTEGRATION_CONNECT_TESTED = "integration.connect_tested"
  INTEGRATION_WRITE_APPROVED = "integration.write_approved"
  INTEGRATION_PROVE_COMPLETED = "integration.prove_completed"
  PACKAGE_EXPORTED = "package.exported"
  PACKAGE_IMPORTED = "package.imported"
  MCP_TOOLS_LIST = "mcp.tools_list"
  MCP_TOOLS_CALL = "mcp.tools_call"
  HARNESS_CONFIRMED = "harness.confirmed"
  HARNESS_REJECTED = "harness.rejected"
  TENANT_SETTINGS_UPDATED = "tenant.settings_updated"


class AuditEvent(BaseModel):
  """append-only 审计事件。

  业务含义：不可改历史；payload 禁止含凭证明文。
  """

  model_config = ConfigDict(extra="forbid")

  event_id: UUID = Field(description="事件 UUID")
  tenant_id: str = Field(description="租户 ID")
  event_type: AuditEventType = Field(description="事件类型")
  actor: Actor = Field(description="操作者")
  occurred_at: datetime = Field(description="发生时间")
  exec_id: UUID | None = Field(default=None, description="关联执行 ID")
  graph_id: str | None = Field(default=None, description="关联图谱 ID")
  graph_version: str | None = Field(default=None, description="关联图谱版本")
  pack_id: str | None = Field(default=None, description="关联 Pack ID")
  plan_id: UUID | None = Field(default=None, description="关联 DslPlan ID")
  payload: dict[str, Any] | None = Field(default=None, description="事件上下文")
  correlation_id: str | None = Field(default=None, description="关联 ID")
