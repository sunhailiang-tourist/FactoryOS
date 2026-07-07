"""Integration Studio 内核（Connect · Discover · Map · Prove）。

作用：Studio 六步 API 业务真源；Registry 落库 · Shadow Prove 语义。
业务关联：STU-02/03/11 · POST discover · PUT mappings · POST prove/run。
上游：server.api.modules.integration
下游：platform_registry · connector_sdk.registry
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml
"""
from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.connector_sdk.registry import validate_blueprint
from os_core.platform_registry import pack_store, tenant_config_store
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

_SENSITIVE_KEYS = frozenset({"password", "secret", "api_key", "token", "credential"})


def register_studio_connect(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  lifecycle: str = "connected",
) -> dict[str, Any]:
  """POST /v1/integration/connect/register — Studio Connect 落库。

  功能：写入 Studio 专用 system_relations 行并授权 Pack。
  业务含义：STU-02 Registry 经 API 落库（区别于 bootstrap fixture 行）。
  上游：integration connect/register HTTP
  下游：system_relations · tenant_pack_entitlements
  """
  relation_id = f"rel-studio-{tenant_id}-{pack_id}"[:128]
  body_text = json.dumps(
    {"source": "studio_api", "pack_id": pack_id, "lifecycle": lifecycle},
    ensure_ascii=False,
  )
  existing = session.execute(
    text("SELECT relation_id FROM system_relations WHERE relation_id = :rid LIMIT 1"),
    {"rid": relation_id},
  ).first()
  if existing:
    session.execute(
      text(
        """
        UPDATE system_relations
        SET lifecycle = :lifecycle, body = :body
        WHERE relation_id = :relation_id
        """
      ),
      {
        "relation_id": relation_id,
        "lifecycle": lifecycle,
        "body": body_text,
      },
    )
    created = False
  else:
    session.execute(
      text(
        """
        INSERT INTO system_relations (
          relation_id, tenant_id, pack_id, environment, path, body, lifecycle
        ) VALUES (
          :relation_id, :tenant_id, :pack_id, 'prod', :path, :body, :lifecycle
        )
        """
      ),
      {
        "relation_id": relation_id,
        "tenant_id": tenant_id,
        "pack_id": pack_id,
        "path": f"studio/{pack_id}",
        "body": body_text,
        "lifecycle": lifecycle,
      },
    )
    created = True
  tenant_config_store.ensure_pack_entitlement(
    session,
    tenant_id=tenant_id,
    pack_id=pack_id,
  )
  session.commit()
  return {
    "relation_id": relation_id,
    "tenant_id": tenant_id,
    "pack_id": pack_id,
    "lifecycle": lifecycle,
    "created": created,
  }


def run_discover(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  sample_paths: list[str] | None = None,
  openapi_url: str | None = None,
) -> dict[str, Any]:
  """POST /v1/integration/discover — CMV 候选发现。

  功能：从 Pack Blueprint ops 与 sample_paths 推导 verb 候选。
  业务含义：Studio Discover 步；顾问零仓库配置入口。
  参数 sample_paths：Legacy OpenAPI 采样路径（mock 推导 verb）。
  参数 openapi_url：预留远程 OpenAPI 拉取（本 Step mock）。
  """
  _ = tenant_id, openapi_url
  blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
  candidates: list[dict[str, Any]] = []
  if blueprint:
    ops = (blueprint.get("spec") or {}).get("ops") or []
    for op in ops:
      if not isinstance(op, dict):
        continue
      verb = op.get("verb")
      if not verb:
        continue
      candidates.append(
        {
          "verb": str(verb),
          "confidence": 0.92,
          "suggested_mapping": op.get("mapping") or {},
        }
      )
  for path in sample_paths or []:
    candidates.append(
      {
        "verb": "QUERY_ENTITY",
        "confidence": 0.75,
        "path": path,
        "suggested_mapping": {"entity_type": "work_order"},
      }
    )
  if not candidates:
    raise PlatformError(
      ErrorCode.CONNECTOR_NOT_CONFIGURED,
      f"No discover candidates for pack {pack_id}",
      http_status=404,
    )
  return {
    "pack_id": pack_id,
    "verb_candidates": candidates,
    "verbs": candidates,
    "candidates": candidates,
  }


def validate_blueprint_payload(blueprint: dict[str, Any]) -> dict[str, Any]:
  """POST /v1/integration/blueprint/validate — Blueprint 结构校验。

  功能：复用 connector_sdk.registry.validate_blueprint。
  业务含义：Studio Discover/CI 校验 CMV · L2 revert 声明。
  参数 blueprint：ConnectorBlueprint JSON。
  返回：valid 与 errors 列表。
  """
  result = validate_blueprint(blueprint)
  return {
    "valid": result["valid"],
    "errors": result["errors"],
  }


