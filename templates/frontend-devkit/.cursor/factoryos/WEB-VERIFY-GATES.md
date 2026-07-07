# WEB · Verify 纪律

> **新对话**执行；只写 `verify/`；不重写业务码。

## 激活

`【WebVerify回合】Step N`（在 Test·Step N 之后）

## 落盘

`_web_pipeline/<date>/verify/verify-<HHmm>-stepN.md`

## 核对清单

1. plan Step N 范围 = git diff 范围
2. 追踪链：contracts ↔ registry ↔ i18n ↔ rbac
3. 边界：`check_boundary_lock.py` 绿
4. harness：`check_harness.py` 绿
5. 测试：Test 报告与命令可复现
6. 无未授权结构变更
7. 无 FactoryOS 越权路径

## 输出

| 项 | 内容 |
|----|------|
| 结论 | PASS / FAIL |
| 风险 | 无 / 须用户确认 |
| 下一步 | `可以继续` Step N+1 / 回 Dev 修 |

## 禁止

Verify 改业务 · 跳过 boundary 检查 · 替用户发「可以继续」
