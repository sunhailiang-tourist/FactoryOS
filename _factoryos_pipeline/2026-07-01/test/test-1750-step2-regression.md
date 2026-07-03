# Step 2 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 2
- **命名**：`test-1750-step2-regression.md`
- **口令**：`【Test·Step 2 验收】`（对照 `step-stop-0950-step2.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `connector_sdk/registry.py` | `assert_tenant_connector_configured` | Step2 | ✅ | PASS |
| `platform_registry/tenant_config_store.py` | system_relation · pack entitlements | Step2 | ✅ | PASS |
| `license_service/service.py` | `tenant_pack_entitlements` 真源 | Step2 | ✅ | PASS |
| `execution_service/service.py` | connector → license 顺序门禁 + audit | Step2 | ✅ | PASS |
| `check_import_boundaries.py` | license → platform_registry | Step2 | ✅ | PASS |

**未改动（符合 Step2 范围）**：Package · MCP API — 留 Step3–5。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| T-03 | 未配置 connector → 403 CONNECTOR_NOT_CONFIGURED | `test_T03_*` | **PASS** |
| T-01 | Step1 回归 | `test_shadow_w7` | **PASS** |
| T-02 · workflow | W6 license 回归 | `test_license_t02_w6` · `test_license_w6_step1` | **PASS** |
| import_boundaries | 矩阵绿 | `test_import_boundaries` | **PASS** |
| 存量 | `-m 'not pending'` 排除 Step3–7 红测 | 95 passed · 1 skipped | **PASS** |

```bash
uv run pytest src/tests/integration/test_connector_t03_w7.py -k 'T-03' -v   # 1 passed
uv run pytest src/tests/integration/test_shadow_w7.py src/tests/integration/test_license_t02_w6.py src/tests/integration/test_license_w6_step1.py -q  # 3 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_package_w7.py \
  --ignore=src/tests/integration/test_mcp_w7.py \
  --ignore=src/tests/integration/test_dsl_e08_w7.py \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 95 passed · 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | connector 门禁在 registry · license 读 tenant_config_store | ✅ |
| 门禁顺序 | connector 配置 → license → graph → rule | ✅ |
| 写路径 | T-03 在 L2 写前拦截 · audit `execute.failed` | ✅ |
| 红线 | 无 silent no-op · 403 显式错误码 | ✅ |
| 注释 | registry · license · store 函数头齐全 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| T-03 | `POST /v1/execute` | tenant=tenant-connector-missing-w7 | **PASS** |

**T-03 出参（HTTP · 摘要）**：

```json
{
  "code": "CONNECTOR_NOT_CONFIGURED",
  "message": "Connector pack conn-mock not configured for tenant tenant-connector-missing-w7"
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 真源升级 | license 从 W6 内存 dict → `tenant_pack_entitlements`；T-02 仍绿 |
| 可维护性 | `has_system_relation_for_pack` 与 blueprint 加载解耦，语义清晰 |

## 6. 结论

**结论：通过**

- Step 2 目标 **T-03 绿** · Step1/T-02 回归绿 · **存量 95/95 绿**

**下一步**：**Verify 新会话** `【Verify回合】Step 2` → `./scripts/gate step --step 2 -k 'T-03'`
