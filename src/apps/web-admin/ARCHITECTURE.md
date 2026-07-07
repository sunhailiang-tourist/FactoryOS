# web-admin 前端架构 v1.7

> 版本：**v1.8.0+s5** · 日期：2026-07-07  
> **v1.8**：Playwright 壳层 · bundle size · Storybook · RHF+Zod · eslint sector 矩阵（WEB-PROFILE S2+S3）  
> **v1.7**：API 四层链 · TanStack Query · MSW · 测试基座（WEB-PROFILE S1）  
> **v1.6**：四层样式 · ECharts · animate 预设 · CSS Modules per module  
> **工程策略**：[ENGINEERING.md](./ENGINEERING.md) · 一键 `./scripts/activate.sh`

---

## 0. 前端自治域（钉死 · 2026-07-06）

```text
┌─────────────────────────────────────────────┐
│  web-admin = Frontend Autonomous Domain      │
│  验收盘：./scripts/activate.sh（无 server）   │
│  ac_scope：WEB-PROFILE（≠ STU-001）          │
└─────────────────────────────────────────────┘
         │ 联调时（后置）
         ▼
   REST API（外部 · 非架构前置）
```

| 层 | 职责 | 与后端 |
|----|------|--------|
| L0 治理 | DevKit Profile · harness · 7 标签 | **无** |
| L1 壳 | router · layout · theme · motion | **无** |
| L2 客户端 | request · functions · query · generated | **只消费** pinned 契约镜像 |
| L3 假数据 | MSW · fixtures | **替代** live API 直至联调 |
| L4 质量 | vitest · RTL ·（S2）Playwright | **无** pytest |

**禁止**：用 STU Step / OpenAPI 业务 path / `src/tests/**` 定义或阻塞 WEB-PROFILE。

Charter：[_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md](../../../_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md)

---

## 1. 应用完整结构（v1.7 目标树）

```text
src/apps/web-admin/
├── README.md · ARCHITECTURE.md · ENGINEERING.md
├── package.json · vite.config.ts · vitest.config.ts · eslint.config.js
├── devkit.profile.yaml · devkit.manifest.standalone.yaml
├── scripts/
│   ├── activate.sh · check_harness.py · create-module.mjs
│   ├── check_codegen_fresh.py          # OpenAPI → generated 同步
│   └── devkit/
├── devkit/kernel/                      # standalone AI 内核快照
└── src/
    ├── main.tsx                        # import @/styles/global.css
    ├── bootstrap.tsx                   # QueryClientProvider · 可选 MSW
    ├── AppShell.tsx
    ├── vite-env.d.ts
    ├── registry.harness.test.ts
    │
    ├── test/                           # 测试基座（非业务）
    │   ├── setup.ts
    │   └── render.tsx
    │
    ├── mocks/                          # MSW · VITE_MSW=1 本地无后端
    │   ├── browser.ts · server.ts
    │   └── handlers/{module-id}.ts
    │
    ├── styles/                         # L1 Token + L3 Tailwind + motion
    │   ├── contracts/README.md
    │   ├── tokens.css · global.css
    │   ├── styles.test.ts
    │   └── motion/                     # animate 白名单（styles 子目录）
    │       ├── contracts/README.md
    │       ├── presets.ts · MotionContainer.tsx
    │       └── index.ts
    │
    ├── components/                     # 全局 UI（≥2 模块复用）
    │   ├── README.md · index.ts
    │   ├── AppThemeProvider.tsx · PageLoading.tsx
    │   ├── theme.ts · syncThemeVars.ts
    │   └── charts/                     # ECharts 封装
    │       ├── contracts/README.md
    │       ├── register.ts · BaseChart.tsx · LineChart.tsx · BarChart.tsx
    │       └── charts.test.ts
    │
    ├── router/                         # glob → ROUTE_MODULE_ENTRIES
    │   ├── contracts/README.md
    │   ├── browser-router.tsx          # createBrowserRouter（Route.lazy 须 data router）
    │   ├── registry.ts · compose.tsx · types.ts
    │   ├── guards/
    │   └── modules/{module-id}/registry.ts
    │
    ├── layout/                         # 域壳 · glob 聚合
    │   ├── contracts/README.md
    │   ├── registry.ts · RootLayout.tsx
    │   └── modules/{domain}/
    │
    ├── config/                         # feature flags · env
    │   ├── contracts/README.md
    │   ├── registry.ts · env.ts
    │   └── modules/{domain}/
    │
    ├── store/                          # UI / 会话态（Zustand）— 非 Server State
    │   ├── contracts/README.md
    │   ├── registry.ts · types.ts
    │   ├── common/
    │   └── modules/{module-id}/
    │
    ├── api/                            # ★ v1.7 四层数据链
    │   ├── contracts/README.md
    │   ├── registry.ts · registry.types.ts
    │   ├── generated/                  # L0 codegen（禁止手改）
    │   │   ├── README.md
    │   │   └── openapi.d.ts
    │   ├── request/                    # L1 HTTP 传输
    │   │   ├── client.ts · interceptors.ts · errors.ts · error-codes.ts
    │   │   └── errors.test.ts
    │   ├── functions/{module-id}/      # L2 纯 fetch（无 React）
    │   │   ├── registry.ts · *.fn.ts
    │   │   └── index.ts
    │   └── query/                      # L3 Server State（TanStack Query）
    │       ├── contracts/README.md
    │       ├── client.ts · keys.ts · index.ts
    │       └── hooks/use*.ts
    │
    └── pages/{module-id}/              # 业务页 · module-id 注册制
        ├── contracts/README.md
        ├── *.lazy.tsx
        ├── styles/*.module.css
        └── components/
```

