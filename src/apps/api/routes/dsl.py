"""DSL 域 HTTP 路由（OpenAPI GET /v1/dsl/registry）。

作用：薄路由；读取 CMV 注册表。
业务关联：D-01。
上游：FastAPI app
下游：shared_contracts.cmv_registry
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from os_core.shared_contracts.cmv_registry import list_dsl_actions

router = APIRouter(tags=["DSL"])


@router.get("/v1/dsl/registry")
def list_dsl_registry_http() -> list[dict[str, Any]]:
  """GET /v1/dsl/registry（D-01）。"""
  return list_dsl_actions()
