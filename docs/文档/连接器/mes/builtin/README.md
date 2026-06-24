# MES · builtin（产品 B Lite）

| Registry Key | `mes-builtin` |
|--------------|---------------|
| system | `mes` |
| vendor | `builtin` |
| Pack ID | `conn-mes-builtin` |
| 规格 | [产品B-Lite无ERP内置账本](../../../规格说明/产品B-Lite无ERP内置账本.md) |

## 说明

无外部 MES 时，读写 **PostgreSQL `builtin_ledger` schema**，实现 D1 报工闭环。

## 样例

| 文件 | 用途 |
|------|------|
| [query_work_order.response.json](./samples/query_work_order.response.json) | QUERY_WO 读 |
| [work_report.request.json](./samples/work_report.request.json) | WORK_REPORT 写 |
| [work_report.response.json](./samples/work_report.response.json) | WriteResult |

## 实施导入

编码 workshop 后使用 `builtin_import`（应急开发时实现）导入 `samples/*.csv`。
