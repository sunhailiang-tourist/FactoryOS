"""Execution 域 HTTP 路由（OpenAPI POST /v1/execute · revert）。

作用：薄路由；委托 execution_service。
业务关联：E-02 真写 · E-04/E-05 revert。
上游：modules/*/routers
下游：os_core.execution_service
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.execution_service import execute, revert_execution
from os_core.shared_contracts.models.execution import ExecuteRequest

router = APIRouter(tags=["Execution"])


@router.post("/v1/execute")
def execute_http(
  body: ExecuteRequest,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/execute（L2 真写 / dry_run）。"""
  record = execute(session, body)
  session.commit()
  return record.model_dump(mode="json")


@router.post("/v1/execute/{exec_id}/revert")
def revert_execution_http(
  exec_id: UUID,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/execute/{execId}/revert（E-04 · E-05）。"""
  record = revert_execution(session, exec_id)
  session.commit()
  return record.model_dump(mode="json")
