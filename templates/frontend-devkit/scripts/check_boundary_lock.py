#!/usr/bin/env python3
"""web-admin 独立边界 + 架构锁强制门禁。

用法：
  python scripts/check_boundary_lock.py
  WEB_STRICT_BOUNDARY=1 python scripts/check_boundary_lock.py

作用：托管于 FactoryOS 时拦截跨项目写码与结构漂移。
业务关联：contracts/WEB-ARCHITECTURE-LOCK.yaml · .cursor/rules/WEB-00*
上游：activate.sh · check_harness.py
下游：AI 工作流停机关键词「确认越权」「确认结构变更」
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT / "scripts"))

from boundary_lock_lib import run_all_checks  # noqa: E402


def _git_staged_paths(app_root: Path) -> list[str]:
  try:
    proc = subprocess.run(
      ["git", "diff", "--cached", "--name-only"],
      cwd=app_root,
      capture_output=True,
      text=True,
      check=False,
    )
  except OSError:
    return []
  if proc.returncode != 0:
    return []
  return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
  strict = os.environ.get("WEB_STRICT_BOUNDARY", "").strip() in {"1", "true", "yes"}
  staged = _git_staged_paths(APP_ROOT) if strict else None
  errors = run_all_checks(APP_ROOT, staged_paths=staged)
  if errors:
    print("web-admin boundary/lock FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    print(
      "\n停机：须用户发送「确认结构变更」或「确认越权」后方可继续。",
      file=sys.stderr,
    )
    return 1
  mode = "strict+staged" if strict and staged else "static"
  print(f"OK: web-admin boundary lock ({mode})")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
