# shared_contracts/models · Pydantic 领域模型

本目录为 **`contracts/schemas` export 的运行时代码映射**（published 真源 = Contract Registry · ADR-008）；全平台 DTO 单一 import 路径 `os_core.shared_contracts.models`。

| 文件 | 对齐 Schema / 用途 |
|------|-------------------|
| `execution.py` | ExecutionRecord · ExecutionEvidence |
| `audit.py` | AuditEvent |
| `dsl.py` | DslPlan · PlanStep |
| `graph.py` | BusinessGraph |
| `rule.py` | RuleSet |
| `domain.py` | DomainEvent 信封 |
| `common.py` | 跨模型共用类型 |
| `__init__.py` | 聚合导出 `__all__` |

## 门禁

```bash
uv run pytest src/tests/contract/test_shared_contracts.py -q
./scripts/harness --tier contracts
./scripts/gate step --step 2 -k 'workflow'
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| 字段增删 | **先** Contract Registry publish → 同步 `contracts/schemas/` export → 再改本目录 · contract pytest 绿 |
| 新模型文件 | 更新 `__init__.py` `__all__` · 父级 [shared_contracts/README.md](../README.md) |
| ORM 实体 | 各 service 自有表模型；字段语义须与本目录 Pydantic 一致 |

## 不负责什么

- JSON Schema **published 真源**（Contract Registry）；**export 镜像**在 `contracts/schemas/`
- 数据库表定义（在 `src/server/db/migrations/versions/`）
- 校验规则、Graph/Rule 业务语义

## 文档链接

- [shared_contracts/README.md](../README.md)
- [contracts/schemas/](../../../../contracts/schemas/)
- W1 plan Step2 优先 Schema 清单
