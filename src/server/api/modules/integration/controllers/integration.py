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

  apiVersion: str | None = Field(default=None, description="Blueprint API 版本")
  kind: str | None = Field(default=None, description="Blueprint 资源类型")
  metadata: dict[str, Any] | None = Field(default=None, description="Blueprint 元数据")
  spec: dict[str, Any] | None = Field(default=None, description="Blueprint 规格体")


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
  """POST /v1/integration/connect/test（P-03 · Studio Step 1）。

  功能：薄路由委托 connect_test 内核。
  业务含义：Studio Connect 步验证 Pack 可达与 Override 生效。
  下游：connector_sdk.connect_test.run_connect_test。
  """
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
  """POST /v1/integration/connect/register（STU-02 · Registry API 落库）。

  功能：Studio Connect 注册 Pack 到 system_relations。
  业务含义：区别于 bootstrap fixture 的 API 落库真路径。
  下游：studio_integration.register_studio_connect。
  """
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
  """POST /v1/integration/discover（STU-02 · CMV 候选发现）。

  功能：从 Blueprint 推导 CMV verb 候选。
  业务含义：Studio Discover 步零仓库配置入口。
  下游：studio_integration.run_discover。
  """
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
  """POST /v1/integration/blueprint/validate（Blueprint 结构校验）。

  功能：校验 ConnectorBlueprint 结构与 CMV 声明。
  业务含义：Discover/CI 前置；L2 revert 字段合规。
  下游：studio_integration.validate_blueprint_payload。
  """
  payload = body.model_dump(exclude_none=True)
  return validate_blueprint_payload(payload)


@router.put("/v1/integration/mappings/{pack_id}")
def save_mappings_http(
  pack_id: str,
  body: MappingsBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """PUT /v1/integration/mappings/{packId}（STU-11 · secrets_ref）。

  功能：保存字段映射；禁止明文 secret。
  业务含义：Map 步凭证仅存 secrets_ref。
  下游：studio_integration.save_pack_mappings。
  """
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
  """POST /v1/integration/prove/run（STU-03 · Shadow Prove）。

  功能：Contract Test + 对账样例（mock，无 Legacy 真写）。
  业务含义：Shadow 前置；approve_write 默认 false。
  下游：studio_integration.run_prove。
  """
  return run_prove(
    session,
    tenant_id=body.tenant_id,
    pack_id=body.pack_id,
    approve_write=body.approve_write,
    approved_by=body.approved_by,
  )
