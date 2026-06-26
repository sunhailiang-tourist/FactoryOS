"""确认规划绝对门禁（plan.ok ↔ workflow_state.plan）。

作用：任何编码/测试/step/delivery 前机械校验「确认规划」已完成。
业务关联：L1 关键词 `确认规划` + `./scripts/gate plan` 不可跳过。
上游：check_pipeline · gate_cli · Cursor protect-paths hook
下游：阻断无 plan 写码/跑 step
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"
STATE_FILE = PIPELINE / "workflow_state.md"
PLAN_GATE = PIPELINE / ".gates" / "plan.ok"

PHASE_ORDER = ("STEP0", "PLANNING", "CAN_TEST", "CAN_CODE", "DELIVERY")
BLOCKED_WITHOUT_PLAN = frozenset({"STEP0", "PLANNING"})
EMPTY_PLAN_TOKENS = frozenset({"", "null", "None", "~", "—"})


def read_workflow_state() -> dict[str, str]:
  """解析 workflow_state.md yaml 块内键值。"""
  if not STATE_FILE.is_file():
    return {}
  text = STATE_FILE.read_text(encoding="utf-8")
  out: dict[str, str] = {}
  for key in ("phase", "agent", "step", "plan", "test_plan"):
    m = re.search(rf"^{key}:\s*(.*)$", text, re.MULTILINE)
    if not m:
      continue
    value = m.group(1).strip()
    if value:
      out[key] = value
  return out


def parse_plan_ok() -> dict[str, str] | None:
  """读取 plan.ok 内容；不存在返回 None。"""
  if not PLAN_GATE.is_file():
    return None
  out: dict[str, str] = {}
  for line in PLAN_GATE.read_text(encoding="utf-8").splitlines():
    if "=" in line:
      k, v = line.split("=", 1)
      out[k.strip()] = v.strip()
  return out or None


def resolve_plan_path(state: dict[str, str]) -> Path | None:
  """workflow_state.plan → 仓库内 Path；无效返回 None。"""
  raw = state.get("plan", "").strip()
  if raw in EMPTY_PLAN_TOKENS:
    return None
  path = Path(raw)
  if not path.is_absolute():
    path = ROOT / path
  return path


def validate_plan_confirmed(
  *,
  require_phase_min: str = "CAN_TEST",
) -> list[str]:
  """绝对门禁：须用户「确认规划」且 `./scripts/gate plan` 已盖章。

  参数 require_phase_min：最低 phase（CAN_TEST=测·编码前 · CAN_CODE=写业务码）
  返回：错误列表；空列表表示通过
  """
  errors: list[str] = []
  state = read_workflow_state()
  phase = state.get("phase", "STEP0")

  if phase in BLOCKED_WITHOUT_PLAN:
    errors.append(
      f"绝对门禁：phase={phase} — 须 Step0 后「确认规划」+ ./scripts/gate plan，禁止跳过"
    )

  plan_path = resolve_plan_path(state)
  if plan_path is None:
    errors.append(
      "绝对门禁：workflow_state.plan 未填写 — 无规划禁止测试/编码/step/delivery"
    )
  elif not plan_path.is_file():
    errors.append(f"绝对门禁：plan 文件不存在 — {state.get('plan')}")

  gate = parse_plan_ok()
  if gate is None:
    errors.append(
      "绝对门禁：缺少 _factoryos_pipeline/.gates/plan.ok — "
      "须用户「确认规划」后执行 ./scripts/gate plan"
    )
  elif plan_path is not None:
    gated = gate.get("plan", "")
    state_rel = state.get("plan", "")
    if gated not in ("latest", state_rel):
      errors.append(
        "绝对门禁：plan.ok 与 workflow_state.plan 不一致 — "
        f"plan.ok={gated!r} state.plan={state_rel!r}；须重新 ./scripts/gate plan"
      )

  if require_phase_min in PHASE_ORDER and phase in PHASE_ORDER:
    if PHASE_ORDER.index(phase) < PHASE_ORDER.index(require_phase_min):
      errors.append(
        f"绝对门禁：phase={phase} 未达到 {require_phase_min} — "
        "须按关键词顺序：确认规划 → gate plan → 可以开始"
      )

  return errors


def format_plan_gate_errors(errors: list[str]) -> str:
  """合并错误为单行提示（Hook / CLI 用）。"""
  return " | ".join(errors)
