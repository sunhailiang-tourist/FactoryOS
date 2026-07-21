"""WEB 轨 stamp 绝对门禁（独立于 FactoryOS gate）。

作用：materials.ok / plan.ok / test.ok / code.ok ↔ _web_pipeline/workflow_state.md
业务关联：WEB-步步流 L4；迁出后仍可用，不依赖仓库根 ./scripts/gate
上游：web_gate_cli · protect-paths（WEB 分支）· WebDev
下游：阻断无 stamp 写 plan / App src
关联文档：.cursor/factoryos/WEB-GATES.md · WEB-HARNESS-EVAL.md
"""
from __future__ import annotations

import re
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
PIPELINE = APP_ROOT / "_web_pipeline"
GATES_DIR = PIPELINE / ".gates"
STATE_FILE = PIPELINE / "workflow_state.md"
MATERIALS_GATE = GATES_DIR / "materials.ok"
PLAN_GATE = GATES_DIR / "plan.ok"
TEST_GATE = GATES_DIR / "test.ok"
CODE_GATE = GATES_DIR / "code.ok"

EMPTY = frozenset({"", "null", "None", "~", "—", "-"})


def read_workflow_state() -> dict[str, str]:
  """解析 WEB workflow_state yaml 块。"""
  if not STATE_FILE.is_file():
    return {}
  return parse_state_yaml(STATE_FILE.read_text(encoding="utf-8"))


def parse_state_yaml(text: str) -> dict[str, str]:
  """从 markdown 解析键值。"""
  out: dict[str, str] = {}
  for key in ("phase", "agent", "step", "plan", "test_plan", "materials"):
    m = re.search(rf"^{key}:\s*(.*)$", text, re.MULTILINE)
    if not m:
      continue
    value = m.group(1).strip()
    if key == "materials" and value.lower() in ("na", "n/a"):
      out[key] = "na"
      continue
    if value and value not in EMPTY:
      out[key] = value
  return out


def parse_gate_stamp(path: Path) -> dict[str, str] | None:
  """读取 .gates/*.ok。"""
  if not path.is_file():
    return None
  out: dict[str, str] = {}
  for line in path.read_text(encoding="utf-8").splitlines():
    if "=" in line:
      k, v = line.split("=", 1)
      out[k.strip()] = v.strip()
  return out or None


def resolve_under_app(raw: str) -> Path:
  """相对 App 根解析路径。"""
  path = Path(raw)
  if not path.is_absolute():
    path = APP_ROOT / path
  return path


def invalidate_downstream(*, through: str = "plan") -> None:
  """上游重盖章作废下游。"""
  if through in ("materials", "plan", "test") and CODE_GATE.is_file():
    CODE_GATE.unlink()
  if through in ("materials", "plan") and TEST_GATE.is_file():
    TEST_GATE.unlink()
  if through == "materials" and PLAN_GATE.is_file():
    PLAN_GATE.unlink()


def write_materials_gate_stamp(
  *,
  materials_rel: str | None = None,
  mode: str = "file",
  reason: str = "",
) -> None:
  """写入 materials.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  invalidate_downstream(through="materials")
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  if mode == "na":
    MATERIALS_GATE.write_text(
      f"mode=na\nreason={reason or 'non-feature'}\nat={ts}\n",
      encoding="utf-8",
    )
    return
  MATERIALS_GATE.write_text(
    f"mode=file\nmaterials={materials_rel}\nat={ts}\n",
    encoding="utf-8",
  )


def write_plan_gate_stamp(plan_rel: str) -> None:
  """写入 plan.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  invalidate_downstream(through="plan")
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  PLAN_GATE.write_text(f"plan={plan_rel}\nat={ts}\n", encoding="utf-8")


