"""W2 Step3：execution_service dry_run（E-06）与幂等（E-07）。

业务：唯一写入口试跑；dry_run 不写 Legacy；同 idempotency_key 不重复写。
上游：os_core.execution_service · connector_sdk mock write
下游：gate step --step 3 -k 'E-06'
"""
from __future__ import annotations

import importlib
from typing import Any

import pytest


def _execute_request(env: dict[str, str], **overrides: Any) -> dict:
  base = {
    "tenant_id": "default",
    "graph_id": env["graph_id"],
    "graph_version": env["version"],
    "ruleset_id": env["ruleset_id"],
    "verb": "GOVERNED_WRITE",
    "params": {"entity": "work_order"},
    "dry_run": True,
    "actor": {"user_id": "test-operator", "role": "operator", "channel": "api"},
  }
  base.update(overrides)
  return base


def _get_execution_service():
  module = importlib.import_module("os_core.execution_service")
  execute_fn = getattr(module, "execute", None)
  assert execute_fn is not None, "缺少 os_core.execution_service.execute"
  return execute_fn


def _get_mock_legacy_module():
  return importlib.import_module("os_core.connector_sdk.mock_legacy")


def _reset_mock_legacy_writes() -> None:
  mock = _get_mock_legacy_module()
  reset = getattr(mock, "reset_write_count", None)
  assert reset is not None, "缺少 connector_sdk.mock_legacy.reset_write_count"
  reset()


def _mock_legacy_write_count() -> int:
  mock = _get_mock_legacy_module()
  getter = getattr(mock, "get_write_count", None)
  assert getter is not None, "缺少 connector_sdk.mock_legacy.get_write_count"
  return getter()


@pytest.fixture
def kernel_w3_env(migrated_db_session):
  """E-06/E-07 内核测试 W3 门禁前置。"""
  from tests.integration.w3_helpers import seed_frozen_env_kernel

  return seed_frozen_env_kernel(migrated_db_session)


@pytest.mark.integration
@pytest.mark.parametrize("case", ["dry_run"], ids=["E-06"])
def test_E06_dry_run_does_not_write_legacy(
  case: str,
  migrated_db_session,
  kernel_w3_env: dict[str, str],
) -> None:
  """E-06：dry_run=true 时 status=simulated 且 Legacy mock 无写入。"""
  execute = _get_execution_service()
  _reset_mock_legacy_writes()
  before = _mock_legacy_write_count()

  result = execute(
    session=migrated_db_session,
    request=_execute_request(kernel_w3_env, dry_run=True, idempotency_key="e06-key-001"),
  )
  migrated_db_session.commit()

  assert result.status == "simulated", result
  after = _mock_legacy_write_count()
  assert after == before, f"dry_run 不应写 Legacy：before={before} after={after}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["idempotency"], ids=["E-07"])
def test_E07_idempotency_key_no_duplicate_write(
  case: str,
  migrated_db_session,
  kernel_w3_env: dict[str, str],
) -> None:
  """E-07：相同 idempotency_key 重试不重复写 Legacy，返回同一 exec_id。"""
  execute = _get_execution_service()
  _reset_mock_legacy_writes()

  key = "e07-idem-key-001"
  req = _execute_request(kernel_w3_env, dry_run=True, idempotency_key=key)

  first = execute(session=migrated_db_session, request=req)
  migrated_db_session.commit()
  writes_after_first = _mock_legacy_write_count()

  second = execute(session=migrated_db_session, request=req)
  migrated_db_session.commit()
  writes_after_second = _mock_legacy_write_count()

  assert first.exec_id == second.exec_id
  assert writes_after_second == writes_after_first, "幂等重试不得增加 Legacy 写次数"
