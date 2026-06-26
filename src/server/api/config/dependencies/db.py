"""DB 会话依赖（config/dependencies）。

作用：测试/运行时 DB 会话 + Registry bootstrap。

作用：与 pytest migrated_db_session 共用 SQLite shared memory。
业务关联：W2 audit/execute · ADR-008 Registry 真源。
上游：modules/*/controllers
下游：SQLAlchemy Session · platform_registry
"""
from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from os_core.platform_registry import bootstrap_registry, set_registry_session
from os_core.shared_contracts.repo_paths import repo_root


def _database_url() -> str:
  """返回测试/本地 DB URL（与 conftest 默认一致）。"""
  return os.environ.get(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:?cache=shared",
  )


_engine = None
_SessionLocal: sessionmaker[Session] | None = None
_migration_applied = False


def _apply_migrations(engine) -> None:
  """首次建连时 upgrade head（与 conftest migrated_db_session 对齐）。"""
  global _migration_applied
  if _migration_applied:
    return
  from alembic import command
  from alembic.config import Config

  cfg = Config(str(repo_root() / "alembic.ini"))
  cfg.set_main_option("sqlalchemy.url", _database_url())
  with engine.begin() as conn:
    cfg.attributes["connection"] = conn
    command.upgrade(cfg, "head")
  _migration_applied = True


def _ensure_engine() -> sessionmaker[Session]:
  """懒初始化引擎与会话工厂。"""
  global _engine, _SessionLocal
  if _SessionLocal is not None:
    return _SessionLocal
  url = _database_url()
  kwargs: dict = {}
  if ":memory:" in url:
    kwargs["connect_args"] = {"check_same_thread": False}
    kwargs["poolclass"] = StaticPool
  _engine = create_engine(url, **kwargs)
  _apply_migrations(_engine)
  _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
  seed = _SessionLocal()
  bootstrap_registry(seed)
  set_registry_session(seed)
  return _SessionLocal


def get_db_session() -> Generator[Session, None, None]:
  """FastAPI 依赖：请求级 Session，结束时 close。"""
  factory = _ensure_engine()
  session = factory()
  set_registry_session(session)
  try:
    yield session
  finally:
    set_registry_session(None)
    session.close()
