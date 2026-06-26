"""Contract Registry 只读访问（contract_sets / contract_artifacts）。

作用：published contract_set 与 artifact body 查询。
业务关联：cmv_registry · schema_loader · gate L0 对账。
上游：bootstrap publish · Studio API
下游：shared_contracts loaders
"""
from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

_ACTIVE_SET = "factoryos-v1"


def is_seeded(session: Session) -> bool:
  """Registry 是否已 bootstrap（contract_sets 含 factoryos-v1）。"""
  row = session.execute(
    text("SELECT set_id FROM contract_sets WHERE set_id = :set_id LIMIT 1"),
    {"set_id": _ACTIVE_SET},
  ).first()
  return row is not None


def get_active_set_id(session: Session, *, environment: str = "prod") -> str | None:
  """查环境绑定的 published contract_set。"""
  row = (
    session.execute(
      text(
        """
    SELECT set_id FROM contract_environment_bindings
    WHERE environment = :environment AND active = 1
    ORDER BY binding_id LIMIT 1
    """
      ),
      {"environment": environment},
    )
    .mappings()
    .first()
  )
  return str(row["set_id"]) if row else None


def get_artifact_body(
  session: Session,
  *,
  set_id: str,
  kind: str,
  artifact_key: str,
) -> str | None:
  """按 set/kind/key 取 artifact 文本 body。"""
  row = (
    session.execute(
      text(
        """
    SELECT body FROM contract_artifacts
    WHERE set_id = :set_id AND kind = :kind AND artifact_key = :artifact_key
    LIMIT 1
    """
      ),
      {"set_id": set_id, "kind": kind, "artifact_key": artifact_key},
    )
    .mappings()
    .first()
  )
  return str(row["body"]) if row else None


def get_cmv_body(session: Session, *, set_id: str | None = None) -> str | None:
  """CMV 注册表 YAML body。"""
  sid = set_id or _ACTIVE_SET
  return get_artifact_body(session, set_id=sid, kind="cmv", artifact_key="cmv/CMV注册表.yaml")


def get_schema_body(
  session: Session,
  *,
  filename: str,
  set_id: str | None = None,
) -> str | None:
  """JSON Schema artifact body。"""
  sid = set_id or _ACTIVE_SET
  return get_artifact_body(
    session,
    set_id=sid,
    kind="schema",
    artifact_key=f"schemas/{filename}",
  )


def get_schema_json(
  session: Session,
  *,
  filename: str,
  set_id: str | None = None,
) -> dict[str, Any] | None:
  """JSON Schema 解析为 dict。"""
  body = get_schema_body(session, filename=filename, set_id=set_id)
  if not body:
    return None
  data = json.loads(body)
  return data if isinstance(data, dict) else None
