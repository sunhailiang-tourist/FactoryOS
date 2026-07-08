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
  """读取 pack_registry.body 原文。

  功能：按 pack_id 查 pack_registry 表 body 列。
  业务含义：Blueprint YAML 文本真源；load_blueprint 底层依赖。
  参数 pack_id：Connector Pack 主键（conn-*）。
  返回：YAML 文本或 None。
  """
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
  """读取 pack_registry.registry_key。

  功能：按 pack_id 查 registry_key 列。
  业务含义：package export 写入 connector_configs 路径键。
  参数 pack_id：Connector Pack 主键。
  返回：registry_key 字符串或 None。
  """
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
  """解析 Blueprint YAML 为 dict。

  功能：get_pack_body_text + yaml.safe_load。
  业务含义：connector_sdk.registry 加载 Blueprint 的 DB 优先路径。
  参数 pack_id：Connector Pack 主键。
  返回：Blueprint dict 或 None。
  """
  body = get_pack_body_text(session, pack_id=pack_id)
  if not body:
    return None
  data = yaml.safe_load(body)
  return data if isinstance(data, dict) else None
