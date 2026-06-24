# ERP · kingdee（金蝶 · Path A 灯塔）

| Registry Key (read) | `erp-kingdee-read` |
|---------------------|--------------------|
| Registry Key (write) | `erp-kingdee-write` |
| system | `erp` |
| vendor | `kingdee` |
| Pack ID (read) | `conn-erp-kingdee-read` |
| Pack ID (write) | `conn-erp-kingdee-write` |
| 路径 | **Path A** · Starter-A（哈森灯塔） |
| 规格 | [连接器规格 §3.1](../../../规格说明/连接器.md) |

## 说明

哈森灯塔 **无独立 MES**；生产报工通过金蝶 ERP 生产/报工 API 落账。  
`WORK_REPORT` → `execution_service` → `conn-erp-kingdee-write` → 金蝶 API。

## 样例（Gate 0'）

| 文件 | 用途 |
|------|------|
| [query_work_order.response.json](./samples/query_work_order.response.json) | QUERY_WO 读（ERP 工单） |
| [work_report.request.json](./samples/work_report.request.json) | WORK_REPORT 写请求 |
| [work_report.response.json](./samples/work_report.response.json) | WriteResult + before/after 快照 |
| [reconcile_readback.response.json](./samples/reconcile_readback.response.json) | 对账 read-back（AC-MVP-001） |

## 字段映射（草案）

| DSL 参数 | 金蝶字段（示例） | 说明 |
|----------|------------------|------|
| `work_order_id` | `FBillNo` / 内码 | 生产订单号 |
| `quantity` | `FQty` | 报工数量 |
| `reported_by` | `FOperator` | 报工人 |
| `idempotency_key` | 请求头 / 自定义字段 | 幂等 |

> 正式映射在 Graph workshop 后定稿；本目录样例供 Gate 0' 与 Contract Test 占位。

## Blueprint

认证目录：[catalog/erp/kingdee-write.yaml](../catalog/erp/kingdee-write.yaml)（待创建 Bronze 模板）
