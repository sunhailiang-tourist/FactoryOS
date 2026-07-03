# 测试用例与改动面：W7 Gate 0 — GIP · Shadow · Package · MCP failing tests

- **对照 plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **命名**：`test-1655-w7-gate0-gip-mcp.md`
- **目的**：**新增** · W7 Step1～7 failing tests（Gate 0 剩余 14 项 pending AC）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_shadow_w7.py` | 新增 | Step1 T-01 shadow_mode |
| `src/tests/integration/test_connector_t03_w7.py` | 新增 | Step2 T-03 CONNECTOR_NOT_CONFIGURED |
| `src/tests/integration/test_package_w7.py` | 新增 | Step3–4 P-01～P-03 Package |
| `src/tests/integration/test_mcp_w7.py` | 新增 | Step5 M-01/M-02 MCP |
| `src/tests/integration/test_dsl_e08_w7.py` | 新增 | Step6 D-04/E-08 |
| `src/tests/integration/test_negative_w7.py` | 新增 | Step7 N-01～N-04 |
| `src/tests/ac/test_base001_registry.py` | 修改 | W7 AC 移出 pending |

## 2. AC 用例

| ID | 标题 | 类型 | Step | 期望 |
|----|------|------|------|------|
| T-01 | shadow_mode | integration | 1 | L2 simulated · Legacy 不变 |
| T-03 | Connector 未配置 | integration | 2 | 403 CONNECTOR_NOT_CONFIGURED |
| P-01 | Package export | integration | 3 | JSON 含 graphs/rulesets/connector_configs |
| P-02 | Package import | integration | 4 | tenant B resolve Pack |
| P-03 | Override 差量 | integration | 4 | overrides base_url 生效 |
| M-01 | MCP tools/list | integration | 5 | 仅已授权 CMV |
| M-02 | MCP tools/call | integration | 5 | DslPlan · Legacy 写 0 |
| D-04 | L2 无 compensator | integration | 6 | 422 拒绝注册 |
| E-08 | Agent 禁直写 | workflow | 6 | orchestrator 无 connector 写 import |
| N-01～N-04 | 负向安全 | integration | 7 | 见 BASE-001 §十三 |
| 存量 W1～W6 | 回归 | 每 Step | `pytest -m 'not pending'` |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'T-01'
./scripts/gate step --step 2 -k 'T-03'
./scripts/gate step --step 3 -k 'P-01'
./scripts/gate step --step 4 -k 'P-02'
./scripts/gate step --step 5 -k 'M-01'
./scripts/gate step --step 6 -k 'D-04'
./scripts/gate step --step 7 -k 'N-01'
./scripts/gate delivery
```

## 4. 标准测试用例

| ID | 标题 | 前置 | 步骤摘要 | 期望 |
|----|------|------|----------|------|
| T-01 | shadow | frozen graph | PUT settings shadow=true → L2 execute dry_run=false | simulated · Legacy 0 写 |
| T-03 | no connector | frozen graph | tenant 无 pack → execute | 403 |
| P-01 | export | default tenant | POST packages/export | ImplementationPackage |
| P-02 | import | P-01 包 | POST packages/import tenant B | health ok |
| P-03 | override | tenant B | PUT settings connector_overrides | connect/test 新 URL |
| M-01 | list | default | POST /mcp/v1/default tools/list | tools≥1 |
| M-02 | call | frozen graph | tools/call GOVERNED_WRITE | DslPlan · Legacy 0 |
| D-04 | cmv | — | POST registry/cmv/verbs L2 无 compensator | 422 |
| E-08 | agent | — | 静态扫描 agent_orchestrator | 无 runtime 写 import |
| N-01 | bypass | — | POST /v1/internal/execute | 404/403 |
| N-02 | checksum | draft graph | 篡改 checksum → freeze | 409/422 |
| N-03 | tenant | exec tenant A | tenant B GET execution | 403 |
| N-04 | sqli | frozen graph | entity_id 注入模式 | 400/422 |

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-0900-w7-gate0-gip-mcp.md` ✓ |
| Step 范围 | 7 Step · Gate 0 14 pending AC ✓ |
| MCP | 对外预留 · `/mcp/v1/{tenantId}` 不变 ✓ |
| 不在 W7 | 真实 ERP · OAuth 2.1 生产 · 公网 MCP ✓ |

## Gate A–G 摘要

| Gate | 结论 |
|------|------|
| A 复盘 | license/reconciliation ✅ · 本轮 Shadow/Package/MCP/负向 |
| B 目的 | **新增** — W7 failing tests 驱动 Gate 0 红→绿 |
| C 协作 | plan Step1–7 模块路径与 AC 一一对齐 |
| D 质量 | 每 Step 验收交付架构评估 |
| E 接口 | 见下方分区 |
| F 字段 | TenantSettings 增 shadow_mode/overrides；无破坏性删字段 |
| G 命名 | `test-1655` = 落盘当下 HHmm |

## 📦 本次新增接口（测）

```json
GET /v1/tenants/{tenantId}/settings
PUT /v1/tenants/{tenantId}/settings
{
  "shadow_mode": true,
  "write_approved": false,
  "connector_overrides": {
    "conn-mock": { "base_url": "https://override-mes.example.local/v1" }
  }
}
```

```json
POST /v1/packages/export
{ "tenant_id": "default", "delivery": "D1" }
```

```json
POST /v1/packages/import
{
  "package_id": "<uuid>",
  "tenant_id": "tenant-b-w7",
  "version": "v1.0.0",
  "exported_at": "2026-07-01T00:00:00Z",
  "graphs": [],
  "rulesets": []
}
```

```json
POST /mcp/v1/default
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

```json
POST /mcp/v1/default
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "GOVERNED_WRITE",
    "arguments": {
      "tenant_id": "default",
      "graph_id": "<frozen>",
      "graph_version": "v1.0.0",
      "intent": "report work order wo-m02 completed qty 1"
    }
  }
}
```

## 🔁 本次需求涉及到的接口（字段调整）

`POST /v1/execute`：T-03 未配置 Connector 须返回 `CONNECTOR_NOT_CONFIGURED`（403）。

## 结论

Test-plan 就绪 → `gate test` → Dev **`可以开始`** Step 1（T-01）
