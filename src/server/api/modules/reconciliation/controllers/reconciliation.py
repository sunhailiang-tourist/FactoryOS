"""Reconciliation 域 HTTP 路由（OpenAPI POST /v1/reconciliation/run）。

作用：薄路由；委托 reconciliation_service.run_reconciliation。
业务关联：K-01/K-02 对账 Job HTTP 入口。
上游：modules/*/routers
下游：os_core.reconciliation_service
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.reconciliation_service import run_reconciliation

router = APIRouter(tags=["Reconciliation"])


class ReconciliationRunBody(BaseModel):
  """POST /v1/reconciliation/run 请求体（OpenAPI ReconciliationRunRequest）。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  scope: Literal["daily", "ad_hoc"] = Field(default="ad_hoc", description="对账范围")
  graph_id: str | None = Field(default=None, description="可选 Graph 过滤")
  since: datetime | None = Field(default=None, description="可选起始时间")


@router.post("/v1/reconciliation/run")
def run_reconciliation_http(
  body: ReconciliationRunBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/reconciliation/run（K-01 ok · K-02 drift_detected）。"""
  report = run_reconciliation(
    session,
    tenant_id=body.tenant_id,
    scope=body.scope,
    graph_id=body.graph_id,
    since=body.since,
  )
  return report.model_dump(mode="json")
