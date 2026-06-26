# Step 2 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md` · Step 2
- **命名**：`test-1426-step2-regression.md`
- **口令**：`【Test·Step 2 验收】`（对照 `step-stop-1420-step2.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `connector_sdk/runtime/execute.py` | 新增 | Step2 execute_op | ✅ | PASS |
| `connector_sdk/runtime/entity.py` | 新增 | entity.get/update | ✅ | PASS |
| `connector_sdk/runtime/mapping.py` | 新增 | mapping 负向 | ✅ | PASS |
| `connector_sdk/mock_legacy.py` | 扩展 | entity store | ✅ | PASS |
| `execution_service` | — | Step3 | ❌ 未改 | 符合分步 |
| revert HTTP | — | Step4 | ❌ 未改 | 符合分步 |

**合理超前**：C-04 read-back 在 Step2 随 `entity_update` 一并实现；plan 原排 Step4，属 runtime 同域，可接受。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| B-02 | Runtime L2 · legacy_refs | `test_B02_*` | **PASS** |
| B-03 | mapping 缺字段 → MAPPING_ERROR | `test_B03_*` | **PASS** |
| C-02 | entity.get snapshot | `test_C02_*` | **PASS** |
| C-03 | entity.update · legacy_refs | `test_C03_*` | **PASS** |
| C-04 | write 后 read-back | `test_C04_*` | **PASS**（超前） |
| E-02/E-04/E-05/E-09+ | execution L2 / revert | Step3–4 | **FAIL**（预期） |
| 存量 | W1–W3 + Step1 | `-m 'not pending'` | **PASS**（54 项） |

```bash
uv run pytest src/tests/integration/test_connector_blueprint_w4.py -k 'B-02 or B-03' -v   # 2 passed
uv run pytest src/tests/integration/test_connector_runtime_w4.py -v                        # 3 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 54 passed · 4 failed（E Step3–4 预期红）
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | runtime 在 os_core；execute → entity → mock_legacy | ✅ |
| 写路径 | Legacy 写经 mock_legacy；Step3 再经 execution_service 接线 | ✅ |
| 红线 | R-01 内核测直调 runtime，非 Agent 旁路 | ✅ |
| 注释 | execute/entity/mapping/mock_legacy 文件头齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| B-02 | `execute_op(GOVERNED_WRITE)` | conn-mock runtime | **PASS** |

**B-02 出参（内核）**：

```json
{
  "legacy_refs": {
    "legacy_id": "work_order/wo-w4-b02",
    "entity_type": "work_order",
    "entity_id": "wo-w4-b02"
  },
  "before_snapshot": { "fields": { "status": "open", "completed_qty": 0 } },
  "after_snapshot": { "fields": { "status": "in_progress", "completed_qty": 1 } }
}
```

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| C-02 | `entity_get` | work_order/wo-w4-c02 | **PASS** |

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 分层 | execute → entity → mock_legacy 链清晰 |
| 可维护性 | `legacy_refs` 当前为 dict — Step3 接线 execution 时须对齐 schema 数组形态 |

## 6. 结论

**结论：通过**

**下一步**：**Verify 新会话** `【Verify回合】Step 2` → `./scripts/gate step --step 2 -k 'C-02'`
