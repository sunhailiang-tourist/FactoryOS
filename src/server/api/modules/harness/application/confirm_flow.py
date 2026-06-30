"""Harness 确认门编排（W5 Step3 · H-02）。

作用：plan → audit → execution；import 边界下编排位于 API 层。
业务关联：R-11 确认门 · H-02 confirm→execute。
上游：POST /v1/harness/confirm controller
下游：agent_orchestrator.get_plan · audit_service · execution_service
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from os_core.agent_orchestrator import get_plan
from os_core.audit_service.store import append_audit_event
from os_core.execution_service import execute
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.common import Actor, ActorChannel
from os_core.shared_contracts.models.dsl import DslPlan
from os_core.shared_contracts.models.execution import ExecuteRequest, ExecutionRecord


def confirm_harness(
  session: Session,
  *,
  plan_id: UUID,
  confirmed: bool,
  user_id: str,
  dry_run: bool = False,
) -> ExecutionRecord | DslPlan:
  """Harness 确认门：confirmed → Rule→Execute；reject → audit only。

  功能：读 plan_store · 写 harness audit · 委托 execution。
  业务含义：未 confirm 不得写 Legacy（R-11）。
  上游：harness HTTP controller
  下游：execution_service.execute
  """
  plan = get_plan(plan_id)
  if plan is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Plan not found: {plan_id}",
      http_status=404,
    )

  actor = Actor(user_id=user_id, role="operator", channel=ActorChannel.API)

  if not confirmed:
    append_audit_event(
      session=session,
      tenant_id=plan.tenant_id,
      event_type=AuditEventType.HARNESS_REJECTED,
      actor=actor,
      plan_id=plan_id,
      graph_id=plan.graph_id,
      graph_version=plan.graph_version,
      payload={"reason": "operator_rejected"},
    )
    session.commit()
    return plan

  append_audit_event(
    session=session,
    tenant_id=plan.tenant_id,
    event_type=AuditEventType.HARNESS_CONFIRMED,
    actor=actor,
    plan_id=plan_id,
    graph_id=plan.graph_id,
    graph_version=plan.graph_version,
    payload={"dry_run": dry_run, "step_count": len(plan.steps)},
  )

  step = plan.steps[0]
  record = execute(
    session,
    ExecuteRequest(
      tenant_id=plan.tenant_id,
      graph_id=plan.graph_id,
      graph_version=plan.graph_version,
      verb=step.verb,
      params=dict(step.params),
      actor=actor,
      ruleset_id=plan.ruleset_id,
      scope_id=plan.scope_id,
      idempotency_key=step.idempotency_key,
      dry_run=dry_run,
    ),
  )
  session.commit()
  return record
