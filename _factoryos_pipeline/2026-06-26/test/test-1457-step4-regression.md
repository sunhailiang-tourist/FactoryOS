# Step 4 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md` · Step 4
- **命名**：`test-1457-step4-regression.md`
- **口令**：`【Test·Step 4 验收】`（对照 `step-stop-1445-step4.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `execution_service/service.py` | `revert_execution` | Step4 | ✅ | PASS |
| `execution_service/store.py` | `update_execution_status` | Step4 | ✅ | PASS |
| `connector_sdk/mock_legacy.py` | `restore_entity` | Step4 | ✅ | PASS |
| `apps/api/routes/execute.py` | POST revert | Step4 | ✅ | PASS |
| `apps/api/routes/executions.py` | GET execution | 支撑 E-04 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| E-04 | revert · Legacy 恢复 | `test_E04_*` | **PASS** |
| E-05 | 重复 revert → 409 | `test_E05_*` | **PASS** |
| B-04 | L2 无 revert 校验 | `test_B04_*` | **PASS** |
| C-04 | read-back | `test_C04_*` | **PASS** |
| E-02/E-09 | L2 写回归 | 4/4 E 用例 | **PASS** |
| 存量 | `-m 'not pending'` | 60 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_execution_e02_e04_e05.py -v   # 4 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 60 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | revert 路由薄；逻辑在 execution_service | ✅ |
| 写路径 | revert 经 mock_legacy.restore_entity | ✅ R-01 |
| 红线 | dry_run/simulated → 409；audit append-only | ✅ |
| 注释 | revert_execution 齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-04 | `POST /v1/execute/{execId}/revert` | L2 写成功后 | **PASS** |

**E-04 出参**：

```json
{
  "status": "reverted",
  "verb": "GOVERNED_WRITE",
  "dry_run": false
}
```

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-05 | 重复 revert | 已 reverted 再 POST | **PASS** · 409 |

**E-05 出参**：

```json
{
  "detail": "Execution already reverted",
  "code": "REVERT_NOT_ALLOWED"
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 分层 | revert 与 execute 对称，落位正确 |
| 可维护性 | mock 直恢复；后续可接 blueprint revert op |

## 6. 结论

**结论：通过**

- **E-04 · E-05 绿**；W4 本轮 AC 全绿；**存量 60/60 绿**
- W4 四步单步 Test 验收全部完成

**下一步**：Verify·Step4 → `gate step --step 4 -k 'E-04'` → **【Test·终轮回归】**
