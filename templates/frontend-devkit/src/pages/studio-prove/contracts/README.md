# studio-prove

## 是什么

Studio **第 4 步 · Prove**：Shadow 模式、Contract Test、对账样例与开写批准入口。

## 功能

- 开启/确认 `tenant.shadow_mode`
- `POST /v1/integration/prove/run`
- 展示 Contract Test 与 K-01 对账结果
- 触发 **G-WRITE-APPROVE** 人审（Audit `integration.write_approved`）

## 业务含义

生产写前的硬 Gate：Shadow 期间 L2 写 Legacy 须 403 或 simulated（STU-03、STU-04）。

## 用法

| 角色 | 行为 |
|------|------|
| integrator | 跑 Prove、提交开写申请 |
| admin | shadow 开关（若独立入口则复用 admin 能力） |
| 业务负责人 | 签字批准开写 |

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | `studio-prove` |
| route name | `studio.prove` |
| path | `/studio/prove` |
| i18n namespace | `studio-prove` |
| rbac permission | `studio.prove.view` |
| layout | `studio` |
| api | `integration.prove.run` |

## 上下游

- **上游**：Map 映射 · Pack Contract Test 定义
- **下游**：Freeze · 生产写路径

## 不负责

- Graph submit/freeze UI（Freeze 步）
- Package 导出（Export）

## 验收（AC）

- **STU-03**：shadow_mode 与 L2 写拦截
- **STU-04**：开写双签与 Audit
- 规格 §3 Prove 四规则

## 变更规则

1. 改 `router/modules/studio-prove/registry.ts` · store · api → **同步** 本文件追踪链 + `router|store|api/contracts/README.md` 登记索引。
2. `scripts/check_harness.py` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：`StudioProvePage.lazy.tsx`
- 路由：`router/modules/studio-prove/registry.ts`
