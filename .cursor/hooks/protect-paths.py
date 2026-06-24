#!/usr/bin/env python3
"""Cursor preToolUse hook: SH-步步流路径保护（fail closed）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / "_factoryos_pipeline" / "workflow_state.md"
PLAN_GATE = ROOT / "_factoryos_pipeline" / ".gates" / "plan.ok"

ALWAYS_OK_PREFIXES = (
    ".cursor/",
    "scripts/",
    "contracts/",
    "_factoryos_pipeline/",
    ".github/",
    "docs/",
)

ALWAYS_OK_FILES = {
    "pyproject.toml",
    "uv.lock",
    "README.md",
    "CODEOWNERS",
    ".pre-commit-config.yaml",
    ".gitignore",
}


def read_state() -> tuple[str, str]:
    if not STATE.is_file():
        return "STEP0", "dev"
    text = STATE.read_text(encoding="utf-8")
    phase_m = re.search(r"^phase:\s*(\S+)", text, re.MULTILINE)
    agent_m = re.search(r"^agent:\s*(\S+)", text, re.MULTILINE)
    return (
        phase_m.group(1) if phase_m else "STEP0",
        agent_m.group(1) if agent_m else "dev",
    )


def norm_path(raw: str) -> str:
    p = raw.replace("\\", "/").lstrip("./")
    try:
        return str(Path(p).as_posix())
    except OSError:
        return p


def extract_path(payload: dict) -> str | None:
    tool_input = payload.get("tool_input") or payload.get("arguments") or {}
    if isinstance(tool_input, dict):
        for key in ("path", "file_path", "target_file"):
            if key in tool_input:
                return norm_path(str(tool_input[key]))
    return None


def is_always_ok(path: str) -> bool:
    if path in ALWAYS_OK_FILES:
        return True
    if path.endswith(".md"):
        return True
    return any(path.startswith(p) for p in ALWAYS_OK_PREFIXES)


def is_test_path(path: str) -> bool:
    return path.startswith("src/tests/")


def is_business_path(path: str) -> bool:
    if not path.endswith((".py", ".ts", ".tsx", ".sql")):
        return False
    return path.startswith(
        ("src/os_core/", "src/apps/", "src/integration/")
    ) and not path.startswith("src/tests/")


def deny(user: str, agent: str) -> None:
    out = {
        "permission": "deny",
        "user_message": user,
        "agent_message": agent,
    }
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        deny("Hook 无法解析输入", "protect-paths hook JSON error")
        return

    tool = str(payload.get("tool_name") or payload.get("tool") or "")
    if tool not in ("Write", "StrReplace", "Delete", "ApplyPatch", "edit_file"):
        print(json.dumps({"permission": "allow"}))
        return

    path = extract_path(payload)
    if not path or is_always_ok(path):
        print(json.dumps({"permission": "allow"}))
        return

    phase, agent = read_state()

    if agent == "test":
        if is_test_path(path) or path.startswith("_factoryos_pipeline/"):
            print(json.dumps({"permission": "allow"}))
            return
        deny(
            f"Test Agent 仅可写 src/tests/** 与 _factoryos_pipeline/（当前试图写 {path}）",
            "Switch to Dev agent or update workflow_state agent=test only for tests.",
        )
        return

    if is_business_path(path) and phase != "CAN_CODE":
        deny(
            f"phase={phase}：未收到「可以开始」前禁止写业务代码（{path}）。"
            f"请更新 workflow_state → phase: CAN_CODE",
            f"Blocked {path}. Set phase CAN_CODE after user says 可以开始.",
        )
        return

    if is_test_path(path):
        if not PLAN_GATE.is_file():
            deny(
                "须先 ./scripts/gate plan（确认规划 + analyze）才能写 src/tests",
                "Run gate plan and stamp plan.ok before editing tests.",
            )
            return
        if phase not in ("CAN_TEST", "CAN_CODE", "DELIVERY"):
            deny(
                f"phase={phase}：需「确认规划」后 Test 才可写 src/tests（{path}）",
                "Set phase CAN_TEST after 确认规划.",
            )
            return

    print(json.dumps({"permission": "allow"}))


if __name__ == "__main__":
    main()
