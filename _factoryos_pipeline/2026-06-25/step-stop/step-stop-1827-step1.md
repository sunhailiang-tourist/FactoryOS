# Step 停机：Step 1 — Alembic + audit_service 内核

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`
- **时间**：2026-06-25 18:27

## 1. Step 标识

Step 1 — Alembic 002 + audit_service append-only 内核

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `alembic/versions/002_audit_execution.py` | 新增 audit_events · execution_records |
| `src/os_core/audit_service/__init__.py` | 包入口 |
| `src/os_core/audit_service/store.py` | append_audit_event · list_audit_events |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| workflow | 无 HTTP | pytest 绿 |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 业务在 os_core |
| 2 | 响应契约 | Pass — AuditEvent Pydantic |
| 3 | 鉴权/租户 | Pass — 查询带 tenant_id |
| 4 | 红线 | Pass — 仅 INSERT |
| 5 | Schema | Pass — 对齐 AuditEvent.schema |
| 6 | 输入校验 | Pass — Actor.model_validate |
| 7 | Shadow | N/A Step1 |
| 8 | 幂等/补偿 | N/A — execution_records 表已预埋唯一索引 |
| 9 | 静态检查 | Pass |
| 10 | 注释 | Pass |

## 5. Harness 结果

```bash
pytest src/tests/integration/test_audit_e03.py::test_w2_audit_execution_migration_tables \
  src/tests/integration/test_audit_e03.py::test_audit_service_append_only_kernel \
  src/tests/workflow/ -k 'workflow' -q
# 3 passed
```

待：`./scripts/gate step --step 1 -k 'workflow'`（需 Test·Step1 + Verify 后）

## 6. 最短验证路径

`alembic upgrade head` → `append_audit_event` → `list_audit_events` 有记录

## 7. Verify（必填）

- 落盘：`verify/verify-<HHmm>-step1.md`
- 口令：`【Verify回合】Step 1`

## 8. 等待

请：**【Test·Step 1 验收】** → **【Verify回合】Step 1** → `gate step` 绿 → `可以继续`
