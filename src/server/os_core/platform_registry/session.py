"""Registry 全局 Session 绑定（进程内 · 测试/API 启动时注入）。

作用：让 cmv_registry / schema_loader / connector registry 统一读 DB。
业务关联：ADR-008 运行时真源切换。
上游：conftest · server.api lifespan
下游：platform_registry stores · shared_contracts loaders
"""
from __future__ import annotations

from sqlalchemy.orm import Session

_registry_session: Session | None = None


def get_registry_session() -> Session | None:
  """返回当前绑定的 Registry Session；未绑定时 loader 回退 export 文件。"""
  return _registry_session


def set_registry_session(session: Session | None) -> None:
  """绑定/解绑 Registry Session（须在 bootstrap 之后、首次 loader 调用之前）。"""
  global _registry_session
  _registry_session = session
