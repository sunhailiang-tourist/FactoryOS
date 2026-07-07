# studio-discover

## 是什么

Studio **第 2 步 · Discover**：上传 OpenAPI/Blueprint，列出候选 CMV 动词。

## 功能

- 上传或选择 Blueprint
- `POST /v1/integration/discover` · `POST /v1/integration/blueprint/validate`
- 展示动词/实体候选清单供 Map 步选用

## 业务含义

把 Legacy 系统能力「发现」为 Pack 可映射候选，避免手改 YAML（STU-R2）。

## 用法

integrator 在 Connect 通过后进入；与 customer_it 核对 API 文档完整性。

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-discover` |
| route name | `studio.discover` |
| path | `/studio/discover` |
| i18n namespace | `studio-discover` |
| rbac permission | `studio.discover.view` |
| layout | `studio` |
| store | 待 Step 4 |
| api | `integration.discover` · `integration.blueprint.validate` |

## 上下游

- **上游**：Connect 连通报告
- **下游**：Map 步字段映射

## 不负责

- 映射编辑与 AI 建议（Map）
- Contract Test（Prove）

## 验收（AC）

- **STU-01**：零仓库 onboard 链 discover 步可完成（P0）

## 变更规则

1. 改 `router/modules/studio-discover/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioDiscoverPage.lazy.tsx`
- 路由：`router/modules/studio-discover/registry.ts`
