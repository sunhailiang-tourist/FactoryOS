# Step 停机：Step 1 — tenant shadow_mode（T-01）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 1 — 租户级 shadow_mode · GET/PUT settings · L2 execute → simulated

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/tenant_service/` | 新建内核 · shadow 真源（REST/MCP 共用） |
| `src/server/os_core/platform_registry/tenant_config_store.py` | `upsert_tenant_settings` |
| `src/server/os_core/execution_service/service.py` | `effective_shadow = dry_run ∨ tenant_shadow` |
| `src/server/os_core/registry.py` | 登记 `tenant_service` |
| `src/server/api/modules/tenant/` | 薄 HTTP · controllers/tenant.py |
| `src/server/api/router/v1/registry.py` | 登记 tenant 域 |
| `contracts/repo-structure.yaml` | kernel module_count 12 · tenant_service |
| `src/server/os_core/mcp_gateway/README.md` | 下游 cross-ref tenant_service |

## 3. 落位说明（MCP 扩展）

- **真源**：`os_core/tenant_service` — `get/update/resolve_shadow_mode`；Step 5 MCP 直接 import，不经 API 层
- **HTTP 面**：`modules/tenant/` 仅路由/依赖注入
- **execution**：读 `resolve_shadow_mode()`，与 dry_run 合并；禁止在 API 层判断 shadow

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| T-01 | GET/PUT `/v1/tenants/{id}/settings` + POST `/v1/execute` | ✅ pytest 绿 |

## 5. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层 | Pass — API 薄 · 内核 tenant_service |
| 2 | OpenAPI | Pass — TenantSettings 路径对齐 v1.1 |
| 3 | 红线 | Pass — shadow 时 L2 不写 Legacy |
| 4 | MCP 预留 | Pass — 内核共用 · mcp_gateway README 已链 |
| 5–10 | 其余 | Pass |

## 6. Harness

```bash
uv run pytest src/tests/integration/test_shadow_w7.py -k 'T-01' -v
```

## 7. Verify

- 口令：`【Verify回合】Step 1`

## 8. 等待

Test Step 1 验收 → Verify → `gate step --step 1 -k 'T-01'` → 用户 `可以继续`
