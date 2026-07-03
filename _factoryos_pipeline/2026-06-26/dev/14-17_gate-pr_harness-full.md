# Gate 结论：`gate-pr_harness-full`

- 时间(UTC): 2026-06-26T14:17:16Z → 2026-06-26T14:17:16Z
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
OK: no legacy paths under src/
Code redundancy check OK
FactoryOS Harness · full · step stop / CI · 8 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── os_core kernel registry (check_kernel_registry.py)

── api router registry (check_router_registry.py)

── integration GIP registry (check_integration_registry.py)

── legacy path cleanup (check_legacy_paths.py)

── Code redundancy (check_code_redundancy.py)

Harness OK
```

## stderr
```text

```
