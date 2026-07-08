"""Package 域 HTTP 路由（OpenAPI /v1/packages/*）。

作用：薄路由；委托 package_service。
业务关联：P-01 export · P-02 import（Step4）。
上游：modules/*/routers
下游：os_core.package_service
"""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.package_service import export_implementation_package, import_implementation_package

router = APIRouter(tags=["Package"])


class PackageExportBody(BaseModel):
  """POST /v1/packages/export 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="导出来源租户 ID")
  delivery: Literal["D1", "D2"] = Field(default="D1", description="交付阶段")


@router.post("/v1/packages/export")
def export_package_http(
  body: PackageExportBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/packages/export（P-01）。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Package 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.package_service。
  """
  return export_implementation_package(
    session,
    tenant_id=body.tenant_id,
    delivery=body.delivery,
  )


@router.post("/v1/packages/import")
def import_package_http(
  body: dict[str, Any],
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/packages/import（P-02）。
  功能：薄路由 HTTP 处理；委托 os_core。
  业务含义：Package 域对外 API 入口。
  上游：FastAPI 请求 · Depends 注入。
  下游：os_core.package_service。
  """
  return import_implementation_package(session, package=body)
