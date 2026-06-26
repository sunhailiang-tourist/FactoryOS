# dsl · CMV 动词注册表 HTTP 域

> **OpenAPI**：`GET /v1/dsl/registry` · AC **D-01**  
> **内核**：`os_core/shared_contracts/cmv_registry`

## 是什么

**CMV（Common Manufacturing Verbs）** 动词白名单的只读 HTTP 面。  
Execution 仅允许 registry 中声明的 DSL 动词（如 `WORK_REPORT`、`QUERY_WO`）。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/dsl/registry` | 返回 CMV 动词列表（动作 · 描述 · 分类） |

## 怎么用

```bash
curl -s http://127.0.0.1:8000/v1/dsl/registry
```

无 DB 依赖；直接读 `cmv_registry.list_dsl_actions()`。

## 承载业务

- **动词治理**：统一制造语义 · Agent/Studio 下拉 · Execution 校验  
- **published 真源**：Contract Registry CMV artifact（ADR-008）  
- **export 镜像**：`contracts/cmv/CMV注册表.yaml` → 代码 `cmv_registry.py`（DB 优先 · export 回退）

## 上下游

- **上游**：Studio DSL 面板 · Agent 规划 · 文档生成  
- **下游**：`shared_contracts.cmv_registry`（无 store）  
- **执行链**：`execution_service` 校验 verb ∈ registry

## 门禁

```bash
./scripts/check_cmv_sync.py
uv run pytest src/tests/contract/test_shared_contracts.py -q
```

## 关联文档

- [contracts/cmv/CMV注册表.yaml](../../../../contracts/cmv/CMV注册表.yaml)  
- [CMV 同步规则](../../../docs/文档/数据结构/CMV同步规则.md)
