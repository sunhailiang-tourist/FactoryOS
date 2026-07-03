# 测试用例与改动面：W5 agent FSM stub · Harness 确认门 failing tests

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **命名**：`test-1142-w5-agent-harness.md`（HHmm=1142 落盘当下本地时间）
- **目的**：新增 · W5 Step1～4 failing tests（H-01 · H-02 · H-03 · workflow Step1 · 存量回归）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_agent_orchestrator_w5_step1.py` | 新增 | Step1 内核 `create_plan` stub |
| `src/tests/integration/test_harness_w5.py` | 新增 | H-01 plan · H-02 confirm · H-03 audit 链 |
| `src/tests/ac/test_base001_registry.py` | 修改 | H-01～H-03 移出 pending 池 |

## 2. AC 用例

| ID | 标题 | 类型 | Step | 期望 |
|----|------|------|------|------|
| workflow | create_plan 内核 stub | integration | 1 | `agent_orchestrator.create_plan` → DslPlan |
| H-01 | 感知→计划 | integration | 2 | POST `/v1/agent/plan` · 不执行 · Legacy write=0 |
| H-02 | 确认门 | integration | 3 | plan → confirm → ExecutionRecord · 未确认不写 |
| H-03 | Harness 全链路 audit | integration | 4 | confirm 后 audit 含 plan/exec 关联 |
| G/R/E/B/C 存量 | W1–W4 | 回归 | 每 Step | `pytest -m 'not pending'` |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'workflow'
./scripts/gate step --step 2 -k 'H-01'
./scripts/gate step --step 3 -k 'H-02'
./scripts/gate step --step 4 -k 'H-03'
```

## 4. 标准测试用例

| ID | 标题 | 前置 | 步骤摘要 | 期望 |
|----|------|------|----------|------|
| Step1 | create_plan | migrated_db · frozen graph | 内核 `create_plan(intent=…)` | DslPlan · steps≥1 |
| H-01 | agent plan | frozen graph | POST `/v1/agent/plan` | 200 · DslPlan required · mock write=0 |
| H-02 | confirm gate | H-01 plan_id | POST `/v1/harness/confirm` confirmed=true | 200 · ExecutionRecord |
| H-03 | audit trail | H-02 exec_id | GET `/v1/audit/events` | harness.confirmed + execute.* |

### DB 策略

- 延续 W1–W4：`TEST_DATABASE_URL` 或 SQLite + Alembic upgrade head
- Step1 内核测经 `os_core.agent_orchestrator` 公开 API
- H-* 走 HTTP + `frozen_graph_env` fixture

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-0330-w5-agent-harness.md` ✓ |
| Step 范围 | 1 workflow → 2 H-01 → 3 H-02 → 4 H-03 ✓ |
| 不在 W5 | perception 501 · M/T 全量 · 52 其余 pending ✓ |
| 必测 | H-01～H-03 · workflow Step1 · 存量 77 回归 |
| 公共链路风险 | **高** — agent 写路径 · Harness 确认门 · execution 接线 |
| 红线 | R-01 Agent 禁写 Legacy · R-11 确认前禁止 execute |

## Gate A–G 摘要

| Gate | 结论 |
|------|------|
| A 复盘 | agent_orchestrator · harness confirm · OpenAPI v1.1 四端点 |
| B 目的 | **新增** — W5 failing tests 驱动红→绿 |
| C 协作 | plan：agent/harness modules · DslPlan · 4 Step |
| D 质量 | 待 Dev 实现后单步评估 |
| E 接口 | 见下节 |
| F 字段 | DslPlan · HarnessConfirmRequest · ExecutionRecord 响应 |
| G 命名 | test-1142 与落盘时间一致 ✓ |

## 📦 本次新增接口

```json
POST /v1/agent/plan
POST /v1/harness/confirm
```

## 🔁 本次需求涉及到的接口（字段调整）

**POST `/v1/agent/plan` 入参**：

```json
{
  "tenant_id": "default",
  "graph_id": "graph-fixture-abc",
  "graph_version": "v1.0.0",
  "intent": "report work order wo-h01 completed qty 1"
}
```

**POST `/v1/agent/plan` 出参（DslPlan）**：

```json
{
  "plan_id": "00000000-0000-4000-8000-000000000001",
  "tenant_id": "default",
  "graph_id": "graph-fixture-abc",
  "graph_version": "v1.0.0",
  "source": "agent",
  "steps": [{ "verb": "WORK_REPORT", "params": { "work_order_id": "wo-h01" } }],
  "created_at": "2026-06-30T03:00:00Z",
  "expires_at": "2026-06-30T04:00:00Z",
  "dry_run": false
}
```

**POST `/v1/harness/confirm` 入参**：

```json
{
  "plan_id": "00000000-0000-4000-8000-000000000001",
  "confirmed": true,
  "user_id": "operator-1",
  "dry_run": true
}
```

**POST `/v1/harness/confirm` 出参（确认后）**：

```json
{
  "exec_id": "00000000-0000-4000-8000-000000000002",
  "status": "simulated",
  "verb": "WORK_REPORT",
  "dry_run": true
}
```
