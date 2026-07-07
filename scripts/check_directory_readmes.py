#!/usr/bin/env python3
"""Validate directory README manifest — 登记目录须有 README · 未登记目录须用户确认。

Usage:
  uv run python scripts/check_directory_readmes.py
"""
from __future__ import annotations

import sys

from directory_readme_lib import (
  format_report,
  validate_required_readmes,
  validate_unregistered_dirs,
)


def main() -> int:
  errors = validate_required_readmes() + validate_unregistered_dirs()
  print(format_report(errors))
  return 1 if errors else 0


if __name__ == "__main__":
  sys.exit(main())
