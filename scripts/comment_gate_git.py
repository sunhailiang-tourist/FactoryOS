"""Git 路径解析（CMNT-C staged/changed 注释门禁）。

作用：为 check_comments.py · comment_fix.py 提供精准文件范围。
业务关联：双速双严策略 · 仅审本次提交。
上游：git CLI
下游：check_comments.py · comment_fix.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PYTHON_PREFIXES = ("src/server/os_core/", "src/server/api/")
TS_SKIP_PARTS = (
  "api/generated/",
  ".d.ts",
  "vite-env.d.ts",
  "node_modules/",
)


def _run_git(args: list[str]) -> list[str]:
  try:
    r = subprocess.run(
      ["git", *args],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
  except OSError:
    return []
  if r.returncode != 0:
    return []
  return [ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()]


def git_staged_relpaths() -> list[str]:
  """git diff --cached --name-only（本次 commit 范围）。"""
  return _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])


def git_changed_relpaths() -> list[str]:
  """工作区改动：unstaged + staged + untracked。"""
  rels: set[str] = set()
  for args in (
    ["diff", "--name-only", "HEAD"],
    ["diff", "--name-only", "--cached"],
    ["ls-files", "--others", "--exclude-standard"],
  ):
    rels.update(_run_git(args))
  return sorted(rels)


def _is_python_gate_path(rel: str) -> bool:
  return rel.endswith(".py") and any(rel.startswith(p) for p in PYTHON_PREFIXES)


def _is_ts_gate_path(rel: str) -> bool:
  if not rel.endswith((".ts", ".tsx")):
    return False
  if not rel.startswith("src/apps/") or "/src/" not in rel:
    return False
  posix = rel.replace("\\", "/")
  return not any(part in posix for part in TS_SKIP_PARTS)


def filter_gate_paths(rels: list[str]) -> tuple[list[Path], list[Path]]:
  """返回 (python_paths, ts_paths) 绝对路径，去重排序。"""
  py: list[Path] = []
  ts: list[Path] = []
  seen: set[str] = set()
  for rel in sorted(rels):
    if rel in seen:
      continue
    seen.add(rel)
    path = (ROOT / rel).resolve()
    if not path.is_file():
      continue
    if _is_python_gate_path(rel):
      py.append(path)
    elif _is_ts_gate_path(rel):
      ts.append(path)
  return py, ts


def python_full_roots() -> list[Path]:
  return [
    (ROOT / "src" / "server" / "os_core").resolve(),
    (ROOT / "src" / "server" / "api").resolve(),
  ]


def ts_full_app_roots() -> list[Path]:
  out: list[Path] = []
  apps = ROOT / "src" / "apps"
  if apps.is_dir():
    for child in sorted(apps.iterdir()):
      if child.is_dir() and (child / "src").is_dir():
        out.append(child.resolve())
  return out
