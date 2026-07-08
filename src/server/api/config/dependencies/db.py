"""PostgreSQL Session Depends。

作用：get_db_session 提供请求级 SQLAlchemy Session。
业务关联：ADR-002 写路径须经 os_core service。
上游：settings DATABASE_URL · lifespan 连接池。
下游：os_core/*/service · store。
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
    "sqlite:///file:factoryos_local?mode=memory&cache=shared&uri=true",
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
  # 业务：首次建连时创建引擎、跑迁移、bootstrap Registry 并缓存 Session 工厂
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
  """请求级 SQLAlchemy Session Depends。

  功能：yield Session 并在请求结束 commit/rollback。
  业务含义：controllers 唯一 DB 注入入口。
  上游：settings DATABASE_URL。
  下游：os_core/*/service。
  """
  factory = _ensure_engine()
  session = factory()
  set_registry_session(session)
  try:
    yield session
  finally:
    set_registry_session(None)
    session.close()
