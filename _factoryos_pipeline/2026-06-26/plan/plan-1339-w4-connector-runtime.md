# 预开发说明：W4 — connector_sdk/runtime · L2 真写 · Revert

- **日期**：2026-06-26
- **对照契约**：`contracts/openapi/工厂操作系统-v1.1.yaml` · `contracts/acceptance/验收用例-BASE-001-平台底座.md` · `contracts/schemas/ConnectorBlueprint.schema.json`
- **架构入口**：`docs/文档/架构/FactoryOS完整架构设计.md` §16 W4 行
- **依赖 W3**：graph freeze · rule evaluate · DSL 门禁 · E-01 ✅

---

## 1. 迭代目标

**一句话**：Blueprint Runtime 加载 catalog 样例，经 `execution_service` 完成 L2 真写（snapshot）与 Revert 闭环。

**可测要点**：B-01～B-04 · C-02～C-04 · E-02 · E-04 · E-05 · W1–W3 存量回归不破坏。

**不在 W4**：D-04 · E-08 · H/K/P/T/M · 52 P0 全绿（留 W5–W8）

---

## 2. AC 对账表

| AC ID | 标题 | 本迭代 | Step | 验证方式 |
|-------|------|--------|------|----------|
| B-01 | 加载 mock blueprint | 是 | 1 | `-k 'B-01'` |
| B-02 | Runtime 执行 L2 op | 是 | 2 | `-k 'B-02'` |
| B-03 | mapping 错误 | 是 | 2 | `-k 'B-03'` |
| B-04 | revert/reconcile 声明 | 是 | 4 | `-k 'B-04'` |
| C-02 | read entity | 是 | 2 | `-k 'C-02'` |
| C-03 | write entity | 是 | 2 | `-k 'C-03'` |
| C-04 | revert read-back | 是 | 4 | `-k 'C-04'` |
| E-02 | L2 写成功 + snapshot | 是 | 3 | `-k 'E-02'` |
| E-03 | Audit 产生 | 是 | 3 | 随 E-02 回归 |
| E-04 | Revert 成功 | 是 | 4 | `-k 'E-04'` |
| E-05 | 重复 revert 409 | 是 | 4 | `-k 'E-05'` |
| E-09 | Evidence 可重建 | 是 | 3–4 | E-02 后 evidence 含 snapshot |
| G/R/D/E-01 等 | W3 存量 | 回归 | 每 Step | `pytest -m 'not pending'` |

---

## 3. 红线对账

| 红线 | 本迭代涉及 | 负向测试 |
|------|------------|----------|
| R-01 写路径唯一 | execution → connector_sdk | E-08 仍 pending；import_boundaries |
| R-02 Rule 默认 deny | 保留 W3 链 | R-01 回归 |
| R-04 append-only audit | revert 写 audit | E-03 回归 |
| Graph 未 freeze | 保留 G-03 | G-03 回归 |

---

## 4. 接口清单

| 方法 | 路径 | 用途 | Step |
|------|------|------|------|
| GET | `/v1/connectors/{packId}/health` | C-01 存量 | 回归 |
| POST | `/v1/execute` | L2 真写 E-02 | 3 |
| POST | `/v1/execute/{execId}/revert` | E-04/E-05 | 4 |
| GET | `/v1/executions/{execId}/evidence` | E-09 增强 | 3–4 |

---

## 5. 模块与文件

| 模块 | 路径 | 变更 |
|------|------|------|
| connector_sdk | `src/server/os_core/connector_sdk/runtime/` | **新增** loader · execute_op · revert_op |
| connector_sdk | `src/server/os_core/connector_sdk/registry.py` | **新增** catalog 加载 |
| catalog | `src/integration/catalog/conn-mock.yaml` | **扩展** ConnectorBlueprint + GOVERNED_WRITE op |
| execution | `src/server/os_core/execution_service/service.py` | L2 走 runtime · snapshot 字段 · revert |
| execution | `src/server/os_core/execution_service/store.py` | before/after snapshot 持久化（若 schema 需 migration） |
| API | `src/server/api/modules/*/controllers/execute.py` | **新增/扩展** revert 路由 |
| 测试 | `src/tests/integration/test_connector_b*.py` · `test_execution_e02*.py` | 新增 |

---

## 6. 分步计划

### Step 1 — Blueprint catalog + Runtime 骨架

| 项 | 内容 |
|----|------|
| AC ID | B-01 |
| 接口 | 内部 `load_blueprint(pack_id)` |
| 模块路径 | `connector_sdk/runtime/` · `registry.py` · `conn-mock.yaml` |
| Harness | `./scripts/gate step --step 1 -k 'B-01'` |
| 风险 | conn-mock 须对齐 `ConnectorBlueprint.schema.json` |

### Step 2 — Runtime read/write + mapping 负向

| 项 | 内容 |
|----|------|
| AC ID | B-02 · B-03 · C-02 · C-03 |
| 接口 | runtime `entity.get` / `entity.update` mock |
| 模块路径 | `runtime/execute.py` · mock_legacy 扩展 snapshot store |
| Harness | `./scripts/gate step --step 2 -k 'C-02'` |
| 风险 | mapping 缺字段 → `MAPPING_ERROR` |

### Step 3 — execution L2 真写 + snapshot + E-09

| 项 | 内容 |
|----|------|
| AC ID | E-02 · E-03 · E-09 |
| 接口 | `POST /v1/execute` 非 dry_run L2 |
| 模块路径 | `execution_service/service.py` 替换 `mock_legacy_write` 为 runtime |
| Harness | `./scripts/gate step --step 3 -k 'E-02'` |
| 风险 | migration 004 若 ExecutionRecord 缺 snapshot 字段 |

### Step 4 — Revert HTTP + 闭环

| 项 | 内容 |
|----|------|
| AC ID | E-04 · E-05 · C-04 · B-04 |
| 接口 | `POST /v1/execute/{execId}/revert` |
| 模块路径 | `execution_service/revert.py` · `routes/execute.py` |
| Harness | `./scripts/gate step --step 4 -k 'E-04'` |
| 风险 | simulated/dry_run 须 409；L2 op 无 revert 声明 → 422 |

---

## 7. Harness 验收盘（全局）

```bash
./scripts/gate step --step 1 -k 'B-01'
./scripts/gate step --step 2 -k 'C-02'
./scripts/gate step --step 3 -k 'E-02'
./scripts/gate step --step 4 -k 'E-04'
./scripts/gate delivery
./scripts/gate pr
```

**纪律**：每 Step 须 Dev step-stop → Test 单步验收 → Verify → `gate step` 绿 → 用户 `可以继续`（禁止 W3 式批量跳步）。

---

## 8. 存量回归（每 Step 附加）

```bash
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
```

W3 graph/rule/dsl + W2 audit/execution/evidence 须保持绿。
