# Harness 回灌 PR 草稿

> 同一 `FT-*` 连续出现 ≥2 次，或单次造成 stamp/契约回退时填写。  
> 生成辅助：`python scripts/check_failure_taxonomy.py --codes FT-…`

## 元信息

| 项 | 内容 |
|----|------|
| 税则码 | FT- |
| 触发来源 | Test / Verify / gate / sensor / harness-eval |
| 证据路径 | `_factoryos_pipeline/…` 或日志摘录 |
| 拟回灌面 | 规则 / 模板 / 脚本 / contracts |

## 问题（一句话）

（Agent 反复踩的坑是什么）

## 根因（Harness 层，不是业务层）

（缺哪条机械检查 / 文案不够 LLM 可执行 / stamp 可绕过）

## 回灌改动清单

| 路径 | 改什么 |
|------|--------|
| | |

## 验收

```bash
./scripts/gate harness-eval
python scripts/check_failure_taxonomy.py --validate
# 若动了 step-stop 合同：
# 补一条 HE 或扩展现有 HE
```

## 非目标

- 不在本 PR 修业务功能（业务另开 Step）
- 不放宽 stamp / 不手写 `.gates/*`
