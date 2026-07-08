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
  """清空 JSON Schema 进程内缓存。

  功能：失效 load_schema 的 lru_cache。
  业务含义：contract_set 发布后须重载 Schema。
  上游：Registry session 切换 · 测试 teardown。
  下游：load_schema 下次调用重读 DB/export。
  """
  load_schema.cache_clear()


def schemas_dir() -> Path:
  """返回 contracts/schemas export 目录。

  功能：暴露 _SCHEMAS_DIR 路径。
  业务含义：CI 镜像与文档生成；运行时优先读 Registry DB。
  返回：schemas 目录 Path。
  """
  return _SCHEMAS_DIR


@lru_cache(maxsize=64)
def load_schema(filename: str) -> dict[str, Any]:
  """按文件名加载 JSON Schema（DB 优先 · export 回退）。

  功能：contract_store.get_schema_json 或读 export 文件。
  业务含义：Pydantic/OpenAPI 校验与 contract test 共用 Schema 真源。
  参数 filename：如 BusinessGraph.schema.json。
  返回：解析后的 Schema dict。
  异常：export 缺失时 FileNotFoundError。
  """
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
