# WEB · Step 0（开工前理解）

> 输出 ≤8 行摘要 + 核对清单；全过 → 等用户 `可以继续`。  
> **新功能**：须先完成材料准入（见下）才可进入 0-A。

## 材料准入（新功能 · 先于 0-A）

1. 功能需求文案  
2. 需求资料 ≥1  
3. 追问「是否还有补充？」→ 有/无补充  
4. 用户 `材料已齐` → `./scripts/web_gate materials --materials …`  
   Bug/联调：`./scripts/web_gate materials --na --reason '…'`

模板：`templates/materials-intake-template.md`

## 0-A · 模块与写路径

| 检查 | 通过标准 |
|------|----------|
| 工作根 | 仅本 App（`src/apps/web-admin/` 或迁出后 App 根） |
| 目标模块 | `pages/{module-id}/` 明确 |
| 写路径 | 符合 ARCHITECTURE 注册制；不触达 FactoryOS 后端 |
| 边界 | 无越权（WEB-00） |

## 0-B · 契约与 AC

| 检查 | 通过标准 |
|------|----------|
| 追踪链 | contracts 与 router/i18n/rbac 一致 |
| AC | **WEB-PROFILE** W-xx |
| OpenAPI | 只读 generated + codegen 轨 |
| 结构 | 涉 sector → 须确认结构变更 |

## 0-C · 托管环境

| 检查 | 通过标准 |
|------|----------|
| 验收盘 | `./scripts/activate.sh` · `./scripts/web_gate` |
| 流水线 | `_web_pipeline/<date>/`（禁止 `_factoryos_pipeline`） |

## 输出模板

```text
Step0 摘要：
- 目标 / module-id
- 材料：已齐 path / na
- AC：W-xx
- 边界 / 结构
→ 「可以继续」进入规划
```
