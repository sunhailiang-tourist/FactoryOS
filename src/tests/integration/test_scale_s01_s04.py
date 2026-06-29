"""W1 Step3：规模预埋 S-01～S-04（Alembic · TenantRegistry · OutboxPort）。

业务：ADR-007 表结构预埋；S0 单 Cell 默认 tenant；in-process outbox 不依赖 Redis。
上游：`src/server/db/migrations/` · `alembic.ini` · `os_core.shared_contracts`
下游：gate step --step 3 -k 'S-01'（子用例 S-02～S-04 同文件）
"""
from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest

DEFAULT_TENANT_ID = "default"
EXPECTED_CELL_ID = "cell-default"
EXPECTED_PLACEMENT_TIER = "pool"
SCALE_TABLES = ("tenants", "connector_instances", "tenant_quotas", "outbox_events")
TENANT_SCALE_COLUMNS = ("cell_id", "placement_tier", "region")


def _require_alembic(repo_root: Path) -> None:
  alembic_ini = repo_root / "alembic.ini"
  assert alembic_ini.is_file(), "W1 Step3: 缺少 alembic.ini（S-01 前置）"
  versions = repo_root / "src" / "server" / "db" / "migrations" / "versions"
  assert versions.is_dir(), "W1 Step3: 缺少 src/server/db/migrations/versions/"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["migration"], ids=["S-01"])
def test_S01_scale_tables_after_migration(case: str, repo_root: Path) -> None:
  """S-01：upgrade head 后规模预埋四表存在，tenants 含 cell/placement/region 列。"""
  _require_alembic(repo_root)

  from alembic import command
  from alembic.config import Config
  from sqlalchemy import create_engine, inspect
  from sqlalchemy.pool import StaticPool

  db_url = os.environ.get(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:?cache=shared",
  )
  cfg = Config(str(repo_root / "alembic.ini"))
  cfg.set_main_option("sqlalchemy.url", db_url)

  engine_kwargs: dict = {}
  if ":memory:" in db_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine_kwargs["poolclass"] = StaticPool

  engine = create_engine(db_url, **engine_kwargs)
  with engine.begin() as conn:
    cfg.attributes["connection"] = conn
    command.upgrade(cfg, "head")

  inspector = inspect(engine)
  for table in SCALE_TABLES:
    assert inspector.has_table(table), f"缺少规模表 {table}"

  tenant_cols = {c["name"] for c in inspector.get_columns("tenants")}
  for col in TENANT_SCALE_COLUMNS:
    assert col in tenant_cols, f"tenants 缺少列 {col}"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["seed"], ids=["S-02"])
def test_S02_default_tenant_seed_values(case: str, migrated_db_session) -> None:
  """S-02：默认 tenant seed 为 cell-default / pool。"""
  from sqlalchemy import text

  row = migrated_db_session.execute(
    text(
      "SELECT cell_id, placement_tier FROM tenants "
      "WHERE tenant_id = :tid LIMIT 1"
    ),
    {"tid": DEFAULT_TENANT_ID},
  ).mappings().first()
  assert row is not None, f"缺少默认 tenant {DEFAULT_TENANT_ID}"
  assert row["cell_id"] == EXPECTED_CELL_ID
  assert row["placement_tier"] == EXPECTED_PLACEMENT_TIER


@pytest.mark.integration
@pytest.mark.parametrize("case", ["registry"], ids=["S-03"])
def test_S03_tenant_registry_get_cell(case: str, migrated_db_session) -> None:
  """S-03：TenantRegistry.get_cell(default) 返回 cell-default。"""
  registry_module = importlib.import_module("os_core.shared_contracts.tenant_registry")
  registry_cls = getattr(registry_module, "TenantRegistry", None)
  assert registry_cls is not None, "缺少 TenantRegistry"

  registry = registry_cls(migrated_db_session)
  cell = registry.get_cell(DEFAULT_TENANT_ID)
  assert cell == EXPECTED_CELL_ID


@pytest.mark.integration
@pytest.mark.parametrize("case", ["outbox"], ids=["S-04"])
def test_S04_outbox_port_persists_event(case: str, migrated_db_session) -> None:
  """S-04：in-process OutboxPort 写入 outbox_events 可持久化。"""
  outbox_module = importlib.import_module("os_core.shared_contracts.outbox")
  port_cls = getattr(outbox_module, "OutboxPort", None)
  assert port_cls is not None, "缺少 OutboxPort"

  port = port_cls(migrated_db_session)
  event_id = port.publish(
    tenant_id=DEFAULT_TENANT_ID,
    event_type="factoryos.test.outbox",
    payload={"probe": True},
  )
  assert event_id, "publish 应返回 event_id"

  from sqlalchemy import text

  count = migrated_db_session.execute(
    text("SELECT COUNT(*) AS n FROM outbox_events WHERE tenant_id = :tid"),
    {"tid": DEFAULT_TENANT_ID},
  ).scalar_one()
  assert count >= 1
