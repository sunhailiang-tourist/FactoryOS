# Verify 整体验收：W7 — Gate 0（Shadow · Package · MCP · DSL · 负向安全）

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **summary**：`change-summary-1145-w7-gate0-gip-mcp.md` · **终轮**：`test-1140-final-regression.md`

- **分支**：`dev_sunhailiang_core_260624`
- **验收口令**：W7 整体验收
- **日期**：2026-07-01

## 1. 七步联动链（Dev → Test → Verify → gate step）

| Step | AC | step-stop | Test 回归 | Verify（最终） | gate step |
|------|-----|-----------|-----------|----------------|-----------|
| 1 | T-01 | `step-stop-1705-step1.md` | `test-1736-step1-regression.md` | `verify-1741-step1.md` 通过 | ✅ |
| 2 | T-03 | `step-stop-0950-step2.md` | `test-1750-step2-regression.md` | `verify-1751-step2.md` 通过 | ✅ |
| 3 | P-01 | `step-stop-1030-step3.md` | `test-0923-step3-regression.md` | `verify-0924-step3.md` 通过 | ✅ |
| 4 | P-02/P-03 | `step-stop-1105-step4.md` | `test-0936-step4-regression.md` | `verify-0940-step4.md` 通过 | ✅ |
| 5 | M-01/M-02 | `step-stop-1120-step5.md` | `test-0942-step5-regression.md` | `verify-1049-step5.md` 通过 | ✅ |
| 6 | D-04/E-08 | `step-stop-1205-step6.md` | `test-1107-step6-regression.md` | `verify-1112-step6.md` 通过 | ✅ |
| 7 | N-01～N-04 | `step-stop-1215-step7.md` | `test-1122-step7-regression.md` | `verify-1128-step7.md` 通过 | ✅ |

## 2. W7 AC 全量行为验收（本轮复跑）

| AC ID | Step | 验收项 | pytest | 结果 |
|-------|------|--------|--------|------|
| T-01 | 1 | shadow_mode → L2 simulated · Legacy 0 写 | `test_shadow_w7` | **PASS** |
| T-03 | 2 | CONNECTOR_NOT_CONFIGURED 403 | `test_connector_t03_w7` | **PASS** |
| P-01 | 3 | Package export graphs/rulesets/connectors | `test_package_w7` | **PASS** |
| P-02 | 4 | import tenant B · health 200 | `test_package_w7` | **PASS** |
| P-03 | 4 | override base_url · connect/test | `test_package_w7` | **PASS** |
| M-01 | 5 | tools/list 已授权 CMV | `test_mcp_w7` | **PASS** |
| M-02 | 5 | tools/call → DslPlan · Legacy 0 写 | `test_mcp_w7` | **PASS** |
| D-04 | 6 | L2 无 compensator → 422 | `test_dsl_e08_w7` | **PASS** |
| E-08 | 6 | orchestrator 无 connector 写路径 | `test_dsl_e08_w7` | **PASS** |
| N-01 | 7 | 无 internal execute 旁路 | `test_negative_w7` | **PASS** |
| N-02 | 7 | checksum 篡改 freeze 拒绝 | `test_negative_w7` | **PASS** |
| N-03 | 7 | 跨 tenant GET execution → 403 | `test_negative_w7` | **PASS** |
| N-04 | 7 | SQL injection params → 422 | `test_negative_w7` | **PASS** |

**W7 专项集成**：13/13 passed（本轮复跑）

## 3. 存量与 Gate 0 终轮

| 检查 | 命令/证据 | 结果 |
|------|-----------|------|
| 全量回归 | `pytest … -m 'not pending'` | **107 passed** |
| gate delivery | `gate_cli.py delivery` | **OK** · `03-49_gate-delivery_*` |
| gate pr | `gate_cli.py pr` | **OK** · harness full + static + deptry |
| 内核模块 | `repo-structure.yaml` | **13 modules** |
| W7 pending AC | plan §3 14 项 | **ACTIVE 注册 · 无 pending 占位** |
| static quality | ruff · pyright | **OK** |
| import_boundaries | check script | **OK** |

## 4. 架构与红线（整体验收）

| 维度 | 结论 | 说明 |
|------|------|------|
| 分层 | **Pass** | 新内核 tenant/package/mcp + API 薄路由 |
| 写路径 R-01 | **Pass** | MCP/Agent 无 Legacy 直写；Shadow 不写 Legacy |
| plan 边界 | **Pass** | 无真实 ERP · 无 OAuth 公网 · Y2 扩展点保留 |
| 注释/README | **Pass** | 新模块均有 README + 函数头 |
| W1–W6 存量 | **Pass** | license/reconciliation/harness 等未回归破坏 |

## 5. 已知备忘（非阻断）

| 项 | 说明 |
|----|------|
| `DEFAULT_PACK_ID` 硬编码 | W7+ 从 relation 解析 |
| `verify_mcp_access` OAuth | Y2 同函数扩展 |
| M-03 traceparent | P1 · W7 未交付 |
| tag `core-v1.0.0` | **人工** · plan §Gate 0 判定 |

## 6. 机械门禁（本轮复跑）

```bash
.venv/bin/pytest src/tests/integration/test_*_w7.py -v                    # 13 passed
.venv/bin/pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q  # 107 passed
.venv/bin/python scripts/gate_cli.py delivery                             # OK
.venv/bin/python scripts/gate_cli.py pr                                   # OK
```

## 7. 结论（必填）

结论：**通过**

W7 Gate 0 整体验收 **通过**：七步联动链全绿 · 14 项 plan AC 行为绿 · 终轮 107 pytest 绿 · `gate delivery` · `gate pr` 绿。

**可提交**：summary 已落盘 · `phase: DELIVERY` · 用户 **`可以 commit`** 后开 PR。

阻断理由（若有）：无

## 8. 建议

1. commit + PR（标题见 `change-summary-1145-w7-gate0-gip-mcp.md`）。
2. 人工 tag `core-v1.0.0` 前对照 AC-BASE-001 §十四 checklist。
3. W8：M-03 · 真实 Connector · MCP OAuth 等 Y2 项按路线图续开。
