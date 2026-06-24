#!/usr/bin/env python3
"""依赖声明门禁：src/ 的 import 须在 pyproject.toml 中声明（deptry DEP001）。

失败时提示：uv add <pkg>  或  uv add --dev <pkg>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "deptry",
        "src",
        "--ignore",
        "DEP002,DEP003,DEP004,DEP005",
        "--optional-dependencies-dev-groups",
        "dev",
    ]
    print(f"\n── deptry (DEP001 · declared imports)\n  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(
            "\ndeptry FAILED — declare deps with: uv add <pkg>  or  uv add --dev <pkg>",
            file=sys.stderr,
        )
        return 1
    print("deptry OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
