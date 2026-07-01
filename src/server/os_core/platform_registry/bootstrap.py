"""Registry 幂等 bootstrap（export/fixture → DB 真源）。

作用：首次启动或测试 DB 从 contracts/ + integration/ 灌入 published Registry。
业务关联：ADR-008 迁移期 · CI pytest migrated_db_session。
上游：contracts/ · src/integration/（export 镜像）
下游：contract_store · pack_store · tenant_config_store
"""
from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path

import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.platform_registry import contract_store, tenant_config_store
from os_core.shared_contracts.repo_paths import contracts_dir, integration_dir


def _checksum(body: str) -> str:
  digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
  return f"sha256:{digest}"


def _insert_contract_set(session: Session) -> None:
  session.execute(
    text(
      """
      INSERT INTO contract_sets (set_id, semver, status, description)
      VALUES (:set_id, :semver, :status, :description)
      """
    ),
    {
      "set_id": "factoryos-v1",
      "semver": "1.0.0",
      "status": "published",
      "description": "FactoryOS v1 contract set (bootstrap)",
    },
  )


def _insert_artifact(
  session: Session,
  *,
  artifact_id: str,
  kind: str,
  artifact_key: str,
  body: str,
) -> None:
  session.execute(
    text(
      """
      INSERT INTO contract_artifacts (
        artifact_id, set_id, kind, artifact_key, body, checksum, version
      ) VALUES (
        :artifact_id, :set_id, :kind, :artifact_key, :body, :checksum, 1
      )
      """
    ),
    {
      "artifact_id": artifact_id,
      "set_id": "factoryos-v1",
      "kind": kind,
      "artifact_key": artifact_key,
      "body": body,
      "checksum": _checksum(body),
    },
  )


def _seed_contracts(session: Session) -> None:
  cmv_path = contracts_dir() / "cmv" / "CMV注册表.yaml"
  if cmv_path.is_file():
    body = cmv_path.read_text(encoding="utf-8")
    _insert_artifact(
      session,
      artifact_id="artifact-cmv-registry",
      kind="cmv",
      artifact_key="cmv/CMV注册表.yaml",
      body=body,
    )

  schemas_dir = contracts_dir() / "schemas"
  if schemas_dir.is_dir():
    for path in sorted(schemas_dir.glob("*.schema.json")):
      body = path.read_text(encoding="utf-8")
      _insert_artifact(
        session,
        artifact_id=f"artifact-schema-{path.stem}",
        kind="schema",
        artifact_key=f"schemas/{path.name}",
        body=body,
      )

  openapi_dir = contracts_dir() / "openapi"
  if openapi_dir.is_dir():
    for path in sorted(openapi_dir.glob("*.yaml")):
      body = path.read_text(encoding="utf-8")
      _insert_artifact(
        session,
        artifact_id=f"artifact-openapi-{path.stem}",
        kind="openapi",
        artifact_key=f"openapi/{path.name}",
        body=body,
      )

  session.execute(
    text(
      """
      INSERT INTO contract_environment_bindings (
        binding_id, environment, set_id, cell_id, active
      ) VALUES (
        :binding_id, :environment, :set_id, NULL, 1
      )
      """
    ),
    {
      "binding_id": f"bind-prod-{uuid.uuid4().hex[:8]}",
      "environment": "prod",
      "set_id": "factoryos-v1",
    },
  )
  session.execute(
    text(
      """
      INSERT INTO contract_publish_records (
        record_id, set_id, from_status, to_status, published_by, diff_summary
      ) VALUES (
        :record_id, :set_id, 'draft', 'published', :published_by, :diff_summary
      )
      """
    ),
    {
      "record_id": f"cpr-{uuid.uuid4().hex[:12]}",
      "set_id": "factoryos-v1",
      "published_by": "bootstrap",
      "diff_summary": "initial seed from contracts export",
    },
  )


