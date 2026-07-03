# Step 3 单步验收 · Test 回归报告

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md` · Step 3
- **命名**：`test-1445-step3-regression.md`
- **口令**：`Step3 回归` / `【Test·Step 3 验收】`（对照 `step-stop-1440-step3.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `reconciliation_service/service.py` | `run_reconciliation` 内核 | Step3 | ✅ | PASS |
| `reconciliation_service/__init__.py` | 包导出 | Step3 | ✅ | PASS |
| `reconciliation_service/README.md` | 模块说明 | 新模块门禁 | ✅ | PASS |
| `shared_contracts/models/reconciliation.py` | ReconciliationReport/Drift | Step3 | ✅ | PASS |
| `execution_service/store.py` | `list_success_legacy_writes` | Step3 数据源 | ✅ | PASS |
| `os_core/registry.py` | 登记 reconciliation_service | 治理 | ✅ | PASS |
| `check_import_boundaries.py` | reconciliation 矩阵 | 静态 | ✅ | PASS |

**未改动（符合 Step3 范围）**：`POST /v1/reconciliation/run` API — 留 Step4（K-02）。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| K-01 | `run_reconciliation` → status=ok · drifts=[] | `test_K01_*` | **PASS** |
| K-01 | ReconciliationReport schema required 字段 | `test_K01_*` | **PASS** |
| T-02 · workflow | Step1–2 回归 | `test_license_w6_*` | **PASS** |
| import_boundaries | 矩阵含 reconciliation_service | `test_import_boundaries` | **PASS** |
| 内核 registry | 11 modules 对齐 | `check_kernel_registry` · `test_os_core_registry_*` | **PASS** |
| 存量 | `-m 'not pending'` 排除 K-02 | 84 passed · 1 skipped | **PASS** |
| K-02 | Step4 HTTP 红测 | `test_K02_*` | **预期红** |

```bash
uv run pytest src/tests/integration/test_reconciliation_w6.py -k 'K-01' -v   # 1 passed
uv run pytest src/tests/integration/test_license_w6_step1.py src/tests/integration/test_license_t02_w6.py -q  # 2 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -k 'not K-02' -q
# 84 passed · 1 skipped · 1 deselected
uv run python scripts/check_kernel_registry.py  # OK: 11 modules
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | 内核 read-back mock_legacy · 不写 Legacy | ✅ |
| 写路径 | 仅读 `execution_records` + mock_legacy.get_entity | ✅ Shadow 规格 |
| 契约 | 返回 `ReconciliationReport` Pydantic · path=A | ✅ |
| 跳过规则 | dry_run/shadow/非 success 跳过 | ✅ |
| 注释 | service · store · README 齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| K-01 | `run_reconciliation(session, tenant_id, scope)` | L2 真写后 read-back | **PASS** |

**K-01 出参（内核 · 摘要）**：

```json
{
  "status": "ok",
  "drifts": [],
  "tenant_id": "default",
  "scope": "ad_hoc",
  "path": "A",
  "records_checked": 1
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 数据源 | `list_success_legacy_writes` 过滤条件与 Shadow 规格一致 |
| 可维护性 | `_compare_fields` 可复用于 K-02 drift |
| 存量修复 | `test_registry_harness` 10→11 模块（W6 license + reconciliation） |

## 6. 结论

**结论：通过**

- Step 3 目标 **K-01 绿** · Step1–2 回归绿 · **存量 84/84 绿**（K-02 除外）
- 内核 registry 存量测试已同步 11 模块

**下一步**：**Verify 新会话** `【Verify回合】Step 3` → `./scripts/gate step --step 3 -k 'K-01'`
