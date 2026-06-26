# Step 2 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md` · Step 2
- **命名**：`test-1132-step2-regression.md`（HHmm=1132 · 补录）
- **口令**：`【Test·Step 2 验收】`（对照 `step-stop-1132-step2.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `src/os_core/graph_service/service.py` | 生命周期 | submit/freeze/clone/deprecate | ✅ | PASS |
| `src/apps/api/routes/graphs.py` | 新增 | 薄 HTTP 路由 | ✅ | PASS |
| `src/apps/api/routes/error_handlers.py` | 新增 | PlatformError 映射 | ✅ | PASS |
| `src/tests/integration/test_graph_w3.py` | G-02～G-08 | 生命周期 AC | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| G-02 | draft 可 PUT | `test_G02_update_draft_graph` | **PASS** |
| G-03 | 未 freeze execute → 409 | `test_G03_execute_l2_on_draft_graph_rejected` | **PASS** |
| G-04 | submit → in_review | `test_G04_submit_to_in_review` | **PASS** |
| G-05 | freeze + checksum | `test_G05_freeze_graph_with_frozen_ruleset` | **PASS** |
| G-06 | frozen 不可改 | `test_G06_frozen_graph_not_editable` | **PASS** |
| G-07 | clone 新版本 | `test_G07_clone_new_draft_version` | **PASS** |
| G-08 | deprecated 拒绝 execute | `test_G08_execute_on_deprecated_graph_rejected` | **PASS** |

```bash
uv run pytest src/tests/integration/test_graph_w3.py -k 'G-0' -v
uv run python scripts/gate_cli.py step --step 2 -k 'G-05'
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | apps/api 仅路由；规则在 graph_service | **通过** |
| 写路径 | G-03 阻断未 freeze 的 L2 写 | **通过** |
| 红线 | frozen 不可 PUT（G-06） | **通过** |
| 注释 | graphs.py · error_handlers 文件头 | **通过** |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| G-03 | `POST /v1/execute` on draft | 409 `GRAPH_NOT_FROZEN` | **PASS** |
| G-05 | `POST .../freeze` | status=frozen + checksum | **PASS** |

## 5. 架构与代码质量评估（本 Step）

**通过** — HTTP 与 service 职责清晰；error_handlers 集中映射。

## 6. 结论

**结论：通过**

- 补录 · 对照终轮 42 passed。
- 通过 → **Verify·Step 2**（`verify-1140-step2.md`）
