"""Backward-compatible re-export → devkit.frontend_contract_lib."""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
  sys.path.insert(0, str(_SCRIPTS))

from devkit.frontend_contract_lib import *  # noqa: F403
