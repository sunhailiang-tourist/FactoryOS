# reconciliation_service · 对账 Job

## 是什么

ExecutionRecord **read-back** 与 Legacy snapshot 比对，产出 ReconciliationReport。

## 主要功能

- `run_reconciliation` 内核（W6 stub · mock_legacy read-back）
- drift 检测与 status=ok | drift_detected

## 不负责什么

- 真实 ERP/MES HTTP read-back（W7+）
- 自动修复 drift

## 上下游

- **上游**：`server/api` POST `/v1/reconciliation/run`
- **下游**：`connector_sdk.mock_legacy` · `execution_service` 账本只读

## 相关文档

- Shadow-Mode与对账规格 · AC K-01/K-02 · ADR-004/005
