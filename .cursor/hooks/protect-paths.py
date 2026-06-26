#!/usr/bin/env python3
"""Cursor preToolUse hook: SH-步步流路径保护（fail closed · 确认规划绝对门禁）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SCRIPTS = ROOT / "scripts"
STATE = ROOT / "_factoryos_pipeline" / "workflow_state.md"

ALWAYS_OK_PREFIXES = (
    ".cursor/",
    "scripts/",
    "contracts/",
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


def _load_plan_gate():
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    return plan_gate_lib


def read_state() -> dict[str, str]:
    if not STATE.is_file():
        return {}
    text = STATE.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for key in ("phase", "agent", "step", "plan", "test_plan"):
        m = re.search(rf"^{key}:\s*(.*)$", text, re.MULTILINE)
        if m:
            val = m.group(1).strip()
            if val:
                out[key] = val
    return out


def read_state_legacy() -> tuple[str, str]:
    s = read_state()
    return s.get("phase", "STEP0"), s.get("agent", "dev")


def norm_path(raw: str) -> str:
    p = raw.replace("\\", "/").lstrip("./")
    try:
        return str(Path(p).as_posix())
    except OSError:
        return p


def rel_to_repo(path: str) -> str:
    """绝对/相对路径 → 相对仓库根（Hook 判定用）。"""
    p = Path(path)
    try:
        if p.is_absolute():
            return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        pass
    return norm_path(path)


def extract_path(payload: dict) -> str | None:
    tool_input = payload.get("tool_input") or payload.get("arguments") or {}
    if isinstance(tool_input, dict):
        for key in ("path", "file_path", "target_file"):
            if key in tool_input:
                return rel_to_repo(str(tool_input[key]))
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


def is_migration_path(path: str) -> bool:
    return path.startswith("alembic/versions/") and path.endswith(".py")


def is_chain_pipeline_artifact(path: str) -> bool:
    """联动链落盘：不可被 always_ok 跳过。"""
    if not path.startswith("_factoryos_pipeline/"):
        return False
    name = Path(path).name
    if name.startswith("step-stop-"):
        return True
    if "-step" in name and name.endswith("-regression.md") and name.startswith("test-"):
        return True
    if name.startswith("verify-") and "-step" in name and name.endswith(".md"):
        return True
    return False


def is_pipeline_other(path: str) -> bool:
    """plan · summary · gate 机械日志等（非联动链）。"""
    return path.startswith("_factoryos_pipeline/")


def deny(user: str, agent: str) -> None:
    out = {
        "permission": "deny",
        "user_message": user,
        "agent_message": agent,
    }
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)


def check_plan_absolute(*, require_phase_min: str) -> list[str]:
    try:
        pg = _load_plan_gate()
        return pg.validate_plan_confirmed(require_phase_min=require_phase_min)
    except Exception as exc:  # noqa: BLE001 — hook fail-closed
        return [f"绝对门禁：plan 校验异常 — {exc}"]


def check_step_chain(*, step: int, mode: str) -> list[str]:
    """mode: start_dev | test_accept | verify | closed"""
    try:
        sys.path.insert(0, str(SCRIPTS))
        import step_chain_lib

        if mode == "start_dev":
            return step_chain_lib.validate_can_start_step_dev(step)
        if mode == "test_accept":
            return step_chain_lib.validate_step_dev_done(step)
        if mode == "verify":
            return step_chain_lib.validate_step_test_done(step, require_pass=True)
        if mode == "closed":
            return step_chain_lib.validate_step_chain_closed(step, require_pass=True)
        return [f"联动门禁：未知 mode={mode}"]
    except Exception as exc:  # noqa: BLE001
        return [f"联动门禁：校验异常 — {exc}"]


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
    if not path:
        print(json.dumps({"permission": "allow"}))
        return

    phase, agent = read_state_legacy()
    state = read_state()
    current_step = int(state.get("step", "1") or "1")

    # --- 联动链落盘（优先于 always_ok）---
    if is_chain_pipeline_artifact(path):
        step_num = None
        try:
            sys.path.insert(0, str(SCRIPTS))
            import step_chain_lib

            step_num = step_chain_lib.parse_step_from_pipeline_path(path)
        except Exception:
            pass

        if path.startswith("_factoryos_pipeline/") and "step-stop-" in path:
            # Dev step-stop：须 plan 已确认
            plan_errors = check_plan_absolute(require_phase_min="CAN_CODE")
            if plan_errors:
                deny(plan_errors[0], plan_errors[0])
                return
            if agent != "dev":
                deny(
                    "step-stop 须 Dev agent 落盘（workflow_state agent=dev）",
                    "Set agent=dev for step-stop.",
                )
                return
        elif step_num is not None and "-regression.md" in path and "final" not in path:
            plan_errors = check_plan_absolute(require_phase_min="CAN_TEST")
            if plan_errors:
                deny(plan_errors[0], plan_errors[0])
                return
            chain_errors = check_step_chain(step=step_num, mode="test_accept")
            if chain_errors:
                deny(chain_errors[0], chain_errors[0])
                return
            if agent != "test":
                deny(
                    f"Test·Step {step_num} 验收须 agent=test",
                    "Set agent=test for test step regression.",
                )
                return
        elif step_num is not None and "/verify/verify-" in path:
            plan_errors = check_plan_absolute(require_phase_min="CAN_TEST")
            if plan_errors:
                deny(plan_errors[0], plan_errors[0])
                return
            chain_errors = check_step_chain(step=step_num, mode="verify")
            if chain_errors:
                deny(chain_errors[0], chain_errors[0])
                return

        print(json.dumps({"permission": "allow"}))
        return

    if is_always_ok(path) or is_pipeline_other(path):
        print(json.dumps({"permission": "allow"}))
        return

    if agent == "test":
        rel = path if not path.startswith("/") else rel_to_repo(path)
        if is_test_path(rel) or rel.startswith("_factoryos_pipeline/"):
            plan_errors = check_plan_absolute(require_phase_min="CAN_TEST")
            if plan_errors:
                deny(plan_errors[0], plan_errors[0])
                return
            print(json.dumps({"permission": "allow"}))
            return
        deny(
            f"Test Agent 仅可写 src/tests/** 与 _factoryos_pipeline/（当前试图写 {path}）",
            "Switch to Dev agent or update workflow_state agent=test only for tests.",
        )
        return

    if is_business_path(path) or is_migration_path(path):
        plan_errors = check_plan_absolute(require_phase_min="CAN_CODE")
        if plan_errors:
            deny(plan_errors[0], plan_errors[0])
            return
        chain_errors = check_step_chain(step=current_step, mode="start_dev")
        if chain_errors:
            deny(chain_errors[0], chain_errors[0])
            return
        if phase != "CAN_CODE":
            deny(
                f"phase={phase}：未收到「可以开始」前禁止写业务代码（{path}）。"
                f"须先「确认规划」→ gate plan → 再「可以开始」",
                f"Blocked {path}. Need 确认规划 + gate plan + 可以开始 → CAN_CODE.",
            )
            return

    if is_test_path(path):
        plan_errors = check_plan_absolute(require_phase_min="CAN_TEST")
        if plan_errors:
            deny(plan_errors[0], plan_errors[0])
            return

    print(json.dumps({"permission": "allow"}))


if __name__ == "__main__":
    main()
