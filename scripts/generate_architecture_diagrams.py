#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate FactoryOS architecture diagram family (SVG + PNG)."""
from __future__ import annotations

from pathlib import Path

from diagram_export import write_svg_and_png

OUT = Path(__file__).resolve().parents[1] / "docs" / "文档" / "架构"

FONT = '"PingFang SC", "Heiti SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif'

STYLES = f"""
  text {{ font-family: {FONT}; }}
  .t1 {{ font-size: 26px; font-weight: bold; fill: #1a252f; }}
  .t2 {{ font-size: 13px; fill: #566573; }}
  .zt {{ font-size: 14px; font-weight: bold; fill: #ffffff; }}
  .bt {{ font-size: 12px; font-weight: bold; fill: #1a252f; }}
  .sm {{ font-size: 11px; fill: #333333; }}
  .hi {{ font-size: 10px; fill: #666666; }}
"""


def _write(name: str, svg: str, width: int = 2400) -> None:
    write_svg_and_png(OUT, name, svg, png_width=width)


def system_architecture() -> None:
    w, h = 1800, 2100
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs><style>{STYLES}</style></defs>
  <rect width="{w}" height="{h}" fill="#fafbfc"/>
  <text x="{w//2}" y="42" text-anchor="middle" class="t1">FactoryOS 系统架构图</text>
  <text x="{w//2}" y="68" text-anchor="middle" class="t2">平台分层 · 扩展机制 · Path A/B/C · 规模阶梯 S0-S3 · v2.0 · ADR-000-007</text>

  <!-- users -->
  <rect x="500" y="88" width="800" height="48" rx="8" fill="#fadbd8" stroke="#c0392b" stroke-width="2"/>
  <text x="{w//2}" y="118" text-anchor="middle" class="bt">用户触达：钉钉/企微 H5 · PC 管理台 · 工位屏（角色入口，不含业务规则）</text>

  <!-- L3 -->
  <rect x="80" y="156" width="1080" height="72" rx="8" fill="#fadbd8" stroke="#c0392b" stroke-width="2"/>
  <rect x="80" y="156" width="1080" height="26" rx="8" fill="#922b21"/>
  <text x="96" y="174" class="zt">Platform-L3  Harness 入口层</text>
  <text x="96" y="204" class="sm">h5-worker 移动端壳 · web-admin PC · 感知入口（说/拍/扫/点）· 确认门 / dry_run / 待办</text>
  <text x="96" y="220" class="hi">Harness Loop：感知 → 授权 → 沙箱 → 确认 → 执行 → 验证 → 记录</text>

  <!-- L2 -->
  <rect x="80" y="248" width="1080" height="72" rx="8" fill="#fdebd0" stroke="#d68910" stroke-width="2"/>
  <rect x="80" y="248" width="1080" height="26" rx="8" fill="#d35400"/>
  <text x="96" y="266" class="zt">Platform-L2  Skills 体验层（唯一含 LLM）</text>
  <text x="96" y="296" class="sm">agent_orchestrator：LangGraph FSM → DSL 计划 JSON · license_service：Pack 授权边界</text>
  <text x="96" y="312" class="hi">红线：Agent 无写 Legacy 权限 · 只产出计划，不执行写库</text>

  <!-- L0 -->
  <rect x="80" y="340" width="1080" height="120" rx="10" fill="#d5f5e3" stroke="#1e8449" stroke-width="3"/>
  <rect x="80" y="340" width="1080" height="28" rx="10" fill="#1e8449"/>
  <text x="96" y="360" class="zt">Platform-L0  信任内核（宪法层 · 零 LLM · 全行业复用机制）</text>
  <rect x="96" y="378" width="240" height="68" rx="6" fill="#eafaf1" stroke="#27ae60"/>
  <text x="108" y="400" class="bt">graph_service</text>
  <text x="108" y="418" class="sm">流程版本 draft→frozen</text>
  <text x="108" y="434" class="hi">未冻结禁止 L2 写</text>
  <rect x="352" y="378" width="240" height="68" rx="6" fill="#eafaf1" stroke="#27ae60"/>
  <text x="364" y="400" class="bt">rule_engine</text>
  <text x="364" y="418" class="sm">角色/条件/动作</text>
  <text x="364" y="434" class="hi">默认 deny</text>
  <rect x="608" y="378" width="260" height="68" rx="6" fill="#eafaf1" stroke="#27ae60"/>
  <text x="620" y="400" class="bt">execution_service</text>
  <text x="620" y="418" class="sm">唯一写路径 · Saga · Revert</text>
  <text x="620" y="434" class="hi">幂等 · 对账 · Shadow</text>
  <rect x="884" y="378" width="260" height="68" rx="6" fill="#eafaf1" stroke="#27ae60"/>
  <text x="896" y="400" class="bt">audit_service</text>
  <text x="896" y="418" class="sm">append-only 审计</text>
  <text x="896" y="434" class="hi">全程可追溯</text>

  <!-- L1 -->
  <rect x="80" y="480" width="1080" height="88" rx="8" fill="#d6eaf8" stroke="#2874a6" stroke-width="2"/>
  <rect x="80" y="480" width="1080" height="26" rx="8" fill="#1a5276"/>
  <text x="96" y="498" class="zt">Platform-L1  连接层 GIP</text>
  <text x="96" y="528" class="sm">connector_sdk + Blueprint Runtime + Registry · mcp_gateway（CMV → MCP tools → DslPlan）</text>
  <text x="96" y="546" class="sm">integration/catalog · packs · tenants — 集成外置，不改 L0 内核</text>
  <text x="96" y="562" class="hi">稳定动词 → 各厂商 ERP/MES/WMS API · 禁止 bypass execution 直写</text>

  <!-- Data-L0 -->
  <rect x="80" y="588" width="1080" height="64" rx="8" fill="#fdedec" stroke="#e74c3c" stroke-width="2" stroke-dasharray="6"/>
  <text x="96" y="614" class="bt">Data-L0  客户账本（权威 · FactoryOS 不替代）</text>
  <text x="96" y="636" class="sm">ERP · MES · WMS · OA · CRM … 或 Path C：PostgreSQL builtin 表模拟 L0</text>

  <!-- write path -->
  <rect x="80" y="668" width="1080" height="56" rx="8" fill="#ebf5fb" stroke="#117a65" stroke-width="2"/>
  <text x="96" y="692" class="bt" fill="#117a65">唯一写路径（红线）</text>
  <text x="96" y="712" class="sm">Harness → Agent → Graph(frozen) → Rule(allow) → Execution → Connector → Data-L0 → Audit → Data-L1(RDS)</text>

  <!-- extension sidebar -->
  <rect x="1180" y="156" width="580" height="568" rx="8" fill="#f4ecf7" stroke="#8e44ad" stroke-width="2"/>
  <rect x="1180" y="156" width="580" height="28" rx="8" fill="#7d3c98"/>
  <text x="1196" y="176" class="zt">扩展机制（不动 L0 代码路径）</text>
  <text x="1196" y="208" class="bt">Pack（可授权 SKU）</text>
  <text x="1196" y="226" class="sm">Graph Pack · Capability Pack · Connector Pack · Skill Pack</text>
  <text x="1196" y="252" class="bt">Override（差异配置）</text>
  <text x="1196" y="270" class="sm">Platform / Tenant / Scope 三级 · Scope 优先合并</text>
  <text x="1196" y="296" class="bt">Implementation Package</text>
  <text x="1196" y="314" class="sm">export 快照 → 第二家 import 差量 · 现场→标准资产</text>
  <text x="1196" y="340" class="bt">Registry + License</text>
  <text x="1196" y="358" class="sm">租户绑定 Connector 实例 · 未授权 Pack → 403</text>
  <text x="1196" y="384" class="bt">GIP 三速接入</text>
  <text x="1196" y="402" class="sm">S1 ≤1周 import 包 · S2 ≤2周 AI Blueprint</text>
  <text x="1196" y="418" class="sm">S3 1-2周 Python Connector</text>
  <text x="1196" y="444" class="bt">资产闭环 ⑦⑧⑩</text>
  <text x="1196" y="462" class="sm">freeze → Shadow≥14d → export → Pack库 → import</text>
  <text x="1196" y="488" class="bt">Legacy 固定 10 类</text>
  <text x="1196" y="506" class="sm">mes erp wms oa crm csm aps plm qms mock</text>
  <text x="1196" y="522" class="hi">新厂商只加 vendor，不加 system 类型</text>
  <text x="1196" y="548" class="bt">MCP 开放节奏</text>
  <text x="1196" y="566" class="sm">Y1 末内部 GA · Y2 对外（ADR-004）</text>
  <text x="1196" y="590" class="bt">商业 Pack 层 L0-L3</text>
  <text x="1196" y="608" class="sm">与 Platform 分层同名不同义 · 见 ADR-003</text>
  <text x="1196" y="634" class="bt">部署形态 ADR-007</text>
  <text x="1196" y="652" class="sm">Pool 共享 · Bridge 独立 schema · Silo 独立栈</text>
  <text x="1196" y="668" class="hi">同一 L0 二进制 · placement_tier 差异</text>
  <text x="1196" y="694" class="bt">规模阶梯</text>
  <text x="1196" y="712" class="sm">S0 1-10 tenant · S1 百级 Pool+RLS</text>
  <text x="1196" y="728" class="sm">S2 千级 Cell · S3 Silo+shuffle</text>

  <!-- paths -->
  <rect x="80" y="744" width="1680" height="130" rx="8" fill="#ffffff" stroke="#2874a6" stroke-width="2"/>
  <rect x="80" y="744" width="1680" height="26" rx="8" fill="#2874a6"/>
  <text x="96" y="762" class="zt">三条写入路径 Path A/B/C（同一 L0 内核 — ADR-005）</text>
  <rect x="96" y="782" width="520" height="78" rx="6" fill="#fdebd0" stroke="#d68910" stroke-width="2"/>
  <text x="108" y="804" class="bt" fill="#d35400">Path A · 灯塔（哈森）</text>
  <text x="108" y="824" class="sm">conn-erp-write + erp-read + conn-dingtalk</text>
  <text x="108" y="844" class="hi">Data-L0 = 客户 ERP 权威账本 · 无 MES</text>
  <rect x="636" y="782" width="520" height="78" rx="6" fill="#ebf5fb" stroke="#2874a6"/>
  <text x="648" y="804" class="bt">Path B · 平台通用</text>
  <text x="648" y="824" class="sm">conn-mes 写 + conn-erp-read</text>
  <text x="648" y="844" class="hi">Data-L0 = MES 写 + ERP 读 · 双系统 Overlay</text>
  <rect x="1176" y="782" width="520" height="78" rx="6" fill="#e8f8f5" stroke="#1e8449"/>
  <text x="1188" y="804" class="bt">Path C · Starter-B-Lite</text>
  <text x="1188" y="824" class="sm">conn-mes-builtin → PostgreSQL builtin 表</text>
  <text x="1188" y="844" class="hi">L0 机制与 A/B 完全相同 · Y1 默认不销售</text>

  <!-- gates -->
  <rect x="80" y="892" width="1680" height="100" rx="8" fill="#fef9e7" stroke="#b7950b" stroke-width="2"/>
  <text x="96" y="920" class="bt">交付闸门与业务价值</text>
  <text x="96" y="942" class="sm">Gate 0（Core）：L0 机制 + mock Connector + AC-BASE-001 52 P0 → tag core-v1.0.0</text>
  <text x="96" y="962" class="sm">Gate 0'（工厂）：frozen Graph + 真实 Connector + D1 Skill · 0 智解脱老系统 · 错了能收回 · 现场与账本一致</text>
  <text x="96" y="982" class="hi">ISA-95 L3.5 Overlay · 不替代 ERP/MES · 不是聊天机器人 · 不是数仓</text>

  <!-- legend -->
  <rect x="80" y="1010" width="1680" height="72" rx="8" fill="#eafaf1" stroke="#1e8449"/>
  <text x="96" y="1036" class="bt">图例</text>
  <text x="96" y="1056" class="sm">红=入口 L3 · 橙=体验 L2 · 绿=信任内核 L0 · 蓝=连接 L1 · 虚线红框=客户账本 L0</text>
  <text x="96" y="1072" class="sm">紫框=扩展与商业机制 · 实线箭头写路径必经 execution · Modular Monolith 单 server/api deployable</text>

  <text x="{w//2}" y="1120" text-anchor="middle" class="t2">详见 文档/架构/系统架构图说明.md · 16-OS核心基座 · 2026-06-16</text>
