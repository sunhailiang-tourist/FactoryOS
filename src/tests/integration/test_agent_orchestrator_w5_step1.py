"""W5 Step1：agent_orchestrator 内核 stub · create_plan（workflow 门禁）。

业务：LangGraph 薄 stub 产出 DslPlan；不调用 LiteLLM · 不写 Legacy。
上游：plan Step1 · os_core.agent_orchestrator
下游：gate step --step 1 -k 'workflow'
"""
from __future__ import annotations

import importlib

import pytest
from sqlalchemy.orm import Session
from tests.integration.w3_helpers import seed_frozen_env_kernel

DSL_PLAN_REQUIRED = frozenset({
  "plan_id",
  "tenant_id",
  "graph_id",
  "graph_version",
  "steps",
  "source",
  "created_at",
  "expires_at",
})


def _get_create_plan():
  """导入 W5 Step1 内核 create_plan（未实现时红测）。"""
  module = importlib.import_module("os_core.agent_orchestrator.service")
  fn = getattr(module, "create_plan", None)
  assert fn is not None, "缺少 os_core.agent_orchestrator.service.create_plan"
  return fn


@pytest.fixture
def kernel_w5_env(migrated_db_session: Session) -> dict[str, str]:
  """W5 Step1：frozen graph + ruleset 种子（内核测前置）。"""
  return seed_frozen_env_kernel(
    migrated_db_session,
    graph_id="graph-kernel-w5",
    ruleset_id="ruleset-kernel-w5",
  )


@pytest.mark.integration
@pytest.mark.parametrize("case", ["create_plan"], ids=["workflow"])
def test_w5_step1_create_plan_stub_returns_dsl_plan(
  case: str,
  migrated_db_session: Session,
  kernel_w5_env: dict[str, str],
) -> None:
  """Step1：create_plan 返回合法 DslPlan（steps≥1 · source=agent）。"""
  create_plan = _get_create_plan()
  plan = create_plan(
    tenant_id="default",
    graph_id=kernel_w5_env["graph_id"],
    graph_version=kernel_w5_env["version"],
    intent="report work order wo-kernel-w5 completed qty 1",
    ruleset_id=kernel_w5_env["ruleset_id"],
    allowed_dsl=["QUERY_ENTITY", "GOVERNED_WRITE"],
  )

  if hasattr(plan, "model_dump"):
    body = plan.model_dump(mode="json")
  elif isinstance(plan, dict):
    body = plan
  else:
    pytest.fail(f"create_plan 应返回 DslPlan 或 dict: {type(plan)!r}")

  assert DSL_PLAN_REQUIRED <= set(body.keys()), body
  assert len(body.get("steps") or []) >= 1, body
  assert body.get("source") == "agent", body
  assert body.get("graph_id") == kernel_w5_env["graph_id"]
