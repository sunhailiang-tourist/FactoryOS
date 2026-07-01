"""Platform Registry HTTP 路由（ADR-008 · Studio 读真源）。

作用：暴露 contract/pack/tenant Registry 只读 API。
业务关联：Integration Studio · config_change_requests 前置。
上游：FastAPI · get_db_session
下游：platform_registry stores
"""
from __future__ import annotations

from typing import Any

import yaml
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.platform_registry import contract_store, pack_store, tenant_config_store
from os_core.shared_contracts.cmv_registry import register_dsl_verb

router = APIRouter(tags=["Registry"])


class CmvVerbRegisterBody(BaseModel):
  """POST /v1/registry/cmv/verbs 请求体（D-04）。"""

  verb: str = Field(description="CMV 动词名，如 GOVERNED_WRITE")
  level: str = Field(description="L0 / L2 / L3")
  compensator: str | None = Field(default=None, description="L2/L3 补偿动词")
  params_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object"})
  description: str | None = None


@router.post("/v1/registry/cmv/verbs", status_code=201)
def register_cmv_verb_http(body: CmvVerbRegisterBody) -> dict[str, Any]:
  """POST /v1/registry/cmv/verbs — L2 无 compensator 时 422（D-04）。"""
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
  """当前环境绑定的 published contract_set。"""
  set_id = contract_store.get_active_set_id(session, environment=environment)
  if not set_id:
    raise HTTPException(status_code=404, detail="No active contract set")
  return {"set_id": set_id, "environment": environment, "status": "published"}


@router.get("/v1/registry/packs")
def list_packs(session: Session = Depends(get_db_session)) -> list[dict[str, str]]:
  """pack_registry 已发布 Pack 列表（摘要）。"""
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
  """单 Pack Blueprint（解析后 JSON）。"""
  blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
  if blueprint is None:
    raise HTTPException(status_code=404, detail=f"Pack not found: {pack_id}")
  return blueprint


@router.get("/v1/registry/tenants/{tenant_id}/profile")
def get_tenant_profile(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """tenant_profiles 单行。"""
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    raise HTTPException(status_code=404, detail=f"Tenant not found: {tenant_id}")
  return profile


@router.get("/v1/registry/tenants/{tenant_id}/relations")
def list_tenant_relations(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> list[dict[str, Any]]:
  """租户 system_relations（body 解析为对象）。"""
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
  """Registry 灌入与 contract_set 就绪探针。"""
  seeded = contract_store.is_seeded(session)
  set_id = contract_store.get_active_set_id(session) if seeded else None
  return {
    "registry_seeded": seeded,
    "active_contract_set": set_id,
    "status": "ok" if seeded else "empty",
  }
