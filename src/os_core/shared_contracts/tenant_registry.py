"""租户 → Cell 注册表（S-03 · ADR-007 S0 no-op 路由）。

作用：查询 tenant 所属 cell_id；S0 单 Cell 直读 DB。
业务关联：百级千级演进时 Router 可换实现，接口不变。
上游：apps/api 中间件、未来 Cell Router
下游：tenants 表
关联文档：架构决策记录-007 §15.4
"""
from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

DEFAULT_CELL_ID = "cell-default"


class TenantRegistry:
  """租户 Cell 查询（S0 内存/DB 直读）。

  业务含义：S-03 验收；未找到 tenant 时回退 cell-default（S0 安全默认）。
  """

  def __init__(self, session: Session) -> None:
    """绑定 SQLAlchemy 会话。

    参数 session：已执行 alembic upgrade 的 ORM 会话
    """
    self._session = session

  def get_cell(self, tenant_id: str) -> str:
    """返回租户所属 cell_id。

    功能：SELECT tenants.cell_id。
    业务含义：S2 前无跨 Cell 路由，仅读预埋列。
    上游调用方：路由中间件、集成测试
    下游被调方：tenants 表
    参数 tenant_id：租户标识，如 default
    返回：cell_id 字符串
    """
    row = (
      self._session.execute(
        text("SELECT cell_id FROM tenants WHERE tenant_id = :tid LIMIT 1"),
        {"tid": tenant_id},
      )
      .mappings()
      .first()
    )
    if row is None:
      return DEFAULT_CELL_ID
    return str(row["cell_id"])
