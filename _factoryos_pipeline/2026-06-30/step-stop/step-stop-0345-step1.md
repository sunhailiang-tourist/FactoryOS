# Step 停机：Step 1 — agent_orchestrator 内核 stub + PlanStore

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 1 — agent_orchestrator 内核 stub · create_plan

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/agent_orchestrator/__init__.py` | 包入口 · 导出 create_plan/get_plan |
| `src/server/os_core/agent_orchestrator/service.py` | create_plan 薄 stub（**仅 shared_contracts**） |
| `src/server/os_core/agent_orchestrator/plan_store.py` | 进程内 PlanStore |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| workflow | 内部 `create_plan(...)` | ✅ pytest 绿 |

## 4. 架构修正（Test 阻断项）

| 项 | 处理 |
|----|------|
| import 边界 | 移除 `graph_service` / `rule_engine` import；Graph/Rule 校验改由 **API 层注入** `ruleset_id` · `allowed_dsl` |
| step-stop | 本文件落盘 |

## 5. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — agent 仅 shared_contracts + plan_store |
| 2 | 响应契约 | Pass |
| 3 | 鉴权/租户 | Pass |
| 4 | 红线 | Pass — 无 Legacy 写 |
| 5 | Schema | Pass |
| 6 | 输入校验 | Pass — allowed_dsl 可选校验 |
| 7 | Shadow | N/A |
| 8 | 幂等 | Pass |
| 9 | 静态 | Pass — import_boundaries OK |
| 10 | 注释 | Pass |

## 6. Harness 结果

```bash
uv run pytest src/tests/integration/test_agent_orchestrator_w5_step1.py -k workflow -q
uv run python scripts/check_import_boundaries.py
```

## 7. Verify

- 口令：`【Verify回合】Step 1`

## 8. 等待

Test 复验 → Verify → `可以继续`
