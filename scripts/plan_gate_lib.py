"""确认规划绝对门禁（plan.ok / test.ok / code.ok ↔ workflow_state）。

作用：Hook 与 gate CLI 的机械真源；不依赖 Agent 自报 phase。
业务关联：L1「确认规划」→ gate plan ·「可以开始」→ gate start。
上游：check_pipeline · gate_cli · protect-paths hook
下游：阻断无 stamp 写码 / 伪造 workflow_state 升 phase
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"
GATES_DIR = PIPELINE / ".gates"
STATE_FILE = PIPELINE / "workflow_state.md"
PLAN_GATE = GATES_DIR / "plan.ok"
TEST_GATE = GATES_DIR / "test.ok"
CODE_GATE = GATES_DIR / "code.ok"

PHASE_ORDER = ("STEP0", "PLANNING", "CAN_TEST", "CAN_CODE", "DELIVERY")
BLOCKED_WITHOUT_PLAN = frozenset({"STEP0", "PLANNING"})
EMPTY_PLAN_TOKENS = frozenset({"", "null", "None", "~", "—", "-"})
CODE_PHASES = frozenset({"CAN_CODE", "DELIVERY"})


def read_workflow_state() -> dict[str, str]:
  """解析 workflow_state.md yaml 块内键值。"""
  if not STATE_FILE.is_file():
    return {}
  return parse_state_yaml(STATE_FILE.read_text(encoding="utf-8"))


def parse_state_yaml(text: str) -> dict[str, str]:
  """从 markdown 文本解析 workflow yaml 块。"""
  out: dict[str, str] = {}
  for key in ("phase", "agent", "step", "plan", "test_plan"):
    m = re.search(rf"^{key}:\s*(.*)$", text, re.MULTILINE)
    if not m:
      continue
    value = m.group(1).strip()
    if value and value not in EMPTY_PLAN_TOKENS:
      out[key] = value
  return out


def parse_gate_stamp(path: Path) -> dict[str, str] | None:
  """读取 .gates/*.ok 键值对；不存在返回 None。"""
  if not path.is_file():
    return None
  out: dict[str, str] = {}
  for line in path.read_text(encoding="utf-8").splitlines():
    if "=" in line:
      k, v = line.split("=", 1)
      out[k.strip()] = v.strip()
  return out or None


def parse_plan_ok() -> dict[str, str] | None:
  return parse_gate_stamp(PLAN_GATE)


def parse_test_ok() -> dict[str, str] | None:
  return parse_gate_stamp(TEST_GATE)


def parse_code_ok() -> dict[str, str] | None:
  return parse_gate_stamp(CODE_GATE)


def resolve_plan_path(state: dict[str, str]) -> Path | None:
  """workflow_state.plan → 仓库内 Path；无效返回 None。"""
  raw = state.get("plan", "").strip()
  if raw in EMPTY_PLAN_TOKENS:
    return None
  path = Path(raw)
  if not path.is_absolute():
    path = ROOT / path
  return path


def resolve_test_plan_path(state: dict[str, str]) -> Path | None:
  """workflow_state.test_plan → Path。"""
  raw = state.get("test_plan", "").strip()
  if raw in EMPTY_PLAN_TOKENS:
    return None
  path = Path(raw)
  if not path.is_absolute():
    path = ROOT / path
  return path


def invalidate_downstream_stamps(*, through: str = "plan") -> None:
  """plan/test 重盖章时作废下游 stamp（防旧轮次误用）。"""
  if through in ("plan", "test"):
    if CODE_GATE.is_file():
      CODE_GATE.unlink()
  if through == "plan":
    if TEST_GATE.is_file():
      TEST_GATE.unlink()


def write_plan_gate_stamp(plan_rel: str) -> None:
  """gate plan 成功后写入 plan.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  invalidate_downstream_stamps(through="plan")
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  PLAN_GATE.write_text(f"plan={plan_rel}\nat={ts}\n", encoding="utf-8")


def write_test_gate_stamp(*, plan_rel: str, test_plan_rel: str) -> None:
  """gate test 成功后写入 test.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  invalidate_downstream_stamps(through="test")
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  TEST_GATE.write_text(
    f"plan={plan_rel}\ntest_plan={test_plan_rel}\nat={ts}\n",
    encoding="utf-8",
  )


def write_code_gate_stamp(*, plan_rel: str, step: int) -> None:
  """gate start 成功后写入 code.ok（用户「可以开始」后的机械凭证）。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  CODE_GATE.write_text(
    f"plan={plan_rel}\nstep={step}\nat={ts}\n",
    encoding="utf-8",
  )


def clear_code_gate_stamp() -> None:
  """Step 验收后作废 code.ok，下一 Step 须重新 gate start。"""
  if CODE_GATE.is_file():
    CODE_GATE.unlink()


def _stamp_plan_matches_state(gate: dict[str, str], state: dict[str, str]) -> list[str]:
  errors: list[str] = []
  state_rel = state.get("plan", "")
  gated = gate.get("plan", "")
  if gated not in ("latest", state_rel):
    errors.append(
      "绝对门禁：plan stamp 与 workflow_state.plan 不一致 — "
      f"stamp={gated!r} state.plan={state_rel!r}；须重新 ./scripts/gate plan"
    )
  return errors


def validate_plan_stamp() -> list[str]:
  """机械「确认规划」：仅认 plan 文件 + plan.ok，不看 phase。

  返回：错误列表；空 = 通过
  """
  errors: list[str] = []
  state = read_workflow_state()
  plan_path = resolve_plan_path(state)
  if plan_path is None:
    errors.append(
      "绝对门禁：workflow_state.plan 未填写 — 无规划禁止写 src 代码"
    )
  elif not plan_path.is_file():
    errors.append(f"绝对门禁：plan 文件不存在 — {state.get('plan')}")

  gate = parse_plan_ok()
  if gate is None:
    errors.append(
      "绝对门禁：缺少 _factoryos_pipeline/.gates/plan.ok — "
      "须用户「确认规划」后执行 ./scripts/gate plan（Agent 禁止自写 stamp）"
    )
  elif plan_path is not None:
    errors.extend(_stamp_plan_matches_state(gate, state))
  return errors


def validate_test_stamp() -> list[str]:
  """机械 Test 就绪：plan.ok + test.ok + test_plan 文件。"""
  errors = validate_plan_stamp()
  state = read_workflow_state()
  test_path = resolve_test_plan_path(state)
  if test_path is None:
    errors.append(
      "绝对门禁：workflow_state.test_plan 未填写 — 须 Test 落 test-plan"
    )
  elif not test_path.is_file():
    errors.append(f"绝对门禁：test-plan 不存在 — {state.get('test_plan')}")

  gate = parse_test_ok()
  if gate is None:
    errors.append(
      "绝对门禁：缺少 _factoryos_pipeline/.gates/test.ok — "
      "须 ./scripts/gate test 绿后再「可以开始」"
    )
  else:
    errors.extend(_stamp_plan_matches_state(gate, state))
    state_tp = state.get("test_plan", "")
    gated_tp = gate.get("test_plan", "")
    if gated_tp != state_tp:
      errors.append(
        "绝对门禁：test.ok 与 workflow_state.test_plan 不一致 — "
        f"test.ok={gated_tp!r} state.test_plan={state_tp!r}；须重新 ./scripts/gate test"
      )
  return errors


def validate_code_stamp(*, step: int) -> list[str]:
  """机械「可以开始 Step N」：须 test 链 + code.ok step 对齐。"""
  errors = validate_test_stamp()
  state = read_workflow_state()
  gate = parse_code_ok()
  if gate is None:
    errors.append(
      "绝对门禁：缺少 _factoryos_pipeline/.gates/code.ok — "
      f"须用户「可以开始」后执行 ./scripts/gate start --step {step}"
    )
    return errors

  errors.extend(_stamp_plan_matches_state(gate, state))
  gated_step = gate.get("step", "")
  if str(gated_step) != str(step):
    errors.append(
      "绝对门禁：code.ok step 与 workflow_state.step 不一致 — "
      f"code.ok step={gated_step!r} state.step={step}；"
      f"须 ./scripts/gate start --step {step}"
    )
  return errors


def validate_src_test_write() -> list[str]:
  """写 src/tests/** 前：须 plan.ok（确认规划）。"""
  return validate_plan_stamp()


def validate_src_business_write(*, step: int) -> list[str]:
  """写业务码/迁移前：须 plan + test + code stamp。"""
  return validate_code_stamp(step=step)


def validate_workflow_state_content(text: str) -> list[str]:
  """校验 workflow_state 编辑结果：禁止无 stamp 升到 CAN_TEST/CAN_CODE。"""
  errors: list[str] = []
  new_state = parse_state_yaml(text)
  new_phase = new_state.get("phase", "STEP0")

  if new_phase in ("CAN_TEST", "CAN_CODE", "DELIVERY"):
    errors.extend(validate_plan_stamp())

  if new_phase in ("CAN_CODE", "DELIVERY"):
    errors.extend(validate_test_stamp())

  if new_phase == "CAN_CODE":
    try:
      step_n = int(new_state.get("step", "1") or "1")
    except ValueError:
      errors.append(f"绝对门禁：workflow_state step 非法 — {new_state.get('step')!r}")
      step_n = 1
    errors.extend(validate_code_stamp(step=step_n))

  return errors


def validate_plan_confirmed(
  *,
  require_phase_min: str = "CAN_TEST",
) -> list[str]:
  """绝对门禁：plan stamp + phase 下限（CLI 用；Hook 写码优先用 stamp 函数）。"""
  errors = validate_plan_stamp()
  state = read_workflow_state()
  phase = state.get("phase", "STEP0")

  if phase in BLOCKED_WITHOUT_PLAN:
    errors.append(
      f"绝对门禁：phase={phase} — 须 Step0 后「确认规划」+ ./scripts/gate plan，禁止跳过"
    )

  if require_phase_min in PHASE_ORDER and phase in PHASE_ORDER:
    if PHASE_ORDER.index(phase) < PHASE_ORDER.index(require_phase_min):
      errors.append(
        f"绝对门禁：phase={phase} 未达到 {require_phase_min} — "
        "须按关键词顺序：确认规划 → gate plan → gate test → 可以开始 → gate start"
      )

  return errors


def format_plan_gate_errors(errors: list[str]) -> str:
  """合并错误为单行提示（Hook / CLI 用）。"""
  return " | ".join(errors)
