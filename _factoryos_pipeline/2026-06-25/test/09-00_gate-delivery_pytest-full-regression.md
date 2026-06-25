# Gate 结论：`gate-delivery_pytest-full-regression`

- 时间(UTC): 2026-06-25T09:00:54Z → 2026-06-25T09:00:55Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python -m pytest src/tests/contract src/tests/workflow src/tests/integration -v --tb=short -m not pending`

## stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 19 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  5%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [ 10%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [ 15%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [ 21%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 26%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 31%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 36%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 42%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 47%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 52%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 57%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 63%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 68%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 73%]
src/tests/integration/test_connector_c01.py::test_C01_connector_health_returns_ok[C-01] PASSED [ 78%]
src/tests/integration/test_scale_s01_s04.py::test_S01_scale_tables_after_migration[S-01] PASSED [ 84%]
src/tests/integration/test_scale_s01_s04.py::test_S02_default_tenant_seed_values[S-02] PASSED [ 89%]
src/tests/integration/test_scale_s01_s04.py::test_S03_tenant_registry_get_cell[S-03] PASSED [ 94%]
src/tests/integration/test_scale_s01_s04.py::test_S04_outbox_port_persists_event[S-04] PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 19 passed, 1 warning in 0.62s =========================
```

## stderr
```text

```
