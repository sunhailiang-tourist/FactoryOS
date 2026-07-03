# Step 6 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 6
- **命名**：`test-1107-step6-regression.md`
- **口令**：`Step 6 单步验收落盘`（对照 `step-stop-1205-step6.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `shared_contracts/cmv_registry.py` | `register_dsl_verb` · L2 compensator 校验 | Step6 D-04 | ✅ | PASS |
| `registry/controllers/registry.py` | POST `/v1/registry/cmv/verbs` | Step6 D-04 | ✅ | PASS |
| `agent_orchestrator/` | 无 connector 写 import | Step6 E-08 | ✅ 已满足 | PASS |

**未改动（符合 Step6 范围）**：N-01～N-04 负向安全 — 留 Step7。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| D-04 | L2 无 compensator → 422 | `test_D04_*` | **PASS** |
| E-08 | orchestrator 无 connector 写路径 | `test_E08_*` | **PASS** |
| M-01 · M-02 | Step5 回归 | `test_mcp_w7` | **PASS** |
| P-01～T-03 | Step1–4 抽样 | package 全量 | **PASS** |
| import_boundaries | 矩阵 | `test_import_boundaries` | **PASS** |
| 存量 | `-m 'not pending'` 排除 N-* 红测 | 102 passed · 1 skipped | **PASS** |

```bash
uv run pytest src/tests/integration/test_dsl_e08_w7.py -v   # 2 passed (D-04 · E-08)
uv run pytest src/tests/integration/test_mcp_w7.py src/tests/integration/test_package_w7.py -q  # 5 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 102 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | CMV 校验在 shared_contracts · API 薄路由 | ✅ |
| D-04 | 对齐 `check_cmv_sync` · L2 须 compensator | ✅ |
| E-08 | agent_orchestrator 仅 shared_contracts 依赖 | ✅ R-01 |
| 写路径 | register 仅校验不落库（人审 change-request） | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| D-04 | `POST /v1/registry/cmv/verbs` | L2 · compensator=null | **PASS** |
| E-08 | 静态扫描 agent_orchestrator | forbidden 字符串 | **PASS** |

**D-04 出参（HTTP · 摘要）**：

```json
{
  "code": "BLUEPRINT_INVALID",
  "message": "L2 verb TEST_L2_NO_COMP_W7 must declare compensator"
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 契约轨 | `register_dsl_verb` 与 CMV YAML 规则一致，可复用于 Studio 提案 |
| E-08 | 无新增实现；既有 import 边界保持 |

## 6. 结论

**结论：通过**

- Step 6 目标 **D-04 · E-08 绿** · Step1–5 回归绿 · **存量 102/102 绿**（N-* 除外）

**下一步**：**Verify 新会话** `【Verify回合】Step 6` → `./scripts/gate step --step 6 -k 'D-04'`
