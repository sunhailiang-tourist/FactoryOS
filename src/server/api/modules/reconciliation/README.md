# reconciliation · 对账 HTTP 域

## 是什么

OpenAPI `POST /v1/reconciliation/run` 薄路由，委托 `reconciliation_service.run_reconciliation`。

## 主要功能

- 触发对账 Job（ad_hoc / daily）
- 返回 ReconciliationReport（K-01/K-02）

## 不负责什么

- read-back 比对逻辑（在 `os_core/reconciliation_service`）
- 自动修复 drift

## 上下游

- **上游**：router/v1 · Studio / Cron
- **下游**：`os_core.reconciliation_service`

## 关联文档

- Shadow-Mode与对账规格 · contracts/openapi ReconciliationRunRequest
