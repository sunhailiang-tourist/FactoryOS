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
  """INSERT rulesets。

  功能：将 RuleSet JSON 写入 rulesets 表。
  业务含义：R-01 create_ruleset 数据面落库。
  参数 ruleset：待插入 RuleSet 模型。
  """
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
  """UPDATE rulesets。

  功能：按 ruleset_id 更新 graph 绑定与 body_json。
  业务含义：R-02 编辑 draft 与 R-04 freeze 共用。
  参数 ruleset：含最新字段的 RuleSet。
  """
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
  """按 ID 查 RuleSet。

  功能：SELECT body_json 并反序列化为 RuleSet。
  业务含义：service 层读路径唯一 store 入口。
  参数 ruleset_id：RuleSet 主键。
  返回：RuleSet 或 None。
  """
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
  """列出 RuleSet（可选 graph_id 过滤）。

  功能：按 graph_id 过滤并排序返回。
  业务含义：Studio/管理端枚举 Graph 绑定 RuleSet。
  参数 graph_id：可选过滤键；tenant_id 预留（表未存）。
  返回：RuleSet 列表。
  """
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


def list_rulesets_for_graph_ids(
  session: Session,
  *,
  graph_ids: list[str],
) -> list[RuleSet]:
  """按 graph_id 列表导出 RuleSet（package export 用）。

  功能：聚合 export 快照 rulesets[]。
  业务含义：仅含与导出 Graph 绑定的 RuleSet。
  参数 graph_ids：已导出 Graph 的 id 列表；空则返回空列表。
  """
  if not graph_ids:
    return []
  placeholders = ", ".join(f":gid_{i}" for i in range(len(graph_ids)))
  params = {f"gid_{i}": gid for i, gid in enumerate(graph_ids)}
  rows = (
    session.execute(
      text(
        f"""
        SELECT body_json FROM rulesets
        WHERE graph_id IN ({placeholders})
        ORDER BY ruleset_id
        """
      ),
      params,
    )
    .mappings()
    .all()
  )
  return [_row_to_ruleset(dict(r)) for r in rows]


def has_frozen_ruleset(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
) -> bool:
  """同 graph 版本是否存在 frozen RuleSet。

  功能：委托 find_frozen_ruleset_id 判空。
  业务含义：graph freeze 与 execute 前置校验。
  参数 graph_id/graph_version：Graph 定位键。
  返回：存在 frozen RuleSet 则 True。
  """
  return find_frozen_ruleset_id(session, graph_id=graph_id, graph_version=graph_version) is not None


def find_frozen_ruleset_id(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
) -> str | None:
  """返回首个 frozen RuleSet ID（execute 默认 ruleset）。

  功能：查 rulesets 表首个 frozen 行 ruleset_id。
  业务含义：execution 默认绑定同版本 frozen RuleSet。
  参数 graph_id/graph_version：Graph 定位键。
  返回：ruleset_id 或 None。
  """
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
