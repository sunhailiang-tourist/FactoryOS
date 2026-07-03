# Gate 结论：`gate-step_harness-full_step4`

- 时间(UTC): 2026-06-30T07:09:05Z → 2026-06-30T07:09:20Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest K-02`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
OK: kernel registry aligned (11 modules)
OK: router registry aligned (11 providers)
OK: integration registry aligned
OK: no legacy paths (snapshot forbidden list clean)
OK: repo-structure snapshot aligned (v1 · 11 kernel modules · decision D14)
OK: 项目结构与快照一致 (v1 · 11 kernel · D14)
audit_path_consistency: read=6594 forbidden_hits=0
OK: no forbidden filesystem path refs in scope (snapshot-driven)
Code redundancy check OK
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
testpaths: src/tests
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 100 items / 99 deselected / 1 selected

src/tests/integration/test_reconciliation_w6.py::test_K02_reconciliation_http_detects_drift_after_tamper[K-02] PASSED [100%]

======================= 1 passed, 99 deselected in 0.41s =======================
Harness python: /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python (project .venv)
FactoryOS Harness · full · step stop / CI · 11 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── os_core kernel registry (check_kernel_registry.py)

── api router registry (check_router_registry.py)

── integration GIP registry (check_integration_registry.py)

── legacy path cleanup (check_legacy_paths.py)

── repo-structure snapshot sync (check_repo_structure.py)

── structure drift gate (check_structure_change.py)

── docs path consistency (audit_path_consistency.py)

── Code redundancy (check_code_redundancy.py)

── pytest -k 'K-02'

Harness OK
```

## stderr
```text

```
