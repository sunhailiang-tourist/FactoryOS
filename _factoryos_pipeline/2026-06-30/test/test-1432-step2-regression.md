# Step 2 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md` · Step 2
- **命名**：`test-1432-step2-regression.md`
- **口令**：`【Test·Step 2 验收】`（对照 `step-stop-1425-step2.md` · workflow_state）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `execution_service/service.py` | execute 前 `assert_pack_licensed` · audit `license.denied` | Step2 钩子 | ✅ | PASS |
| `scripts/check_import_boundaries.py` | `execution_service` 可 import `license_service` | 矩阵更新 | ✅ | PASS |

**未改动（符合 Step2 范围）**：`reconciliation_service` · `POST /v1/reconciliation/run` — 留 Step3–4。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| T-02 | 未授权 tenant execute → 403 | `test_T02_*` | **PASS** |
| T-02 | audit `license.denied` ≥1 条 | `test_T02_*` | **PASS** |
| workflow | Step1 回归 | `test_license_w6_step1` | **PASS** |
| import_boundaries | 矩阵含 license_service | `test_import_boundaries` | **PASS** |
| 存量 W1–W5 + T-02 | `-m 'not pending'` 排除 K-01/K-02 | 83 passed · 1 skipped | **PASS** |
| K-01 · K-02 | Step3–4 红测 | 2 failed（预期） | **预期红** |

```bash
uv run pytest src/tests/integration/test_license_t02_w6.py -k 'T-02' -v   # 1 passed
uv run pytest src/tests/integration/test_license_w6_step1.py -q             # 1 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_reconciliation_w6.py -q
# 83 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | license 校验在 `execution_service` 入口 · 幂等查询之后 | ✅ |
| 写路径 | 未授权在 graph/rule 门禁之前拦截 · 无 Legacy 写 | ✅ R-11 |
| 审计 | `AuditEventType.LICENSE_DENIED` · commit 后 re-raise | ✅ |
| 红线 | `DEFAULT_PACK_ID=conn-mock` 与 stub licensed 表一致 | ✅ |
| 注释 | execute 函数头已有业务说明 · 钩子逻辑自解释 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| T-02 | `POST /v1/execute` | tenant=tenant-unlicensed-w6 · dry_run=true | **PASS** |

**T-02 出参（HTTP · 摘要）**：

```json
{
  "code": "MODULE_NOT_LICENSED",
  "message": "Pack conn-mock not licensed for tenant tenant-unlicensed-w6"
}
```

**T-02 audit 证据**：`GET /v1/audit/events?event_type=license.denied` → `len(events) >= 1`

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 门禁顺序 | license → graph → rule → execute，符合 plan「execution 前门禁」 |
| 耦合 | `execution_service` 仅依赖 `assert_pack_licensed` 公开 API |
| 可改进 | pack_id 暂硬编码 `DEFAULT_PACK_ID`；W7+ 可从 connector instance 解析（非本 Step 阻断） |

## 6. 结论

**结论：通过**

- Step 2 目标 **T-02 绿** · Step1 回归绿 · import 边界绿 · **存量 83/83 绿**
- K-01/K-02 仍红，符合 Step3–4 预期

**下一步**：**Verify 新会话** `【Verify回合】Step 2` → `./scripts/gate step --step 2 -k 'T-02'`
