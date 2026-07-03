# Gate 结论：`gate-pr_deptry`

- 时间(UTC): 2026-06-26T14:02:44Z → 2026-06-26T14:02:44Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_deptry.py`

## stdout
```text

── deptry (DEP001 · declared imports)
  $ /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m deptry src/server src/tests --ignore DEP002,DEP003,DEP004,DEP005 --optional-dependencies-dev-groups dev
```

## stderr
```text
Scanning 169 files...

[1msrc/server/api/application/assemble.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/application/assemble.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/application/factory.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/application/factory.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/middleware/registry.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/middleware/registry.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/middleware/registry.py[m[36m:[m7[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/middleware/registry.py[m[36m:[m8[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/middleware/registry.py[m[36m:[m9[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/registry.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/registry.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/registry.py[m[36m:[m7[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/config/registry.py[m[36m:[m8[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/main.py[m[36m:[m4[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/audit/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/audit/controllers/audit.py[m[36m:[m16[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/audit/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/connectors/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/connectors/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/dsl/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/dsl/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/execution/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/execution/controllers/execute.py[m[36m:[m14[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/execution/controllers/executions.py[m[36m:[m14[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/execution/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/execution/routers.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/graphs/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/graphs/controllers/graphs.py[m[36m:[m13[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/graphs/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/probes/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/probes/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/registry/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/registry/controllers/registry.py[m[36m:[m14[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/registry/controllers/registry_changes.py[m[36m:[m14[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/registry/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/registry/routers.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/rulesets/__init__.py[m[36m:[m2[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/rulesets/controllers/rulesets.py[m[36m:[m14[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/modules/rulesets/routers.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/router/catalog.py[m[36m:[m4[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/router/registry.py[m[36m:[m5[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/server/api/router/v1/registry.py[m[36m:[m7[36m:[m1[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/ac/test_base001_registry.py[m[36m:[m8[36m:[m1[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/conftest.py[m[36m:[m12[36m:[m1[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/conftest.py[m[36m:[m100[36m:[m5[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_dsl_w3.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_dsl_w3.py[m[36m:[m56[36m:[m3[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_execution_e06_e07.py[m[36m:[m58[36m:[m3[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_graph_w3.py[m[36m:[m8[36m:[m1[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_graph_w3.py[m[36m:[m38[36m:[m3[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1msrc/tests/integration/test_graph_w3.py[m[36m:[m138[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_registry_adr008.py[m[36m:[m11[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_registry_adr008.py[m[36m:[m25[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_registry_adr008.py[m[36m:[m38[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_registry_changes_adr008.py[m[36m:[m11[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_registry_changes_adr008.py[m[36m:[m51[36m:[m3[36m:[m [1m[31mDEP001[m 'server' imported but missing from the dependency definitions
[1msrc/tests/integration/test_rule_w3.py[m[36m:[m6[36m:[m1[36m:[m [1m[31mDEP001[m 'tests' imported but missing from the dependency definitions
[1m[31mFound 57 dependency issues.[m

For more information, see the documentation: https://deptry.com/

deptry FAILED — declare deps with: uv add <pkg>  or  uv add --dev <pkg>
```