</svg>'''
    _write("系统架构图", svg)


def technical_architecture() -> None:
    w, h = 1800, 2280
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs><style>{STYLES}</style></defs>
  <rect width="{w}" height="{h}" fill="#fafbfc"/>
  <text x="{w//2}" y="42" text-anchor="middle" class="t1">FactoryOS 技术架构图</text>
  <text x="{w//2}" y="68" text-anchor="middle" class="t2">模块映射 · 技术栈 · AI 边界 · 部署映射 · v2.0 · ADR-001/004/007</text>

  <!-- frontend -->
  <rect x="40" y="92" width="1720" height="88" rx="8" fill="#fadbd8" stroke="#c0392b" stroke-width="2"/>
  <rect x="40" y="92" width="1720" height="26" rx="8" fill="#922b21"/>
  <text x="56" y="110" class="zt">前端（Phase 1 后半 · React 18 + TypeScript + Vite）</text>
  <rect x="56" y="126" width="380" height="44" rx="6" fill="#fff" stroke="#c0392b"/>
  <text x="68" y="146" class="bt">src/apps/web-admin</text>
  <text x="68" y="162" class="sm">PC 管理 · Graph freeze · Studio /studio/*</text>
  <rect x="452" y="126" width="380" height="44" rx="6" fill="#fff" stroke="#c0392b"/>
  <text x="464" y="146" class="bt">src/apps/h5-worker</text>
  <text x="464" y="162" class="sm">钉钉/企微 H5 壳 · Harness 确认门</text>
  <rect x="848" y="126" width="380" height="44" rx="6" fill="#fff5f5" stroke="#e74c3c" stroke-dasharray="4"/>
  <text x="860" y="146" class="bt">感知多模态</text>
  <text x="860" y="162" class="sm">语音/图片/扫码 → OSS 短期存储</text>
  <text x="1260" y="154" class="sm">HTTPS → server/api（OpenAPI v1.1.1）</text>

  <!-- api -->
  <rect x="40" y="196" width="1720" height="56" rx="8" fill="#d5e8d4" stroke="#82b366" stroke-width="2"/>
  <text x="56" y="222" class="bt">server/api — FastAPI + Uvicorn · 唯一生产 deployable · HTTP 适配层（无业务规则）</text>
  <text x="56" y="240" class="hi">structlog JSON · OTel spans · tenant_id 上下文 · pyright/mypy 严格</text>

  <!-- os_core L0 -->
  <rect x="40" y="268" width="1200" height="200" rx="8" fill="#d5f5e3" stroke="#1e8449" stroke-width="2"/>
  <rect x="40" y="268" width="1200" height="26" rx="8" fill="#1e8449"/>
  <text x="56" y="286" class="zt">src/server/os_core/ L0 信任内核（零 LLM · import: os_core.*）</text>
  <rect x="56" y="302" width="270" height="72" rx="6" fill="#fff" stroke="#27ae60"/>
  <text x="68" y="322" class="bt">graph_service</text>
  <text x="68" y="340" class="sm">SQLAlchemy async · Graph 版本</text>
  <text x="68" y="356" class="hi">draft → in_review → frozen</text>
  <rect x="342" y="302" width="270" height="72" rx="6" fill="#fff" stroke="#27ae60"/>
  <text x="354" y="322" class="bt">rule_engine</text>
  <text x="354" y="340" class="sm">Pydantic RuleSet · evaluate API</text>
  <text x="354" y="356" class="hi">默认 deny · allow 显式</text>
  <rect x="628" y="302" width="290" height="72" rx="6" fill="#fff" stroke="#27ae60"/>
  <text x="640" y="322" class="bt">execution_service</text>
  <text x="640" y="340" class="sm">Saga · Compensator · 幂等键</text>
  <text x="640" y="356" class="hi">唯一 connector.write 调用方</text>
  <rect x="934" y="302" width="290" height="72" rx="6" fill="#fff" stroke="#27ae60"/>
  <text x="946" y="322" class="bt">audit_service</text>
  <text x="946" y="340" class="sm">append-only · AuditEvent</text>
  <text x="946" y="356" class="hi">ExecutionEvidence E-09</text>
  <rect x="56" y="386" width="1168" height="68" rx="6" fill="#eafaf1" stroke="#1e8449"/>
  <text x="68" y="408" class="bt">shared_contracts</text>
  <text x="68" y="426" class="sm">Pydantic v2 + jsonschema · 15 JSON Schema 加载 · 错误码 · DomainEvent 类型 · tenant/cell 上下文</text>
  <text x="68" y="444" class="hi">全模块依赖基底 · 禁止 import 其他 os_core</text>

  <!-- L2 AI -->
  <rect x="40" y="484" width="780" height="120" rx="8" fill="#fdebd0" stroke="#d68910" stroke-width="3"/>
  <rect x="40" y="484" width="780" height="26" rx="8" fill="#d35400"/>
  <text x="56" y="502" class="zt">src/server/os_core/ L2 体验层 — 唯一允许 LLM 的区域</text>
  <rect x="56" y="518" width="360" height="76" rx="6" fill="#fff" stroke="#d68910"/>
  <text x="68" y="538" class="bt">agent_orchestrator</text>
  <text x="68" y="556" class="sm">LangGraph StateGraph · LiteLLM 路由</text>
  <text x="68" y="572" class="sm">输出 DSL 计划 JSON · 禁止 import connector write</text>
  <rect x="432" y="518" width="360" height="76" rx="6" fill="#fff" stroke="#d68910"/>
  <text x="444" y="538" class="bt">license_service</text>
  <text x="444" y="556" class="sm">Pack 授权校验 · Phase 1 stub</text>
  <text x="444" y="572" class="hi">未授权 capability → 403</text>

  <!-- L1 -->
  <rect x="840" y="484" width="920" height="120" rx="8" fill="#d6eaf8" stroke="#2874a6" stroke-width="2"/>
  <rect x="840" y="484" width="920" height="26" rx="8" fill="#1a5276"/>
  <text x="856" y="502" class="zt">src/server/os_core/ L1 连接层 GIP（零 LLM）</text>
  <rect x="856" y="518" width="420" height="76" rx="6" fill="#fff" stroke="#2874a6"/>
  <text x="868" y="538" class="bt">connector_sdk</text>
  <text x="868" y="556" class="sm">httpx async · Registry · Blueprint Runtime</text>
  <text x="868" y="572" class="hi">10 LegacySystem + vendor 注册</text>
  <rect x="1292" y="518" width="420" height="76" rx="6" fill="#fff" stroke="#2874a6"/>
  <text x="1304" y="538" class="bt">mcp_gateway</text>
  <text x="1304" y="556" class="sm">MCP JSON-RPC · CMV tools/list</text>
  <text x="1304" y="572" class="hi">tools/call → DslPlan only · Y1 末 GA</text>

  <!-- integration -->
  <rect x="40" y="620" width="1720" height="88" rx="8" fill="#e8daef" stroke="#8e44ad" stroke-width="2"/>
  <rect x="40" y="620" width="1720" height="26" rx="8" fill="#7d3c98"/>
  <text x="56" y="638" class="zt">integration/ — GIP 外置（集成团队只改此目录 · Core tag 后 major 不变）</text>
  <text x="56" y="666" class="sm">catalog/ Blueprint 样例 · packs/ Graph/Conn/Skill Pack · tenants/ Override · tools/connector-agent/ S2 AI 辅助</text>
  <text x="56" y="684" class="hi">遵守 os_core-public-api · 仅 Registry + BlueprintRuntime 公开面 · edge-agent P1 PoC</text>

  <!-- infra -->
  <rect x="40" y="724" width="860" height="200" rx="8" fill="#fff2cc" stroke="#d6b656" stroke-width="2"/>
  <text x="56" y="752" class="bt">数据与中间件</text>
  <text x="56" y="776" class="sm">PostgreSQL 16 + SQLAlchemy 2.0 async + asyncpg — Data-L1/L2 · 全表 tenant_id</text>
  <text x="56" y="796" class="sm">W1 预埋：cell_id · placement_tier · connector_instances · outbox_events · tenant_quotas</text>
  <text x="56" y="816" class="sm">Redis/Tair — 会话 · 限流 · S0 进程内队列 → S1 Redis Streams（ADR-007）</text>
  <text x="56" y="836" class="sm">OSS — 语音/图片 30d TTL · 不进 PG</text>
  <text x="56" y="856" class="sm">Alembic 迁移 · pytest + httpx ASGI · contract tests</text>
  <text x="56" y="876" class="hi">B-Lite builtin 表也在 RDS · 模拟 Data-L0</text>
  <text x="56" y="900" class="hi">Data-L3 分析池选配 · 非默认</text>

  <!-- cloud -->
  <rect x="920" y="724" width="840" height="200" rx="8" fill="#ebf5fb" stroke="#2e86ab" stroke-width="2"/>
  <text x="936" y="752" class="bt">阿里云部署映射（Y1）</text>
  <text x="936" y="776" class="sm">生产：SLB → ECS(Uvicorn×4) → RDS 生产 + Redis + OSS</text>
  <text x="936" y="796" class="sm">测试：ECS(GitLab+Runner+staging+Redoc) → RDS 测试 · 禁止连生产库</text>
  <text x="936" y="816" class="sm">S0：单 Monolith + 单 RDS（1-10 tenant）</text>
  <text x="936" y="836" class="sm">S1：Pool + RLS + Outbox Worker · 读副本</text>
  <text x="936" y="856" class="sm">S2：Cell Router + 多 ECS/RDS · connector_worker 可选</text>
  <text x="936" y="876" class="sm">S3：Silo 独立栈复制 10 拓扑 · Enterprise 合同</text>
  <text x="936" y="900" class="hi">LiteLLM/ASR/OCR 出站 API · Cursor 研发本机</text>

  <!-- AI boundary -->
  <rect x="40" y="944" width="1720" height="130" rx="8" fill="#fff5f5" stroke="#e74c3c" stroke-width="2"/>
  <rect x="40" y="944" width="1720" height="26" rx="8" fill="#c0392b"/>
  <text x="56" y="962" class="zt">AI 边界与写链路（双极架构）</text>
  <text x="56" y="990" class="sm">终端智能极：说/拍/扫 → agent_orchestrator(LangGraph+LiteLLM) → DSL JSON</text>
  <text x="56" y="1010" class="sm">内核门禁极：graph(frozen) → rule(allow) → execution(Saga) → connector(httpx) → Legacy</text>
  <text x="56" y="1030" class="sm">禁止：Agent 直写 · graph/rule/execution/audit/connector 含 LLM · open-ended 自主 Agent</text>
  <text x="56" y="1050" class="hi">Harness 确认门 / dry_run 在 L3 · MCP tools/call 只产出 DslPlan · 不直写</text>
  <text x="56" y="1066" class="hi">D1 须同时满足 AC-BASE-001 52 P0 + AC-UX-001 P0</text>

  <!-- connector table -->
  <rect x="40" y="1090" width="1720" height="150" rx="8" fill="#ffffff" stroke="#2874a6" stroke-width="2"/>
  <text x="56" y="1118" class="bt">Connector 实现与 Path（Platform-L1）</text>
  <text x="56" y="1140" class="sm">Path A 哈森：conn-erp-kingdee-read/write + conn-dingtalk · Gate 0' 真实样本</text>
  <text x="56" y="1160" class="sm">Path B 通用：conn-mes-vendor-write + conn-erp-read · Bronze acme stub</text>
  <text x="56" y="1180" class="sm">Path C B-Lite：conn-mes-builtin · PG builtin_ledger 四表</text>
  <text x="56" y="1200" class="sm">其余 7 类 WMS/QMS/APS/PLM/CRM/CSM/OA：stub → Phase 2+ Pack</text>
  <text x="56" y="1220" class="hi">写级别 L0 只读 · L2 写+Revert · L3 通知 · 仅 execution_service 可 write()</text>

  <!-- ci -->
  <rect x="40" y="1256" width="1720" height="72" rx="8" fill="#eafaf1" stroke="#1e8449"/>
  <text x="56" y="1282" class="bt">CI 健身函数（W1 启用）</text>
  <text x="56" y="1302" class="sm">check_import_boundaries · check_openapi_schema_refs · check_cmv_sync · pytest AC-BASE-001 52 P0</text>
  <text x="56" y="1318" class="hi">uv workspace · Modular Monolith · Phase 3 前不拆微服务 · 禁止 Kafka Phase 1</text>

  <text x="{w//2}" y="1360" text-anchor="middle" class="t2">详见 文档/架构/技术架构图说明.md · ADR-001/002 · 2026-06-16</text>
</svg>'''
    _write("技术架构图", svg)


