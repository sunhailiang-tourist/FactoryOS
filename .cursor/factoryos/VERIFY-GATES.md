# Verify 回合 · 独立审阅门禁（T4.5+）

> 对标顶尖 SDD：**implement 与 verify 上下文隔离**。  
> 模板：[templates/verify-template.md](./templates/verify-template.md)

## 何时做

每 **Step**，在 **Test 单步验收落盘之后**、`gate step` 之前：

1. 确认 `test-*-stepN-regression.md` 已落盘且 Test 结论非阻断
2. **新开 Cursor 会话**（或 Task 子 Agent，`readonly: true`）
3. 粘贴口令：`【Verify回合】Step N · 只读审阅`
4. 只读 plan + git diff + step-stop + Test 单步验收 + contracts
5. 落盘 `verify/verify-<HHmm>-stepN.md`
6. 由 Dev/你运行 `./scripts/gate step --step N`（内含 verify 机械检查）

**禁止在 Test 单步验收之前做 Verify。**

## 结论规则

| 结论 | 处置 |
|------|------|
| **通过** | 可进入 `gate step` |
| **需改进** | Dev 修补后重新 Verify；或你 `风险接受并继续` |
| **阻断** | 禁止 `可以继续`；须 `测试不通过` 或修复 |

## gate 机械检查

```bash
./scripts/gate verify --step 1
# 或停机一并：
./scripts/gate step --step 1 -k '<AC-ID>'
```

`check_verify.py` 校验文件存在且含「结论：通过/需改进/阻断」。

## 与 Test Agent 区别

| | Verify | Test（每 Step） |
|---|--------|-----------------|
| 时机 | Test 验收 **之后** | Dev step-stop **之后** |
| 焦点 | 范围/红线/可维护/不超 plan | **行为正确性 + git diff 落位 + pytest** |
| 写代码 | 否 | 仅 `src/tests/**` |
| 输出 | verify 落盘 | test-step-regression 落盘 + pytest 证据 |

二者互补，**不可替代**。
