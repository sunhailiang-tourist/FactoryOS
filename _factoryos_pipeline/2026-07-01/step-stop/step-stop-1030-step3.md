# Step 停机：Step 3 — Package export（P-01）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 3 — Implementation Package export · POST `/v1/packages/export`

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `os_core/package_service/` | 新建 · `export_implementation_package` |
| `api/modules/package/` | 新建 · POST `/v1/packages/export` 薄路由 |
| `graph_service/store.py` | `list_graphs_by_tenant` |
| `rule_engine/store.py` | `list_rulesets_for_graph_ids` |
| `platform_registry/pack_store.py` | `get_pack_registry_key` |
| `platform_registry/bootstrap.py` | `_seed_fixture_graph`（default frozen graph+ruleset） |
| `api/router/v1/registry.py` | 注册 package 域 |
| `os_core/registry.py` | package_service 内核登记 |
| `scripts/check_import_boundaries.py` | package_service 白名单 |
| `contracts/repo-structure.yaml` | kernel 13 · package_service |

## 3. 落位说明

- **内核**：`package_service` 聚合 Graph · RuleSet · connector_configs（REST/MCP 共用）
- **HTTP**：`modules/package` 仅路由/校验，无业务规则
- **夹具**：bootstrap 灌入 `graph-d1-generic-template` + `ruleset-w3-default`，P-01 可独立跑

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| P-01 | POST `/v1/packages/export` | ✅ 200 · graphs/rulesets/connector_configs |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_package_w7.py -k 'P-01' -v
uv run python scripts/check_import_boundaries.py
uv run python scripts/check_repo_structure.py
```

## 6. Verify

- 口令：`【Verify回合】Step 3`

## 7. 等待

Test Step 3 验收 → Verify → `gate step --step 3 -k 'P-01'`
