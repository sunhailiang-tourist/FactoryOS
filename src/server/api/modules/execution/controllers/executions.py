"""Execution 查询 HTTP 路由（GET execution · evidence）。

作用：薄路由；委托 execution_service。
业务关联：E-04 查 revert 后状态 · E-09 evidence。
上游：modules/*/routers
下游：os_core.execution_service
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.execution_service import assemble_evidence
from os_core.execution_service.store import find_by_exec_id

router = APIRouter(tags=["Execution"])


@router.get("/v1/executions/{exec_id}")
def get_execution_http(
  exec_id: UUID,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/executions/{execId}（E-04 状态查询）。"""
  record = find_by_exec_id(session, exec_id)
  if record is None:
    raise HTTPException(status_code=404, detail="Execution not found")
  return record.model_dump(mode="json")


@router.get("/v1/executions/{exec_id}/evidence")
def get_execution_evidence_http(
  exec_id: UUID,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/executions/{execId}/evidence（E-09）。"""
  evidence = assemble_evidence(session, exec_id)
  if evidence is None:
    raise HTTPException(status_code=404, detail="Execution not found")
  return evidence.model_dump(mode="json")
