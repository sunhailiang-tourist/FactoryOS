# Step 停机：Step 2 — CONNECTOR_NOT_CONFIGURED + license 真源（T-03）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 2 — 租户 Connector 绑定门禁 · license 读 tenant_pack_entitlements

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `platform_registry/tenant_config_store.py` | `is_pack_entitled` · `has_system_relation_for_pack` |
| `platform_registry/bootstrap.py` | `_seed_fixture_tenants`（default · tenant-unlicensed-w6） |
| `license_service/service.py` | DB 真源 + Session fallback |
| `connector_sdk/registry.py` | `assert_tenant_connector_configured` |
| `execution_service/service.py` | connector → license 顺序 · audit |
| `scripts/check_import_boundaries.py` | license_service → platform_registry |

## 3. 落位说明

- **T-03**：无 `system_relations` 行 → `CONNECTOR_NOT_CONFIGURED`（先于 license）
- **T-02**：有 relation 无 entitlement → `MODULE_NOT_LICENSED`（回归）
- **license 真源**：`tenant_pack_entitlements`（bootstrap 灌入 · 替代 W6 纯内存 dict）

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| T-03 | POST `/v1/execute` tenant 无 pack | ✅ 403 CONNECTOR_NOT_CONFIGURED |
| T-02 | 回归 tenant-unlicensed-w6 | ✅ MODULE_NOT_LICENSED |
| T-01 | 回归 shadow | ✅（同轮 pytest） |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_connector_t03_w7.py -k 'T-03' -v
uv run pytest src/tests/integration/test_license_t02_w6.py -k 'T-02' -q
```

## 6. Verify

- 口令：`【Verify回合】Step 2`

## 7. 等待

Test Step 2 验收 → Verify → `gate step --step 2 -k 'T-03'`
