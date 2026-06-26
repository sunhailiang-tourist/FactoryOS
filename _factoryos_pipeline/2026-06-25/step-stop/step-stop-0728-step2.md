# Step 停机：Step 2 — shared_contracts 核心 Pydantic

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **时间**：2026-06-25

## 1. Step 标识

Step 2 — shared_contracts 核心 Pydantic（L0 契约代码化）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/shared_contracts/__init__.py` | 包导出 |
| `src/server/os_core/shared_contracts/errors.py` | ErrorCode 枚举 |
| `src/server/os_core/shared_contracts/schema_loader.py` | Schema 加载器 |
| `src/server/os_core/shared_contracts/models/common.py` | Actor 等共享子模型 |
| `src/server/os_core/shared_contracts/models/audit.py` | AuditEvent |
| `src/server/os_core/shared_contracts/models/dsl.py` | DslPlan |
| `src/server/os_core/shared_contracts/models/graph.py` | BusinessGraph |
| `src/server/os_core/shared_contracts/models/rule.py` | RuleSet |
| `src/server/os_core/shared_contracts/models/domain.py` | DomainEvent |
| `src/server/os_core/shared_contracts/models/execution.py` | ExecutionRecord · ExecutionEvidence |
| `src/server/os_core/shared_contracts/models/__init__.py` | 模型聚合导出 |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| contract | 7 Schema required 对齐 | PASS（7/7） |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 纯 DTO，无写 Legacy |
| 2 | 响应契约 | Pass — required 与 JSON Schema 一致 |
| 3 | 鉴权/租户 | N/A |
| 4 | 红线 | Pass — 无执行逻辑 |
| 5 | Schema | Pass — 7 模型对账绿 |
| 6 | 输入校验 | Pass — Pydantic extra=forbid |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A |
| 9 | 静态检查 | Pass |
| 10 | 注释 | Pass — 文件头 + 字段 Field description |

## 5. Harness 结果

```bash
.venv/bin/python scripts/gate_cli.py step --step 2 -k 'contract'
```

```text
harness full + pytest -k contract : PASS
static quality : PASS
verify : MISSING
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/contract/test_shared_contracts.py -v
```

## 7. Verify（必填）

口令：`【Verify回合】Step 2`

## 8. 等待

Verify 落盘且 gate step 全绿后：`可以继续`
