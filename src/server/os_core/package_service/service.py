"""Implementation Package export/import 内核。

作用：聚合租户 Graph · RuleSet · Connector 配置为可移植快照。
业务关联：P-01 export · P-02 import（Step4）· Integration Studio。
上游：POST /v1/packages/export · 未来 MCP gateway
下游：graph_service.store · rule_engine.store · platform_registry
关联文档：contracts/schemas/ImplementationPackage.schema.json
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from sqlalchemy.orm import Session

from os_core.graph_service.store import graph_exists, insert_graph, list_graphs_by_tenant
from os_core.platform_registry import pack_store, tenant_config_store
from os_core.rule_engine.store import get_ruleset, insert_ruleset, list_rulesets_for_graph_ids
from os_core.shared_contracts.models.graph import BusinessGraph
from os_core.shared_contracts.models.rule import RuleSet


def _connector_configs_for_tenant(
  session: Session,
  *,
  tenant_id: str,
) -> list[dict[str, Any]]:
  """system_relations → ImplementationPackage.connector_configs[]。"""
  configs: list[dict[str, Any]] = []
  for rel in tenant_config_store.list_system_relations(session, tenant_id=tenant_id):
    pack_id = str(rel.get("pack_id") or "")
    if not pack_id:
      continue
    registry_key = pack_store.get_pack_registry_key(session, pack_id=pack_id)
    if registry_key is None:
      registry_key = f"catalog/{pack_id}.yaml"
    configs.append({"pack_id": pack_id, "registry_key": registry_key})
  return configs


def export_implementation_package(
  session: Session,
  *,
  tenant_id: str,
  delivery: Literal["D1", "D2"] = "D1",
) -> dict[str, Any]:
  """导出租户 Implementation Package（P-01）。

  功能：读取 DB 中租户 Graph · RuleSet · Connector 绑定。
  业务含义：D1/D2 交付快照，供 import 到新租户或 Git 归档。
  参数 tenant_id：导出来源租户。
  参数 delivery：D1 或 D2 交付阶段标识。
  返回：对齐 ImplementationPackage.schema.json 的 dict。
  """
  graphs = list_graphs_by_tenant(session, tenant_id=tenant_id)
  graph_ids = list({g.id for g in graphs})
  rulesets = list_rulesets_for_graph_ids(session, graph_ids=graph_ids)
  exported_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")

  return {
    "package_id": str(uuid.uuid4()),
    "tenant_id": tenant_id,
    "version": "v1.0.0",
    "delivery": delivery,
    "exported_at": exported_at,
    "graphs": [g.model_dump(mode="json", by_alias=True) for g in graphs],
    "rulesets": [r.model_dump(mode="json") for r in rulesets],
    "connector_configs": _connector_configs_for_tenant(session, tenant_id=tenant_id),
  }


def import_implementation_package(
  session: Session,
  *,
  package: dict[str, Any],
) -> dict[str, Any]:
  """导入 Implementation Package 到目标租户（P-02）。

  功能：写入 Graph · RuleSet · system_relations · entitlements。
  业务含义：跨 tenant 交付；import 后 tenant B 可 resolve Pack。
  参数 package：对齐 ImplementationPackage.schema.json 的请求体。
  返回：tenant_id · imported_graphs · imported_rulesets 计数。
  """
  tenant_id = str(package["tenant_id"])
  tenant_config_store.upsert_tenant_settings(session, tenant_id=tenant_id)

  imported_graphs = 0
  for raw in package.get("graphs") or []:
    graph = BusinessGraph.model_validate(raw)
    graph = graph.model_copy(update={"tenant_id": tenant_id})
    if not graph_exists(session, graph_id=graph.id, version=graph.version):
      insert_graph(session, graph)
      imported_graphs += 1

  imported_rulesets = 0
  for raw in package.get("rulesets") or []:
    ruleset = RuleSet.model_validate(raw)
    if get_ruleset(session, ruleset.id) is None:
      insert_ruleset(session, ruleset)
      imported_rulesets += 1

  for cfg in package.get("connector_configs") or []:
    pack_id = str(cfg.get("pack_id") or "")
    if not pack_id:
      continue
    registry_key = cfg.get("registry_key")
    tenant_config_store.ensure_system_relation(
      session,
      tenant_id=tenant_id,
      pack_id=pack_id,
      registry_key=str(registry_key) if registry_key else None,
    )
    tenant_config_store.ensure_pack_entitlement(
      session,
      tenant_id=tenant_id,
      pack_id=pack_id,
    )

  session.commit()
  return {
    "tenant_id": tenant_id,
    "imported_graphs": imported_graphs,
    "imported_rulesets": imported_rulesets,
  }
