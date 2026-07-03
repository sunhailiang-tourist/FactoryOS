# 测试用例与改动面：W6 对账 Job stub · License stub failing tests

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **命名**：`test-1406-w6-reconcile-license.md`
- **目的**：新增 · W6 Step1～4 failing tests（K-01 · K-02 · T-02 · workflow Step1）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_license_w6_step1.py` | 新增 | Step1 内核 `assert_pack_licensed` |
| `src/tests/integration/test_license_t02_w6.py` | 新增 | T-02 execute 未授权 Pack |
| `src/tests/integration/test_reconciliation_w6.py` | 新增 | K-01 内核 · K-02 HTTP |
| `src/tests/ac/test_base001_registry.py` | 修改 | K-01/K-02/T-02 移出 pending |

## 2. AC 用例

| ID | 标题 | 类型 | Step | 期望 |
|----|------|------|------|------|
| workflow | assert_pack_licensed | integration | 1 | 已授权 pack 不抛错 |
| T-02 | 未授权 Pack | integration | 2 | execute → 403 · audit license.denied |
| K-01 | 无 drift | integration | 3 | run_reconciliation → status=ok |
| K-02 | 模拟 drift | integration | 4 | POST /v1/reconciliation/run → drift_detected |
| 存量 W1–W5 | 回归 | 每 Step | `pytest -m 'not pending'` |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'workflow'
./scripts/gate step --step 2 -k 'T-02'
./scripts/gate step --step 3 -k 'K-01'
./scripts/gate step --step 4 -k 'K-02'
```

## 4. 标准测试用例

| ID | 标题 | 前置 | 步骤摘要 | 期望 |
|----|------|------|----------|------|
| workflow | licensed pack | — | `assert_pack_licensed(default, conn-mock)` | 无异常 |
| T-02 | unlicensed | frozen graph | execute · tenant 无 license | 403 MODULE_NOT_LICENSED |
| K-01 | ok | L2 exec 成功记录 | `run_reconciliation` | status=ok · drifts=[] |
| K-02 | drift | 篡改 mock_legacy | POST `/v1/reconciliation/run` | drift_detected · drifts≥1 |

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-1350-w6-reconcile-license.md` ✓ |
| Step 范围 | 1 workflow → 2 T-02 → 3 K-01 → 4 K-02 ✓ |
| 不在 W6 | 真实 ERP read-back · MCP · P-01～P-03 ✓ |
| 红线 | 对账只 read-back · License 在 execution 前 ✓ |

## Gate A–G 摘要

| Gate | 结论 |
|------|------|
| B 目的 | **新增** — W6 failing tests 驱动红→绿 |
| C 协作 | plan：license_service · reconciliation_service · execution 钩子 |
| E 接口 | POST `/v1/reconciliation/run` · execute license 门禁 |

## 📦 本次新增接口（测）

```json
POST /v1/reconciliation/run
{ "tenant_id": "default", "scope": "ad_hoc" }
```

## 结论

Test-plan 就绪 → `gate test` → Dev **`可以开始`** Step 1
