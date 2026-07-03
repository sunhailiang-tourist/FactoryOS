# Gate 结论：`gate-pr_harness-full`

- 时间(UTC): 2026-06-29T08:17:27Z → 2026-06-29T08:17:43Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
OK: kernel registry aligned (10 modules)
OK: router registry aligned (8 providers)
OK: integration registry aligned
OK: no legacy paths (snapshot forbidden list clean)
OK: repo-structure snapshot aligned (v1 · 10 kernel modules · decision D13)
OK: 项目结构与快照一致 (v1 · 10 kernel · D13)
audit_path_consistency: read=6368 forbidden_hits=0
OK: no forbidden filesystem path refs in scope (snapshot-driven)
Code redundancy check OK
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

Harness OK
```

## stderr
```text

```
