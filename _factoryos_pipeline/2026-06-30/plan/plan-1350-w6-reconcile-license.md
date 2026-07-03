# 预开发说明：W6 — 对账 Job stub · License stub

- **日期**：2026-06-30
- **分支**：`dev_sunhailiang_core_260624`（W5 未 merge，同分支续开）
- **对照契约**：`contracts/openapi/工厂操作系统-v1.1.yaml` · `contracts/acceptance/验收用例-BASE-001-平台底座.md`（K-01/K-02 · T-02）· `contracts/schemas/ReconciliationReport.schema.json`
- **规格**：`docs/文档/规格说明/Shadow-Mode与对账规格.md`
- **路线图**：`docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md` W6
- **依赖 W5**：agent/harness · execution L2 · audit ✅

---

## Step 0 摘要

| 维度 | 结论 |
|------|------|
| **落点** | `license_service` · `reconciliation_service` 内核 · API 薄路由 |
| **写路径** | 对账只 read-back；License 在 execution 前门禁 |
| **本轮 AC** | K-01 · K-02 · T-02 |
| **DB** | 复用 001–004；对账 run 可先内存 |
| **缺口** | B：license 真源用 tenant 静态 JSON stub |

---

## 1. 迭代目标

**一句话**：`POST /v1/reconciliation/run` mock 对账；`license_service` 拦截未授权 Pack（403 + audit）。

**不在 W6**：真实 ERP read-back · P-01～P-03 · MCP（W7）

---

## 2. AC 对账表

| AC ID | 标题 | Step | Harness |
|-------|------|------|---------|
| K-01 | 无 drift | 3 | `-k 'K-01'` |
| K-02 | 模拟 drift | 4 | `-k 'K-02'` |
| T-02 | 未授权 Pack | 2 | `-k 'T-02'` |
| 存量 W1–W5 | 回归 | 每 Step | `-m 'not pending'` |

---

## 3. 分步计划

### Step 1 — license_service stub 内核（workflow）

- `assert_pack_licensed(tenant_id, pack_id)` · 静态 licensed 列表
- Harness：`gate step --step 1 -k 'workflow'`

### Step 2 — execution license 门禁（T-02）

- execute 前校验 · 403 MODULE_NOT_LICENSED · audit `license.denied`
- Harness：`gate step --step 2 -k 'T-02'`

### Step 3 — reconciliation 内核（K-01）

- `run_reconciliation` → ReconciliationReport status=ok
- Harness：`gate step --step 3 -k 'K-01'`

### Step 4 — POST `/v1/reconciliation/run` + K-02

- HTTP · 篡改 mock → drift_detected · OpenAPI 对账
- Harness：`gate step --step 4 -k 'K-02'`

---

## 4. 模块与文件

| 模块 | 路径 |
|------|------|
| license_service | `src/server/os_core/license_service/service.py` |
| reconciliation_service | `src/server/os_core/reconciliation_service/` |
| execution | license 钩子 |
| API | `src/server/api/modules/reconciliation/` |
| 测试 | `test_reconciliation_k*.py` · `test_license_t02*.py` |

---

## 5. Harness 验收盘

```bash
./scripts/gate step --step 4 -k 'K-02'
./scripts/gate delivery
./scripts/gate pr
```

---

## 6. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1.0 | 2026-06-30 | 初版 W6 |
