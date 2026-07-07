# studio-map

## 是什么

Studio **第 3 步 · Map**：编辑 Pack 字段映射，可选 AI 建议与 confidence。

## 功能

- 可视化 mapping 编辑
- `PUT /v1/integration/mappings/{packId}`
- 产出 mapping 文档供 Prove Contract Test 使用

## 业务含义

将 Discover 候选落为 Pack 级字段映射，是「零 Git 配置」核心步之一。

## 用法

integrator 在 Discover 完成后编辑映射；业务负责人可评审映射合理性。

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-map` |
| route name | `studio.map` |
| path | `/studio/map` |
| i18n namespace | `studio-map` |
| rbac permission | `studio.map.view` |
| layout | `studio` |
| api | `integration.mappings.update` |

## 上下游

- **上游**：Discover 候选清单
- **下游**：Prove · Shadow Contract Test

## 不负责

- Shadow 开关与开写批准（Prove）
- Graph 版本冻结（Freeze）

## 验收（AC）

- **STU-01**：onboard 链 map 步可完成

## 变更规则

1. 改 `router/modules/studio-map/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioMapPage.lazy.tsx`
- 路由：`router/modules/studio-map/registry.ts`
