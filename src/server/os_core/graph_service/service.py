"""graph_service 业务编排（CRUD · 生命周期 · freeze）。

作用：Graph 版本链唯一写入口；不写 Legacy。
业务关联：G-01～G-08 · execute 前 frozen 门禁。
上游：server.api.modules.graphs.controllers
下游：business_graphs · audit_service
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
  参数 graph：待创建 BusinessGraph 模型。
  返回：status=draft 的 BusinessGraph。
  异常：版本已存在 409。
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
  """读取 Graph 版本（GET /v1/graphs）。

  功能：委托 store.get_graph。
  业务含义：HTTP GET 与 execute 前置查询共用。
  参数 graph_id/version：Graph 定位键。
  返回：BusinessGraph 或 None。
  """
  return get_graph(session, graph_id=graph_id, version=version)


def update_graph_version(
  session: Session,
  *,
  graph_id: str,
  version: str,
  body: BusinessGraph,
) -> BusinessGraph:
  """更新 draft/in_review Graph（G-02）。

  功能：校验可编辑后 UPDATE body_json。
  业务含义：Studio 编辑图谱内容；frozen/deprecated 拒绝。
  参数 body：新图谱内容（id/version 以路径为准）。
  返回：更新后的 BusinessGraph。
  异常：不存在 404；不可编辑 409。
  """
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
  """draft → in_review（G-04）。

  功能：校验 draft 后 UPDATE status=in_review。
  业务含义：提交审核；freeze 前置状态。
  参数 graph_id/version：Graph 定位键。
  返回：status=in_review 的 BusinessGraph。
  异常：不存在 404；非 draft 409。
  """
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

  功能：校验 in_review + frozen RuleSet 后写入 checksum 并冻结。
  业务含义：execute L2 写前置；产出不可变图谱版本。
  参数 frozen_by：冻结操作者标识。
  返回：status=frozen · 有效 checksum 的 BusinessGraph。
  异常：前置不满足 409。
  """
  # 业务：校验 in_review 与 frozen RuleSet 后计算 checksum 并冻结 Graph
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
  """clone 出新 draft 版本（G-07）。

  功能：复制源版本内容并 bump patch version。
  业务含义：基于 frozen/in_review 版本迭代新 draft。
  参数 graph_id/version：源 Graph 定位键。
  返回：新 draft 版本 BusinessGraph。
  异常：源不存在 404；目标版本已存在 409。
  """
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
  """标记 frozen → deprecated（G-08 测试用内核 API）。

  功能：校验 frozen 后 UPDATE status=deprecated。
  业务含义：下线旧版本；L2 写将被拒绝。
  参数 graph_id/version：Graph 定位键。
  返回：status=deprecated 的 BusinessGraph。
  异常：不存在 404；非 frozen 409。
  """
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

  功能：校验 frozen/deprecated 与 allowed_dsl 白名单。
  业务含义：L2 写须 frozen；deprecated 拒绝 L2；verb 须在白名单。
  参数 verb/verb_level：CMV verb 与级别（L0/L2）。
  返回：通过门禁的 BusinessGraph。
  异常：不满足条件 409/403。
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
