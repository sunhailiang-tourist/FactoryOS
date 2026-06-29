"""结构 commit 门禁：仅 src 主干目录变更时拦截。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


def _import_repo_structure():
  sys.path.insert(0, str(SCRIPTS))
  import repo_structure as mod

  return mod


def test_file_only_staged_does_not_trigger_commit_gate() -> None:
  rs = _import_repo_structure()
  snap = rs.load_snapshot()
  staged = [
    "src/server/os_core/registry.py",
    "src/server/os_core/README.md",
    "src/server/os_core/graph_service/store.py",
    "src/server/api/modules/registry/controllers/foo.py",
    "README.md",
    "docs/准备/2026-06-16/18-基座文档一致性矩阵.md",
  ]
  assert rs.detect_staged_trunk_structure_changes(staged, snap) == []
  assert rs.analyze_commit_coupling(staged, snap) == []


def test_new_kernel_module_triggers_structure_gate() -> None:
  rs = _import_repo_structure()
  snap = rs.load_snapshot()
  staged = ["src/server/os_core/new_skill/service.py"]
  drifts = rs.analyze_commit_coupling(staged, snap)
  kinds = {d.kind for d in drifts}
  assert "commit_new_kernel_module" in kinds
  assert "commit_missing_snapshot" in kinds


def test_new_src_trunk_dir_triggers_structure_gate() -> None:
  rs = _import_repo_structure()
  snap = rs.load_snapshot()
  staged = ["src/server/new_service/main.py"]
  drifts = rs.analyze_commit_coupling(staged, snap)
  kinds = {d.kind for d in drifts}
  assert "commit_new_trunk_dir" in kinds
  assert "commit_missing_snapshot" in kinds


def test_is_allowed_dir_prefix_under_canonical() -> None:
  rs = _import_repo_structure()
  snap = rs.load_snapshot()
  assert rs.is_allowed_dir_prefix("src/server/os_core/graph_service", snap)
  assert rs.is_allowed_dir_prefix("src/server", snap)
  assert not rs.is_allowed_dir_prefix("src/server/new_thing", snap)
