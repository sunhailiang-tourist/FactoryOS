# connector_sdk/runtime · Blueprint Runtime

## 是什么

解释 `integration/catalog` Blueprint，执行 CMV op（read/write/revert）。

## 主要功能

- Step1：包骨架 + registry 加载（B-01）
- Step2+：`execute_op` · mapping · legacy_refs（B-02/B-03 · C-02/C-03）

## 不负责什么

- 业务规则、Rule/Graph 门禁（在 execution_service）

## 上下游

- **上游**：`registry.load_blueprint` · `execution_service`
- **下游**：`mock_legacy`（W4 mock）· 未来 httpx Legacy

## 相关文档

- `docs/文档/规格说明/Connector-Blueprint规格.md`
