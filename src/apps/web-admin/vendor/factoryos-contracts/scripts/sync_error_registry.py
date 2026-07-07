#!/usr/bin/env python3
"""委托 App scripts/sync_error_registry.py（devkit.manifest sync_script 入口）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[3]
script = APP_ROOT / "scripts" / "sync_error_registry.py"
raise SystemExit(subprocess.call([sys.executable, str(script), *sys.argv[1:]]))
