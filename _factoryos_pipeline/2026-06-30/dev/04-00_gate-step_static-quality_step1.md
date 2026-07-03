# Gate 结论：`gate-step_static-quality_step1`

- 时间(UTC): 2026-06-30T04:00:30Z → 2026-06-30T04:00:32Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_static_quality.py`

## stdout
```text

── ruff
[1m[91mE501 [0m[1mLine too long (108 > 100)[0m
  [1m[94m-->[0m src/server/os_core/agent_orchestrator/service.py:60:86
   [1m[94m|[0m
[1m[94m58 |[0m   """产出 DSL 计划（不执行 · 不写 Legacy · 不 import graph/rule 内核）。
[1m[94m59 |[0m
[1m[94m60 |[0m   功能：intent → 单步 GOVERNED_WRITE DslPlan；Graph frozen / Rule 绑定由 **调用方**（API/harness）预先校验。
   [1m[94m|[0m                                                                                                     [1m[91m^^^^^^^^[0m
[1m[94m61 |[0m   业务含义：Harness 确认门的数据载体；确认前 execution 不得被调用。
[1m[94m62 |[0m   上游：POST /v1/agent/plan 薄路由（Step2）
   [1m[94m|[0m

[1m[91mI001 [0m[[1m[96m*[0m] [1mImport block is un-sorted or un-formatted[0m
  [1m[94m-->[0m src/tests/integration/test_agent_orchestrator_w5_step1.py:7:1
   [1m[94m|[0m
[1m[94m 5 |[0m   下游：gate step --step 1 -k 'workflow'
[1m[94m 6 |[0m   """
[1m[94m 7 |[0m [1m[91m/[0m from __future__ import annotations
[1m[94m 8 |[0m [1m[91m|[0m
[1m[94m 9 |[0m [1m[91m|[0m import importlib
[1m[94m10 |[0m [1m[91m|[0m
[1m[94m11 |[0m [1m[91m|[0m import pytest
[1m[94m12 |[0m [1m[91m|[0m from sqlalchemy.orm import Session
[1m[94m13 |[0m [1m[91m|[0m
[1m[94m14 |[0m [1m[91m|[0m from tests.integration.w3_helpers import seed_frozen_env_kernel
   [1m[94m|[0m [1m[91m|_______________________________________________________________^[0m
[1m[94m15 |[0m
[1m[94m16 |[0m   DSL_PLAN_REQUIRED = frozenset({
   [1m[94m|[0m
[1m[96mhelp[0m: [1mOrganize imports[0m

[1m[91mE501 [0m[1mLine too long (130 > 100)[0m
   [1m[94m-->[0m src/tests/integration/test_harness_w5.py:150:101
    [1m[94m|[0m
[1m[94m149 |[0m   event_types = {e.get("event_type") for e in events}
[1m[94m150 |[0m   assert "execute.started" in event_types or "execute.completed" in event_types or "execute.simulated" in event_types, event_types
    [1m[94m|[0m                                                                                                     [1m[91m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1m[94m151 |[0m
[1m[94m152 |[0m   plan_audit = api_client.get(
    [1m[94m|[0m

Found 3 errors.
[[36m*[0m] 1 fixable with the `--fix` option.

── pyright
0 errors, 0 warnings, 0 informations
```

## stderr
```text

Static quality FAILED
```
