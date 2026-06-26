"""execution_service 执行入口（W2 dry_run · 幂等 · 审计）。

作用：唯一写 Legacy 路径编排；W2 仅 mock 写 + append-only audit。
业务关联：E-03 · E-06 · E-07；POST /v1/execute 薄路由委托本模块。
上游：apps/api/routes/execute
下游：audit_service · connector_sdk.mock_legacy · execution_records
关联文档：contracts/openapi ExecuteRequest · ExecutionRecord
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
from os_core.shared_contracts.models.audit import AuditEventType
from os_core.shared_contracts.models.execution import (
  ExecuteRequest,
  ExecutionEvidence,
  ExecutionRecord,
)


def execute(session: Session, request: dict[str, Any] | ExecuteRequest) -> ExecutionRecord:
  """执行 DSL 请求（W2：dry_run/幂等/mock Legacy）。

  功能：落 ExecutionRecord + audit；dry_run 不写 Legacy。
  业务含义：写路径唯一入口；同 idempotency_key 返回同一 exec。
  上游调用方：POST /v1/execute 路由、integration E-06/E-07
  参数 request：ExecuteRequest 或等价 dict
  返回：ExecutionRecord
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

  now = datetime.now(UTC)
  exec_id = uuid4()
  dry_run = req.dry_run
  status: str = "simulated" if dry_run else "success"

  if not dry_run:
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
    ruleset_id=req.ruleset_id,
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
    payload={"verb": req.verb, "dry_run": dry_run},
  )
  append_audit_event(
    session=session,
    tenant_id=req.tenant_id,
    event_type=(
      AuditEventType.EXECUTE_SIMULATED if dry_run else AuditEventType.EXECUTE_COMPLETED
    ),
    actor=req.actor,
    exec_id=exec_id,
    graph_id=req.graph_id,
    graph_version=req.graph_version,
    payload={"status": status},
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
