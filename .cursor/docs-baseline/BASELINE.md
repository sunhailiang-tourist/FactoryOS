# docs 认知基线（docs-baseline）

> **非执行真源** — 用于检测 `docs/` 厚文档演进，并驱动 `.cursor/factoryos/` 工作流同步。  
> 机器契约仍以 `contracts/` 为准；研发闸门仍以 `.cursor/factoryos/` 为准。

## 目录层次（资源隔离）

```text
.cursor/docs-baseline/
├── BASELINE.md              # 本说明（人读）
├── policy/
│   └── WORKFLOW_MAP.json    # docs 路径 → factoryos 受影响项（手维护）
├── manifest/
│   └── MANIFEST.json        # 全量指纹 + tier（refresh 生成）
├── mirror/
│   └── docs/                # 文本镜像，与仓库 docs/ 同相对路径
└── reports/                 # diff 本地输出（不提交报告正文）
```

| 区 | 职责 | 谁改 |
|----|------|------|
| `policy/` | 策略映射、分类规则延伸 | 人 / Agent（有目的时） |
| `manifest/` | 机器快照元数据 | **仅** `docs_baseline refresh` |
| `mirror/` | 可 diff 的文本副本 | **仅** refresh |
| `reports/` | 临时对比报告 | diff / gate 命令 |

## Tier 分类

| Tier | 含义 | 镜像 | CI |
|------|------|------|-----|
| **A** | 工作流敏感（ADR、验收、编码门禁、治理） | ✅ | 变更未 refresh → **fail** |
| **B** | 参考材料（准备、连接器样例、规格长文） | ✅ | 变更未 refresh → **warn** |
| **C** | 已被取代（`docs/数据结构`、`docs/接口`、`docs/scripts`） | ✅ + `superseded_by` | 与 `contracts/` 不一致 → **fail** |
| **D** | 二进制（png/svg/xlsx） | 仅 hash | 变更未 refresh → warn |

## 命令

```bash
./scripts/docs_baseline refresh              # 冻结当前 docs/ 为基线
./scripts/docs_baseline diff                 # 对比 docs/ vs 基线 → reports/latest-diff.md
./scripts/docs_baseline workflow-check       # Tier-A 变更 + 映射命中
./scripts/docs_baseline contracts-crosscheck # Tier-C vs contracts/
./scripts/gate docs-sync                     # PR 分级门禁（A/C fail · B warn）
```

## 刷新纪律

1. **W1 开工前**：执行一次 `refresh`（首版基线）
2. **有意大改 docs/**：改完后 `refresh` + 检查 `workflow-check` 建议项，更新 `.cursor/factoryos/`
3. **禁止**手改 `manifest/`、`mirror/`（除首次落地外的日常维护）

## 与 SH-步步流

Step0-B：若 `workflow-check` 报 Tier-A 未同步 → 标 **B 类缺口**，等你拍板后再 `可以继续`。