def _seed_packs(session: Session) -> None:
  catalog = integration_dir() / "catalog"
  if not catalog.is_dir():
    return
  for path in sorted(catalog.glob("*.yaml")):
    pack_id = path.stem
    body = path.read_text(encoding="utf-8")
    session.execute(
      text(
        """
        INSERT INTO pack_registry (
          pack_id, registry_key, certification_level, body, checksum, status
        ) VALUES (
          :pack_id, :registry_key, :certification_level, :body, :checksum, :status
        )
        """
      ),
      {
        "pack_id": pack_id,
        "registry_key": f"catalog/{path.name}",
        "certification_level": "bronze",
        "body": body,
        "checksum": _checksum(body),
        "status": "published",
      },
    )


def _seed_tenants(session: Session) -> None:
  tenants_dir = integration_dir() / "tenants"
  if not tenants_dir.is_dir():
    return
  for tenant_yaml in sorted(tenants_dir.glob("*/tenant.yaml")):
    raw = tenant_yaml.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
      continue
    meta = data.get("metadata") or {}
    spec = data.get("spec") or {}
    status = data.get("status") or {}
    tenant_id = str(meta.get("tenant_id") or tenant_yaml.parent.name)
    session.execute(
      text(
        """
        INSERT INTO tenant_profiles (
          tenant_id, display_name, path, shadow_mode, write_approved, profile_json
        ) VALUES (
          :tenant_id, :display_name, :path, :shadow_mode, :write_approved, :profile_json
        )
        """
      ),
      {
        "tenant_id": tenant_id,
        "display_name": meta.get("display_name"),
        "path": spec.get("path"),
        "shadow_mode": bool(spec.get("shadow_mode", False)),
        "write_approved": bool(status.get("write_approved", False)),
        "profile_json": json.dumps(data, ensure_ascii=False),
      },
    )
    rel_dir = tenant_yaml.parent / "system_relations"
    if rel_dir.is_dir():
      for rel_path in sorted(rel_dir.glob("*.yaml")):
        rel_body = rel_path.read_text(encoding="utf-8")
        rel_data = yaml.safe_load(rel_body)
        if not isinstance(rel_data, dict):
          continue
        rel_meta = rel_data.get("metadata") or {}
        rel_spec = rel_data.get("spec") or {}
        rel_status = rel_data.get("status") or {}
        connector = rel_spec.get("connector") or {}
        relation_id = str(rel_meta.get("relation_id") or rel_path.stem)
        pack_id = str(connector.get("pack_id") or "unknown")
        session.execute(
          text(
            """
            INSERT INTO system_relations (
              relation_id, tenant_id, pack_id, environment, path, body, lifecycle
            ) VALUES (
              :relation_id, :tenant_id, :pack_id, :environment, :path, :body, :lifecycle
            )
            """
          ),
          {
            "relation_id": relation_id,
            "tenant_id": tenant_id,
            "pack_id": pack_id,
            "environment": rel_spec.get("environment") or "prod",
            "path": rel_meta.get("path"),
            "body": rel_body,
            "lifecycle": rel_status.get("lifecycle") or "draft",
          },
        )
        session.execute(
          text(
            """
            INSERT INTO tenant_pack_entitlements (tenant_id, pack_id, licensed)
            VALUES (:tenant_id, :pack_id, 1)
            """
          ),
          {"tenant_id": tenant_id, "pack_id": pack_id},
        )


