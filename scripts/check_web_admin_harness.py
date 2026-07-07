#!/usr/bin/env python3
"""Backward-compatible wrapper → src/apps/web-admin/scripts/check_harness.py"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "src" / "apps" / "web-admin" / "scripts" / "check_harness.py"
env = {**dict(__import__("os").environ), "FACTORYOS_ROOT": str(ROOT)}
sys.exit(subprocess.run([sys.executable, str(HARNESS)], cwd=HARNESS.parent.parent, env=env).returncode)
