#!/usr/bin/env python3
"""Full-path consistency audit vs contracts/repo-structure.yaml (absolute gate helper).

Usage:
  uv run python scripts/audit_path_consistency.py

Exit 0 = no misleading path refs in scope; 1 = violations listed on stderr.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from repo_structure import (
  compile_allow_line,
  compile_forbidden_patterns,
  load_snapshot,
  repo_root,
)


def _iter_files(root: Path, snap) -> list[Path]:
  out: list[Path] = []
  binary_ext = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in snap.scan_binary_extensions}
  skip_parts = set(snap.scan_skip_path_parts)
  skip_files = set(snap.scan_skip_files)

  for name in snap.scan_roots:
    scan_root = root / name
    if not scan_root.is_dir():
      continue
    for p in scan_root.rglob("*"):
      if not p.is_file() or any(x in p.parts for x in skip_parts):
        continue
      rel = p.relative_to(root).as_posix()
      if rel in skip_files:
        continue
      if p.suffix.lower() in binary_ext:
        continue
      out.append(p)

  for rel in snap.scan_extra_root_files:
    p = root / rel
    if p.is_file() and rel not in skip_files:
      out.append(p)

  return sorted(set(out))


def main() -> int:
  root = repo_root()
  snap = load_snapshot()
  forbidden = compile_forbidden_patterns(snap)
  allow_line = compile_allow_line(snap)
  historical = set(snap.historical_files)
  semantic = [re.compile(p) for p in snap.semantic_forbidden]
  sem_prefixes = snap.semantic_scan_prefixes

  def _semantic_applies(rel: str) -> bool:
    if rel in historical:
      return False
    return any(rel.startswith(p) or rel == p.rstrip("/") for p in sem_prefixes)

  hits: list[str] = []
  read_ok = 0
  for p in _iter_files(root, snap):
    try:
      text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
      continue
    read_ok += 1
    rel = p.relative_to(root).as_posix()
    check_semantic = _semantic_applies(rel)
    for i, line in enumerate(text.splitlines(), 1):
      if allow_line and allow_line.search(line):
        continue
      for pat in forbidden:
        if pat.search(line):
          hits.append(f"{rel}:{i}: {line.strip()[:120]}")
          break
      else:
        if check_semantic:
          for pat in semantic:
            if pat.search(line):
              hits.append(f"{rel}:{i} [semantic]: {line.strip()[:120]}")
              break

  print(f"audit_path_consistency: read={read_ok} forbidden_hits={len(hits)}")
  if hits:
    for h in hits:
      print(f"  {h}", file=sys.stderr)
    return 1
  print("OK: no forbidden filesystem path refs in scope (snapshot-driven)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
