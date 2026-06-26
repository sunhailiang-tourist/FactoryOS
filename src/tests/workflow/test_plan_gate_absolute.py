"""工作流绝对门禁：无「确认规划」+ plan.ok 不得视为可执行。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PLAN_GATE = ROOT / "_factoryos_pipeline" / ".gates" / "plan.ok"
STATE_FILE = ROOT / "_factoryos_pipeline" / "workflow_state.md"


@pytest.mark.workflow
def test_plan_gate_lib_validate_detects_missing_plan_ok() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  if PLAN_GATE.is_file():
    backup = PLAN_GATE.read_text(encoding="utf-8")
    PLAN_GATE.unlink()
  else:
    backup = None
  try:
    errors = plan_gate_lib.validate_plan_confirmed(require_phase_min="CAN_TEST")
    assert any("plan.ok" in e or "绝对门禁" in e for e in errors)
  finally:
    if backup is not None:
      PLAN_GATE.parent.mkdir(parents=True, exist_ok=True)
      PLAN_GATE.write_text(backup, encoding="utf-8")


@pytest.mark.workflow
def test_check_pipeline_step_enforces_plan_absolute_gate() -> None:
  if PLAN_GATE.is_file():
    backup = PLAN_GATE.read_text(encoding="utf-8")
    PLAN_GATE.unlink()
  else:
    backup = None
  try:
    r = subprocess.run(
      [
        sys.executable,
        str(ROOT / "scripts" / "check_pipeline.py"),
        "--gate",
        "step",
        "--step",
        "1",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
    )
    assert r.returncode != 0
    assert "绝对门禁" in r.stderr
  finally:
    if backup is not None:
      PLAN_GATE.parent.mkdir(parents=True, exist_ok=True)
      PLAN_GATE.write_text(backup, encoding="utf-8")


@pytest.mark.workflow
def test_workflow_state_documents_plan_absolute_gate() -> None:
  text = STATE_FILE.read_text(encoding="utf-8")
  assert "绝对门禁" in text
  assert "确认规划" in text
