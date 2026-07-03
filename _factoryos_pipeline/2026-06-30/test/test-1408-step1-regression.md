# Step 1 单步验收 · Test 复验报告

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md` · Step 1
- **命名**：`test-1408-step1-regression.md`
- **口令**：`【Test·Step 1 验收】` / **复验**（对照 `step-stop-1415-step1.md` · workflow_state）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `os_core/license_service/service.py` | `assert_pack_licensed` · `is_pack_licensed` | Step1 内核 | ✅ | PASS |
| `os_core/license_service/__init__.py` | 包导出 | Step1 | ✅ | PASS |
| `os_core/license_service/README.md` | 模块说明 | 新模块门禁 | ✅ | PASS |

**未改动（符合 Step1 范围）**：`execution_service` 钩子 · `reconciliation_service` · API 路由 — 留 Step2–4。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| workflow | `assert_pack_licensed(default, conn-mock)` | `test_w6_step1_*` | **PASS** |
| workflow | 未授权 pack 抛 `MODULE_NOT_LICENSED` | 内核手工校验 | **PASS** |
| import_boundaries | `license_service` 仅 `shared_contracts` | `test_import_boundaries` | **PASS** |
| 存量 W1–W5 | `-m 'not pending'` 排除 Step2–4 红测 | 82 passed · 1 skipped | **PASS** |
| T-02 · K-01 · K-02 | Step2–4 红测 | 3 failed（预期） | **预期红** |

```bash
uv run pytest src/tests/integration/test_license_w6_step1.py -v
# 1 passed

uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q
# 1 passed

uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_license_t02_w6.py \
  --ignore=src/tests/integration/test_reconciliation_w6.py -q
# 82 passed · 1 skipped

# Step2–4 红测（本 Step 不要求绿）
uv run pytest src/tests/integration/test_license_t02_w6.py src/tests/integration/test_reconciliation_w6.py -q
# 3 failed（T-02 · K-01 · K-02）
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | 内核纯函数 · 无 API/execution 耦合 | ✅ |
| 写路径 | Step1 只读校验 · 无 Legacy 写 | ✅ |
| 契约 | `PlatformError` + `ErrorCode.MODULE_NOT_LICENSED` · http 403 | ✅ |
| 注释 | 文件头 · 函数 · README 齐全 | ✅ |
| stub | `default` → `conn-mock` 静态表 | ✅ 对齐 plan |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | 接口/函数 | 步骤 | 结果 |
|--------|-----------|------|------|
| workflow | `assert_pack_licensed` | tenant=default · pack=conn-mock | **PASS** |
| workflow | `assert_pack_licensed` | 未授权 tenant/pack | **PASS**（内核负向） |

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 边界 | `check_import_boundaries.py` 矩阵 `license_service → shared_contracts` 满足 |
| 可测性 | 包级导出便于 Step2 execution 钩子集成 |
| 风险 | `ACTIVE_AC_IDS` 已含 T-02/K-01/K-02，全量 `-m 'not pending'` 暂 3 红 — Step2 起逐步转绿 |

## 6. 结论

**结论：通过**

- Step 1 目标 **workflow 绿** · import 边界绿 · **存量 W1–W5 82/82 绿**
- T-02/K-01/K-02 红测符合 plan Step2–4 预期，不阻断本 Step

**下一步**：**Verify 新会话** `【Verify回合】Step 1` → `./scripts/gate step --step 1 -k 'workflow'`
