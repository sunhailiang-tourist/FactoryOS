"""Audit 域 HTTP 路由（OpenAPI /v1/audit/events）。

作用：薄路由；查询 append-only 审计。
业务关联：E-03 验收。
上游：modules/*/routers
下游：os_core.audit_service.store
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.audit_service.store import list_audit_events

router = APIRouter(tags=["Audit"])


@router.get("/v1/audit/events")
def list_audit_events_http(
  tenant_id: str = Query(..., description="租户 ID"),
  exec_id: UUID | None = Query(default=None, description="过滤执行 ID"),
  event_type: str | None = Query(default=None, description="事件类型"),
  since: datetime | None = Query(default=None, description="起始时间 ISO8601"),
  limit: int = Query(default=100, ge=1, le=500),
  session: Session = Depends(get_db_session),
) -> list[dict[str, Any]]:
  """GET /v1/audit/events（E-03）。

  功能：按 tenant 查询审计事件列表。
  业务含义：append-only 只读；禁止 UPDATE/DELETE。
  """
  events = list_audit_events(
    session=session,
    tenant_id=tenant_id,
    exec_id=exec_id,
    event_type=event_type,
    since=since,
    limit=limit,
  )
  return [e.model_dump(mode="json") for e in events]
