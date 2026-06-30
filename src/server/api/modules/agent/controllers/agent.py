"""Agent 域 HTTP 路由（OpenAPI POST /v1/agent/plan）。

作用：薄路由；Graph/Rule 门禁后委托 agent_orchestrator.create_plan。
业务关联：H-01 感知→计划（仅 plan · 不写 Legacy）。
上游：modules/*/routers
下游：graph_service · rule_engine · agent_orchestrator
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.agent_orchestrator import create_plan
from os_core.graph_service import assert_graph_executable
from os_core.rule_engine.store import find_frozen_ruleset_id
from os_core.shared_contracts.cmv_registry import require_known_verb
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

_AGENT_STUB_VERB = "GOVERNED_WRITE"

router = APIRouter(tags=["Agent"])


class AgentPlanBody(BaseModel):
  """POST /v1/agent/plan 请求体（OpenAPI v1.1）。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  graph_id: str = Field(description="目标图谱 ID")
  graph_version: str = Field(description="目标图谱版本 vX.Y.Z")
  intent: str = Field(description="自然语言或结构化意图")
  context: dict[str, Any] | None = Field(default=None, description="可选上下文（W5 stub 未用）")


@router.post("/v1/agent/plan")
def agent_plan_http(
  body: AgentPlanBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/agent/plan（H-01 · 仅产 DslPlan）。"""
  verb_meta = require_known_verb(_AGENT_STUB_VERB)
  verb_level = str(verb_meta["level"])

  graph = assert_graph_executable(
    session,
    graph_id=body.graph_id,
    graph_version=body.graph_version,
    verb=_AGENT_STUB_VERB,
    verb_level=verb_level,
  )

  ruleset_id = find_frozen_ruleset_id(
    session,
    graph_id=body.graph_id,
    graph_version=body.graph_version,
  )
  if ruleset_id is None:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "No frozen RuleSet bound to this graph version",
      http_status=403,
    )

  plan = create_plan(
    tenant_id=body.tenant_id,
    graph_id=body.graph_id,
    graph_version=body.graph_version,
    intent=body.intent,
    ruleset_id=ruleset_id,
    allowed_dsl=graph.allowed_dsl or None,
  )
  return plan.model_dump(mode="json")
