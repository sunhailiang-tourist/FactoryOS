# SH-步步流 · 工作流状态机

```yaml
phase: READY_FOR_W5_PLAN
agent: dev
step: 0
plan: _factoryos_pipeline/plan/plan-api-v6-full-structure.md
updated: 2026-06-26
goal: v6-full + ADR-008 真源统一 · W1~W4 全绿 · W5 开工前路径兜底
```

## W5 开工前路径兜底（2026-06-26 · 全量扫描）

> **扫描范围**：`docs/` · `.cursor/` · `scripts/` · `src/` · `_factoryos_pipeline/` — **6823** 文件递归 · **6466** 篇文本通读（非抽检）  
> **机械验收盘**：`check_structure_change`（提交门禁）· `audit_path_consistency` · `check_legacy_paths` · `harness --tier full` · `pytest not pending` 72 passed

### 路径真源（v6-full · AI Coding 须遵守）

> **结构快照写源**：[`contracts/repo-structure.yaml`](../contracts/repo-structure.yaml) → 自动生成 [`.cursor/factoryos/PATH-SNAPSHOT.md`](../.cursor/factoryos/PATH-SNAPSHOT.md)

| 类型 | 现行路径 | 废止 |
|------|----------|------|
| HTTP API | `src/server/api/` · import `server.api` | `src/apps/api/` · `routes/` · `deps.py` |
| 内核 | `src/server/os_core/` · import `os_core.*` | `src/os_core/` |
| 迁移（Alembic） | `src/server/db/migrations/` · `versions/` · 根目录 `alembic.ini`（`script_location` 指向前者） | 仓库内**无** `alembic/` 目录 · 勿引用 `alembic/versions/` |
| Edge | `src/server/edge-agent/` | `src/apps/edge-agent/` |
| 前端 | `src/apps/web-admin` · `src/apps/h5-worker` | — |
| GIP export | `src/integration/` | 作编辑真源（ADR-008） |
| 契约 export | `contracts/` | 作编辑真源（ADR-008） |
| Registry 运行时 | PostgreSQL + `/v1/registry/*` | Git YAML 日常编辑 |

**命名双轨（均合法）**：文档中 `os_core/<module>/` = Python 包逻辑路径；`src/server/os_core/<module>/` = 磁盘物理路径。

### 扫描结论

| 检查项 | 结果 |
|--------|------|
| 废止物理路径存在 | ✅ 0（`check_legacy_paths`） |
| `apps.api` / `src/apps/api` 残留（权威目录） | ✅ 0 |
| 虚假路径 `alembic/versions/`（仓库不存在该目录） | ✅ 0 |
| `audit_path_consistency.py`（五目录全文扫描） | ✅ 0 违规 |
| registry.py doc 路径 | ✅ `src/server/os_core/...` |
| `.cursor/rules/工厂操作系统.md` | ✅ 10 模块 + 物理路径 |
| `18-一致性矩阵` D11~D13 | ✅ v6 + ADR-008 + migrations |
| `_factoryos_pipeline` 历史工件 alembic/deps | ✅ 批量勘误 |

### W1~W4 功能链路（72/72）

| 阶段 | 结果 | 关键路径 |
|------|------|----------|
| W1~W3 | ✅ | `src/server/api/modules/*` |
| W4 Connector | ✅ | `src/server/os_core/connector_sdk/runtime` |
| W4 Registry | ✅ | `src/server/api/modules/registry` |
| pending | 20 | W5+ 预期红 |

### W5 下一步（SH-步步流 · 绝对门禁）

> **联动**：Dev→Test→Verify 节拍不变 · 须 **`确认规划`** + `./scripts/gate plan`

1. 新建 `_factoryos_pipeline/<date>/plan/plan-*-w5-*.md`
2. 用户 **`确认规划`** → `./scripts/gate plan`
3. 更新本文件 `plan` / `goal` / `phase: CAN_CODE`
4. Test 写 failing test → Dev **`可以开始`**

### 开发者入口

- HTTP 路由第一站：`src/server/api/router/v1/registry.py`
- 内核第一站：`src/server/os_core/registry.py`
- GIP 清单：`src/integration/registry.py`
- 工作流真源：`.cursor/factoryos/INDEX.md`
