"""CMNT 注释债 L3 验收（pytest 包装 check_python_comments）。

作用：为 gate step --step N -k 'CMNT-0N' 提供可收集用例（避免 0 selected / exit 5）。
业务关联：plan 1a.5 · CMNT-01～05 分批机械门禁。
上游：contracts/python_comment_backfill_batches.yaml
下游：scripts/check_python_comments.py · gate step
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
PYTHON = sys.executable

# 与 contracts/python_comment_backfill_batches.yaml gate_exit 对齐
_CMNT_PATHS: dict[str, list[str]] = {
  "CMNT-01": [
    "src/server/os_core/shared_contracts",
    "src/server/os_core/tenant_service",
  ],
  "CMNT-02": [
    "src/server/os_core/platform_registry",
    "src/server/os_core/connector_sdk",
    "src/server/os_core/rule_engine",
    "src/server/os_core/graph_service",
  ],
  "CMNT-02-b1b": [
    "src/server/os_core/agent_orchestrator",
    "src/server/os_core/audit_service",
    "src/server/os_core/execution_service",
    "src/server/os_core/license_service",
    "src/server/os_core/mcp_gateway",
    "src/server/os_core/package_service",
    "src/server/os_core/reconciliation_service",
  ],
  "CMNT-03": ["src/server/api/modules"],
  "CMNT-04": [
    "src/server/api/config",
    "src/server/api/application",
  ],
}


def _run_comment_gate(*, paths: list[str] | None = None) -> subprocess.CompletedProcess[str]:
  cmd = [PYTHON, str(SCRIPTS / "check_python_comments.py")]
  if paths:
    cmd.extend(["--paths", *paths])
  return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-01"], ids=["CMNT-01"])
def test_CMNT_comment_gate_batch_green(ac_id: str) -> None:
  """CMNT-0N：指定目录 check_python_comments 须 0 violation。"""
  paths = _CMNT_PATHS[ac_id]
  r = _run_comment_gate(paths=paths)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-02"], ids=["CMNT-02"])
def test_CMNT02_os_core_batches_comment_gate(ac_id: str) -> None:
  """CMNT-02：B1a os_core 四目录注释批须全绿（Step 2）。"""
  paths = _CMNT_PATHS[ac_id]
  r = _run_comment_gate(paths=paths)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-02-b1b"], ids=["CMNT-02-b1b"])
def test_CMNT02b1b_os_core_batches_comment_gate(ac_id: str) -> None:
  """CMNT-02-b1b：B1b os_core 七目录注释批须全绿（Step 3 后启用）。"""
  paths = _CMNT_PATHS[ac_id]
  r = _run_comment_gate(paths=paths)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-03"], ids=["CMNT-03"])
def test_CMNT03_api_modules_comment_gate(ac_id: str) -> None:
  """CMNT-03：api/modules 薄路由层注释须全绿（Step 4 后启用）。"""
  paths = _CMNT_PATHS[ac_id]
  r = _run_comment_gate(paths=paths)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-04"], ids=["CMNT-04"])
def test_CMNT04_api_config_comment_gate(ac_id: str) -> None:
  """CMNT-04：api/config + application 底座注释须全绿（Step 5 后启用）。"""
  paths = _CMNT_PATHS[ac_id]
  r = _run_comment_gate(paths=paths)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()


@pytest.mark.workflow
@pytest.mark.parametrize("ac_id", ["CMNT-05"], ids=["CMNT-05"])
def test_CMNT05_full_server_comment_gate(ac_id: str) -> None:
  """CMNT-05：src/server 全量注释扫描 0 violation（Step 5 终轮）。"""
  _ = ac_id
  r = _run_comment_gate(paths=None)
  assert r.returncode == 0, (r.stderr or r.stdout or "comment gate failed").strip()