**图例**：`{module-id}` = `studio-shell` · `studio-connect` · … · `{domain}` = `studio`

---

## 2. 数据流（v1.7 核心语义）

```text
pages/{id}/*.lazy.tsx
  │  只 import: @/api/query/hooks · @/components · @/store/modules/{id} · @/styles/motion
  │  禁止: fetch · echarts · api/functions 直引 · @tanstack/react-query 直引
  ▼
api/query/hooks/useXxx.ts          ← Server State 唯一入口
  ▼
api/functions/{id}/*.fn.ts         ← 纯 async fetch
  ▼
api/request/client.ts
  ▼
api/generated/openapi.d.ts         ← OpenAPI SSOT 镜像类型
  ▲
contracts/openapi/工厂操作系统-v1.1.yaml

横切: mocks/handlers ↔ api/functions（Vitest / VITE_MSW=1）
UI 态: store/modules/{id}        ← 侧栏 · 向导步 · 本地 draft（非 API 缓存）
```

---

## 3. 组件边界（共用归共用 · 私有归私有）

| 位置 | 职责 | import |
|------|------|--------|
| `@/components/*` | 全局 UI（≥2 模块复用或平台级） | 任意 |
| `@/components/charts/*` | ECharts 封装 | pages lazy import；**禁止** 直接 `echarts` |
| `pages/{id}/components/*` | 单模块业务 UI | **仅** 同 module-id |
| `pages/{id}/styles/*` | 模块私有 CSS Modules | **仅** 同 module-id |
| `layout/modules/*` | 域壳（侧栏/Outlet） | 非页面业务 |
| `api/query/hooks/*` | Server State | 可 import `api/functions` + `@tanstack/react-query` |
| `api/functions/*` | 纯 fetch | 仅 `api/request` + `api/generated` 类型 |

**反冗余**：单模块专用不得进全局；多模块重复须合并到 `@/components/`。

---

## 4. 板块自治原则（module-id 注册制 · 不变）

| 板块 | 子目录命名 | 注册制 |
|------|------------|--------|
| `router` | `modules/{module-id}/registry.ts` | **glob 聚合** · lazy → `@/pages/{id}/*` |
| `pages` | `{module-id}/` | 契约 `contracts/README.md` |
| `store` | `modules/{module-id}/` + `common/` | **glob 聚合** · UI 态子表 |
| `layout` | `modules/{domain}/` | **glob 聚合** · 域壳 |
| `config` | `modules/{domain}/` | **glob 聚合** · feature flags |
| `api/functions` | `functions/{module-id}/` | **glob 聚合** · `API_MODULE_ENTRIES` |
| `api/query` | `hooks/use*.ts` + `keys.ts` | 按 module-id 命名 queryKey |
| `i18n` | `modules/{module-id}/` | namespace = module-id · `useT` |
| `rbac` | `modules/{domain}/` | 路由 `permissions` · `RbacGuard` |
| `styles` | `global.css` · `tokens.css` | 契约 `styles/contracts/README.md` |
| `motion` | `presets.ts` | 契约 `styles/motion/contracts/README.md` |

