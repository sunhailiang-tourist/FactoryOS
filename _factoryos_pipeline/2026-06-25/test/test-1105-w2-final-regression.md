# 终轮全量回归 · W2 Test 兜底验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`（Step 1～4 全量）
- **命名**：`test-1105-w2-final-regression.md`（HHmm=1105）
- **口令**：`【Test·终轮回归】`（2026-06-26 · W2 交付前）

## 1. 本轮 git 改动面（W1+W2 可测子集）

| 路径 | 变更 | plan | 落位 | 备注 |
|------|------|------|------|------|
| `alembic/versions/002_audit_execution.py` | 新增 | W2 S1 | ✅ | audit + execution 表 |
| `src/os_core/audit_service/` | 新增 | W2 S1–2 | ✅ | append-only |
| `src/os_core/execution_service/` | 新增 | W2 S3–4 | ✅ | execute · evidence |
| `src/os_core/connector_sdk/mock_legacy.py` | 新增 | W2 S3 | ✅ | E-06/E-07 |
| `src/apps/api/deps.py` | 新增 | W2 S2 | ✅ | DB 会话 |
| `src/apps/api/routes/audit.py` | 新增 | W2 S2 | ✅ | E-03 |
| `src/apps/api/routes/execute.py` | 新增 | W2 S2/4 | ✅ | POST execute |
| `src/apps/api/routes/executions.py` | 新增 | W2 S4 | ✅ | E-09 evidence |
| `src/tests/integration/test_audit_e03.py` 等 | 新增 | Test | ✅ | W2 AC |

## 2. 新增功能正确性（W2 AC 全量）

| AC ID | Step | 业务验收 | pytest 证据 | 结果 |
|-------|------|----------|-------------|------|
| workflow | 1–4 | import_boundaries + `/health` | workflow 套件 | **PASS** |
| E-03 | 2 | execute → audit 可查 | `test_E03_*` | **PASS** |
| E-06 | 3 | dry_run 不写 Legacy | `test_E06_*` | **PASS** |
| E-07 | 3 | idempotency | `test_E07_*` | **PASS** |
| E-09 | 4 | evidence 可重建 | `test_E09_*` | **PASS** |
| S-01～S-04 | W1 | 规模预埋 | `test_S0*` | **PASS** |
| C-01 | W1 | connector health | `test_C01_*` | **PASS** |
| contract | W1/W2 | 7 Schema 对齐 | shared_contracts | **PASS** |
| 52 P0 其余 | — | W3+ | pending | **47 pending**（plan 预期） |

## 3. 存量功能回归

| 域 | 命令 | 结果 |
|----|------|------|
| 全量可测 | `pytest contract workflow integration -m 'not pending'` | **25 passed** |
| harness full | `gate_cli.py pr` harness | **OK** |
| static | `check_static_quality.py` | **OK** |
| deptry | `gate_cli.py pr` deptry | **OK** |
| gate pr | `gate_cli.py pr` | **Gate pr OK** |
| gate delivery | `gate_cli.py delivery` | pytest OK · 需 `phase: DELIVERY` |

```bash
uv run python scripts/gate_cli.py delivery
uv run python scripts/gate_cli.py pr
```

## 4. 代码落位与优雅性（终轮）

| 维度 | 结论 | 说明 |
|------|------|------|
| 模块边界 | **通过** | apps/api 薄路由 · 业务 os_core |
| 写路径 | **通过** | 唯一 execute 入口 · dry_run simulated |
| audit | **通过** | append-only |
| 注释 | **通过** | 中文四要素齐全 |
| 与 plan 一致 | **通过** | 无 Graph/Rule 运行时 · 无 Legacy 真写 |
| 重复逻辑 | **通过** | evidence 复用 list_audit_events |

## 5. 接口分区（终轮交付）

### 📦 本次新增接口

#### `GET /v1/audit/events`（E-03）

入参 query：

```json
{
  "tenant_id": "default",
  "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b"
}
```

出参（数组首条）：

```json
{
  "event_id": "3632b916-4916-442a-baab-64a9b8678194",
  "tenant_id": "default",
  "event_type": "execute.started",
  "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b",
  "actor": {
    "user_id": "test-operator",
    "role": "operator",
    "channel": "api"
  },
  "occurred_at": "2026-06-26T03:02:29.000399Z"
}
```

#### `POST /v1/execute`（E-03/E-06/E-07）

入参：

```json
{
  "tenant_id": "default",
  "graph_id": "graph-d1-generic-template",
  "graph_version": "v1.0.0",
  "verb": "GOVERNED_WRITE",
  "params": {"entity": "work_order", "action": "mock_update"},
  "dry_run": true,
  "idempotency_key": "test-e09-evidence-001",
  "actor": {"user_id": "test-operator", "role": "operator", "channel": "api"}
}
```

出参：

```json
{
  "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b",
  "tenant_id": "default",
  "verb": "GOVERNED_WRITE",
  "status": "simulated",
  "dry_run": true,
  "idempotency_key": "test-e09-evidence-001",
  "shadow_mode": true
}
```

#### `GET /v1/executions/{execId}/evidence`（E-09）

入参：路径 `exec_id`

出参：

```json
{
  "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b",
  "tenant_id": "default",
  "assembled_at": "2026-06-26T03:02:29.000399Z",
  "execution": {
    "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b",
    "status": "simulated",
    "dry_run": true
  },
  "audit_events": [
    {"event_type": "execute.started"},
    {"event_type": "execute.simulated"}
  ],
  "rule_snapshot": null
}
```

### 🔁 本次需求涉及到的接口（字段调整）

**无字段调整**。

W2 为新增 HTTP 路由与内核 API；W1 存量 `/health` · `/v1/connectors/{packId}/health` 响应未改。

## 6. 文件 ↔ 接口对账表

| 文件 | 接口/AC | 说明 |
|------|---------|------|
| `audit_service/store.py` | E-03 内核 | append · list |
| `apps/api/routes/audit.py` | GET `/v1/audit/events` | E-03 HTTP |
| `execution_service/service.py` | E-06/E-07/E-09 | execute · assemble_evidence |
| `apps/api/routes/execute.py` | POST `/v1/execute` | E-03 端到端 |
| `apps/api/routes/executions.py` | GET `.../evidence` | E-09 |
| `connector_sdk/mock_legacy.py` | E-06/E-07 | Legacy 写计数 |
| `alembic/versions/002_*.py` | workflow | migration |
| `tests/integration/test_audit_e03.py` | E-03 | |
| `tests/integration/test_execution_e06_e07.py` | E-06/E-07 | |
| `tests/integration/test_execution_e09.py` | E-09 | |

## 7. 结论

**结论：通过**

- W2 AC 子集 **E-03 · E-06 · E-07 · E-09** 全绿
- 全量可测 **25/25 passed** · **gate pr OK**
- 47 P0 pending（plan 预期，W3+ Gate 0）
- 允许 `workflow_state → DELIVERY` 后 `./scripts/gate delivery` 绿 → **可以 commit**
