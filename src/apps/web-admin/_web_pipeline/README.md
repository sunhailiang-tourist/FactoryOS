# _web_pipeline

## 是什么

web-admin（及 frontend-devkit 脚手架）的 **WEB 独立研发落盘目录**：plan / test / step-stop / verify / summary，以及 `.gates` 四重 stamp。与仓库根 `_factoryos_pipeline` **刻意切割**，迁出 monorepo 后仍可用。

## 子路径

| 路径 | 用途 |
|------|------|
| `plan/` | `materials-*.md` · `plan-*.md` |
| `test/` | 单步/终轮 Test 验收落盘 |
| `step-stop/` | Dev 停机（须含运行时证据） |
| `verify/` | WebVerify 落盘 |
| `summary/` | 变更摘要 |
| `.gates/` | `materials.ok` / `plan.ok` / `test.ok` / `code.ok`（仅 `./scripts/web_gate` 可写） |
| `workflow_state.md` | WEB 工作流状态机 |
| `README.md` | 本说明 |

## 门禁

```bash
./scripts/web_gate materials|plan|test|start|step
./scripts/web_gate harness-eval
./scripts/web_gate harness-gc
```

根 Hook：伪造 `.gates/*` 拒绝；无 `materials.ok` 禁止写 `plan/plan-*.md`；无 `code.ok` 禁止写 App `src/**` 业务。

## 变更纪律

- 新增/废止本目录或改 stamp 语义 → 用户确认结构变更 → 更新 `contracts/directory-readmes.yaml` → `gate pr`
- **禁止**把 WEB 落盘改写到 `_factoryos_pipeline/`
- 模板同步：金样 web-admin → `sync_frontend_template.py`

## 相关文档

- `.cursor/INDEX.md` · `.cursor/factoryos/WEB-GATES.md` · `WEB-HARNESS-EVAL.md`
- `.cursor/factoryos/WEB-步步流.md`
- 仓库结构门禁：`.cursor/rules/项目结构变更门禁.mdc`
