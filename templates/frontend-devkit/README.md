# src/apps/web-admin · PC 管理端

## 前端自治（钉死）

> **开发者全流程手册**（拉代码 → 激活 → 日常开发 → 模板）：[contracts/README.md § 前端工程全流程](../../contracts/README.md#前端工程全流程开发者手册)

| 原则 | 说明 |
|------|------|
| **独立自治** | 完整前端工程；monorepo 内 **托管**，迁出 **standalone** 后质量不变 |
| **零后端依赖** | 日常验收盘 **不** 需要 API 进程 · **不** 以 STU pytest 为前端 Gate |
| **规则真源** | [ENGINEERING.md](./ENGINEERING.md) · [devkit.profile.yaml](./devkit.profile.yaml) · `scripts/check_harness.py` |
| **唯一激活** | `./scripts/activate.sh` → `pnpm check` + profile harness |

**工程 AC**：[WEB-PROFILE](../../contracts/acceptance/验收用例-WEB-PROFILE-前端工程自治.md)（W-00～W-11）

与后端 **唯一关联**：**联调轨**（业务 pages 接 REST）— 属 STU/集成 plan，**不** 定义本应用架构。

---

## 是什么

**React 18 + TypeScript + Vite + MUI + Tailwind v4** 管理平台壳层：module-id 注册制 · 四层 API 客户端 · MSW 本地开发。

## 架构真源

**[ARCHITECTURE.md](./ARCHITECTURE.md)** — 结构 · 治理 · 演进（**纯前端**）。  
**[ENGINEERING.md](./ENGINEERING.md)** — ESLint · Vitest · harness · `pnpm check`。

---

## DevKit 托管与一键激活

### 当前（FactoryOS 内）

```bash
cd src/apps/web-admin
./scripts/activate.sh
```

Umbrella 下 pipeline 落盘可用 FactoryOS 根 `_factoryos_pipeline/`，但 **验收盘仍在 App 内**。

### 迁出为独立仓（standalone）

```bash
cp devkit.manifest.standalone.yaml devkit.manifest.yaml
./scripts/activate.sh
```

**必选**：`vendor/factoryos-contracts/`（OpenAPI · schemas · error-registry · pin）— 迁出后 **零父仓** 契约与错误码自给。

迁出前自测：`pnpm test:w11`

### Standalone 维护 SOP（契约 / 错误码）

| 场景 | 命令 |
|------|------|
| 刷新 vendor 镜像（仅 monorepo 内） | `./scripts/sync_vendor_contracts.sh` |
| OpenAPI codegen | `pnpm codegen:api`（读 vendor 或 umbrella，双路径） |
| 校验 generated 新鲜 | `pnpm codegen:check` |
| 错误码 drift 检查 | `pnpm codegen:registry:check` |
| 错误码同步写盘 | `python scripts/sync_error_registry.py --apply` |
| 零父仓模拟 | `bash scripts/simulate_standalone_activate.sh` |

---

## 本地开发

```bash
cd src/apps/web-admin
pnpm install
pnpm dev          # 可选 VITE_MSW=1
```

## 新建模块

```bash
pnpm create:module
```

## 相关文档

- [TEMPLATE.md](../../templates/frontend-devkit/TEMPLATE.md) — 迁出 / 新 App 脚手架说明
- [DEVKIT.md](../../../.cursor/factoryos/DEVKIT.md) — 伞形 DevKit（迁出后见 `devkit/kernel/`）

## 子路径

| 路径 | 说明 |
|------|------|
| `devkit/` | standalone AI 内核快照 |
| `vendor/` | 契约镜像（迁出必选） |
| `scripts/` | activate · harness · codegen |
| `e2e/` | Playwright 壳层 E2E |
| `.storybook/` | Storybook 配置 |
| `src/` | 前端源码根（各 sector README） |

## 门禁

```bash
./scripts/activate.sh
pnpm check
pnpm test:w11
```

## 变更纪律

- 新增根目录文件夹须 **用户确认** + `contracts/directory-readmes.yaml` + 目录 README
- 架构锁死后结构变更同步 `repo-structure.yaml` · PATH-SNAPSHOT · `gate pr`

## 相关文档

- [ARCHITECTURE.md](./ARCHITECTURE.md) · [ENGINEERING.md](./ENGINEERING.md)
- [contracts/directory-readmes.yaml](../../../contracts/directory-readmes.yaml)

## AI 工作流（独立 · 可迁出）

| 项 | 路径 |
|----|------|
| 入口 | [`.cursor/INDEX.md`](./.cursor/INDEX.md) |
| Dev 口令 | `【WebDev模式启动】` |
| 绝对门禁 | `WEB-00` 独立边界 · `WEB-01` 架构锁 |
| 落盘 | `_web_pipeline/<date>/` |
| 边界校验 | `python scripts/check_boundary_lock.py` |

**迁出**：复制 `.cursor/` + `contracts/WEB-ARCHITECTURE-LOCK.yaml` 到新仓库即可。

