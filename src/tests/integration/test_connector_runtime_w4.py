"""W4 Step2/4：Connector runtime entity read/write（C-02～C-04）。

业务：mock entity.get / entity.update · write 后 read-back 与 after_snapshot 一致。
上游：connector_sdk.runtime · mock_legacy entity store
下游：gate step --step 2 -k 'C-02'
"""
from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any

import pytest

from os_core.connector_sdk import mock_legacy

MOCK_PACK_ID = "conn-mock"
DEFAULT_TENANT_ID = "default"
ENTITY_TYPE = "work_order"
ENTITY_ID = "wo-w4-c02"


def _import_callable(module_path: str, attr: str) -> Callable[..., Any]:
  mod = importlib.import_module(module_path)
  fn = getattr(mod, attr, None)
  assert fn is not None, f"缺少 {module_path}.{attr}"
  return fn


def _entity_key() -> dict[str, str]:
  return {"entity_type": ENTITY_TYPE, "entity_id": ENTITY_ID}


@pytest.fixture(autouse=True)
def _reset_mock_entity_store() -> None:
  """每用例重置 mock Legacy 实体与写计数。"""
  mock_legacy.reset_write_count()
  reset_store = getattr(mock_legacy, "reset_entity_store", None)
  if reset_store is not None:
    reset_store()


@pytest.mark.integration
@pytest.mark.parametrize("case", ["read"], ids=["C-02"])
def test_C02_read_entity_returns_snapshot(case: str) -> None:
  """C-02：entity.get 返回 snapshot dict。"""
  entity_get = _import_callable("os_core.connector_sdk.runtime.entity", "entity_get")
  snapshot = entity_get(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    entity_type=ENTITY_TYPE,
    entity_id=ENTITY_ID,
  )
  assert isinstance(snapshot, dict), snapshot
  assert snapshot.get("entity_type") == ENTITY_TYPE
  assert snapshot.get("entity_id") == ENTITY_ID
  assert "fields" in snapshot


@pytest.mark.integration
@pytest.mark.parametrize("case", ["write"], ids=["C-03"])
def test_C03_write_entity_populates_legacy_refs(case: str) -> None:
  """C-03：entity.update 写 Legacy，legacy_refs populated。"""
  entity_get = _import_callable("os_core.connector_sdk.runtime.entity", "entity_get")
  entity_update = _import_callable("os_core.connector_sdk.runtime.entity", "entity_update")

  before = entity_get(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    entity_type=ENTITY_TYPE,
    entity_id=ENTITY_ID,
  )
  prev_qty = (before.get("fields") or {}).get("completed_qty", 0)
  update_result = entity_update(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    entity_type=ENTITY_TYPE,
    entity_id=ENTITY_ID,
    fields={"status": "in_progress", "completed_qty": prev_qty + 1},
    idempotency_key="c03-idem-001",
  )
  legacy_refs = (
    update_result.get("legacy_refs")
    if isinstance(update_result, dict)
    else getattr(update_result, "legacy_refs", None)
  )
  assert legacy_refs, f"C-03 期望 legacy_refs: {update_result!r}"
  assert mock_legacy.get_write_count() >= 1


@pytest.mark.integration
@pytest.mark.parametrize("case", ["read_back"], ids=["C-04"])
def test_C04_read_back_matches_after_snapshot(case: str) -> None:
  """C-04：write 后 entity.get 与 after_snapshot 一致。"""
  entity_get = _import_callable("os_core.connector_sdk.runtime.entity", "entity_get")
  entity_update = _import_callable("os_core.connector_sdk.runtime.entity", "entity_update")

  target_fields = {"status": "completed", "completed_qty": 5}
  update_result = entity_update(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    entity_type=ENTITY_TYPE,
    entity_id=ENTITY_ID,
    fields=target_fields,
    idempotency_key="c04-idem-001",
  )
  after_snapshot = (
    update_result.get("after_snapshot")
    if isinstance(update_result, dict)
    else getattr(update_result, "after_snapshot", None)
  )
  assert after_snapshot is not None, update_result

  read_back = entity_get(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    entity_type=ENTITY_TYPE,
    entity_id=ENTITY_ID,
  )
  assert read_back.get("fields") == after_snapshot.get("fields"), (read_back, after_snapshot)
