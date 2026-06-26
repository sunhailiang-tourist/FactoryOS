"""Legacy mock 实体存储与写计数（W2 E-06/E-07 · W4 C-02～C-04）。

作用：模拟 Legacy entity.get/update；非 dry_run 递增写计数。
业务关联：Runtime 唯一 mock 后端；真实 httpx 留 Path A。
上游：connector_sdk.runtime
下游：integration 测试 E-06/07 · C-02～C-04
关联文档：contracts/acceptance C-02～C-04
"""
from __future__ import annotations

import copy
from typing import Any

_write_count: int = 0
_entity_store: dict[str, dict[str, Any]] = {}


def reset_write_count() -> None:
  """重置 mock Legacy 写次数（测试前置）。"""
  global _write_count
  _write_count = 0


def reset_entity_store() -> None:
  """重置 mock Legacy 实体表（W4 runtime 测试前置）。"""
  global _entity_store
  _entity_store = {}


def get_write_count() -> int:
  """返回 mock Legacy 累计写次数。"""
  return _write_count


def _entity_key(*, entity_type: str, entity_id: str) -> str:
  return f"{entity_type}:{entity_id}"


def _default_entity(*, entity_type: str, entity_id: str) -> dict[str, Any]:
  return {
    "entity_type": entity_type,
    "entity_id": entity_id,
    "fields": {"status": "open", "completed_qty": 0},
  }


def get_entity(*, entity_type: str, entity_id: str) -> dict[str, Any]:
  """读取 Legacy 实体 snapshot（C-02 · entity.get mock）。"""
  key = _entity_key(entity_type=entity_type, entity_id=entity_id)
  if key not in _entity_store:
    _entity_store[key] = _default_entity(entity_type=entity_type, entity_id=entity_id)
  return copy.deepcopy(_entity_store[key])


def update_entity(
  *,
  entity_type: str,
  entity_id: str,
  fields: dict[str, Any],
  pack_id: str,
  verb: str,
) -> dict[str, Any]:
  """更新 Legacy 实体（C-03 · entity.update mock）。"""
  before = get_entity(entity_type=entity_type, entity_id=entity_id)
  before_snapshot = {
    "entity_type": entity_type,
    "entity_id": entity_id,
    "fields": dict(before.get("fields") or {}),
  }
  key = _entity_key(entity_type=entity_type, entity_id=entity_id)
  stored = _entity_store[key]
  merged = {**(stored.get("fields") or {}), **fields}
  stored["fields"] = merged
  after_snapshot = {
    "entity_type": entity_type,
    "entity_id": entity_id,
    "fields": dict(merged),
  }
  mock_legacy_write(pack_id=pack_id, verb=verb)
  legacy_id = f"{entity_type}/{entity_id}"
  return {
    "legacy_refs": {
      "legacy_id": legacy_id,
      "entity_type": entity_type,
      "entity_id": entity_id,
    },
    "before_snapshot": before_snapshot,
    "after_snapshot": after_snapshot,
  }


def mock_legacy_write(*, pack_id: str, verb: str) -> None:
  """模拟 Connector 写 Legacy（非 dry_run 路径）。"""
  global _write_count
  _ = pack_id, verb
  _write_count += 1


def restore_entity(
  *,
  entity_type: str,
  entity_id: str,
  fields: dict[str, Any],
  pack_id: str = "conn-mock",
) -> None:
  """E-04：将 Legacy 实体恢复为 before_snapshot 字段。"""
  key = _entity_key(entity_type=entity_type, entity_id=entity_id)
  if key not in _entity_store:
    _entity_store[key] = _default_entity(entity_type=entity_type, entity_id=entity_id)
  _entity_store[key]["fields"] = dict(fields)
  mock_legacy_write(pack_id=pack_id, verb="GOVERNED_WRITE_REVERT")


def get_entity_snapshot(*, entity_type: str, entity_id: str) -> dict:
  """E-04 revert 读回 alias（同 get_entity）。"""
  return get_entity(entity_type=entity_type, entity_id=entity_id)
