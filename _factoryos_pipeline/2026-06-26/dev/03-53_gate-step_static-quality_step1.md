# Gate 结论：`gate-step_static-quality_step1`

- 时间(UTC): 2026-06-26T03:53:22Z → 2026-06-26T03:53:27Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_static_quality.py`

## stdout
```text

── ruff
E501 Line too long (101 > 100)
  --> src/tests/workflow/test_plan_gate_absolute.py:43:101
   |
41 |   try:
42 |     r = subprocess.run(
43 |       [sys.executable, str(ROOT / "scripts" / "check_pipeline.py"), "--gate", "step", "--step", "1"],
   |                                                                                                     ^
44 |       cwd=ROOT,
45 |       capture_output=True,
   |

E501 Line too long (102 > 100)
  --> src/tests/workflow/test_step_chain_gate.py:15:101
   |
14 | @pytest.mark.workflow
15 | def test_step_chain_requires_dev_before_test(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
   |                                                                                                     ^^
16 |   sys.path.insert(0, str(SCRIPTS))
17 |   import step_chain_lib
   |

E501 Line too long (110 > 100)
  --> src/tests/workflow/test_step_chain_gate.py:28:101
   |
27 | @pytest.mark.workflow
28 | def test_step_chain_closed_needs_all_three_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
   |                                                                                                     ^^^^^^^^^^
29 |   sys.path.insert(0, str(SCRIPTS))
30 |   import plan_gate_lib
   |

F541 [*] f-string without any placeholders
  --> src/tests/workflow/test_step_chain_gate.py:37:14
   |
35 |   (plan_dir / "test").mkdir()
36 |   (plan_dir / "verify").mkdir()
37 |   plan_rel = f"_factoryos_pipeline/2026-06-99/plan/plan-test.md"
   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |   (plan_dir / "plan").mkdir()
39 |   (plan_dir / "plan" / "plan-test.md").write_text("# plan\n", encoding="utf-8")
   |
help: Remove extraneous `f` prefix

Found 4 errors.
[*] 1 fixable with the `--fix` option.

── pyright
/Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_plan_gate_absolute.py
  /Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_plan_gate_absolute.py:18:10 - error: Import "plan_gate_lib" could not be resolved (reportMissingImports)
/Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_step_chain_gate.py
  /Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_step_chain_gate.py:17:10 - error: Import "step_chain_lib" could not be resolved (reportMissingImports)
  /Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_step_chain_gate.py:30:10 - error: Import "plan_gate_lib" could not be resolved (reportMissingImports)
  /Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_step_chain_gate.py:31:10 - error: Import "step_chain_lib" could not be resolved (reportMissingImports)
  /Users/sunhailiang/hasen-project/FactoryOS/src/tests/workflow/test_step_chain_gate.py:60:10 - error: Import "step_chain_lib" could not be resolved (reportMissingImports)
5 errors, 0 warnings, 0 informations
```

## stderr
```text

Static quality FAILED
```
