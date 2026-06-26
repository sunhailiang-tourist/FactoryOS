"""Rule 域 HTTP 路由（OpenAPI /v1/rulesets/*）。

作用：薄路由；委托 rule_engine。
业务关联：R-01～R-05。
上游：modules/*/routers
下游：os_core.rule_engine
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.rule_engine import (
  create_ruleset,
  evaluate,
  freeze_ruleset,
  get_ruleset_by_id,
  list_rulesets_for_tenant,
  update_ruleset_draft,
)
from os_core.shared_contracts.models.common import Actor
from os_core.shared_contracts.models.rule import RuleSet

router = APIRouter(tags=["Rule"])


class RuleEvaluateBody(BaseModel):
  """POST /v1/rulesets/{id}/evaluate 请求体。"""

  model_config = ConfigDict(extra="forbid")

  graph_id: str = Field(description="图谱 ID")
  graph_version: str = Field(description="图谱版本")
  verb: str = Field(description="DSL 动词")
  actor: Actor = Field(description="操作者")


@router.get("/v1/rulesets")
def list_rulesets_http(
  tenant_id: str = Query(...),
  graph_id: str | None = Query(default=None),
  session: Session = Depends(get_db_session),
) -> list[dict[str, Any]]:
  """GET /v1/rulesets。"""
  items = list_rulesets_for_tenant(session, tenant_id=tenant_id, graph_id=graph_id)
  return [r.model_dump(mode="json") for r in items]


@router.post("/v1/rulesets", status_code=201)
def create_ruleset_http(
  body: RuleSet,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST 创建 draft RuleSet。"""
  ruleset = create_ruleset(session, body)
  session.commit()
  return ruleset.model_dump(mode="json")


@router.get("/v1/rulesets/{ruleset_id}")
def get_ruleset_http(
  ruleset_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET 单条 RuleSet。"""
  ruleset = get_ruleset_by_id(session, ruleset_id)
  if ruleset is None:
    from os_core.shared_contracts.errors import ErrorCode
    from os_core.shared_contracts.exceptions import PlatformError

    raise PlatformError(ErrorCode.RULE_DENIED, f"RuleSet {ruleset_id} not found", http_status=404)
  return ruleset.model_dump(mode="json")


@router.put("/v1/rulesets/{ruleset_id}")
def update_ruleset_http(
  ruleset_id: str,
  body: RuleSet,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """PUT 更新 draft（R-05 负向：frozen 409）。"""
  ruleset = update_ruleset_draft(session, ruleset_id=ruleset_id, body=body)
  session.commit()
  return ruleset.model_dump(mode="json")


@router.post("/v1/rulesets/{ruleset_id}/freeze")
def freeze_ruleset_http(
  ruleset_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST freeze RuleSet。"""
  ruleset = freeze_ruleset(session, ruleset_id=ruleset_id)
  session.commit()
  return ruleset.model_dump(mode="json")


@router.post("/v1/rulesets/{ruleset_id}/evaluate")
def evaluate_rules_http(
  ruleset_id: str,
  body: RuleEvaluateBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST evaluate（R-01/R-02/R-03）。"""
  return evaluate(
    session,
    ruleset_id=ruleset_id,
    graph_id=body.graph_id,
    graph_version=body.graph_version,
    verb=body.verb,
    actor=body.actor,
  )
