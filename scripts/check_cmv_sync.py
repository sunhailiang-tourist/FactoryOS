#!/usr/bin/env python3
"""Validate CMV注册表.yaml against DSL/Blueprint invariants (stdlib only).

Usage:
  python scripts/check_cmv_sync.py

Exit 0 = pass; 1 = validation errors.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMV_PATH = ROOT / "contracts" / "cmv" / "CMV注册表.yaml"

VERB_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
L0_LEVELS = {"L0"}
L2_LEVELS = {"L2", "L3"}


def parse_cmv_entries(text: str) -> list[dict]:
    """Minimal YAML subset parser for CMV verb list."""
    entries: list[dict] = []
    current: dict | None = None
    in_connector_ops = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("verbs:") or line.startswith("rules:") or line.startswith("apiVersion:"):
            in_connector_ops = False
            continue
        if re.match(r"^\s+- verb:", line):
            if current:
                entries.append(current)
            current = {"verb": line.split(":", 1)[1].strip(), "connector_ops": []}
            in_connector_ops = False
            continue
        if current is None:
            continue
        m = re.match(r"^\s+(\w+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if key == "connector_ops":
            in_connector_ops = True
            continue
        if in_connector_ops and key == "system":
            current["connector_ops"].append({"system": val})
            continue
        if in_connector_ops and key == "operation" and current["connector_ops"]:
            current["connector_ops"][-1]["operation"] = val
            continue
        if key in ("level", "compensator", "idempotent", "description"):
            if val == "null":
                current[key] = None
            elif val in ("true", "false"):
                current[key] = val == "true"
            else:
                current[key] = val
            in_connector_ops = False

    if current:
        entries.append(current)
    return entries


def validate(entries: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()

    for entry in entries:
        verb = entry.get("verb")
        if not verb:
            errors.append("entry missing verb")
            continue
        if verb in seen:
            errors.append(f"duplicate verb: {verb}")
        seen.add(verb)
        if not VERB_PATTERN.match(verb):
            errors.append(f"invalid verb name: {verb}")
        level = entry.get("level")
        compensator = entry.get("compensator")
        if level in L2_LEVELS and not compensator and not verb.endswith("_REVERT"):
            errors.append(f"L2 verb {verb} must declare compensator")
        if level in L0_LEVELS and compensator:
            errors.append(f"L0 verb {verb} must not have compensator")
        for op in entry.get("connector_ops") or []:
            if "system" not in op or "operation" not in op:
                errors.append(f"{verb}: connector_ops entry incomplete")

    verb_set = {e["verb"] for e in entries if "verb" in e}
    for entry in entries:
        comp = entry.get("compensator")
        if comp and comp not in verb_set:
            errors.append(f"{entry['verb']}: compensator {comp} not in registry")

    return errors


def main() -> int:
    if not CMV_PATH.exists():
        print(f"ERROR: missing {CMV_PATH}", file=sys.stderr)
        return 1
    text = CMV_PATH.read_text(encoding="utf-8")
    entries = parse_cmv_entries(text)
    errors = validate(entries)
    if errors:
        print("CMV validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"CMV OK: {len(entries)} verbs @ {CMV_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
