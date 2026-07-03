# 终轮全量回归 · Test 兜底验收报告 · W7 Gate 0（复验）

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`（全 Step 1–7）
- **命名**：`test-1148-final-regression.md`
- **口令**：`整体回归w7` · `【Test·终轮回归】`

## 1. W7 AC 专项（13 cases）

| AC ID | Step | 文件 | 结果 |
|-------|------|------|------|
| T-01 | 1 | `test_shadow_w7.py` | **PASS** |
| T-03 | 2 | `test_connector_t03_w7.py` | **PASS** |
| P-01 | 3 | `test_package_w7.py` | **PASS** |
| P-02/P-03 | 4 | `test_package_w7.py` | **PASS** |
| M-01/M-02 | 5 | `test_mcp_w7.py` | **PASS** |
| D-04/E-08 | 6 | `test_dsl_e08_w7.py` | **PASS** |
| N-01～N-04 | 7 | `test_negative_w7.py` | **PASS** |

```bash
uv run pytest src/tests/integration/test_shadow_w7.py \
  src/tests/integration/test_connector_t03_w7.py \
  src/tests/integration/test_package_w7.py \
  src/tests/integration/test_mcp_w7.py \
  src/tests/integration/test_dsl_e08_w7.py \
  src/tests/integration/test_negative_w7.py -v
# 13 passed in 0.99s
```

## 2. 存量全量回归

```bash
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 107 passed in 18.93s
```

| 域 | 结果 |
|----|------|
| contract + workflow + integration | **107 passed** |
| pending 排除 | M-03 等 W8+ AC 仍 pending（符合 Gate 0 范围） |

## 3. 静态与结构门禁

```bash
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes \
  src/tests/workflow/test_registry_harness.py -q
# 13 passed
```

| 项 | 结果 |
|----|------|
| import_boundaries | **PASS** |
| registry harness（13 内核 · 15 API 域） | **PASS** |

## 4. gate delivery 复验

```bash
./scripts/gate delivery
# Gate delivery OK（终轮回归 · 可提示 commit）
```

## 5. 代码落位（终轮）

| 维度 | 结论 |
|------|------|
| 模块边界 | **通过** — tenant · package · mcp · param_safety 落 os_core |
| 写路径红线 | **通过** — MCP/Agent 无 Legacy 直写 |
| 多租户安全 | **通过** — N-03 tenant 隔离 · N-04 param 扫描 |
| 与 plan 一致 | **通过** — 无真实 ERP/OAuth 越 scope |

## 6. 结论

**结论：通过**

- W7 七步 AC **13/13 绿** · 存量 **107/107 绿** · 结构门禁 **13/13 绿**
- Gate 0 plan §3 pending AC 已清零（W7 范围）

**下一步**：`./scripts/gate pr` → 人工 tag `core-v1.0.0` · commit
