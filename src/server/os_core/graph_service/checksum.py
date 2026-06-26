"""BusinessGraph canonical checksum（N-02 预埋）。

作用：freeze 时计算 sha256；draft 用占位符。
业务关联：G-05 freeze 产出有效 checksum。
上游：graph_service.service
下游：business_graphs 表 checksum 列
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from os_core.shared_contracts.cmv_registry import draft_graph_checksum
from os_core.shared_contracts.models.graph import BusinessGraph


def compute_graph_checksum(graph: BusinessGraph) -> str:
  """对 Graph 内容（不含 checksum 字段）计算 sha256。

  功能：canonical JSON sort_keys 后哈希。
  参数 graph：待冻结或校验的 BusinessGraph
  返回：sha256:{hex}
  """
  payload: dict[str, Any] = graph.model_dump(mode="json", by_alias=True)
  payload.pop("checksum", None)
  canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
  digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
  return f"sha256:{digest}"


def default_draft_checksum() -> str:
  """新建 draft Graph 默认 checksum。"""
  return draft_graph_checksum()
