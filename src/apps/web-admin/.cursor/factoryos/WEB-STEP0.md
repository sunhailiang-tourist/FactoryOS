# WEB · Step 0（开工前理解）

> 输出 ≤8 行摘要 + 核对清单；全过 → 等用户 `可以继续`。

## 0-A · 模块与写路径

| 检查 | 通过标准 |
|------|----------|
| 工作根 | 仅 `src/apps/web-admin/`（迁出后为 App 根） |
| 目标模块 | `pages/{module-id}/` 或 sector 子路径明确 |
| 写路径 | 符合 ARCHITECTURE §注册制；不触达 FactoryOS 后端 |
| 边界 | 无越权路径（见 WEB-00） |

## 0-B · 契约与 AC

| 检查 | 通过标准 |
|------|----------|
| 追踪链 | `pages/{id}/contracts/README.md` 与 router/i18n/rbac 一致 |
| AC 范围 | **WEB-PROFILE**（W-xx）；非 STU/pytest |
| OpenAPI | 若涉 API → 只读 `api/generated` + codegen 轨 |
| 结构变更 | 若涉 sector/技术栈 → 标记「须确认结构变更」 |

## 0-C · 托管环境（在 FactoryOS 内时）

| 检查 | 通过标准 |
|------|----------|
| 验收盘 | `./scripts/activate.sh` · 非 umbrella pytest |
| 流水线目录 | `_web_pipeline/<date>/` |
| 禁止 | 改 `frontend-devkit-lock` · 手改 `templates/` |

## 输出模板

```text
Step0 摘要：
- 目标：<module-id / 任务>
- 写路径：<paths>
- AC：<W-xx IDs>
- 边界：无越权 / 须确认越权（说明）
- 结构：无变更 / 须确认结构变更（说明）
缺口：无 / A类…
→ 请回复「可以继续」进入规划
```
