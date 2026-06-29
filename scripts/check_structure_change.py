#!/usr/bin/env python3
"""结构变更提交门禁：快照漂移 → 拦截 commit 并给出同步步骤。

Usage:
  uv run python scripts/check_structure_change.py           # 手动对账
  uv run python scripts/check_structure_change.py --pre-commit  # git pre-commit

Exit 0 = 结构与快照一致；1 = 漂移（stderr 含修复步骤）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from repo_structure import (
  StructureDrift,
  analyze_structure_drift,
  format_drift_report,
  format_remediation,
  load_snapshot,
  render_path_snapshot_md,
  repo_root,
)

ROOT = repo_root()
SNAPSHOT_YAML = "contracts/repo-structure.yaml"
PATH_SNAPSHOT_MD = ".cursor/factoryos/PATH-SNAPSHOT.md"


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


def _staged_new_kernel_modules(staged: list[str], known: set[str]) -> set[str]:
  """从暂存路径推断「新内核模块目录名」（不含 os_core 根下的 registry.py / README.md）。"""
  found: set[str] = set()
  for path in staged:
    if not path.startswith("src/server/os_core/"):
      continue
    parts = path.split("/")
    # 仅 src/server/os_core/<module>/... 算模块；根目录单文件（registry.py 等）跳过
    if len(parts) < 5:
      continue
    mod = parts[3]
    if mod in known or mod.startswith(".") or mod == "__pycache__":
      continue
    found.add(mod)
  return found


def _touches_structure_prefix(staged: list[str], prefixes: tuple[str, ...]) -> bool:
  return any(any(p.startswith(pref) for pref in prefixes) for p in staged)


def analyze_commit_coupling(staged: list[str]) -> list[StructureDrift]:
  """暂存区是否携带结构变更但未同步快照。"""
  if not staged:
    return []
  snap = load_snapshot()
  known_kernel = set(snap.kernel_modules)
  drifts: list[StructureDrift] = []

  has_yaml = SNAPSHOT_YAML in staged
  has_md = PATH_SNAPSHOT_MD in staged
  new_mods = _staged_new_kernel_modules(staged, known_kernel)

  for mod in sorted(new_mods):
    drifts.append(
      StructureDrift(
        "commit_touched_structure",
        f"暂存区含新内核路径 src/server/os_core/{mod}/（未在 snapshot.kernel.modules）",
      )
    )

  touches = _touches_structure_prefix(staged, snap.commit_watch_prefixes)
  if touches and (new_mods or SNAPSHOT_YAML in staged) and not has_yaml:
    drifts.append(
      StructureDrift(
        "commit_missing_snapshot",
        f"触及结构路径时须同 commit staged `{SNAPSHOT_YAML}`",
      )
    )

  if has_yaml:
    expected = render_path_snapshot_md(load_snapshot())
    if not expected.endswith("\n"):
      expected += "\n"
    md_path = ROOT / PATH_SNAPSHOT_MD
    current = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    if current != expected and not has_md:
      drifts.append(
        StructureDrift(
          "commit_missing_path_snapshot",
          f"已改 `{SNAPSHOT_YAML}` 须运行 gen_path_snapshot 并 staged `{PATH_SNAPSHOT_MD}`",
        )
      )

  return drifts


def run_check(*, pre_commit: bool) -> int:
  snap = load_snapshot()
  report = analyze_structure_drift(snap)
  staged: list[str] | None = None

  if pre_commit:
    staged = git_staged_paths()
    if staged is not None:
      report.drifts.extend(analyze_commit_coupling(staged))

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
    help="Git pre-commit mode: also validate staged files include snapshot updates",
  )
  args = parser.parse_args()
  return run_check(pre_commit=args.pre_commit)


if __name__ == "__main__":
  sys.exit(main())
