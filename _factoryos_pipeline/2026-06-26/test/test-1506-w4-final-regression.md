# 终轮全量回归 · W4 Test 兜底验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`（含 W1–W3 存量）
- **命名**：`test-1506-w4-final-regression.md`（HHmm=1506）
- **口令**：`【Test·终轮回归】`（2026-06-26 · W4 四步链闭合后）

## 1. 本轮 git diff 全量改动面

| 路径 | 变更 | plan Step | 落位合理 | 备注 |
|------|------|-----------|----------|------|
| `connector_sdk/registry.py` | 新增 | 1 | ✅ | B-01/B-04 |
| `connector_sdk/runtime/` | execute · entity · mapping | 2 | ✅ | B-02/B-03 · C-02～C-04 |
| `integration/catalog/conn-mock.yaml` | ConnectorBlueprint | 1 | ✅ | |
| `connector_sdk/mock_legacy.py` | entity store · restore | 2/4 | ✅ | |
| `execution_service/service.py` | L2 runtime · revert | 3/4 | ✅ | E-02/E-04 |
| `execution_service/store.py` | snapshot 持久化 · status 更新 | 3/4 | ✅ | |
| `apps/api/routes/execute.py` | POST revert | 4 | ✅ | E-04/E-05 |
| `apps/api/routes/executions.py` | GET execution | 4 | ✅ | |
| `shared_contracts/errors.py` | BLUEPRINT_INVALID 等 | 1 | ✅ | |
| `src/tests/integration/test_*_w4.py` · `test_execution_e02_e04_e05.py` | 测试 | Test | ✅ | |

**无超 plan 文件**；未实现 D-04 · E-08 · H/K/P/T/M（plan 预期）。

## 2. 新增功能正确性（本轮 AC 全量）

| AC ID | Step | 业务验收 | pytest 证据 | 结果 |
|-------|------|----------|-------------|------|
| B-01 | 1 | 加载 conn-mock blueprint | `test_B01_*` | **PASS** |
| B-02 | 2 | Runtime L2 · legacy_refs | `test_B02_*` | **PASS** |
| B-03 | 2 | MAPPING_ERROR | `test_B03_*` | **PASS** |
| B-04 | 4 | L2 无 revert → BLUEPRINT_INVALID | `test_B04_*` | **PASS** |
| C-02 | 2 | entity.get snapshot | `test_C02_*` | **PASS** |
| C-03 | 2 | entity.update | `test_C03_*` | **PASS** |
| C-04 | 4 | read-back | `test_C04_*` | **PASS** |
| E-02 | 3 | L2 真写 + snapshots | `test_E02_*` | **PASS** |
| E-03 | 3 | audit 回归 | `test_E03_*` | **PASS** |
| E-04 | 4 | revert 成功 | `test_E04_*` | **PASS** |
| E-05 | 4 | 重复 revert 409 | `test_E05_*` | **PASS** |
| E-09 | 3–4 | evidence 含 snapshot | `test_E09_*` | **PASS** |
| G/R/D/E-01/06/07 等 | 存量 | W3/W2 回归 | 各用例 | **PASS** |

```bash
uv run pytest src/tests/integration/test_connector_blueprint_w4.py \
  src/tests/integration/test_connector_runtime_w4.py \
  src/tests/integration/test_execution_e02_e04_e05.py -v
# 11 passed（W4 专项）

uv run python scripts/gate_cli.py step --step 1 -k 'B-01'   # OK
uv run python scripts/gate_cli.py step --step 2 -k 'C-02'   # OK
uv run python scripts/gate_cli.py step --step 3 -k 'E-02'   # OK
uv run python scripts/gate_cli.py step --step 4 -k 'E-04'   # OK
```

## 3. 存量功能回归

| 域 | 回归范围 | 命令 | 结果 |
|----|----------|------|------|
| workflow | 红线/门禁/健康检查 | `pytest src/tests/workflow/` | **PASS** |
| contract | OpenAPI/Schema/CMV | `pytest src/tests/contract/` | **PASS** |
| integration | W1–W4 全量非 pending | `pytest src/tests/integration/ -m 'not pending'` | **PASS** |

```bash
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 60 passed · 1 skipped
```

## 4. 代码落位与优雅性（终轮）

| 维度 | 结论 | 说明 |
|------|------|------|
| 模块边界 | **通过** | registry/runtime 在 connector_sdk；revert 在 execution_service |
| 写路径 | **通过** | L2 真写/revert 经 execution → runtime → mock_legacy |
| 重复逻辑 | **通过** | CMV level · mapping 校验单点 |
| 注释可读性 | **通过** | 新模块文件头 + 函数四要素 |
| 与 plan 一致 | **通过** | 四步分步交付；无批量跳步 |
| 可改进 | **非阻断** | `DEFAULT_PACK_ID` 硬编码；revert 未走 blueprint revert op |

## 5. 接口分区（终轮交付）

### 📦 本次新增接口

| 方法 | 路径 | AC |
|------|------|-----|
| POST | `/v1/execute/{execId}/revert` | E-04 · E-05 |

### 🔁 本次需求涉及到的接口（字段调整）

**POST `/v1/execute`**（非 dry_run L2）响应增：

```json
{
  "status": "success",
  "dry_run": false,
  "before_snapshot": {
    "entity_type": "work_order",
    "entity_id": "wo-1",
    "fields": { "status": "open", "completed_qty": 0 }
  },
  "after_snapshot": {
    "entity_type": "work_order",
    "entity_id": "wo-1",
    "fields": { "status": "in_progress", "completed_qty": 1 }
  },
  "legacy_refs": [
    { "system": "mock", "ref_type": "work_order", "ref_id": "work_order/wo-1" }
  ]
}
```

**POST `/v1/execute/{execId}/revert`** 响应：

```json
{
  "status": "reverted",
  "verb": "GOVERNED_WRITE",
  "before_snapshot": { "entity_type": "work_order", "entity_id": "wo-1", "fields": { "status": "open" } },
  "after_snapshot": { "entity_type": "work_order", "entity_id": "wo-1", "fields": { "status": "in_progress" } },
  "finished_at": "2026-06-26T06:57:15.029420Z"
}
```

**GET `/v1/executions/{execId}/evidence`** — `execution` 对象含 `before_snapshot` / `after_snapshot`（E-09 增强）。

## 6. 文件 ↔ 接口对账表

| 文件 | 接口/AC | 说明 |
|------|---------|------|
| `connector_sdk/registry.py` | 内部 `load_blueprint` | B-01 · B-04 |
| `connector_sdk/runtime/execute.py` | runtime op | B-02 · B-03 |
| `connector_sdk/runtime/entity.py` | entity get/update | C-02～C-04 |
| `execution_service/service.py` | execute · revert | E-02 · E-04 · E-05 |
| `apps/api/routes/execute.py` | POST execute · POST revert | E-02 · E-04 |
| `apps/api/routes/executions.py` | GET execution · evidence | E-09 |

## 7. 结论

**结论：通过**

- W4 plan AC **B-01～B-04 · C-02～C-04 · E-02/03/04/05/09** 全绿
- 存量 **60/60** 非 pending 绿；四步 `gate step` 全绿
- 52 P0 其余 **16 pending**（E-08 · H/K/P/T/M 等，留 W5–W8）
- 允许 `./scripts/gate delivery` 绿后提示 **可以提交**
