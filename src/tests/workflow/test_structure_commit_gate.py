"""结构 commit 门禁：误报与提示文案。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


def _import_check_structure():
  sys.path.insert(0, str(SCRIPTS))
  import check_structure_change as mod

  return mod


def test_staged_paths_ignore_os_core_root_files() -> None:
  mod = _import_check_structure()
  known = {"shared_contracts", "graph_service"}
  staged = [
    "src/server/os_core/registry.py",
    "src/server/os_core/README.md",
    "src/server/os_core/graph_service/store.py",
    "src/server/os_core/new_skill/service.py",
  ]
  assert mod._staged_new_kernel_modules(staged, known) == {"new_skill"}
