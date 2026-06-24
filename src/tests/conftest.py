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


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def contracts_dir() -> Path:
    return CONTRACTS


@pytest.fixture(scope="session")
def openapi_path() -> Path:
    return OPENAPI
