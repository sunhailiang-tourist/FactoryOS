"""Registry 变更请求 HTTP 路由（人审写路径 · ADR-008）。

作用：Studio/AI 提案 → pending → 人审 approve/reject → Registry 落库。
业务关联：R-09 AI 不得自动 publish；须 UI 确认。
上游：Integration Studio
下游：change_request_store
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.platform_registry import change_request_store
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

router = APIRouter(tags=["Registry"])


class ChangeRequestCreate(BaseModel):
  """创建变更请求（提案）。"""

  tenant_id: str | None = Field(default=None, description="可选租户 ID")
  kind: str = Field(description="pack_upsert | system_relation_upsert")
  proposed_by: str = Field(description="提案人 ID")
  proposal_body: dict[str, Any] = Field(description="提案内容体")
  ai_model_id: str | None = Field(default=None, description="可选 AI 模型 ID")


class ChangeRequestDecision(BaseModel):
  """人审决定。"""

  actor_id: str = Field(description="审批人 ID")
  reason: str | None = Field(default=None, description="可选拒绝原因")


@router.post("/v1/registry/change-requests", status_code=201)
def create_change_request(
  body: ChangeRequestCreate,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """提交变更提案（pending，不直接改 Registry）。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Registry 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.platform_registry。
  异常: PlatformError · REG_* / VAL_SCHEMA_FAILED 等
  """
  if body.kind not in ("pack_upsert", "system_relation_upsert"):
    raise PlatformError(
      ErrorCode.REG_UNSUPPORTED_KIND,
      f"Unsupported kind: {body.kind}",
      http_status=422,
    )
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
    raise PlatformError(
      ErrorCode.VAL_SCHEMA_FAILED,
      str(exc),
      http_status=422,
    ) from exc


@router.get("/v1/registry/change-requests")
def list_change_requests(
  session: Session = Depends(get_db_session),
  tenant_id: str | None = None,
  status: str | None = None,
) -> list[dict[str, Any]]:
  """列出变更请求。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Registry 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.platform_registry。
  异常: PlatformError · REG_* / VAL_SCHEMA_FAILED 等
  """
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
  """单条变更请求。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Registry 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.platform_registry。
  异常: PlatformError · REG_* / VAL_SCHEMA_FAILED 等
  """
  row = change_request_store.get_change_request(session, request_id=request_id)
  if row is None:
    raise PlatformError(
      ErrorCode.REG_CHANGE_NOT_FOUND,
      "Change request not found",
      http_status=404,
    )
  return row


@router.post("/v1/registry/change-requests/{request_id}/approve")
def approve_change_request(
  request_id: str,
  body: ChangeRequestDecision,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """人审批准并应用 Registry 变更。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Registry 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.platform_registry。
  异常: PlatformError · REG_* / VAL_SCHEMA_FAILED 等
  """
  try:
    return change_request_store.approve_change_request(
      session,
      request_id=request_id,
      approved_by=body.actor_id,
    )
  except ValueError as exc:
    raise PlatformError(
      ErrorCode.REG_CHANGE_REJECTED,
      str(exc),
      http_status=409,
    ) from exc


@router.post("/v1/registry/change-requests/{request_id}/reject")
def reject_change_request(
  request_id: str,
  body: ChangeRequestDecision,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """人审拒绝。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Registry 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.platform_registry。
  异常: PlatformError · REG_* / VAL_SCHEMA_FAILED 等
  """
  try:
    return change_request_store.reject_change_request(
      session,
      request_id=request_id,
      rejected_by=body.actor_id,
      reason=body.reason,
    )
  except ValueError as exc:
    raise PlatformError(
      ErrorCode.REG_CHANGE_REJECTED,
      str(exc),
      http_status=409,
    ) from exc