def _seed_fixture_tenants(session: Session) -> None:
  """集成测试夹具租户：default（全授权）· tenant-unlicensed-w6（有 Connector 无 License）。"""
  fixtures: tuple[tuple[str, bool], ...] = (
    ("default", True),
    ("tenant-unlicensed-w6", False),
  )
  for tenant_id, licensed in fixtures:
    if tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id) is None:
      session.execute(
        text(
          """
          INSERT INTO tenant_profiles (
            tenant_id, display_name, path, shadow_mode, write_approved, profile_json
          ) VALUES (
            :tenant_id, :display_name, NULL, 0, 0, NULL
          )
          """
        ),
        {"tenant_id": tenant_id, "display_name": tenant_id},
      )
    relation_id = f"rel-{tenant_id}-conn-mock"
    existing_rel = session.execute(
      text(
        """
        SELECT 1 FROM system_relations
        WHERE tenant_id = :tenant_id AND pack_id = 'conn-mock' LIMIT 1
        """
      ),
      {"tenant_id": tenant_id},
    ).first()
    if existing_rel is None:
      session.execute(
        text(
          """
          INSERT INTO system_relations (
            relation_id, tenant_id, pack_id, environment, path, body, lifecycle
          ) VALUES (
            :relation_id, :tenant_id, 'conn-mock', 'test', NULL, :body, 'active'
          )
          """
        ),
        {
          "relation_id": relation_id,
          "tenant_id": tenant_id,
          "body": "fixture: conn-mock for AC regression",
        },
      )
    session.execute(
      text(
        """
        DELETE FROM tenant_pack_entitlements
        WHERE tenant_id = :tenant_id AND pack_id = 'conn-mock'
        """
      ),
      {"tenant_id": tenant_id},
    )
    if licensed:
      session.execute(
        text(
          """
          INSERT INTO tenant_pack_entitlements (tenant_id, pack_id, licensed)
          VALUES (:tenant_id, 'conn-mock', 1)
          """
        ),
        {"tenant_id": tenant_id},
      )


def _seed_fixture_graph(session: Session) -> None:
  """集成测试夹具：default 租户 frozen graph + ruleset（P-01 export 前置）。"""
  graph_id = "graph-d1-generic-template"
  version = "v1.0.0"
  ruleset_id = "ruleset-w3-default"
  existing = session.execute(
    text(
      """
      SELECT 1 FROM business_graphs
      WHERE graph_id = :graph_id AND version = :version LIMIT 1
      """
    ),
    {"graph_id": graph_id, "version": version},
  ).first()
  if existing is not None:
    return

  now = "2026-06-01T00:00:00Z"
  graph_body = {
    "id": graph_id,
    "version": version,
    "status": "frozen",
    "checksum": "sha256:bootstrap-fixture-graph-checksum-placeholder00000000",
    "tenant_id": "default",
    "nodes": [{"id": "node-start", "type": "start", "label": "Start"}],
    "edges": [],
    "allowed_dsl": ["QUERY_ENTITY", "GOVERNED_WRITE"],
    "metadata": {"created_at": now, "updated_at": now},
  }
  session.execute(
    text(
      """
      INSERT INTO business_graphs (
        graph_id, version, tenant_id, status, checksum, body_json
      ) VALUES (
        :graph_id, :version, :tenant_id, :status, :checksum, :body_json
      )
      """
    ),
    {
      "graph_id": graph_id,
      "version": version,
      "tenant_id": "default",
      "status": "frozen",
      "checksum": graph_body["checksum"],
      "body_json": json.dumps(graph_body, ensure_ascii=False),
    },
  )
  ruleset_body = {
    "id": ruleset_id,
    "graph_id": graph_id,
    "graph_version": version,
    "status": "frozen",
    "default_effect": "deny",
    "rules": [
      {
        "id": "rule-allow-operator",
        "effect": "allow",
        "subjects": ["role:operator"],
        "actions": ["QUERY_ENTITY", "GOVERNED_WRITE"],
        "priority": 10,
      }
    ],
    "metadata": {"created_at": now, "updated_at": now},
  }
  session.execute(
    text(
      """
      INSERT INTO rulesets (
        ruleset_id, graph_id, graph_version, status, body_json
      ) VALUES (
        :ruleset_id, :graph_id, :graph_version, :status, :body_json
      )
      """
    ),
    {
      "ruleset_id": ruleset_id,
      "graph_id": graph_id,
      "graph_version": version,
      "status": "frozen",
      "body_json": json.dumps(ruleset_body, ensure_ascii=False),
    },
  )


def bootstrap_registry(session: Session, *, root: Path | None = None) -> bool:
  """幂等灌入 Registry；已 seed 则跳过。返回本次是否新写入。"""
  _ = root  # 保留参数兼容 conftest；路径由 repo_paths 解析
  if contract_store.is_seeded(session):
    return False
  _insert_contract_set(session)
  _seed_contracts(session)
  _seed_packs(session)
  _seed_tenants(session)
  _seed_fixture_tenants(session)
  _seed_fixture_graph(session)
  session.commit()
  return True
