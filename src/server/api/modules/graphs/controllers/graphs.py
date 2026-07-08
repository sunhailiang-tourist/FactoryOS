"""Graph 域 HTTP 路由（OpenAPI /v1/graphs/*）。

作用：薄路由；委托 graph_service。
业务关联：G-01～G-08。
上游：modules/*/routers
下游：os_core.graph_service
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.graph_service import (
  clone_graph_version,
  create_graph,
  freeze_graph_version,
  get_graph_version,
  submit_graph_version,
  update_graph_version,
)
from os_core.rule_engine import ensure_studio_ruleset_for_graph
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.graph import BusinessGraph, GraphStatus

router = APIRouter(tags=["Graph"])


@router.post("/v1/graphs", status_code=201)
def create_graph_http(
  body: BusinessGraph,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/graphs（G-01 draft）。

  功能：创建 BusinessGraph 草稿版本。
  业务含义：Studio 资产步 Graph 入库起点。
  上游：BusinessGraph body · get_db_session。
  下游：graph_service.create_graph。
  """
  graph = create_graph(session, body)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.get("/v1/graphs/{graph_id}")
def get_graph_http(
  graph_id: str,
  version: str | None = Query(default=None),
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/graphs/{graphId}。

  功能：按 graph_id + version 读取 Graph。
  业务含义：Studio 编辑/冻结前加载真源。
  参数 version：默认 v1.0.0。
  下游：graph_service.get_graph_version。
  异常: PlatformError · GRAPH_NOT_FROZEN 等
  """
  ver = version or "v1.0.0"
  graph = get_graph_version(session, graph_id=graph_id, version=ver)
  if graph is None:
    from os_core.shared_contracts.errors import ErrorCode
    from os_core.shared_contracts.exceptions import PlatformError

    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{ver} not found",
      http_status=404,
    )
  return graph.model_dump(mode="json", by_alias=True)


@router.put("/v1/graphs/{graph_id}/versions/{version}")
def update_graph_http(
  graph_id: str,
  version: str,
  body: BusinessGraph,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """PUT 更新 draft/in_review（G-02 · G-06 负向）。

  功能：更新指定版本 Graph 内容。
  业务含义：frozen 后不可改（G-06 负向在 service 拦截）。
  下游：graph_service.update_graph_version。
  """
  graph = update_graph_version(session, graph_id=graph_id, version=version, body=body)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/submit")
def submit_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST submit draft→in_review（G-04）。

  功能：状态迁移 draft→in_review。
  业务含义：顾问提交审核前必经步。
  下游：graph_service.submit_graph_version。
  """
  graph = submit_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/freeze")
def freeze_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST freeze（G-05 · STU-01 Studio 链：submit + RuleSet + freeze 编排）。

  功能：三步编排——draft 则 submit → ensure RuleSet → freeze Graph。
  业务含义：顾问零仓库完成 Graph+Rule 闭环；编排留在 API 层不污染 os_core 边界。
  上游：freeze_graph_http · get_db_session。
  下游：graph_service · rule_engine.ensure_studio_ruleset_for_graph。
  异常: PlatformError · GRAPH_NOT_FROZEN 等
  """
  graph = get_graph_version(session, graph_id=graph_id, version=version)
  if graph is None:
    raise PlatformError(
      ErrorCode.GRAPH_NOT_FROZEN,
      f"Graph {graph_id}@{version} not found",
      http_status=404,
    )
  # 业务步 1：draft 须先 submit，否则 freeze 门禁拒绝
  if graph.status == GraphStatus.DRAFT:
    graph = submit_graph_version(session, graph_id=graph_id, version=version)
  # 业务步 2：无 frozen RuleSet 时自动创建并 freeze（STU-01）
  ensure_studio_ruleset_for_graph(session, graph=graph)
  # 业务步 3：Graph 版本冻结，供 execution 消费
  graph = freeze_graph_version(session, graph_id=graph_id, version=version, frozen_by="studio")
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/clone", status_code=201)
def clone_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST clone 新版本 draft（G-07）。

  功能：从 frozen 版本克隆新 draft。
  业务含义：多版本迭代而不破坏已冻结真源。
  下游：graph_service.clone_graph_version。
  """
  graph = clone_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)
