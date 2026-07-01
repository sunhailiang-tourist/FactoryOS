"""Pack Registry 只读访问（pack_registry · Connector Blueprint）。

作用：从 DB 加载 Blueprint YAML 文本/对象。
业务关联：B-01 Blueprint 加载 · W4 connector runtime。
上游：Studio publish · bootstrap seed
下游：connector_sdk.registry
"""
from __future__ import annotations

from typing import Any

import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session


def get_pack_body_text(session: Session, *, pack_id: str) -> str | None:
  """pack_registry.body 原文。"""
  row = (
    session.execute(
      text("SELECT body FROM pack_registry WHERE pack_id = :pack_id LIMIT 1"),
      {"pack_id": pack_id},
    )
    .mappings()
    .first()
  )
  return str(row["body"]) if row else None


def get_pack_registry_key(session: Session, *, pack_id: str) -> str | None:
  """pack_registry.registry_key（export connector_configs 用）。"""
  row = (
    session.execute(
      text(
        "SELECT registry_key FROM pack_registry WHERE pack_id = :pack_id LIMIT 1"
      ),
      {"pack_id": pack_id},
    )
    .mappings()
    .first()
  )
  return str(row["registry_key"]) if row else None


def get_pack_blueprint(session: Session, *, pack_id: str) -> dict[str, Any] | None:
  """解析 Blueprint YAML 为 dict。"""
  body = get_pack_body_text(session, pack_id=pack_id)
  if not body:
    return None
  data = yaml.safe_load(body)
  return data if isinstance(data, dict) else None
