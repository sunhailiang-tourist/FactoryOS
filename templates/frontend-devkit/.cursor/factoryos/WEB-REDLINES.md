# WEB · 红线清单（锁死 v2.0.0-s5）

## R-WEB-01 独立域

- 验收盘 **仅** `./scripts/activate.sh`
- **禁止** STU Step / pytest 定义 WEB 业务

## R-WEB-02 边界

- **禁止** 写 `os_core` / `src/apps/api` / `src/tests`
- **禁止** 未 `确认越权` 改 FactoryOS 全局契约/模板

## R-WEB-03 结构

- **禁止** 增删 `src/` 一级 sector（12 个锁死）
- **禁止** 未 `确认结构变更` 改 lock/profile/ESLint 层界

## R-WEB-04 层界

- `pages/**` 禁止 fetch · 直引 RQ · 直引 i18next · 直引 `@/api/functions`
- `api/functions` 禁止 React

## R-WEB-05 注册制

- 禁止手改聚合 `registry.ts`（仅 glob）
- 新模块须 `create:module` + contracts 追踪链

## R-WEB-06 技术版图

- **禁止** SSR
- **禁止** 自动引入 plugins 轨（P2 延后）
- i18n 仅 zh-CN + en-US

## R-WEB-07 契约

- `api/generated` 仅 codegen
- OpenAPI SSOT 只读镜像

## R-WEB-08 AI 落盘

- 须 `_web_pipeline/` 落盘；禁止仅聊天宣称完成

## R-WEB-09 Test

- Test 禁止改业务实现

## R-WEB-10 宣称

- boundary + harness + `pnpm check` 未绿 **禁止** 宣称通过/可提交
