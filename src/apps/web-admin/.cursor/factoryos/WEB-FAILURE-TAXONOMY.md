# WEB 失败税则（WFT-*）

> 代码真源：`scripts/web_failure_taxonomy_lib.py` · 本文件须登记全部码

| 码 | 摘要 |
|----|------|
| `WFT-MATERIALS-MISSING` | 材料准入缺失或新功能滥用 N/A |
| `WFT-STAMP-CHAIN` | WEB 四重 stamp 断裂 |
| `WFT-PLAN-STRUCTURE` | plan 缺 Step 总览/详表 |
| `WFT-PLAN-UI` | UI 对账非法状态 |
| `WFT-RUNTIME-EVIDENCE` | step-stop 缺运行时证据 |
| `WFT-TEST-FAIL` | Test 结论非通过或缺落盘 |
| `WFT-VERIFY-BLOCK` | Verify 阻断被当成通过 |
| `WFT-BOUNDARY` | 独立边界/架构锁失败 |
| `WFT-SENSOR-LINT` | WEB 传感器发现 TS/语法问题 |
| `WFT-TAXONOMY` | 税则表不完整 |
| `WFT-HARNESS-DRIFT` | WEB 文档死链/过期 draft |
| `WFT-CLAIM-GREEN` | 未绿宣称通过 |

同一码连续 ≥2 次 → 回灌 `.cursor/` 规则或 `scripts/web_*`，禁止只修业务。
