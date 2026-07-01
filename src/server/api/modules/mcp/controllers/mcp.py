"""MCP 域 HTTP 路由（OpenAPI POST /mcp/v1/{tenantId}）。

作用：薄路由；委托 mcp_gateway.handle_mcp_json_rpc。
业务关联：M-01 tools/list · M-02 tools/call。
上游：modules/mcp/routers
下游：os_core.mcp_gateway
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.mcp_gateway import handle_mcp_json_rpc

router = APIRouter(tags=["MCP"])


@router.post("/mcp/v1/{tenant_id}")
def mcp_json_rpc_http(
  tenant_id: str,
  body: dict[str, Any],
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /mcp/v1/{tenantId}（M-01 · M-02）。"""
  return handle_mcp_json_rpc(session, tenant_id=tenant_id, request=body)
