"""规则集模型。

作用：对齐 规则集.schema.json（RuleSet）。
业务关联：Rule Engine 授权；默认 deny（R-04）。
上游：rule_engine
下游：execution_service
关联文档：contracts/schemas/规则集.schema.json
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RuleSetStatus(StrEnum):
  """规则集状态。"""

  DRAFT = "draft"
  FROZEN = "frozen"
  DEPRECATED = "deprecated"


class RuleEffect(StrEnum):
  """单条规则效果。"""

  ALLOW = "allow"
  DENY = "deny"


class ConditionOp(StrEnum):
  """条件运算符。"""

  EQ = "eq"
  NE = "ne"
  LT = "lt"
  LTE = "lte"
  GT = "gt"
  GTE = "gte"
  IN = "in"
  NOT_IN = "not_in"


class RuleCondition(BaseModel):
  """规则条件项。"""

  model_config = ConfigDict(extra="forbid")

  field: str = Field(description="字段路径，如 time.within_shift")
  op: ConditionOp = Field(description="比较运算符")
  value: Any = Field(description="比较值")


class Rule(BaseModel):
  """授权规则条目。"""

  model_config = ConfigDict(extra="forbid")

  id: str = Field(description="规则 ID，rule- 前缀")
  effect: RuleEffect = Field(description="allow 或 deny")
  subjects: list[str] = Field(description="主体列表，如 role:worker")
  actions: list[str] = Field(description="DSL 动词列表")
  conditions: list[RuleCondition] | None = Field(default=None, description="附加条件")
  priority: int = Field(default=0, description="优先级，deny 优先策略在引擎内")


class RuleSetMetadata(BaseModel):
  """规则集元数据。"""

  model_config = ConfigDict(extra="forbid")

  created_at: datetime = Field(description="创建时间")
  updated_at: datetime = Field(description="更新时间")
  frozen_at: datetime | None = Field(default=None, description="冻结时间")
  frozen_by: str | None = Field(default=None, description="冻结操作者")


class RuleSet(BaseModel):
  """绑定 Graph 版本的规则集。

  业务含义：evaluate 输入；frozen 后不可原地修改（R-08）。
  """

  model_config = ConfigDict(extra="forbid")

  id: str = Field(description="规则集 ID，ruleset- 前缀")
  graph_id: str = Field(description="绑定的图谱 ID")
  graph_version: str = Field(description="绑定的图谱版本")
  status: RuleSetStatus = Field(description="规则集状态")
  rules: list[Rule] = Field(min_length=1, description="至少一条规则")
  metadata: RuleSetMetadata = Field(description="元数据")
  default_effect: RuleEffect = Field(
    default=RuleEffect.DENY,
    description="无匹配时默认效果",
  )
