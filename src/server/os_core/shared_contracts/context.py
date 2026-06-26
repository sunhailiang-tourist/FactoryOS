"""请求上下文（tenant_id 等）— contextvars 真源。

作用：middleware 注入 · os_core 只读当前租户键。
业务关联：ADR-007 多租户 · 多租户与隔离规格 MT-01。
上游：config/tenant/middleware
下游：audit · execution · graph store 查询
"""
from __future__ import annotations

from contextvars import ContextVar, Token

_tenant_id: ContextVar[str] = ContextVar("tenant_id", default="default")


def get_tenant_id() -> str:
  """当前上下文 tenant_id。"""
  return _tenant_id.get()


def set_tenant_id(tenant_id: str) -> Token[str]:
  """设置 tenant_id，返回 reset token。"""
  return _tenant_id.set(tenant_id)


def reset_tenant_id(token: Token[str]) -> None:
  """恢复先前 tenant_id。"""
  _tenant_id.reset(token)
