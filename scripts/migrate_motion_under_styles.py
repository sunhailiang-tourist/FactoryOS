#!/usr/bin/env python3
"""将 src/motion 迁入 src/styles/motion（保持子目录结构）。"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src/apps/web-admin"
SRC = APP / "src"
OLD = SRC / "motion"
NEW = SRC / "styles/motion"

REPLACEMENTS = [
  ("src/apps/web-admin/src/motion/", "src/apps/web-admin/src/styles/motion/"),
  ("@/motion/presets", "@/styles/motion/presets"),
  ("@/motion", "@/styles/motion"),
  ("from '@/motion'", "from '@/styles/motion'"),
  ("`motion/presets.ts`", "`styles/motion/presets.ts`"),
  ("motion/presets.ts", "styles/motion/presets.ts"),
  ("motion/contracts/README.md", "styles/motion/contracts/README.md"),
  ("上游：motion/", "上游：styles/motion/"),
  ("| `motion/` | animate 白名单 |", "| `styles/motion/` | animate 白名单（styles 子目录） |"),
  ("- `motion/` | animate 白名单", "- `styles/motion/` | animate 白名单（见 styles/README）"),
  ("├── motion/", "│   └── motion/                   # animate 白名单（styles 子目录）"),
  ("    ├── motion/                         # animate 白名单", "    │   └── motion/                   # animate 白名单"),
  ("| `motion` | `presets.ts` | 契约 `motion/contracts/README.md` |", "| `styles/motion` | `presets.ts` | 契约 `styles/motion/contracts/README.md` |"),
  ("· @/motion", "· @/styles/motion"),
  ("@/motion`", "@/styles/motion`"),
  ("- src/apps/web-admin/src/motion", "- src/apps/web-admin/src/styles/motion"),
]

DOC_GLOBS = [
  APP / "ARCHITECTURE.md",
  APP / "ENGINEERING.md",
  APP / "README.md",
  APP / "src/README.md",
  APP / "src/components/README.md",
  APP / "src/styles/README.md",
  APP / "src/styles/contracts/README.md",
  ROOT / "contracts/directory-readmes.yaml",
  ROOT / "scripts/install_directory_readmes.py",
  ROOT / "templates/frontend-devkit/TEMPLATE.md",
]


def _apply_replacements(text: str) -> str:
  for old, new in REPLACEMENTS:
    text = text.replace(old, new)
  return text


def _patch_motion_readme_relatives(text: str) -> str:
  return text.replace("[ARCHITECTURE.md](../../ARCHITECTURE.md)", "[ARCHITECTURE.md](../../../ARCHITECTURE.md)").replace(
    "[ENGINEERING.md](../../ENGINEERING.md)", "[ENGINEERING.md](../../../ENGINEERING.md)"
  )


def main() -> int:
  if not OLD.is_dir():
    if NEW.is_dir():
      print("already migrated:", NEW.relative_to(ROOT))
      return 0
    raise SystemExit(f"missing {OLD}")

  if NEW.exists():
    shutil.rmtree(NEW)
  shutil.move(str(OLD), str(NEW))
  print("moved", OLD.relative_to(ROOT), "→", NEW.relative_to(ROOT))

  for path in NEW.rglob("*"):
    if path.is_file() and path.suffix in {".ts", ".tsx", ".md"}:
      text = path.read_text(encoding="utf-8")
      text = _apply_replacements(text)
      if path.name == "README.md":
        text = _patch_motion_readme_relatives(text)
      path.write_text(text, encoding="utf-8")

  for rel in ("pages/studio-shell/StudioHomePage.lazy.tsx", "styles/styles.test.ts"):
    path = SRC / rel
    if path.is_file():
      path.write_text(_apply_replacements(path.read_text(encoding="utf-8")), encoding="utf-8")
      print("patched", path.relative_to(ROOT))

  for doc in DOC_GLOBS:
    if not doc.is_file():
      continue
    doc.write_text(_apply_replacements(doc.read_text(encoding="utf-8")), encoding="utf-8")
    print("patched", doc.relative_to(ROOT))

  # styles/README：补充 motion 子路径说明
  styles_readme = APP / "src/styles/README.md"
  if styles_readme.is_file() and "styles/motion/" not in styles_readme.read_text(encoding="utf-8"):
    insert = "| `motion/` | animate 白名单 · MotionContainer · presets.ts |\n"
    styles_readme.write_text(
      styles_readme.read_text(encoding="utf-8").replace(
        "| `contracts/README.md` | 样式分层契约 |\n",
        "| `contracts/README.md` | 样式分层契约 |\n| `motion/` | animate 白名单 · MotionContainer |\n",
      ),
      encoding="utf-8",
    )
    print("patched styles/README table")

  yaml = ROOT / "contracts/directory-readmes.yaml"
  text = yaml.read_text(encoding="utf-8")
  if "src/apps/web-admin/src/styles/motion" not in text:
    text = text.replace("  - src/apps/web-admin/src/motion\n", "  - src/apps/web-admin/src/styles/motion\n")
    yaml.write_text(text, encoding="utf-8")

  if "motion" not in (ROOT / "contracts/directory-readmes.yaml").read_text():
    pass
  exempt_block = "  - modules\n  - kernel\n"
  if "  - motion\n" not in (ROOT / "contracts/directory-readmes.yaml").read_text():
    yaml.write_text(
      yaml.read_text(encoding="utf-8").replace(exempt_block, exempt_block + "  - motion\n"),
      encoding="utf-8",
    )
    print("added motion to exempt_dir_names")

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