---

## 5. 追踪链（v1.7 扩展）

以 `studio-shell` 为例：

```text
route name → router/modules/studio-shell
          → pages/studio-shell
          → pages/studio-shell/styles
          → store/modules/studio-shell        # UI 态
          → api/query/hooks/useStudioFlows  # Server State ★
          → api/functions/studio-shell        # fetch
          → api/generated                     # 类型
          → mocks/handlers/studio-shell       # mock
          → pages/studio-shell/contracts/README.md
```

---

## 6. 新建模块

```bash
pnpm create:module
# 1. pages/{id}/contracts/README.md（含 query hook 名）
# 2. 若需 API → api/functions/{id} + api/query/hooks/use*
# 3. mocks/handlers/{id}.ts（或 README 声明 defer）
# 4. pnpm check && ./scripts/check_harness.py
```

---

## 7. 样式 · 图表 · 动效 · 门禁（v1.6 延续）

- HTTP 仅经 `api/request/client.ts` · **pages 禁止 fetch**（ESLint）
- **MUI** — Form/Table/Dialog/Stepper
- **Tailwind v4** — 原子布局；无 preflight
- **CSS Modules** — `pages/{id}/styles/*.module.css`
- **ECharts** — `@/components/charts` · `vendor-echarts` 分包
- **animate.css** — `styles/motion/presets.ts` · `MotionContainer`
- **Token** — `theme.ts` → `syncThemeVars()` → `:root` → Tailwind `@theme`

---

## 8. DevKit 与契约（绝对门禁）

- **DevKit Profile**：`devkit.profile.yaml` · `scripts/activate.sh` · `scripts/check_harness.py`
- 页面模块：`pages/{id}/contracts/README.md` ↔ router/store/api/query 追踪链
- 板块根：`{sector}/contracts/README.md` 登记索引
- 每个 `.ts`/`.tsx` **7 标签文件头**；见 [ENGINEERING.md](./ENGINEERING.md) §4c
- **S1 新增 harness**：`openapi_codegen_fresh` · `query_layer_boundary`
- 独立迁出：[devkit.manifest.standalone.yaml](./devkit.manifest.standalone.yaml)

---

## 9. 样式四层（v1.6 锁死）

```text
L4  pages/{id}/styles/*.module.css     模块私有布局
L3  Tailwind utilities                 原子 spacing/flex
L2  MUI components                      表单/表格/Dialog
L1  CSS Variables ← MUI theme          Design Token 真源
```

---

## 10. 演进路线（基座级 · 非业务）

| 阶段 | 内容 | 状态 |
|------|------|------|
| v1.6 | module-id · 样式四层 · charts · motion · DevKit | ✅ 已落地 |
| **v1.7 S1** | codegen · Query · MSW · RTL 基座 | ✅ WEB-PROFILE W-01～W-05 |
| **v1.8 S2** | Playwright 冒烟 · size-limit 体积门禁 | ✅ WEB-PROFILE W-06～W-07 |
| **v1.9 S3** | Storybook · RHF+Zod · eslint-boundaries 矩阵 | ✅ WEB-PROFILE W-08～W-10 |
| **Standalone S** | vendor 镜像 · codegen 双路径 · simulate 零父仓 | ✅ WEB-PROFILE W-11 |


---

## 11. 架构版本锁（D16）

- 金样：`src/apps/web-admin`
- 模板：`templates/frontend-devkit`（`sync_frontend_template.py`）
- 锁文件：`contracts/frontend-devkit-lock.yaml`
- **结构/治理/技术策略变更须经用户确认** → 改金样 → sync → bump lock version。
