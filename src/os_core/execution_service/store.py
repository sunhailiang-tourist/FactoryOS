"""execution_records 持久化。

作用：ExecutionRecord 落库与幂等查询。
业务关联：E-07 idempotency_key；E-02 snapshot；E-09 evidence 数据源。
上游：execution_service.service
下游：execution_records 表
关联文档：contracts/schemas/执行记录.schema.json
"""
from __future__ import annotations

import json
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.shared_contracts.models.common import Actor
from os_core.shared_contracts.models.execution import ExecutionRecord, LegacyRef


def _parse_json(value: str | None) -> dict | list | None:
  if not value:
    return None
  return json.loads(value)


def _row_to_record(row: dict) -> ExecutionRecord:
  """DB 行 → ExecutionRecord。"""
  actor = Actor.model_validate(json.loads(row["actor_json"]))
  params = json.loads(row["params_json"]) if row.get("params_json") else None
  before_snapshot = _parse_json(row.get("before_snapshot_json"))
  after_snapshot = _parse_json(row.get("after_snapshot_json"))
  legacy_raw = _parse_json(row.get("legacy_refs_json"))
  legacy_refs: list[LegacyRef] | None = None
  if isinstance(legacy_raw, list):
    legacy_refs = [LegacyRef.model_validate(item) for item in legacy_raw]

  return ExecutionRecord(
    exec_id=UUID(row["exec_id"]),
    tenant_id=row["tenant_id"],
    verb=row["verb"],
    status=row["status"],
    graph_id=row["graph_id"],
    graph_version=row["graph_version"],
    actor=actor,
    started_at=datetime.fromisoformat(row["started_at"]),
    scope_id=row.get("scope_id"),
    ruleset_id=row.get("ruleset_id"),
    idempotency_key=row.get("idempotency_key"),
    shadow_mode=bool(row.get("shadow_mode")),
    params=params,
    before_snapshot=before_snapshot if isinstance(before_snapshot, dict) else None,
    after_snapshot=after_snapshot if isinstance(after_snapshot, dict) else None,
    legacy_refs=legacy_refs,
    dry_run=bool(row.get("dry_run")),
    finished_at=(
      datetime.fromisoformat(row["finished_at"]) if row.get("finished_at") else None
    ),
  )


_SELECT_COLUMNS = """
        SELECT exec_id, tenant_id, verb, status, graph_id, graph_version,
               actor_json, started_at, scope_id, ruleset_id, idempotency_key,
               shadow_mode, params_json, before_snapshot_json, after_snapshot_json,
               legacy_refs_json, dry_run, finished_at
"""


def find_by_exec_id(session: Session, exec_id: UUID) -> ExecutionRecord | None:
  """按 exec_id 查单条 ExecutionRecord（E-09 evidence 数据源）。"""
  row = (
    session.execute(
      text(
        f"""
        {_SELECT_COLUMNS}
        FROM execution_records
        WHERE exec_id = :exec_id
        LIMIT 1
        """
      ),
      {"exec_id": str(exec_id)},
    )
    .mappings()
    .first()
  )
  if row is None:
    return None
  return _row_to_record(dict(row))


def find_by_idempotency(
  session: Session,
  *,
  tenant_id: str,
  idempotency_key: str,
) -> ExecutionRecord | None:
  """按 tenant + idempotency_key 查已有执行（E-07）。"""
  row = (
    session.execute(
      text(
        f"""
        {_SELECT_COLUMNS}
        FROM execution_records
        WHERE tenant_id = :tenant_id AND idempotency_key = :key
        LIMIT 1
        """
      ),
      {"tenant_id": tenant_id, "key": idempotency_key},
    )
    .mappings()
    .first()
  )
  if row is None:
    return None
  return _row_to_record(dict(row))


def insert_execution_record(session: Session, record: ExecutionRecord) -> None:
  """INSERT execution_records（单行）。"""
  actor_json = json.dumps(
    record.actor.model_dump(mode="json", exclude_none=True),
    ensure_ascii=False,
  )
  params_json = (
    json.dumps(record.params, ensure_ascii=False) if record.params is not None else None
  )
  before_json = (
    json.dumps(record.before_snapshot, ensure_ascii=False)
    if record.before_snapshot is not None
    else None
  )
  after_json = (
    json.dumps(record.after_snapshot, ensure_ascii=False)
    if record.after_snapshot is not None
    else None
  )
  legacy_json = None
  if record.legacy_refs:
    legacy_json = json.dumps(
      [ref.model_dump(mode="json") for ref in record.legacy_refs],
      ensure_ascii=False,
    )
  session.execute(
    text(
      """
      INSERT INTO execution_records (
        exec_id, tenant_id, verb, status, graph_id, graph_version,
        actor_json, started_at, scope_id, ruleset_id, idempotency_key,
        shadow_mode, params_json, before_snapshot_json, after_snapshot_json,
        legacy_refs_json, dry_run, finished_at
      ) VALUES (
        :exec_id, :tenant_id, :verb, :status, :graph_id, :graph_version,
        :actor_json, :started_at, :scope_id, :ruleset_id, :idempotency_key,
        :shadow_mode, :params_json, :before_snapshot_json, :after_snapshot_json,
        :legacy_refs_json, :dry_run, :finished_at
      )
      """
    ),
    {
      "exec_id": str(record.exec_id),
      "tenant_id": record.tenant_id,
      "verb": record.verb,
      "status": record.status,
      "graph_id": record.graph_id,
      "graph_version": record.graph_version,
      "actor_json": actor_json,
      "started_at": record.started_at.isoformat(),
      "scope_id": record.scope_id,
      "ruleset_id": record.ruleset_id,
      "idempotency_key": record.idempotency_key,
      "shadow_mode": record.shadow_mode,
      "params_json": params_json,
      "before_snapshot_json": before_json,
      "after_snapshot_json": after_json,
      "legacy_refs_json": legacy_json,
      "dry_run": record.dry_run,
      "finished_at": record.finished_at.isoformat() if record.finished_at else None,
    },
  )


def update_execution_status(
  session: Session,
  exec_id: UUID,
  *,
  status: str,
  finished_at: datetime | None = None,
) -> None:
  """更新 execution_records 状态（E-04 revert）。"""
  session.execute(
    text(
      """
      UPDATE execution_records
      SET status = :status,
          finished_at = COALESCE(:finished_at, finished_at)
      WHERE exec_id = :exec_id
      """
    ),
    {
      "exec_id": str(exec_id),
      "status": status,
      "finished_at": finished_at.isoformat() if finished_at else None,
    },
  )
