"""contracts/schemas JSON Schema 加载器。

作用：从仓库契约目录只读加载 Schema 文本/对象。
业务关联：校验、文档生成、测试对账。
上游：contracts/schemas/*.schema.json
下游：contract 测试、未来 jsonschema 校验
关联文档：contracts/README.md
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[3]
_SCHEMAS_DIR = _ROOT / "contracts" / "schemas"


def schemas_dir() -> Path:
  """返回 contracts/schemas 目录路径。

  业务含义：W1 契约真源在仓库内固定相对路径。
  返回：Schema 目录绝对路径
  """
  return _SCHEMAS_DIR


@lru_cache(maxsize=64)
def load_schema(filename: str) -> dict[str, Any]:
  """按文件名加载 JSON Schema。

  功能：读取并解析单个 Schema 文件。
  业务含义：运行时与测试共用同一加载入口，避免路径硬编码分散。
  上游调用方：contract 测试、集成校验
  下游被调方：contracts/schemas 文件
  参数 filename：如 ``执行记录.schema.json``
  返回：解析后的 Schema 字典
  """
  path = _SCHEMAS_DIR / filename
  if not path.is_file():
    msg = f"Schema not found: {path}"
    raise FileNotFoundError(msg)
  return json.loads(path.read_text(encoding="utf-8"))
