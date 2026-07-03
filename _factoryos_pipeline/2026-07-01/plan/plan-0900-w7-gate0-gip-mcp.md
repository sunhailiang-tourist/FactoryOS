# 预开发说明：W7 — Gate 0 冲刺（GIP · Shadow · Package · MCP 内部 GA）

- **日期**：2026-07-01
- **分支**：`dev_sunhailiang_core_260624`（W6 已 commit；可续开或 `dev_*_w7_*`）
- **对照契约**：`contracts/acceptance/验收用例-BASE-001-平台底座.md` · `contracts/openapi/工厂操作系统-v1.1.yaml`
- **规格**：Shadow-Mode与对账规格 · ADR-004 GIP · 感知与多模态入口 · ADR-006 MCP
- **路线图**：`docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md` W7～W8 → **Gate 0 / core-v1.0.0**
- **依赖 W6**：license stub · reconciliation stub · harness/agent ✅

---

## Step 0 摘要

| 维度 | 结论 |
|------|------|
| **目标** | AC-BASE-001 **剩余 P0 全绿** → Gate 0 |
| **不在 W7** | 真实 ERP/钉钉 Connector · 生产 MCP OAuth（Y2 实现，**W7 保留扩展点**） |
| **MCP 策略** | W7 交付 **M-01/M-02 内部 stub**；路由/契约按 OpenAPI **`/mcp/v1/{tenantId}` 不变**；鉴权层 **可插拔**（S0 内部 key/no-op，Y2 OAuth 2.1） |
| **pending AC** | D-04 · E-08 · P-01～P-03 · T-01 · T-03 · M-01 · M-02 · N-01～N-04（14 项） |
| **DB** | 复用 001–004；Package 可先文件+内存，tenant settings 可读 `integration/tenants` |

---

## 1. 迭代目标

**一句话**：补齐 Gate 0 剩余 P0（Shadow · Package · MCP stub · DSL/安全负向），**MCP 对外能力在架构上预留、W7 不关闭 Y2 路径**。

**Gate 0 判定**（AC-BASE-001 §十四）：上述 pending **全部 PASS** + 存量 W1～W6 回归绿 → `./scripts/gate delivery` → tag **`core-v1.0.0`**（人工）。

---

## 2. MCP 策略（用户确认：保留对外开放能力）

### 2.1 W7 做什么

| 项 | W7 交付 | 验收 |
|----|---------|------|
| `POST /mcp/v1/{tenantId}` | JSON-RPC 2.0 薄路由 | OpenAPI 对账 |
| `tools/list` | 已授权 CMV 子集（license + tenant） | **M-01** |
| `tools/call` | → `agent_orchestrator` → **DslPlan** | **M-02** Legacy 写计数 0 |
| `_meta.traceparent` | 解析钩子 stub（可选 Step） | M-03 P1，W7 末或 W8 |

### 2.2 W7 不做什么（Y2 留扩展，不删路由）

| 项 | W7 | Y2 对外 |
|----|-----|---------|
| OAuth 2.1 / 第三方 IdP | **接口占位** `McpAuthContext` · config 开关 | 实现 token 校验 |
| 工具级 ACL / Partner Registry | license + CMV 已有 | 目录化 |
| 公网暴露 | 仅 dev/staging 内部调用 | 正式对外开放 |

### 2.3 实现约束（防锁死）

- **唯一 HTTP 面**：`modules/mcp/` → 复用 OpenAPI 路径，**禁止** 另起 `/internal/mcp`
- **内核**：`os_core/mcp_gateway/` 只做 JSON-RPC 分发 + 调 orchestrator；**禁止** connector.write
- **鉴权**：API 层 `Depends(verify_mcp_access)` — W7 实现 `allow_internal`；Y2 同函数扩展 OAuth
- **与 REST 等价**：`tools/call` 语义 = `POST /v1/agent/plan` + 结构化 params，均走 Harness 后才能 execute

---

## 3. AC 对账表

| AC ID | 标题 | Step | Harness |
|-------|------|------|---------|
| T-01 | shadow_mode 租户级 | 1 | `-k 'T-01'` |
| T-03 | Connector 未配置 | 2 | `-k 'T-03'` |
| P-01 | Package export | 3 | `-k 'P-01'` |
| P-02 | Package import | 4 | `-k 'P-02'` |
| P-03 | Override 差量 | 4 | `-k 'P-03'` |
| M-01 | MCP tools/list | 5 | `-k 'M-01'` |
| M-02 | MCP tools/call → Plan | 5 | `-k 'M-02'` |
| D-04 | L2 无 compensator | 6 | `-k 'D-04'` |
| E-08 | Agent 禁直写 | 6 | `-k 'E-08'` |
| N-01～N-04 | 负向安全 | 7 | `-k 'N-01'`… |
| 存量 W1～W6 | 回归 | 每 Step | `-m 'not pending'` |

---

## 4. 分步计划

### Step 1 — tenant shadow_mode（T-01）

- `GET/PUT /v1/tenants/{id}/settings`（OpenAPI 已有）
- execution：tenant.shadow_mode=true → L2 **simulated**，不写 Legacy
- 读 `integration/tenants` 或 DB stub
- Harness：`gate step --step 1 -k 'T-01'`

### Step 2 — Connector 未配置 + license 真源升级（T-03）

- `CONNECTOR_NOT_CONFIGURED` 403 + audit
- `license_service` 读 tenant `licensed_packs`（替代 W6 纯内存 dict）
- Harness：`gate step --step 2 -k 'T-03'`

### Step 3 — Package export（P-01）

- `POST /v1/packages/export` 或 plan 定稿路径
- JSON：graphs · rulesets · connector_configs
- Harness：`gate step --step 3 -k 'P-01'`

### Step 4 — Package import + Override（P-02 · P-03）

- import 到 tenant B · resolve Pack
- overrides.yaml 改 base_url → runtime 生效
- Harness：`gate step --step 4 -k 'P-02'` / `-k 'P-03'`

### Step 5 — MCP Gateway 内部 GA + 对外预留（M-01 · M-02）

- `modules/mcp/` + `mcp_gateway/service.py`
- `verify_mcp_access` 可插拔；W7 internal pass
- Harness：`gate step --step 5 -k 'M-01'` · `-k 'M-02'`

### Step 6 — DSL D-04 + Agent E-08

- CMV 注册 L2 无 compensator → 422
- import boundary / 专项测：orchestrator 不得 import connector.write
- Harness：`gate step --step 6 -k 'D-04'` · `-k 'E-08'`

### Step 7 — 负向安全 N-* + Gate 0 终轮

- N-01～N-04 integration 负向
- 终轮 Test · `gate delivery` · pending AC 清零
- Harness：`gate step --step 7 -k 'N-01'`（或 bundle gate 0 script）

---

## 5. 模块与文件（预估）

| 模块 | 路径 |
|------|------|
| tenant settings | `modules/tenant/` 或扩展现有 |
| license 真源 | `license_service` + `integration/tenants` |
| package | `modules/package/` · `os_core` 可选 package_service |
| mcp_gateway | `os_core/mcp_gateway/` · `modules/mcp/` |
| 测试 | `test_shadow_w7.py` · `test_package_w7.py` · `test_mcp_w7.py` · `test_negative_w7.py` |

---

## 6. Harness 验收盘

```bash
./scripts/gate step --step 7 -k 'N-01'
./scripts/gate delivery
./scripts/gate pr
# pending AC = 0 → 人工 tag core-v1.0.0
```

---

## 7. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1.0 | 2026-07-01 | 初版 W7 · MCP 保留 Y2 对外扩展 |
