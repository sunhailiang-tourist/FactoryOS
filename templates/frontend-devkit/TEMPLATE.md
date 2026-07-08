# frontend-devkit · 前端工程基座模板

> **模板 ID**：`frontend-devkit` · **版本**：`2.0.0-s5` · **金样真源**：`src/apps/web-admin`  
> **锁文件**：[`contracts/frontend-devkit-lock.yaml`](../../../contracts/frontend-devkit-lock.yaml)  
> **等权声明**：本模板与 web-admin **项目结构、治理策略、技术策略 100% parity**（`check_frontend_template_parity.py` 门禁）。

---

## 〇、架构验证结论（2026-07-07）

> **仓库级开发者手册**（拉代码 → 激活 → 联调 → 红灯）：monorepo 根 [`contracts/README.md`](../../../contracts/README.md#前端工程全流程开发者手册)

| 前提 | 验证结果 |
|------|----------|
| **灵活可扩展** | ✅ module-id 注册制 + `pnpm create:module`；增业务不增框架复杂度 |
| **AI 工作流独立自治** | ✅ WEB-PROFILE · harness 18 项 · 7 标签 · `devkit/kernel` · standalone 验收盘 |
| **业务 + 联调就绪** | ✅ 四层 API · MSW/联调双轨 · i18n/RBAC · S4 性能门禁 |
| **一键复刻** | ✅ `scaffold_frontend_app.sh` + 本模板 parity 锁 |

**结论**：金样已达可交付基座；模板经 `sync_frontend_template.py` 同步，可用于一键生成新前端 App。

---

## 一、一句话

**一条命令复刻 web-admin 级前端基座** → `pnpm install` → `./scripts/activate.sh` → 在注册制下写业务。

---

## 二、业务流 → 项目结构（验证链）

```text
用户/角色
    ↓ getActorContext().role
rbac/modules/{domain}/registry.ts          # 角色→权限
    ↓ permissions on route
router/modules/{module-id}/registry.ts     # 懒加载路由
    ↓
layout/modules/{domain}/                   # 域壳（Studio 响应式侧栏）
    ↓
pages/{module-id}/*.lazy.tsx               # 业务页（只经 query hooks）
    ↓
api/query/hooks → api/functions → api/request → api/generated
    ↑ OpenAPI SSOT（vendor/factoryos-contracts）
横切：i18n/modules/{module-id}/ · mocks/handlers · store/modules（UI 态）
```

### module-id 追踪链（锁死）

每个 `pages/{module-id}/contracts/README.md` 须对齐：

| 项 | 登记 |
|----|------|
| module-id | router registry |
| i18n namespace | `i18n/modules/{id}/` |
| rbac permission | `rbac/modules/{domain}/` |
| query hook | `api/query/hooks/` |
| api id | `api/functions/{id}/` |

---

## 三、一键创建新项目

### Monorepo 内

```bash
./scripts/scaffold_frontend_app.sh <app-id>
# 或
uv run python scripts/devkit/scaffold_frontend_app.py --id <app-id>
```

| 参数 | 说明 |
|------|------|
| `--id` | kebab-case，如 `order-console` |
| `--ac-scope` | 默认 `<PREFIX>-PROFILE` |

脚手架：复制本模板 → 替换标识 → 注册 `devkit.manifest.yaml` → 同步 `devkit/kernel/`。

### 创建后

```bash
cd src/apps/<app-id>
pnpm install
./scripts/activate.sh
```

---

## 四、项目结构（版本锁死 · D16）

```text
<app-id>/
├── ARCHITECTURE.md · ENGINEERING.md · TEMPLATE.md
├── devkit.profile.yaml              # 18 harness checks
├── devkit.manifest.standalone.yaml
├── devkit/kernel/                   # AI 步步流快照
├── vendor/factoryos-contracts/      # OpenAPI + error-registry 镜像
├── scripts/
│   ├── activate.sh · check_harness.py
│   ├── run_codegen_api.py           # codegen:api（类型）
│   ├── form/                        # form:generate（S7 · 表单）
│   └── create-module.mjs
└── src/
    ├── api/          # 四层：generated → request → functions → query
    ├── components/   # 全局 UI · forms · charts · skeletons
    ├── config/ · layout/ · router/ · store/
    ├── i18n/         # zh-CN + en-US · useT
    ├── rbac/         # 路由级权限 · usePermissions 预留
    ├── pages/        # 业务（示例 studio-*）
    ├── mocks/ · styles/ · test/
```

### 一级 sector（增删须用户确认）

`api` · `components` · `config` · `i18n` · `layout` · `mocks` · `pages` · `rbac` · `router` · `store` · `styles` · `test`

---

## 五、治理策略（锁死）

| 层 | 机制 |
|----|------|
| L0 本地 | `pnpm check`（codegen → tsc → eslint → vitest → build → size → e2e → storybook） |
| L1 DevKit | `scripts/check_harness.py`（registry · contracts · 7 标签 · export JSDoc · 层界 · i18n/rbac） |
| L2 Umbrella | `./scripts/harness` 调度 Profile |
| 目录 | D15 `directory-readmes.yaml` |
| 模板 | `check_frontend_template_parity.py` |

### ESLint sector 矩阵（摘要）

- `pages/**` 禁止 fetch · 直引 `api/functions` · `@tanstack/react-query` · `i18next`
- `components/**` 禁止 pages · query hooks
- `api/functions` 禁止 pages/store/components/query

---

## 六、技术策略（锁死）

| 类别 | 选型 |
|------|------|
| 框架 | React 18 + TS + Vite 5 |
| UI | MUI 6 + Tailwind v4 |
| 路由 | react-router-dom 6 数据路由 · lazy · loader/prefetch |
| 数据 | TanStack Query 5 · Zustand（UI 态） |
| 表单 | RHF + Zod · `scripts/form/`（生成轨） |
| 契约 | `codegen:api` + vendor 镜像 + error-registry |
| i18n | i18next · namespace = module-id |
| RBAC | 路由 `permissions` + `RbacGuard` |
| 性能 S4 | 首屏壳 · skeleton · vendor-react 预算 · resource_chain |
| 测试 | Vitest + RTL · Playwright · Storybook |

**明确不做**：SSR（B 端 CSR 足够）。

---

## 七、变更纪律（必读）

1. **结构/治理/技术策略** 变更 → **须用户书面确认** → 改金样 `web-admin` → 验收盘绿 → `sync_frontend_template.py` → `check_frontend_template_parity.py` → bump `frontend-devkit-lock.yaml` version。
2. **仅业务实现**（pages 内容、文案、OpenAPI 增量）→ 可在金样/App 内直接开发，不改 sector 列表。
3. **禁止** 手改 `templates/frontend-devkit/` 绕过金样（`TEMPLATE.md` · `template.manifest.yaml` 除外）。

### 维护者刷新模板

```bash
cd src/apps/web-admin && ./scripts/activate.sh    # 金样须绿
uv run python scripts/devkit/sync_frontend_template.py
uv run python scripts/devkit/check_frontend_template_parity.py
# 人工更新 template.manifest.yaml + frontend-devkit-lock.yaml version
```

---

## 八、日常速查

```bash
pnpm dev
VITE_MSW=1 pnpm dev              # 无后端
VITE_MSW=0 pnpm dev              # 联调
pnpm create:module
pnpm codegen:api && pnpm codegen:check
pnpm check
./scripts/activate.sh
```

---

## 九、真源索引

| 文档 | 路径 |
|------|------|
| 架构 | `./ARCHITECTURE.md` |
| 工程策略 | `./ENGINEERING.md` |
| 版本锁 | `../../../contracts/frontend-devkit-lock.yaml` |
| 脚手架 | `../../../scripts/devkit/scaffold_frontend_app.py` |
| Parity 门禁 | `../../../scripts/devkit/check_frontend_template_parity.py` |

---

**结论**：本模板 = **web-admin 可复刻克隆体 + D16 版本锁**。新建前端 = 同等权重基座；业务在注册制上生长。
