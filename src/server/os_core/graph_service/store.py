"""business_graphs 持久化。

作用：BusinessGraph JSON 落库与按 id+version 查询。
业务关联：G-01～G-08 数据面。
上游：graph_service.service
下游：business_graphs 表（Alembic 003）
"""
from __future__ import annotations

import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.shared_contracts.models.graph import BusinessGraph


def _row_to_graph(row: dict) -> BusinessGraph:
  """DB body_json → BusinessGraph。"""
  data = json.loads(row["body_json"])
  return BusinessGraph.model_validate(data)


def insert_graph(session: Session, graph: BusinessGraph) -> None:
  """INSERT business_graphs（新版本行）。"""
  body = graph.model_dump(mode="json", by_alias=True)
  session.execute(
    text(
      """
      INSERT INTO business_graphs (
        graph_id, version, tenant_id, status, checksum, body_json
      ) VALUES (
        :graph_id, :version, :tenant_id, :status, :checksum, :body_json
      )
      """
    ),
    {
      "graph_id": graph.id,
      "version": graph.version,
      "tenant_id": graph.tenant_id,
      "status": graph.status.value,
      "checksum": graph.checksum,
      "body_json": json.dumps(body, ensure_ascii=False),
    },
  )


def update_graph(session: Session, graph: BusinessGraph) -> None:
  """UPDATE 已有 graph_id+version 行。"""
  body = graph.model_dump(mode="json", by_alias=True)
  session.execute(
    text(
      """
      UPDATE business_graphs
      SET tenant_id = :tenant_id,
          status = :status,
          checksum = :checksum,
          body_json = :body_json
      WHERE graph_id = :graph_id AND version = :version
      """
    ),
    {
      "graph_id": graph.id,
      "version": graph.version,
      "tenant_id": graph.tenant_id,
      "status": graph.status.value,
      "checksum": graph.checksum,
      "body_json": json.dumps(body, ensure_ascii=False),
    },
  )


def get_graph(
  session: Session,
  *,
  graph_id: str,
  version: str,
) -> BusinessGraph | None:
  """按 graph_id + version 查单条。"""
  row = (
    session.execute(
      text(
        """
        SELECT body_json FROM business_graphs
        WHERE graph_id = :graph_id AND version = :version
        LIMIT 1
        """
      ),
      {"graph_id": graph_id, "version": version},
    )
    .mappings()
    .first()
  )
  if row is None:
    return None
  return _row_to_graph(dict(row))


def graph_exists(session: Session, *, graph_id: str, version: str) -> bool:
  """版本行是否存在。"""
  return get_graph(session, graph_id=graph_id, version=version) is not None


def list_graphs_by_tenant(session: Session, *, tenant_id: str) -> list[BusinessGraph]:
  """列出租户可见 Graph（含 tenant_id 匹配或 NULL 共享模板）。

  功能：package export 聚合 graphs[]。
  业务含义：export 须含至少一条 frozen/in_review/draft 图谱。
  参数 tenant_id：导出来源租户 ID。
  返回：BusinessGraph 列表（按 graph_id · version 排序）。
  """
  rows = (
    session.execute(
      text(
        """
        SELECT body_json FROM business_graphs
        WHERE tenant_id = :tenant_id OR tenant_id IS NULL
        ORDER BY graph_id, version
        """
      ),
      {"tenant_id": tenant_id},
    )
    .mappings()
    .all()
  )
  return [_row_to_graph(dict(r)) for r in rows]


def has_frozen_ruleset_for_graph(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
) -> bool:
  """同 graph 版本是否存在 frozen RuleSet（G-05 前置；避免 import rule_engine）。"""
  row = (
    session.execute(
      text(
        """
        SELECT 1 FROM rulesets
        WHERE graph_id = :graph_id
          AND graph_version = :graph_version
          AND status = 'frozen'
        LIMIT 1
        """
      ),
      {"graph_id": graph_id, "graph_version": graph_version},
    )
    .first()
  )
  return row is not None
