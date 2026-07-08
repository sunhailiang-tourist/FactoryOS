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
  """返回当前绑定的 Registry Session。

  功能：读取进程内全局 _registry_session。
  业务含义：未绑定时 cmv/schema loader 回退 contracts/ export。
  返回：Session 或 None。
  """
  return _registry_session


def set_registry_session(session: Session | None) -> None:
  """绑定或解绑 Registry Session。

  功能：写入进程内全局 _registry_session。
  业务含义：须在 bootstrap 之后、首次 loader 调用之前完成注入。
  参数 session：目标 Session；None 表示解绑。
  """
  global _registry_session
  _registry_session = session
