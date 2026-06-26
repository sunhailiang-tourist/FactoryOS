"""rulesets 持久化。

作用：RuleSet JSON 落库与查询。
业务关联：R-01～R-05。
上游：rule_engine.service
下游：rulesets 表（Alembic 003）
"""
from __future__ import annotations

import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.shared_contracts.models.rule import RuleSet


def _row_to_ruleset(row: dict) -> RuleSet:
  """body_json → RuleSet。"""
  return RuleSet.model_validate(json.loads(row["body_json"]))


def insert_ruleset(session: Session, ruleset: RuleSet) -> None:
  """INSERT rulesets。"""
  body = ruleset.model_dump(mode="json")
  session.execute(
    text(
      """
      INSERT INTO rulesets (ruleset_id, graph_id, graph_version, status, body_json)
      VALUES (:ruleset_id, :graph_id, :graph_version, :status, :body_json)
      """
    ),
    {
      "ruleset_id": ruleset.id,
      "graph_id": ruleset.graph_id,
      "graph_version": ruleset.graph_version,
      "status": ruleset.status.value,
      "body_json": json.dumps(body, ensure_ascii=False),
    },
  )


def update_ruleset(session: Session, ruleset: RuleSet) -> None:
  """UPDATE rulesets。"""
  body = ruleset.model_dump(mode="json")
  session.execute(
    text(
      """
      UPDATE rulesets
      SET graph_id = :graph_id,
          graph_version = :graph_version,
          status = :status,
          body_json = :body_json
      WHERE ruleset_id = :ruleset_id
      """
    ),
    {
      "ruleset_id": ruleset.id,
      "graph_id": ruleset.graph_id,
      "graph_version": ruleset.graph_version,
      "status": ruleset.status.value,
      "body_json": json.dumps(body, ensure_ascii=False),
    },
  )


def get_ruleset(session: Session, ruleset_id: str) -> RuleSet | None:
  """按 ID 查 RuleSet。"""
  row = (
    session.execute(
      text("SELECT body_json FROM rulesets WHERE ruleset_id = :id LIMIT 1"),
      {"id": ruleset_id},
    )
    .mappings()
    .first()
  )
  if row is None:
    return None
  return _row_to_ruleset(dict(row))


def list_rulesets(
  session: Session,
  *,
  tenant_id: str | None = None,
  graph_id: str | None = None,
) -> list[RuleSet]:
  """列出 RuleSet（可选 graph_id 过滤）。"""
  clauses = ["1=1"]
  params: dict[str, object] = {}
  if graph_id is not None:
    clauses.append("graph_id = :graph_id")
    params["graph_id"] = graph_id
  where = " AND ".join(clauses)
  rows = (
    session.execute(
      text(f"SELECT body_json FROM rulesets WHERE {where} ORDER BY ruleset_id"),
      params,
    )
    .mappings()
    .all()
  )
  _ = tenant_id  # W3 表未存 tenant；HTTP 层过滤预留
  return [_row_to_ruleset(dict(r)) for r in rows]


def has_frozen_ruleset(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
) -> bool:
  """同 graph 版本是否存在 frozen RuleSet。"""
  return find_frozen_ruleset_id(session, graph_id=graph_id, graph_version=graph_version) is not None


def find_frozen_ruleset_id(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
) -> str | None:
  """返回首个 frozen RuleSet ID（execute 默认 ruleset）。"""
  row = (
    session.execute(
      text(
        """
        SELECT ruleset_id FROM rulesets
        WHERE graph_id = :graph_id
          AND graph_version = :graph_version
          AND status = 'frozen'
        ORDER BY ruleset_id
        LIMIT 1
        """
      ),
      {"graph_id": graph_id, "graph_version": graph_version},
    )
    .mappings()
    .first()
  )
  if row is None:
    return None
  return str(row["ruleset_id"])
