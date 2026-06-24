# 规格说明·Connector Agent（GIP Intelligence · S2）

| 版本 | **v1.0.0** |
|------|------------|
| 日期 | 2026-06-16 |
| 范围 | GIP L2 · **S2 接入路径** AI 辅助 Blueprint |
| 模块 | `integration/tools/connector-agent/`（**非 Core**） |
| 对标 | Boomi Integration Advisor · OpenAPI → Blueprint 草稿 |

---

## 1. 职责

从 **厂商 OpenAPI / 样例 JSON / 字段说明** 生成 **ConnectorBlueprint 草稿** + mapping 建议，供集成人员在 Studio **人工审核** 后 Prove。

```text
输入：OpenAPI URL / 样例文件 / 自然语言字段说明
  → Connector Agent（LLM + 结构化输出）
  → ConnectorBlueprint YAML 草稿 + confidence 分数
  → Studio Map 步人工确认
  → POST /v1/integration/blueprint/validate
```

**禁止**：

- Agent 产出直接晋升 Silver/Gold（须 Contract Test + Shadow）  
- Agent 写入 `os_core/*`  
- Agent 注册 CMV 外私有动词  

---

## 2. 输出契约

```json
{
  "pack_id": "conn-erp-acme-write",
  "blueprint_draft": { },
  "verb_mappings": [
    { "verb": "WORK_REPORT", "confidence": 0.86, "op_index": 1 }
  ],
  "warnings": ["missing revert on WORK_REPORT"],
  "model_id": "gpt-4.1-mini"
}
```

`blueprint_draft` **MUST** 可通过 `ConnectorBlueprint.schema.json` 校验后方可保存。

---

## 3. 与三速接入（S1/S2/S3）

| 速度 | Connector Agent 角色 |
|------|----------------------|
| **S1** | 不用（import 已有 Silver Pack） |
| **S2** | **主路径**：生成草稿，目标 ≤2 周定版 |
| **S3** | 仅辅助 builtin/简单 REST；复杂仍 Python Pack |

**日历**：S2「≤2 周」= 含人工 Prove + Shadow，非单次 LLM 调用。

---

## 4. 工具接口（研发期 CLI · Y1）

```bash
connector-agent generate \
  --openapi ./vendor/openapi.yaml \
  --cmv WORK_REPORT,QUERY_WO \
  --output integration/catalog/erp/acme-write.yaml
```

W17+ 可暴露 Studio API：`POST /v1/integration/discover` 内部调用（已有 OpenAPI 路由占位）。

---

## 5. 安全与治理

| 项 | 要求 |
|----|------|
| LLM | dev/staging 默认便宜模型；**生产 Blueprint 生成须人工签字** |
| 凭证 | Agent **不得** 接触生产 secrets；仅用样例/anonymized payload |
| Audit | `event_type=connector_agent.generate` 写入 Audit |
| R-11 | Agent 输出 **不得** 自动触发 Execution |

---

## 6. Phase

| Phase | 范围 |
|-------|------|
| Gate 0 | **不阻塞**；手动 YAML |
| W17+ | CLI + Studio 建议条 |
| Y2 | Mapping Copilot、drift 诊断 |

---

## 7. 验收（待 AC-CONN-AGENT-001）

| ID | 条件 |
|----|------|
| CA-01 | 从 kingdee 样例 JSON 生成 draft，validate 通过 ≥1 op |
| CA-02 | 缺 revert 时 warnings 非空 |
| CA-03 | 无人工确认不得写入 catalog Silver |

---

## 8. 参考

- [17-GIP](../准备/2026-06-16/17-集成平台化战略(GIP).md) §5.2  
- [Integration-Studio规格](./Integration-Studio规格.md)
