"""Depends(get_tenant_id)。"""
from __future__ import annotations

from fastapi import Request


def get_tenant_id(request: Request) -> str:
  return getattr(request.state, "tenant_id", "default")
