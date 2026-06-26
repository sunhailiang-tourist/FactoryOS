# Gate 结论：`gate-step_harness-full_step4`

- 时间(UTC): 2026-06-26T03:13:15Z → 2026-06-26T03:13:16Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest E-09`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
Code redundancy check OK
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
testpaths: src/tests
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 72 items / 71 deselected / 1 selected

src/tests/integration/test_execution_e09.py::test_E09_execution_evidence_rebuildable[E-09] PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= 1 passed, 71 deselected, 1 warning in 0.51s ==================
FactoryOS Harness · full · step stop / CI · 4 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── Code redundancy (check_code_redundancy.py)

── pytest -k 'E-09'

Harness OK
```

## stderr
```text

```
