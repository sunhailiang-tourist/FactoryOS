"""Execution 查询 HTTP 路由（OpenAPI GET /v1/executions/{execId}/evidence）。

作用：薄路由；委托 execution_service.assemble_evidence。
业务关联：E-09 可重建审计包。
上游：FastAPI app
下游：os_core.execution_service
关联文档：contracts/schemas/ExecutionEvidence.schema.json
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.api.deps import get_db_session
from os_core.execution_service import assemble_evidence

router = APIRouter(tags=["Execution"])


@router.get("/v1/executions/{exec_id}/evidence")
def get_execution_evidence_http(
  exec_id: UUID,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/executions/{execId}/evidence（E-09）。

  功能：返回 Execution + audit_events 聚合包。
  业务含义：F1 合规只读入口；无 exec 时 404。
  """
  evidence = assemble_evidence(session, exec_id)
  if evidence is None:
    raise HTTPException(status_code=404, detail="Execution not found")
  return evidence.model_dump(mode="json")
