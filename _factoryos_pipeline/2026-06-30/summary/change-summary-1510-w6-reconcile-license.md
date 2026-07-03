# PR 变更摘要：W6 — 对账 Job stub · License stub

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **日期**：2026-06-30
- **分支**：`dev_sunhailiang_core_260624`（W5 同分支续开 · 未 merge）

## 标题建议（PR title）

`feat(w6): license gate · reconciliation stub · K-01/K-02/T-02`

## 变更背景（Why）

W5 已具备 Agent/Harness 闭环；W6 补齐 **Pack 授权门禁** 与 **对账 Job stub**（mock_legacy read-back），落实 BASE-001 **T-02 / K-01 / K-02**，为 Shadow-Mode 实施期对账铺路。

## 主要改动（What）

| 模块 | 文件/路径 | 说明 |
|------|-----------|------|
| license_service | `src/server/os_core/license_service/` | `assert_pack_licensed` 静态 stub |
| execution | `execution_service/service.py` | execute 前 license 门禁 + `license.denied` audit |
| reconciliation_service | `src/server/os_core/reconciliation_service/` | `run_reconciliation` · mock read-back |
| reconciliation HTTP | `src/server/api/modules/reconciliation/` | `POST /v1/reconciliation/run` |
| contracts | `shared_contracts/models/reconciliation.py` | ReconciliationReport / Drift |
| execution store | `list_success_legacy_writes` | 对账数据源 |
| 结构 | `registry.py` · `repo-structure.yaml` | 内核 11 模块 |
| import 边界 | `check_import_boundaries.py` | execution→license · reconciliation→execution |
| 测试 | `test_license_w6_*` · `test_reconciliation_w6.py` | workflow · T-02 · K-01/K-02 |
| AC registry | `test_base001_registry.py` | K-01/K-02/T-02 active |

## AC 通过情况

| AC ID | Step | 结果 | 证据 |
|-------|------|------|------|
| workflow | 1 | **PASS** | `test_license_w6_step1` |
| T-02 | 2 | **PASS** | 403 MODULE_NOT_LICENSED + audit |
| K-01 | 3 | **PASS** | `run_reconciliation` status=ok |
| K-02 | 4 | **PASS** | HTTP drift_detected after tamper |

W1–W5 存量回归：终轮 `test-1501-final-regression.md` 通过。

## 业务口径确认（Behavior）

- **License**：tenant 静态列表（W6 stub）；未授权 Pack → 403，不写 Legacy，写 `license.denied`。
- **对账**：只读 ExecutionRecord success 写 + mock_legacy get_entity；产出 ReconciliationReport。
- **K-02**：篡改 mock Legacy 字段 → `drift_detected` + drifts 明细。

## 风险与兼容性

| 项 | 说明 |
|----|------|
| licensed 真源 | W6 内存 stub；W7+ 读 integration/tenants |
| ERP read-back | 未实现；Path A mock only |
| records_skipped_shadow | 计数含 dry_run/非 success，命名略宽 |

## 测试结论（Test）

```bash
./scripts/gate step --step 1 -k 'workflow'   # OK
./scripts/gate step --step 2 -k 'T-02'       # OK
./scripts/gate step --step 3 -k 'K-01'       # OK
./scripts/gate step --step 4 -k 'K-02'       # OK
./scripts/gate delivery                      # 待 phase=DELIVERY 后重跑
./scripts/gate pr                            # delivery 绿后
```

终轮：`test-1501-final-regression.md` · Verify：`verify-1450-step3` · `verify-*-step4`

## Summary（3 条，可贴 PR）

1. 新增 `license_service` + execution 前门禁：未授权 Pack 403 + `license.denied` audit（T-02）。
2. 新增 `reconciliation_service` + `POST /v1/reconciliation/run`：mock read-back 对账，K-01 ok / K-02 drift_detected。
3. 内核扩至 11 模块；四步 gate + 终轮回归绿，W1–W5 存量不回归。
