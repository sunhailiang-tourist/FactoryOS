#!/usr/bin/env python3
"""FactoryOS CLI — 接入与扩展交互引导（文档真源驱动）。

主命令:
  factoryos guide              交互式选择链路并逐步引导
  factoryos guide onboard      新客户 D1 全链路
  factoryos guide import       第二家 S1 导入
  factoryos guide extend       扩展新厂商 Connector
  factoryos guide extend-d2    D2 定制扩展
  factoryos guide ops          运维事件
  factoryos guide list         列出所有链路
  factoryos guide map [flow]   一图看清整条链路（人+系统）
  factoryos guide --json onboard  机器可读输出
  factoryos harness [--tier T]    SH-步步流统一验收盘（L0–L2）
  factoryos gate <plan|test|step|pr|gate0|docs-sync>  Spec×Harness Gate

W1 阶段：guide 不依赖 API 运行时；curl 命令在 API 就绪后可直接执行。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FLOWS_PATH = ROOT / "src" / "integration" / "tools" / "guide" / "flows.json"

# ANSI（非 TTY 时自动关闭）
_USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    if not _USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(t: str) -> str:
    return _c("1", t)


def dim(t: str) -> str:
    return _c("2", t)


def red(t: str) -> str:
    return _c("31", t)


def green(t: str) -> str:
    return _c("32", t)


def yellow(t: str) -> str:
    return _c("33", t)


def cyan(t: str) -> str:
    return _c("36", t)


def load_data() -> dict[str, Any]:
    if not FLOWS_PATH.is_file():
        print(f"flows 真源缺失: {FLOWS_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(FLOWS_PATH.read_text(encoding="utf-8"))


def substitute(text: str, tenant: str, vendor: str) -> str:
    return (
        text.replace("{tenant}", tenant or "<tenant>")
        .replace("{vendor}", vendor or "<vendor>")
        .replace("{system}", "erp")
        .replace("{graph_id}", "<graph_id>")
        .replace("{version}", "v1.0.0")
        .replace("{packId}", "conn-erp-" + (vendor or "vendor") + "-write")
    )


def mode_label(mode: str, automated: bool) -> str:
    if mode == "human":
        return f"{yellow('👤 人')} · {red('须签字/确认')}"
    if mode == "hybrid":
        auto = green("系统可自动") if automated else yellow("系统+人协作")
        return f"{cyan('👤+🤖')} · {auto}"
    return cyan("🤖 系统")


def render_step(
    index: int,
    total: int,
    gate_id: str,
    gate: dict[str, Any],
    tenant: str,
    vendor: str,
    *,
    compact: bool = False,
) -> str:
    lines: list[str] = []
    sep = "━" * 62
    lines.append(sep)
    lines.append(
        bold(f"步骤 {index}/{total} · {gate_id} · {gate['title']}")
    )
    lines.append(sep)
    lines.append(f"角色: {', '.join(gate.get('roles', []))}")
    lines.append(mode_label(gate.get("mode", "hybrid"), gate.get("automated", False)))
    if gate.get("forbidden"):
        lines.append(red(f"禁止: {gate['forbidden']}"))
    lines.append("")

    if not compact:
        lines.append(bold("【你要做什么】"))
        for i, item in enumerate(gate.get("do", []), 1):
            lines.append(f"  {i}. {item}")
        lines.append("")

    cmds = gate.get("commands") or []
    if cmds:
        lines.append(bold("【执行命令】"))
        for cmd in cmds:
            lines.append(f"  $ {dim(substitute(cmd, tenant, vendor))}")
        lines.append("")

    files = gate.get("files") or []
    if files:
        lines.append(bold("【改哪些文件】"))
        for f in files:
            lines.append(f"  · {substitute(f, tenant, vendor)}")
        lines.append("")

    apis = gate.get("api") or []
    if apis:
        lines.append(bold("【API（OpenAPI v1.1.1）】"))
        for api in apis:
            lines.append(f"  · {api}")
        lines.append("")

    arts = gate.get("artifacts") or []
    if arts:
        lines.append(bold("【产出物】"))
        for a in arts:
            lines.append(f"  ✓ {a}")
        lines.append("")

    return "\n".join(lines)


def render_flow_map(flow: dict[str, Any], data: dict[str, Any]) -> str:
    gates = data["gates"]
    lines = [
        "",
        bold(f"链路总览 · {flow['title']}"),
        dim(flow.get("summary", "")),
        f"周期: {flow.get('duration', '—')}  |  文档: {flow.get('doc', '')}",
        "",
        "  图例: " + yellow("👤人审") + "  " + cyan("👤+🤖协作") + "  " + green("🤖可自动"),
        "",
    ]
    steps = flow["steps"]
    for i, gid in enumerate(steps):
        g = gates[gid]
        mode = g.get("mode", "hybrid")
        if mode == "human":
            icon = yellow("👤")
        elif g.get("automated"):
            icon = green("🤖")
        else:
            icon = cyan("⚙")
        branch = "├─" if i < len(steps) - 1 else "└─"
        lines.append(f"  {branch} {icon} {bold(gid)} {g['title']}")
    lines.append("")
    lines.append(dim("运行逐步引导: factoryos guide " + flow["id"] + " --tenant <id>"))
    lines.append("")
    return "\n".join(lines)


def run_interactive_flow(
    flow: dict[str, Any],
    data: dict[str, Any],
    tenant: str,
    vendor: str,
    *,
    auto: bool = False,
) -> None:
    gates = data["gates"]
    steps = flow["steps"]
    total = len(steps)

    print(render_flow_map(flow, data))

    if not auto and sys.stdin.isatty():
        try:
            input(dim("按 Enter 开始逐步引导（q 退出）… ") or "\n")
        except (EOFError, KeyboardInterrupt):
            print()
            return

    for i, gid in enumerate(steps, 1):
        gate = gates.get(gid)
        if not gate:
            print(red(f"未知 Gate: {gid}"), file=sys.stderr)
            continue
        print(render_step(i, total, gid, gate, tenant, vendor))
        if i < total:
            if auto or not sys.stdin.isatty():
                continue
            try:
                ans = input(dim("[Enter] 下一步  [q] 退出  [m] 重看总览: ")).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if ans == "q":
                break
            if ans == "m":
                print(render_flow_map(flow, data))

    print(bold(green("\n✓ 链路引导结束。详述见: docs/文档/规格说明/人工决策Playbook.md 或 .cursor/factoryos/\n")))


def cmd_guide_list(data: dict[str, Any]) -> None:
    print(bold("\nFactoryOS 接入 / 扩展链路（factoryos guide <id>）\n"))
    pad = dim(" " * 16)
    for fid, flow in data["flows"].items():
        print(f"  {cyan(fid):16} {flow['title']}")
        print(f"  {pad} {flow.get('when', '')}")
        print()
    print(dim("新人入口: factoryos guide"))
    print(dim("一图总览: factoryos guide map onboard\n"))


def cmd_guide_map(data: dict[str, Any], flow_id: str | None) -> None:
    flows = data["flows"]
    if flow_id:
        if flow_id not in flows:
            print(red(f"未知链路: {flow_id}"), file=sys.stderr)
            sys.exit(1)
        print(render_flow_map(flows[flow_id], data))
        return
    for flow in flows.values():
        print(render_flow_map(flow, data))


def pick_flow_interactive(data: dict[str, Any]) -> str:
    flows = data["flows"]
    items = list(flows.items())
    print(bold("\n你要做什么？（输入序号）\n"))
    for i, (fid, flow) in enumerate(items, 1):
        print(f"  {bold(str(i))}. [{fid}] {flow['title']}")
        print(f"     {dim(flow.get('when', ''))}")
    print(f"\n  {dim('0')} 退出\n")
    while True:
        try:
            raw = input("请选择: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if raw in ("0", "q", "quit"):
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return items[int(raw) - 1][0]
        if raw in flows:
            return raw
        print(red("无效选择，请输入序号或链路 id"))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="factoryos",
        description="FactoryOS 接入与扩展 CLI（guide = 人+系统完整链路引导）",
    )
    sub = parser.add_subparsers(dest="command")

    g = sub.add_parser(
        "guide",
        help="交互式接入/扩展链路引导（新人一条命令学会）",
    )
    g.add_argument(
        "flow",
        nargs="?",
        choices=["onboard", "import", "extend", "extend-d2", "ops", "list", "map"],
        help="链路类型；省略则交互选择",
    )
    g.add_argument(
        "map_target",
        nargs="?",
        help="与 map 合用：factoryos guide map onboard",
    )
    g.add_argument("--tenant", "-t", default="", help="租户 ID，替换命令中的 {tenant}")
    g.add_argument("--vendor", "-v", default="", help="厂商 slug，替换 {vendor}")
    g.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON（供 CI/文档生成）",
    )
    g.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="非交互，一次打印全部步骤",
    )
    g.add_argument(
        "--step",
        help="仅显示某一 Gate（内部调试用）",
    )

    h = sub.add_parser(
        "harness",
        help="SH-步步流统一 Harness（contracts/boundaries/step/full/auto）",
    )
    h.add_argument(
        "--tier",
        "-t",
        default="full",
        choices=["contracts", "boundaries", "step", "full", "auto"],
        help="L0 契约 → L1 边界 → step/full 四门；auto=git diff",
    )
    h.add_argument(
        "--pytest",
        "-k",
        metavar="EXPR",
        help="L3：静态检查通过后跑 pytest -k EXPR",
    )
    h.add_argument("pytest_extra", nargs="*", help="传给 pytest 的额外参数")

    gt = sub.add_parser("gate", help="SH-步步流 Gate（plan/test/step/pr/gate0/docs-sync/analyze）")
    gt.add_argument(
        "gate_name",
        choices=["plan", "test", "step", "pr", "gate0", "analyze", "verify", "docs-sync"],
    )
    gt.add_argument("--plan", type=Path)
    gt.add_argument("-k", "--pytest", metavar="EXPR")
    gt.add_argument("--step", type=int, default=1)
    gt.add_argument("pytest_extra", nargs="*")

    args = parser.parse_args()

    if args.command == "gate":
        cmd = [sys.executable, str(ROOT / "scripts" / "gate_cli.py"), args.gate_name]
        if args.gate_name in ("plan", "analyze") and args.plan:
            cmd.extend(["--plan", str(args.plan)])
        if args.gate_name == "step":
            cmd.extend(["--step", str(args.step)])
            if args.pytest:
                cmd.extend(["-k", args.pytest, *args.pytest_extra])
            elif args.pytest_extra:
                cmd.extend(args.pytest_extra)
        elif args.gate_name == "verify":
            cmd.extend(["--step", str(args.step)])
        elif args.pytest_extra:
            cmd.extend(args.pytest_extra)
        sys.exit(subprocess.call(cmd, cwd=ROOT))

    if args.command == "harness":
        cmd = [sys.executable, str(ROOT / "scripts" / "check_harness.py"), "--tier", args.tier]
        if args.pytest:
            cmd.extend(["--pytest", args.pytest, *args.pytest_extra])
        elif args.pytest_extra:
            cmd.extend(args.pytest_extra)
        sys.exit(subprocess.call(cmd, cwd=ROOT))

    if args.command != "guide":
        parser.print_help()
        print(
            dim("\n提示: 运行 factoryos guide 开始接入引导\n"),
            file=sys.stderr,
        )
        sys.exit(0 if args.command is None else 1)

    data = load_data()
    flows = data["flows"]

    # extend 是 extend-vendor 的别名
    flow_alias = {"extend": "extend-vendor"}
    flow_id = args.flow
    if flow_id in flow_alias:
        flow_id = flow_alias[flow_id]

    if flow_id == "list":
        cmd_guide_list(data)
        return

    if flow_id == "map":
        target = args.map_target
        if target in flow_alias:
            target = flow_alias[target]
        cmd_guide_map(data, target)
        return

    if args.json:
        fid = flow_id or "onboard"
        if fid not in flows and fid in flow_alias:
            fid = flow_alias[fid]
        if fid not in flows:
            fid = pick_flow_interactive(data)
        out = {
            "flow": flows[fid],
            "gates": {g: data["gates"][g] for g in flows[fid]["steps"]},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.step:
        gate = data["gates"].get(args.step)
        if not gate:
            print(red(f"未知 Gate: {args.step}"), file=sys.stderr)
            sys.exit(1)
        print(render_step(1, 1, args.step, gate, args.tenant, args.vendor))
        return

    if not flow_id:
        flow_id = pick_flow_interactive(data)

    if flow_id not in flows:
        print(red(f"未知链路: {flow_id}"), file=sys.stderr)
        sys.exit(1)

    tenant = args.tenant
    if not tenant and sys.stdin.isatty() and not args.yes:
        try:
            tenant = input(dim("租户 ID（可回车跳过）: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            tenant = ""

    run_interactive_flow(
        flows[flow_id],
        data,
        tenant,
        args.vendor,
        auto=args.yes,
    )


if __name__ == "__main__":
    main()
