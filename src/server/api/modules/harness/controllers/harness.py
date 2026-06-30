"""Harness 域 HTTP 路由（OpenAPI POST /v1/harness/confirm）。

作用：薄路由；委托 application.confirm_harness。
业务关联：H-02 确认门 · H-03 audit 链路。
上游：modules/*/routers
下游：harness.application.confirm_flow
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from server.api.modules.harness.application.confirm_flow import confirm_harness
from sqlalchemy.orm import Session

router = APIRouter(tags=["Harness"])


class HarnessConfirmBody(BaseModel):
  """POST /v1/harness/confirm 请求体（OpenAPI v1.1）。"""

  model_config = ConfigDict(extra="forbid")

  plan_id: UUID = Field(description="待确认的 DslPlan UUID")
  confirmed: bool = Field(description="true=确认执行 · false=拒绝")
  user_id: str = Field(description="操作员 ID")
  dry_run: bool = Field(default=False, description="试跑不写 Legacy")


@router.post("/v1/harness/confirm")
def harness_confirm_http(
  body: HarnessConfirmBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/harness/confirm（H-02 · confirm→execute）。"""
  result = confirm_harness(
    session,
    plan_id=body.plan_id,
    confirmed=body.confirmed,
    user_id=body.user_id,
    dry_run=body.dry_run,
  )
  return result.model_dump(mode="json")
