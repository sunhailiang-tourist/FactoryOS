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
from os_core.rule_engine.store import (
  get_ruleset,
  has_frozen_ruleset,
  insert_ruleset,
  list_rulesets,
  update_ruleset,
)
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.common import Actor, ActorChannel
from os_core.shared_contracts.models.graph import BusinessGraph
from os_core.shared_contracts.models.rule import RuleEffect, RuleSet, RuleSetStatus


def _now() -> datetime:
  return datetime.now(UTC)


def create_ruleset(session: Session, ruleset: RuleSet) -> RuleSet:
  """创建 draft RuleSet。

  功能：校验 ID 唯一后写入 rulesets 表。
  业务含义：R-01 RuleSet 生命周期起点；Studio 自动建 RuleSet 亦走此路径。
  参数 ruleset：待创建 RuleSet 模型。
  返回：status=draft 的 RuleSet。
  异常：ID 冲突 409。
  """
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
  """按 ID 读取 RuleSet。

  功能：委托 rule_engine.store.get_ruleset。
  业务含义：HTTP GET 与 execution 前置查询共用。
  参数 ruleset_id：RuleSet 主键。
  返回：RuleSet 或 None。
  """
  return get_ruleset(session, ruleset_id)


def list_rulesets_for_tenant(
  session: Session,
  *,
  tenant_id: str,
  graph_id: str | None = None,
) -> list[RuleSet]:
  """列出 RuleSet（可按 graph 过滤）。

  功能：委托 list_rulesets。
  业务含义：Studio/管理端枚举 Graph 绑定 RuleSet。
  参数 graph_id：可选过滤键。
  返回：RuleSet 列表。
  """
  _ = tenant_id
  return list_rulesets(session, graph_id=graph_id)


def update_ruleset_draft(
  session: Session,
  *,
  ruleset_id: str,
  body: RuleSet,
) -> RuleSet:
  """更新 draft RuleSet；frozen 不可改（R-05）。

  功能：合并 body 并保留 created_at。
  业务含义：顾问编辑授权规则；frozen 后只读。
  参数 ruleset_id · body：目标 ID 与更新内容。
  返回：更新后 RuleSet。
  异常：不存在 404 · frozen 409。
  """
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
  """draft → frozen 并写审计（R-05）。

  功能：状态迁移 draft→frozen，记录 RULESET_FROZEN 审计。
  业务含义：Graph freeze 前置；execution 仅认 frozen RuleSet。
  参数 ruleset_id · frozen_by：目标 RuleSet 与操作者。
  返回：frozen RuleSet。
  异常：非 draft 409。
  """
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


def ensure_studio_ruleset_for_graph(
  session: Session,
  *,
  graph: BusinessGraph,
  frozen_by: str = "studio",
) -> None:
  """Studio onboard：无 RuleSet 时自动创建并 freeze（STU-01 六步闭环）。

  功能：按 graph.allowed_dsl 生成 allow integrator/operator 的 draft RuleSet。
  业务含义：顾问零仓库 freeze 前置；graph_service 仅校验 frozen RuleSet 存在。
  上游：graphs freeze_graph_http API 编排。
  下游：create_ruleset · freeze_ruleset · audit_service。
  参数 graph：待绑定 BusinessGraph；frozen_by 默认 studio。
  """
  if has_frozen_ruleset(session, graph_id=graph.id, graph_version=graph.version):
    return
  ruleset_id = f"ruleset-{graph.id}-{graph.version}"[:120]
  if get_ruleset(session, ruleset_id) is None:
    now = _now().isoformat().replace("+00:00", "Z")
    verbs = list(graph.allowed_dsl or ["QUERY_ENTITY", "GOVERNED_WRITE"])
    ruleset = RuleSet.model_validate(
      {
        "id": ruleset_id,
        "graph_id": graph.id,
        "graph_version": graph.version,
        "status": "draft",
        "default_effect": "deny",
        "rules": [
          {
            "id": "rule-studio-allow",
            "effect": "allow",
            "subjects": ["role:operator", "role:integrator"],
            "actions": verbs,
            "priority": 10,
          }
        ],
        "metadata": {"created_at": now, "updated_at": now},
      }
    )
    create_ruleset(session, ruleset)
  ruleset = get_ruleset(session, ruleset_id)
  if ruleset is not None and ruleset.status != RuleSetStatus.FROZEN:
    freeze_ruleset(session, ruleset_id=ruleset_id, frozen_by=frozen_by)


def evaluate(
  session: Session,
  *,
  ruleset_id: str,
  graph_id: str,
  graph_version: str,
  verb: str,
  actor: Actor,
) -> dict[str, str | None]:
  """Rule 授权判定（R-01～R-04）。

  功能：加载 RuleSet 并调用 evaluate_ruleset。
  业务含义：L2 写前默认 deny；ALLOW 方可进入 execution。
  参数 ruleset_id · graph_id/version · verb · actor：判定上下文。
  返回：effect 与 matched_rule_id。
  异常：RuleSet 不存在 404 · graph 版本不一致 422。
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
  """execution 门禁：deny 时抛 RULE_DENIED。

  功能：包装 evaluate，非 ALLOW 则 403。
  业务含义：execution_service 写库前最后一道 Rule 闸。
  参数：同 evaluate。
  返回：ALLOW 时 evaluate 结果。
  异常：deny → PlatformError 403。
  """
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
