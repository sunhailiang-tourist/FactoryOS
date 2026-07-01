"""Integration 域 HTTP 路由（OpenAPI /v1/integration/*）。

作用：薄路由；委托 connector_sdk.connect_test。
业务关联：Studio Connect 步 · P-03 Override 验证。
上游：modules/integration/routers
下游：os_core.connector_sdk.connect_test
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.connector_sdk.connect_test import run_connect_test

router = APIRouter(tags=["Integration"])


class ConnectTestBody(BaseModel):
  """POST /v1/integration/connect/test 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  pack_id: str = Field(description="Connector Pack ID")


@router.post("/v1/integration/connect/test")
def connect_test_http(
  body: ConnectTestBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/integration/connect/test（P-03 · Studio Step 1）。"""
  return run_connect_test(
    session,
    tenant_id=body.tenant_id,
    pack_id=body.pack_id,
  )
