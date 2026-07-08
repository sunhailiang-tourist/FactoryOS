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
  """读取当前异步上下文中的 tenant_id。

  功能：从 ContextVar 取值，默认 default。
  业务含义：MT-01 多厂隔离键；无 middleware 时回退 default。
  返回：当前租户 ID 字符串。
  """
  return _tenant_id.get()


def set_tenant_id(tenant_id: str) -> Token[str]:
  """设置当前上下文 tenant_id。

  功能：ContextVar.set 并返回 reset token。
  业务含义：HTTP middleware 每请求注入租户键。
  参数 tenant_id：本请求所属租户。
  返回：reset_tenant_id 所需的 Token。
  """
  return _tenant_id.set(tenant_id)


def reset_tenant_id(token: Token[str]) -> None:
  """恢复 set_tenant_id 之前的 tenant_id。

  功能：ContextVar.reset(token)。
  业务含义：请求结束清理，防止上下文泄漏到下一请求。
  参数 token：set_tenant_id 返回的 Token。
  """
  _tenant_id.reset(token)
