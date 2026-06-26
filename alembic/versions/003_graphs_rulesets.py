"""W3 business_graphs · rulesets 表。

Revision ID: 003_graphs_rulesets
Revises: 002_audit_execution
Create Date: 2026-06-26

业务：Graph 版本链 · RuleSet 绑定 graph_version（G-* · R-*）。
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003_graphs_rulesets"
down_revision: Union[str, None] = "002_audit_execution"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """创建 business_graphs · rulesets 表。"""
  op.create_table(
    "business_graphs",
    sa.Column("graph_id", sa.String(length=128), nullable=False),
    sa.Column("version", sa.String(length=32), nullable=False),
    sa.Column("tenant_id", sa.String(length=64), nullable=True),
    sa.Column("status", sa.String(length=32), nullable=False),
    sa.Column("checksum", sa.String(length=80), nullable=False),
    sa.Column("body_json", sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint("graph_id", "version"),
  )
  op.create_index("ix_business_graphs_tenant", "business_graphs", ["tenant_id"])

  op.create_table(
    "rulesets",
    sa.Column("ruleset_id", sa.String(length=128), primary_key=True),
    sa.Column("graph_id", sa.String(length=128), nullable=False),
    sa.Column("graph_version", sa.String(length=32), nullable=False),
    sa.Column("status", sa.String(length=32), nullable=False),
    sa.Column("body_json", sa.Text(), nullable=False),
  )
  op.create_index(
    "ix_rulesets_graph",
    "rulesets",
    ["graph_id", "graph_version"],
  )


def downgrade() -> None:
  """回滚 graphs/rulesets 表。"""
  op.drop_index("ix_rulesets_graph", table_name="rulesets")
  op.drop_table("rulesets")
  op.drop_index("ix_business_graphs_tenant", table_name="business_graphs")
  op.drop_table("business_graphs")
