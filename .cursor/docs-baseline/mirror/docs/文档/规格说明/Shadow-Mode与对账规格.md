# 规格说明·Shadow Mode 与对账

| 版本 | v1.0.0 |
|------|--------|
| 范围 | 租户级影子运行 + 对账 Job |
| 决策 | ADR-004 · ADR-005 · [04-工厂实施手册](../../准备/2026-06-16/04-工厂实施手册.md) |
| 验收 | AC-BASE-001 T-01, K-01, K-02 |

## 1. Shadow Mode

### 1.1 语义

| 字段 | 说明 |
|------|------|
| `tenant.shadow_mode` | `true` = 该 tenant 所有 L2 写 **模拟执行** |
| ExecutionRecord | `shadow_mode=true`；**`status=simulated`**（非 success） |
| Legacy（Data-L0） | **不变**（Connector `write` 不被调用） |
| Audit | 正常 append |

### 1.2 开关

- 设置：`PUT /v1/tenants/{id}/settings` body `{ "shadow_mode": true }`
- 默认：新 tenant **shadow_mode=true** 直至 Integration Studio **Prove** 步批准
- 批准：Audit 事件 `integration.write_approved` 后允许 `shadow_mode=false`

### 1.3 标准交付

- D1 Step 4 / Studio Prove：**Shadow ≥14 天**（`08` R2、`04` Step 4）
- 期间对账 Job 每日运行；drift → 告警，不自动开写

### 1.4 dry_run vs shadow_mode

| 维度 | `dry_run=true`（单次） | `tenant.shadow_mode=true`（租户级） |
|------|------------------------|-------------------------------------|
| 范围 | 当前 ExecuteRequest | 该 tenant 全部 L2 写 |
| 终态 | `status=simulated` | `status=simulated` |
| Harness Simulate 步 | ✅ | — |
| 实施 Shadow ≥14d | — | ✅ |

两者同时为 true 时，语义相同：**不写 Legacy**。

## 2. 对账 Job（Reconciliation）

### 2.1 API

```http
POST /v1/reconciliation/run
```

Body（可选）：

```json
{
  "tenant_id": "string",
  "scope": "daily | ad_hoc",
  "graph_id": "string",
  "since": "date-time"
}
```

### 2.2 逻辑

1. 读取 Data-L1 ExecutionRecord（success, 非 reverted, 非 shadow）
2. 对每个 `legacy_refs` 调用 Connector **read-back**（Blueprint `reconcile.read_verb`）
3. 比较 qty/status/关键字段
4. 产出 `ReconciliationReport`：status=`ok` | `drift_detected` + 明细

### 2.3 按路径

| 路径 | read-back 目标 |
|------|----------------|
| Path A（ERP 写） | ERP API |
| Path B（MES 写） | MES API |
| Path C（builtin） | 内置表 count/sum |

## 3. 与 Harness 关系

- Harness **Simulate** 步：单次请求的 shadow/dry_run
- **tenant.shadow_mode**：租户级长期 Shadow（实施期）

## 4. Gate

- **Core 1.0 P0**：K-01 无 drift（mock）；K-02 模拟 drift；**T-01** shadow 不写 Legacy，`status=simulated`
