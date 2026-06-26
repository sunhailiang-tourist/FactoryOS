"""DSL 执行计划模型。

作用：对齐 DslPlan.schema.json。
业务关联：Agent/MCP/Harness 产出计划；确认前不得写 Legacy（R-11）。
上游：agent_orchestrator、mcp_gateway、harness
下游：execution_service（确认后）
关联文档：contracts/schemas/DslPlan.schema.json
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DslPlanSource(StrEnum):
  """计划来源通道。"""

  MCP = "mcp"
  AGENT = "agent"
  HARNESS = "harness"
  PERCEPTION = "perception"
  API = "api"


class PerceptionModality(StrEnum):
  """多模态类型。"""

  VOICE = "voice"
  IMAGE = "image"
  SCAN = "scan"
  TEXT = "text"


class PerceptionRef(BaseModel):
  """多模态输入引用。"""

  model_config = ConfigDict(extra="forbid")

  modality: PerceptionModality = Field(description="模态类型")
  ref_id: str = Field(description="存储或会话引用 ID")
  confidence: float | None = Field(default=None, ge=0.0, le=1.0, description="识别置信度")


class PlanStep(BaseModel):
  """DSL 计划单步。"""

  model_config = ConfigDict(extra="forbid")

  verb: str = Field(description="CMV 动词，大写下划线")
  params: dict[str, Any] = Field(description="动词参数")
  idempotency_key: str | None = Field(default=None, description="本步幂等键")


class DslPlan(BaseModel):
  """DSL 执行计划。

  业务含义：Harness 确认门前仅为意图；confirmed_at 前禁止 execution 写 Legacy。
  """

  model_config = ConfigDict(extra="forbid")

  plan_id: UUID = Field(description="计划 UUID")
  tenant_id: str = Field(description="租户 ID")
  graph_id: str = Field(description="目标图谱 ID")
  graph_version: str = Field(description="目标图谱版本 vX.Y.Z")
  steps: list[PlanStep] = Field(min_length=1, description="至少一步 DSL")
  source: DslPlanSource = Field(description="计划来源")
  created_at: datetime = Field(description="创建时间")
  expires_at: datetime = Field(description="过期时间")
  ruleset_id: str | None = Field(default=None, description="可选 RuleSet")
  scope_id: str | None = Field(default=None, description="作用域")
  dry_run: bool = Field(default=False, description="干跑标记")
  perception_refs: list[PerceptionRef] | None = Field(
    default=None,
    description="多模态引用",
  )
  summary: str | None = Field(default=None, description="用户可见摘要")
  confirmed_at: datetime | None = Field(default=None, description="Harness 确认时间")
  confirmed_by: str | None = Field(default=None, description="确认人")
