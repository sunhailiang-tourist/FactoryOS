"""Dev → Test → Verify 联动绝对门禁（plan 目录隔离）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


@pytest.mark.workflow
def test_step_chain_requires_dev_before_test(
  tmp_path: Path,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  sys.path.insert(0, str(SCRIPTS))
  import step_chain_lib

  plan_dir = tmp_path / "2026-06-99"
  (plan_dir / "test").mkdir(parents=True)
  monkeypatch.setattr(step_chain_lib, "plan_pipeline_dir", lambda s=None: plan_dir)

  errors = step_chain_lib.validate_step_test_done(1, require_pass=False)
  assert any("step-stop" in e or "Dev" in e for e in errors)


@pytest.mark.workflow
def test_step_chain_closed_needs_all_three_artifacts(
  tmp_path: Path,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  sys.path.insert(0, str(SCRIPTS))
  import plan_gate_lib
  import step_chain_lib

  plan_dir = tmp_path / "2026-06-99"
  (plan_dir / "step-stop").mkdir(parents=True)
  (plan_dir / "test").mkdir()
  (plan_dir / "verify").mkdir()
  plan_rel = "_factoryos_pipeline/2026-06-99/plan/plan-test.md"
  (plan_dir / "plan").mkdir()
  (plan_dir / "plan" / "plan-test.md").write_text("# plan\n", encoding="utf-8")

  stop = plan_dir / "step-stop" / "step-stop-1200-step1.md"
  stop.write_text("## 结论：通过\n", encoding="utf-8")
  reg = plan_dir / "test" / "test-1200-step1-regression.md"
  reg.write_text("## 结论：通过\n", encoding="utf-8")
  vf = plan_dir / "verify" / "verify-1200-step1.md"
  vf.write_text("## 结论：通过\n", encoding="utf-8")

  fake_state = {"plan": plan_rel}

  monkeypatch.setattr(step_chain_lib, "plan_pipeline_dir", lambda s=None: plan_dir)
  monkeypatch.setattr(plan_gate_lib, "read_workflow_state", lambda: fake_state)

  assert step_chain_lib.validate_step_chain_closed(1) == []
  assert step_chain_lib.validate_can_start_step_dev(2) == []


@pytest.mark.workflow
def test_can_start_step2_blocked_without_step1_chain(monkeypatch: pytest.MonkeyPatch) -> None:
  sys.path.insert(0, str(SCRIPTS))
  import step_chain_lib

  monkeypatch.setattr(
    step_chain_lib,
    "plan_pipeline_dir",
    lambda s=None: ROOT / "_factoryos_pipeline" / "2099-01-01",
  )
  errors = step_chain_lib.validate_can_start_step_dev(2)
  assert errors
  assert any("Step 1" in e or "step1" in e.lower() for e in errors)


@pytest.mark.workflow
def test_check_pipeline_step_uses_plan_scoped_chain() -> None:
  r = subprocess.run(
    [
      sys.executable,
      str(SCRIPTS / "check_pipeline.py"),
      "--gate",
      "step",
      "--step",
      "1",
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  if r.returncode == 0:
    pytest.skip("step 1 chain already closed in repo")
  assert "联动门禁" in r.stderr or "step-stop" in r.stderr.lower()


@pytest.mark.workflow
def test_workflow_state_documents_step_chain_gate() -> None:
  text = (ROOT / "_factoryos_pipeline" / "workflow_state.md").read_text(encoding="utf-8")
  assert "联动" in text or "Dev→Test→Verify" in text
