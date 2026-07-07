# studio-shell

## 是什么

Integration Studio **向导壳与概览页**：展示六步 flows 元数据，作为 `/studio/*` 默认入口。

## 功能

- 拉取并展示 `GET /v1/studio/flows` 步骤列表（sidebar 与概览共用 store）
- 概览页说明向导用途与已注册步骤数

## 业务含义

实施顾问进入 Studio 的第一屏；不执行具体接入动作，只提供导航上下文（**壳层 · 非联调业务**）。

## 用法

| 角色 | 行为 |
|------|------|
| integrator / admin | 访问 `/studio`，查看概览后从侧栏进入六步 |
| operator | **403**（联调时 API RBAC；本地 MSW 用 mock 角色） |

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-shell` |
| route name | `studio.home` |
| path | `/studio` |
| layout | `studio` → `layout/modules/studio/StudioShellLayout` |
| store key | `studio/shell` → `useStudioShellStore`（纯 UI 态） |
| i18n namespace | `studio-shell` |
| rbac permission | `studio.shell.view` |
| query hook | `useStudioFlows` → `api/query/hooks/useStudioFlows.ts` |
| api id | `studio.flows.list` → `getStudioFlows()`（经 hook，pages 禁直引） |

## 上下游

- **上游**：`layout` 侧栏、`bootstrap` 初始化 flows
- **下游**：`api/functions/studio-shell/flows.fn.ts` · `store/modules/studio-shell/`

## 不负责

- 各步业务表单（connect / discover / … 独立 page 模块）
- Registry 写入、Graph freeze、Package 导出

## 验收（WEB-PROFILE · 本模块）

- **W-04**：RTL 冒烟可 mount 本页（MSW 提供 flows）
- 侧栏步骤数与 mock/API flows 一致
- **禁止** 写 STU-09 / pytest 作为本模块工程 AC（联调轨另计）

## 变更规则

1. 改 `router/modules/studio-shell/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioHomePage.lazy.tsx`
- 私有组件：`pages/studio-shell/components/`（仅本模块）
- 全局组件：`@/components/`（如 PageLoading）
- 路由登记：`router/modules/studio-shell/registry.ts`（**勿**在 pages 下再建 registry）
