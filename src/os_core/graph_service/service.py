"""graph_service 业务编排（CRUD · 生命周期 · freeze）。

作用：Graph 版本链唯一写入口；不写 Legacy。
业务关联：G-01～G-08 · execute 前 frozen 门禁。
上游：apps/api/routes/graphs
下游：business_graphs · audit_service · rule_engine.store
关联文档：contracts/schemas/业务图谱.schema.json
"""
from __future__ import annotations

import re
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from os_core.audit_service.store import append_audit_event
from os_core.graph_service.checksum import compute_graph_checksum, default_draft_checksum
from os_core.graph_service.store import (
  get_graph,
  graph_exists,
  has_frozen_ruleset_for_graph,
  insert_graph,
  update_graph,
)
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.common import Actor, ActorChannel
from os_core.shared_contracts.models.graph import BusinessGraph, GraphStatus


def _now() -> datetime:
  return datetime.now(UTC)


def _ensure_editable(graph: BusinessGraph) -> None:
  """draft/in_review 可编辑；frozen/deprecated 409。"""
  if graph.status in (GraphStatus.FROZEN, GraphStatus.DEPRECATED):
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph.id}@{graph.version} is {graph.status.value}, not editable",
      http_status=409,
    )


def create_graph(session: Session, graph: BusinessGraph) -> BusinessGraph:
  """创建 draft Graph（G-01）。

  功能：INSERT 新版本行；默认 draft checksum。
  业务含义：新流程版本起点；同 id+version 不可重复。
  """
  if graph_exists(session, graph_id=graph.id, version=graph.version):
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph.id}@{graph.version} already exists",
      http_status=409,
    )
  now = _now()
  if graph.status != GraphStatus.DRAFT:
    graph = graph.model_copy(update={"status": GraphStatus.DRAFT})
  if not graph.checksum or graph.checksum == default_draft_checksum():
    graph = graph.model_copy(update={"checksum": default_draft_checksum()})
  meta = graph.metadata.model_copy(update={"created_at": now, "updated_at": now})
  graph = graph.model_copy(update={"metadata": meta})
  insert_graph(session, graph)
  append_audit_event(
    session=session,
    tenant_id=graph.tenant_id or "platform",
    event_type=AuditEventType.GRAPH_CREATED,
    actor=Actor(user_id="system", role="system", channel=ActorChannel.API),
    graph_id=graph.id,
    graph_version=graph.version,
    payload={"status": graph.status.value},
  )
  return graph


def get_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
) -> BusinessGraph | None:
  """读取 Graph 版本（GET /v1/graphs）。"""
  return get_graph(session, graph_id=graph_id, version=version)


def update_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
  body: BusinessGraph,
) -> BusinessGraph:
  """更新 draft/in_review Graph（G-02）。"""
  existing = get_graph(session, graph_id=graph_id, version=version)
  if existing is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  _ensure_editable(existing)
  now = _now()
  meta = body.metadata.model_copy(
    update={
      "created_at": existing.metadata.created_at,
      "updated_at": now,
    }
  )
  updated = body.model_copy(
    update={
      "id": graph_id,
      "version": version,
      "status": existing.status,
      "checksum": existing.checksum,
      "metadata": meta,
    }
  )
  update_graph(session, updated)
  return updated


def submit_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
) -> BusinessGraph:
  """draft → in_review（G-04）。"""
  graph = get_graph(session, graph_id=graph_id, version=version)
  if graph is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  if graph.status != GraphStatus.DRAFT:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph must be draft to submit, got {graph.status.value}",
      http_status=409,
    )
  now = _now()
  meta = graph.metadata.model_copy(update={"updated_at": now})
  updated = graph.model_copy(update={"status": GraphStatus.IN_REVIEW, "metadata": meta})
  update_graph(session, updated)
  return updated


