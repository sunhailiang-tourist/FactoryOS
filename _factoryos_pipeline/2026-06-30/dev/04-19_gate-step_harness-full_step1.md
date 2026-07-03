# Gate 结论：`gate-step_harness-full_step1`

- 时间(UTC): 2026-06-30T04:18:47Z → 2026-06-30T04:19:17Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest workflow`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
OK: kernel registry aligned (10 modules)
OK: router registry aligned (8 providers)
OK: integration registry aligned
OK: no legacy paths (snapshot forbidden list clean)
OK: repo-structure snapshot aligned (v1 · 10 kernel modules · decision D14)
OK: 项目结构与快照一致 (v1 · 10 kernel · D14)
audit_path_consistency: read=6426 forbidden_hits=0
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
collecting ... collected 98 items / 73 deselected / 25 selected

src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [  4%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [  8%]
src/tests/integration/test_agent_orchestrator_w5_step1.py::test_w5_step1_create_plan_stub_returns_dsl_plan[workflow] PASSED [ 12%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 16%]
src/tests/workflow/test_plan_gate_absolute.py::test_plan_gate_lib_validate_detects_missing_plan_ok PASSED [ 20%]
src/tests/workflow/test_plan_gate_absolute.py::test_check_pipeline_step_enforces_plan_absolute_gate PASSED [ 24%]
src/tests/workflow/test_plan_gate_absolute.py::test_workflow_state_documents_plan_absolute_gate PASSED [ 28%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 32%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 36%]
src/tests/workflow/test_registry_harness.py::test_kernel_registry_harness_green PASSED [ 40%]
src/tests/workflow/test_registry_harness.py::test_router_registry_harness_green PASSED [ 44%]
src/tests/workflow/test_registry_harness.py::test_main_has_no_include_router PASSED [ 48%]
src/tests/workflow/test_registry_harness.py::test_os_core_registry_lists_ten_modules PASSED [ 52%]
src/tests/workflow/test_registry_harness.py::test_integration_registry_harness_green PASSED [ 56%]
src/tests/workflow/test_registry_harness.py::test_legacy_paths_harness_green PASSED [ 60%]
src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green PASSED [ 64%]
src/tests/workflow/test_registry_harness.py::test_path_consistency_harness_green PASSED [ 68%]
src/tests/workflow/test_registry_harness.py::test_structure_change_gate_green PASSED [ 72%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_requires_dev_before_test PASSED [ 76%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_closed_needs_all_three_artifacts PASSED [ 80%]
src/tests/workflow/test_step_chain_gate.py::test_can_start_step2_blocked_without_step1_chain PASSED [ 84%]
src/tests/workflow/test_step_chain_gate.py::test_check_pipeline_step_uses_plan_scoped_chain SKIPPED [ 88%]
src/tests/workflow/test_step_chain_gate.py::test_workflow_state_documents_step_chain_gate PASSED [ 92%]
src/tests/workflow/test_structure_commit_gate.py::test_staged_paths_ignore_os_core_root_files_via_script PASSED [ 96%]
src/tests/workflow/test_structure_commit_gate.py::test_structure_check_manual_mode_green PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========== 24 passed, 1 skipped, 73 deselected, 1 warning in 15.11s ===========
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

── pytest -k 'workflow'

Harness OK
```

## stderr
```text

```
