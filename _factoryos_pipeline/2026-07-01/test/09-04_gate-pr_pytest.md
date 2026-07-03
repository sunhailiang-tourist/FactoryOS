# Gate 结论：`gate-pr_pytest`

- 时间(UTC): 2026-07-01T09:04:19Z → 2026-07-01T09:04:36Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m pytest src/tests/contract src/tests/workflow -v --tb=short`

## stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 50 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  2%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [  4%]
src/tests/contract/test_openapi_contract.py::test_openapi_w5_agent_harness_paths PASSED [  6%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [  8%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [ 10%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 12%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 14%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 16%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 18%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 20%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 22%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 24%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_parses_w3c_segment[lowercase-flags] PASSED [ 26%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_parses_w3c_segment[uppercase-flags] PASSED [ 28%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_rejects_invalid[empty] PASSED [ 30%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_rejects_invalid[garbage] PASSED [ 32%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_rejects_invalid[short-trace-id] PASSED [ 34%]
src/tests/contract/test_trace_context.py::test_trace_id_from_traceparent_rejects_invalid[none] PASSED [ 36%]
src/tests/contract/test_trace_context.py::test_trace_id_from_mcp_meta_reads_traceparent_key PASSED [ 38%]
src/tests/contract/test_trace_context.py::test_trace_id_from_mcp_meta_ignores_non_dict PASSED [ 40%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 42%]
src/tests/workflow/test_plan_gate_absolute.py::test_validate_plan_stamp_requires_plan_ok PASSED [ 44%]
src/tests/workflow/test_plan_gate_absolute.py::test_validate_src_test_write_blocked_without_plan_ok PASSED [ 46%]
src/tests/workflow/test_plan_gate_absolute.py::test_validate_code_stamp_requires_code_ok PASSED [ 48%]
src/tests/workflow/test_plan_gate_absolute.py::test_workflow_state_can_test_blocked_without_plan_ok PASSED [ 50%]
src/tests/workflow/test_plan_gate_absolute.py::test_write_plan_gate_invalidates_downstream_stamps PASSED [ 52%]
src/tests/workflow/test_plan_gate_absolute.py::test_check_pipeline_step_enforces_plan_absolute_gate PASSED [ 54%]
src/tests/workflow/test_plan_gate_absolute.py::test_workflow_state_documents_plan_absolute_gate PASSED [ 56%]
src/tests/workflow/test_plan_gate_absolute.py::test_protect_paths_hook_module_documents_stamps PASSED [ 58%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 60%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 62%]
src/tests/workflow/test_registry_harness.py::test_kernel_registry_harness_green PASSED [ 64%]
src/tests/workflow/test_registry_harness.py::test_router_registry_harness_green PASSED [ 66%]
src/tests/workflow/test_registry_harness.py::test_main_has_no_include_router PASSED [ 68%]
src/tests/workflow/test_registry_harness.py::test_os_core_registry_lists_kernel_modules PASSED [ 70%]
src/tests/workflow/test_registry_harness.py::test_registry_annotations_harness_green PASSED [ 72%]
src/tests/workflow/test_registry_harness.py::test_api_router_domains_have_usage_metadata PASSED [ 74%]
src/tests/workflow/test_registry_harness.py::test_kernel_modules_have_usage_metadata PASSED [ 76%]
src/tests/workflow/test_registry_harness.py::test_integration_registry_harness_green PASSED [ 78%]
src/tests/workflow/test_registry_harness.py::test_legacy_paths_harness_green PASSED [ 80%]
src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green PASSED [ 82%]
src/tests/workflow/test_registry_harness.py::test_path_consistency_harness_green PASSED [ 84%]
src/tests/workflow/test_registry_harness.py::test_structure_change_gate_green PASSED [ 86%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_requires_dev_before_test PASSED [ 88%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_closed_needs_all_three_artifacts PASSED [ 90%]
src/tests/workflow/test_step_chain_gate.py::test_can_start_step2_blocked_without_step1_chain PASSED [ 92%]
src/tests/workflow/test_step_chain_gate.py::test_check_pipeline_step_uses_plan_scoped_chain SKIPPED [ 94%]
src/tests/workflow/test_step_chain_gate.py::test_workflow_state_documents_step_chain_gate PASSED [ 96%]
src/tests/workflow/test_structure_commit_gate.py::test_staged_paths_ignore_os_core_root_files_via_script PASSED [ 98%]
src/tests/workflow/test_structure_commit_gate.py::test_structure_check_manual_mode_green PASSED [100%]

======================== 49 passed, 1 skipped in 16.06s ========================
```

## stderr
```text

```
