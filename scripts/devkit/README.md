# scripts/devkit

FactoryOS **可拔插 DevKit** 实现库。

| 模块 | 用途 |
|------|------|
| [manifest.py](./manifest.py) | 解析 `devkit.manifest.yaml` |
| [run_profiles.py](./run_profiles.py) | 调度各 App `scripts/check_harness.py` |
| [bootstrap_standalone.py](./bootstrap_standalone.py) | standalone 复制 `.cursor` + pipeline |
| [frontend_contract_lib.py](./frontend_contract_lib.py) | 前端 contracts/文件头对账 |
| [sync_frontend_template.py](./sync_frontend_template.py) | web-admin → `templates/frontend-devkit` |
| [check_frontend_template_parity.py](./check_frontend_template_parity.py) | 金样↔模板 parity 门禁（D16） |
| [scaffold_frontend_app.py](./scaffold_frontend_app.py) | 一键创建等权前端 App |

入口：`../scaffold_frontend_app.sh` · `../check_devkit_profiles.py` · 真源文档：`.cursor/factoryos/DEVKIT.md`