def data_architecture() -> None:
    w, h = 1800, 1100
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs><style>{STYLES}</style></defs>
  <rect width="{w}" height="{h}" fill="#ffffff"/>
  <text x="{w//2}" y="40" text-anchor="middle" class="t1">FactoryOS 数据架构图</text>
  <text x="{w//2}" y="66" text-anchor="middle" class="t2">Data-L0 ~ L3 · 云映射 · 写路径 · 三路径 · 规模预埋 · v1.1 · ADR-007</text>

  <rect x="40" y="88" width="900" height="68" rx="8" fill="#E8DAEF" stroke="#566573" stroke-width="1.5"/>
  <text x="56" y="114" class="bt">Data-L3  分析/数据池（选配）</text>
  <text x="56" y="136" class="sm">全量同步 · 看板 · 跨系统汇总 — 非 Overlay 默认 · 需书面采购 · 客户信任 + D1 结案后</text>

  <rect x="40" y="172" width="900" height="68" rx="8" fill="#D6EAF8" stroke="#566573" stroke-width="1.5"/>
  <text x="56" y="198" class="bt">Data-L2  业务缓存（按需 · TTL · 最小字段）</text>
  <text x="56" y="220" class="sm">工单快照 · 查询加速 · Graph 孪生引用 — 能读 ERP 就不落库</text>

  <rect x="40" y="256" width="900" height="68" rx="8" fill="#D5F5E3" stroke="#566573" stroke-width="1.5"/>
  <text x="56" y="282" class="bt">Data-L1  运行数据（必做 · RDS 生产/测试）</text>
  <text x="56" y="304" class="sm">Graph/Rule 版本 · Audit · ExecutionRecord · ExecutionEvidence · 对账 · License · shadow_mode</text>

  <rect x="40" y="340" width="900" height="68" rx="8" fill="#FDEBD0" stroke="#566573" stroke-width="1.5"/>
  <text x="56" y="366" class="bt">Data-L0  客户账本（权威 · 不在 FactoryOS PG，Overlay 不替代）</text>
  <text x="56" y="388" class="sm">ERP · MES · WMS · OA … — Path C 时 builtin_ledger 表在 RDS 模拟 L0</text>

  <text x="490" y="160" text-anchor="middle" class="hi">信任后选配</text>
  <text x="490" y="244" text-anchor="middle" class="hi">Connector read / 写前快照</text>
  <text x="490" y="328" text-anchor="middle" class="hi">写成功后记录 + 对账</text>
  <line x1="490" y1="156" x2="490" y2="172" stroke="#7f8c8d" stroke-width="2"/>
  <line x1="490" y1="240" x2="490" y2="256" stroke="#7f8c8d" stroke-width="2"/>
  <line x1="490" y1="324" x2="490" y2="340" stroke="#7f8c8d" stroke-width="2"/>

  <rect x="980" y="88" width="780" height="320" rx="10" fill="#F8F9F9" stroke="#2E86AB" stroke-width="2"/>
  <text x="1370" y="120" text-anchor="middle" class="bt" fill="#1a5276">阿里云资源映射</text>
  <text x="1000" y="152" class="bt">RDS 生产 / RDS 测试</text>
  <text x="1020" y="172" class="sm">Data-L1 + L2 · 全表 tenant_id · RLS@S1</text>
  <text x="1000" y="200" class="bt">OSS 对象存储</text>
  <text x="1020" y="220" class="sm">语音/图片 · 30d TTL · 不进 PG</text>
  <text x="1000" y="248" class="bt">Redis / Tair</text>
  <text x="1020" y="268" class="sm">会话/限流 · S1 Redis Streams · Outbox Worker</text>
  <text x="1000" y="296" class="bt">GitLab（测试域 ECS）</text>
  <text x="1020" y="316" class="sm">源码 · OpenAPI v1.1.1 · 15 Schema 真源</text>
  <text x="1000" y="344" class="bt">客户 ERP/MES（出站 HTTPS）</text>
  <text x="1020" y="364" class="sm">Data-L0 权威 · Connector 读写 · Edge Agent 私网</text>
  <text x="1000" y="392" class="bt">W1 规模预埋表（ADR-007）</text>
  <text x="1020" y="412" class="sm">tenants.cell_id · connector_instances · outbox_events · tenant_quotas</text>

  <rect x="40" y="430" width="1720" height="64" rx="8" fill="#EBF5FB" stroke="#2E86AB" stroke-width="1.5"/>
  <text x="56" y="454" class="bt" fill="#1a5276">写操作数据流</text>
  <text x="56" y="474" class="sm">H5 → Harness 确认 → Agent(DSL JSON) → Rule → Execution → Connector write → Data-L0 · 并行 Audit+ExecutionRecord+Evidence → Data-L1</text>
  <text x="56" y="490" class="sm">对账 Job read-back 核对 L0 · Revert 读 before 快照 → Compensator → Connector 写回 L0</text>

  <rect x="40" y="510" width="840" height="200" rx="8" fill="#FEF9E7" stroke="#B7950B" stroke-width="1.5"/>
  <text x="56" y="538" class="bt">测试域 vs 生产域</text>
  <text x="56" y="562" class="sm">测试 RDS：联调/UAT · 7 天备份 · 可重建 · 禁止连生产库</text>
  <text x="56" y="582" class="sm">生产 RDS：Shadow/真实工人 · 15 天备份 · 哈森 tenant 数据</text>
  <text x="56" y="602" class="sm">测试 ECS：GitLab + Runner + staging + Redoc</text>
  <text x="56" y="622" class="sm">生产 ECS：SLB + Nginx + API（无 GitLab）</text>
  <text x="56" y="642" class="sm">Cursor / LiteLLM 研发：本机 + staging</text>
  <text x="56" y="662" class="sm">多模态媒体：API → OSS SDK · 30d 生命周期</text>
  <text x="56" y="690" class="hi">原则：事实落 L0 · 操作证明落 L1 · 不全量抄 ERP</text>

  <rect x="900" y="510" width="860" height="200" rx="8" fill="#EAFAF1" stroke="#1E8449" stroke-width="1.5"/>
  <text x="916" y="538" class="bt">三条切入 · 同一数据流内核</text>
  <text x="916" y="566" class="sm">A 哈森灯塔：ERP 读+写 + 钉钉 → 报工事实落客户 ERP</text>
  <text x="916" y="594" class="sm">B 通用 MES 厂：MES 写 + ERP 读 → 报工事实落 MES</text>
  <text x="916" y="622" class="sm">C B-Lite：conn-mes-builtin → 事实落 RDS builtin 表（模拟 L0）</text>
  <text x="916" y="650" class="sm">部署：Pool 共享 RDS+RLS · Bridge 独立 schema · Silo 独立 RDS</text>
  <text x="916" y="678" class="sm">S0 单 Cell · S1 百级 · S2 Cell 路由 max 200/Cell · S3 千级+</text>
  <text x="916" y="698" class="hi">扩展：新厂商 = 新 Connector Pack，不改 execution 内核</text>

  <rect x="40" y="728" width="1720" height="56" rx="8" fill="#f4ecf7" stroke="#8e44ad"/>
  <text x="56" y="752" class="bt">按客户类型数据策略</text>
  <text x="56" y="772" class="sm">A 有 ERP：L0=客户 ERP · L1 必做 · L2 按需最小 · L3 不默认  |  有 MES 厂：L0=ERP+MES · 同上  |  C B-Lite：L0=builtin 表 · L1 必做 · Y1 默认不销售</text>

  <text x="{w//2}" y="820" text-anchor="middle" class="hi">详见 文档/架构/数据架构图说明.md · 06-数据边界 · 10-阿里云 · 15-研发资源清单</text>
  <text x="{w//2}" y="840" text-anchor="middle" class="t2">FactoryOS Data Architecture · v1.1 · 2026-06-16</text>
