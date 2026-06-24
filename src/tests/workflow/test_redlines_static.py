"""工作流静态兜底：红线相关的可静态验证项（无需运行 API）。

E-08 等需运行时的用例仍在 ac/test_base001_registry pending 中。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.workflow
def test_import_boundaries_script_passes() -> None:
  r = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "check_import_boundaries.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr


@pytest.mark.workflow
def test_workflow_state_template_exists() -> None:
  p = ROOT / "_factoryos_pipeline" / "workflow_state.md"
  assert p.is_file(), "missing _factoryos_pipeline/workflow_state.md"
