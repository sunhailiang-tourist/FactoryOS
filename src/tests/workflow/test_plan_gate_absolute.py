"""工作流绝对门禁：stamp 机械校验 · 不依赖 Agent 自报 phase。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
GATES = ROOT / "_factoryos_pipeline" / ".gates"
PLAN_GATE = GATES / "plan.ok"
TEST_GATE = GATES / "test.ok"
CODE_GATE = GATES / "code.ok"
STATE_FILE = ROOT / "_factoryos_pipeline" / "workflow_state.md"


def _backup_gates() -> dict[str, str | None]:
  out: dict[str, str | None] = {}
  for p in (PLAN_GATE, TEST_GATE, CODE_GATE):
    out[str(p)] = p.read_text(encoding="utf-8") if p.is_file() else None
  return out


def _restore_gates(backup: dict[str, str | None]) -> None:
  for path_str, content in backup.items():
    p = Path(path_str)
    if content is None:
      if p.is_file():
        p.unlink()
    else:
      p.parent.mkdir(parents=True, exist_ok=True)
      p.write_text(content, encoding="utf-8")


@pytest.mark.workflow
def test_validate_plan_stamp_requires_plan_ok() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  backup = _backup_gates()
  if PLAN_GATE.is_file():
    PLAN_GATE.unlink()
  try:
    errors = plan_gate_lib.validate_plan_stamp()
    assert any("plan.ok" in e for e in errors)
  finally:
    _restore_gates(backup)


@pytest.mark.workflow
def test_validate_src_test_write_blocked_without_plan_ok() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  backup = _backup_gates()
  if PLAN_GATE.is_file():
    PLAN_GATE.unlink()
  try:
    errors = plan_gate_lib.validate_src_test_write()
    assert errors
  finally:
    _restore_gates(backup)


@pytest.mark.workflow
def test_validate_code_stamp_requires_code_ok() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  backup = _backup_gates()
  if CODE_GATE.is_file():
    CODE_GATE.unlink()
  try:
    errors = plan_gate_lib.validate_code_stamp(step=1)
    assert any("code.ok" in e for e in errors)
  finally:
    _restore_gates(backup)


@pytest.mark.workflow
def test_workflow_state_can_test_blocked_without_plan_ok() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  backup = _backup_gates()
  if PLAN_GATE.is_file():
    PLAN_GATE.unlink()
  try:
    text = STATE_FILE.read_text(encoding="utf-8")
    text = text.replace("phase: CAN_TEST", "phase: PLANNING")
    text = text.replace("phase: CAN_CODE", "phase: PLANNING")
    simulated = text.replace("phase: PLANNING", "phase: CAN_TEST", 1)
    errors = plan_gate_lib.validate_workflow_state_content(simulated)
    assert any("plan.ok" in e for e in errors)
  finally:
    _restore_gates(backup)


@pytest.mark.workflow
def test_write_plan_gate_invalidates_downstream_stamps() -> None:
  sys.path.insert(0, str(ROOT / "scripts"))
  import plan_gate_lib

  backup = _backup_gates()
  GATES.mkdir(parents=True, exist_ok=True)
  TEST_GATE.write_text("plan=x\ntest_plan=y\nat=z\n", encoding="utf-8")
  CODE_GATE.write_text("plan=x\nstep=1\nat=z\n", encoding="utf-8")
  try:
    plan_gate_lib.write_plan_gate_stamp("_factoryos_pipeline/2026-07-01/plan/plan-x.md")
    assert PLAN_GATE.is_file()
    assert not TEST_GATE.is_file()
    assert not CODE_GATE.is_file()
  finally:
    _restore_gates(backup)


@pytest.mark.workflow
def test_check_pipeline_step_enforces_plan_absolute_gate() -> None:
  backup = _backup_gates()
  if PLAN_GATE.is_file():
    PLAN_GATE.unlink()
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
    _restore_gates(backup)


@pytest.mark.workflow
def test_workflow_state_documents_plan_absolute_gate() -> None:
  text = STATE_FILE.read_text(encoding="utf-8")
  assert "绝对门禁" in text
  assert "确认规划" in text


@pytest.mark.workflow
def test_protect_paths_hook_module_documents_stamps() -> None:
  hook = (ROOT / ".cursor" / "hooks" / "protect-paths.py").read_text(encoding="utf-8")
  assert "plan.ok" in hook
  assert "code.ok" in hook
  assert "test.ok" in hook
