# 验收用例 WEB-PROFILE：web-admin 前端工程自治

| 版本 | v1.0.0 |
|------|--------|
| 范围 | `src/apps/web-admin/**` **纯前端工程**（结构 · 治理 · 测试 · 构建） |
| 通过标准 | P0 全绿 · `cd src/apps/web-admin && ./scripts/activate.sh` |
| 关联 | [ARCHITECTURE.md](../../src/apps/web-admin/ARCHITECTURE.md) · [ENGINEERING.md](../../src/apps/web-admin/ENGINEERING.md) |

**钉死**：本 AC **与** [STU-001](./验收用例-STU-001-Studio配置主路径.md) **无对账关系**。STU 验后端 + 联调；WEB-PROFILE 验前端自治。二者 **仅** 在联调阶段由人串联，**禁止** 写进同一 Step / 同一 gate 关键字。

---

## 〇、自治断言（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| W-00 | 独立验收盘 | `./scripts/activate.sh`（无 API · 无 pytest） | `pnpm check` + `check_harness.py` 全绿 |
| W-00b | Profile 真源 | 读 `devkit.profile.yaml` | `ac_scope: WEB-PROFILE`；**非** STU-001 |
| W-00c | 规则不冗余 | 前端细则 | 仅 `ENGINEERING.md` + App harness；**不** 依赖根 `gate pr` 作日常验收盘 |

---

## 一、v1.7 基座（P0 · 原 WEB-S1）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| W-01 | 契约镜像 codegen | `pnpm codegen:check` · harness `openapi_codegen_fresh` | `api/generated/` 与 **pinned** OpenAPI 镜像同步；禁止手改 generated |
| W-02 | Query 基座 | bootstrap `QueryClientProvider` · 示例 hook | pages 经 hooks 取数；**数据来自 MSW/mock**，非 live API |
| W-03 | Query 层界 | ESLint + `query_layer_boundary` | pages 禁 `@/api/functions` · 禁直引 `@tanstack/react-query` |
| W-04 | MSW + RTL | vitest jsdom · router 冒烟 | ≥1 RTL 绿；handler 与 `api/functions` 对齐 |
| W-05 | 文档与 profile | ARCHITECTURE · ENGINEERING · devkit.profile | checks 登记；`pnpm check` 全绿 |

---

## 二、v1.8+（P0 · 纯前端架构）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| W-06 | Playwright 壳层 | `pnpm e2e` · `e2e/shell.spec.ts` | 路由 redirect · layout nav · MSW 数据展示 |
| W-07 | size-limit | `pnpm build` + `pnpm size:check` | vendor chunk ≤ profile 上限 |
| W-08 | Storybook | `.storybook/` + `pnpm storybook:build` | ≥1 stories · Theme decorator |
| W-09 | 表单基座 | `components/forms` · `ApiErrorBanner` · vitest | RHF+Zod · 错误展示 |
| W-10 | eslint sector 矩阵 | `eslint.config.js` sector rules | pages/api/components/request 边界 |
| W-11 | Standalone S | 迁出仓 `activate.sh` 零父仓全绿 | 待 |

---

## 三、Harness 参考

```bash
cd src/apps/web-admin && pnpm check && python scripts/check_harness.py
```

> 废止：`./scripts/gate step -k 'STU-09'` 作为 web-admin 基座验收盘。
