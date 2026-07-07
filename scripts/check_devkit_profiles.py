#!/usr/bin/env python3
"""Umbrella harness：运行 devkit.manifest.yaml 登记的全部 App Profile。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "devkit" / "run_profiles.py"
venv_py = ROOT / ".venv" / "bin" / "python"
python = str(venv_py) if venv_py.is_file() else sys.executable
sys.exit(subprocess.run([python, str(HARNESS), "--root", str(ROOT)], cwd=ROOT).returncode)
