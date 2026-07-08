#!/usr/bin/env python3
"""commit 交互式注释门禁（CMNT-C · pre-commit 专用）。

作用：校验 staged → 展示违规与必要性 → 用户确认后补全 → 重新 stage 再验。
业务关联：双速双严 · 用户确认后才写入 comment_fix。
上游：check_comments.run_check · comment_fix 补齐逻辑
下游：.pre-commit-config.yaml factoryos-comments-staged

非 TTY（CI/脚本）：仅拦截，不交互、不自动补全。
"""
from __future__ import annotations

import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_fix_lib as cfl  # noqa: E402
import comment_gate_git as cgg  # noqa: E402
from check_comments import run_check  # noqa: E402

# 违规关键词 → (规则层, 必要性说明)
_VIOLATION_HINTS: list[tuple[str, str, str]] = [
  ("missing module docstring", "P0", "文件头四标签是读代码懂业务的入口；无文件头禁止合入。"),
  ("file header missing", "P0", "TS 七标签文件头须齐全，便于 harness 与跨模块追踪。"),
  ("missing file header", "P0", "TS 七标签文件头须齐全，便于 harness 与跨模块追踪。"),
  ("missing docstring", "P0", "公开函数须有功能/上下游说明，否则调用链不可审计。"),
  ("exported function missing JSDoc", "P0", "export 函数是对外 API，JSDoc 为前端门禁硬要求。"),
  ("JSDoc missing", "P0", "export 函数 JSDoc 关键词不全，无法机械验收。"),
  ("Field(description", "P1", "Pydantic 字段 description 是契约自描述，禁止裸字段上线。"),
  ("block comment", "P2", "复杂函数体须有块注释，说明业务分支而非实现细节。"),
  ("PlatformError", "P3", "抛 PlatformError 须在 doc 写异常/错误码，便于排障与 AC 对账。"),
  ("throws but", "P3", "throw 须在 JSDoc 声明异常语义，避免调用方误用。"),
  ("file header too short", "P0", "文件头过短视为模板敷衍，须写清作用与上下游。"),
]


def _classify_errors(errors: list[str]) -> dict[str, list[str]]:
  """按规则层聚合违规行。"""
  buckets: dict[str, list[str]] = defaultdict(list)
  for err in errors:
    layer = "其他"
    for needle, lvl, _ in _VIOLATION_HINTS:
      if needle.lower() in err.lower():
        layer = lvl
        break
    buckets[layer].append(err)
  return dict(buckets)


def _print_report(errors: list[str], py_n: int, ts_n: int) -> None:
  print("\n⛔ 注释门禁：本次 staged 未通过（CMNT-C）", file=sys.stderr)
  print(f"   范围：{py_n} 个 Python · {ts_n} 个 TypeScript\n", file=sys.stderr)

  buckets = _classify_errors(errors)
  for lvl in ("P0", "P1", "P2", "P3", "其他"):
    if lvl not in buckets:
      continue
    print(f"── {lvl} 违规 ({len(buckets[lvl])} 条)", file=sys.stderr)
    for e in buckets[lvl]:
      print(f"   · {e}", file=sys.stderr)
    print(file=sys.stderr)

  print("── 必要性说明（为何拦截）", file=sys.stderr)
  seen: set[str] = set()
  for err in errors:
    for needle, lvl, why in _VIOLATION_HINTS:
      if needle.lower() in err.lower() and why not in seen:
        print(f"   [{lvl}] {why}", file=sys.stderr)
        seen.add(why)
  print(file=sys.stderr)


def _prompt(question: str) -> bool:
  try:
    ans = input(f"{question} [y/N]: ").strip().lower()
  except (EOFError, KeyboardInterrupt):
    print("\n已取消。", file=sys.stderr)
    return False
  return ans in ("y", "yes", "是")


def _git_add(paths: list[Path]) -> None:
  if not paths:
    return
  rels = []
  for p in paths:
    try:
      rels.append(p.relative_to(cgg.ROOT).as_posix())
    except ValueError:
      rels.append(p.as_posix())
  subprocess.run(["git", "add", *rels], cwd=cgg.ROOT, check=False)


def _apply_staged_fix(py: list[Path], ts: list[Path]) -> list[str]:
  changed: list[str] = []
  for path in [*py, *ts]:
    ok = cfl.fix_python_file(path) if path.suffix == ".py" else cfl.fix_ts_file(path)
    if ok:
      changed.append(path.relative_to(cgg.ROOT).as_posix())
  return changed


def run_commit_hook(*, interactive: bool | None = None) -> int:
  """pre-commit 入口。interactive=None 时按 isatty 判断。"""
  errors, py_n, ts_n = run_check("staged")
  if not errors:
    print("Comment gate OK (staged interactive)")
    return 0

  _print_report(errors, py_n, ts_n)

  is_tty = interactive if interactive is not None else sys.stdin.isatty()
  if not is_tty:
    print(
      "非交互终端：仅拦截，不自动补全。请本地执行：",
      file=sys.stderr,
    )
    print("  uv run python scripts/comment_fix.py --staged --apply", file=sys.stderr)
    return 1

  print(
    "将插入【注释骨架】（关键词齐全），业务语义须你稍后润色。",
    file=sys.stderr,
  )
  if not _prompt("是否自动补齐注释骨架"):
    print(
      "已拒绝自动补全。请手改或 comment_fix --staged --apply 后重新 commit。",
      file=sys.stderr,
    )
    return 1

  py, ts = cgg.filter_gate_paths(cgg.git_staged_relpaths())
  patched = _apply_staged_fix(py, ts)
  if not patched:
    print("未产生可写改动（可能需手改）。", file=sys.stderr)
    return 1

  print("\n已补全文件：", file=sys.stderr)
  for rel in patched:
    print(f"   · {rel}", file=sys.stderr)

  _git_add([cgg.ROOT / r for r in patched])

  if not _prompt("确认将以上补全纳入本次 commit"):
    print("已取消。请 git add / git restore 后重新 commit。", file=sys.stderr)
    return 1

  errors2, _, _ = run_check("staged")
  if errors2:
    print("\n补全后仍有违规（需人工处理）：", file=sys.stderr)
    for e in errors2[:20]:
      print(f"   · {e}", file=sys.stderr)
    return 1

  print("\n✅ 注释骨架已补齐并通过复检，commit 继续。", file=sys.stderr)
  return 0


def main() -> int:
  import argparse

  p = argparse.ArgumentParser(description="Interactive comment gate for git commit")
  p.add_argument("--non-interactive", action="store_true", help="force block-only mode")
  args = p.parse_args()
  return run_commit_hook(interactive=False if args.non_interactive else None)


if __name__ == "__main__":
  sys.exit(main())
