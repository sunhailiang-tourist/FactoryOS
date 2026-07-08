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
  """解析 FactoryOS 仓库根目录。

  功能：自本文件向上查找含 pyproject.toml 的目录。
  业务含义：目录搬迁后避免 Path(__file__).parents[N] 漂移。
  返回：仓库根 Path。
  异常：未找到时 RuntimeError。
  """
  here = Path(__file__).resolve()
  for parent in here.parents:
    if (parent / "pyproject.toml").is_file():
      return parent
  msg = "FactoryOS repo root (pyproject.toml) not found"
  raise RuntimeError(msg)


def contracts_dir() -> Path:
  """返回 contracts/ export 镜像路径。

  功能：repo_root / contracts。
  业务含义：CI 与离线 bootstrap 读契约镜像真源。
  返回：contracts 目录 Path。
  """
  return repo_root() / "contracts"


def integration_dir() -> Path:
  """返回 integration export 镜像路径。

  功能：repo_root / src/integration。
  业务含义：Pack 源码 · path 模板 YAML · fixture 镜像。
  返回：src/integration Path。
  """
  return repo_root() / "src" / "integration"



def alembic_versions_dir() -> Path:
  """返回 Alembic 迁移 versions 目录。

  功能：repo_root / src/server/db/migrations/versions。
  业务含义：迁移脚本与 bootstrap 对账路径。
  返回：versions 目录 Path。
  """
  return repo_root() / "src" / "server" / "db" / "migrations" / "versions"
