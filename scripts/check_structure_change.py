#!/usr/bin/env python3
"""结构变更提交门禁：仅 src 主干目录变化时拦截 commit。

Usage:
  uv run python scripts/check_structure_change.py           # 全量对账（gate pr）
  uv run python scripts/check_structure_change.py --pre-commit  # git pre-commit

Exit 0 = 通过；1 = 漂移（stderr 含修复步骤）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from repo_structure import (
  StructureReport,
  analyze_commit_coupling,
  analyze_structure_drift,
  format_drift_report,
  format_remediation,
  load_snapshot,
  repo_root,
)

ROOT = repo_root()


def git_staged_paths() -> list[str] | None:
  """暂存区路径；非 git 仓库返回 None。"""
  try:
    r = subprocess.run(
      ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
      cwd=ROOT,
      capture_output=True,
      text=True,
    )
  except OSError:
    return None
  if r.returncode != 0:
    return None
  return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def run_check(*, pre_commit: bool) -> int:
  snap = load_snapshot()
  staged: list[str] | None = None

  if pre_commit:
    staged = git_staged_paths()
    if staged is not None:
      coupling = analyze_commit_coupling(staged, snap)
      if not coupling:
        print("OK: 本次 commit 无 src 主干目录变更，结构 commit 门禁跳过")
        return 0
      report = StructureReport(drifts=coupling)
    else:
      report = analyze_structure_drift(snap)
  else:
    report = analyze_structure_drift(snap)

  if report.ok:
    print(
      f"OK: 项目结构与快照一致 "
      f"(v{snap.version} · {snap.kernel_module_count} kernel · {snap.decision_ref})"
    )
    return 0

  print(format_drift_report(report), file=sys.stderr)
  print(format_remediation(report, staged=staged if pre_commit else None), file=sys.stderr)
  return 1


def main() -> int:
  parser = argparse.ArgumentParser(description="Structure snapshot drift gate (commit blocker)")
  parser.add_argument(
    "--pre-commit",
    action="store_true",
    help="Git pre-commit: only block when staged changes touch src trunk directory layout",
  )
  args = parser.parse_args()
  return run_check(pre_commit=args.pre_commit)


if __name__ == "__main__":
  sys.exit(main())
