# Step 3 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md` · Step 3
- **命名**：`test-1053-step3-regression.md`（HHmm=1053）
- **口令**：`【Test·Step 3 验收】`
- **step-stop**：`step-stop-1052-step3.md`

## 1. 改动面说明

Step 3 内核（`execution_service` · `mock_legacy`）已在 Step 2 提前落地；本 Step 为 **行为对账 + README 文档**。

| 路径 | plan Step | 本 Step | 结论 |
|------|-----------|---------|------|
| `os_core/execution_service/service.py` | 3 | Step2 已交付 | PASS（复验） |
| `os_core/connector_sdk/mock_legacy.py` | 3 | Step2 已交付 | PASS（复验） |
| `os_core/execution_service/README.md` | 3 | Step3 文档 | PASS |

## 2. 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest | 结果 |
|-------|--------|--------|------|
| E-06 | dry_run → simulated · Legacy 不写 | `test_E06_dry_run_does_not_write_legacy` | **PASS** |
| E-07 | 同 idempotency_key → 同 exec_id | `test_E07_idempotency_key_no_duplicate_write` | **PASS** |
| E-03 存量 | audit 套件 | `test_audit_e03.py` | **PASS** (3/3) |
| W1+W2 存量 | workflow/contract/S-*/C-01 | `-m 'not pending'` | **PASS** (22/22) |
| E-09 | evidence（Step4） | `test_E09_*` | **FAIL**（Step4 范围 · 预期红） |

```bash
uv run pytest src/tests/integration/test_execution_e06_e07.py -v
# → 2 passed

uv run python scripts/check_static_quality.py
# → OK

uv run python scripts/gate_cli.py step --step 3 -k 'E-06'
# → 本报告落盘后执行
```

## 3. 代码落位合理性

| 维度 | 结论 |
|------|------|
| 写路径 | **通过** — `execute()` 唯一入口；`dry_run` 跳过 `mock_legacy_write` |
| E-06 | **通过** — `status=simulated` · `shadow_mode=true` · 写计数不变 |
| E-07 | **通过** — `find_by_idempotency` 早返回 · 不重复写 Legacy |
| 红线 R-07 | **通过** — dry_run 先于生产写路径 |
| Verify W2 | **需改进** — 尚无 W2 `verify-*-step3.md`（gate 可能误用 W1 `verify-1543`） |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC | 步骤 | 结果 |
|--------|-----|------|------|
| E-06 | dry_run 不写 Legacy | `execute(dry_run=True)` + `get_write_count()` | PASS |
| E-07 | 幂等 | 同 key 两次 `execute` | PASS |

**E-06 行为证据（内核）**：

- 入参：`dry_run=true` · `idempotency_key=e06-key-001`
- 出参：`status=simulated`
- Legacy mock 写计数：执行前后 **不变**

**E-07 行为证据（内核）**：

- 入参：同 `idempotency_key=e07-idem-key-001` 调用两次
- 出参：两次 `exec_id` **相同** · 第二次不增加 Legacy 写计数

结构依据：`contracts/acceptance` E-06 · E-07 · `ExecutionRecord.status=simulated`

**HTTP**：本 Step plan 无新 HTTP（execute 路由属 Step2/4 提前交付）。

## 5. 架构与代码质量评估

**结论子项**：

| 维度 | 评估 |
|------|------|
| 功能 E-06/E-07 | **通过** |
| 幂等实现 | **通过** — DB 唯一索引 + `find_by_idempotency` |
| 与 plan 节拍 | **需改进** — 实现已在 Step2 完成；Step3 为对账 Step |
| 存量回归 | **通过** — 22 项绿 |
| E-09 | **不在本 Step** — 仍红，待 Step4 |

## 6. 结论

**结论：需改进**

**E-06 · E-07 功能验收通过**（2/2 绿 · 存量 22 绿 · static OK）。

**机械关单欠账**：

1. **【Verify回合】Step 3**（新对话 · W2 plan）→ `verify-*-step3.md`（勿沿用 W1 `verify-1543`）
2. 重跑 `./scripts/gate step --step 3 -k 'E-06'` → 须 **Gate step OK**

**下一步**：W2 Step4 · E-09 evidence 路由 → **【Test·Step 4 验收】**
