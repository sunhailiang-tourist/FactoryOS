"""W1 规模预埋表（AC S-01～S-04 · ADR-007 §15）。

Revision ID: 001_scale_s01_s04
Revises:
Create Date: 2026-06-25

业务：tenants 规模字段 + 空表 connector_instances/tenant_quotas/outbox_events；
      seed 默认 tenant default → cell-default / pool。
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "001_scale_s01_s04"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DEFAULT_TENANT_ID = "default"
DEFAULT_CELL_ID = "cell-default"
DEFAULT_PLACEMENT_TIER = "pool"


def upgrade() -> None:
  """创建规模预埋表并 seed 默认 tenant。"""
  op.create_table(
    "tenants",
    sa.Column("tenant_id", sa.String(length=64), primary_key=True),
    sa.Column(
      "cell_id",
      sa.String(length=128),
      nullable=False,
      server_default=DEFAULT_CELL_ID,
    ),
    sa.Column(
      "placement_tier",
      sa.String(length=32),
      nullable=False,
      server_default=DEFAULT_PLACEMENT_TIER,
    ),
    sa.Column("region", sa.String(length=64), nullable=True),
  )

  op.create_table(
    "connector_instances",
    sa.Column("instance_id", sa.String(length=64), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("pack_id", sa.String(length=128), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )

  op.create_table(
    "tenant_quotas",
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("quota_key", sa.String(length=64), nullable=False),
    sa.Column("limit_value", sa.Integer(), nullable=False, server_default="0"),
  )

  op.create_table(
    "outbox_events",
    sa.Column("event_id", sa.String(length=36), primary_key=True),
    sa.Column("tenant_id", sa.String(length=64), nullable=False),
    sa.Column("event_type", sa.String(length=128), nullable=False),
    sa.Column("payload", sa.Text(), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
    sa.Column(
      "created_at",
      sa.DateTime(timezone=False),
      nullable=False,
      server_default=sa.text("(CURRENT_TIMESTAMP)"),
    ),
  )

  tenants_table = sa.table(
    "tenants",
    sa.column("tenant_id", sa.String),
    sa.column("cell_id", sa.String),
    sa.column("placement_tier", sa.String),
    sa.column("region", sa.String),
  )
  op.bulk_insert(
    tenants_table,
    [
      {
        "tenant_id": DEFAULT_TENANT_ID,
        "cell_id": DEFAULT_CELL_ID,
        "placement_tier": DEFAULT_PLACEMENT_TIER,
        "region": None,
      }
    ],
  )


def downgrade() -> None:
  """回滚规模预埋表。"""
  op.drop_table("outbox_events")
  op.drop_table("tenant_quotas")
  op.drop_table("connector_instances")
  op.drop_table("tenants")
