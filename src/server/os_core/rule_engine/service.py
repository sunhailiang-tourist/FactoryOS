"""rule_engine 业务编排（RuleSet CRUD · freeze · evaluate）。

作用：L2 写前授权；默认 deny。
业务关联：R-01～R-05 · execution 门禁。
上游：server.api.modules.rulesets.controllers · execution_service
下游：rulesets · audit_service
"""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from os_core.audit_service.store import append_audit_event
from os_core.rule_engine.evaluate import evaluate_ruleset
from os_core.rule_engine.store import get_ruleset, insert_ruleset, list_rulesets, update_ruleset
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.common import Actor, ActorChannel
from os_core.shared_contracts.models.rule import RuleEffect, RuleSet, RuleSetStatus


def _now() -> datetime:
  return datetime.now(UTC)


def create_ruleset(session: Session, ruleset: RuleSet) -> RuleSet:
  """创建 draft RuleSet。"""
  if get_ruleset(session, ruleset.id) is not None:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      f"RuleSet {ruleset.id} already exists",
      http_status=409,
    )
  now = _now()
  meta = ruleset.metadata.model_copy(update={"created_at": now, "updated_at": now})
  created = ruleset.model_copy(update={"status": RuleSetStatus.DRAFT, "metadata": meta})
  insert_ruleset(session, created)
  return created


def get_ruleset_by_id(session: Session, ruleset_id: str) -> RuleSet | None:
  """GET /v1/rulesets/{id}。"""
  return get_ruleset(session, ruleset_id)


def list_rulesets_for_tenant(
  session: Session,
  *,
  tenant_id: str,
  graph_id: str | None = None,
) -> list[RuleSet]:
  """GET /v1/rulesets 列表。"""
  _ = tenant_id
  return list_rulesets(session, graph_id=graph_id)


def update_ruleset_draft(
  session: Session,
  *,
  ruleset_id: str,
  body: RuleSet,
) -> RuleSet:
  """更新 draft RuleSet；frozen 409（R-05）。"""
  existing = get_ruleset(session, ruleset_id)
  if existing is None:
    raise PlatformError(ErrorCode.RULE_DENIED, f"RuleSet {ruleset_id} not found", http_status=404)
  if existing.status == RuleSetStatus.FROZEN:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "RuleSet is frozen and cannot be modified",
      http_status=409,
    )
  now = _now()
  meta = body.metadata.model_copy(
    update={"created_at": existing.metadata.created_at, "updated_at": now}
  )
  updated = body.model_copy(
    update={"id": ruleset_id, "status": existing.status, "metadata": meta}
  )
  update_ruleset(session, updated)
  return updated


def freeze_ruleset(
  session: Session,
  *,
  ruleset_id: str,
  frozen_by: str = "system",
) -> RuleSet:
  """draft → frozen（R-05 负向：已 frozen 再 PUT 在 update 拦截）。"""
  ruleset = get_ruleset(session, ruleset_id)
  if ruleset is None:
    raise PlatformError(ErrorCode.RULE_DENIED, f"RuleSet {ruleset_id} not found", http_status=404)
  if ruleset.status != RuleSetStatus.DRAFT:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      f"RuleSet must be draft to freeze, got {ruleset.status.value}",
      http_status=409,
    )
  now = _now()
  meta = ruleset.metadata.model_copy(
    update={"updated_at": now, "frozen_at": now, "frozen_by": frozen_by}
  )
  frozen = ruleset.model_copy(update={"status": RuleSetStatus.FROZEN, "metadata": meta})
  update_ruleset(session, frozen)
  append_audit_event(
    session=session,
    tenant_id="platform",
    event_type=AuditEventType.RULESET_FROZEN,
    actor=Actor(user_id=frozen_by, role="system", channel=ActorChannel.API),
    graph_id=ruleset.graph_id,
    graph_version=ruleset.graph_version,
    payload={"ruleset_id": ruleset.id},
  )
  return frozen


def evaluate(
  session: Session,
  *,
  ruleset_id: str,
  graph_id: str,
  graph_version: str,
  verb: str,
  actor: Actor,
) -> dict[str, str | None]:
  """POST evaluate + execution 内嵌调用（R-01～R-03 · R-04）。

  graph_id/version 须与 RuleSet 绑定一致，否则 422。
  """
  ruleset = get_ruleset(session, ruleset_id)
  if ruleset is None:
    raise PlatformError(ErrorCode.RULE_DENIED, f"RuleSet {ruleset_id} not found", http_status=404)
  if ruleset.graph_id != graph_id or ruleset.graph_version != graph_version:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "RuleSet graph_version mismatch",
      http_status=422,
    )
  effect, matched = evaluate_ruleset(ruleset, verb=verb, actor=actor)
  return {"effect": effect.value, "matched_rule_id": matched}


def assert_allowed_for_execute(
  session: Session,
  *,
  ruleset_id: str,
  graph_id: str,
  graph_version: str,
  verb: str,
  actor: Actor,
) -> dict[str, str | None]:
  """execution 门禁：deny → 403 RULE_DENIED。"""
  result = evaluate(
    session,
    ruleset_id=ruleset_id,
    graph_id=graph_id,
    graph_version=graph_version,
    verb=verb,
    actor=actor,
  )
  if result["effect"] != RuleEffect.ALLOW.value:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "Rule evaluation denied",
      http_status=403,
    )
  return result
