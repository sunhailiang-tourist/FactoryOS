"""pytest 全局配置与 AC 注册表。

作用：为 AC-BASE-001 提供统一 marker、契约路径 fixture。
上游：contracts/acceptance · contracts/openapi
下游：src/tests/ac · contract 子套件
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.ac_registry import load_ac_ids

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
OPENAPI = CONTRACTS / "openapi" / "工厂操作系统-v1.1.yaml"

AC_IDS = load_ac_ids()


def pytest_configure(config: pytest.Config) -> None:
    for ac_id in AC_IDS:
        config.addinivalue_line("markers", f"ac({ac_id}): AC-BASE-001 case {ac_id}")
    config.addinivalue_line("markers", "integration: DB / API integration tests")


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def migrated_db_session(repo_root: Path):
    """Alembic upgrade head 后的 DB 会话（S-02～S-04 共用）。

    功能：无 PG 时用 SQLite 内存库；CI 可设 TEST_DATABASE_URL 覆盖。
    业务：规模预埋 AC 的数据面断言前置。
    """
    import os

    alembic_ini = repo_root / "alembic.ini"
    if not alembic_ini.is_file():
        pytest.fail("W1 Step3: 缺少 alembic.ini — migrated_db_session 不可用")

    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    db_url = os.environ.get(
      "TEST_DATABASE_URL",
      "sqlite:///:memory:?cache=shared",
    )
    cfg = Config(str(alembic_ini))
    cfg.set_main_option("sqlalchemy.url", db_url)

    engine_kwargs: dict = {}
    if ":memory:" in db_url:
      engine_kwargs["connect_args"] = {"check_same_thread": False}
      engine_kwargs["poolclass"] = StaticPool

    engine = create_engine(db_url, **engine_kwargs)
    with engine.begin() as conn:
      cfg.attributes["connection"] = conn
      command.upgrade(cfg, "head")

    factory = sessionmaker(bind=engine)
    session = factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture(scope="session")
def contracts_dir() -> Path:
    return CONTRACTS


@pytest.fixture(scope="session")
def openapi_path() -> Path:
    return OPENAPI
