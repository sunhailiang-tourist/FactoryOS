# WEB · Dev Gate 1–4

> plan 为**唯一执行清单**；未 `确认规划` 禁止 `可以开始` 写 `src/**`。

## 关键词

| 词 | 解锁 |
|----|------|
| `可以继续` | Step0 通过 |
| `确认规划` | plan 落盘 `_web_pipeline/<date>/plan/` |
| `可以开始` | 仅当前 Step N 编码 |
| `确认结构变更` | 解锁 sector/技术版图/lock |
| `确认越权` | 解锁跨 FactoryOS 边界写 |
| `测试不通过` | 回当前 Step |

## Gate 1–3 · 规划（一次确认）

落盘：`plan/plan-<HHmm>-<slug>.md`（模板 `templates/plan-template.md`）

必填：

1. 需求与 **WEB-PROFILE AC** 对账
2. **红线**（WEB-REDLINES.md）对账
3. Mermaid 数据流（router→pages→query→api）
4. Step 列表（每 Step 路径 + 验收盘命令）
5. **边界声明**：是否触达 FactoryOS 全局 / 是否结构变更

## Gate 4 · 开始 Step N 前

1. plan 已落盘
2. Test 已写/更新 **failing** tests（Vitest/RTL 或 E2E）
3. 输出 `确认项（≤3）`
4. 问：「是否 `可以开始` Step N？」

## 每 Step 实现纪律

1. **仅本 Step** 文件；git diff 复核 Step 1…N-1
2. **pages** 只经 `@/api/query/hooks` · `@/i18n/core/useT`
3. 新模块优先 `pnpm create:module`（含 i18n/rbac）
4. 中文文件头（读代码像读业务流程）
5. 停机：`step-stop/step-stop-<HHmm>-stepN.md`

## 10 项自检（停机 Pass/Fail）

1. 层界：pages 无 fetch/RQ/i18next 直引
2. 追踪链：contracts 与 registry 同步
3. i18n：namespace JSON 存在
4. rbac：router `permissions` 登记
5. query：hook 为页面唯一取数入口
6. MSW：新端点有 handler
7. 边界：无 FactoryOS 后端改动
8. 结构：无未授权 sector 变更
9. lint/tsc 无新增红
10. 无重复逻辑（≥2 处须抽取）

## 交付

全部 Step `可以继续` 后：

1. `summary/change-summary-<HHmm>.md`
2. `check_boundary_lock` + `check_harness` + `pnpm check` 全绿
3. 用户明确 `可以提交` 后才提示 git commit

## 禁止

跳 Step · 超 plan · 改 os_core · 改 templates/lock · Agent 自批越权
