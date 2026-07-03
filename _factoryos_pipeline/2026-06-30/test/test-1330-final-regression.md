# 终轮全量回归 · Test 兜底验收报告（W5 agent + Harness）

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`（Step 1–4 全量）
- **命名**：`test-1330-final-regression.md`
- **口令**：`【Test·终轮回归】`

## 1. 本轮 git diff 全量改动面

| 路径 | 变更 | plan Step | 落位合理 |
|------|------|-----------|----------|
| `src/server/os_core/agent_orchestrator/` | 内核 stub · plan_store | 1 | ✅ |
| `src/server/api/modules/agent/` | POST `/v1/agent/plan` | 2 | ✅ |
| `src/server/api/modules/harness/` | POST `/v1/harness/confirm` | 3 | ✅ |
| `src/server/api/router/v1/registry.py` | 登记 agent · harness | 2–3 | ✅ |
| `src/tests/integration/test_*_w5*.py` | H-01～H-03 · workflow | 1–4 | ✅ |
| `src/tests/contract/test_openapi_contract.py` | W5 OpenAPI 对账 | 4 | ✅ |
| `src/tests/ac/test_base001_registry.py` | H-01～H-03 active | 1–4 | ✅ |
| `scripts/check_harness.py` · `gate` · `harness` | venv python 兜底 | 基建 | ✅ |
| `pyproject.toml` | Starlette 警告过滤 | 基建 | ✅ |

## 2. 新增功能正确性（本轮 AC 全量）

| AC ID | Step | 业务验收 | pytest 证据 | 结果 |
|-------|------|----------|-------------|------|
| workflow | 1 | create_plan stub | `test_agent_orchestrator_w5_step1` | **PASS** |
| H-01 | 2 | plan 不写 Legacy | `test_H01_*` | **PASS** |
| H-02 | 3 | confirm→execute | `test_H02_*` | **PASS** |
| H-03 | 4 | audit 全链路 | `test_H03_*` | **PASS** |
| OpenAPI | 4 | agent/harness 路径 | `test_openapi_w5_agent_harness_paths` | **PASS** |

## 3. 存量功能回归

| 域 | 命令 | 结果 |
|----|------|------|
| 全量非 pending | `pytest src/tests -m 'not pending' -q` | **81 passed · 1 skipped** |
| W5 集成 | `test_harness_w5.py` + `test_agent_orchestrator_w5_step1.py` | **4 passed** |
| Step4 gate | `./scripts/gate step --step 4 -k 'H-03'` | **PASS** |

```bash
./scripts/gate delivery   # 本报告落盘后执行
```

## 4. 代码落位与优雅性（终轮）

| 维度 | 结论 |
|------|------|
| 模块边界 | agent_orchestrator 仅 shared_contracts；Graph/Rule 在 API 层 |
| 写路径 | plan 阶段无 Legacy；confirm 后走 execution_service |
| 与 plan 一致 | 无 perception 端点 · 无 LiteLLM |

## 5. 接口分区（终轮交付）

### 新增

- `POST /v1/agent/plan` → DslPlan
- `POST /v1/harness/confirm` → ExecutionRecord | DslPlan

### 存量回归

- `POST /v1/execute` · `GET /v1/audit/events` · W1–W4 链路

## 6. 结论

**结论：通过**

- W5 Step 1–4 全绿 · 存量 81 passed · 允许 `./scripts/gate delivery` → commit
