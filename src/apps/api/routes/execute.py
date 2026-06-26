"""Execution 域 HTTP 路由（OpenAPI POST /v1/execute）。

作用：薄路由；委托 execution_service.execute。
业务关联：E-03 端到端产生 audit；W2 Step2 最小 execute。
上游：FastAPI app
下游：os_core.execution_service
关联文档：contracts/openapi ExecuteRequest
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.deps import get_db_session
from os_core.execution_service import execute
from os_core.shared_contracts.models.execution import ExecuteRequest

router = APIRouter(tags=["Execution"])


@router.post("/v1/execute")
def execute_http(
  body: ExecuteRequest,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/execute（W2 dry_run 路径）。

  功能：创建 ExecutionRecord 并产生 audit。
  业务含义：唯一写 Legacy 入口；dry_run 时 status=simulated。
  """
  record = execute(session, body)
  session.commit()
  return record.model_dump(mode="json")
