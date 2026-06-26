"""FastAPI 依赖：测试/运行时 DB 会话。

作用：与 pytest migrated_db_session 共用 SQLite shared memory。
业务关联：W2 audit/execute 路由须读写同一库。
上游：routes/audit · routes/execute
下游：SQLAlchemy Session
关联文档：src/tests/conftest.py migrated_db_session
"""
from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


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
  from pathlib import Path

  from alembic import command
  from alembic.config import Config

  root = Path(__file__).resolve().parents[3]
  cfg = Config(str(root / "alembic.ini"))
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
  return _SessionLocal


def get_db_session() -> Generator[Session, None, None]:
  """FastAPI 依赖：请求级 Session，结束时 close。

  功能：yield SQLAlchemy Session。
  业务含义：路由与 integration 测试共享 :memory: 库（cache=shared）。
  """
  factory = _ensure_engine()
  session = factory()
  try:
    yield session
  finally:
    session.close()
