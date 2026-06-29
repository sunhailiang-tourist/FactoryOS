# Step 停机：Step 3 — Alembic 规模预埋 S-01～S-04

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **时间**：2026-06-25

## 1. Step 标识

Step 3 — Alembic 规模预埋（ADR-007 表结构）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `alembic.ini` | 新建 |
| `src/server/db/migrations/env.py` | 迁移环境（支持 pytest 注入 connection） |
| `src/server/db/migrations/versions/001_scale_s01_s04.py` | 四表 + default tenant seed |
| `src/server/os_core/shared_contracts/tenant_registry.py` | TenantRegistry.get_cell |
| `src/server/os_core/shared_contracts/outbox.py` | OutboxPort.publish |
| `src/tests/conftest.py` | SQLite shared + connection 注入 upgrade |
| `src/tests/integration/test_scale_s01_s04.py` | 同上（S-01 同库断言） |

## 3. AC / 接口

| AC ID | 结果 |
|-------|------|
| S-01 | PASS — 四表 + tenants 规模列 |
| S-02 | PASS — default → cell-default / pool |
| S-03 | PASS — TenantRegistry |
| S-04 | PASS — OutboxPort 持久化 |

## 4. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层 | Pass — 持久化在 shared_contracts 端口，无 api 业务 |
| 2 | 响应契约 | N/A |
| 3 | 鉴权/租户 | Pass — tenant_id 列预埋 |
| 4 | 红线 | Pass — 无 Legacy 写 |
| 5 | Schema | Pass |
| 6 | 输入校验 | Pass — publish 参数类型 |
| 7–8 | Shadow/幂等 | N/A |
| 9 | 静态 | Pass |
| 10 | 注释 | Pass |

## 5. Harness

```bash
.venv/bin/python scripts/gate_cli.py step --step 3 -k 'S-01'
```

harness + pytest S-01 子集：**PASS** · verify：**MISSING**

## 6. 最短验证

```bash
uv run pytest src/tests/integration/test_scale_s01_s04.py -v
```

## 7. Verify

`【Verify回合】Step 3`

## 8. 等待

Verify 全绿后：`可以继续` → Step 4
