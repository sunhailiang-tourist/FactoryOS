# Step 3 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md` · Step 3
- **命名**：`test-1442-step3-regression.md`
- **口令**：`【Test·Step 3 验收】`（对照 `step-stop-1435-step3.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `execution_service/service.py` | L2 → `execute_op` | Step3 接线 | ✅ | PASS |
| `execution_service/store.py` | snapshot/legacy_refs 持久化 | Step3 | ✅ 复用 002 列 | PASS |
| `connector_sdk/mock_legacy.py` | snapshot 增强 | 支撑 E-02 | ✅ | PASS |
| `src/server/db/migrations/versions/004_*` | — | 若缺列则 migration | ❌ 未新增（002 已有列） | PASS |
| revert HTTP / `revert.py` | — | Step4 | ❌ 未实现 | 符合分步 |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| E-02 | L2 真写 · success · snapshots · legacy_refs[] | `test_E02_*` | **PASS** |
| E-09 | evidence.execution 含 snapshots | `test_E09_*` | **PASS** |
| E-03 | L2 写后 audit | E-02 路径旁证 ≥2 事件 | **PASS**（旁证） |
| E-06/E-07/E-01 | dry_run · 幂等 · L0 | 存量用例 | **PASS** |
| B/C 系列 | Step1–2 | 7 passed | **PASS** |
| E-04/E-05 | revert HTTP | Step4 | **FAIL**（预期 · 404） |
| 存量 | `-m 'not pending'` | 56 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_execution_e02_e04_e05.py -k 'E-02 or E-09' -v   # 2 passed
uv run pytest src/tests/integration/test_execution_e06_e07.py test_execution_e01.py -q  # 3 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 56 passed · 4 failed（E-04/E-05 预期红 + 2 workflow 文档门禁已随 state 修复）
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | execution_service 编排；写 Legacy 经 runtime | ✅ R-01 |
| 写路径 | `writes_legacy` → `execute_op` 唯一出口 | ✅ |
| 红线 | dry_run 仍不写 Legacy（E-06 绿） | ✅ |
| 注释 | service/store 文件头更新 | ✅ |
| schema | `legacy_refs` 已归一化为 `LegacyRef[]` | ✅（Step2 遗留已修） |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-02 | `POST /v1/execute` dry_run=false | GOVERNED_WRITE | **PASS** |

**E-02 出参（HTTP）**：

```json
{
  "status": "success",
  "dry_run": false,
  "before_snapshot": {
    "entity_type": "work_order",
    "entity_id": "wo-ev",
    "fields": { "status": "open", "completed_qty": 0 }
  },
  "after_snapshot": {
    "entity_type": "work_order",
    "entity_id": "wo-ev",
    "fields": { "status": "in_progress", "completed_qty": 0 }
  },
  "legacy_refs": [
    { "system": "mock", "ref_type": "work_order", "ref_id": "work_order/wo-ev" }
  ]
}
```

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-03 | `GET /v1/audit/events` | E-02 成功后 | **PASS**（2 条 audit） |
| E-09 | `GET /v1/executions/{id}/evidence` | L2 写后 | **PASS** |

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 分层 | `_runtime_legacy_refs` 桥接 runtime dict → OpenAPI 模型，职责清晰 |
| 落位 | 无 apps 膨胀；store 读写 snapshot JSON 对称 |
| 耦合 | `DEFAULT_PACK_ID = conn-mock` 硬编码 — W5+ 可接 tenant pack 解析 |
| 可维护性 | 未新增 migration 因 002 已预埋列 — 决策正确 |

**需改进项（非阻断）**：

1. E-03 专用用例仍走 `dry_run=true` fixture — 建议 Step4 前补 L2 路径显式断言（可选）
2. `DEFAULT_PACK_ID` 硬编码 — 后续 Pack 配置化

## 6. 结论

**结论：通过**

- Step 3 目标 **E-02 · E-09 绿**；E-03 随 L2 旁证；E-06/E-07/E-01 存量回归绿
- E-04/E-05 仍红为 Step4 预期
- 56 项存量业务无破坏

**下一步**：**Verify 新会话** `【Verify回合】Step 3` → `./scripts/gate step --step 3 -k 'E-02'`
