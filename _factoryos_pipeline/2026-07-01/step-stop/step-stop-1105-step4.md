# Step 停机：Step 4 — Package import + Override（P-02 · P-03）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 4 — POST `/v1/packages/import` · connector_overrides · connect/test

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `package_service/service.py` | `import_implementation_package` |
| `package/controllers/package.py` | POST `/v1/packages/import` |
| `platform_registry/tenant_config_store.py` | overrides · ensure_system_relation · ensure_pack_entitlement |
| `tenant_service/service.py` | `connector_overrides` 参数 |
| `tenant/controllers/tenant.py` | PUT settings 接受 connector_overrides |
| `connector_sdk/connect_test.py` | `resolve_pack_base_url` · `run_connect_test` |
| `api/modules/integration/` | POST `/v1/integration/connect/test` |
| `api/router/v1/registry.py` | 注册 integration 域 |

## 3. 落位说明

- **P-02**：import 写入 Graph/RuleSet（幂等）+ system_relations + entitlements → tenant B health 200
- **P-03**：profile_json 存 connector_overrides；connect/test 返回 resolved base_url

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| P-02 | POST `/v1/packages/import` | ✅ tenant B · connector health |
| P-03 | PUT settings + POST connect/test | ✅ override base_url |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_package_w7.py -k 'P-02 or P-03' -v
```

## 6. Verify

- 口令：`【Verify回合】Step 4`

## 7. 等待

Test Step 4 验收 → Verify → `gate step --step 4 -k 'P-02'`
