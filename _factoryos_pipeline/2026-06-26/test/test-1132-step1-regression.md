# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md` · Step 1
- **命名**：`test-1132-step1-regression.md`（HHmm=1132 · 补录）
- **口令**：`【Test·Step 1 验收】`（对照 `step-stop-1132-step1.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `src/server/db/migrations/versions/003_graphs_rulesets.py` | 新增 | Step1 migration | ✅ | PASS |
| `src/server/os_core/graph_service/` | 新增 | graph CRUD 内核 | ✅ | PASS |
| `src/tests/integration/w3_helpers.py` | 新增 | 测试夹具 | ✅ | PASS |
| `src/tests/integration/test_graph_w3.py` | 新增 | G-01 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项（业务一句话） | pytest / 证据 | 结果 |
|-------|----------------------|---------------|------|
| G-01 | 创建 draft graph | `test_G01_create_draft_graph[G-01]` | **PASS** |
| harness | gate step 1 | `-k 'G-01'` | **PASS** |
| workflow | import_boundaries | contract/workflow | **PASS** |

```bash
uv run pytest src/tests/integration/test_graph_w3.py -k G-01 -v
uv run python scripts/gate_cli.py step --step 1 -k 'G-01'
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | 业务在 `os_core/graph_service`；无 apps 写规则 | **通过** |
| 写路径 | Graph 表 INSERT/UPDATE；无 Legacy 写 | **通过** |
| 红线 | R-01 无关本步 | **通过** |
| 注释 | README + store/service 文件头 | **通过** |
| 模块治理 | graph_service 有 README | **通过** |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| G-01 | `POST /v1/graphs` | 入参 sample_graph_body → 201 draft | **PASS** |

**入参 JSON（G-01）**：

```json
{
  "graph_id": "graph-g01",
  "version": "v1.0.0",
  "nodes": [{"id": "n1", "label": "Start"}],
  "edges": [],
  "allowed_dsl": ["QUERY_ENTITY", "GOVERNED_WRITE"]
}
```

**出参 JSON（G-01）**：

```json
{
  "graph_id": "graph-g01",
  "version": "v1.0.0",
  "status": "draft",
  "checksum": "sha256:..."
}
```

## 5. 架构与代码质量评估（本 Step）

分层 · 落位 · 耦合 · 可维护性：**通过** — store/service 分离；checksum 独立模块。

## 6. 结论

**结论：通过**

- 补录说明：W3 代码批量合入；本报告对照终轮 `test-1132-w3-final-regression.md` 回溯 Step1 证据。
- 通过 → 进入 **Verify·Step 1**（`verify-1140-step1.md`）
