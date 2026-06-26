# CMV 同步规则

> 版本：v1.0.0 | 日期：2026-06-16  
> **published 真源**：Contract Registry `contract_artifacts`（CMV · ADR-008）  
> **export 镜像**：`contracts/cmv/CMV注册表.yaml` · 本文件为同步规则说明  
> 消费方：DSL Registry · Blueprint `spec.ops[].verb` · MCP `tools/list` · OpenAPI `/v1/dsl/registry`

## 1. 单一真源（ADR-008）

```text
Contract Registry（publish/frozen CMV artifact）
  ├─→ export → contracts/cmv/CMV注册表.yaml（CI · harness 对账）
  ├─→ os_core/shared_contracts/cmv_registry.py（runtime load · DB 优先回退 export）
  ├─→ GET /v1/dsl/registry → DSLAction[]（补 params_schema）
  ├─→ MCP tools/list（工具名 = verb）
  └─→ Blueprint 校验（spec.ops[].verb ∈ CMV）
```

**禁止**：在 code、Blueprint、MCP 中硬编码未登记动词。

## 2. 字段映射

| CMV YAML | DSLAction JSON | 说明 |
|----------|----------------|------|
| `verb` | `verb` | 大写 SNAKE_CASE |
| `level` | `level` | L0–L3 |
| `compensator` | `compensator` | L2 必填（`*_REVERT` 除外） |
| `idempotent` | `idempotent` | L2 写默认 true |
| `connector_ops` | `connector_ops` | system + operation |
| — | `params_schema` | W1 由 Pack 或 jsonschema 文件生成 |

## 3. CI 校验

```bash
python scripts/check_cmv_sync.py
```

| 规则 | 脚本检查 |
|------|----------|
| verb 命名 | `^[A-Z][A-Z0-9_]*$` |
| L2 有 compensator | ✅ |
| compensator 存在 | ✅ |
| 无重复 verb | ✅ |

**W1 扩展**（Coding 阶段）：

```bash
# 可选：CMV → DSLAction JSON 快照 diff
python scripts/codegen_cmv_registry.py --check
```

## 4. Blueprint 对齐

- `ConnectorBlueprint.spec.ops[].verb` **必须** ∈ CMV
- L2 op **必须** 声明 `revert` + `reconcile.read_verb`（L0 CMV）
- 见 [ConnectorBlueprint.schema.json](../schemas/ConnectorBlueprint.schema.json)

## 5. 新增动词流程（ADR-008）

1. Contract Registry **publish** CMV artifact  
2. export 同步至 `CMV注册表.yaml`  
3. `python scripts/check_cmv_sync.py`  
4. 更新 [DSL执行动词.md](../../docs/文档/规格说明/DSL执行动词.md)  
5. 绑定 Capability Pack → [能力追溯矩阵](../../docs/文档/架构/能力-模块包-模块追溯矩阵.md)  
6. ADR 或 Pack 版本说明（L2 新动词）

## 6. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-16 | C1-4 初版；check_cmv_sync.py |
