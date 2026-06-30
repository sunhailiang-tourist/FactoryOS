"""reconciliation_service 对账编排（W6 stub · mock_legacy read-back）。

作用：run_reconciliation 比对 ExecutionRecord 与 Legacy snapshot。
业务关联：K-01 无 drift · K-02 drift_detected。
上游：server/api POST /v1/reconciliation/run（Step4）
下游：execution_service.store · connector_sdk.mock_legacy
关联文档：Shadow-Mode与对账规格 §2.2
"""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from os_core.connector_sdk import mock_legacy
from os_core.execution_service.store import list_success_legacy_writes
from os_core.shared_contracts.models.reconciliation import (
  ReconciliationDrift,
  ReconciliationReport,
)

_RECONCILE_PATH = "A"


def _entity_from_snapshot(
  record_params: dict | None,
  after_snapshot: dict,
) -> tuple[str, str]:
  """从 after_snapshot / params 解析 entity_type · entity_id。"""
  params = record_params or {}
  entity_type = str(
    after_snapshot.get("entity_type") or params.get("entity_type") or "work_order"
  )
  entity_id = str(after_snapshot.get("entity_id") or params.get("entity_id") or "")
  return entity_type, entity_id


def _compare_fields(
  *,
  exec_id: UUID,
  entity_type: str,
  entity_id: str,
  expected_fields: dict,
  actual_fields: dict,
) -> list[ReconciliationDrift]:
  """逐字段比对 after_snapshot vs Legacy read-back。"""
  drifts: list[ReconciliationDrift] = []
  legacy_ref = f"{entity_type}/{entity_id}"
  for field in sorted(set(expected_fields) | set(actual_fields)):
    expected = expected_fields.get(field)
    actual = actual_fields.get(field)
    if expected != actual:
      drifts.append(
        ReconciliationDrift(
          exec_id=exec_id,
          legacy_ref=legacy_ref,
          system="mock",
          field=field,
          expected=expected,
          actual=actual,
        )
      )
  return drifts


def run_reconciliation(
  session: Session,
  *,
  tenant_id: str,
  scope: str = "ad_hoc",
  graph_id: str | None = None,
  since: datetime | None = None,
) -> ReconciliationReport:
  """对账 Job 内核：read-back mock Legacy 并产出 ReconciliationReport。

  功能：遍历 success L2 写，比对 after_snapshot.fields 与 Legacy。
  业务含义：K-01 无 drift → status=ok；篡改后 → drift_detected。
  上游：API 路由或集成测试直接调用
  参数 tenant_id/scope/graph_id/since：对账范围
  返回：ReconciliationReport（Pydantic）
  """
  started_at = datetime.now(UTC)
  run_id = uuid4()
  scope_val: str = scope if scope in ("daily", "ad_hoc") else "ad_hoc"

  records = list_success_legacy_writes(
    session,
    tenant_id=tenant_id,
    graph_id=graph_id,
    since=since,
  )

  drifts: list[ReconciliationDrift] = []
  records_checked = 0
  records_skipped_shadow = 0

  for record in records:
    if record.dry_run or record.shadow_mode or record.status != "success":
      records_skipped_shadow += 1
      continue
    after = record.after_snapshot
    if not isinstance(after, dict):
      continue

    records_checked += 1
    entity_type, entity_id = _entity_from_snapshot(record.params, after)
    expected_fields = dict(after.get("fields") or {})

    actual_entity = mock_legacy.get_entity(entity_type=entity_type, entity_id=entity_id)
    actual_fields = dict(actual_entity.get("fields") or {})

    drifts.extend(
      _compare_fields(
        exec_id=record.exec_id,
        entity_type=entity_type,
        entity_id=entity_id,
        expected_fields=expected_fields,
        actual_fields=actual_fields,
      )
    )

  finished_at = datetime.now(UTC)
  status = "drift_detected" if drifts else "ok"

  return ReconciliationReport(
    run_id=run_id,
    tenant_id=tenant_id,
    scope=scope_val,  # type: ignore[arg-type]
    graph_id=graph_id,
    since=since,
    started_at=started_at,
    finished_at=finished_at,
    status=status,
    records_checked=records_checked,
    records_skipped_shadow=records_skipped_shadow,
    path=_RECONCILE_PATH,
    drifts=drifts,
  )
