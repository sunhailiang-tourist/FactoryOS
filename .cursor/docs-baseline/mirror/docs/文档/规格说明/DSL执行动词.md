# 规格说明·DSL：执行动词注册表

| 版本 | v0.2.0 |
|------|--------|
| 范围 | DSL 框架 + **CMV**（见 [CMV注册表.yaml](../数据结构/CMV注册表.yaml)） |
| Schema | [DSL动作.schema.json](../数据结构/DSL动作.schema.json) |

## 1. 职责

- 全局 **DSL 动词注册表**（Registry）
- 动词 → 安全级别（L0–L3）
- 动词 → params JSON Schema
- 动词 → Compensator（写操作）
- 动词 → Connector 操作映射

Agent 只能产出已注册动词；Executor 只执行已注册动词。

## 2. 动词命名（CMV）

- 全大写 + 下划线；**published 真源** = Contract Registry CMV artifact；**export 镜像**：[CMV注册表.yaml](../数据结构/CMV注册表.yaml)（ADR-008）
- **禁止** vendor 私有动词（ADR-004）

## 3. 底座内置动词（用于 Phase 1 内核测试）

| 动词 | Level | Compensator | 用途 |
|------|-------|-------------|------|
| `QUERY_ENTITY` | L0 | null | 跨系统只读查询（mock） |
| `GOVERNED_WRITE` | L2 | `GOVERNED_WRITE_REVERT` | 测试 governed 写 + revert |
| `GOVERNED_WRITE_REVERT` | L2 | null | 补偿写 |
| `QUERY_EXECUTION_HISTORY` | L0 | null | 查 ExecutionRecord |

> 以上 **不绑定具体 MES 字段**，params 使用抽象 `entity_type`, `entity_id`, `payload`。

## 4. 垂直 Pack 预留动词（未启用直至 Graph frozen）

| 动词 | Level | Compensator | 说明 |
|------|-------|-------------|------|
| `QUERY_WO` | L0 | null | 工单查询 |
| `WORK_REPORT` | L2 | `WORK_REPORT_REVERT` | 报工 |
| `WORK_REPORT_REVERT` | L2 | null | 报工撤销 |
| `QUERY_REPORT_HISTORY` | L0 | null | 报工历史 |

工厂 Graph workshop 后，在租户 RuleSet 中授权上述动词子集。

## 5. Params 示例（底座）

### QUERY_ENTITY

```json
{
  "entity_type": "string",
  "entity_id": "string",
  "fields": ["string"]
}
```

### GOVERNED_WRITE

```json
{
  "entity_type": "string",
  "entity_id": "string",
  "payload": { "type": "object" },
  "idempotency_key": "string"
}
```

### GOVERNED_WRITE_REVERT

```json
{
  "legacy_ref": "mock.entity:uuid",
  "reason": "operator mistake"
}
```

> HTTP 撤销入口为 `POST /v1/execute/{exec_id}/revert`；`execution_service` 将 `exec_id` 映射为对应 `legacy_ref` 再调用 compensator 动词。

## 6. 注册 API

```http
GET  /v1/dsl/registry
GET  /v1/dsl/registry/{verb}
POST /v1/dsl/registry   # admin only；新动词需 ADR 或 Pack 版本说明
```

## 7. 扩展规则

1. 新 L2 动词 **必须** 同时注册 Compensator
2. L3 动词 Phase 2 前禁止默认启用
3. 动词变更不修改已有注册条目；deprecated 标记 + 新 verb

## 8. 与 Graph 关系

- Graph.allowed_dsl 是动词 **白名单**
- 执行时：`verb ∈ registry` AND `verb ∈ graph.allowed_dsl` AND Rule allow

## 9. 底座验收

见 [AC-BASE-001](../验收/验收用例-BASE-001-平台底座.md) § DSL 章节。