def write_test_gate_stamp(*, plan_rel: str, test_plan_rel: str) -> None:
  """写入 test.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  invalidate_downstream(through="test")
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  TEST_GATE.write_text(
    f"plan={plan_rel}\ntest_plan={test_plan_rel}\nat={ts}\n",
    encoding="utf-8",
  )


def write_code_gate_stamp(*, plan_rel: str, step: int) -> None:
  """写入 code.ok。"""
  from datetime import datetime, timezone

  GATES_DIR.mkdir(parents=True, exist_ok=True)
  ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  CODE_GATE.write_text(
    f"plan={plan_rel}\nstep={step}\nat={ts}\n",
    encoding="utf-8",
  )


def clear_code_gate_stamp() -> None:
  """Step 验收后作废 code.ok。"""
  if CODE_GATE.is_file():
    CODE_GATE.unlink()


def validate_materials_stamp() -> list[str]:
  """须 materials.ok。"""
  errors: list[str] = []
  gate = parse_gate_stamp(MATERIALS_GATE)
  if gate is None:
    errors.append(
      "WEB绝对门禁：缺少 _web_pipeline/.gates/materials.ok — "
      "须「材料已齐」后执行 ./scripts/web_gate materials"
    )
    return errors
  if gate.get("mode") == "na":
    if not gate.get("reason"):
      errors.append("WEB绝对门禁：materials.ok mode=na 须含 reason")
    return errors
  raw = gate.get("materials", "").strip()
  if not raw:
    errors.append("WEB绝对门禁：materials.ok 缺少 materials=")
    return errors
  path = resolve_under_app(raw)
  if not path.is_file():
    errors.append(f"WEB绝对门禁：materials 文件不存在 — {raw}")
  return errors


def validate_materials_for_plan(plan_path: Path | None) -> list[str]:
  """gate plan 前置：新功能禁止 mode=na。"""
  errors = validate_materials_stamp()
  if plan_path is None or not plan_path.is_file():
    return errors
  text = plan_path.read_text(encoding="utf-8")
  type_m = re.search(r"\*\*类型\*\*[：:]\s*(.+)|^\s*[-*]\s*\*\*类型\*\*[：:]\s*(.+)", text, re.M)
  if not type_m:
    type_m = re.search(r"类型[：:]\s*(新功能|Bug|重构)", text)
  type_val = ""
  if type_m:
    type_val = next((g for g in type_m.groups() if g), "") or type_m.group(0)
  gate = parse_gate_stamp(MATERIALS_GATE) or {}
  if "新功能" in type_val and gate.get("mode") == "na":
    errors.append(
      f"{plan_path.name}: 类型=新功能 禁止 materials.ok mode=na — "
      "须 ./scripts/web_gate materials --materials <path>"
    )
  return errors


def validate_plan_stamp() -> list[str]:
  """须 plan.ok + plan 文件。"""
  errors: list[str] = []
  state = read_workflow_state()
  raw = state.get("plan", "")
  if not raw or raw in EMPTY:
    errors.append("WEB绝对门禁：workflow_state.plan 未填写")
  else:
    plan_path = resolve_under_app(raw)
    if not plan_path.is_file():
      errors.append(f"WEB绝对门禁：plan 不存在 — {raw}")
  gate = parse_gate_stamp(PLAN_GATE)
  if gate is None:
    errors.append(
      "WEB绝对门禁：缺少 plan.ok — 须「确认规划」后 ./scripts/web_gate plan"
    )
  elif raw and gate.get("plan") not in ("latest", raw):
    errors.append(
      "WEB绝对门禁：plan stamp 与 state 不一致 "
      f"stamp={gate.get('plan')!r} state={raw!r}"
    )
  return errors


def validate_test_stamp() -> list[str]:
  """须 test.ok。"""
  errors = validate_plan_stamp()
  if parse_gate_stamp(TEST_GATE) is None:
    errors.append("WEB绝对门禁：缺少 test.ok — 须 ./scripts/web_gate test")
  return errors


def validate_code_stamp(*, step: int | None = None) -> list[str]:
  """须 code.ok。"""
  errors = validate_test_stamp()
  gate = parse_gate_stamp(CODE_GATE)
  if gate is None:
    errors.append(
      "WEB绝对门禁：缺少 code.ok — 须「可以开始」后 ./scripts/web_gate start --step N"
    )
    return errors
  if step is not None and gate.get("step") and gate["step"] != str(step):
    errors.append(
      f"WEB绝对门禁：code.ok step={gate.get('step')} ≠ 请求 step={step}"
    )
  return errors


def validate_src_business_write(*, step: int = 1) -> list[str]:
  """写 App src 业务前：plan+test+code。"""
  return validate_code_stamp(step=step)


def ensure_pipeline_scaffold() -> None:
  """确保 _web_pipeline 骨架存在。"""
  for sub in ("plan", "test", "step-stop", "verify", "summary"):
    (PIPELINE / sub).mkdir(parents=True, exist_ok=True)
  GATES_DIR.mkdir(parents=True, exist_ok=True)
  readme = PIPELINE / "README.md"
  if not readme.is_file():
    readme.write_text(
      "# _web_pipeline\n\n"
      "WEB 独立落盘（禁止用 `_factoryos_pipeline` 代替）。\n\n"
      "stamp：`.gates/materials.ok|plan.ok|test.ok|code.ok` — 仅 `./scripts/web_gate` 可写。\n",
      encoding="utf-8",
    )
  if not STATE_FILE.is_file():
    STATE_FILE.write_text(
      "# WEB 工作流状态机\n\n"
      "> Agent 收到关键词后更新；stamp 仅 `./scripts/web_gate` 可写。\n\n"
      "```yaml\n"
      "phase: STEP0\n"
      "agent: web-dev\n"
      "step: 0\n"
      "plan: null\n"
      "test_plan: null\n"
      "materials: null\n"
      "updated: pending\n"
      "```\n",
      encoding="utf-8",
    )
