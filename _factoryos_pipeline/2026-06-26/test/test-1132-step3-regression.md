# Step 3 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md` · Step 3
- **命名**：`test-1132-step3-regression.md`（HHmm=1132 · 补录）
- **口令**：`【Test·Step 3 验收】`（对照 `step-stop-1132-step3.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `src/os_core/rule_engine/` | 新增 | evaluate + CRUD | ✅ | PASS |
| `src/apps/api/routes/rulesets.py` | 新增 | 薄 HTTP | ✅ | PASS |
| `src/tests/integration/test_rule_w3.py` | 新增 | R-01～R-05 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| R-01 | 默认 deny | `test_R01_default_deny_no_matching_rule` | **PASS** |
| R-02 | allow 匹配 | `test_R02_allow_rule_passes` | **PASS** |
| R-03 | deny 优先 | `test_R03_deny_priority_over_allow` | **PASS** |
| R-04 | 版本不匹配 | `test_R04_ruleset_graph_version_mismatch` | **PASS** |
| R-05 | frozen 不可改 | `test_R05_frozen_ruleset_not_editable` | **PASS** |

```bash
uv run pytest src/tests/integration/test_rule_w3.py -v
uv run python scripts/gate_cli.py step --step 3 -k 'R-01'
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | evaluate 纯函数 · service 编排 | **通过** |
| 写路径 | R-01 默认 deny → execute 403 | **通过** |
| 红线 | 无 bypass execution 门禁 | **通过** |
| 注释 | rule_engine README 齐全 | **通过** |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| R-01 | `POST /v1/execute` operator | 403 `RULE_DENIED` | **PASS** |

## 5. 架构与代码质量评估（本 Step）

**通过** — evaluate 可单测；store 与 HTTP 分离。

## 6. 结论

**结论：通过**

- 补录 · 对照终轮 42 passed。
- 通过 → **Verify·Step 3**（`verify-1140-step3.md`）