def _mappings_contain_plaintext_secret(mappings: dict[str, Any]) -> bool:
  """检测 mappings 树中是否含明文凭证字段。"""

  def walk(node: Any) -> bool:
    if isinstance(node, dict):
      for key, value in node.items():
        key_lower = str(key).lower()
        if key_lower in _SENSITIVE_KEYS and isinstance(value, str) and value.strip():
          return True
        if walk(value):
          return True
    elif isinstance(node, list):
      return any(walk(item) for item in node)
    return False

  return walk(mappings)


def _mappings_require_secrets_ref(mappings: dict[str, Any]) -> bool:
  """是否必须提供 secrets_ref（auth/credentials 段 · 非纯字段映射）。"""
  if _mappings_contain_plaintext_secret(mappings):
    return True
  top = {str(k).lower() for k in mappings}
  return bool(top & {"auth", "credentials", "secrets"})


def _strip_sensitive_values(mappings: dict[str, Any]) -> dict[str, Any]:
  """响应侧剔除明文 secret 字段。"""

  def walk(node: Any) -> Any:
    if isinstance(node, dict):
      out: dict[str, Any] = {}
      for key, value in node.items():
        if str(key).lower() in _SENSITIVE_KEYS:
          continue
        out[key] = walk(value)
      return out
    if isinstance(node, list):
      return [walk(item) for item in node]
    return node

  cleaned = walk(mappings)
  return cleaned if isinstance(cleaned, dict) else {}


def save_pack_mappings(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  mappings: dict[str, Any],
  secrets_ref: str | None = None,
) -> dict[str, Any]:
  """PUT /v1/integration/mappings/{packId} — 字段映射落库。

  功能：映射写入 tenant profile_json.pack_mappings；禁止明文 secret。
  业务含义：STU-11 凭证仅存 secrets_ref · 响应不回显明文。
  参数 tenant_id · pack_id · mappings · secrets_ref：落库键与映射树。
  返回：脱敏后的 mappings 与 secrets_ref。
  异常：明文 secret 或缺 secrets_ref → 422。
  """
  if _mappings_contain_plaintext_secret(mappings):
    raise PlatformError(
      ErrorCode.MAPPING_ERROR,
      "Plaintext secrets in mappings are forbidden; use secrets_ref only",
      http_status=422,
    )
  resolved_ref: str | None = (
    str(secrets_ref).strip() if secrets_ref and str(secrets_ref).strip() else None
  )
  if _mappings_require_secrets_ref(mappings) and not resolved_ref:
    raise PlatformError(
      ErrorCode.MAPPING_ERROR,
      "secrets_ref is required for connector credential mappings",
      http_status=422,
    )
  stored_mappings = _strip_sensitive_values(mappings)
  tenant_config_store.save_pack_mapping_config(
    session,
    tenant_id=tenant_id,
    pack_id=pack_id,
    mappings=stored_mappings,
    secrets_ref=resolved_ref,
  )
  session.commit()
  body: dict[str, Any] = {
    "tenant_id": tenant_id,
    "pack_id": pack_id,
    "mappings": stored_mappings,
  }
  if resolved_ref:
    body["secrets_ref"] = resolved_ref
  return body


def run_prove(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  approve_write: bool = False,
  approved_by: str | None = None,
) -> dict[str, Any]:
  """POST /v1/integration/prove/run — Contract Test + 对账样例。

  功能：校验 Pack 已注册并返回 Prove 报告（mock · 无 Legacy 真写）。
  业务含义：STU-03 Shadow 前置；approve_write=false 时不开生产写。
  参数 approve_write：是否在本步申请 write_approved（默认 false）。
  返回：contract_tests · reconciliation · shadow_mode 报告。
  """
  _ = approved_by
  tenant_config_store.assert_pack_configured_for_tenant(
    session,
    tenant_id=tenant_id,
    pack_id=pack_id,
  )
  blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
  verbs: list[str] = []
  if blueprint:
    for op in (blueprint.get("spec") or {}).get("ops") or []:
      if isinstance(op, dict) and op.get("verb"):
        verbs.append(str(op["verb"]))
  if not verbs:
    verbs = ["GOVERNED_WRITE"]
  contract_tests = [{"verb": verb, "passed": True} for verb in verbs]
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  shadow_mode = bool(profile.get("shadow_mode")) if profile else False
  return {
    "status": "passed",
    "contract_tests": contract_tests,
    "reconciliation": {
      "status": "matched",
      "matched_count": len(contract_tests),
      "mismatched_count": 0,
      "samples": [],
    },
    "write_approved": approve_write,
    "shadow_mode": shadow_mode,
  }
