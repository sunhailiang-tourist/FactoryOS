#!/usr/bin/env python3
"""Generate .cursor/factoryos/PATH-SNAPSHOT.md from contracts/repo-structure.yaml.

Usage:
  uv run python scripts/gen_path_snapshot.py
  uv run python scripts/gen_path_snapshot.py --check   # fail if stale

Exit 0 = OK; 1 = stale or error.
"""
from __future__ import annotations

import argparse
import sys

from repo_structure import PATH_SNAPSHOT_MD, load_snapshot, render_path_snapshot_md, repo_root


def main() -> int:
  parser = argparse.ArgumentParser(description="Generate PATH-SNAPSHOT.md from repo-structure.yaml")
  parser.add_argument("--check", action="store_true", help="Fail if generated content differs from on-disk file")
  args = parser.parse_args()

  snapshot = load_snapshot()
  content = render_path_snapshot_md(snapshot)
  if not content.endswith("\n"):
    content += "\n"

  if args.check:
    if not PATH_SNAPSHOT_MD.is_file():
      print(f"FAIL: missing {PATH_SNAPSHOT_MD.relative_to(repo_root())}", file=sys.stderr)
      return 1
    if PATH_SNAPSHOT_MD.read_text(encoding="utf-8") != content:
      print(
        f"FAIL: {PATH_SNAPSHOT_MD.relative_to(repo_root())} stale — run: uv run python scripts/gen_path_snapshot.py",
        file=sys.stderr,
      )
      return 1
    print("OK: PATH-SNAPSHOT.md up to date")
    return 0

  PATH_SNAPSHOT_MD.parent.mkdir(parents=True, exist_ok=True)
  PATH_SNAPSHOT_MD.write_text(content, encoding="utf-8")
  print(f"Wrote {PATH_SNAPSHOT_MD.relative_to(repo_root())}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
