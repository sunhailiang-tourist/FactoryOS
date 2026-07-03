# Step 停机：Step 4 — POST /v1/reconciliation/run（K-02）

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 4 — HTTP 对账 · 篡改 mock → drift_detected · OpenAPI 对齐

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/api/modules/reconciliation/` | 新建 HTTP 域 |
| `src/server/api/router/v1/registry.py` | ROUTER_PROVIDERS 登记 |
| `src/server/api/modules/README.md` | 域清单 |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| K-02 | POST `/v1/reconciliation/run` | ✅ pytest 绿 |

## 4. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层 | Pass — API 薄路由 · 内核 run_reconciliation |
| 2 | OpenAPI | Pass — 路径/标签与 v1.1 一致 |
| 3 | 红线 | Pass — 只读对账 |
| 4–10 | 其余 | Pass |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_reconciliation_w6.py -k 'K-02' -q
```

## 6. Verify

- 口令：`【Verify回合】Step 4`

## 7. 等待

Test → Verify → `gate step --step 4 -k 'K-02'` → W6 delivery
