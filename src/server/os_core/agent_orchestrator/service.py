"""agent_orchestrator 薄 stub：意图 → DslPlan（无 LLM · 无写 Legacy）。

作用：W5 Step1 内核 create_plan；固定 CMV 动词映射。
业务关联：H-01 计划阶段 · REDLINES R01/R11。
上游：server.api agent 路由（Step2）— **Graph/Rule 门禁在 API 层**
下游：plan_store · harness.confirm（Step3）
关联文档：contracts/schemas/DslPlan.schema.json · ADR-002 · os_core-public-api
"""
from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from os_core.agent_orchestrator.plan_store import save_plan
from os_core.shared_contracts.cmv_registry import require_known_verb
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.dsl import DslPlan, DslPlanSource, PlanStep

_PLAN_TTL = timedelta(hours=1)
_VERB_STUB = "GOVERNED_WRITE"
_WO_PATTERN = re.compile(r"\bwo[-\w]+\b", re.IGNORECASE)


def _now() -> datetime:
  return datetime.now(UTC)


def _parse_work_order_id(intent: str) -> str:
  """从自然语言 intent 提取工单号 stub（无 LLM）。"""
  match = _WO_PATTERN.search(intent)
  if match:
    return match.group(0)
  return "wo-stub-default"


def _parse_quantity(intent: str) -> int:
  """提取数量 stub；默认 1。"""
  match = re.search(r"\bqty\s+(\d+)\b", intent, re.IGNORECASE)
  if match:
    return int(match.group(1))
  match = re.search(r"\bcompleted\s+(\d+)\b", intent, re.IGNORECASE)
  if match:
    return int(match.group(1))
  return 1


def create_plan(
  *,
  tenant_id: str,
  graph_id: str,
  graph_version: str,
  intent: str,
  ruleset_id: str | None = None,
  allowed_dsl: list[str] | None = None,
  source: DslPlanSource = DslPlanSource.AGENT,
  verb: str | None = None,
  trace_id: str | None = None,
) -> DslPlan:
  """产出 DSL 计划（不执行 · 不写 Legacy · 不 import graph/rule 内核）。

  功能：intent → 单步 GOVERNED_WRITE DslPlan；
  Graph frozen / Rule 绑定由 **调用方**（API/harness）预先校验。
  业务含义：Harness 确认门的数据载体；确认前 execution 不得被调用。
  上游：POST /v1/agent/plan 薄路由（Step2）
  下游：plan_store.save_plan
  参数 ruleset_id/allowed_dsl：由 API 层注入（graph_service + rule_engine 查询结果）。
  参数 source：MCP gateway 传 DslPlanSource.MCP。
  参数 verb：tools/call 的 CMV 名；默认 GOVERNED_WRITE。
  参数 trace_id：MCP SEP-414 解析结果；非 MCP 通道为 None。
  """
  verb_to_use = verb or _VERB_STUB
  require_known_verb(verb_to_use)
  if allowed_dsl is not None and verb_to_use not in allowed_dsl:
    raise PlatformError(
      ErrorCode.DSL_NOT_IN_GRAPH,
      f"Verb {verb_to_use} not in graph allowed_dsl",
      http_status=422,
    )

  work_order_id = _parse_work_order_id(intent)
  quantity = _parse_quantity(intent)
  now = _now()
  plan_id = uuid4()
  idempotency_key = f"plan-{plan_id}-step-0"

  plan = DslPlan(
    plan_id=plan_id,
    tenant_id=tenant_id,
    graph_id=graph_id,
    graph_version=graph_version,
    ruleset_id=ruleset_id,
    steps=[
      PlanStep(
        verb=verb_to_use,
        params={
          "entity": "work_order",
          "work_order_id": work_order_id,
          "quantity": quantity,
        },
        idempotency_key=idempotency_key,
      )
    ],
    source=source,
    created_at=now,
    expires_at=now + _PLAN_TTL,
    summary=f"Agent plan: {work_order_id} qty {quantity}",
    dry_run=False,
    trace_id=trace_id,
  )
  save_plan(plan)
  return plan
