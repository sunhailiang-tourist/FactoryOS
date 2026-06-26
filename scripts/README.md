# scripts · 脚本目录

> FactoryOS 仓库根 **`scripts/`** 唯一真源（CI · SH-步步流 Harness · docs_baseline · guide 调试 CLI）。  
> 研发工作流：[`.cursor/factoryos/PRE-DEV-CHAIN.md`](../.cursor/factoryos/PRE-DEV-CHAIN.md) · [SH-步步流](../.cursor/factoryos/SH-步步流.md)  
> **对外实施主路径** = Integration Studio（管理台 UI），见 [UI-FIRST-CONFIG-PRINCIPLE](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)。

---

## 新人 30 秒

| 我想… | 命令 / 入口 |
|--------|-------------|
| **激活开发环境（首仓/新机器）** | [README §激活](../README.md#激活开发环境) · `./scripts/activate_dev_env.sh` |
| **接入/扩展（实施/客户）** | **Integration Studio**（`src/apps/web-admin`）— 见 [INTEGRATION-CHAIN](../.cursor/factoryos/INTEGRATION-CHAIN.md) |
| 平台研发：本地跑 CI 同款检查 | `./scripts/harness` 或 `./scripts/factoryos harness` |
| 平台研发：调试 flows 状态机 | `./scripts/factoryos guide`（**非实施主路径**） |
| 看有哪些接入链路（调试） | `./scripts/factoryos guide list` |
| 改契约后自检 | `./scripts/harness --tier contracts` |
| 改 `src/server/os_core` 后自检 | `./scripts/harness --tier auto` |
| 更新架构图 PNG/SVG | `uv run python scripts/generate_all_diagrams.py`（SVG 必出；PNG 需系统 **libcairo**：macOS `brew install cairo`） |

---

## Gate · 文件一览

| 文件 | 作用 |
|------|------|
| **`activate_dev_env.sh`** | **开发环境激活**（README 唯一入口 · frozen sync · gate pr · pre-commit） |
| **`gate`** | Bash 入口 → `gate_cli.py` |
| **`gate_cli.py`** | **Spec×Harness Gate**：`plan` · `test` · `step` · `delivery` · `verify` · `pr` · `gate0` · `analyze` · `docs-sync` |
| **`pipeline_artifacts.py`** | Gate 强制输出：`_factoryos_pipeline/<date>/{dev,test,verify}/HH-MM_*.md` |
| **`check_deptry.py`** | import ↔ `pyproject.toml` 声明（`gate pr` · DEP001） |
| **`check_uv_lock.sh`** | `uv lock --check`（pre-commit · pyproject 变更时） |
| **`venv_exec.sh`** | pre-commit 统一走 `.venv/bin/python` |
| **`check_plan_spec.py`** | plan ↔ contracts AC/路径一致性（确认规划门） |
| **`plan_gate_lib.py`** | **确认规划绝对门禁**：`plan.ok` ↔ `workflow_state.plan`（Hook · gate step/delivery） |
| **`check_pipeline.py`** | 落盘工件 + `workflow_state` 阶段检查（含 step 单步 Test · delivery 终轮） |
| **`check_test_regression.py`** | 单步/终轮 Test 落盘与结论门禁 |

```bash
./scripts/gate plan
./scripts/gate step --step N -k 'G-01'
./scripts/gate delivery
./scripts/gate pr
./scripts/factoryos gate gate0
```

激活清单：[.cursor/factoryos/ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

### CLI · guide 调试（平台内部 · 非实施主路径）

> **硬性规定**：实施顾问与客户 IT **不以** 本 CLI 作为主接入路径；见 [UI-FIRST §U4](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)。

| 文件 | 作用 |
|------|------|
| **`factoryos`** | Bash 入口；转调 `factoryos_cli.py` |
| **`factoryos_cli.py`** | **flows.json 终端渲染器**（`guide`）。供平台研发调试 Gate 状态机、CI 文档生成、离线演练。真源 `src/integration/tools/guide/flows.json`。不依赖 API 运行时。 |

```bash
./scripts/factoryos guide              # 交互选链路（调试）
./scripts/factoryos guide onboard      # 打印 D1 步骤
./scripts/factoryos guide map onboard  # 一图总览
./scripts/factoryos guide --json onboard  # 机器可读 JSON（CI / 文档生成）
```

---

### Harness · 统一入口 + 四门（CI 同款）

| 文件 | 作用 |
|------|------|
| **`harness`** | Bash 入口 → `check_harness.py` |
| **`check_harness.py`** | **统一验收盘**：`--tier contracts\|boundaries\|step\|full\|auto`；可选 `--pytest -k` |

```bash
./scripts/harness                          # full = CI / Step 停机
./scripts/harness --tier contracts         # L0 仅契约
./scripts/harness --tier boundaries        # L0+L1
./scripts/harness --tier auto              # git diff 推断
./scripts/harness --tier step --pytest -k 'G-01'   # 四门 + pytest L3
./scripts/factoryos harness --tier auto    # 同上（factoryos 子命令）
```

| tier | 层级 | 跑哪些 |
|------|------|--------|
| `contracts` | L0 | openapi refs · cmv sync |
| `boundaries` | L1 | + import boundaries · kernel/router/integration registry · legacy paths |
| `step` / `full` | L2 | + code redundancy |
| `auto` | 推断 | 按 git diff 选上表最高层；无 diff → `full` |

四门均为 **stdlib only**，无第三方依赖。也可单独跑子脚本（调试时）：

| 文件 | 检查什么 | 真源路径 | 失败意味着 |
|------|----------|----------|------------|
| **`check_openapi_schema_refs.py`** | OpenAPI 中 `$ref` 是否指向存在的 JSON Schema | `contracts/openapi/` → `contracts/schemas/` | 接口文档与 Schema 断裂；前端/测试契约不可信 |
| **`check_cmv_sync.py`** | CMV 动词注册表：命名、L2 补偿器、connector_ops 完整性 | `contracts/cmv/CMV注册表.yaml` | 新 DSL 动词不合规；Revert 链断裂 |
| **`check_import_boundaries.py`** | `os_core` 十模块依赖矩阵 + `integration/` 禁止 import 私有 API | `src/server/os_core/` · `src/integration/` | 架构分层被破坏 |
| **`check_kernel_registry.py`** | `os_core/registry.py` ↔ 磁盘 10 内核模块 | `src/server/os_core/` | 内核模块漏登记 |
| **`check_router_registry.py`** | `router/v1/registry.py` ↔ `modules/*/routers.py`；main 禁 include_router | `src/server/api/` | HTTP 面失控 |
| **`check_integration_registry.py`** | `integration/registry.py` ↔ GIP 挂载 | `src/integration/` | 集成目录漏登记 |
| **`check_legacy_paths.py`** | 禁止 `src/apps/api` · `src/os_core` · `src/db` 等废止路径复活 | `src/` | 结构回退 |
| **`check_code_redundancy.py`** | `os_core` / `server.api` 跨文件重复函数体 | `src/server/os_core/` · `src/server/api/` | 违反编码绝对门禁 |

```bash
python scripts/check_import_boundaries.py   # 单独调试
python scripts/check_cmv_sync.py
python scripts/check_openapi_schema_refs.py
python scripts/check_code_redundancy.py
```

GitHub Actions：`.github/workflows/ci.yml` 跑 `check_harness.py --tier full` + tenants 密钥 grep。

---

### 文档图 · 一次性生成（非 CI）

依赖 **`cairosvg`**（Python）+ 系统 **libcairo**（PNG 导出；无则仅更新 SVG）。**`python-pptx`**（宣讲 PPT）。改 ADR/架构说明后手动跑，**不**纳入每 Step Harness。

| 文件 | 输出 | 说明 |
|------|------|------|
| **`generate_architecture_diagrams.py`** | `docs/文档/架构/` 下 **系统/技术/数据/核心模块** 四张 SVG+PNG | 大块 SVG 内嵌；反映 ADR-000～007 分层与 Path A/B/C |
| **`generate_base_capability_diagram.py`** | `docs/文档/架构/基座能力说明图.svg/.png` | 基座能力结构说明（非技术人+技术人双视角） |
| **`generate_all_diagrams.py`** | 依次调用上两个 generator | 日常更新架构图用这一条 |
| **`generate_internal_deck.py`** | `docs/准备/2026-06-16/FactoryOS-内部宣讲-v3.1.pptx` | 内部宣讲 PPT；附录嵌入架构 PNG |

```bash
pip install cairosvg python-pptx   # 首次需要
python scripts/generate_all_diagrams.py
python scripts/generate_internal_deck.py   # 可选
```

---

## Harness 与 SH-步步流 v2（分层更优雅）

当前工作流已在 **每 Step 停机前** 要求四门 + `pytest`。四门全跑简单可靠；按**改动面分层**更清晰、反馈更快：

### 分层验收盘

| 层级 | 何时跑 | 脚本 |
|------|--------|------|
| **L0 · 契约基线** | Step 0-B · `确认规划` · 仅改 `contracts/` | `./scripts/harness --tier contracts` |
| **L1 · 模块边界** | 改 `src/server/os_core` · `src/integration` | `./scripts/harness --tier boundaries` |
| **L2 · 代码质量** | 改 `os_core` / `src/apps` 业务 `.py` | `./scripts/harness --tier step` |
| **L3 · 行为证明** | Step 停机 · Test | `./scripts/harness --tier full --pytest -k '<AC-ID>'` |

### 工作流节点对照

| SH-步步流节点 | 建议 Harness | 说明 |
|-------------|--------------|------|
| **Step 0-B** 契约对齐 | L0 | 确认 OpenAPI/CMV 与 plan 一致；无代码也可绿 |
| **`确认规划`** plan 落盘 | L0 | plan 含接口/AC 时契约必须已绿 |
| **Step N 编码完成 · 停机** | **full + pytest** | `./scripts/harness --tier full --pytest -k '<AC-ID>'` |
| **Test · 跑测前** | L0+L1+L2+L3 | 与 Dev 同一验收盘，避免双标准 |
| **仅改 `contracts/` 的 PR** | L0 | 不必等 os_core 存在 |
| **仅改 `src/integration/packs`** | L0+L1 | integration import 边界 |
| **Gate 0 / CI** | L0+L1+L2（+pytest W1 后） | `.github/workflows/ci.yml` |

### 回归触发（Test Agent 自动判断）

| 改动目录 | 必跑脚本 |
|----------|----------|
| `contracts/openapi` · `contracts/schemas` | `check_openapi_schema_refs` |
| `contracts/cmv` · 新 DSL 动词 | `check_cmv_sync` |
| `src/server/os_core/**` · `src/integration/**` | `check_import_boundaries` |
| `src/server/os_core/**` · `src/server/api/**` 业务逻辑 | `check_code_redundancy` |

### 结论

- **是，把检查脚本钉进工作流节点更优雅**：契约检查前置到 Step 0/规划，模块/冗余检查绑定 Python 改动面，Step 完成四门+pytest 全绿 —— 形成 **Spec（contracts）+ Harness（scripts）+ 测试（pytest）** 闭环。
- **比「每步盲目四门」更优雅的是「分层 + Step 末全量」**：平时按改动面跑子集，**停机前仍四门全绿**，与 CI 一致，假通过难混。

---

## docs 认知基线 · `docs_baseline`

| 文件 | 作用 |
|------|------|
| **`docs_baseline`** | Bash 入口 → `docs_baseline.py` |
| **`docs_baseline.py`** | `refresh` · `diff` · `workflow-check` · `contracts-crosscheck` · `gate` |

基线目录（与 `factoryos/` 隔离）：`.cursor/docs-baseline/` — 见 [BASELINE.md](../.cursor/docs-baseline/BASELINE.md)

```bash
./scripts/docs_baseline refresh              # W1 前冻结 docs/
./scripts/docs_baseline diff --write-report
./scripts/docs_baseline workflow-check       # Tier-A → 建议更新 factoryos
./scripts/gate docs-sync                     # PR：A/C fail · B warn
```

---

## 与目录布局

```text
scripts/                    ← 本目录（真源）
.cursor/docs-baseline/        ← docs 认知基线（manifest · mirror · policy）
.cursor/factoryos/           ← 研发工作流真源
contracts/                   ← check_openapi · check_cmv 读取
docs/                        ← 厚文档；generate_* 输出；baseline 镜像源
```

---

## 维护约定

- 新增 **CI 门禁脚本** → 注册到 `check_harness.py` + 更新 `ci.yml` + 本文 + `.cursor/factoryos/HARNESS-SCRIPTS.md`
- **docs 大改** → `./scripts/docs_baseline refresh` + `workflow-check` → 同步 `.cursor/factoryos/`
- **禁止** 在 `src/scripts/` 或 `docs/scripts/` 保留副本
- 改 `contracts/` 只改 `contracts/`，脚本路径以 `contracts/` 为准（B 策略）
