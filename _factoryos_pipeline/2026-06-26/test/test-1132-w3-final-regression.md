# 终轮全量回归 · W3 Test 兜底验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`（含 W1+W2 存量）
- **命名**：`test-1132-w3-final-regression.md`（HHmm=1132）
- **口令**：`【Test·终轮回归】`（2026-06-26 · W3 交付前）

## 1. 本轮改动面（W3 + 存量）

| 模块 | 路径 | plan | 结论 |
|------|------|------|------|
| 迁移 | `src/server/db/migrations/versions/003_graphs_rulesets.py` | W3 S1 | PASS |
| graph | `os_core/graph_service/` | W3 S1–2 | PASS |
| rule | `os_core/rule_engine/` | W3 S3 | PASS |
| CMV/DSL | `shared_contracts/cmv_registry.py` | W3 S4 | PASS |
| execution 门禁 | `execution_service/service.py` | W3 S4 | PASS |
| API | `routes/graphs.py` · `rulesets.py` · `dsl.py` | W3 S2–4 | PASS |
| 测试 | `test_graph_w3.py` · `test_rule_w3.py` · `test_dsl_w3.py` · `test_execution_e01.py` | Test | PASS |

## 2. W3 AC 全量（+ W1/W2 回归）

| AC ID | 业务验收 | 结果 |
|-------|----------|------|
| G-01～G-08 | Graph 生命周期 | **PASS** ×8 |
| R-01～R-05 | Rule 授权 | **PASS** ×5 |
| D-01～D-03 | DSL registry 门禁 | **PASS** ×3 |
| E-01 | L0 只读 frozen graph | **PASS** |
| E-03/06/07/09 | W2 存量 | **PASS** |
| S-01～S-04 · C-01 | W1 存量 | **PASS** |
| contract · workflow | 契约/红线 | **PASS** |
| 52 P0 其余 | W4+ | **30 pending**（plan 预期） |

```bash
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending'
# → 42 passed

uv run python scripts/gate_cli.py step --step 1 -k 'G-01'   # OK
uv run python scripts/gate_cli.py step --step 2 -k 'G-05'   # OK
uv run python scripts/gate_cli.py step --step 3 -k 'R-01'   # OK
uv run python scripts/gate_cli.py step --step 4 -k 'E-01'   # OK
uv run python scripts/gate_cli.py pr                          # OK
```

## 3. 存量回归

| 域 | 结果 |
|----|------|
| integration 全量（非 pending） | **28/28** |
| contract + workflow | **14/14** |
| **合计** | **42 passed** |
| static quality | **OK** |

## 4. 代码落位（终轮）

| 维度 | 结论 |
|------|------|
| 分层 | **通过** — graph/rule/dsl 在 os_core；API 薄路由 |
| 写路径 | **通过** — G-03 未 freeze → 409；R-01 默认 deny |
| W2 未破坏 | **通过** — E-03/06/07/09 仍绿 |
| 过程 | **需改进（非阻断）** — W3 批量实现；逐步 Test/Verify 已补录（test-1132-stepN · verify-1140-stepN · step-stop-1132-stepN） |

## 5. 接口分区

### 📦 本次新增接口（W3 主要）

| 方法 | 路径 | AC |
|------|------|-----|
| POST/GET/PATCH | `/v1/graphs` · `/v1/graphs/{id}` 等 | G-* |
| POST/GET | `/v1/rulesets` 等 | R-* |
| GET | `/v1/dsl/registry` | D-01 |
| POST | `/v1/execute`（门禁增强） | E-01 · G-03 · R-01 |

### 🔁 字段调整

**无** — W3 新增 Graph/Rule/DSL 域；W2 execute/audit/evidence 响应字段未破坏性变更。

## 6. 结论

**结论：通过**

- W3 plan AC 子集 **G/R/D/E-01** 全绿 + W1/W2 存量 **42/42**
- `gate pr` **OK** · 四步 `gate step` **OK**
- 30 P0 pending（E-02/04 等 · plan 留 W4+）
- 允许 `phase: DELIVERY` 后 `gate delivery` → **可以 commit**
