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
from os_core.shared_contracts.models.graph import BusinessGraph

router = APIRouter(tags=["Graph"])


@router.post("/v1/graphs", status_code=201)
def create_graph_http(
  body: BusinessGraph,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/graphs（G-01 draft）。"""
  graph = create_graph(session, body)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.get("/v1/graphs/{graph_id}")
def get_graph_http(
  graph_id: str,
  version: str | None = Query(default=None),
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/graphs/{graphId}。"""
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
  """PUT 更新 draft/in_review（G-02 · G-06 负向）。"""
  graph = update_graph_version(session, graph_id=graph_id, version=version, body=body)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/submit")
def submit_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST submit draft→in_review（G-04）。"""
  graph = submit_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/freeze")
def freeze_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST freeze（G-05）。"""
  graph = freeze_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)


@router.post("/v1/graphs/{graph_id}/versions/{version}/clone", status_code=201)
def clone_graph_http(
  graph_id: str,
  version: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST clone 新版本 draft（G-07）。"""
  graph = clone_graph_version(session, graph_id=graph_id, version=version)
  session.commit()
  return graph.model_dump(mode="json", by_alias=True)
