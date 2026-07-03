# Gate 结论：`gate-step_static-quality_step3`

- 时间(UTC): 2026-06-30T06:49:54Z → 2026-06-30T06:49:56Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_static_quality.py`

## stdout
```text

── ruff
[1m[91mF821 [0m[1mUndefined name `Any`[0m
  [1m[94m-->[0m src/server/os_core/reconciliation_service/service.py:28:29
   [1m[94m|[0m
[1m[94m26 |[0m def _entity_from_snapshot(
[1m[94m27 |[0m   record_params: dict | None,
[1m[94m28 |[0m   after_snapshot: dict[str, Any],
   [1m[94m|[0m                             [1m[91m^^^[0m
[1m[94m29 |[0m ) -> tuple[str, str]:
[1m[94m30 |[0m   """从 after_snapshot / params 解析 entity_type · entity_id。"""
   [1m[94m|[0m

Found 1 error.

── pyright
/Users/sunhailiang/hasen-project/FactoryOS/src/server/os_core/reconciliation_service/service.py
  /Users/sunhailiang/hasen-project/FactoryOS/src/server/os_core/reconciliation_service/service.py:28:29 - error: 未定义“Any” (reportUndefinedVariable)
1 error, 0 warnings, 0 informations
```

## stderr
```text

Static quality FAILED
```
