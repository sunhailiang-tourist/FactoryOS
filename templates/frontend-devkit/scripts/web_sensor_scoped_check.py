#!/usr/bin/env python3
"""WEB 编辑后传感器：对 App src 下 ts/tsx 做基础检查并输出修复说明书。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]


def is_web_src(rel: str) -> bool:
  norm = rel.replace("\\", "/").lstrip("./")
  return (
    "/src/" in f"/{norm}"
    and norm.endswith((".ts", ".tsx", ".js", ".jsx", ".mjs"))
    and "node_modules" not in norm
  )


def scoped_check(rel_path: str) -> tuple[bool, str]:
  """返回 (ok, llm_message)。"""
  norm = rel_path.replace("\\", "/").lstrip("./")
  # 支持从 monorepo 根传入 src/apps/web-admin/src/...
  path = Path(norm)
  if not path.is_absolute():
    # try app-relative then repo-relative
    cand = APP_ROOT / norm
    if not cand.is_file() and norm.startswith("src/apps/"):
      # strip to after app name
      parts = norm.split("/")
      if len(parts) >= 4:
        cand = APP_ROOT / "/".join(parts[3:])
    path = cand
  if not path.is_file():
    return True, ""

  lines = [f"【WEB传感器 WFT-SENSOR-LINT】已编辑 `{norm}`"]
  ok = True
  # tsc 太重；优先 eslint --fix-dry-run 若存在
  eslint = APP_ROOT / "node_modules" / ".bin" / "eslint"
  if eslint.is_file():
    proc = subprocess.run(
      [str(eslint), str(path), "--max-warnings", "0"],
      cwd=str(APP_ROOT),
      capture_output=True,
      text=True,
      timeout=60,
      check=False,
    )
    if proc.returncode != 0:
      ok = False
      out = (proc.stdout or proc.stderr or "")[:1500]
      lines.extend(
        [
          "- eslint: FAIL",
          "```",
          out or "(no output)",
          "```",
          "- 修复：按 eslint 改本文件 → 再 `pnpm exec eslint <file>` → "
          "`./scripts/web_gate` / `check_harness`",
        ]
      )
    else:
      lines.append("- eslint: OK")
  else:
    lines.append("- eslint: 跳过（未 install）")
  if ok:
    lines.append(
      "- 下一步：本 Step 停机前填 step-stop「运行时证据」；"
      "改门禁后跑 `./scripts/web_gate harness-eval`"
    )
  return ok, "\n".join(lines)


def main() -> int:
  if len(sys.argv) < 2:
    print("Usage: web_sensor_scoped_check.py <path>", file=sys.stderr)
    return 2
  rel = sys.argv[1]
  if not is_web_src(rel) and "src/" not in rel.replace("\\", "/"):
    print(f"skip: {rel}")
    return 0
  ok, msg = scoped_check(rel)
  print(msg)
  return 0 if ok else 1


if __name__ == "__main__":
  raise SystemExit(main())
