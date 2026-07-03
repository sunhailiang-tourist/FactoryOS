# Step 5 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 5
- **命名**：`test-0942-step5-regression.md`
- **口令**：`Step 5 单步验收`（对照 `step-stop-1120-step5.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `mcp_gateway/service.py` | `handle_mcp_json_rpc` · list/call | Step5 内核 | ✅ | PASS |
| `mcp_gateway/__init__.py` | 公开 API | Step5 | ✅ | PASS |
| `api/modules/mcp/` | POST `/mcp/v1/{tenantId}` 薄路由 | Step5 | ✅ | PASS |
| `agent_orchestrator/service.py` | `source=mcp` · verb 参数 | Step5 复用 | ✅ | PASS |
| `tenant_config_store.py` | `list_licensed_pack_ids` | M-01 | ✅ | PASS |
| `api/router/v1/registry.py` | mcp 域登记 | Step5 | ✅ | PASS |
| `check_import_boundaries.py` | mcp_gateway 白名单 | 静态 | ✅ | PASS |

**未改动（符合 Step5 范围）**：OAuth 2.1 公网暴露 — 留 Y2；D-04/E-08 — 留 Step6。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| M-01 | tools/list → 已授权 CMV | `test_M01_*` | **PASS** |
| M-02 | tools/call → DslPlan · Legacy 0 写 | `test_M02_*` | **PASS** |
| P-01～P-03 · T-01 · T-03 | Step1–4 回归 | package · shadow · connector | **PASS** |
| import_boundaries · repo-structure | 门禁 | workflow harness | **PASS** |
| 存量 | `-m 'not pending'` 排除 Step6–7 红测 | 100 passed · 1 skipped | **PASS** |

```bash
uv run pytest src/tests/integration/test_mcp_w7.py -v   # 2 passed
uv run pytest src/tests/integration/test_package_w7.py src/tests/integration/test_shadow_w7.py src/tests/integration/test_connector_t03_w7.py -q  # 5 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_dsl_e08_w7.py \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 100 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | API 薄路由 · JSON-RPC 在 mcp_gateway · 不写 Legacy | ✅ R-01 |
| 路径 | 唯一 HTTP 面 `/mcp/v1/{tenantId}` | ✅ plan §2.3 |
| M-01 | licensed packs → Blueprint ops → tools | ✅ |
| M-02 | Graph/Rule 门禁 → `create_plan(source=mcp)` | ✅ |
| 注释 | service · README · mcp 模块齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| M-01 | POST `/mcp/v1/default` tools/list | default tenant | **PASS** |
| M-02 | tools/call GOVERNED_WRITE | frozen graph · intent | **PASS** |

**M-02 证据**：`source` ∈ {agent, mcp} · `mock_legacy` 写计数不变

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| Y2 预留 | 鉴权可插拔（W7 internal pass）；路由不变 |
| 存量修复 | Test 同步 router **15 域**（mcp） |

## 6. 结论

**结论：通过**

- Step 5 目标 **M-01 · M-02 绿** · Step1–4 回归绿 · **存量 100/100 绿**

**下一步**：**Verify 新会话** `【Verify回合】Step 5` → `./scripts/gate step --step 5 -k 'M-01'`
