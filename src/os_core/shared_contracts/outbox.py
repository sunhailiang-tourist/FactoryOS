"""进程内 Outbox 端口（S-04 · FactoryOS Queue S0 实现）。

作用：将域事件持久化到 outbox_events；S1 可换 Redis Streams 不改调用方。
业务关联：ADR-007 S7-19 消息演进预埋。
上游：graph_service、execution_service（未来）
下游：outbox_events 表、未来 Worker 消费
关联文档：架构决策记录-007 §15.5
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class OutboxPort:
  """in-process Outbox 写入端口（S0）。

  业务含义：同事务或独立 commit 持久化事件；W1 仅验 DB 行存在。
  """

  def __init__(self, session: Session) -> None:
    """绑定 SQLAlchemy 会话。"""
    self._session = session

  def publish(
    self,
    tenant_id: str,
    event_type: str,
    payload: dict[str, Any],
  ) -> str:
    """写入一条 outbox 事件并提交。

    功能：INSERT outbox_events。
    业务含义：解耦发布与消费；S0 不启动独立 Worker。
    上游调用方：内核服务、集成测试
    下游被调方：outbox_events 表
    参数 tenant_id：租户 ID
    参数 event_type：事件类型字符串
    参数 payload：JSON 可序列化载荷
    返回：新生成的 event_id（UUID 字符串）
    """
    event_id = str(uuid.uuid4())
    self._session.execute(
      text(
        "INSERT INTO outbox_events "
        "(event_id, tenant_id, event_type, payload, status) "
        "VALUES (:event_id, :tenant_id, :event_type, :payload, 'pending')"
      ),
      {
        "event_id": event_id,
        "tenant_id": tenant_id,
        "event_type": event_type,
        "payload": json.dumps(payload, ensure_ascii=False),
      },
    )
    self._session.commit()
    return event_id
