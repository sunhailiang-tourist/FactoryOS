"""Tenant 配置 Registry（tenant_profiles · system_relations · overrides）。

作用：租户级配置与系统关系只读/写入（Studio 主路径）。
业务关联：配置枢纽 Layer B · connector_instances 激活。
上游：Studio · import/export
下游：connector runtime · execution gates
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_tenant_profile(session: Session, *, tenant_id: str) -> dict[str, Any] | None:
  """tenant_profiles 单行。"""
  row = (
    session.execute(
      text(
        """
        SELECT tenant_id, display_name, path, shadow_mode, write_approved, profile_json
        FROM tenant_profiles WHERE tenant_id = :tenant_id LIMIT 1
        """
      ),
      {"tenant_id": tenant_id},
    )
    .mappings()
    .first()
  )
  return dict(row) if row else None


def list_system_relations(session: Session, *, tenant_id: str) -> list[dict[str, Any]]:
  """租户 system_relations 列表。"""
  rows = session.execute(
    text(
      """
      SELECT relation_id, tenant_id, pack_id, environment, path, body, lifecycle
      FROM system_relations WHERE tenant_id = :tenant_id
      """
    ),
    {"tenant_id": tenant_id},
  ).mappings()
  return [dict(r) for r in rows]
