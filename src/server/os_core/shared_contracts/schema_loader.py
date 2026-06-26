"""contracts/schemas JSON Schema 加载器（Contract Registry 真源 · ADR-008）。

作用：从 Registry 或 export 镜像只读加载 Schema。
业务关联：校验、文档生成、测试对账。
上游：platform_registry.contract_store（优先）· contracts/schemas export
下游：contract 测试、未来 jsonschema 校验
关联文档：ADR-008 · contracts/README.md
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from os_core.shared_contracts.repo_paths import contracts_dir, repo_root

_ROOT = repo_root()
_SCHEMAS_DIR = contracts_dir() / "schemas"


def clear_cache() -> None:
  """Session 切换后清空 Schema 缓存。"""
  load_schema.cache_clear()


def schemas_dir() -> Path:
  """返回 contracts/schemas export 目录（CI 镜像 · 非运行时真源）。"""
  return _SCHEMAS_DIR


@lru_cache(maxsize=64)
def load_schema(filename: str) -> dict[str, Any]:
  """按文件名加载 JSON Schema（DB 优先 · export 回退）。"""
  from os_core.platform_registry import contract_store
  from os_core.platform_registry.session import get_registry_session

  session = get_registry_session()
  if session is not None:
    data = contract_store.get_schema_json(session, filename=filename)
    if data is not None:
      return data

  path = _SCHEMAS_DIR / filename
  if not path.is_file():
    msg = f"Schema not found: {path}"
    raise FileNotFoundError(msg)
  return json.loads(path.read_text(encoding="utf-8"))
