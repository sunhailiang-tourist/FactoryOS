# 测试用例与改动面：W2 audit · execution failing tests

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`
- **命名**：`test-1813-w2-audit-execution.md`（HHmm=1813 落盘当下本地时间）
- **目的**：新增 · W2 Step1～4 failing tests（E-03 · E-06 · E-07 · E-09 · workflow 存量）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_audit_e03.py` | 新增 | E-03 · W2 migration 002 表 |
| `src/tests/integration/test_execution_e06_e07.py` | 新增 | E-06 dry_run · E-07 幂等 |
| `src/tests/integration/test_execution_e09.py` | 新增 | E-09 evidence HTTP |
| `src/tests/conftest.py` | 修改 | `api_client` · `sample_execute_request` fixture |
| `src/tests/ac/test_base001_registry.py` | 修改 | W2 目标 AC 移出 pending 池 |

## 2. AC 用例

| ID | 标题 | 类型 | 期望 |
|----|------|------|------|
| workflow | import_boundaries | workflow | 存量绿（W1 已覆盖） |
| E-03 | Audit 产生 | integration | 执行后 GET `/v1/audit/events` 有 append-only 记录 |
| E-06 | dry_run 不写 | integration | `dry_run=true` → status=simulated · Legacy 不变 |
| E-07 | idempotency | integration | 同 `idempotency_key` 不重复写 · 返回同一 exec |
| E-09 | Evidence 可重建 | integration | GET evidence 200 · 过 ExecutionEvidence required |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'workflow'
./scripts/gate step --step 2 -k 'E-03'
./scripts/gate step --step 3 -k 'E-06'
./scripts/gate step --step 4 -k 'E-09'
```

## 4. 标准测试用例

| ID | 标题 | 类型 | 前置 | 步骤摘要 | 期望 |
|----|------|------|------|----------|------|
| E-03 | audit HTTP | integration | migration 002 · execute dry_run | GET `/v1/audit/events?tenant_id&exec_id` | ≥1 AuditEvent |
| E-06 | dry_run | integration | execution_service | execute dry_run=true | simulated · mock write count=0 |
| E-07 | 幂等 | integration | execution_service | 同 key 两次 execute | 同 exec_id · write count 不增 |
| E-09 | evidence | integration | POST `/v1/execute` | GET `/v1/executions/{id}/evidence` | required 字段齐全 |

### DB 策略

- 延续 W1：`TEST_DATABASE_URL` 或 SQLite `cache=shared` + Alembic upgrade head（含 `002_*`）
- E-06/E-07 通过 `os_core.execution_service` 公开 API（Step3 无 HTTP）

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-1809-w2-audit-execution.md` ✓ |
| Step 范围 | 1～4 · E-03/06/07/09 ✓ |
| 不在 W2 | E-01/02/04/05 · D-* · G/R · 52 其余 pending ✓ |
| 必测 | E-03 · E-06 · E-07 · E-09 · workflow 存量回归 |
| 回归 | W1 S-* · C-01 · contract · workflow 全量 |
| 公共链路风险 | **中** — 触及 execution 写路径 · audit append-only · 无 Rule/Graph 运行时 |
| 红线 | 写仅经 execution_service · dry_run 不写 Legacy · audit 无 UPDATE/DELETE |
