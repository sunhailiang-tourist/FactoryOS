# Step 停机：Step 2 — audit HTTP + E-03

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`
- **时间**：2026-06-26 09:41

## 1. Step 标识

Step 2 — GET /v1/audit/events · POST /v1/execute（产生 audit）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/apps/api/deps.py` | DB 会话 + alembic upgrade |
| `src/apps/api/routes/audit.py` | GET /v1/audit/events |
| `src/apps/api/routes/execute.py` | POST /v1/execute |
| `src/os_core/execution_service/` | execute 内核（E-03 依赖） |
| `src/os_core/connector_sdk/mock_legacy.py` | mock 写计数 |
| `src/os_core/shared_contracts/models/execution.py` | ExecuteRequest |
| `src/apps/api/main.py` | 注册 audit/execute 路由 |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| E-03 | GET /v1/audit/events · POST /v1/execute | pytest 绿 |

## 4. Harness

```bash
pytest src/tests/integration/test_audit_e03.py -k 'E-03'  # PASS
check_static_quality.py  # PASS
```

## 5. 等待

【Test·Step 2 验收】→ 【Verify回合】Step 2 → `gate step --step 2 -k 'E-03'`
