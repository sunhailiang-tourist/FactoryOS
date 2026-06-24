# CMV 同步规则

> 版本：v1.0.0 | 日期：2026-06-16  
> 真源：`CMV注册表.yaml`  
> 消费方：DSL Registry · Blueprint `spec.ops[].verb` · MCP `tools/list` · OpenAPI `/v1/dsl/registry`

## 1. 单一真源

```text
CMV注册表.yaml
  ├─→ os_core/shared_contracts/cmv_loader.py（W1 codegen 或 runtime load）
  ├─→ GET /v1/dsl/registry → DSLAction[]（补 params_schema）
  ├─→ MCP tools/list（工具名 = verb）
  └─→ Blueprint 校验（spec.ops[].verb ∈ CMV）
```

**禁止**：在代码、Blueprint、MCP 中硬编码未登记动词。

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
- 见 [ConnectorBlueprint.schema.json](./ConnectorBlueprint.schema.json)

## 5. 新增动词流程

1. 更新 `CMV注册表.yaml`  
2. `python scripts/check_cmv_sync.py`  
3. 更新 [DSL执行动词.md](../规格说明/DSL执行动词.md)  
4. 绑定 Capability Pack → [能力追溯矩阵](../架构/能力-模块包-模块追溯矩阵.md)  
5. ADR 或 Pack 版本说明（L2 新动词）

## 6. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-16 | C1-4 初版；check_cmv_sync.py |
