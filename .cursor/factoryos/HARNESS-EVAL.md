# Harness Eval · 黄金题（L4 · P0）

> 冻结 **10** 道题：改 rules / hook / 门禁脚本后必须全绿，否则视为治理回退。  
> 真源：`scripts/harness_eval_lib.py` · CLI：`scripts/check_harness_eval.py`

## 命令

```bash
./scripts/gate harness-eval
python scripts/check_harness_eval.py --list
python scripts/check_harness_eval.py --case HE-07
./scripts/gate harness-gc              # 熵清理（可加 --strict）
```

## 题目一览

| ID | 期望 | 税则 | 题意 |
|----|------|------|------|
| HE-01 | 应失败 | FT-PLAN-STRUCTURE | plan 缺 Step 总览 |
| HE-02 | 应通过 | FT-PLAN-STRUCTURE | 最小合法 plan v2 |
| HE-03 | 应失败 | FT-MATERIALS-MISSING | 新功能材料 N/A |
| HE-04 | 应通过 | FT-MATERIALS-MISSING | 新功能 + materials 文件 |
| HE-05 | 应失败 | FT-PLAN-UI | UI「待实现」 |
| HE-06 | 应失败 | FT-STEP-STOP-UI | step-stop 缺 UI 对账 |
| HE-07 | 应失败 | FT-RUNTIME-EVIDENCE | step-stop 缺运行时证据 |
| HE-08 | 应失败 | FT-VERIFY-BLOCK | Verify 结论阻断 |
| HE-09 | 应失败 | FT-STAMP-CHAIN | 新功能 materials mode=na |
| HE-10 | 应通过 | FT-TAXONOMY | 税则表完整 |

## 何时必跑

| 时机 | 要求 |
|------|------|
| 改 `plan_gate_lib` / `check_plan_spec` / `step_chain_lib` / hooks | **必须** `gate harness-eval` |
| 改 STEP0 / plan-template / GATES 门禁语义 | **必须** |
| 日常业务 Step | 不强制（业务仍用 `gate step`） |
| CI / 可选 | 可挂 `gate pr` 旁路或独立 job |

## 关联

- [FAILURE-TAXONOMY.md](./FAILURE-TAXONOMY.md)
- [HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md)
- PostToolUse：`.cursor/hooks/post-edit-sensor.py`
