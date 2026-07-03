# 预开发说明：W5 — agent FSM（薄）· Harness 确认门 · OpenAPI 对齐

- **日期**：2026-06-30
- **对照契约**：`contracts/openapi/工厂操作系统-v1.1.yaml` · `contracts/acceptance/验收用例-BASE-001-平台底座.md`（H-01～H-03）· `contracts/schemas/DslPlan.schema.json`
- **路线图**：`docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md` §五 W5
- **依赖 W4**：execution L2 真写 · rule evaluate · graph freeze · E-02/E-04 ✅

---

## 1. 迭代目标

**一句话**：LangGraph **薄 stub**（无真实 LLM）产出 `DslPlan`；HTTP **`/v1/agent/plan`** + **`/v1/harness/confirm`** 闭环；**未确认不写 Legacy**（Harness 确认门 · H-01）。

**可测要点**：BASE-001 **H-01 · H-02 · H-03**；OpenAPI v1.1 四端点 schema 对齐；W1–W4 存量回归不破坏。

**不在 W5**：真实 LiteLLM/ASR/OCR（留 W5+ perception）；UX-001 M/T 全量；52 P0 全绿（W6–W8）；钉钉/H5 前端。

---

## 2. AC 对账表

| AC ID | 标题 | 本迭代 | Step | 验证方式 |
|-------|------|--------|------|----------|
| H-01 | 感知→计划（仅 plan） | 是 | 2 | `-k 'H-01'` |
| H-02 | 确认门 plan→confirm→execute | 是 | 3 | `-k 'H-02'` |
| H-03 | Harness 全链路 audit | 是 | 4 | `-k 'H-03'` |
| G/R/E 存量 | W1–W4 | 回归 | 每 Step | `pytest -m 'not pending'` |

---

## 3. 红线对账

| 红线 | 本迭代涉及 | 负向测试 |
|------|------------|----------|
| REDLINES R01 Agent 禁写 Legacy | agent 只产 DslPlan | import_boundaries · H-01 Legacy 写计数 0 |
| REDLINES R11 Harness 确认门 | confirm 前禁止 execute | H-01 · 仅 plan 时 mock_legacy write=0 |
| REDLINES R02 Rule 默认 deny | confirm 后仍过 rule_engine | 沿用 W3 链 |
| REDLINES R03 非 frozen Graph | plan 须校验 graph 状态 | 409 负向（可选 Step 3） |

---

## 4. 接口清单

| 方法 | 路径 | 用途 | Step |
|------|------|------|------|
| POST | `/v1/agent/plan` | 意图 → DslPlan（不执行） | 2 |
| POST | `/v1/harness/confirm` | 确认 → Rule → Execute | 3 |
| POST | `/v1/execute` | 存量 direct execute | 回归 |
| GET | `/v1/dsl/registry` | 存量 D-01 | 回归 |

OpenAPI 预留、**W5 不实现**：`/v1/perception/voice` · `/v1/perception/image`（返回 501 或不在 router 注册）。

---

## 5. 模块与文件

| 模块 | 路径 | 变更 |
|------|------|------|
| agent_orchestrator | `src/server/os_core/agent_orchestrator/` | **新增** `service.py` · `plan_store.py` · stub FSM |
| harness（内核） | `src/server/os_core/agent_orchestrator/harness.py` 或同级 | confirm 编排（调 rule + execution） |
| API agent | `src/server/api/modules/agent/` | **新增** controllers · routers |
| API harness | `src/server/api/modules/harness/` | **新增** controllers · routers |
| router | `src/server/api/router/v1/registry.py` | 注册 agent · harness providers |
| 迁移（可选） | `src/server/db/migrations/versions/005_dsl_plans.py` | `dsl_plans` 表（若不用纯内存） |
| 测试 | `src/tests/integration/test_harness_h01*.py` 等 | 新增 |

> **结构说明**：在已有 `src/server/api/modules/` 下新增 **agent** · **harness** 子目录（非 src 主干变更，pre-commit 不拦）。

---

## 6. 分步计划

### Step 1 — `agent_orchestrator` 内核 stub + PlanStore

| 项 | 内容 |
|----|------|
| AC ID | workflow（内核） |
| 接口 | 内部 `create_plan(tenant_id, graph_id, graph_version, intent) -> DslPlan` |
| 模块路径 | `agent_orchestrator/service.py` · `plan_store.py` · `__init__.py` |
| Harness | `./scripts/gate step --step 1 -k 'workflow'` |
| 风险 | stub 动词须 ⊆ CMV；对齐 `DslPlan` Pydantic · 无 connector.write |

**stub 行为**：固定映射 `intent` 关键词 → 单步 `WORK_REPORT`（与 W4 mock graph 兼容）；**不调用 LiteLLM**。

### Step 2 — POST `/v1/agent/plan` + H-01（含确认门负向）

| 项 | 内容 |
|----|------|
| AC ID | H-01 |
| 接口 | POST `/v1/agent/plan` |
| 模块路径 | `modules/agent/` · 薄路由 → `agent_orchestrator` |
| Harness | `./scripts/gate step --step 2 -k 'H-01'` |
| 风险 | plan 入库后 `plan_id` UUID；确认前 `mock_legacy` 写计数必须为 0 |

### Step 3 — POST `/v1/harness/confirm` + H-02

| 项 | 内容 |
|----|------|
| AC ID | H-02 |
| 接口 | POST `/v1/harness/confirm`（`confirmed=true` → execute；`false` → audit reject） |
| 模块路径 | `modules/harness/` · `agent_orchestrator/harness.py` |
| Harness | `./scripts/gate step --step 3 -k 'H-02'` |
| 风险 | `dry_run=true` → simulated · 无 Legacy 写；须写 audit `harness.confirmed/rejected` |

### Step 4 — H-03 全链路 audit + 回归 + OpenAPI 对账

| 项 | 内容 |
|----|------|
| AC ID | H-03 |
| 接口 | GET `/v1/audit/events` 过滤 plan/exec |
| 模块路径 | 测试为主 · OpenAPI response schema 对账 |
| Harness | `./scripts/gate step --step 4 -k 'H-03'` |
| 风险 | pending AC 仍 20；仅 H-* 从 pending 摘出 |

---

## 7. Harness 验收盘（全局）

```bash
./scripts/gate step --step 4 -k 'H-03'
./scripts/gate delivery
./scripts/gate pr
```

---

## 8. Step 0 摘要（Dev 已核对）

| 维度 | 结论 |
|------|------|
| 写路径 | agent → DslPlan → harness/confirm → rule → execution → connector |
| 落点模块 | `agent_orchestrator`（L2）· `server/api` agent/harness 薄路由 |
| W1–W4 | 79 passed · harness 11/11 · 路径快照 D14 |
| DB | 现有 001–004 migrations；Step1 决定 005 或内存 PlanStore |
| 缺口 | 无 A 类；perception 端点刻意延后 |

---

## 9. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1.0 | 2026-06-30 | 初版：W5 agent stub + harness confirm · H-01～H-03 |
