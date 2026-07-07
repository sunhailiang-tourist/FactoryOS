#!/usr/bin/env python3
"""契约路径解析 — umbrella / standalone 双路径（W-11）。

作用：为 codegen · harness 提供 OpenAPI / vendor 根路径。
业务关联：vendor/factoryos-contracts · contracts/openapi。
上游：devkit.manifest.yaml · FACTORYOS_ROOT · WEB_PROFILE_STANDALONE
下游：check_codegen_fresh · check_standalone_ready
"""
from __future__ import annotations

import os
from pathlib import Path

OPENAPI_FILENAME = "工厂操作系统-v1.1.yaml"
VENDOR_REL = Path("vendor") / "factoryos-contracts"


def app_root_from_here(caller_file: str | Path) -> Path:
  """由 scripts/*.py 定位 App 根目录。"""
  return Path(caller_file).resolve().parents[1]


def vendor_contracts_root(app_root: Path) -> Path:
  """standalone 契约镜像根。"""
  return app_root / VENDOR_REL


def umbrella_openapi_path(app_root: Path) -> Path:
  """FactoryOS monorepo contracts/openapi 路径。"""
  return (app_root / ".." / ".." / ".." / "contracts" / "openapi" / OPENAPI_FILENAME).resolve()


def vendor_openapi_path(app_root: Path) -> Path:
  """vendor 镜像 OpenAPI 路径。"""
  return vendor_contracts_root(app_root) / "openapi" / OPENAPI_FILENAME


def is_standalone_mode(app_root: Path) -> bool:
  """是否按 standalone 解析契约（迁出仓 / 模拟零父仓）。"""
  if os.environ.get("WEB_PROFILE_STANDALONE") == "1":
    return True
  manifest = app_root / "devkit.manifest.yaml"
  if manifest.is_file() and "mode: standalone" in manifest.read_text(encoding="utf-8"):
    return True
  umbrella = umbrella_openapi_path(app_root)
  vendor = vendor_openapi_path(app_root)
  return vendor.is_file() and not umbrella.is_file()


def resolve_openapi_path(app_root: Path) -> Path:
  """解析 codegen 使用的 OpenAPI 真源（standalone 优先 vendor）。"""
  vendor = vendor_openapi_path(app_root)
  umbrella = umbrella_openapi_path(app_root)
  if is_standalone_mode(app_root):
    return vendor
  if umbrella.is_file():
    return umbrella
  return vendor
