"""业务图谱模型。

作用：对齐 业务图谱.schema.json（BusinessGraph）。
业务关联：Graph freeze 门禁；仅 frozen 允许 L2 写（R-03）。
上游：graph_service
下游：rule_engine、execution_service
关联文档：contracts/schemas/业务图谱.schema.json
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GraphStatus(StrEnum):
  """图谱生命周期状态。"""

  DRAFT = "draft"
  IN_REVIEW = "in_review"
  FROZEN = "frozen"
  DEPRECATED = "deprecated"


class GraphNodeType(StrEnum):
  """图谱节点类型。"""

  START = "start"
  QUERY = "query"
  ACTION = "action"
  CONFIRM = "confirm"
  GATEWAY = "gateway"
  END = "end"


class GraphNode(BaseModel):
  """业务图谱节点。"""

  model_config = ConfigDict(extra="forbid")

  id: str = Field(description="节点 ID，node- 前缀")
  type: GraphNodeType = Field(description="节点类型")
  label: str = Field(description="展示标签")
  dsl_verbs: list[str] | None = Field(default=None, description="节点关联动词")
  entity_ref: str | None = Field(default=None, description="逻辑实体引用")
  config: dict[str, Any] | None = Field(default=None, description="扩展配置")


class GraphEdge(BaseModel):
  """业务图谱边。"""

  model_config = ConfigDict(extra="forbid", populate_by_name=True)

  id: str = Field(description="边 ID，edge- 前缀")
  from_: str = Field(alias="from", description="源节点 ID")
  to: str = Field(description="目标节点 ID")
  condition: str | None = Field(default=None, description="Rule 条件表达式")
  label: str | None = Field(default=None, description="边标签")


class GraphMetadata(BaseModel):
  """图谱元数据。"""

  model_config = ConfigDict(extra="forbid")

  created_at: datetime = Field(description="创建时间")
  updated_at: datetime = Field(description="更新时间")
  frozen_at: datetime | None = Field(default=None, description="冻结时间")
  frozen_by: str | None = Field(default=None, description="冻结操作者")
  description: str | None = Field(default=None, description="说明")
  pack_id: str | None = Field(default=None, description="来源 Pack ID")


class BusinessGraph(BaseModel):
  """FactoryOS 业务图谱。

  业务含义：流程冻结载体；checksum 用于 N-02 防篡改。
  """

  model_config = ConfigDict(extra="forbid")

  id: str = Field(description="图谱 ID，graph- 前缀")
  version: str = Field(description="语义版本 vX.Y.Z")
  status: GraphStatus = Field(description="生命周期状态")
  checksum: str = Field(description="canonical JSON SHA-256")
  nodes: list[GraphNode] = Field(min_length=1, description="至少一个节点")
  edges: list[GraphEdge] = Field(description="边列表，可为空")
  metadata: GraphMetadata = Field(description="元数据")
  tenant_id: str | None = Field(default=None, description="租户 ID；null 为平台模板")
  allowed_dsl: list[str] | None = Field(default=None, description="允许的 DSL 动词子集")
