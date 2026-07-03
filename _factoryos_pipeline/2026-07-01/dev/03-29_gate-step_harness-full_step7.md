# Gate 结论：`gate-step_harness-full_step7`

- 时间(UTC): 2026-07-01T03:29:25Z → 2026-07-01T03:29:40Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest N-01`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
OK: kernel registry aligned (13 modules)
OK: router registry aligned (15 providers)
OK: integration registry aligned
Registry annotations OK
OK: no legacy paths (snapshot forbidden list clean)
OK: repo-structure snapshot aligned (v1 · 13 kernel modules · decision D14)
OK: 项目结构与快照一致 (v1 · 13 kernel · D14)
audit_path_consistency: read=6775 forbidden_hits=0
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
collecting ... collected 108 items / 107 deselected / 1 selected

src/tests/integration/test_negative_w7.py::test_N01_no_internal_execute_bypass_endpoint[N-01] PASSED [100%]

====================== 1 passed, 107 deselected in 0.41s =======================
Harness python: /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python (project .venv)
FactoryOS Harness · full · step stop / CI · 12 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── os_core kernel registry (check_kernel_registry.py)

── api router registry (check_router_registry.py)

── integration GIP registry (check_integration_registry.py)

── Registry annotations (check_registry_annotations.py)

── legacy path cleanup (check_legacy_paths.py)

── repo-structure snapshot sync (check_repo_structure.py)

── structure drift gate (check_structure_change.py)

── docs path consistency (audit_path_consistency.py)

── Code redundancy (check_code_redundancy.py)

── pytest -k 'N-01'

Harness OK
```

## stderr
```text

```
