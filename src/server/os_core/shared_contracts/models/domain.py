"""域事件信封模型。

作用：对齐 DomainEvent.schema.json。
业务关联：同进程事件总线；S-04 outbox 可换实现不改 payload。
上游：graph_service、execution_service
下游：内部 handler、未来消息队列
关联文档：contracts/schemas/DomainEvent.schema.json
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DomainEventType(StrEnum):
  """域事件类型。"""

  GRAPH_FROZEN = "graph.frozen"
  EXECUTION_COMPLETED = "execution.completed"
  EXECUTION_REVERTED = "execution.reverted"


class DomainEvent(BaseModel):
  """Core 同进程事件信封。

  业务含义：W1 handler 接口预留；payload 形态由 event_type 决定。
  """

  model_config = ConfigDict(extra="forbid")

  event_id: UUID = Field(description="事件 UUID")
  event_type: DomainEventType = Field(description="事件类型")
  occurred_at: datetime = Field(description="发生时间")
  tenant_id: str = Field(description="租户 ID")
  payload: dict[str, Any] = Field(description="类型特定载荷")
  trace_id: str | None = Field(default=None, description="追踪 ID")
