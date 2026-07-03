# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 1
- **命名**：`test-1730-step1-regression.md`
- **口令**：`【Test·Step 1 验收】`（对照 `step-stop-1705-step1.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `os_core/tenant_service/` | get/update/resolve_shadow_mode | Step1 内核 | ✅ | PASS |
| `platform_registry/tenant_config_store.py` | upsert_tenant_settings | Step1 | ✅ | PASS |
| `execution_service/service.py` | effective_shadow = dry_run ∨ tenant_shadow | Step1 | ✅ | PASS |
| `api/modules/tenant/` | GET/PUT settings 薄路由 | Step1 | ✅ | PASS |
| `api/router/v1/registry.py` | tenant 域登记 | Step1 | ✅ | PASS |
| `registry.py` | 登记 tenant_service（12 内核） | Step1 | ✅ | PASS |
| `contracts/repo-structure.yaml` | kernel module_count 12 | 结构门禁 | ✅ | PASS |
| `check_import_boundaries.py` | execution→tenant_service 矩阵 | **缺** | ❌ | **FAIL** |
| `.cursor/factoryos/PATH-SNAPSHOT.md` | 与 repo-structure 同步 | 结构门禁 | ❌ | **过期** |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| T-01 | PUT shadow_mode → L2 simulated · Legacy 0 写 | `test_T01_*` | **PASS** |
| T-01 | ExecutionRecord shadow_mode=true | `test_T01_*` | **PASS** |
| import_boundaries | execution_service → tenant_service | `test_import_boundaries` | **FAIL** |
| 内核 registry | 12 modules | `check_kernel_registry` | **PASS** |
| repo-structure | PATH-SNAPSHOT 同步 | `check_repo_structure` | **FAIL** |
| 存量 W1–W6 | 排除 W7 Step2–7 红测 | 90 passed · 3 workflow 红 | **需改进** |

```bash
uv run pytest src/tests/integration/test_shadow_w7.py -k 'T-01' -v   # 1 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # FAIL
uv run python scripts/check_kernel_registry.py  # OK: 12 modules
uv run python scripts/check_repo_structure.py   # FAIL: PATH-SNAPSHOT 过期
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | tenant_service 内核 · API 薄路由 · MCP 可复用 | ✅ |
| 写路径 | effective_shadow 时 L2 不写 Legacy | ✅ R-11 / Shadow 规格 |
| 真源 | resolve_shadow_mode 单点 · execution 合并 dry_run | ✅ |
| 注释 | tenant_service · controller · README | ✅ |
| 门禁 | import 矩阵未补 tenant_service | ❌ 需 Dev 修 |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| T-01 | PUT `/v1/tenants/default/settings` | shadow_mode=true | **PASS** |
| T-01 | POST `/v1/execute` dry_run=false | L2 GOVERNED_WRITE | **PASS** |

**T-01 出参（HTTP · 摘要）**：

```json
{
  "status": "simulated",
  "shadow_mode": true,
  "dry_run": false
}
```

Legacy `mock_legacy` 写计数前后不变。

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| MCP 预留 | tenant_service 内核 API 可供 Step5 mcp_gateway 复用 — 对齐 plan §2 |
| 存量修复 | Test 已同步 registry 12 内核 · router 12 域 |
| 阻断项 | `check_import_boundaries.py` 须补 `tenant_service` 条目及 execution_service.allowed |

## 6. Dev 须修（复验前）

1. `scripts/check_import_boundaries.py` — `execution_service.allowed` 增加 `tenant_service`；登记 `tenant_service` 包矩阵
2. 运行 `./scripts/check_repo_structure.py` 同步 `.cursor/factoryos/PATH-SNAPSHOT.md`

## 7. 结论

**结论：需改进**

- Step 1 目标 **T-01 绿** · 分层与 shadow 行为正确
- **存量 workflow 红**：import_boundaries · PATH-SNAPSHOT — Dev 修后 Test 复验 → Verify

**下一步**：Dev 修门禁 → **Test 复验 Step 1** → `【Verify回合】Step 1` → `./scripts/gate step --step 1 -k 'T-01'`
