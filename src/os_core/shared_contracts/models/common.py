"""跨契约共享的子模型与枚举。

作用：Actor、通道等被 Execution/Audit 等复用的结构。
业务关联：多模块 DTO 一致，避免重复定义。
上游：contracts/schemas 内嵌 actor 定义
下游：ExecutionRecord、AuditEvent 等
关联文档：contracts/schemas/
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ActorChannel(StrEnum):
  """操作者接入通道。"""

  WEB = "web"
  H5 = "h5"
  API = "api"
  SYSTEM = "system"
  MCP = "mcp"


class Actor(BaseModel):
  """执行或审计操作者身份。

  业务含义：Rule 判定与 Audit 追溯的主体；不含凭证明文。
  """

  model_config = ConfigDict(extra="forbid")

  user_id: str = Field(description="用户或系统主体 ID")
  role: str = Field(description="角色标识，如 role:worker")
  channel: ActorChannel | None = Field(
    default=None,
    description="接入通道；系统内部调用可为 system",
  )


ExecutionStatus = Literal[
  "pending",
  "running",
  "success",
  "failed",
  "reverted",
  "revert_failed",
  "simulated",
]

ConnectorOutcome = Literal[
  "success",
  "timeout",
  "legacy_4xx",
  "legacy_5xx",
  "mapping_error",
  "circuit_open",
]
