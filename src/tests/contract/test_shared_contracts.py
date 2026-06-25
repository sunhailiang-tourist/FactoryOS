"""W1 Step2：shared_contracts Pydantic 与 contracts/schemas 字段对齐。

业务：L0 契约代码化；required 字段须与 JSON Schema 真源一致。
上游：contracts/schemas/*.schema.json
下游：os_core.shared_contracts.models（Dev Step2 实现）
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

# plan §Step2 优先 Schema 清单：(模块属性名, schema 文件名)
W1_SCHEMA_PAIRS: list[tuple[str, str]] = [
  ("ExecutionRecord", "执行记录.schema.json"),
  ("AuditEvent", "AuditEvent.schema.json"),
  ("DslPlan", "DslPlan.schema.json"),
  ("BusinessGraph", "业务图谱.schema.json"),
  ("RuleSet", "规则集.schema.json"),
  ("DomainEvent", "DomainEvent.schema.json"),
  ("ExecutionEvidence", "ExecutionEvidence.schema.json"),
]


def _load_schema_required(schemas_dir: Path, filename: str) -> set[str]:
  data = json.loads((schemas_dir / filename).read_text(encoding="utf-8"))
  return set(data.get("required", []))


@pytest.mark.contract
@pytest.mark.parametrize(
  ("model_attr", "schema_file"),
  W1_SCHEMA_PAIRS,
  ids=[f"contract-{attr}" for attr, _ in W1_SCHEMA_PAIRS],
)
def test_shared_contract_model_required_fields_match_schema(
  model_attr: str,
  schema_file: str,
  contracts_dir: Path,
) -> None:
  """Pydantic 模型存在且 required 字段与 JSON Schema 一致。"""
  schemas_dir = contracts_dir / "schemas"
  expected_required = _load_schema_required(schemas_dir, schema_file)

  models = importlib.import_module("os_core.shared_contracts.models")
  model_cls = getattr(models, model_attr, None)
  assert model_cls is not None, f"os_core.shared_contracts.models 缺少 {model_attr}"

  schema = model_cls.model_json_schema()
  actual_required = set(schema.get("required", []))
  assert actual_required == expected_required, (
    f"{model_attr}: model required {sorted(actual_required)} "
    f"!= schema required {sorted(expected_required)}"
  )
