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
  """重置 mock Legacy 写次数。

  功能：将全局 _write_count 归零。
  业务含义：测试前置；隔离 E-06/E-07 写计数断言。
  上游：pytest fixture · 测试用例 setUp。
  """
  global _write_count
  _write_count = 0


def reset_entity_store() -> None:
  """重置 mock Legacy 实体表。

  功能：清空全局 _entity_store。
  业务含义：W4 runtime 测试前置；避免跨用例实体污染。
  上游：pytest fixture · runtime 测试 setUp。
  """
  global _entity_store
  _entity_store = {}


def get_write_count() -> int:
  """返回 mock Legacy 累计写次数。

  功能：读取全局 _write_count。
  业务含义：E-06 dry_run 与 E-07 非 dry_run 写计数验收。
  返回：累计写次数整数。
  """
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
  """读取 Legacy 实体 snapshot（C-02 · entity.get mock）。

  功能：按 entity_type:entity_id 查内存 store；不存在则建默认。
  业务含义：Runtime entity.get 唯一 mock 后端。
  参数 entity_type/entity_id：Legacy 实体定位键。
  返回：实体 dict 深拷贝。
  """
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
  """更新 Legacy 实体（C-03 · entity.update mock）。

  功能：合并 fields 写入 store 并递增写计数。
  业务含义：GOVERNED_WRITE 路径产出 legacy_refs 与 snapshots。
  参数 fields：待合并字段；pack_id/verb：写审计上下文。
  返回：含 legacy_refs · before/after_snapshot 的 dict。
  """
  # 业务：读取 before 快照、合并 fields 写 store 并返回写审计结构
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
  """模拟 Connector 写 Legacy（非 dry_run 路径）。

  功能：递增全局 _write_count。
  业务含义：E-06/E-07 写计数与 revert 路径共用计数器。
  参数 pack_id/verb：写上下文（当前仅计数，未分支）。
  """
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
  """E-04：将 Legacy 实体恢复为 before_snapshot 字段。

  功能：覆盖 store 中实体 fields 并触发 revert 写计数。
  业务含义：GOVERNED_WRITE revert 补偿路径。
  参数 fields：恢复目标字段快照。
  """
  key = _entity_key(entity_type=entity_type, entity_id=entity_id)
  if key not in _entity_store:
    _entity_store[key] = _default_entity(entity_type=entity_type, entity_id=entity_id)
  _entity_store[key]["fields"] = dict(fields)
  mock_legacy_write(pack_id=pack_id, verb="GOVERNED_WRITE_REVERT")


def get_entity_snapshot(*, entity_type: str, entity_id: str) -> dict:
  """E-04 revert 读回 alias（同 get_entity）。

  功能：委托 get_entity 返回当前实体快照。
  业务含义：revert 后验收读回与 C-02 共用语义。
  参数 entity_type/entity_id：Legacy 实体定位键。
  返回：实体 dict。
  """
  return get_entity(entity_type=entity_type, entity_id=entity_id)
