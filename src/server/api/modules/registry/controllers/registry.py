"""Platform Registry HTTP 路由（ADR-008 · Studio 读真源）。

作用：暴露 contract/pack/tenant Registry 只读 API。
业务关联：Integration Studio · config_change_requests 前置。
上游：FastAPI · get_db_session
下游：platform_registry stores
"""
from __future__ import annotations

from typing import Any

import yaml
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.platform_registry import (
  contract_store,
  pack_store,
  path_template_store,
  tenant_config_store,
)
from os_core.shared_contracts.cmv_registry import register_dsl_verb
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

router = APIRouter(tags=["Registry"])


class CmvVerbRegisterBody(BaseModel):
  """POST /v1/registry/cmv/verbs 请求体（D-04）。"""

  verb: str = Field(description="CMV 动词名，如 GOVERNED_WRITE")
  level: str = Field(description="L0 / L2 / L3")
  compensator: str | None = Field(default=None, description="L2/L3 补偿动词")
  params_schema: dict[str, Any] = Field(
    default_factory=lambda: {"type": "object"},
    description="动词参数 JSON Schema",
  )
  description: str | None = Field(default=None, description="动词业务说明")


class TenantProvisionBody(BaseModel):
  """POST /v1/registry/tenants 请求体（STU-10 onboard）。"""

  tenant_id: str = Field(description="新租户 ID")
  display_name: str = Field(description="展示名")
  path_template_id: str = Field(description="path-a | path-b | path-c")


@router.get("/v1/registry/path-templates")
def list_path_templates_http() -> list[dict[str, Any]]:
  """GET /v1/registry/path-templates — path-a/b/c 标准模板。

  功能：列出 Path 开通模板摘要。
  业务含义：STU-10 Studio onboard 选路。
  下游：path_template_store.list_path_templates。
  """
  return path_template_store.list_path_templates()


@router.post("/v1/registry/tenants", status_code=201)
def provision_tenant_http(
  body: TenantProvisionBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """POST /v1/registry/tenants — 按 Path 模板开通租户（STU-10）。

  功能：按模板写入 tenant 与 Pack 绑定。
  业务含义：顾问 API 开通租户，非手改 YAML。
  下游：path_template_store.provision_tenant。
  """
  return path_template_store.provision_tenant(
    session,
    tenant_id=body.tenant_id,
    display_name=body.display_name,
    path_template_id=body.path_template_id,
  )


@router.get("/v1/registry/tenants/{tenant_id}")
def get_tenant_summary_http(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/registry/tenants/{tenantId} — 租户摘要（STU-10）。

  功能：返回 onboard 后租户摘要字段。
  业务含义：Studio 确认开通结果。
  下游：path_template_store.get_tenant_summary。
  """
  return path_template_store.get_tenant_summary(session, tenant_id=tenant_id)


@router.post("/v1/registry/cmv/verbs", status_code=201)
def register_cmv_verb_http(body: CmvVerbRegisterBody) -> dict[str, Any]:
  """POST /v1/registry/cmv/verbs — L2 无 compensator 时 422（D-04）。

  功能：运行时注册 DSL verb 元数据。
  业务含义：Discover 扩展动词；L2 须 compensator。
  下游：cmv_registry.register_dsl_verb。
  """
  return register_dsl_verb(
    verb=body.verb,
    level=body.level,
    compensator=body.compensator,
    params_schema=body.params_schema,
    description=body.description,
  )


@router.get("/v1/registry/contract-set/active")
def get_active_contract_set(
  session: Session = Depends(get_db_session),
  environment: str = "prod",
) -> dict[str, Any]:
  """当前环境绑定的 published contract_set。

  功能：查询 active contract_set ID。
  业务含义：Integration 读契约真源就绪探针。
  参数 environment：默认 prod。
  返回：set_id 与 status。
  异常: PlatformError · REG_NO_ACTIVE_CONTRACT 等
  """
  set_id = contract_store.get_active_set_id(session, environment=environment)
  if not set_id:
    raise PlatformError(
      ErrorCode.REG_NO_ACTIVE_CONTRACT,
      "No active contract set",
      http_status=404,
    )
  return {"set_id": set_id, "environment": environment, "status": "published"}


@router.get("/v1/registry/packs")
def list_packs(session: Session = Depends(get_db_session)) -> list[dict[str, str]]:
  """pack_registry 已发布 Pack 列表（摘要）。

  功能：SQL 查询 pack_registry 摘要行。
  业务含义：Studio 选 Pack · Registry 浏览。
  返回：pack_id · registry_key · certification_level。
  """
  from sqlalchemy import text

  rows = session.execute(
    text(
      """
      SELECT pack_id, registry_key, certification_level, status
      FROM pack_registry ORDER BY pack_id
      """
    ),
  ).mappings()
  return [dict(r) for r in rows]


@router.get("/v1/registry/packs/{pack_id}")
def get_pack(pack_id: str, session: Session = Depends(get_db_session)) -> dict[str, Any]:
  """单 Pack Blueprint（解析后 JSON）。

  功能：加载并返回 Pack Blueprint dict。
  业务含义：Discover/Prove 读 Pack 规格真源。
  下游：pack_store.get_pack_blueprint。
  异常: PlatformError · REG_PACK_NOT_FOUND 等
  """
  blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
  if blueprint is None:
    raise PlatformError(
      ErrorCode.REG_PACK_NOT_FOUND,
      f"Pack not found: {pack_id}",
      http_status=404,
    )
  return blueprint


@router.get("/v1/registry/tenants/{tenant_id}/profile")
def get_tenant_profile(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """tenant_profiles 单行。

  功能：Registry 读租户 profile 原始行。
  业务含义：Studio/实施查看 Shadow · pack_mappings。
  下游：tenant_config_store.get_tenant_profile。
  异常: PlatformError · REG_TENANT_NOT_FOUND 等
  """
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    raise PlatformError(
      ErrorCode.REG_TENANT_NOT_FOUND,
      f"Tenant not found: {tenant_id}",
      http_status=404,
    )
  return profile


@router.get("/v1/registry/tenants/{tenant_id}/relations")
def list_tenant_relations(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> list[dict[str, Any]]:
  """租户 system_relations（body 解析为对象）。

  功能：列出 relation 并将 body YAML 解析为 document。
  业务含义：Studio 查看 Connector 绑定详情。
  下游：tenant_config_store.list_system_relations。
  """
  rows = tenant_config_store.list_system_relations(session, tenant_id=tenant_id)
  out: list[dict[str, Any]] = []
  for row in rows:
    item = dict(row)
    body = item.pop("body", None)
    if isinstance(body, str):
      parsed = yaml.safe_load(body)
      item["document"] = parsed if isinstance(parsed, dict) else {"raw": body}
    out.append(item)
  return out


@router.get("/v1/registry/health")
def registry_health(session: Session = Depends(get_db_session)) -> dict[str, Any]:
  """Registry 灌入与 contract_set 就绪探针。

  功能：检查 seed 状态与 active contract_set。
  业务含义：部署/CI 健康检查；未 seed 时 status=empty。
  返回：registry_seeded · active_contract_set · status。
  """
  seeded = contract_store.is_seeded(session)
  set_id = contract_store.get_active_set_id(session) if seeded else None
  return {
    "registry_seeded": seeded,
    "active_contract_set": set_id,
    "status": "ok" if seeded else "empty",
  }
