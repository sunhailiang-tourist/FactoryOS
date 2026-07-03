# Step 3 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 3
- **命名**：`test-0923-step3-regression.md`
- **口令**：`Step 3 单步验收` / `【Test·Step 3 验收】`

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `os_core/package_service/service.py` | `export_implementation_package` | Step3 内核 | ✅ | PASS |
| `os_core/package_service/__init__.py` | 包导出 | Step3 | ✅ | PASS |
| `os_core/package_service/README.md` | 模块说明 | 新模块门禁 | ✅ | PASS |
| `graph_service/store.py` | `list_graphs_by_tenant` | Step3 数据源 | ✅ | PASS |
| `rule_engine/store.py` | `list_rulesets_for_graph_ids` | Step3 数据源 | ✅ | PASS |
| `platform_registry/pack_store.py` | registry_key 查询 | Step3 | ✅ | PASS |
| `api/modules/package/` | POST `/v1/packages/export` 薄路由 | Step3 | ✅ | PASS |
| `api/router/v1/registry.py` | package 域登记 | Step3 | ✅ | PASS |
| `registry.py` · repo-structure | 13 内核模块 | 治理 | ✅ | PASS |

**未改动（符合 Step3 范围）**：`POST /v1/packages/import` · Override — 留 Step4（P-02/P-03）。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| P-01 | export → graphs · rulesets · connector_configs | `test_P01_*` | **PASS** |
| P-01 | ImplementationPackage required 字段 | schema 对账 | **PASS** |
| T-01 · T-03 | Step1–2 回归 | shadow · connector | **PASS** |
| import_boundaries · repo-structure | 门禁 | workflow harness | **PASS** |
| 存量 | `-m 'not pending'` 排除 P-02+ 红测 | 96 passed · P-02/P-03 预期红 | **PASS** |

```bash
uv run pytest src/tests/integration/test_package_w7.py -k 'P-01' -v   # 1 passed
uv run pytest src/tests/integration/test_shadow_w7.py src/tests/integration/test_connector_t03_w7.py src/tests/integration/test_license_t02_w6.py -q  # 3 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes \
  src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green -q  # 2 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_mcp_w7.py \
  --ignore=src/tests/integration/test_dsl_e08_w7.py \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 96 passed · 2 failed (P-02/P-03) · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | API 薄路由 · 聚合在 package_service 内核 | ✅ |
| 写路径 | export 只读 DB · 不写 Legacy | ✅ |
| 契约 | 对齐 `ImplementationPackage.schema.json` | ✅ |
| MCP 预留 | 内核 `export_implementation_package` 可供 Step5 复用 | ✅ |
| 注释 | service · README · store 函数头齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| P-01 | `POST /v1/packages/export` | tenant=default · delivery=D1 | **PASS** |

**P-01 出参（HTTP · 摘要）**：

```json
{
  "package_id": "<uuid>",
  "tenant_id": "default",
  "version": "v1.0.0",
  "delivery": "D1",
  "exported_at": "<iso8601>",
  "graphs": ["..."],
  "rulesets": ["..."],
  "connector_configs": [{ "pack_id": "conn-mock", "registry_key": "..." }]
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 数据源 | graph/rule/connector 三源聚合，无重复 HTTP 逻辑 |
| 存量修复 | Test 同步 13 内核模块 · 13 API 域（package） |

## 6. 结论

**结论：通过**

- Step 3 目标 **P-01 绿** · Step1–2 回归绿 · **存量 96/96 绿**（P-02/P-03 除外）

**下一步**：**Verify 新会话** `【Verify回合】Step 3` → `./scripts/gate step --step 3 -k 'P-01'`
