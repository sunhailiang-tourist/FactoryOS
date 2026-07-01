"""W7 Step6：DSL D-04 · Agent E-08。

业务：L2 无 compensator 拒绝注册 · orchestrator 不得直写 connector。
上游：plan Step6
下游：gate step --step 6 -k 'D-04' · '-k E-08'
"""
from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
AGENT_ORCHESTRATOR = ROOT / "src" / "server" / "os_core" / "agent_orchestrator"


def _get_register_dsl_verb():
  """导入 CMV 注册校验（W7 Step6 · 未实现时红测）。"""
  module = importlib.import_module("os_core.shared_contracts.cmv_registry")
  fn = getattr(module, "register_dsl_verb", None)
  assert fn is not None, "缺少 cmv_registry.register_dsl_verb（D-04）"
  return fn


@pytest.mark.integration
@pytest.mark.parametrize("case", ["l2_no_compensator"], ids=["D-04"])
def test_D04_register_l2_without_compensator_rejected_422(
  case: str,
  api_client: TestClient,
) -> None:
  """D-04：POST registry L2 无 compensator → 422。"""
  resp = api_client.post(
    "/v1/registry/cmv/verbs",
    json={
      "verb": "TEST_L2_NO_COMP_W7",
      "level": "L2",
      "compensator": None,
      "params_schema": {"type": "object"},
      "description": "W7 D-04 negative",
    },
  )
  if resp.status_code == 404:
    register_dsl_verb = _get_register_dsl_verb()
    with pytest.raises(Exception) as exc_info:
      register_dsl_verb(
        verb="TEST_L2_NO_COMP_W7",
        level="L2",
        compensator=None,
        params_schema={"type": "object"},
      )
    assert "422" in str(exc_info.value) or "compensator" in str(exc_info.value).lower()
    return

  assert resp.status_code == 422, resp.text
  body = resp.json()
  assert "compensator" in str(body).lower() or body.get("code"), body


@pytest.mark.workflow
@pytest.mark.parametrize("case", ["no_connector_write"], ids=["E-08"])
def test_E08_agent_orchestrator_must_not_import_connector_write(case: str) -> None:
  """E-08：agent_orchestrator 不得 import connector 写路径。"""
  forbidden = (
    "connector_sdk.runtime",
    "execute_op",
    "mock_legacy",
    "entity_update",
  )
  assert AGENT_ORCHESTRATOR.is_dir(), f"missing {AGENT_ORCHESTRATOR}"
  violations: list[str] = []
  for py_file in AGENT_ORCHESTRATOR.rglob("*.py"):
    text = py_file.read_text(encoding="utf-8")
    for needle in forbidden:
      if needle in text:
        violations.append(f"{py_file.relative_to(ROOT)}: {needle}")
  assert not violations, "E-08 violations:\n" + "\n".join(violations)
