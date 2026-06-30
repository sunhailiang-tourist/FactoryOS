"""对账报告模型。

作用：对齐 ReconciliationReport.schema.json。
业务关联：K-01/K-02 对账 Job 产出。
上游：reconciliation_service
下游：POST /v1/reconciliation/run OpenAPI
关联文档：contracts/schemas/ReconciliationReport.schema.json
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReconciliationDrift(BaseModel):
  """单条 drift 明细（ExecutionRecord vs Legacy read-back）。"""

  model_config = ConfigDict(extra="forbid")

  exec_id: UUID = Field(description="ExecutionRecord.exec_id")
  legacy_ref: str | None = Field(default=None, description="Legacy 引用（entity_type/entity_id）")
  system: str | None = Field(default=None, description="Legacy 系统标识")
  field: str = Field(description="不一致字段名")
  expected: Any = Field(description="ExecutionRecord after_snapshot 期望值")
  actual: Any = Field(description="Legacy read-back 实际值")
  severity: Literal["warning", "critical"] = Field(default="critical", description="严重级别")
  explainable: bool = Field(default=False, description="是否可解释 drift")


class ReconciliationReport(BaseModel):
  """对账 Job 结果。"""

  model_config = ConfigDict(extra="forbid")

  run_id: UUID = Field(description="对账 run UUID")
  tenant_id: str = Field(description="租户 ID")
  scope: Literal["daily", "ad_hoc"] | None = Field(default=None, description="对账范围")
  graph_id: str | None = Field(default=None, description="可选 Graph 过滤")
  since: datetime | None = Field(default=None, description="可选起始时间")
  started_at: datetime = Field(description="Job 开始时间")
  finished_at: datetime = Field(description="Job 结束时间")
  status: Literal["ok", "drift_detected", "failed"] = Field(description="对账结论")
  records_checked: int | None = Field(default=None, ge=0, description="已核对 ExecutionRecord 数")
  records_skipped_shadow: int | None = Field(
    default=None,
    ge=0,
    description="跳过的 shadow/dry_run 记录数",
  )
  path: Literal["A", "B", "C"] | None = Field(default=None, description="Legacy 路径")
  drifts: list[ReconciliationDrift] = Field(default_factory=list, description="drift 明细")
  error: dict[str, str] | None = Field(default=None, description="failed 时错误信息")
