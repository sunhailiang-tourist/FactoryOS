"""Integration 域 HTTP 路由（OpenAPI /v1/integration/*）。

作用：薄路由；委托 connector_sdk Studio 内核。
业务关联：Studio Connect→Prove 六步 · STU-02/03/11。
上游：modules/integration/routers
下游：os_core.connector_sdk.connect_test · studio_integration
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.connector_sdk.connect_test import run_connect_test
from os_core.connector_sdk.studio_integration import (
  register_studio_connect,
  run_discover,
  run_prove,
  save_pack_mappings,
  validate_blueprint_payload,
)

router = APIRouter(tags=["Integration"])


class ConnectTestBody(BaseModel):
  """POST /v1/integration/connect/test 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  pack_id: str = Field(description="Connector Pack ID")


class ConnectRegisterBody(BaseModel):
  """POST /v1/integration/connect/register 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  pack_id: str = Field(description="Connector Pack ID")
  lifecycle: str = Field(default="connected", description="关系生命周期")


class DiscoverBody(BaseModel):
  """POST /v1/integration/discover 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  pack_id: str = Field(description="Connector Pack ID")
  openapi_url: str | None = Field(default=None, description="远程 OpenAPI URL")
  sample_paths: list[str] | None = Field(default=None, description="采样路径列表")


class BlueprintValidateBody(BaseModel):
  """POST /v1/integration/blueprint/validate 请求体（ConnectorBlueprint）。"""

  model_config = ConfigDict(extra="allow")

  apiVersion: str | None = None
  kind: str | None = None
  metadata: dict[str, Any] | None = None
  spec: dict[str, Any] | None = None


class MappingsBody(BaseModel):
  """PUT /v1/integration/mappings/{packId} 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  mappings: dict[str, Any] = Field(description="字段映射树")
  secrets_ref: str | None = Field(default=None, description="凭证 Vault 引用")


class ProveRunBody(BaseModel):
  """POST /v1/integration/prove/run 请求体。"""

  model_config = ConfigDict(extra="forbid")

  tenant_id: str = Field(description="租户 ID")
  pack_id: str = Field(description="Connector Pack ID")
  approve_write: bool = Field(default=False, description="是否申请生产写批准")
  approved_by: str | None = Field(default=None, description="批准人 ID")


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


@router.post("/v1/integration/connect/register", status_code=201)
def connect_register_http(
  body: ConnectRegisterBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/integration/connect/register（STU-02 · Registry API 落库）。"""
  result = register_studio_connect(
    session,
    tenant_id=body.tenant_id,
    pack_id=body.pack_id,
    lifecycle=body.lifecycle,
  )
  return result


@router.post("/v1/integration/discover")
def discover_http(
  body: DiscoverBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/integration/discover（STU-02 · CMV 候选发现）。"""
  return run_discover(
    session,
    tenant_id=body.tenant_id,
    pack_id=body.pack_id,
    sample_paths=body.sample_paths,
    openapi_url=body.openapi_url,
  )


@router.post("/v1/integration/blueprint/validate")
def blueprint_validate_http(
  body: BlueprintValidateBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/integration/blueprint/validate（Blueprint 结构校验）。"""
  payload = body.model_dump(exclude_none=True)
  return validate_blueprint_payload(payload)


@router.put("/v1/integration/mappings/{pack_id}")
def save_mappings_http(
  pack_id: str,
  body: MappingsBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """PUT /v1/integration/mappings/{packId}（STU-11 · secrets_ref）。"""
  return save_pack_mappings(
    session,
    tenant_id=body.tenant_id,
    pack_id=pack_id,
    mappings=body.mappings,
    secrets_ref=body.secrets_ref,
  )


@router.post("/v1/integration/prove/run")
def prove_run_http(
  body: ProveRunBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/integration/prove/run（STU-03 · Shadow Prove）。"""
  return run_prove(
    session,
    tenant_id=body.tenant_id,
    pack_id=body.pack_id,
    approve_write=body.approve_write,
    approved_by=body.approved_by,
  )
