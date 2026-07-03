# W1～W8 全量复盘（复验）· Test 兜底验收报告 · 治理改动后

- **范围**：AC-BASE-001 **52 P0 + M-03** · 本轮增量：trace_context 契约单测 · registry/README 治理
- **命名**：`test-1711-w1-w8-full-regression-reverify.md`
- **口令**：`W1~W8 再次回归全量复盘收尾`（治理改动后复验）

## 1. 本轮 git diff 改动面

| 路径 | 变更 | 业务影响 | 结论 |
|------|------|----------|------|
| `src/tests/contract/test_trace_context.py` | **新增** 7 contract cases | M-03 解析单测 | ✅ 无业务逻辑变更 |
| `os_core/registry.py` | mcp_gateway metadata · audit_service depends | 文档/registry 对齐 | ✅ PASS |
| `api/router/v1/registry.py` | mcp 域 usage 增 M-03 | 元数据 | ✅ PASS |
| `os_core/README.md` · `mcp_gateway/README.md` · `shared_contracts/README.md` | 文档 | 无运行时变更 | ✅ PASS |
| `.cursor/factoryos/MODULE-MAP.md` · `AC-P0-INDEX.md` | 索引 | 无运行时变更 | ✅ PASS |

**无** `execution_service` / `mcp_gateway/service.py` 等业务实现变更。

## 2. 执行摘要

| 维度 | 上次 (1656) | 本轮复验 | 结果 |
|------|-------------|----------|------|
| 全 suite | 109 passed | **116 passed**, 2 skipped | **PASS** (+7 trace contract) |
| integration | 67 passed | **67 passed** | **PASS** |
| contract | 13 passed | **20 passed** | **PASS** |
| workflow | 29 passed | **29 passed**, 1 skipped | **PASS** |
| pending AC | 0 | **0** | **PASS** |
| `./scripts/gate pr` | OK | **OK** | **PASS** |
| `./scripts/gate delivery` | OK | ⚠️ `phase≠DELIVERY` | harness 阻断（非 pytest） |

```bash
uv run pytest src/tests/ -q
# 116 passed, 2 skipped in 16.97s
uv run pytest src/tests/integration/ -q    # 67 passed
uv run pytest src/tests/contract/ -q         # 20 passed
./scripts/gate pr                            # OK
```

## 3. W1～W8 业务链路（复验全绿）

| 迭代 | 代表测试 | 结果 |
|------|----------|------|
| W1 规模/Registry | `test_scale_s01_s04` · `test_registry_adr008` | **PASS** |
| W2 Audit/Execution | `test_audit_e03` · `test_execution_e0*` | **PASS** |
| W3 Graph/Rule/DSL | `test_graph_w3` · `test_rule_w3` · `test_dsl_w3` | **PASS** |
| W4 Connector | `test_connector_blueprint_w4` · `test_connector_runtime_w4` | **PASS** |
| W5 Agent/Harness | `test_agent_orchestrator_w5` · `test_harness_w5` | **PASS** |
| W6 License/Reconcile | `test_license_w6*` · `test_reconciliation_w6` | **PASS** |
| W7 Shadow/Package/MCP/负向 | `test_shadow_w7` · `test_package_w7` · `test_mcp_w7` · `test_negative_w7` | **PASS** |
| W8 M-03 trace | `test_mcp_w8` · **`test_trace_context`** | **PASS** |

## 4. M-03 双层验证（本轮重点）

| 层 | 用例 | 结果 |
|----|------|------|
| contract | traceparent 合法/非法 · mcp_meta 入口 | **7/7 PASS** |
| integration | plan.trace_id · audit correlation_id · no-meta | **2/2 PASS** |

## 5. 结构与红线

| 项 | 结果 |
|----|------|
| 13 内核 · 15 API 域 harness | **PASS** |
| import_boundaries | **PASS** |
| E-08 Agent 禁直写 | **PASS** |
| 主写路径 N-01～N-04 | **PASS** |

## 6. 结论

**结论：通过**

- **W1～W8 业务链路复验 116/116 pytest 绿**（2 skipped 为 registry 空 pending + workflow skip）
- 治理改动（文档/registry/trace 单测）**未破坏存量链路**
- `gate pr` **绿** · commit 前须 Dev 将 `workflow_state.phase` 恢复 **`DELIVERY`** 再跑 `gate delivery`

**下一步**：`phase: DELIVERY` → `gate delivery` → 用户 **`可以提交`** → tag `core-v1.0.0`
