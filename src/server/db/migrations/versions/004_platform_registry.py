"""B 档 Platform Registry（ADR-008 · 18 表 + schema 审计 + connector_instances 扩列）。

Revision ID: 004_platform_registry
Revises: 003_graphs_rulesets
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "004_platform_registry"
down_revision: str | None = "003_graphs_rulesets"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  """创建 Platform Registry 表并扩展 connector_instances。"""
  op.create_table(
    "contract_sets",
    sa.Column("set_id", sa.String(length=128), primary_key=True),
    sa.Column("semver", sa.String(length=32), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "contract_artifacts",
    sa.Column("artifact_id", sa.String(length=128), primary_key=True),
    sa.Column("set_id", sa.String(length=128), nullable=False),
    sa.Column("kind", sa.String(length=64), nullable=False),
    sa.Column("artifact_key", sa.String(length=256), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("checksum", sa.String(length=80), nullable=False),
    sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
  )
  op.create_index("ix_contract_artifacts_set", "contract_artifacts", ["set_id"])
  op.create_table(
    "contract_compatibility_rules",
    sa.Column("rule_id", sa.String(length=128), primary_key=True),
    sa.Column("set_id", sa.String(length=128), nullable=False),
    sa.Column("artifact_kind", sa.String(length=64), nullable=False),
    sa.Column("compatibility_mode", sa.String(length=32), nullable=False),
    sa.Column("rule_body", sa.Text(), nullable=True),
  )
  op.create_table(
    "contract_environment_bindings",
    sa.Column("binding_id", sa.String(length=128), primary_key=True),
    sa.Column("environment", sa.String(length=32), nullable=False),
    sa.Column("set_id", sa.String(length=128), nullable=False),
    sa.Column("cell_id", sa.String(length=128), nullable=True),
    sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
  )
  op.create_index(
    "ix_contract_env_bindings_env",
    "contract_environment_bindings",
    ["environment", "cell_id"],
  )
  op.create_table(
    "contract_publish_records",
    sa.Column("record_id", sa.String(length=128), primary_key=True),
    sa.Column("set_id", sa.String(length=128), nullable=False),
    sa.Column("from_status", sa.String(length=32), nullable=True),
    sa.Column("to_status", sa.String(length=32), nullable=False),
    sa.Column("published_by", sa.String(length=128), nullable=False),
    sa.Column("diff_summary", sa.Text(), nullable=True),
    sa.Column(
      "published_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "contract_consumer_pins",
    sa.Column("pin_id", sa.String(length=128), primary_key=True),
    sa.Column("consumer_key", sa.String(length=128), nullable=False),
    sa.Column("set_id", sa.String(length=128), nullable=False),
    sa.Column("artifact_id", sa.String(length=128), nullable=True),
  )
  op.create_index("ix_contract_consumer_pins_key", "contract_consumer_pins", ["consumer_key"])
  op.create_table(
    "pack_registry",
    sa.Column("pack_id", sa.String(length=128), primary_key=True),
    sa.Column("registry_key", sa.String(length=256), nullable=False),
    sa.Column("certification_level", sa.String(length=32), nullable=False, server_default="bronze"),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("checksum", sa.String(length=80), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
  )
  op.create_table(
    "pack_certification_records",
    sa.Column("cert_id", sa.String(length=128), primary_key=True),
    sa.Column("pack_id", sa.String(length=128), nullable=False),
    sa.Column("level", sa.String(length=32), nullable=False),
    sa.Column("evidence", sa.Text(), nullable=True),
    sa.Column("certified_by", sa.String(length=128), nullable=True),
    sa.Column(
      "certified_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "system_relations",
    sa.Column("relation_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("pack_id", sa.String(length=128), nullable=False),
    sa.Column("environment", sa.String(length=32), nullable=False, server_default="prod"),
    sa.Column("path", sa.String(length=8), nullable=True),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("lifecycle", sa.String(length=32), nullable=False, server_default="draft"),
  )
  op.create_index("ix_system_relations_tenant", "system_relations", ["tenant_id"])
  op.create_table(
    "tenant_profiles",
    sa.Column("tenant_id", sa.String(length=64), primary_key=True),
    sa.Column("display_name", sa.String(length=256), nullable=True),
    sa.Column("path", sa.String(length=8), nullable=True),
    sa.Column("shadow_mode", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    sa.Column("write_approved", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    sa.Column("profile_json", sa.Text(), nullable=True),
  )
  op.create_table(
    "override_documents",
    sa.Column("override_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("scope", sa.String(length=64), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
  )
  op.create_index("ix_override_documents_tenant", "override_documents", ["tenant_id"])
  op.create_table(
    "tenant_pack_entitlements",
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("pack_id", sa.String(length=128), nullable=False),
    sa.Column("licensed", sa.Boolean(), nullable=False, server_default=sa.text("1")),
  )
  op.create_index("ix_tenant_pack_entitlements_tenant", "tenant_pack_entitlements", ["tenant_id"])
  op.create_table(
    "config_versions",
    sa.Column("version_id", sa.String(length=128), primary_key=True),
    sa.Column("entity_type", sa.String(length=64), nullable=False),
    sa.Column("entity_id", sa.String(length=128), nullable=False),
    sa.Column("version_no", sa.Integer(), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("created_by", sa.String(length=128), nullable=True),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_index("ix_config_versions_entity", "config_versions", ["entity_type", "entity_id"])
  op.create_table(
    "snapshot_blobs",
    sa.Column("snapshot_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=True),
    sa.Column("kind", sa.String(length=64), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("checksum", sa.String(length=80), nullable=False),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "config_rollback_points",
    sa.Column("rollback_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=True),
    sa.Column("label", sa.String(length=256), nullable=False),
    sa.Column("snapshot_id", sa.String(length=128), nullable=True),
    sa.Column("version_id", sa.String(length=128), nullable=True),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "config_change_requests",
    sa.Column("request_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=True),
    sa.Column("kind", sa.String(length=64), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
    sa.Column("proposed_by", sa.String(length=128), nullable=False),
    sa.Column("proposal_body", sa.Text(), nullable=False),
    sa.Column("ai_model_id", sa.String(length=128), nullable=True),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "import_export_jobs",
    sa.Column("job_id", sa.String(length=128), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=True),
    sa.Column("direction", sa.String(length=16), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
    sa.Column("payload_ref", sa.Text(), nullable=True),
    sa.Column("error_message", sa.Text(), nullable=True),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  op.create_table(
    "deployment_schema_audit",
    sa.Column("audit_id", sa.String(length=128), primary_key=True),
    sa.Column("environment", sa.String(length=32), nullable=False),
    sa.Column("alembic_revision", sa.String(length=64), nullable=False),
    sa.Column("deployed_by", sa.String(length=128), nullable=True),
    sa.Column(
      "deployed_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )
  with op.batch_alter_table("connector_instances") as batch_op:
    batch_op.add_column(sa.Column("relation_id", sa.String(length=128), nullable=True))
    batch_op.add_column(sa.Column("base_url", sa.String(length=512), nullable=True))
    batch_op.add_column(sa.Column("secrets_ref", sa.String(length=512), nullable=True))
    batch_op.add_column(sa.Column("edge_agent_id", sa.String(length=128), nullable=True))
    batch_op.add_column(sa.Column("environment", sa.String(length=32), nullable=True))
    batch_op.add_column(sa.Column("mapping_overrides_json", sa.Text(), nullable=True))


def downgrade() -> None:
  """回滚 Platform Registry。"""
  with op.batch_alter_table("connector_instances") as batch_op:
    batch_op.drop_column("mapping_overrides_json")
    batch_op.drop_column("environment")
    batch_op.drop_column("edge_agent_id")
    batch_op.drop_column("secrets_ref")
    batch_op.drop_column("base_url")
    batch_op.drop_column("relation_id")
  op.drop_table("deployment_schema_audit")
  op.drop_table("import_export_jobs")
  op.drop_table("config_change_requests")
  op.drop_table("config_rollback_points")
  op.drop_table("snapshot_blobs")
  op.drop_index("ix_config_versions_entity", table_name="config_versions")
  op.drop_table("config_versions")
  op.drop_index("ix_tenant_pack_entitlements_tenant", table_name="tenant_pack_entitlements")
  op.drop_table("tenant_pack_entitlements")
  op.drop_index("ix_override_documents_tenant", table_name="override_documents")
  op.drop_table("override_documents")
  op.drop_table("tenant_profiles")
  op.drop_index("ix_system_relations_tenant", table_name="system_relations")
  op.drop_table("system_relations")
  op.drop_table("pack_certification_records")
  op.drop_table("pack_registry")
  op.drop_index("ix_contract_consumer_pins_key", table_name="contract_consumer_pins")
  op.drop_table("contract_consumer_pins")
  op.drop_table("contract_publish_records")
  op.drop_index("ix_contract_env_bindings_env", table_name="contract_environment_bindings")
  op.drop_table("contract_environment_bindings")
  op.drop_table("contract_compatibility_rules")
  op.drop_index("ix_contract_artifacts_set", table_name="contract_artifacts")
  op.drop_table("contract_artifacts")
  op.drop_table("contract_sets")
