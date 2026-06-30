"""契约层：OpenAPI 真源存在性与 Harness 脚本可执行性。

业务：确保 L2 Spec 轨机器可读真源未断裂；与 scripts/check_harness L0 互补。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.contract
def test_openapi_file_exists(openapi_path: Path) -> None:
  assert openapi_path.is_file(), f"missing OpenAPI: {openapi_path}"


@pytest.mark.contract
def test_openapi_has_v1_paths(openapi_path: Path) -> None:
  text = openapi_path.read_text(encoding="utf-8")
  assert "/v1/graphs" in text
  assert "openapi:" in text or "paths:" in text


@pytest.mark.contract
def test_openapi_w5_agent_harness_paths(openapi_path: Path) -> None:
  """W5 Step4：OpenAPI v1.1 须声明 agent plan · harness confirm 端点。"""
  text = openapi_path.read_text(encoding="utf-8")
  assert "/v1/agent/plan:" in text
  assert "/v1/harness/confirm:" in text
  assert "DslPlan" in text
  assert "ExecutionRecord" in text


@pytest.mark.workflow
def test_harness_contracts_tier_green() -> None:
  r = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "check_harness.py"), "--tier", "contracts"],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.workflow
def test_gate_plan_script_exists() -> None:
  assert (ROOT / "scripts" / "gate_cli.py").is_file()
