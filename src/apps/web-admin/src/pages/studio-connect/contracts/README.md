# studio-connect

## 是什么

Studio **第 1 步 · Connect**：录入凭证引用、测试 ERP/Edge 连通。

## 功能

- 选择 tenant / Path 模板、绑定 `system_relations`
- 提交 `secrets_ref`（Vault 引用，**非**明文）
- 触发 `POST /v1/integration/connect/test` 并展示连通报告

## 业务含义

新客户 onboard 的第一步（Playbook **G-CONNECT**）；Registry 经 API 写入 draft relation（STU-R1）。

## 用法

| 角色 | 行为 |
|------|------|
| integrator + customer_it | 填凭证 ref、部署 Edge（私网 ERP）、点「测试连通」 |
| operator | 无访问 |

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-connect` |
| route name | `studio.connect` |
| path | `/studio/connect` |
| i18n namespace | `studio-connect` |
| rbac permission | `studio.connect.view` |
| layout | `studio` |
| store key | `studio/connect`（Step 4 实现） |
| api id | `studio.connect.test` → `postConnectTest()` |

## 上下游

- **上游**：tenant 已 provision · Path 模板（STU-10）
- **下游**：Discover 步 · Audit `integration.connect_ok`

## 不负责

- Blueprint 上传（Discover）
- 字段映射编辑（Map）
- CLI `factoryos integration connect`（仅平台研发调试，非 D1 主路径）

## 验收（AC）

- **STU-02**：connect 后 DB 有 `system_relations` / `connector_instances`
- **STU-11**：Registry 仅存 `secrets_ref`，无明文密钥

## 变更规则

1. 改 `router/modules/studio-connect/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioConnectPage.lazy.tsx`
- HTTP 只经 `api/request/client.ts`；业务调用放 `api/functions/studio-connect/*.fn.ts`
- 路由：`router/modules/studio-connect/registry.ts`
