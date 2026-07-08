"""Git 路径解析（CMNT-C · 前端 App · standalone / umbrella 双模）。

作用：为 check_comments.py · comment_fix.py 提供 staged/changed/full 范围。
业务关联：web-admin 迁出后 src/ 路径；monorepo 内 src/apps/<id>/src/ 路径。
上游：git CLI · devkit.manifest.yaml
下游：check_comments.py · comment_fix.py · check_comments_commit_hook.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

TS_SKIP_PARTS = (
  "api/generated/",
  ".d.ts",
  "vite-env.d.ts",
  "node_modules/",
)


def _run_git(args: list[str], *, cwd: Path) -> list[str]:
  try:
    r = subprocess.run(
      ["git", *args],
      cwd=cwd,
      capture_output=True,
      text=True,
      check=False,
    )
  except OSError:
    return []
  if r.returncode != 0:
    return []
  return [ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()]


def git_toplevel() -> Path | None:
  """仓库 git 根；非 git 仓返回 None。"""
  lines = _run_git(["rev-parse", "--show-toplevel"], cwd=APP_ROOT)
  if not lines:
    return None
  return Path(lines[0]).resolve()


def ts_git_prefix() -> str:
  """门禁 TS 路径在 git 相对路径下的前缀。"""
  top = git_toplevel()
  if top is None or top.resolve() == APP_ROOT.resolve():
    return "src/"
  rel = APP_ROOT.resolve().relative_to(top).as_posix()
  return f"{rel}/src/"


def git_staged_relpaths() -> list[str]:
  top = git_toplevel() or APP_ROOT
  return _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=top)


def git_changed_relpaths() -> list[str]:
  top = git_toplevel() or APP_ROOT
  rels: set[str] = set()
  for args in (
    ["diff", "--name-only", "HEAD"],
    ["diff", "--name-only", "--cached"],
    ["ls-files", "--others", "--exclude-standard"],
  ):
    rels.update(_run_git(args, cwd=top))
  return sorted(rels)


def _is_ts_gate_path(rel: str) -> bool:
  if not rel.endswith((".ts", ".tsx")):
    return False
  prefix = ts_git_prefix()
  if not rel.startswith(prefix):
    return False
  posix = rel.replace("\\", "/")
  return not any(part in posix for part in TS_SKIP_PARTS)


def filter_gate_paths(rels: list[str]) -> list[Path]:
  """返回本 App 门禁 TS 绝对路径（去重排序）。"""
  out: list[Path] = []
  top = git_toplevel() or APP_ROOT
  seen: set[str] = set()
  for rel in sorted(rels):
    if rel in seen or not _is_ts_gate_path(rel):
      continue
    seen.add(rel)
    path = (top / rel).resolve()
    if path.is_file():
      out.append(path)
  return out


def ts_full_src_root() -> Path:
  """--full 扫描：始终 App 内 src/。"""
  return (APP_ROOT / "src").resolve()
