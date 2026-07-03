# PR 变更摘要：W5 — agent stub · Harness 确认门 · OpenAPI 对齐

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **日期**：2026-06-30
- **分支**：`dev_sunhailiang_core_260624` · commit `w5开发完成`

## 标题建议（PR title）

`feat(w5): agent stub · harness confirm gate · H-01～H-03`

## 变更背景（Why）

W4 已具备 L2 真写与 revert；W5 补齐 **Agent → DslPlan → Harness 确认 → Rule → Execute** 闭环，落实 REDLINES **R-01（Agent 禁写 Legacy）** 与 **R-11（确认门）**，并为 OpenAPI v1.1 agent/harness 端点对齐。

## 主要改动（What）

| 模块 | 文件/路径 | 说明 |
|------|-----------|------|
| agent_orchestrator | `src/server/os_core/agent_orchestrator/` | `create_plan` 薄 stub（无 LLM）· 内存 `plan_store` |
| agent HTTP | `src/server/api/modules/agent/` | `POST /v1/agent/plan` · Graph/Rule 门禁在 API 层 |
| harness HTTP | `src/server/api/modules/harness/` | `POST /v1/harness/confirm` · `confirm_flow` 编排 |
| router | `src/server/api/router/v1/registry.py` | 登记 agent · harness providers |
| 文档 | `src/server/api/modules/README.md` | 域清单补 agent · harness |
| 契约测试 | `src/tests/contract/test_openapi_contract.py` | W5 OpenAPI 路径/schema 对账 |
| 集成测试 | `test_agent_orchestrator_w5_step1.py` · `test_harness_w5.py` | workflow · H-01～H-03 |
| AC registry | `src/tests/ac/test_base001_registry.py` | H-01～H-03 摘 pending |
| 基建 | `scripts/check_harness.py` · `pyproject.toml` | venv python 兜底 · Starlette 警告过滤 |

## AC 通过情况

| AC ID | Step | 结果 | 证据 |
|-------|------|------|------|
| workflow | 1 | **PASS** | `test_w5_step1_create_plan_stub_returns_dsl_plan` |
| H-01 | 2 | **PASS** | plan 阶段 Legacy 写计数 0 |
| H-02 | 3 | **PASS** | confirm → ExecutionRecord（dry_run/simulated 可控） |
| H-03 | 4 | **PASS** | audit 含 `harness.confirmed` + execute 事件 |
| OpenAPI | 4 | **PASS** | `test_openapi_w5_agent_harness_paths` |

W1–W4 存量回归：**81 passed · 1 skipped**（`-m 'not pending'`）。

## 业务口径确认（Behavior）

- **plan 阶段**：仅产 `DslPlan` 入内存 store，**不调用 execution**，**不写 Legacy**。
- **confirm=true**：写 `harness.confirmed` audit → `execution_service.execute`（仍过 W3 rule/graph 链）。
- **confirm=false**：仅 `harness.rejected` audit，返回原 plan。
- **stub 行为**：intent 正则抽工单号/数量 → 单步 `GOVERNED_WRITE`；无 LiteLLM。

## 风险与兼容性

| 项 | 说明 |
|----|------|
| PlanStore 内存 | 进程重启 plan 丢失；W6+ 可换 005 migration |
| 单步 plan | 仅 `plan.steps[0]`；多步留后续 |
| perception | `/v1/perception/*` 按 plan 未注册 |
| import 边界 | Graph/Rule  intentionally 在 API 层，非 agent_orchestrator 内核 |

## 测试结论（Test）

```bash
./scripts/gate step --step 1 -k 'workflow'   # OK
./scripts/gate step --step 2 -k 'H-01'       # OK
./scripts/gate step --step 3 -k 'H-02'       # OK
./scripts/gate step --step 4 -k 'H-03'       # OK
./scripts/gate delivery                      # OK
./scripts/gate pr                            # OK
```

终轮：`test-1330-final-regression.md` · Verify：`verify-1218-step1` … `verify-1309-step4`

## Summary（3 条，可贴 PR）

1. 新增 Agent 薄 stub：`POST /v1/agent/plan` 产出 DslPlan，plan 阶段零 Legacy 写（H-01 · R-11）。
2. 新增 Harness 确认门：`POST /v1/harness/confirm` 确认后走 rule→execution，全链路 audit 可追踪（H-02/H-03）。
3. OpenAPI v1.1 agent/harness 端点对账绿；W1–W4 存量 81 passed，四步 gate + delivery + pr 全绿。
