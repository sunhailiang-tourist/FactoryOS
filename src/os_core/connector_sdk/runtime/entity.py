"""Runtime entity read/write（W4 Step2 · C-02～C-04）。

作用：薄封装 mock_legacy 实体 API；对齐 Blueprint GOVERNED_WRITE。
业务关联：entity.get / entity.update 验收。
上游：runtime.execute · 测试直接调用
下游：mock_legacy
"""
from __future__ import annotations

from typing import Any

from os_core.connector_sdk import mock_legacy


def entity_get(
  *,
  pack_id: str,
  tenant_id: str,
  entity_type: str,
  entity_id: str,
) -> dict[str, Any]:
  """C-02：读取 entity snapshot。"""
  _ = pack_id, tenant_id
  return mock_legacy.get_entity(entity_type=entity_type, entity_id=entity_id)


def entity_update(
  *,
  pack_id: str,
  tenant_id: str,
  entity_type: str,
  entity_id: str,
  fields: dict[str, Any],
  idempotency_key: str | None = None,
) -> dict[str, Any]:
  """C-03/C-04：更新 entity 并返回 legacy_refs 与 snapshots。"""
  _ = tenant_id, idempotency_key
  return mock_legacy.update_entity(
    entity_type=entity_type,
    entity_id=entity_id,
    fields=fields,
    pack_id=pack_id,
    verb="GOVERNED_WRITE",
  )
