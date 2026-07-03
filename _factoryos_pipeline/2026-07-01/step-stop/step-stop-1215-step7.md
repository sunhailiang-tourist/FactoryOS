# Step 停机：Step 7 — 负向安全 N-01～N-04 · Gate 0

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 7 — 负向安全 · Gate 0 终轮

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `shared_contracts/param_safety.py` | `assert_params_safe` · SQL 注入模式拒绝（N-04） |
| `execution_service/service.py` | execute 前 param 校验 · `get_execution_for_tenant`（N-03） |
| `api/modules/execution/controllers/executions.py` | GET execution/evidence tenant 隔离 |

## 3. 落位说明

- **N-03**：`caller_tenant_id` ≠ `record.tenant_id` → `TENANT_FORBIDDEN` 403
- **N-04**：params 含 `';` / `--` / `DROP TABLE` 等 → `MAPPING_ERROR` 422
- **N-01/N-02**：无代码改动（已绿）

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| N-01 | POST `/v1/internal/execute` | ✅ 404 |
| N-02 | checksum 篡改 freeze | ✅ 409/422 |
| N-03 | GET `/v1/executions/{id}` 跨 tenant | ✅ 403 |
| N-04 | POST `/v1/execute` SQL injection | ✅ 422 |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_negative_w7.py -v
```

## 6. Verify

- 口令：`【Verify回合】Step 7`

## 7. 等待

Test Step 7 验收 → Verify → `gate step --step 7 -k 'N-01'` → 终轮 `gate delivery`
