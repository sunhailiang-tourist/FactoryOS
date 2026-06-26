"""execution_service 执行入口（W2 dry_run · 幂等 · W3 Graph/Rule/DSL 门禁）。

作用：唯一写 Legacy 路径编排；W3 接入 graph freeze · rule evaluate · CMV。
业务关联：E-01～E-09 · G-03 · R-01 · D-02/D-03。
上游：apps/api/routes/execute
下游：graph_service · rule_engine · audit_service · connector_sdk
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from os_core.audit_service.store import append_audit_event, list_audit_events
from os_core.connector_sdk import mock_legacy
from os_core.execution_service.store import (
  find_by_exec_id,
  find_by_idempotency,
  insert_execution_record,
)
from os_core.graph_service import assert_graph_executable
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
)


def execute(session: Session, request: dict[str, Any] | ExecuteRequest) -> ExecutionRecord:
  """执行 DSL 请求（W3：Graph/Rule/DSL 门禁 + dry_run/幂等）。

  功能：校验 frozen · Rule allow · CMV；L0 不写 Legacy；L2 dry_run 不写。
  业务含义：写路径唯一入口；同 idempotency_key 返回同一 exec。
  """
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

  if writes_legacy:
    mock_legacy.mock_legacy_write(pack_id="conn-mock", verb=req.verb)

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
  """组装 ExecutionEvidence（E-09 可重建审计包）。

  功能：聚合 execution_records + audit_events。
  业务含义：合规只读入口；W2 不含 rule_snapshot。
  上游调用方：GET /v1/executions/{execId}/evidence
  参数 exec_id：执行 UUID
  返回：ExecutionEvidence；无记录时 None
  """
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
