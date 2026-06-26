"""执行记录与证据包模型。

作用：对齐 执行记录.schema.json · ExecutionEvidence.schema.json。
业务关联：Execution 写路径账本、E-09 证据重建。
上游：execution_service
下游：audit_service、OpenAPI /v1/executions
关联文档：contracts/schemas/执行记录.schema.json
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from os_core.shared_contracts.models.audit import AuditEvent
from os_core.shared_contracts.models.common import Actor, ConnectorOutcome, ExecutionStatus


class ExecuteRequest(BaseModel):
  """POST /v1/execute 请求体（对齐 OpenAPI ExecuteRequest）。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  graph_id: str = Field(description="业务图谱 ID")
  graph_version: str = Field(description="图谱版本")
  verb: str = Field(description="DSL 动词")
  params: dict[str, Any] = Field(description="动词参数")
  actor: Actor = Field(description="操作者")
  ruleset_id: str | None = Field(default=None, description="RuleSet ID")
  scope_id: str | None = Field(default=None, description="作用域 ID")
  idempotency_key: str | None = Field(default=None, description="幂等键")
  dry_run: bool = Field(default=False, description="试跑不写 Legacy")


class LegacyRef(BaseModel):
  """Legacy 系统实体引用。"""

  model_config = ConfigDict(extra="forbid")

  system: str = Field(description="目标系统标识，如 erp-kingdee")
  ref_type: str = Field(description="实体类型")
  ref_id: str = Field(description="外部系统主键")


class ConnectorTraceEntry(BaseModel):
  """单次 Connector 调用追踪。"""

  model_config = ConfigDict(extra="forbid")

  pack_id: str = Field(description="Connector Pack ID")
  verb: str = Field(description="CMV 动词")
  latency_ms: int = Field(description="调用耗时毫秒")
  outcome: ConnectorOutcome = Field(description="调用结果分类")
  system: str | None = Field(default=None, description="可选系统标识")
  error_code: str | None = Field(default=None, description="失败时的错误码")


class ExecutionError(BaseModel):
  """执行失败错误体。"""

  model_config = ConfigDict(extra="forbid")

  code: str | None = Field(default=None, description="错误码")
  message: str | None = Field(default=None, description="人类可读说明")


class ExecutionRecord(BaseModel):
  """单次 DSL 执行记录（Revert 锚点）。

  业务含义：每次受控写或模拟写的账本行；E-02/E-04 真源结构。
  """

  model_config = ConfigDict(extra="forbid")

  exec_id: UUID = Field(description="执行 UUID")
  tenant_id: str = Field(description="租户 ID")
  verb: str = Field(description="DSL 动词")
  status: ExecutionStatus = Field(description="执行状态")
  graph_id: str = Field(description="绑定的业务图谱 ID")
  graph_version: str = Field(description="图谱语义版本")
  actor: Actor = Field(description="触发执行的操作者")
  started_at: datetime = Field(description="开始时间 ISO8601")
  scope_id: str | None = Field(default=None, description="产线/工位等作用域")
  ruleset_id: str | None = Field(default=None, description="绑定的 RuleSet ID")
  idempotency_key: str | None = Field(default=None, description="L2 写幂等键")
  shadow_mode: bool = Field(default=False, description="Shadow 模式不写 Legacy")
  params: dict[str, Any] | None = Field(default=None, description="动词参数")
  before_snapshot: dict[str, Any] | None = Field(default=None, description="写前快照")
  after_snapshot: dict[str, Any] | None = Field(default=None, description="写后快照")
  legacy_refs: list[LegacyRef] | None = Field(default=None, description="Legacy 引用列表")
  connector_trace: list[ConnectorTraceEntry] | None = Field(
    default=None,
    description="Connector 调用链",
  )
  compensator_verb: str | None = Field(default=None, description="补偿动词")
  revert_of: UUID | None = Field(default=None, description="被 revert 的原 exec_id")
  error: ExecutionError | None = Field(default=None, description="失败详情")
  finished_at: datetime | None = Field(default=None, description="结束时间")
  dry_run: bool = Field(default=False, description="干跑不写 Legacy")


class RuleSnapshot(BaseModel):
  """执行前 Rule 判定快照。"""

  model_config = ConfigDict(extra="forbid")

  effect: str = Field(description="allow 或 deny")
  ruleset_id: str | None = Field(default=None, description="RuleSet ID")
  graph_id: str | None = Field(default=None, description="Graph ID")
  graph_version: str | None = Field(default=None, description="Graph 版本")
  matched_rule_id: str | None = Field(default=None, description="命中的规则 ID")


class ExecutionEvidence(BaseModel):
  """单次执行可重建审计包（E-09）。

  业务含义：聚合 execution + audit + rule 快照供只读查询。
  """

  model_config = ConfigDict(extra="forbid")

  exec_id: UUID = Field(description="执行 UUID")
  tenant_id: str = Field(description="租户 ID")
  execution: ExecutionRecord = Field(description="执行记录本体")
  audit_events: list[AuditEvent] = Field(description="关联审计事件")
  assembled_at: datetime = Field(description="证据包组装时间")
  rule_snapshot: RuleSnapshot | None = Field(default=None, description="Rule 判定快照")
  graph_checksum: str | None = Field(default=None, description="frozen Graph checksum")
  dsl_plan_id: UUID | None = Field(default=None, description="来源 DslPlan ID")
  reconciliation_refs: list[UUID] | None = Field(default=None, description="对账 run_id 列表")
  trace_id: str | None = Field(default=None, description="分布式追踪 ID")
