# 验收用例 B-LITE-001：无 ERP 内置账本（产品 B Lite）

| 版本 | v0.1.0 |
|------|--------|
| 日期 | 2026-06-16 |
| 前置 | [AC-BASE-001](./验收用例-BASE-001-平台底座.md) 全绿；[AC-UX-001](./验收用例-UX-001-终端体验与多模态.md) P0 绿 |
| 规格 | [产品B-Lite无ERP内置账本](../规格说明/产品B-Lite无ERP内置账本.md) |

---

## 1. 范围

验证 **无外部 ERP/MES** 租户下，`conn-mes-builtin` + D1 Pack 可完成与 Overlay 等价的报工闭环。

**不在范围**：真 ERP 对接、财务、全量主数据治理。

---

## 2. 测试环境

| 项 | 要求 |
|----|------|
| tenant | `test-builtin-001` |
| connectors | 仅 `mes-builtin` + mock IM |
| Graph | frozen `graph-work-report` v1（与 Overlay 共用模板） |
| 数据 | `builtin_import` 或 fixture 注入 ≥3 张工单 |

---

## 3. 用例

| ID | 场景 | 步骤 | 期望 |
|----|------|------|------|
| BL-01 | 健康检查 | `health_check` mes-builtin | `status=ok` |
| BL-02 | 查工单 | DSL `QUERY_WO` | 返回 planned/completed_qty |
| BL-03 | Shadow 不写 | dry_run `WORK_REPORT` | `work_report` 无新行 |
| BL-04 | 受控写入 | Rule 通过 + `WORK_REPORT` | 新行 + `completed_qty` 增加 |
| BL-05 | 幂等 | 相同 `idempotency_key` 重试 | 不重复插入 |
| BL-06 | Revert | `WORK_REPORT_REVERT` | `status=reverted`；qty 回退 |
| BL-07 | 对账 | 对账 Job 跑一轮 | 零 unexplained drift |
| BL-08 | 无 ERP | 访问未配置 `erp-*` | 403 `CONNECTOR_NOT_CONFIGURED` |
| BL-09 | 多模态 E2E | 语音/mock → Harness 确认 → 写 | 与 BL-04 一致；UX-001 mock |
| BL-10 | tenant 隔离 | tenant A 写；tenant B 读 | B 不可见 A 工单 |

---

## 4. 自动化

```text
tests/
  integration/
    builtin_ledger/
      test_bl_01_health.py
      test_bl_04_work_report.py
      ...
  fixtures/
    builtin/
      materials.csv
      work_orders.csv
```

CI：与 BASE-001 同 pipeline；**LLM / ASR mock**（与 UX-001 一致）。

---

## 5. 签字

| 角色 | 姓名 | 日期 |
|------|------|------|
| 产品 | | |
| 研发 | | |
| 客户业务（B0 workshop） | | |
