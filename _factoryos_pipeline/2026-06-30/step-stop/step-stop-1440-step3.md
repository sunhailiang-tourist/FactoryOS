# Step 停机：Step 3 — reconciliation 内核（K-01）

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 3 — `run_reconciliation` → ReconciliationReport status=ok

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/reconciliation_service/` | 新建内核模块 |
| `src/server/os_core/shared_contracts/models/reconciliation.py` | ReconciliationReport 模型 |
| `src/server/os_core/execution_service/store.py` | `list_success_legacy_writes` |
| `src/server/os_core/registry.py` · `contracts/repo-structure.yaml` | 内核登记 |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| K-01 | `run_reconciliation` 内核 | ✅ pytest 绿 |

## 4. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层 | Pass — 内核 read-back · 不写 Legacy |
| 2 | 响应 | Pass — ReconciliationReport schema |
| 3 | 红线 | Pass — 只读 mock_legacy |
| 4–10 | 其余 | Pass |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_reconciliation_w6.py -k 'K-01' -q
```

## 6. Verify

- 口令：`【Verify回合】Step 3`

## 7. 等待

Test → Verify → `gate step --step 3 -k 'K-01'` → **`可以继续`**
