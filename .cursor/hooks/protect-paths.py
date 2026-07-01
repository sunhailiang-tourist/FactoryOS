#!/usr/bin/env python3
"""Cursor preToolUse hook: SH-步步流路径保护（fail closed · stamp 绝对门禁）。

真源 stamp（仅 ./scripts/gate 可写）：
  plan.ok  ← gate plan（用户「确认规划」后）
  test.ok  ← gate test
  code.ok  ← gate start（用户「可以开始」后）

Agent 改 workflow_state 升 phase 须与 stamp 一致，否则 deny。
"""
from __future__ import annotations

import json
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
    pg = _load_plan_gate()
    return pg.read_workflow_state()


def norm_path(raw: str) -> str:
    p = raw.replace("\\", "/").lstrip("./")
    try:
        return str(Path(p).as_posix())
    except OSError:
        return p


def rel_to_repo(path: str) -> str:
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


def extract_tool_input(payload: dict) -> dict:
    tool_input = payload.get("tool_input") or payload.get("arguments") or {}
    return tool_input if isinstance(tool_input, dict) else {}


def is_always_ok(path: str) -> bool:
    if path in ALWAYS_OK_FILES:
        return True
    if path.endswith(".md") and not path.startswith("_factoryos_pipeline/"):
        return True
    return any(path.startswith(p) for p in ALWAYS_OK_PREFIXES)


def is_test_path(path: str) -> bool:
    return path.startswith("src/tests/")


def is_business_path(path: str) -> bool:
    if not path.endswith((".py", ".ts", ".tsx", ".sql")):
        return False
    return path.startswith(
        ("src/server/os_core/", "src/server/api/", "src/integration/")
    ) and not path.startswith("src/tests/")


def is_migration_path(path: str) -> bool:
    return (
        path.startswith("src/server/db/migrations/versions/")
        or path.startswith("alembic/versions/")
    ) and path.endswith(".py")


def is_src_code_path(path: str) -> bool:
    return path.startswith("src/") and path.endswith((".py", ".sql"))


def is_gate_stamp_path(path: str) -> bool:
    return path.startswith("_factoryos_pipeline/.gates/")


def is_workflow_state_path(path: str) -> bool:
    return path == "_factoryos_pipeline/workflow_state.md"


def is_plan_draft_path(path: str) -> bool:
    return "/plan/plan-" in path and path.endswith(".md")


def is_chain_pipeline_artifact(path: str) -> bool:
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
    return path.startswith("_factoryos_pipeline/")


def simulate_file_content(
    tool: str, path: str, tool_input: dict
) -> str | None:
    """模拟 Write/StrReplace 后的文件内容（workflow_state 校验用）。"""
    full = ROOT / path
    if tool == "Write":
        return tool_input.get("contents") or tool_input.get("content")
    if tool == "StrReplace" and full.is_file():
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        text = full.read_text(encoding="utf-8")
        if old not in text:
            return None
        return text.replace(old, new, 1)
    return None


def deny(user: str, agent: str) -> None:
    out = {
        "permission": "deny",
        "user_message": user,
        "agent_message": agent,
    }
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)


def check_step_chain(*, step: int, mode: str) -> list[str]:
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

    pg = _load_plan_gate()
    tool_input = extract_tool_input(payload)
    state = read_state()
    agent = state.get("agent", "dev")
    try:
        current_step = int(state.get("step", "1") or "1")
    except ValueError:
        current_step = 1

    # --- .gates stamp：仅 gate CLI（shell）可写 ---
    if is_gate_stamp_path(path):
        deny(
            "绝对门禁：_factoryos_pipeline/.gates/* 仅 ./scripts/gate 可写 — "
            "Agent 禁止伪造 plan.ok / test.ok / code.ok",
            "Run ./scripts/gate plan|test|start — never Write stamp files.",
        )
        return

    # --- workflow_state：升 phase 须 stamp 对齐 ---
    if is_workflow_state_path(path):
        if tool == "Delete":
            deny(
                "绝对门禁：禁止删除 workflow_state.md",
                "workflow_state is required.",
            )
            return
        simulated = simulate_file_content(tool, path, tool_input)
        if simulated is None:
            deny(
                "绝对门禁：无法校验 workflow_state 编辑 — fail closed",
                "Could not simulate workflow_state edit.",
            )
            return
        ws_errors = pg.validate_workflow_state_content(simulated)
        if ws_errors:
            deny(ws_errors[0], ws_errors[0])
            return
        print(json.dumps({"permission": "allow"}))
        return

    # --- plan 草稿：PLANNING 阶段允许 ---
    if is_plan_draft_path(path):
        print(json.dumps({"permission": "allow"}))
        return

    # --- 联动链落盘 ---
    if is_chain_pipeline_artifact(path):
        step_num = None
        try:
            sys.path.insert(0, str(SCRIPTS))
            import step_chain_lib

            step_num = step_chain_lib.parse_step_from_pipeline_path(path)
        except Exception:
            pass

        if path.startswith("_factoryos_pipeline/") and "step-stop-" in path:
            errors = pg.validate_code_stamp(step=step_num or current_step)
            if errors:
                deny(errors[0], errors[0])
                return
            if agent != "dev":
                deny(
                    "step-stop 须 Dev agent 落盘（workflow_state agent=dev）",
                    "Set agent=dev for step-stop.",
                )
                return
        elif step_num is not None and "-regression.md" in path and "final" not in path:
            errors = pg.validate_plan_stamp()
            if errors:
                deny(errors[0], errors[0])
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
            errors = pg.validate_plan_stamp()
            if errors:
                deny(errors[0], errors[0])
                return
            chain_errors = check_step_chain(step=step_num, mode="verify")
            if chain_errors:
                deny(chain_errors[0], chain_errors[0])
                return

        print(json.dumps({"permission": "allow"}))
        return

    # --- 其他 pipeline 落盘：须 plan.ok ---
    if is_pipeline_other(path):
        errors = pg.validate_plan_stamp()
        if errors:
            deny(errors[0], errors[0])
            return
        print(json.dumps({"permission": "allow"}))
        return

    if is_always_ok(path):
        print(json.dumps({"permission": "allow"}))
        return

    # --- src 测试代码：须 plan.ok（不看 phase）---
    if is_test_path(path):
        errors = pg.validate_src_test_write()
        if errors:
            deny(errors[0], errors[0])
            return
        print(json.dumps({"permission": "allow"}))
        return

    # --- 业务码 / 迁移：须 plan + test + code.ok ---
    if is_business_path(path) or is_migration_path(path):
        errors = pg.validate_src_business_write(step=current_step)
        if errors:
            deny(errors[0], errors[0])
            return
        chain_errors = check_step_chain(step=current_step, mode="start_dev")
        if chain_errors:
            deny(chain_errors[0], chain_errors[0])
            return
        print(json.dumps({"permission": "allow"}))
        return

    if is_src_code_path(path):
        deny(
            f"绝对门禁：未分类的 src 代码路径禁止写入 — {path}；"
            "须先「确认规划」+ gate plan",
            f"Blocked unclassified src path {path}.",
        )
        return

    print(json.dumps({"permission": "allow"}))


if __name__ == "__main__":
    main()
