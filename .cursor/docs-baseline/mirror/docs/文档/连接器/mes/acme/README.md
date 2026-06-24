# MES · Acme（Path B 占位厂商）

> 认证：**Bronze 占位** | Path **B**（MES 写 + ERP 读）  
> Blueprint：待选定真实 MES 厂商后替换 `vendor` 与 API 路径。

## 样例

| 文件 | 用途 |
|------|------|
| [samples/query_work_order.response.json](./samples/query_work_order.response.json) | QUERY_WO |
| [samples/work_report.request.json](./samples/work_report.request.json) | WORK_REPORT |
| [samples/work_report.response.json](./samples/work_report.response.json) | 写回 |
| [samples/reconcile_readback.response.json](./samples/reconcile_readback.response.json) | 对账 read-back |

验收：[AC-MVP-001](../../验收/验收用例-MVP-001-报工垂直闭环.md) Path B 用例 **在选定厂商前标记 blocked**。