def freeze_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
  frozen_by: str = "system",
) -> BusinessGraph:
  """冻结 Graph（G-05）。

  前置：in_review + 同版本已有 frozen RuleSet。
  产出：status=frozen · 有效 checksum。
  """
  graph = get_graph(session, graph_id=graph_id, version=version)
  if graph is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  if graph.status != GraphStatus.IN_REVIEW:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph must be in_review to freeze, got {graph.status.value}",
      http_status=409,
    )
  if not has_frozen_ruleset_for_graph(session, graph_id=graph_id, graph_version=version):
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      "Cannot freeze graph without a frozen RuleSet for this version",
      http_status=409,
    )
  now = _now()
  checksum = compute_graph_checksum(graph)
  meta = graph.metadata.model_copy(
    update={"updated_at": now, "frozen_at": now, "frozen_by": frozen_by}
  )
  updated = graph.model_copy(
    update={"status": GraphStatus.FROZEN, "checksum": checksum, "metadata": meta}
  )
  update_graph(session, updated)
  append_audit_event(
    session=session,
    tenant_id=graph.tenant_id or "platform",
    event_type=AuditEventType.GRAPH_FROZEN,
    actor=Actor(user_id=frozen_by, role="system", channel=ActorChannel.API),
    graph_id=graph.id,
    graph_version=graph.version,
    payload={"checksum": checksum},
  )
  return updated


def clone_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
) -> BusinessGraph:
  """clone 出新 draft 版本（G-07）。"""
  source = get_graph(session, graph_id=graph_id, version=version)
  if source is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  new_version = _bump_patch_version(version)
  if graph_exists(session, graph_id=graph_id, version=new_version):
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Target version {new_version} already exists",
      http_status=409,
    )
  now = _now()
  meta = source.metadata.model_copy(
    update={
      "created_at": now,
      "updated_at": now,
      "frozen_at": None,
      "frozen_by": None,
    }
  )
  cloned = source.model_copy(
    update={
      "version": new_version,
      "status": GraphStatus.DRAFT,
      "checksum": default_draft_checksum(),
      "metadata": meta,
    }
  )
  insert_graph(session, cloned)
  return cloned


def deprecate_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
) -> BusinessGraph:
  """标记 frozen → deprecated（G-08 测试用内核 API）。"""
  graph = get_graph(session, graph_id=graph_id, version=version)
  if graph is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  if graph.status != GraphStatus.FROZEN:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Only frozen graph can be deprecated, got {graph.status.value}",
      http_status=409,
    )
  now = _now()
  meta = graph.metadata.model_copy(update={"updated_at": now})
  updated = graph.model_copy(update={"status": GraphStatus.DEPRECATED, "metadata": meta})
  update_graph(session, updated)
  return updated


def assert_graph_executable(
  session: Session,
  *,
  graph_id: str,
  graph_version: str,
  verb: str,
  verb_level: str,
) -> BusinessGraph:
  """execute 前 Graph 门禁（G-03 · G-08 · D-03）。

  L2 写：须 frozen；deprecated 拒绝 L2。
  L0 读：须 frozen（E-01）。
  allowed_dsl 白名单校验（D-03）。
  """
  graph = get_graph(session, graph_id=graph_id, version=graph_version)
  if graph is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{graph_version} not found",
      http_status=409,
    )
  if graph.status == GraphStatus.DEPRECATED and verb_level == "L2":
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      "Graph is deprecated",
      http_status=409,
    )
  if graph.status != GraphStatus.FROZEN:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph status is {graph.status.value}, L2 requires frozen",
      http_status=409,
    )
  if graph.allowed_dsl and verb not in graph.allowed_dsl:
    raise PlatformError(
      ErrorCode.DSL_NOT_IN_GRAPH,
      f"Verb {verb} not in graph allowed_dsl",
      http_status=403,
    )
  return graph


def _bump_patch_version(version: str) -> str:
  """vX.Y.Z → vX.Y.(Z+1)。"""
  match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
  if not match:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Invalid version format: {version}",
      http_status=400,
    )
  major, minor, patch = (int(match.group(i)) for i in range(1, 4))
  return f"v{major}.{minor}.{patch + 1}"
