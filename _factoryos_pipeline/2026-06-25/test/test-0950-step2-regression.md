# Step 2 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md` · Step 2
- **命名**：`test-0950-step2-regression.md`（HHmm=0950）
- **口令**：`【Test·Step 2 验收】`
- **step-stop**：`step-stop-0941-step2.md`

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan Step | 落位 | 结论 |
|------|------|-----------|------|------|
| `src/server/api/modules/*/controllers/audit.py` | 新增 | 2 | ✅ 薄路由 | PASS |
| `src/server/api/config/dependencies/db.py` | 新增 | 2 | ✅ DB 会话 | PASS |
| `src/server/api/modules/*/controllers/execute.py` | 新增 | **4**（提前） | ⚠️ 超 Step | 见 §5 |
| `src/server/os_core/execution_service/` | 新增 | **3**（提前） | ⚠️ 超 Step | 见 §5 |
| `src/server/os_core/connector_sdk/mock_legacy.py` | 新增 | 3 | ⚠️ 提前 | 见 §5 |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| E-03 | POST execute → GET audit | `test_E03_audit_events_after_execute[E-03]` | **PASS** |
| E-03 | 存量 Step1 内核 | migration + append kernel | **PASS** (2/2) |
| E-06 | dry_run 不写 Legacy | `test_E06_*` | **PASS**（Step3 范围 · 已提前绿） |
| E-07 | idempotency | `test_E07_*` | **PASS**（Step3 范围 · 已提前绿） |
| E-09 | evidence HTTP | `test_E09_*` | **FAIL**（Step4 · 预期红） |
| W1 存量 | contract/workflow/S-*/C-01 | `-m 'not pending'` | **PASS** (19/19) |

```bash
uv run pytest src/tests/integration/test_audit_e03.py -v
# → 3 passed

uv run pytest src/tests/integration/test_audit_e03.py -k 'E-03' -v
# → 1 passed

uv run python scripts/check_static_quality.py
# → OK

uv run python scripts/gate_cli.py step --step 2 -k 'E-03'
# → harness/static OK · test regression 本文件落盘前 MISSING
# → Verify 须 W2 专用 verify-*-step2.md（勿用 W1 verify-1532）
```

## 3. 代码落位合理性

| 维度 | 结论 |
|------|------|
| 分层 | **通过** — audit/execute 路由委托 os_core |
| 写路径 | **通过** — execute 经 execution_service；dry_run → simulated |
| audit | **通过** — GET 只读 · append-only |
| 注释 | **通过** — audit.py · execute.py 四要素齐全 |
| plan 边界 | **需改进** — Step2 合入 Step3/4 部分实现（见下） |

## 4. 已改动代码测试报告（本 Step · E-03）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-03 | POST `/v1/execute` | dry_run execute | PASS |
| E-03 | GET `/v1/audit/events` | 按 exec_id 查询 | PASS |

**入参 POST `/v1/execute`**：

```json
{
  "tenant_id": "default",
  "graph_id": "graph-d1-generic-template",
  "graph_version": "v1.0.0",
  "verb": "GOVERNED_WRITE",
  "params": {"entity": "work_order", "action": "mock_update"},
  "dry_run": true,
  "idempotency_key": "test-idem-w2-001",
  "actor": {"user_id": "test-operator", "role": "operator", "channel": "api"}
}
```

**出参 execute（摘要）**：

```json
{
  "exec_id": "88c622f4-465d-4175-94ee-35544c333b31",
  "tenant_id": "default",
  "status": "simulated",
  "dry_run": true,
  "idempotency_key": "test-idem-w2-001"
}
```

**出参 GET `/v1/audit/events?tenant_id=default&exec_id=...`（首条）**：

```json
{
  "event_id": "3632b916-4916-442a-baab-64a9b8678194",
  "tenant_id": "default",
  "event_type": "execute.started",
  "exec_id": "88c622f4-465d-4175-94ee-35544c333b31",
  "graph_id": "graph-d1-generic-template",
  "graph_version": "v1.0.0"
}
```

结构依据：`contracts/schemas/AuditEvent.schema.json` · OpenAPI `ExecutionRecord`

## 5. 架构与代码质量评估

**结论子项**：

| 维度 | 评估 |
|------|------|
| E-03 功能 | **通过** |
| 超 scope | **需改进** — Dev 在 Step2 一并交付 `execution_service` + `POST /v1/execute`，导致 E-06/E-07 提前变绿；E-09 仍红（缺 evidence 路由） |
| Verify | **需改进** — 尚无 W2 `verify-*-step2.md`；机械 gate 可能误匹配 W1 `verify-1532-step2.md` |
| 存量回归 | **通过** — W1 19 项仍绿 |

## 6. 结论

**结论：需改进**

**E-03 功能验收通过**（3/3 audit 套件绿 · W1 存量绿 · static OK）。

**机械关单欠账**（须补齐后再 `gate step --step 2`）：

1. **【Verify回合】Step 2**（新对话 · W2 plan）→ `verify-*-step2.md`
2. 重跑 `./scripts/gate step --step 2 -k 'E-03'` → 须 **Gate step OK**

**Step3 建议**：E-06/E-07 已绿，Dev Step3 可改为 **复验 + step-stop 对账**；重点留 **Step4 E-09 evidence 路由**。

- 你 **`风险接受并继续`** → 可暂跳过 Verify 欠账（不推荐）
- 或完成 W2 Verify Step2 → 结论升 **通过** → `可以继续 W2 Step3/4`
