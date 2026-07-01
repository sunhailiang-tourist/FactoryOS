"""Execution 查询 HTTP 路由（GET execution · evidence）。

作用：薄路由；委托 execution_service。
业务关联：E-04 查 revert 后状态 · E-09 evidence。
上游：modules/*/routers
下游：os_core.execution_service
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from server.api.config.dependencies.db import get_db_session
from server.api.config.tenant.dependencies import get_tenant_id
from sqlalchemy.orm import Session

from os_core.execution_service import assemble_evidence_for_tenant, get_execution_for_tenant

router = APIRouter(tags=["Execution"])


@router.get("/v1/executions/{exec_id}")
def get_execution_http(
  exec_id: UUID,
  request: Request,
  tenant_id: str | None = Query(default=None, description="调用方租户 ID"),
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/executions/{execId}（E-04 · N-03 tenant 隔离）。"""
  caller_tenant = tenant_id or get_tenant_id(request)
  record = get_execution_for_tenant(
    session,
    exec_id,
    caller_tenant_id=caller_tenant,
  )
  return record.model_dump(mode="json")


@router.get("/v1/executions/{exec_id}/evidence")
def get_execution_evidence_http(
  exec_id: UUID,
  request: Request,
  tenant_id: str | None = Query(default=None, description="调用方租户 ID"),
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/executions/{execId}/evidence（E-09 · N-03 tenant 隔离）。"""
  caller_tenant = tenant_id or get_tenant_id(request)
  evidence = assemble_evidence_for_tenant(
    session,
    exec_id,
    caller_tenant_id=caller_tenant,
  )
  return evidence.model_dump(mode="json")
