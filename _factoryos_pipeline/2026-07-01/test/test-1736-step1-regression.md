# Step 1 单步验收 · Test 复验报告

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md` · Step 1
- **命名**：`test-1736-step1-regression.md`
- **口令**：`Test 复验 Step 1`（初验 `test-1730-step1-regression.md` · 需改进项已修）

## 1. 复验项（初验阻断 → 本轮）

| 项 | 初验 | 复验 | 证据 |
|----|------|------|------|
| `check_import_boundaries` | FAIL | **PASS** | `tenant_service` 矩阵 · execution 可 import |
| `PATH-SNAPSHOT.md` | 过期 | **PASS** | `check_repo_structure` 绿 |
| 内核 12 模块 · router 12 域 | Test 已同步 | **PASS** | registry harness |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| T-01 | shadow_mode L2 simulated · Legacy 0 写 | `test_T01_*` | **PASS** |
| import_boundaries | execution → tenant_service | `test_import_boundaries` | **PASS** |
| repo-structure | PATH-SNAPSHOT 同步 | `test_repo_structure_harness` | **PASS** |
| 内核 registry | 12 modules | `test_os_core_registry_*` | **PASS** |
| 存量 W1–W6 + T-01 | 排除 W7 Step2–7 红测 | 95 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_shadow_w7.py -k 'T-01' -v   # 1 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' \
  --ignore=src/tests/integration/test_connector_t03_w7.py \
  --ignore=src/tests/integration/test_package_w7.py \
  --ignore=src/tests/integration/test_mcp_w7.py \
  --ignore=src/tests/integration/test_dsl_e08_w7.py \
  --ignore=src/tests/integration/test_negative_w7.py -q
# 95 passed
```

## 3. 代码落位合理性（复验确认）

| 维度 | 结论 |
|------|------|
| 分层 | tenant_service 内核 · API 薄路由 · MCP 可复用 resolve_shadow_mode |
| 写路径 | effective_shadow 时 L2 不写 Legacy |
| 门禁 | import 矩阵与 repo-structure 与实现一致 |

## 4. 结论

**结论：通过**

- 初验 **需改进** 项已全部关闭 · **T-01 绿** · **存量 95/95 绿**

**下一步**：**Verify 新会话** `【Verify回合】Step 1` → `./scripts/gate step --step 1 -k 'T-01'`
