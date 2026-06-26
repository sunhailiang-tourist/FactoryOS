"""仓库根路径解析（目录搬迁后仍稳定）。

作用：替代各模块内 Path(__file__).parents[N] 硬编码。
业务关联：ADR-008 src/server/ 重组 · bootstrap · loader export 回退。
上游：任意 os_core 模块
下游：contracts/ · src/integration/ export 镜像路径
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def repo_root() -> Path:
  """向上查找含 pyproject.toml 的目录作为仓库根。"""
  here = Path(__file__).resolve()
  for parent in here.parents:
    if (parent / "pyproject.toml").is_file():
      return parent
  msg = "FactoryOS repo root (pyproject.toml) not found"
  raise RuntimeError(msg)


def contracts_dir() -> Path:
  """contracts/ export 镜像目录。"""
  return repo_root() / "contracts"


def integration_dir() -> Path:
  """integration export 镜像目录（src/integration）。"""
  return repo_root() / "src" / "integration"



def alembic_versions_dir() -> Path:
  """Alembic versions 目录（src/server/db/migrations/versions）。"""
  return repo_root() / "src" / "server" / "db" / "migrations" / "versions"
