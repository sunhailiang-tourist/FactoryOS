# WEB · Dev Gate 1–4（含 L4 stamp）

> plan 为唯一执行清单；未 `确认规划`+`web_gate plan` 禁止 `可以开始` 写 `src/**`。  
> 真源 stamp：[WEB-GATES.md](./WEB-GATES.md)

## 关键词

| 词 | 解锁 |
|----|------|
| `材料已齐` | `./scripts/web_gate materials` |
| `可以继续` | Step0 通过 |
| `确认规划` | plan + `./scripts/web_gate plan` |
| `可以开始` | `./scripts/web_gate start --step N` |
| `确认结构变更` / `确认越权` | 架构 / 边界 |
| `测试不通过` | 回当前 Step |

## Gate 1–3 · 规划

落盘：`_web_pipeline/<date>/plan/plan-<HHmm>-<slug>.md`（模板 v2）

必填：

1. **类型** + **材料准入**
2. WEB-PROFILE AC 对账
3. 红线对账
4. **§4 Step 总览** + **### Step N**（路径 · 验收盘）
5. 边界/结构声明
6. UI 命中判定（是则禁「待实现」）

然后：`./scripts/web_gate plan --plan …`

## Gate 4 · 开始 Step N

1. `web_gate test` 已绿（test.ok）
2. failing tests 已落盘
3. `./scripts/web_gate start --step N`

## 每 Step

1. 仅本 Step；10 项自检  
2. step-stop **含运行时证据**  
3. WebTest → WebVerify → `./scripts/web_gate step --step N`

## 交付

`activate.sh` 全绿 · 改门禁后 `web_gate harness-eval` · 用户 `可以提交`
