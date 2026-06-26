"""Connector Blueprint catalog 加载与校验（W4 Step1 · B-01/B-04）。

作用：从 integration/catalog 加载 Pack Blueprint；L2 op 须声明 revert。
业务关联：B-01 加载 conn-mock · B-04 L2 无 revert → BLUEPRINT_INVALID。
上游：integration/catalog/*.yaml
下游：connector_sdk.runtime · execution_service（W4 Step3+）
关联文档：docs/文档/规格说明/Connector-Blueprint规格.md
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from os_core.shared_contracts.cmv_registry import get_verb_level
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.repo_paths import integration_dir, repo_root

_REPO_ROOT = repo_root()
_CATALOG_DIR = integration_dir() / "catalog"


def _catalog_path(pack_id: str) -> Path:
  """catalog 文件路径：`{pack_id}.yaml`。"""
  return _CATALOG_DIR / f"{pack_id}.yaml"


def validate_blueprint(blueprint: dict[str, Any]) -> dict[str, Any]:
  """校验 Blueprint 结构；L2 CMV op 须含 revert（B-04）。"""
  errors: list[dict[str, str]] = []

  if blueprint.get("apiVersion") != "factoryos.io/v1":
    errors.append(
      {"code": ErrorCode.BLUEPRINT_INVALID, "message": "apiVersion must be factoryos.io/v1"}
    )
  if blueprint.get("kind") != "ConnectorBlueprint":
    errors.append(
      {"code": ErrorCode.BLUEPRINT_INVALID, "message": "kind must be ConnectorBlueprint"}
    )

  metadata = blueprint.get("metadata") or {}
  if metadata.get("pack_id") and not str(metadata["pack_id"]).startswith("conn-"):
    errors.append(
      {"code": ErrorCode.BLUEPRINT_INVALID, "message": "metadata.pack_id must match conn-*"}
    )

  ops = (blueprint.get("spec") or {}).get("ops") or []
  if not ops:
    errors.append({"code": ErrorCode.BLUEPRINT_INVALID, "message": "spec.ops must not be empty"})

  for op in ops:
    if not isinstance(op, dict):
      continue
    verb = op.get("verb")
    if not verb:
      continue
    level = get_verb_level(str(verb))
    if level == "L2" and not op.get("revert"):
      errors.append(
        {
          "code": ErrorCode.BLUEPRINT_INVALID,
          "message": f"L2 op {verb} requires revert declaration",
        }
      )

  return {"valid": not errors, "errors": errors}


@lru_cache(maxsize=32)
def _load_blueprint_file(pack_id: str) -> dict[str, Any]:
  """加载 Blueprint（Registry DB 优先 · integration/catalog 回退）。"""
  from os_core.platform_registry import pack_store
  from os_core.platform_registry.session import get_registry_session

  session = get_registry_session()
  if session is not None:
    blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
    if blueprint is not None:
      return blueprint

  path = _catalog_path(pack_id)
  if not path.is_file():
    raise PlatformError(
      ErrorCode.CONNECTOR_NOT_CONFIGURED,
      f"Blueprint catalog missing for pack_id={pack_id}: {path.relative_to(_REPO_ROOT)}",
      http_status=403,
    )
  raw = yaml.safe_load(path.read_text(encoding="utf-8"))
  if not isinstance(raw, dict):
    raise PlatformError(
      ErrorCode.BLUEPRINT_INVALID,
      f"Invalid blueprint YAML: {path.name}",
      http_status=422,
    )
  return raw


def load_blueprint(*, pack_id: str, tenant_id: str) -> dict[str, Any]:
  """加载 tenant 可见 Blueprint（B-01）。"""
  _ = tenant_id
  blueprint = _load_blueprint_file(pack_id)
  meta_pack = (blueprint.get("metadata") or {}).get("pack_id")
  if meta_pack and meta_pack != pack_id:
    raise PlatformError(
      ErrorCode.BLUEPRINT_INVALID,
      f"metadata.pack_id={meta_pack} does not match requested pack_id={pack_id}",
      http_status=422,
    )
  validation = validate_blueprint(blueprint)
  if not validation["valid"]:
    first = validation["errors"][0]["message"] if validation["errors"] else "invalid blueprint"
    raise PlatformError(ErrorCode.BLUEPRINT_INVALID, first, http_status=422)
  return blueprint
