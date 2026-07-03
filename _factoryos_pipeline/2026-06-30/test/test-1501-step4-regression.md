# Step 4 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md` · Step 4
- **命名**：`test-1501-step4-regression.md`
- **口令**：`Step4 终轮回归`（对照 `step-stop-1455-step4.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `api/modules/reconciliation/` | POST `/v1/reconciliation/run` 薄路由 | Step4 | ✅ | PASS |
| `api/router/v1/registry.py` | reconciliation provider | Step4 | ✅ | PASS |
| `api/modules/README.md` | 域清单 | 文档 | ✅ | PASS |

**内核**：Step3 已交付 `run_reconciliation`；Step4 仅 HTTP 暴露。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| K-02 | 篡改 mock → POST run → drift_detected | `test_K02_*` | **PASS** |
| K-02 | drifts ≥ 1 | `test_K02_*` | **PASS** |
| K-01 | Step3 回归 | `test_K01_*` | **PASS** |
| T-02 · workflow | Step1–2 回归 | `test_license_w6_*` | **PASS** |
| OpenAPI | `/v1/reconciliation/run` 已声明 | `工厂操作系统-v1.1.yaml` | **PASS** |

```bash
uv run pytest src/tests/integration/test_reconciliation_w6.py -k 'K-02' -v   # 1 passed
uv run pytest src/tests/integration/test_reconciliation_w6.py -v               # 2 passed
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | API 薄路由 · 业务在 reconciliation_service | ✅ |
| 写路径 | HTTP 只 read-back · 无 Legacy 写 | ✅ |
| 契约 | `ReconciliationRunBody` · 返回 `model_dump` JSON | ✅ |
| 注释 | controller · README 齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| K-02 | `POST /v1/reconciliation/run` | L2 写 → 篡改 mock_legacy → run | **PASS** |

**K-02 出参（HTTP · 摘要）**：

```json
{
  "status": "drift_detected",
  "drifts": [
    {
      "field": "completed_qty",
      "expected": 2,
      "actual": 999,
      "legacy_ref": "work_order/wo-k01-<suffix>"
    }
  ]
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| API 设计 | 与 OpenAPI ReconciliationRunRequest 字段对齐 |
| 复用 | 直接委托 Step3 内核，无重复比对逻辑 |

## 6. 结论

**结论：通过**

**下一步**：并入终轮 `test-1501-final-regression.md` → Verify → `gate step --step 4 -k 'K-02'`
