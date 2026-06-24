# Verify 回合 · 独立审阅门禁（T4.5+）

> 对标顶尖 SDD：**implement 与 verify 上下文隔离**。  
> 模板：[templates/verify-template.md](./templates/verify-template.md)

## 何时做

每 **Step 停机前**，在 Dev 写完 step-stop 之后、用户 `可以继续` 之前：

1. **新开 Cursor 会话**（或 Task 子 Agent，`readonly: true`）
2. 粘贴口令：`【Verify回合】Step N · 只读审阅`
3. 只读 plan + git diff + step-stop + contracts
4. 落盘 `verify/verify-<HHmm>-stepN.md`
5. 运行 `./scripts/gate verify --step N` 或 `./scripts/gate step --step N`

## 结论规则

| 结论 | 处置 |
|------|------|
| **通过** | 可进入 `gate step` |
| **需改进** | Dev 修补后重新 Verify |
| **阻断** | 禁止 `可以继续`；须 `测试不通过` 或修复 |

## gate 机械检查

```bash
./scripts/gate verify --step 1
```

`check_verify.py` 校验文件存在且含「结论：通过/需改进/阻断」。

## 与 Test Agent 区别

| | Verify | Test |
|---|--------|------|
| 时机 | 每 Step 后 | 跑测阶段 |
| 写代码 | 否 | 仅 `src/tests/**` |
| 输出 | verify 落盘 | test 报告 + pytest |
