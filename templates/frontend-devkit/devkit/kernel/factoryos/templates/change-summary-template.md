# PR 变更摘要：<标题>

## 标题建议（PR title）

## 变更背景（Why）

## 主要改动（What）

| 模块 | 文件 | 说明 |
|------|------|------|

## AC 通过情况

| AC ID | 结果 |
|-------|------|

## 业务口径确认（Behavior）

## 风险与兼容性

## 测试结论（Test）

- `./scripts/gate step --step N -k '...'` · `./scripts/gate delivery` · `./scripts/gate pr`：

## Summary（3 条，可贴 PR）

1.
2.
3.


## 注释门禁（须满足）

真源：`contracts/comment-gate-spec.md`

- 每个 `.ts/.tsx` 七标签文件头
- 每个 `export function` 含 JSDoc（功能/业务 + 上游/下游/怎么用）
- 复杂函数体 `//` 块注释 · `throw` 须写异常
