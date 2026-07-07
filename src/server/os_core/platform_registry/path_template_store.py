"""Path 模板 Registry（Studio tenant onboard · STU-10）。

作用：加载 path-a/b/c 模板 · 按模板 provision 租户与 Pack 绑定。
业务关联：GET /v1/registry/path-templates · POST /v1/registry/tenants。
上游：integration/catalog/path-templates/*.yaml
下游：tenant_config_store · system_relations
关联文档：docs/文档/架构/配置枢纽与关系模型.md
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.platform_registry import tenant_config_store
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.repo_paths import integration_dir

_PATH_TEMPLATES_DIR = integration_dir() / "catalog" / "path-templates"
_STANDARD_IDS = ("path-a", "path-b", "path-c")


def _load_template_file(path: Path) -> dict[str, Any] | None:
  """读取单个 PathTemplate YAML。"""
  if not path.is_file():
    return None
  raw = yaml.safe_load(path.read_text(encoding="utf-8"))
  return raw if isinstance(raw, dict) else None


def list_path_templates() -> list[dict[str, Any]]:
  """列出标准 path 模板（path-a/b/c）。

  功能：扫描 catalog/path-templates 目录。
  业务含义：Studio 创建 tenant 时选择路径并预填 Pack 组合。
  返回：含 template_id · display_name · packs 的摘要列表。
  """
  templates: list[dict[str, Any]] = []
  if not _PATH_TEMPLATES_DIR.is_dir():
    return templates
  for template_id in _STANDARD_IDS:
    doc = _load_template_file(_PATH_TEMPLATES_DIR / f"{template_id}.yaml")
    if doc is None:
      continue
    meta = doc.get("metadata") or {}
    spec = doc.get("spec") or {}
    packs = spec.get("packs") or []
    templates.append(
      {
        "template_id": str(meta.get("template_id") or template_id),
        "id": str(meta.get("template_id") or template_id),
        "display_name": meta.get("display_name"),
        "path": spec.get("path"),
        "packs": packs,
        "description": spec.get("description"),
      }
    )
  return templates


def get_path_template(template_id: str) -> dict[str, Any] | None:
  """按 template_id 加载 PathTemplate 文档。"""
  doc = _load_template_file(_PATH_TEMPLATES_DIR / f"{template_id}.yaml")
  if doc is None:
    return None
  meta = doc.get("metadata") or {}
  if str(meta.get("template_id") or template_id) != template_id:
    return None
  return doc


def provision_tenant(
  session: Session,
  *,
  tenant_id: str,
  display_name: str,
  path_template_id: str,
) -> dict[str, Any]:
  """POST /v1/registry/tenants — 按 Path 模板开通租户。

  功能：写入 tenant_profiles · 绑定模板 Pack 到 system_relations。
  业务含义：STU-10/ STU-02 Registry 经 API 落库（非手改 tenants/*.yaml）。
  参数 path_template_id：path-a | path-b | path-c
  返回：租户摘要（含 tenant_id · path · packs）
  """
  template = get_path_template(path_template_id)
  if template is None:
    raise PlatformError(
      ErrorCode.VAL_SCHEMA_FAILED,
      f"Unknown path template: {path_template_id}",
      http_status=422,
    )
  spec = template.get("spec") or {}
  path_code = str(spec.get("path") or path_template_id[-1:].upper())
  packs = [str(p) for p in (spec.get("packs") or []) if p]

  tenant_config_store.upsert_tenant_settings(
    session,
    tenant_id=tenant_id,
    shadow_mode=False,
    write_approved=False,
  )
  session.execute(
    text(
      """
      UPDATE tenant_profiles
      SET display_name = :display_name, path = :path
      WHERE tenant_id = :tenant_id
      """
    ),
    {
      "tenant_id": tenant_id,
      "display_name": display_name,
      "path": path_code,
    },
  )

  for pack_id in packs:
    tenant_config_store.ensure_system_relation(
      session,
      tenant_id=tenant_id,
      pack_id=pack_id,
      registry_key=f"path-templates/{path_template_id}",
    )
    tenant_config_store.ensure_pack_entitlement(
      session,
      tenant_id=tenant_id,
      pack_id=pack_id,
    )

  session.commit()
  return {
    "tenant_id": tenant_id,
    "display_name": display_name,
    "path_template_id": path_template_id,
    "path": path_code,
    "packs": packs,
  }


def get_tenant_summary(session: Session, *, tenant_id: str) -> dict[str, Any]:
  """GET /v1/registry/tenants/{tenantId} — 租户摘要。

  功能：返回 OpenAPI 友好字段（非 profile 原始行）。
  业务含义：Studio onboard 后查询开通结果。
  """
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    raise PlatformError(
      ErrorCode.REG_TENANT_NOT_FOUND,
      f"Tenant not found: {tenant_id}",
      http_status=404,
    )
  return {
    "tenant_id": profile["tenant_id"],
    "display_name": profile.get("display_name"),
    "path": profile.get("path"),
    "shadow_mode": bool(profile.get("shadow_mode")),
    "write_approved": bool(profile.get("write_approved")),
  }
