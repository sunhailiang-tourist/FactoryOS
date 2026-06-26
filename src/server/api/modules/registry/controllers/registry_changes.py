"""Registry 变更请求 HTTP 路由（人审写路径 · ADR-008）。

作用：Studio/AI 提案 → pending → 人审 approve/reject → Registry 落库。
业务关联：R-09 AI 不得自动 publish；须 UI 确认。
上游：Integration Studio
下游：change_request_store
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.platform_registry import change_request_store

router = APIRouter(tags=["Registry"])


class ChangeRequestCreate(BaseModel):
  """创建变更请求（提案）。"""

  tenant_id: str | None = None
  kind: str = Field(description="pack_upsert | system_relation_upsert")
  proposed_by: str
  proposal_body: dict[str, Any]
  ai_model_id: str | None = None


class ChangeRequestDecision(BaseModel):
  """人审决定。"""

  actor_id: str
  reason: str | None = None


@router.post("/v1/registry/change-requests", status_code=201)
def create_change_request(
  body: ChangeRequestCreate,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """提交变更提案（pending，不直接改 Registry）。"""
  if body.kind not in ("pack_upsert", "system_relation_upsert"):
    raise HTTPException(status_code=422, detail=f"Unsupported kind: {body.kind}")
  try:
    return change_request_store.create_change_request(
      session,
      tenant_id=body.tenant_id,
      kind=body.kind,
      proposed_by=body.proposed_by,
      proposal_body=body.proposal_body,
      ai_model_id=body.ai_model_id,
    )
  except Exception as exc:  # noqa: BLE001 — HTTP 映射
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/v1/registry/change-requests")
def list_change_requests(
  session: Session = Depends(get_db_session),
  tenant_id: str | None = None,
  status: str | None = None,
) -> list[dict[str, Any]]:
  """列出变更请求。"""
  return change_request_store.list_change_requests(
    session,
    tenant_id=tenant_id,
    status=status,
  )


@router.get("/v1/registry/change-requests/{request_id}")
def get_change_request(
  request_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """单条变更请求。"""
  row = change_request_store.get_change_request(session, request_id=request_id)
  if row is None:
    raise HTTPException(status_code=404, detail="Change request not found")
  return row


@router.post("/v1/registry/change-requests/{request_id}/approve")
def approve_change_request(
  request_id: str,
  body: ChangeRequestDecision,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """人审批准并应用 Registry 变更。"""
  try:
    return change_request_store.approve_change_request(
      session,
      request_id=request_id,
      approved_by=body.actor_id,
    )
  except ValueError as exc:
    raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/v1/registry/change-requests/{request_id}/reject")
def reject_change_request(
  request_id: str,
  body: ChangeRequestDecision,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """人审拒绝。"""
  try:
    return change_request_store.reject_change_request(
      session,
      request_id=request_id,
      rejected_by=body.actor_id,
      reason=body.reason,
    )
  except ValueError as exc:
    raise HTTPException(status_code=409, detail=str(exc)) from exc
