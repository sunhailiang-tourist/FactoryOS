# Verify 回合：W7 Step 1 — tenant shadow_mode（T-01）

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-1705-step1.md` · `test-1736-step1-regression.md`（复验，初验 `test-1730`）

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-1705-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-1736-step1-regression.md`
- **对照 AC**：T-01（harness `-k 'T-01'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 1 范围 | **Pass** | tenant_service 内核 · API 薄路由 · execution effective_shadow；无 MCP/Package |
| 2 | 写路径 / 红线 | **Pass** | `effective_shadow = dry_run ∨ tenant_shadow` · L2 simulated · Legacy 0 写 |
| 3 | AC 可测 | **Pass** | `test_T01_tenant_shadow_mode_l2_write_simulated_no_legacy[T-01]` 绿 |
| 4 | 无重复逻辑 | **Pass** | shadow 真源仅在 `tenant_service.resolve_shadow_mode` |
| 5 | 注释四要素 | **Pass** | tenant_service · execution 钩子 · tenant controller · README |
| 6 | MCP 预留 | **Pass** | 内核 REST/MCP 共用；API 层不判 shadow |
| 7 | import_boundaries | **Pass** | execution → tenant_service 矩阵 · script 绿 |
| 8 | repo-structure | **Pass** | 12 内核模块（Test 复验） |
| 9 | 静态质量 | **Fail** | ruff I001/E501 · `execution_service/service.py`；另 W7 红测文件 import 排序 |

## 范围边界

| 项 | 评估 |
|----|------|
| 初验 import_boundaries / PATH-SNAPSHOT | **已关闭**（Test 复验） |
| `DEFAULT_PACK_ID` 硬编码 | **备忘** — 与 W6 一致 |
| W7 Step2–7 红测文件 ruff | **需 Dev 修** — 阻塞全仓 static quality |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_shadow_w7.py -k 'T-01' -v   # 1 passed
.venv/bin/python scripts/check_import_boundaries.py                      # OK
.venv/bin/python scripts/check_static_quality.py                          # FAIL（4 ruff）
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'T-01'             # 待执行
```

**static quality 明细**：

- `execution_service/service.py:8` — I001 import 块未排序（`tenant_service` 插入位置）
- `execution_service/service.py:174` — E501 行宽 109 > 100
- `test_package_w7.py` · `test_negative_w7.py` — I001（W7 编码前红测，非 Step1 业务但阻塞 gate）

联动链：`step-stop-1705-step1.md` → `test-1736-step1-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：需改进

阻断理由（若有）：T-01 行为与分层 **通过**，但 **static quality 未绿**，`gate step 1` 无法全绿。

## 建议

1. Dev 修 `execution_service/service.py` import 排序 + audit payload 换行（E501）。
2. 对 W7 红测文件跑 `ruff check --fix` 或手动排序 import。
3. 修补后复验 Verify → `gate step --step 1 -k 'T-01'`。
