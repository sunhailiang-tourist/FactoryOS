# web-admin 工程策略

> 版本：**v1.4.0** · DevKit Profile · 与 [ARCHITECTURE.md](./ARCHITECTURE.md) v1.8 配套  
> **v1.4**：Playwright · size-limit · Storybook · RHF+Zod · sector ESLint  
> **v1.3**：API 四层 · codegen · Query 层界 · MSW · RTL 基座  
> **一键激活**：`./scripts/activate.sh` · **一键自检**：`pnpm check` + `scripts/check_harness.py`

## 0. DevKit（可独立迁出）

| 文件 | 用途 |
|------|------|
| [devkit.profile.yaml](./devkit.profile.yaml) | Profile 声明（**WEB-PROFILE** · W-01～W-11 checks） |
| [devkit.manifest.standalone.yaml](./devkit.manifest.standalone.yaml) | **Standalone 模板** |
| [TEMPLATE.md](../../../templates/frontend-devkit/TEMPLATE.md) | **frontend-devkit 金样模板**（一键 scaffold 新 App） |
| [scripts/activate.sh](./scripts/activate.sh) | 一键激活 |
| [scripts/check_harness.py](./scripts/check_harness.py) | L1 工程门禁真源 |
| [scripts/check_codegen_fresh.py](./scripts/check_codegen_fresh.py) | OpenAPI → generated 同步（S1） |
| [DEVKIT.md](../../../.cursor/factoryos/DEVKIT.md) | 伞形 / standalone 说明 |

## 1. 门禁分层

| 层 | 命令 | 内容 |
|----|------|------|
| L0 本地 | `pnpm check` | codegen · tsc · ESLint · Vitest · build · size · Playwright · Storybook build |
| L1 DevKit | `scripts/check_harness.py` | registry · 文件头 · contracts · query 层界 · codegen · 架构 tooling |
| L2 Umbrella | `./scripts/harness --tier step` | `devkit_profiles` **调度** web-admin（不重复规则） |

## 2. Registry 自动聚合（禁止手工 patch 聚合文件）

| 板块 | 子目录 | 导出常量 |
|------|--------|----------|
| router | `modules/{module-id}/` | `ROUTE_MODULE_ENTRIES` |
| store | `modules/{module-id}/` + `common/` | `STORE_MODULE_ENTRIES` |
| layout | `modules/{domain}/` | `LAYOUT_MODULE_ENTRIES` |
| config | `modules/{domain}/` | `CONFIG_MODULE_ENTRIES` |
| api/functions | `functions/{module-id}/` | `API_MODULE_ENTRIES` |

`pnpm create:module` 创建 router·pages·store·api·mocks·**i18n·rbac** 子切片（含 `permissions` 与 contracts 登记）；**勿**手改聚合 `registry.ts`。

## 3. import 边界（ESLint 强制）

| 规则 | 说明 |
|------|------|
| `pages/**` 禁止 `fetch` | 必须经 `@/api/query/hooks` |
| `pages/**` 禁止 `echarts` | 必须经 `@/components/charts` |
| `pages/**` 禁止 `@/api/functions` 直引 | 必须经 `@/api/query/hooks` |
| `pages/**` 禁止 `@tanstack/react-query` 直引 | 必须经 `@/api/query/hooks` |
| `api/query/hooks/**` | 允许 `api/functions` + `@tanstack/react-query` |
| `api/functions/**` | 仅 `api/request` + `api/generated` 类型 |
| `api/request/**` | 禁止 pages/components/query/functions |
| `components/**` | 禁止 pages · query hooks |

## 3a. API 四层（v1.7 · S1）

| 层 | 路径 | 职责 |
|----|------|------|
| L0 契约 | `api/generated/openapi.d.ts` | `pnpm codegen:api` · **禁止手改** |
| L1 传输 | `api/request/` | client · interceptors · errors |
| L2 fetch | `api/functions/{id}/*.fn.ts` | 纯 async · 无 React |
| L3 Server State | `api/query/hooks/` | TanStack Query · queryKey 工厂 |

**codegen**：

```bash
pnpm codegen:api      # 写 generated/
pnpm codegen:check    # 变更 OpenAPI 后须 diff 为空
```

## 3b. 样式分层（v1.6）

| 层 | 技术 | 用途 |
|----|------|------|
| Token | `theme.ts` → `syncThemeVars` | Design Token |
| 组件 | MUI | Form · Table · Dialog |
| 原子 | Tailwind v4 | flex · gap · padding |
| 模块 | `pages/{id}/styles/*.module.css` | 页面私有 |
| 图表 | `@/components/charts` | ECharts |
| 动效 | `@/styles/motion` | animate 白名单 |

## 4. 目录禁词（harness 强制）

- 禁止 `src/common/`（用 `@/components/` 或 `{sector}/common/`）
- 禁止任意 `**/shared/**` 目录名

## 4b. 契约同步（绝对门禁）

| 层级 | 契约路径 | 须同步内容 |
|------|----------|------------|
| 页面模块 | `pages/{module-id}/contracts/README.md` | 追踪链含 **query hook** |
| 板块根 | `{router,store,api,layout,config}/contracts/README.md` | 登记索引 |
| query | `api/query/contracts/README.md` | queryKey ↔ module-id ↔ fn |
| generated | `api/generated/README.md` | codegen 规则 |

## 4c. 文件头注释（绝对门禁）

每个 `.ts` / `.tsx`（除 `vite-env.d.ts`）须含 **7 标签**：模块 · 作用 · 怎么用 · 解决 · 上游 · 下游 · 关联。

## 5. 契约镜像（迁出必选 · vendor 自给）

