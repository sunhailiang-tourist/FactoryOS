# Step 停机：Step 5 — MCP Gateway（M-01 · M-02）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 5 — POST `/mcp/v1/{tenantId}` · tools/list · tools/call

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `mcp_gateway/service.py` | `handle_mcp_json_rpc` · list_tools · call_tool |
| `mcp_gateway/__init__.py` | 公开 API |
| `api/modules/mcp/` | POST `/mcp/v1/{tenant_id}` 薄路由 |
| `agent_orchestrator/service.py` | `source` · `verb` 参数（MCP 复用） |
| `platform_registry/tenant_config_store.py` | `list_licensed_pack_ids` |
| `api/router/v1/registry.py` | 注册 mcp 域 |
| `scripts/check_import_boundaries.py` | mcp_gateway 白名单扩展 |

## 3. 落位说明

- **M-01**：已授权 Pack Blueprint ops → tools/list（仅 licensed CMV）
- **M-02**：Graph/Rule 门禁 → `create_plan(source=mcp)` · 不写 Legacy

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| M-01 | POST `/mcp/v1/default` tools/list | ✅ GOVERNED_WRITE 等 |
| M-02 | tools/call | ✅ DslPlan · Legacy 写 0 |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_mcp_w7.py -v
uv run python scripts/check_import_boundaries.py
```

## 6. Verify

- 口令：`【Verify回合】Step 5`

## 7. 等待

Test Step 5 验收 → Verify → `gate step --step 5 -k 'M-01'`
