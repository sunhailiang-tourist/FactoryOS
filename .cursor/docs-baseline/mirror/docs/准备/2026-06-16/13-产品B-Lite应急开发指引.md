# 产品 B Lite 应急开发指引

> 版本：v0.1.0 | 日期：2026-06-16  
> 触发：老板决策「立即承接无 ERP 客户」  
> 真源规格：[产品B-Lite无ERP内置账本](../../文档/规格说明/产品B-Lite无ERP内置账本.md)

---

## 1. 拍板当天（Day 0）

```text
□ 确认客户满足 B-01～B-05（编码 workshop 是否已结案？）
□ 销售合同走 Starter-B SKU，非 Overlay Starter
□ 技术负责人读：产品B-Lite 规格 + AC-B-LITE-001
□ 确认 AC-BASE-001 已绿（无底座则先 Gate 0，不可跳）
```

---

## 2. 第一周

| 天 | 任务 |
|----|------|
| D1 | Alembic：`builtin_ledger` 四表 migration |
| D2 | `connector_sdk/mes/builtin`：read（QUERY_WO） |
| D3 | write（WORK_REPORT）+ 事务 + 幂等 |
| D4 | revert（WORK_REPORT_REVERT） |
| D5 | Registry + License `conn-mes-builtin`；BL-01～BL-06 单测 |

---

## 3. 第二周

| 天 | 任务 |
|----|------|
| D6 | 对账 Job builtin 分支（BL-07） |
| D7 | `builtin_import` CLI + CSV 模板 |
| D8 | 租户配置模板；tenant 隔离测试（BL-10） |
| D9 | 接 Harness 确认门 E2E（BL-09）；复用 UX-001 mock |
| D10 | Shadow 14 天环境就绪；实施文档交接 |

---

## 4. 不可砍项

- Graph freeze + Rule + Audit + Revert（与 Overlay 相同）  
- B0 编码 workshop 书面签字  
- 无 ERP **不等于** 无确认门 / 无 Shadow  

---

## 5. 人力与周期

| 前提 | 增量工期 |
|------|----------|
| AC-BASE-001 已绿 | **2～4 周**（1～2 后端） |
| 底座未就绪 | 先 **8～11 周** Gate 0，再 +2～4 周 |

---

## 6. 相关文档

| 文档 | 用途 |
|------|------|
| [产品B-Lite无ERP内置账本](../../文档/规格说明/产品B-Lite无ERP内置账本.md) | 数据模型 + API 契约 |
| [AC-B-LITE-001](../../文档/验收/验收用例-B-LITE-001-无ERP内置账本.md) | 验收 |
| [mes/builtin/samples](../../文档/连接器/mes/builtin/samples/) | 请求/响应样例 |
| [11 内部宣讲 PPT](./11-内部宣讲PPT大纲.md) 第 7 页 | 老板口径 |
