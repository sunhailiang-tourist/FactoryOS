# WEB Harness Eval（WHE-01～10）

> 冻结 10 道题：改 WEB 门禁/规则后必须全绿。  
> CLI：`./scripts/web_gate harness-eval` · `python scripts/web_check_harness_eval.py`

| ID | 期望 | 税则 | 题意 |
|----|------|------|------|
| WHE-01 | 应失败 | WFT-PLAN-STRUCTURE | 缺 Step 总览 |
| WHE-02 | 应通过 | WFT-PLAN-STRUCTURE | 最小合法 plan |
| WHE-03 | 应失败 | WFT-MATERIALS-MISSING | 新功能材料 N/A |
| WHE-04 | 应通过 | WFT-MATERIALS-MISSING | 新功能+materials |
| WHE-05 | 应失败 | WFT-PLAN-UI | UI 待实现 |
| WHE-06 | 应失败 | WFT-RUNTIME-EVIDENCE | step-stop 缺自检 |
| WHE-07 | 应失败 | WFT-RUNTIME-EVIDENCE | 缺运行时证据 |
| WHE-08 | 应失败 | WFT-VERIFY-BLOCK | Verify 阻断 |
| WHE-09 | 应失败 | WFT-STAMP-CHAIN | 新功能 materials na |
| WHE-10 | 应通过 | WFT-TAXONOMY | 税则完整 |
