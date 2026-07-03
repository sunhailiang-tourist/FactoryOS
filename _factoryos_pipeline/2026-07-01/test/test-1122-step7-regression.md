# Step 7 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 7
- **命名**：`test-1122-step7-regression.md`
- **口令**：`Step 7 单步验收落盘`（对照 `step-stop-1215-step7.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `shared_contracts/param_safety.py` | `assert_params_safe` · SQL 注入模式 | Step7 N-04 | ✅ | PASS |
| `execution_service/service.py` | execute 前 param 校验 · `get_execution_for_tenant` · `assemble_evidence_for_tenant` | Step7 N-03/N-04 | ✅ | PASS |
| `execution_service/__init__.py` | 导出 tenant 隔离 API | Step7 N-03 | ✅ | PASS |
| `api/modules/execution/controllers/executions.py` | GET execution/evidence 走 tenant 隔离 | Step7 N-03 | ✅ | PASS |

**N-01/N-02（step-stop 声明无本 Step 新增实现）**：N-01 路由不存在 → 404；N-02 既有 freeze/checksum 校验 → 409/422。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| N-01 | 无 `/v1/internal/execute` 旁路 | `test_N01_*` | **PASS** |
| N-02 | checksum 篡改 freeze 拒绝 | `test_N02_*` | **PASS** |
| N-03 | 跨 tenant GET execution → 403 | `test_N03_*` | **PASS** |
| N-04 | params SQL injection → 422 | `test_N04_*` | **PASS** |
| D-04 · E-08 | Step6 回归 | `test_dsl_e08_w7` | **PASS** |
| M-01 · M-02 | Step5 回归 | `test_mcp_w7` | **PASS** |
| P-01～T-03 | Step1–4 抽样 | shadow · connector · package | **PASS** |
| import_boundaries | 矩阵 | `test_import_boundaries` | **PASS** |
| 存量 | `-m 'not pending'` 全量含 N-* | 106 passed · 1 skipped | **PASS** |

```bash
uv run pytest src/tests/integration/test_negative_w7.py -v   # 4 passed (N-01～N-04)
uv run pytest src/tests/integration/test_shadow_w7.py src/tests/integration/test_connector_t03_w7.py \
  src/tests/integration/test_package_w7.py src/tests/integration/test_mcp_w7.py \
  src/tests/integration/test_dsl_e08_w7.py -q   # 9 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q   # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 106 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | N-04 校验在 shared_contracts · execute 入口调用 · API 薄路由 | ✅ |
| N-03 | tenant 隔离在 os_core · controller 仅注入 caller_tenant | ✅ |
| N-01 | 无新增路由；404 符合「无旁路」 | ✅ |
| N-02 | freeze 前 checksum 与 graph body 一致性（既有逻辑） | ✅ |
| 写路径 | execution_service 唯一写 Legacy；GET 只读隔离 | ✅ ADR-002 |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| N-01 | POST `/v1/internal/execute` | 404 | **PASS** |
| N-02 | PUT graph checksum 篡改 → freeze | 409/422 | **PASS** |
| N-03 | tenant A execute · tenant B GET | 403 | **PASS** |
| N-04 | POST `/v1/execute` SQL injection entity_id | 422 | **PASS** |

**N-04 出参（HTTP · 摘要）**：

```json
{
  "code": "MAPPING_ERROR",
  "message": "Unsafe param value rejected: entity_id"
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 安全轨 | param_safety 递归扫描 params · 模式可扩展 |
| 多租户 | GET execution/evidence 共用 `get_execution_for_tenant` · 403 真源一致 |
| Gate 0 | Step1–7 AC 全绿 · 存量 106/106 绿（1 skipped 为 pending 标记） |

## 6. 结论

**结论：通过**

- Step 7 目标 **N-01～N-04 绿** · Step1–6 回归绿 · **存量 106/106 绿**
- W7 Gate 0 七步 Dev+Test 链路完成

**下一步**：**Verify 新会话** `【Verify回合】Step 7` → `./scripts/gate step --step 7 -k 'N-01'` → Test 终轮回归 → `gate delivery`