| 镜像 | 路径 | 维护 |
|------|------|------|
| OpenAPI + schemas | `vendor/factoryos-contracts/openapi/` · `schemas/` | monorepo 内 `sync_vendor_contracts.sh` |
| 错误码 SSOT | `vendor/factoryos-contracts/error-registry.yaml` | `scripts/sync_error_registry.py --apply` |
| TS 消费 | `api/request/error-codes.ts` | **禁止手改** · `pnpm codegen:registry:check` |
| OpenAPI 消费 | `api/generated/openapi.d.ts` | `pnpm codegen:api` · `pnpm codegen:check` |

**钉死**：standalone **不** 依赖 `../../../contracts/`；umbrella 内 `sync_vendor_contracts.sh` 仅开发便利。

### 错误码变更 SOP（App 内自给）

```bash
# 1. 改 vendor/factoryos-contracts/error-registry.yaml（或 bump submodule）
# 2. 检查 drift
pnpm codegen:registry:check
# 3. 确认后写盘
python scripts/sync_error_registry.py --apply
# 4. 再验绿
pnpm codegen:registry:check
```

## 6. 测试策略（v1.3）

| 类型 | 位置 | 用途 |
|------|------|------|
| 单元 | `src/**/*.test.ts` | request · registry · motion · charts |
| 组件/集成 | `src/**/*.test.tsx` · `src/test/render.tsx` | RTL + MSW · router · hooks · layout |
| 模块冒烟 | `src/pages/studio-steps.smoke.test.tsx` | 七 module-id lazy 页参数化 |
| Mock | `src/mocks/` | Vitest server · dev `VITE_MSW=1`（main.tsx 条件启 worker） |
| E2E | `e2e/` + Playwright | 壳层 **9** 场景 · 六步路由 + 侧栏导航 |
| Storybook | `.storybook/` + `*.stories.tsx` | **7 页模块** + Global 组件 · `storybook:build` 纳入 check |
| 体积 | `scripts/check_bundle_size.py` | build 后 vendor chunk 上限 |
| 联调 pytest | `src/tests/integration/`（FactoryOS 根） | **非** WEB-PROFILE 验收盘 · 联调轨专用 |

**Vitest**：`vitest.config.ts` · `environment: jsdom` · `setupFiles: src/test/setup.ts`

## 7. 新建模块 Checklist

```bash
pnpm create:module
# 1. pages/{id}/contracts/README.md（含 useXxx hook 名）
# 2. api/functions/{id}/*.fn.ts + api/query/hooks/useXxx.ts
# 3. mocks/handlers/{id}.ts
# 4. pnpm codegen:api（若 OpenAPI 有新 path）
# 5. pnpm codegen:registry:check
# 6. pnpm check && ./scripts/check_harness.py
```

## 8. 流水线（WEB-PROFILE 轨）

- Charter：[plan-web-admin-profile-autonomy.md](../../../_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md)
- v1.7 分步：[plan-web-admin-s1-base-v17.md](../../../_factoryos_pipeline/2026-07-06/plan/plan-web-admin-s1-base-v17.md)
- **验收盘**：`./scripts/activate.sh`（**禁止** 用 STU `gate step` 代替）
- Umbrella `./scripts/gate step -k 'W-0N'` 仅 optional · 改 `src/apps/web-admin/**` 时
- Test Agent **不** 写 App 内 Vitest；App 测试由 Dev / 本仓维护

## 9. 目录 README 门禁（D15）

每个**登记目录**须有 `README.md`（格式参照 [contracts/README.md](../../../contracts/README.md)）。

| 类型 | 要求 |
|------|------|
| 应用根子目录（`devkit/` `vendor/` `scripts/` …） | 完整五节：是什么 · 子路径 · 门禁 · 变更纪律 · 相关文档 |
| `src/` 一级 sector | README 存在 + harness sector contracts 对账 |
| 未登记新目录 | **禁止** — 须用户确认后写入 `contracts/directory-readmes.yaml` |

```bash
uv run python scripts/check_directory_readmes.py   # umbrella
bash scripts/py.sh scripts/check_harness.py        # web-admin 子树
```

结构锁死后变更 SOP：用户确认 → `directory-readmes.yaml` + `repo-structure.yaml` + `gate pr`。

## 10. 性能基准 S4（锁死 · 无 SSR）

| 能力 | 落点 | 门禁 |
|------|------|------|
| 首屏占位壳 | `index.html#fos-boot-shell` | 人工 + Lighthouse |
| 默认 MSW | `.env.development` `VITE_MSW=1` | `pnpm dev` |
| 骨架屏 | `@/components/skeletons` | RTL |
| 路由错误降级 | `RouteErrorFallback` + `errorElement` | 路由测试 |
| 数据预取 | `router/loaders` + `StudioNavLink` prefetch | harness |
| 切屏动画 | `StudioAnimatedOutlet` + `styles/motion` | e2e |
| 响应式壳 | `StudioShellLayout` md↓ temporary drawer | RTL |
| vendor-react | `vite.config.ts` manualChunks | `check_bundle_size.py` |
| 资源三角 | `check_resource_chain.py` | harness |

目标（PC）：LCP P75 < 1.5s · 步间导航感知 < 200ms · CLS < 0.05。

## 11. i18n + RBAC（S5 · 锁死）

| sector | 路径 | 消费入口 |
|--------|------|----------|
| i18n | `i18n/modules/{module-id}/` | `useT(namespace)` · 禁止直引 i18next |
| rbac | `rbac/modules/{domain}/` | 路由 `permissions` · `RbacGuard` · `usePermissions`（按钮级预留） |

追踪链：`pages/{id}/contracts` 须含 `i18n namespace` · `rbac permission`。

form 生成（S7）：`scripts/form/` · 契约 `scripts/form/contracts/README.md`。
