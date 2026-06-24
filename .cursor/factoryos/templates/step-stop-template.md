# Step 停机：<Step N — 名称>

- **plan**：`_factoryos_pipeline/<date>/plan/plan-*.md`
- **时间**：YYYY-MM-DD HH:mm

## 1. Step 标识

Step N — <流程节点名>

## 2. 改动文件

| 路径 | 变更 |
|------|------|

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | |
| 2 | 响应契约 | |
| 3 | 鉴权/租户 | |
| 4 | 红线 | |
| 5 | Schema | |
| 6 | 输入校验 | |
| 7 | Shadow | |
| 8 | 幂等/补偿 | |
| 9 | 静态检查 | |
| 10 | 注释 | |

## 5. Harness 结果

```bash
./scripts/gate step --step N -k '<AC-ID>'
```

```text
gate step : PASS/FAIL
```

## 6. 最短验证路径

（你如何用一句话复测）

## 7. Verify（必填）

- 落盘：`verify/verify-<HHmm>-stepN.md`
- 结论：通过 / 需改进 / 阻断
- 口令：`【Verify回合】Step N`

## 8. 等待

请回复：`可以继续` 或 `测试不通过` + 现象