</svg>'''
    _write("数据架构图", svg, width=2000)


def core_module_architecture() -> None:
    w, h = 1800, 2000
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{STYLES}</style>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#34495e"/></marker>
  </defs>
  <rect width="{w}" height="{h}" fill="#fafbfc"/>
  <text x="{w//2}" y="42" text-anchor="middle" class="t1">FactoryOS 核心模块系统架构图</text>
  <text x="{w//2}" y="68" text-anchor="middle" class="t2">9 个 os_core 模块 · 依赖矩阵 · 写路径 · integration 外置 · v1.0 · 膨胀期守则</text>

  <!-- api -->
  <rect x="600" y="88" width="600" height="52" rx="8" fill="#d5e8d4" stroke="#82b366" stroke-width="2"/>
  <text x="{w//2}" y="120" text-anchor="middle" class="bt">src/server/api — FastAPI HTTP 适配（router/registry · modules · 无业务规则）</text>

  <!-- L3/L2 entry -->
  <rect x="80" y="160" width="520" height="64" rx="8" fill="#fadbd8" stroke="#c0392b"/>
  <text x="96" y="186" class="bt">L3 入口</text>
  <text x="96" y="206" class="sm">web-admin · h5-worker → /v1/* API</text>
  <rect x="620" y="160" width="520" height="64" rx="8" fill="#fdebd0" stroke="#d68910"/>
  <text x="636" y="186" class="bt">L2 体验（含 LLM）</text>
  <text x="636" y="206" class="sm">agent_orchestrator · license_service</text>
  <rect x="1160" y="160" width="560" height="64" rx="8" fill="#d6eaf8" stroke="#2874a6"/>
  <text x="1176" y="186" class="bt">L1 连接 + MCP</text>
  <text x="1176" y="206" class="sm">connector_sdk · mcp_gateway</text>

  <!-- L0 core -->
  <rect x="80" y="248" width="1640" height="200" rx="10" fill="#d5f5e3" stroke="#1e8449" stroke-width="3"/>
  <rect x="80" y="248" width="1640" height="28" rx="10" fill="#1e8449"/>
  <text x="96" y="268" class="zt">L0 信任内核 — graph → rule → execution → audit（写路径主轴）</text>
  <rect x="96" y="288" width="360" height="140" rx="8" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <text x="108" y="312" class="bt">graph_service</text>
  <text x="108" y="332" class="sm">职责：Graph 版本生命周期</text>
  <text x="108" y="350" class="sm">draft → in_review → frozen</text>
  <text x="108" y="368" class="sm">扩展：clone 新版本 + freeze</text>
  <text x="108" y="386" class="sm">验收：未 freeze 执行 L2 写 → 409</text>
  <text x="108" y="404" class="hi">可调：shared_contracts, audit</text>
  <rect x="476" y="288" width="360" height="140" rx="8" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <text x="488" y="312" class="bt">rule_engine</text>
  <text x="488" y="332" class="sm">职责：授权判定 allow/deny</text>
  <text x="488" y="350" class="sm">默认拒绝 · 匹配 allow 才过</text>
  <text x="488" y="368" class="sm">扩展：新 RuleSet 版本/Pack</text>
  <text x="488" y="386" class="sm">验收：无 allow → 403</text>
  <text x="488" y="404" class="hi">可调：shared_contracts, audit</text>
  <rect x="856" y="288" width="400" height="140" rx="8" fill="#fff" stroke="#27ae60" stroke-width="3"/>
  <text x="868" y="312" class="bt">execution_service ★ 唯一写 Legacy</text>
  <text x="868" y="332" class="sm">Saga · Revert/Compensator · 幂等键</text>
  <text x="868" y="350" class="sm">Shadow/dry_run · 对账 read-back</text>
  <text x="868" y="368" class="sm">ExecutionEvidence 产出</text>
  <text x="868" y="386" class="sm">扩展：新 DSL 动词 + Connector 映射</text>
  <text x="868" y="404" class="hi">可调：shared_contracts, audit, connector公开面, rule/graph公开面</text>
  <rect x="1276" y="288" width="428" height="140" rx="8" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <text x="1288" y="312" class="bt">audit_service</text>
  <text x="1288" y="332" class="sm">append-only 操作日志</text>
  <text x="1288" y="350" class="sm">AuditEvent · 不可篡改</text>
  <text x="1288" y="368" class="sm">扩展：新 event_type</text>
  <text x="1288" y="386" class="sm">每次写 append 记录</text>
  <text x="1288" y="404" class="hi">可调：shared_contracts only</text>

  <!-- shared_contracts -->
  <rect x="80" y="468" width="1640" height="56" rx="8" fill="#ecf0f1" stroke="#95a5a6" stroke-width="2"/>
  <text x="96" y="492" class="bt">shared_contracts — 类型/Schema/错误码/tenant上下文/DomainEvent · 全模块基底</text>
  <text x="96" y="512" class="hi">禁止 import 任何其他 os_core 模块</text>

  <!-- L1 detail -->
  <rect x="80" y="544" width="800" height="120" rx="8" fill="#d6eaf8" stroke="#2874a6" stroke-width="2"/>
  <text x="96" y="570" class="bt">connector_sdk（L1）</text>
  <text x="96" y="590" class="sm">Registry：tenant → ConnectorInstance 解析</text>
  <text x="96" y="608" class="sm">Blueprint Runtime · httpx async · 10 LegacySystem + vendor</text>
  <text x="96" y="626" class="sm">扩展：新 Connector 类 + integration/catalog 注册</text>
  <text x="96" y="644" class="hi">禁止 import execution 私有 · 仅 shared_contracts</text>
  <rect x="920" y="544" width="800" height="120" rx="8" fill="#d6eaf8" stroke="#2874a6" stroke-width="2"/>
  <text x="936" y="570" class="bt">mcp_gateway（L1）</text>
  <text x="936" y="590" class="sm">CMV → MCP tools/list · tools/call → DslPlan</text>
  <text x="936" y="608" class="sm">治理型 Agent 接入 · SEP-414 trace</text>
  <text x="936" y="626" class="sm">Y1 末内部 GA · 禁止直写 Legacy</text>
  <text x="936" y="644" class="hi">可调：shared_contracts, agent 公开面 · 禁止 execution 私有</text>

  <!-- L2 detail -->
  <rect x="80" y="684" width="800" height="100" rx="8" fill="#fdebd0" stroke="#d68910" stroke-width="2"/>
  <text x="96" y="710" class="bt">agent_orchestrator（L2 · 唯一 LLM）</text>
  <text x="96" y="730" class="sm">LangGraph FSM → DSL 计划 JSON · Skill Pack 挂载</text>
  <text x="96" y="748" class="sm">扩展：新 Skill FSM · 禁止 connector.write</text>
  <text x="96" y="766" class="hi">仅输出计划 → execution 执行</text>
  <rect x="920" y="684" width="800" height="100" rx="8" fill="#fdebd0" stroke="#d68910" stroke-width="2"/>
  <text x="936" y="710" class="bt">license_service（L2）</text>
  <text x="936" y="730" class="sm">Pack 是否已授权 · pack_id 登记</text>
  <text x="936" y="748" class="sm">未授权 Pack → 403 hard deny</text>
  <text x="936" y="766" class="hi">可调：shared_contracts</text>

  <!-- integration -->
  <rect x="80" y="804" width="1640" height="88" rx="8" fill="#e8daef" stroke="#8e44ad" stroke-width="2" stroke-dasharray="6"/>
  <text x="96" y="830" class="bt">integration/（非 os_core · GIP 外置 · 集成团队维护）</text>
  <text x="96" y="850" class="sm">catalog/ Blueprint · packs/ Graph/Conn/Skill · tenants/ Override · tools/connector-agent/</text>
  <text x="96" y="870" class="hi">遵守 os_core-public-api · Runtime 通过 Registry 加载 · 不触发 Core major</text>

  <!-- write path arrows -->
  <rect x="80" y="912" width="1640" height="72" rx="8" fill="#ebf5fb" stroke="#117a65" stroke-width="2"/>
  <text x="96" y="938" class="bt" fill="#117a65">运行时写路径（模块调用序）</text>
  <text x="96" y="960" class="sm">api → agent(计划) → graph(校验frozen) → rule(evaluate) → execution(run) → connector_sdk(write) → Legacy/Data-L0</text>
  <text x="96" y="976" class="sm">并行：execution → audit(append) · mcp_gateway 产出 DslPlan 后仍走 rule→execution · 禁止任何旁路</text>

  <!-- dependency matrix -->
  <rect x="80" y="1004" width="1640" height="200" rx="8" fill="#ffffff" stroke="#2c3e50" stroke-width="2"/>
  <rect x="80" y="1004" width="1640" height="26" rx="8" fill="#2c3e50"/>
  <text x="96" y="1022" class="zt">模块依赖矩阵（膨胀期守则 §2 · CI 强制）</text>
  <text x="96" y="1050" class="sm">shared_contracts ← 全部模块 · audit ← graph/rule/execution</text>
  <text x="96" y="1070" class="sm">execution ← connector_sdk公开面 + rule公开面 + graph公开面</text>
  <text x="96" y="1090" class="sm">agent ← shared_contracts_contracts only（禁止 execution 内部写路径）</text>
  <text x="96" y="1110" class="sm">mcp_gateway ← shared_contracts + agent公开面 · connector ← shared_contracts_contracts only</text>
  <text x="96" y="1130" class="sm">跨模块仅通过 api.py/public/ 暴露 · server/api 无业务规则 · integration/ 仅 Registry+BlueprintRuntime</text>
  <text x="96" y="1150" class="sm">禁止 extract L0 四模块为独立写服务 · connector_worker 不得持有写 Legacy 权限（ADR-007）</text>
  <text x="96" y="1170" class="hi">W1 预留 DomainEvent/outbox stub · S1 Redis Streams · 同进程函数调用 Core 1.0</text>

  <!-- capability matrix -->
  <rect x="80" y="1220" width="1640" height="200" rx="8" fill="#eafaf1" stroke="#1e8449" stroke-width="2"/>
  <text x="96" y="1248" class="bt">基座能力矩阵（模块 → 能力）</text>
  <text x="96" y="1272" class="sm">流程冻结 graph · 权限判定 rule · 受控写库 execution · 操作审计 audit · 撤回/幂等/试跑/对账 execution</text>
  <text x="96" y="1292" class="sm">多系统适配 connector · 自然语言入口 agent · Pack 授权 license · 治理型 MCP mcp_gateway</text>
  <text x="96" y="1312" class="sm">Gate 0：AC-BASE-001 52 P0 · tag core-v1.0.0 · 15 Schema + OpenAPI v1.1.1</text>
  <text x="96" y="1332" class="sm">可接工厂：上述 + 真实 Connector + frozen Graph · 不在基座：行业 Graph 内容/厂商协议细节</text>
  <text x="96" y="1352" class="sm">十个切入点：①Graph ②Rule ③Execution ④Connector ⑤Skill ⑥Harness ⑦freeze ⑧export ⑨新Pack ⑩import</text>
  <text x="96" y="1372" class="hi">完成标准见 16-OS核心基座 §9 · 能力追溯见 能力-模块包-模块追溯矩阵</text>

  <!-- external -->
  <rect x="80" y="1440" width="800" height="80" rx="8" fill="#fdedec" stroke="#e74c3c" stroke-dasharray="5"/>
  <text x="96" y="1466" class="bt">外部 Data-L0</text>
  <text x="96" y="1486" class="sm">ERP/MES/WMS/OA 或 builtin PG 表 · Connector 出站 HTTPS</text>
  <text x="96" y="1506" class="hi">Path A/B/C 仅 L1 目标不同</text>
  <rect x="920" y="1440" width="800" height="80" rx="8" fill="#fff2cc" stroke="#d6b656"/>
  <text x="936" y="1466" class="bt">Data-L1 RDS</text>
  <text x="936" y="1486" class="sm">Graph/Rule/Execution/Audit/Reconciliation · tenant_id 全表</text>
  <text x="936" y="1506" class="hi">PostgreSQL 16 · Alembic</text>

  <text x="{w//2}" y="1560" text-anchor="middle" class="t2">详见 文档/架构/核心模块架构图说明.md · 16-OS核心基座 §4 · ADR-001 · 2026-06-16</text>
</svg>'''
    _write("核心模块架构图", svg)


def main() -> None:
    system_architecture()
    technical_architecture()
    data_architecture()
    core_module_architecture()
    print("All architecture diagrams generated.")


if __name__ == "__main__":
    main()
