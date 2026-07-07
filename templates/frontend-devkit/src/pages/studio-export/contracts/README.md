# studio-export

## 是什么

Studio **第 6 步 · Export**：导出 Implementation Package；第二家 **import** 向导入口。

## 功能

- `POST /v1/packages/export` 下载 Package JSON
- import 向导（STU-07）：选模板 + Override + 填凭证
- 含 Graph/Rule/Pack 引用，与 P-01～P-03 一致

## 业务含义

首家 D1 交付物与第二家复制飞轮起点（STU-R5）；Git `integration/` 仅为 export 镜像。

## 用法

| 场景 | 行为 |
|------|------|
| 首家 D1 | Export Package v1 |
| 第二家 S1 | Import → Override → Prove（步骤数少于首家） |

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-export` |
| route name | `studio.export` |
| path | `/studio/export` |
| i18n namespace | `studio-export` |
| rbac permission | `studio.export.view` |
| layout | `studio` |
| api | `packages.export` · `packages.import` |

## 上下游

- **上游**：Freeze 完成
- **下游**：阶段 3 哈森 UAT · 第二家 tenant

## 不负责

- Pack 市场/catalog（Y2）
- drift 仪表盘（P1 可选）

## 验收（AC）

- **STU-06**：可下载 Package JSON
- **STU-07**：第二家 import 主路径在 Studio
- **STU-08**：Runbook 无「改 YAML 上线」

## 变更规则

1. 改 `router/modules/studio-export/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioExportPage.lazy.tsx`
- 路由：`router/modules/studio-export/registry.ts`
