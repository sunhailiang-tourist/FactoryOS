"""W4 Step1–2/4：Blueprint registry · runtime · 校验（B-01～B-04）。

业务：catalog 加载 conn-mock · L2 op 执行 · mapping 负向 · revert 声明门禁。
上游：connector_sdk.registry · connector_sdk.runtime
下游：gate step --step 1 -k 'B-01'
"""
from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any

import pytest

MOCK_PACK_ID = "conn-mock"
DEFAULT_TENANT_ID = "default"


def _import_callable(module_path: str, attr: str) -> Callable[..., Any]:
  """按模块路径导入可调用对象（W4 runtime 未实现时红测）。"""
  mod = importlib.import_module(module_path)
  fn = getattr(mod, attr, None)
  assert fn is not None, f"缺少 {module_path}.{attr}"
  return fn


def _sample_governed_write_params() -> dict[str, Any]:
  return {
    "entity_type": "work_order",
    "entity_id": "wo-w4-b02",
    "fields": {"status": "in_progress", "completed_qty": 1},
  }


@pytest.mark.integration
@pytest.mark.parametrize("case", ["load"], ids=["B-01"])
def test_B01_load_mock_blueprint_lists_governed_write(case: str) -> None:
  """B-01：Registry 加载 conn-mock blueprint，ops 含 GOVERNED_WRITE。"""
  load_blueprint = _import_callable("os_core.connector_sdk.registry", "load_blueprint")
  blueprint = load_blueprint(pack_id=MOCK_PACK_ID, tenant_id=DEFAULT_TENANT_ID)
  assert blueprint is not None
  ops = blueprint.get("spec", {}).get("ops", [])
  verbs = {op.get("verb") for op in ops}
  assert "GOVERNED_WRITE" in verbs, f"conn-mock ops 须含 GOVERNED_WRITE: {verbs}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["runtime_l2"], ids=["B-02"])
def test_B02_runtime_execute_l2_populates_legacy_refs(case: str) -> None:
  """B-02：Runtime 执行 GOVERNED_WRITE，legacy_refs 非空。"""
  execute_op = _import_callable("os_core.connector_sdk.runtime.execute", "execute_op")
  result = execute_op(
    pack_id=MOCK_PACK_ID,
    tenant_id=DEFAULT_TENANT_ID,
    verb="GOVERNED_WRITE",
    params=_sample_governed_write_params(),
    idempotency_key="b02-idem-001",
  )
  if isinstance(result, dict):
    legacy_refs = result.get("legacy_refs")
  else:
    legacy_refs = getattr(result, "legacy_refs", None)
  assert legacy_refs, f"B-02 期望 legacy_refs populated: {result!r}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["mapping_error"], ids=["B-03"])
def test_B03_mapping_error_on_missing_required_field(case: str) -> None:
  """B-03：缺必填 mapping 字段时返回 MAPPING_ERROR。"""
  execute_op = _import_callable("os_core.connector_sdk.runtime.execute", "execute_op")
  with pytest.raises(Exception) as exc_info:
    execute_op(
      pack_id=MOCK_PACK_ID,
      tenant_id=DEFAULT_TENANT_ID,
      verb="GOVERNED_WRITE",
      params={"entity_type": "work_order"},
      idempotency_key="b03-idem-001",
    )
  message = str(exc_info.value)
  code = getattr(exc_info.value, "code", "")
  assert "MAPPING_ERROR" in message or code == "MAPPING_ERROR", message


_INVALID_L2_WITHOUT_REVERT: dict[str, Any] = {
  "apiVersion": "factoryos.io/v1",
  "kind": "ConnectorBlueprint",
  "metadata": {
    "pack_id": "conn-test-invalid",
    "system": "mock",
    "vendor": "factoryos",
    "level": "L2",
  },
  "spec": {
    "auth": {"type": "none", "secrets_ref": "none"},
    "base_url": "http://mock.local",
    "ops": [
      {
        "verb": "GOVERNED_WRITE",
        "method": "POST",
        "path": "/entity/update",
      }
    ],
  },
}


@pytest.mark.integration
@pytest.mark.parametrize("case", ["no_revert"], ids=["B-04"])
def test_B04_l2_op_without_revert_is_blueprint_invalid(case: str) -> None:
  """B-04：L2 op 未声明 revert → BLUEPRINT_INVALID / 校验失败。"""
  validate_blueprint = _import_callable("os_core.connector_sdk.registry", "validate_blueprint")
  result = validate_blueprint(_INVALID_L2_WITHOUT_REVERT)
  if isinstance(result, dict):
    assert result.get("valid") is False, result
    error_codes = {e.get("code") for e in result.get("errors", []) if isinstance(e, dict)}
    assert "BLUEPRINT_INVALID" in error_codes or any(
      "revert" in str(e).lower() for e in result.get("errors", [])
    ), result
  else:
    assert getattr(result, "valid", True) is False, result
