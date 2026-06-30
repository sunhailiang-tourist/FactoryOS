"""结构 commit 门禁：仅 src 主干目录变更时拦截。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


def _run_structure_check(*, pre_commit: bool = False) -> subprocess.CompletedProcess[str]:
  cmd = [sys.executable, str(SCRIPTS / "check_structure_change.py")]
  if pre_commit:
    cmd.append("--pre-commit")
  return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def test_staged_paths_ignore_os_core_root_files_via_script() -> None:
  """脚本级：仅文件改动时 pre-commit 应跳过（不 import scripts 包，避免 deptry 误报）。"""
  r = _run_structure_check(pre_commit=True)
  assert r.returncode == 0, r.stderr or r.stdout
  assert "无 src 主干目录变更" in (r.stdout or "")


def test_structure_check_manual_mode_green() -> None:
  r = _run_structure_check()
  assert r.returncode == 0, r.stderr or r.stdout
