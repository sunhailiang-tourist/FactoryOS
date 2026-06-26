"""Alembic 迁移环境。

作用：执行规模预埋表 revision（S-01～S-04）。
业务关联：ADR-007 W1 migration；测试可用 SQLite 内存库。
上游：alembic.ini
下游：alembic/versions/
关联文档：docs/文档/架构/架构决策记录-007-百级千级演进策略.md §15
"""
from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Engine

config = context.config

if config.config_file_name is not None:
  fileConfig(config.config_file_name)

target_metadata = None


def _engine_for_url(url: str) -> Engine:
  """SQLite :memory: 须 StaticPool + cache=shared 方与 pytest 同库。"""
  if ":memory:" in url:
    return engine_from_config(
      config.get_section(config.config_ini_section, {}),
      prefix="sqlalchemy.",
      poolclass=pool.StaticPool,
      connect_args={"check_same_thread": False},
    )
  return engine_from_config(
    config.get_section(config.config_ini_section, {}),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
  )


def run_migrations_offline() -> None:
  """离线模式执行 migration。"""
  url = config.get_main_option("sqlalchemy.url")
  context.configure(
    url=url,
    target_metadata=target_metadata,
    literal_binds=True,
    dialect_opts={"paramstyle": "named"},
  )

  with context.begin_transaction():
    context.run_migrations()


def run_migrations_online() -> None:
  """在线模式执行 migration。"""
  url = config.get_main_option("sqlalchemy.url") or ""
  connection = config.attributes.get("connection")

  if connection is not None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
      context.run_migrations()
    return

  connectable = _engine_for_url(url)

  with connectable.connect() as conn:
    context.configure(connection=conn, target_metadata=target_metadata)

    with context.begin_transaction():
      context.run_migrations()


if context.is_offline_mode():
  run_migrations_offline()
else:
  run_migrations_online()
