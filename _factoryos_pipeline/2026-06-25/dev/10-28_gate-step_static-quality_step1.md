# Gate 结论：`gate-step_static-quality_step1`

- 时间(UTC): 2026-06-25T10:28:48Z → 2026-06-25T10:28:51Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_static_quality.py`

## stdout
```text

── ruff
[1m[91mUP017 [0m[[1m[96m*[0m] [1mUse `datetime.UTC` alias[0m
  [1m[94m-->[0m src/os_core/audit_service/store.py:57:38
   [1m[94m|[0m
[1m[94m55 |[0m   """
[1m[94m56 |[0m   event_id = uuid4()
[1m[94m57 |[0m   when = occurred_at or datetime.now(timezone.utc)
   [1m[94m|[0m                                      [1m[91m^^^^^^^^^^^^[0m
[1m[94m58 |[0m   exec_uuid = _parse_exec_id(exec_id)
[1m[94m59 |[0m   plan_uuid = _parse_exec_id(plan_id) if plan_id is not None else None
   [1m[94m|[0m
[1m[96mhelp[0m: [1mConvert to `datetime.UTC` alias[0m

[1m[91mI001 [0m[[1m[96m*[0m] [1mImport block is un-sorted or un-formatted[0m
  [1m[94m-->[0m src/tests/integration/test_audit_e03.py:7:1
   [1m[94m|[0m
[1m[94m 5 |[0m   下游：gate step --step 2 -k 'E-03'
[1m[94m 6 |[0m   """
[1m[94m 7 |[0m [1m[91m/[0m from __future__ import annotations
[1m[94m 8 |[0m [1m[91m|[0m
[1m[94m 9 |[0m [1m[91m|[0m import importlib
[1m[94m10 |[0m [1m[91m|[0m
[1m[94m11 |[0m [1m[91m|[0m import pytest
[1m[94m12 |[0m [1m[91m|[0m from fastapi.testclient import TestClient
[1m[94m13 |[0m [1m[91m|[0m from sqlalchemy import inspect
   [1m[94m|[0m [1m[91m|______________________________^[0m
   [1m[94m|[0m
[1m[96mhelp[0m: [1mOrganize imports[0m

Found 2 errors.
[[36m*[0m] 2 fixable with the `--fix` option.

── pyright
0 errors, 0 warnings, 0 informations
```

## stderr
```text

Static quality FAILED
```
