"""W2 audit + execution 表（AuditEvent · ExecutionRecord）。

Revision ID: 002_audit_execution
Revises: 001_scale_s01_s04
Create Date: 2026-06-25

业务：append-only audit_events · execution 账本 execution_records；
      幂等键 tenant+idempotency_key 唯一（E-07 预备）。
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "002_audit_execution"
down_revision: str | None = "001_scale_s01_s04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  """创建 audit_events · execution_records 表。"""
  op.create_table(
    "audit_events",
    sa.Column("event_id", sa.String(length=36), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("event_type", sa.String(length=64), nullable=False),
    sa.Column("actor_json", sa.Text(), nullable=False),
    sa.Column("occurred_at", sa.String(length=32), nullable=False),
    sa.Column("exec_id", sa.String(length=36), nullable=True),
    sa.Column("graph_id", sa.String(length=128), nullable=True),
    sa.Column("graph_version", sa.String(length=32), nullable=True),
    sa.Column("pack_id", sa.String(length=128), nullable=True),
    sa.Column("plan_id", sa.String(length=36), nullable=True),
    sa.Column("payload_json", sa.Text(), nullable=True),
    sa.Column("correlation_id", sa.String(length=128), nullable=True),
  )
  op.create_index("ix_audit_events_tenant_exec", "audit_events", ["tenant_id", "exec_id"])

  op.create_table(
    "execution_records",
    sa.Column("exec_id", sa.String(length=36), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("verb", sa.String(length=128), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False),
    sa.Column("graph_id", sa.String(length=128), nullable=False),
    sa.Column("graph_version", sa.String(length=32), nullable=False),
    sa.Column("actor_json", sa.Text(), nullable=False),
    sa.Column("started_at", sa.String(length=32), nullable=False),
    sa.Column("scope_id", sa.String(length=128), nullable=True),
    sa.Column("ruleset_id", sa.String(length=128), nullable=True),
    sa.Column("idempotency_key", sa.String(length=128), nullable=True),
    sa.Column("shadow_mode", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    sa.Column("params_json", sa.Text(), nullable=True),
    sa.Column("before_snapshot_json", sa.Text(), nullable=True),
    sa.Column("after_snapshot_json", sa.Text(), nullable=True),
    sa.Column("legacy_refs_json", sa.Text(), nullable=True),
    sa.Column("connector_trace_json", sa.Text(), nullable=True),
    sa.Column("compensator_verb", sa.String(length=128), nullable=True),
    sa.Column("revert_of", sa.String(length=36), nullable=True),
    sa.Column("error_json", sa.Text(), nullable=True),
    sa.Column("finished_at", sa.String(length=32), nullable=True),
    sa.Column("dry_run", sa.Boolean(), nullable=False, server_default=sa.text("0")),
  )
  op.create_index(
    "uq_execution_tenant_idempotency",
    "execution_records",
    ["tenant_id", "idempotency_key"],
    unique=True,
    sqlite_where=sa.text("idempotency_key IS NOT NULL"),
  )


def downgrade() -> None:
  """回滚 W2 表。"""
  op.drop_index("uq_execution_tenant_idempotency", table_name="execution_records")
  op.drop_table("execution_records")
  op.drop_index("ix_audit_events_tenant_exec", table_name="audit_events")
  op.drop_table("audit_events")
