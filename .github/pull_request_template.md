## Summary

- **plan**（必填）：`_factoryos_pipeline/<date>/plan/plan-<HHmm>-<slug>.md`
- **AC ID**（必填）：例如 `G-01` `E-03`（须出现在正文）
- **Harness**：本地 `./scripts/gate pr` 已绿

## Test plan

- test-plan：`_factoryos_pipeline/<date>/test/test-*.md`

## Verify（每 Step PR 或 Step 合并说明）

- verify 落盘路径（若适用）：

## Checklist

- [ ] `workflow_state.md` phase 与本轮一致
- [ ] `./scripts/gate pr` 本地通过
- [ ] plan 路径与 AC ID 已写入本 PR 描述（CI 强制）
- [ ] 业务 `.py` 变更含 `src/tests/` 更新
- [ ] 无 Test Agent 越权改动 `src/os_core` / `src/apps` 业务
- [ ] 若改 `docs/` Tier-A：`./scripts/docs_baseline refresh` + `workflow-check`
