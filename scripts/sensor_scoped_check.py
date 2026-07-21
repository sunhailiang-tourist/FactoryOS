#!/usr/bin/env python3
"""编辑后 scoped 传感器（给 PostToolUse / 人工复用）。

作用：对刚改的业务 .py 做 py_compile + 可选 ruff；输出「给 LLM 的修复说明书」。
业务关联：L4 P1 Guides/Sensors — 错误信息即可执行下一步，而非仅报失败。
上游：.cursor/hooks/post-edit-sensor.py
下游：Agent 下一轮工具调用
关联文档：FAILURE-TAXONOMY.md · FT-SENSOR-LINT
"""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUSINESS_PREFIXES = (
  "src/server/os_core/",
  "src/server/api/",
  "src/integration/",
)


def is_business_py(rel: str) -> bool:
  """是否业务 Python 路径。"""
  norm = rel.replace("\\", "/")
  return norm.endswith(".py") and any(norm.startswith(p) for p in BUSINESS_PREFIXES)


def scoped_check(rel_path: str) -> tuple[bool, str]:
  """对单文件跑传感器。

  返回：(ok, message)。message 始终面向 LLM（含修复步骤）。
  """
  norm = rel_path.replace("\\", "/").lstrip("./")
  path = ROOT / norm
  if not path.is_file():
    return True, ""

  lines: list[str] = [
    f"【传感器 FT-SENSOR-LINT】已编辑 `{norm}`",
  ]
  ok = True

  try:
    py_compile.compile(str(path), doraise=True)
    lines.append("- py_compile: OK")
  except py_compile.PyCompileError as exc:
    ok = False
    lines.extend(
      [
        "- py_compile: FAIL",
        f"- 错误：{exc.msg}",
        "- 修复步骤：1) 打开上述文件定位行号 2) 修正语法 3) 保存后再继续实现",
        "- 禁止：忽略语法错误继续写其它文件",
      ]
    )

  ruff = ROOT / ".venv" / "bin" / "ruff"
  if not ruff.is_file():
    ruff_cmd = ["ruff"]
  else:
    ruff_cmd = [str(ruff)]
  try:
    proc = subprocess.run(
      [*ruff_cmd, "check", str(path)],
      cwd=str(ROOT),
      capture_output=True,
      text=True,
      timeout=30,
      check=False,
    )
  except (FileNotFoundError, subprocess.TimeoutExpired):
    lines.append("- ruff: 跳过（未安装或超时）")
  else:
    if proc.returncode == 0:
      lines.append("- ruff check: OK")
    else:
      ok = False
      out = (proc.stdout or proc.stderr or "").strip()[:1500]
      lines.extend(
        [
          "- ruff check: FAIL",
          "```",
          out or "(no output)",
          "```",
          "- 修复步骤：1) 按 ruff 提示改本文件 2) 可跑 "
          f"`ruff check {norm} --fix`（若安全）3) 再 `./scripts/harness --tier auto`",
          "- 税则回灌：若同类问题反复出现 → "
          "`python scripts/check_failure_taxonomy.py --codes FT-SENSOR-LINT`",
        ]
      )

  if ok:
    lines.append(
      "- 下一步建议：改完本 Step 后跑 `./scripts/harness --tier auto`；"
      "停机前确保 step-stop 含 UI字段对账 + 运行时证据"
    )
  return ok, "\n".join(lines)


def main() -> int:
  if len(sys.argv) < 2:
    print("Usage: sensor_scoped_check.py <rel/path.py>", file=sys.stderr)
    return 2
  rel = sys.argv[1]
  if not is_business_py(rel):
    print(f"skip non-business: {rel}")
    return 0
  ok, msg = scoped_check(rel)
  print(msg)
  return 0 if ok else 1


if __name__ == "__main__":
  raise SystemExit(main())
