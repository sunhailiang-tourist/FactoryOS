# Step 4 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 4
- **命名**：`test-0936-step4-regression.md`
- **口令**：`Step 4 单步验收`（对照 `step-stop-1105-step4.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `package_service/service.py` | `import_implementation_package` | Step4 | ✅ | PASS |
| `package/controllers/package.py` | POST `/v1/packages/import` | Step4 | ✅ | PASS |
| `tenant_config_store.py` | overrides · ensure_system_relation/entitlement | Step4 | ✅ | PASS |
| `tenant_service/service.py` | `connector_overrides` | Step4 P-03 | ✅ | PASS |
| `tenant/controllers/tenant.py` | PUT settings 接受 overrides | Step4 | ✅ | PASS |
| `connector_sdk/connect_test.py` | `resolve_pack_base_url` · connect test | Step4 P-03 | ✅ | PASS |
| `api/modules/integration/` | POST `/v1/integration/connect/test` | Step4 | ✅ | PASS |
| `api/router/v1/registry.py` | integration 域 | Step4 | ✅ | PASS |

**未改动（符合 Step4 范围）**：MCP Gateway HTTP — 留 Step5。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| P-02 | export → import tenant B → health 200 | `test_P02_*` | **PASS** |
| P-03 | PUT overrides → connect/test base_url | `test_P03_*` | **PASS** |
| P-01 | Step3 回归 | `test_P01_*` | **PASS** |
| T-01 · T-03 | Step1–2 回归 | shadow · connector | **PASS** |
| import_boundaries · repo-structure | 门禁 | workflow harness | **PASS** |
| 存量 | `-m 'not pending'` 排除 Step5–7 红测 | 98 passed · 1 skipped | **PASS** |

```bash
uv run pytest src/tests/integration/test_package_w7.py -v   # 3 passed (P-01～P-03)
uv run pytest src/tests/integration/test_shadow_w7.py src/tests/integration/test_connector_t03_w7.py -q  # 2 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes \
  src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green -q  # 2 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_mcp_w7.py \
  --ignore=src/tests/integration/test_dsl_e08_w7.py \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 98 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | import 内核 · connect/test 在 connector_sdk · API 薄路由 | ✅ |
| 写路径 | import 写 Graph/Rule/relations · 非 Legacy 直写 | ✅ |
| P-03 | overrides 存 profile_json · runtime 合并 base_url | ✅ |
| 注释 | package · tenant · connect_test 齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| P-02 | `POST /v1/packages/import` | export default → import tenant B | **PASS** |
| P-03 | PUT settings + `POST /v1/integration/connect/test` | override base_url | **PASS** |

**P-02 证据**：import 后 `GET /v1/connectors/conn-mock/health?tenant_id=<B>` → status ok/degraded

**P-03 证据**：connect/test 返回 `base_url` 或 `resolved_base_url` = override URL

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 幂等 | import 跳过已存在 graph/ruleset · relations upsert |
| 存量修复 | Test 同步 router **14 域**（integration） |

## 6. 结论

**结论：通过**

- Step 4 目标 **P-02 · P-03 绿** · P-01 回归绿 · **存量 98/98 绿**

**下一步**：**Verify 新会话** `【Verify回合】Step 4` → `./scripts/gate step --step 4 -k 'P-02'`
