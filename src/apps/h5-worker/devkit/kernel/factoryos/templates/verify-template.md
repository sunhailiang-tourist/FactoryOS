# Verify 回合：<Step N — 名称>

> **必须在新会话 / 子 Agent 中只读完成**（禁止在同一实现会话自评）。  
> 落盘：`_factoryos_pipeline/<date>/verify/verify-<HHmm>-stepN.md`

- **plan**：`_factoryos_pipeline/<date>/plan/plan-*.md`
- **step-stop**：`_factoryos_pipeline/<date>/step-stop/step-stop-*-stepN.md`
- **对照 AC**：

## 1. 只读输入（Verify Agent 须阅读）

- [ ] plan 本 Step 段落
- [ ] `git diff` 本 Step 改动
- [ ] step-stop 十项自检
- [ ] `contracts/` 相关 AC / OpenAPI

## 2. 核对项（Pass/Fail）

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | | |
| 2 | 写路径 / R-01–R-11 | | |
| 3 | AC 断言可测 | | |
| 4 | 无重复逻辑迹象 | | |
| 5 | 注释四要素 | | |

## 3. 结论（必填 · gate 检查）

结论：通过 / 需改进 / 阻断

阻断理由（若有）：

## 4. 建议（3 条以内）

1.
2.
3.
