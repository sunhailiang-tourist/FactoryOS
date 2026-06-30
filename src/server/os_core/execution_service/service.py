"""execution_service 执行入口（W2 dry_run · 幂等 · W3 门禁 · W4 L2 runtime）。

作用：唯一写 Legacy 路径编排；W4 L2 真写经 connector_sdk runtime。
业务关联：E-01～E-09 · G-03 · R-01 · D-02/D-03。
上游：server.api.modules.execution.controllers
下游：graph_service · rule_engine · audit_service · connector_sdk.runtime
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from os_core.audit_service.store import append_audit_event, list_audit_events
from os_core.connector_sdk.runtime.execute import execute_op
from os_core.execution_service.store import (
  find_by_exec_id,
  find_by_idempotency,
  insert_execution_record,
  update_execution_status,
)
from os_core.graph_service import assert_graph_executable
from os_core.license_service import assert_pack_licensed
from os_core.rule_engine import assert_allowed_for_execute
from os_core.rule_engine.store import find_frozen_ruleset_id
from os_core.shared_contracts.cmv_registry import require_known_verb
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.execution import (
  ExecuteRequest,
  ExecutionEvidence,
  ExecutionRecord,
  LegacyRef,
)

DEFAULT_PACK_ID = "conn-mock"


def _runtime_legacy_refs(raw: dict[str, Any]) -> list[LegacyRef]:
  """Runtime dict legacy_refs → OpenAPI LegacyRef 列表。"""
  return [
    LegacyRef(
      system="mock",
      ref_type=str(raw.get("entity_type", "entity")),
      ref_id=str(raw.get("legacy_id") or raw.get("entity_id", "")),
    )
  ]


def execute(session: Session, request: dict[str, Any] | ExecuteRequest) -> ExecutionRecord:
  """执行 DSL 请求（W3 门禁 + W4 L2 runtime 真写）。"""
  req = (
    request
    if isinstance(request, ExecuteRequest)
    else ExecuteRequest.model_validate(request)
  )

  if req.idempotency_key:
    existing = find_by_idempotency(
      session,
      tenant_id=req.tenant_id,
      idempotency_key=req.idempotency_key,
    )
    if existing is not None:
      return existing

  try:
    assert_pack_licensed(tenant_id=req.tenant_id, pack_id=DEFAULT_PACK_ID)
  except PlatformError as exc:
    if exc.code == ErrorCode.MODULE_NOT_LICENSED:
      append_audit_event(
        session=session,
        tenant_id=req.tenant_id,
        event_type=AuditEventType.LICENSE_DENIED,
        actor=req.actor,
        pack_id=DEFAULT_PACK_ID,
        payload={"pack_id": DEFAULT_PACK_ID, "verb": req.verb},
      )
      session.commit()
    raise

  verb_meta = require_known_verb(req.verb)
  verb_level = str(verb_meta["level"])

  assert_graph_executable(
    session,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    verb=req.verb,
    verb_level=verb_level,
  )

  ruleset_id = req.ruleset_id or find_frozen_ruleset_id(
    session,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
  )
  if ruleset_id is None:
    raise PlatformError(
      ErrorCode.RULE_DENIED,
      "No frozen RuleSet bound to this graph version",
      http_status=403,
    )

  rule_result = assert_allowed_for_execute(
    session,
    ruleset_id=ruleset_id,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    verb=req.verb,
    actor=req.actor,
  )

  now = datetime.now(UTC)
  exec_id = uuid4()
  dry_run = req.dry_run
  writes_legacy = verb_level == "L2" and not dry_run
  status: str = "simulated" if dry_run and verb_level == "L2" else "success"

  before_snapshot: dict[str, Any] | None = None
  after_snapshot: dict[str, Any] | None = None
  legacy_refs: list[LegacyRef] | None = None

  if writes_legacy:
    op_result = execute_op(
      pack_id=DEFAULT_PACK_ID,
      tenant_id=req.tenant_id,
      verb=req.verb,
      params=dict(req.params or {}),
      idempotency_key=req.idempotency_key,
    )
    before_snapshot = op_result.get("before_snapshot")
    after_snapshot = op_result.get("after_snapshot")
    raw_refs = op_result.get("legacy_refs")
    if isinstance(raw_refs, dict):
      legacy_refs = _runtime_legacy_refs(raw_refs)

  record = ExecutionRecord(
    exec_id=exec_id,
    tenant_id=req.tenant_id,
    verb=req.verb,
    status=status,  # type: ignore[arg-type]
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    actor=req.actor,
    started_at=now,
    scope_id=req.scope_id,
    ruleset_id=ruleset_id,
    idempotency_key=req.idempotency_key,
    shadow_mode=dry_run,
    params=req.params,
    before_snapshot=before_snapshot,
    after_snapshot=after_snapshot,
    legacy_refs=legacy_refs,
    dry_run=dry_run,
    finished_at=now,
  )
  insert_execution_record(session, record)

  append_audit_event(
    session=session,
    tenant_id=req.tenant_id,
    event_type=AuditEventType.EXECUTE_STARTED,
    actor=req.actor,
    exec_id=exec_id,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    payload={"verb": req.verb, "dry_run": dry_run, "verb_level": verb_level},
  )
  append_audit_event(
    session=session,
    tenant_id=req.tenant_id,
    event_type=(
      AuditEventType.EXECUTE_SIMULATED
      if dry_run and verb_level == "L2"
      else AuditEventType.EXECUTE_COMPLETED
    ),
    actor=req.actor,
    exec_id=exec_id,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    payload={"status": status, "rule": rule_result},
  )

  return record


def assemble_evidence(session: Session, exec_id: UUID) -> ExecutionEvidence | None:
  """组装 ExecutionEvidence（E-09 可重建审计包）。"""
  record = find_by_exec_id(session, exec_id)
  if record is None:
    return None

  events = list_audit_events(
    session=session,
    tenant_id=record.tenant_id,
    exec_id=exec_id,
    limit=500,
  )
  return ExecutionEvidence(
    exec_id=exec_id,
    tenant_id=record.tenant_id,
    execution=record,
    audit_events=events,
    assembled_at=datetime.now(UTC),
  )


def revert_execution(session: Session, exec_id: UUID) -> ExecutionRecord:
  """Revert 已成功的 L2 执行（E-04 · E-05）。

  功能：恢复 Legacy 至 before_snapshot；原记录 status→reverted。
  业务含义：补偿写路径；重复 revert 或 simulated → 409。
  """
  record = find_by_exec_id(session, exec_id)
  if record is None:
    raise PlatformError(
      ErrorCode.REVERT_NOT_ALLOWED,
      f"Execution not found: {exec_id}",
      http_status=404,
    )

  if record.status == "reverted":
    raise PlatformError(
      ErrorCode.REVERT_NOT_ALLOWED,
      "Execution already reverted",
      http_status=409,
    )

  if record.dry_run or record.status == "simulated":
    raise PlatformError(
      ErrorCode.REVERT_NOT_ALLOWED,
      "Cannot revert simulated or dry_run execution",
      http_status=409,
    )

  before = record.before_snapshot
  if not before or not isinstance(before, dict):
    raise PlatformError(
      ErrorCode.REVERT_NOT_ALLOWED,
      "No before_snapshot to revert",
      http_status=409,
    )

  params = record.params or {}
  entity_type = str(before.get("entity_type") or params.get("entity_type", "work_order"))
  entity_id = str(before.get("entity_id") or params.get("entity_id", ""))
  fields = dict(before.get("fields") or {})

  from os_core.connector_sdk import mock_legacy

  mock_legacy.restore_entity(
    entity_type=entity_type,
    entity_id=entity_id,
    fields=fields,
    pack_id=DEFAULT_PACK_ID,
  )

  now = datetime.now(UTC)
  update_execution_status(session, exec_id, status="reverted", finished_at=now)

  append_audit_event(
    session=session,
    tenant_id=record.tenant_id,
    event_type=AuditEventType.EXECUTE_REVERTED,
    actor=record.actor,
    exec_id=exec_id,
    graph_id=record.graph_id,
    graph_version=record.graph_version,
    payload={"reverted_from": record.status},
  )

  updated = find_by_exec_id(session, exec_id)
  assert updated is not None
  return updated
