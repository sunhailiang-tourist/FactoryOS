# contracts · 机器契约真源（B 策略）

本目录为 **CI / pytest / Agent 契约** 唯一机器可读真源；日常编码不依赖 `docs/`。

| 路径 | 内容 |
|------|------|
| `openapi/` | FactoryOS Platform API v1.1.1 |
| `schemas/` | 16 份 JSON Schema |
| `cmv/` | CMV 注册表 + 同步规则 |
| `acceptance/` | AC-BASE / MVP / UX / B-LITE 验收用例 |
| `fixtures/business-graphs/` | Graph/RuleSet 草稿 JSON |

## 门禁

```bash
./scripts/harness --tier contracts    # L0
./scripts/gate plan                   # 确认规划（含 L0）
./scripts/gate pr                     # CI 同款全量
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| `openapi/` · `schemas/` | `harness --tier contracts` + contract pytest |
| `acceptance/` | 更新 `src/tests/ac/` · AC-P0-INDEX |
| 与 `docs/文档/数据结构` 对齐 | **只改本目录**；`docs_baseline contracts-crosscheck` |

## 认知策略

- 工作流：[.cursor/factoryos/INDEX.md](../.cursor/factoryos/INDEX.md)
- docs 漂移：[.cursor/docs-baseline/BASELINE.md](../.cursor/docs-baseline/BASELINE.md)
- 开发前链路：[PRE-DEV-CHAIN.md](../.cursor/factoryos/PRE-DEV-CHAIN.md)

厚 ADR 仍在 `docs/`（可选外迁）；**改契约只改本目录**。
