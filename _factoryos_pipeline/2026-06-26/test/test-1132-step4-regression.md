# Step 4 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md` · Step 4
- **命名**：`test-1132-step4-regression.md`（HHmm=1132 · 补录）
- **口令**：`【Test·Step 4 验收】`（对照 `step-stop-1132-step4.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `src/os_core/shared_contracts/cmv_registry.py` | 新增 | CMV 动词表 | ✅ | PASS |
| `src/os_core/shared_contracts/exceptions.py` | 新增 | PlatformError | ✅ | PASS |
| `src/os_core/execution_service/service.py` | 修改 | graph→rule→DSL 链 | ✅ | PASS |
| `src/apps/api/routes/dsl.py` | 新增 | GET registry | ✅ | PASS |
| `src/tests/integration/test_dsl_w3.py` | 新增 | D-01～D-03 | ✅ | PASS |
| `src/tests/integration/test_execution_e01.py` | 新增 | E-01 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| D-01 | registry 列表 | `test_D01_list_dsl_registry` | **PASS** |
| D-02 | 未知 verb | `test_D02_unknown_verb_rejected` | **PASS** |
| D-03 | graph allowed_dsl | `test_D03_verb_not_in_graph_allowed_dsl` | **PASS** |
| E-01 | L0 QUERY 不写 Legacy | `test_E01_l0_query_on_frozen_graph` | **PASS** |
| W2 | E-03/06/07/09 | 存量 integration | **PASS** |

```bash
uv run pytest src/tests/integration/test_dsl_w3.py src/tests/integration/test_execution_e01.py -v
uv run python scripts/gate_cli.py step --step 4 -k 'E-01'
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | 门禁在 execution_service 单入口 | **通过** |
| 写路径 | E-01 mock_legacy write_count=0 | **通过** |
| 红线 | D-02/D-03 拒绝非法动词 | **通过** |
| W2 未破坏 | audit/execution/evidence 仍绿 | **通过** |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-01 | `POST /v1/execute` QUERY_ENTITY | 200 · 0 Legacy writes | **PASS** |
| D-02 | verb=UNKNOWN_VERB | 400 `DSL_UNKNOWN` | **PASS** |

## 5. 架构与代码质量评估（本 Step）

**通过** — 门禁链顺序清晰；exceptions 统一 HTTP 映射。

## 6. 结论

**结论：通过**

- 补录 · 终轮 `test-1132-w3-final-regression.md` 42/42 · `gate pr` OK。
- 通过 → **Verify·Step 4**（`verify-1140-step4.md`）→ W3 四步链闭合
