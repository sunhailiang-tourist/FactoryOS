# contracts · export 镜像（ADR-008 废止编辑真源）

> **状态**：Export / CI 镜像 · **非**运行时日常编辑真源  
> **真源**：[ADR-008](../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md) · PostgreSQL `contract_*` Registry + Studio publish

本目录保留 **export/import 快照** 与 **gate/contract pytest 对账镜像**；日常契约变更经 Studio publish 写入 Registry，再 export 回本目录（CI 可选）。

| 路径 | 内容 |
|------|------|
| `openapi/` | FactoryOS Platform API v1.1.1 |
| `schemas/` | 16 份 JSON Schema |
| `cmv/` | CMV 注册表 + 同步规则 |
| `acceptance/` | AC-BASE / MVP / UX / B-LITE 验收用例 |
| `fixtures/business-graphs/` | Graph/RuleSet 草稿 JSON |

## 门禁

```bash
./scripts/harness --tier contracts    # L0（对 published contract_set + export 镜像）
./scripts/gate plan
./scripts/gate pr
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| Registry publish 后 export | `harness --tier contracts` + contract pytest |
| `acceptance/` | 更新 `src/tests/ac/` · AC-P0-INDEX |
| 与 `docs/文档/数据结构` 对齐 | Registry artifact 格式 · docs_baseline crosscheck |

## 认知策略

- 工作流：[.cursor/factoryos/INDEX.md](../.cursor/factoryos/INDEX.md)
- UI-FIRST：[UI-FIRST-CONFIG-PRINCIPLE.md](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)
- ADR-008：配置与契约平面 DB 化

**禁止**：将本目录作为实施顾问日常编辑入口。
