"""Tenant FastAPI Depends。

作用：get_tenant_id 从 request.state 读取租户 ID。
业务关联：controllers 与 os_core 共用 tenant 上下文。
上游：tenant/middleware。
下游：modules/*/controllers · quota checker。
"""
from __future__ import annotations

from fastapi import Request


def get_tenant_id(request: Request) -> str:
  """从 request.state 读取 tenant_id。

  功能：FastAPI Depends 注入当前租户 ID。
  业务含义：与 TenantMiddleware 上下文一致。
  上游：tenant/middleware。
  返回：str tenant_id。
  """
  return getattr(request.state, "tenant_id", "default")
