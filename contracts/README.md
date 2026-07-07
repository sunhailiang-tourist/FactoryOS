# contracts · 契约平面与工程真源索引

> **契约镜像状态**：Export / CI 镜像 · **非**运行时日常编辑真源（ADR-008）  
> **真源**：[ADR-008](../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md) · PostgreSQL `contract_*` Registry + Studio publish

---

## 快速导航

| 我是谁 | 从这里开始 |
|--------|------------|
| **前端开发者**（web-admin / 新建 App） | [§ 前端工程全流程](#前端工程全流程开发者手册) |
| **后端 / 契约编辑** | [§ 契约镜像目录](#契约镜像目录) · Registry publish |
| **维护模板 / 金样** | [§ 模板与版本锁](#模板与版本锁维护者) · `frontend-devkit-lock.yaml` |
| **AI Agent（Dev/Test）** | [INDEX.md](../.cursor/factoryos/INDEX.md) · `【Dev模式启动】` |

---

## 契约镜像目录

本目录保留 **export/import 快照** 与 **gate/contract pytest 对账镜像**；日常契约变更经 Studio publish 写入 Registry，再 export 回本目录（CI 可选）。

| 路径 | 内容 |
|------|------|
| `openapi/` | FactoryOS Platform API v1.1.1 |
| `repo-structure.yaml` | **仓库结构快照**（路径真源 · harness 对账） |
| `frontend-devkit-lock.yaml` | **前端模板版本锁**（金样 ↔ 模板 parity · D16） |
| `directory-readmes.yaml` | 登记目录 README 门禁（D15） |
| `schemas/` | 16 份 JSON Schema |
| `cmv/` | CMV 注册表 + 同步规则 |
| `acceptance/` | AC-BASE / MVP / UX / WEB-PROFILE 验收用例 |
| `fixtures/business-graphs/` | Graph/RuleSet 草稿 JSON |

### 契约门禁

```bash
./scripts/harness --tier contracts    # L0
./scripts/gate plan
./scripts/gate pr
```

### 契约变更纪律

| 改了 | 必做 |
|------|------|
| **`repo-structure.yaml`** | `gen_path_snapshot.py` · 一致性矩阵 · `gate pr` |
| **新增登记目录** | 用户确认 → `directory-readmes.yaml` · 目录 `README.md` |
| Registry publish 后 export | `harness --tier contracts` + contract pytest |
| `acceptance/` | 更新 `src/tests/ac/` · AC-P0-INDEX |

**禁止**：将本目录作为实施顾问日常编辑入口（契约内容走 Registry）。

---

# 前端工程全流程（开发者手册）

> **版本锁**：`frontend-devkit-lock.yaml` · **2.0.0-s5**  
> **金样 App**：`src/apps/web-admin` · **模板**：`templates/frontend-devkit`  
> **目标**：从拉代码到写业务，全程有文档、有命令、有红灯提示，不靠口口相传。

---

## 0. 先确认你在哪条路径

```text
┌─ 路径 A：开发/维护金样 web-admin（Integration Studio）
│     cd src/apps/web-admin
│
└─ 路径 B：新建一个与 web-admin 等权的前端 App
      ./scripts/scaffold_frontend_app.sh <app-id>
      cd src/apps/<app-id>
```

两条路径 **工程机制相同**（注册制 · harness · activate）；仅业务模块与标识不同。

---

## 1. 获取代码

```bash
git clone <FactoryOS-repo-url>
cd FactoryOS
```

| 感知点 | 说明 |
|--------|------|
| 仓库根 `devkit.manifest.yaml` | 登记所有前端 Profile（含 web-admin） |
| `contracts/frontend-devkit-lock.yaml` | 前端架构版本锁；**结构变更看这里** |
| `templates/frontend-devkit/` | 一键 scaffold 用的模板（**勿手改**，从金样 sync） |

---

## 2. 环境准备（一次性）

| 依赖 | 用途 | 检查 |
|------|------|------|
| **Node 20+** | 前端构建 | `node -v` |
| **pnpm** | 包管理 | `pnpm -v` |
| **Python 3.11+** | harness / codegen 脚本 | `python3 -V` |
| **uv**（推荐） | 根脚本运行 | `uv --version` |

```bash
# 可选：Playwright 浏览器（e2e 首次会装）
cd src/apps/web-admin && pnpm install
```

---

## 3. 初始化与激活（必做 · 验收盘）

```bash
cd src/apps/web-admin          # 或 src/apps/<your-app-id>
./scripts/activate.sh
```

### `activate.sh` 会做什么（实时感知）

| 步骤 | 终端输出 | 含义 |
|------|----------|------|
| `pnpm install` | 装依赖 | 首次较慢，正常 |
| `pnpm check` | 全链自检 | codegen → tsc → eslint → vitest → build → e2e → storybook |
| `check_harness.py` | 工程门禁 | registry · contracts · 文件头 · i18n/rbac · 层界 |
| 结尾横幅 | DevKit 已激活 | 打印 AI 口令与落盘路径 |

**全绿 = 可以开发。** 任一步红 = **停**，按下方 [§ 红灯怎么办](#红灯怎么办) 处理，不要硬写业务代码。

### 初始化后读这三份（15 分钟）

| 顺序 | 文档 | 解决什么 |
|------|------|----------|
| 1 | `ARCHITECTURE.md` | 结构地图 · 业务数据流 · sector 注册制 |
| 2 | `ENGINEERING.md` | 门禁分层 · ESLint 层界 · 日常命令 |
| 3 | `src/pages/<module>/contracts/README.md` | 单模块追踪链范例（studio-shell） |

---

## 4. 日常开发循环（推荐节奏）

```text
  改代码
    ↓
  pnpm dev                    # 本地看效果（默认 MSW 可开）
    ↓
  pnpm lint / vitest          # 快反馈
    ↓
  python scripts/check_harness.py   # 工程规则
    ↓
  提交前 pnpm check           # 全链（与 CI 同）
```

### 本地开发命令

```bash
pnpm dev                      # http://localhost:5173
VITE_MSW=1 pnpm dev           # 无后端 · MSW 拦截 API（默认开发推荐）
VITE_MSW=0 pnpm dev           # 联调 · 打真实 API
```

### 实时感知地图（开发时你会遇到）

| 时机 | 谁提示你 | 提示什么 |
|------|----------|----------|
| 启动 dev | Vite 终端 | 编译错误 · 端口 |
| 保存文件 | ESLint（IDE / `pnpm lint`） | pages 禁止 fetch · 禁止直引 query/i18next |
| 跑测试 | Vitest | 组件/路由 smoke 失败位置 |
| 跑 harness | `check_harness.py` | **缺 contracts** · 追踪链不一致 · 缺 i18n JSON |
| 跑 check | `pnpm check` | e2e / bundle 超限 |
| 新建目录 | harness D15 | 未登记目录 → 须补 `directory-readmes.yaml` |
| Cursor AI | `【Dev模式启动】` | 步步流 · 落盘 `_factoryos_pipeline/` |

---

## 5. 业务流 → 代码放哪（注册制 · 必背）

```text
角色 role
  → rbac/modules/{domain}/registry.ts
  → router/modules/{module-id}/registry.ts   # permissions + lazy 路由
  → layout/modules/{domain}/                   # 壳（侧栏/Outlet）
  → pages/{module-id}/*.lazy.tsx               # 业务 UI
  → api/query/hooks/useXxx.ts                  # 页面唯一数据入口
  → api/functions/{module-id}/*.fn.ts
  → api/request/client.ts
  → api/generated/openapi.d.ts  ← vendor 或 umbrella OpenAPI
  → i18n/modules/{module-id}/zh-CN.json · en-US.json
  → mocks/handlers/{module-id}.ts
```

**铁律**：`pages/**` 禁止 `fetch`、禁止直引 `@tanstack/react-query`、禁止直引 `i18next`（用 `useT`）。

### 新增业务模块（一条命令）

```bash
pnpm create:module
# 交互输入 domain / step / step label → 自动切片：
#   router（含 permissions）· pages · store · api · mocks
#   i18n/modules/{id}/zh-CN.json · en-US.json + i18n/registry.ts 登记
#   rbac/modules/{domain}/registry.ts（新 domain 时联动 rbac/registry.ts）
#   router/i18n/rbac contracts 登记索引行
#   pages/{id}/contracts/README.md 追踪链（含 i18n namespace · rbac permission）
# 然后补全业务实现 → pnpm check && python scripts/check_harness.py
```

---

## 6. 契约与 codegen（与后端对齐时）

| 任务 | 命令 | 说明 |
|------|------|------|
| 刷新 OpenAPI 类型 | `pnpm codegen:api` | 写 `api/generated/` · **禁止手改** |
| 确认无 drift | `pnpm codegen:check` | 提交前必跑 |
| 错误码同步 | `pnpm codegen:registry:check` | vendor `error-registry.yaml` |
| 表单生成（S7） | `pnpm form:generate` | 读 `scripts/form/contracts/README.md` |

Monorepo 内刷新 vendor 镜像：`./scripts/sync_vendor_contracts.sh`（standalone 用 vendor 自给）。

---

## 7. 联调（后端就绪后）

```bash
# 1. 关 MSW
VITE_MSW=0 pnpm dev

# 2. 配置 API 基址（见 src/config/env.ts）

# 3. OpenAPI 有变更
pnpm codegen:api && pnpm codegen:check

# 4. 仍须工程轨全绿
./scripts/activate.sh
```

联调失败先看 **网络/鉴权**；工程轨（harness/eslint）与 API 是否通 **分开查**。

---

## 8. 一键用模板创建新前端 App

```bash
# 在仓库根
./scripts/scaffold_frontend_app.sh order-console

cd src/apps/order-console
pnpm install
./scripts/activate.sh
```

| 步骤 | 说明 |
|------|------|
| scaffold | 复制 `templates/frontend-devkit` → `src/apps/<id>/`，替换标识 |
| 注册 | 写入根 `devkit.manifest.yaml` · `repo-structure.yaml` |
| 阅读 | `src/apps/<id>/TEMPLATE.md`（用法真源） |

**不要**从空目录手搭 Vite；**不要** copy web-admin 文件夹漏文件。

---

## 9. 模板与版本锁（维护者）

金样演进 SOP（**结构/治理变更须项目负责人书面确认**）：

```bash
cd src/apps/web-admin && ./scripts/activate.sh     # 1. 金样全绿
uv run python scripts/devkit/sync_frontend_template.py
uv run python scripts/devkit/check_frontend_template_parity.py
# 3. bump contracts/frontend-devkit-lock.yaml + templates/.../template.manifest.yaml
```

| 文件 | 作用 |
|------|------|
| `contracts/frontend-devkit-lock.yaml` | sector 列表 · harness · 变更纪律 |
| `scripts/devkit/check_frontend_template_parity.py` | 金样 ↔ 模板字节 parity |
| `templates/frontend-devkit/TEMPLATE.md` | scaffold 后开发者读本 |

---

## 10. 文档导航（不知道读啥时）

| 问题 | 去读 |
|------|------|
| 目录能放什么 | 各 sector 下 `README.md` · `contracts/README.md` |
| 路由怎么登记 | `src/router/contracts/README.md` |
| API 四层 | `src/api/README.md` · `ENGINEERING.md` §3a |
| i18n / RBAC | `src/i18n/contracts/README.md` · `src/rbac/contracts/README.md` |
| 性能策略 | `ENGINEERING.md` §10 S4 |
| WEB-PROFILE 验收 | `contracts/acceptance/验收用例-WEB-PROFILE-前端工程自治.md` |
| AI 研发流 | `.cursor/factoryos/INDEX.md` |

---

## AI 工作流（web-admin 独立 · 可迁出）

| 项 | 说明 |
|----|------|
| 入口 | `src/apps/web-admin/.cursor/INDEX.md` |
| Dev | `【WebDev模式启动】` |
| 绝对门禁 | WEB-00 独立边界 · WEB-01 架构锁 |
| 解锁词 | `确认越权` · `确认结构变更` |
| 落盘 | `_web_pipeline/<date>/`（**非** `_factoryos_pipeline/`） |
| 校验 | `python scripts/check_boundary_lock.py` |

**迁出**：复制 `web-admin/.cursor/` + `contracts/WEB-ARCHITECTURE-LOCK.yaml` 即可独立运行。

---

## 红灯怎么办

| harness / lint 报错关键词 | 处理 |
|---------------------------|------|
| `missing pages/.../contracts/README.md` | 补契约 · 对齐追踪链表 |
| `i18n namespace` / `missing i18n/modules` | 补 `zh-CN.json` + `en-US.json` |
| `rbac permission mismatch` | 对齐 `router/registry permissions` 与 rbac 子表 |
| `pages must not import` | 改走 `@/api/query/hooks` 或 `useT` |
| `file header missing` | 文件头补全 7 标签（见编码绝对门禁） |
| `parity drift` | 维护者跑 `sync_frontend_template.py` |
| `directory-readmes` | 新目录须用户确认后登记 yaml |

---

## 认知策略（全局）

- 工作流：[.cursor/factoryos/INDEX.md](../.cursor/factoryos/INDEX.md)
- UI-FIRST：[UI-FIRST-CONFIG-PRINCIPLE.md](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)
- 前端金样：[src/apps/web-admin/README.md](../src/apps/web-admin/README.md)
- ADR-008：配置与契约平面 DB 化

---

**前端开发者口诀**：`activate 绿了再写码` · `create:module 扩业务` · `contracts 对追踪链` · `pages 只走 hooks` · `结构变更看 lock 文件`。
