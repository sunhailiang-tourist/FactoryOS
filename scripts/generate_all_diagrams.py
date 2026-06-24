#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all FactoryOS architecture diagrams (SVG + PNG)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "generate_architecture_diagrams.py",
    "generate_base_capability_diagram.py",
]


def main() -> None:
    for name in SCRIPTS:
        path = ROOT / "scripts" / name
        print(f"--- {name} ---")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All diagrams generated.")


if __name__ == "__main__":
    main()
