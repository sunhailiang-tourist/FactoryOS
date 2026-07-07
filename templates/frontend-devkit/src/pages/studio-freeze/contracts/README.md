# studio-freeze

## 是什么

Studio **第 5 步 · Freeze**：Graph 工作坊提交与冻结，人审 Gate 上屏。

## 功能

- Graph 版本 submit / freeze 操作 UI
- `POST /v1/graphs/{id}/versions/{version}/submit` · `.../freeze`
- 展示冻结状态与 Audit **GRAPH_FREEZE**

## 业务含义

业务规则图定版；禁止 API 直调 freeze 绕过 UI 作为生产路径（STU-05、STU-R3）。

## 用法

业务负责人在 Prove 通过后进入；冻结后 Harness/生产读 frozen Graph。

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-freeze` |
| route name | `studio.freeze` |
| path | `/studio/freeze` |
| i18n namespace | `studio-freeze` |
| rbac permission | `studio.freeze.view` |
| layout | `studio` |
| api | `graphs.submit` · `graphs.freeze` |

## 上下游

- **上游**：Prove 开写批准
- **下游**：Export · Harness plan→confirm

## 不负责

- Package JSON 组装（Export）
- 工人 H5 确认流（阶段 2 UX-001）

## 验收（AC）

- **STU-05**：Studio freeze + Audit `GRAPH_FREEZE`

## 变更规则

1. 改 `router/modules/studio-freeze/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioFreezePage.lazy.tsx`
- 路由：`router/modules/studio-freeze/registry.ts`
