# Ax OS · Figma 导入套件

> **Cursor 接入（优先读）**：[Cursor-Figma接入手册.md](./Cursor-Figma接入手册.md)  
> MCP 配置：仓库根 `.cursor/mcp.json` · Agent 规则：`.cursor/rules/figma-ax-os-workflow.mdc`

## 策略（与 Cursor 合流）

```text
PRD v2.1 → factoryos-v2 线框 → Figma（Token/原型）→ Figma MCP → web-admin / h5-worker
```

第三方主链 = **Figma 官方远程 MCP**（`https://mcp.figma.com/mcp`）。

---

## 包含什么

| 文件 | 用途 |
|------|------|
| **`Cursor-Figma接入手册.md`** | Cursor 授权 · Day1 建文件 · Prompt 模板 |
| `ax-os-figma-kit.html` | 6 屏高保真 HTML → **html.to.design** |
| `design-tokens.json` | Figma Variables / Tokens Studio |
| `ax-os-dashboard-figma-ref.png` | L02 位图参考（**勿抄错误子导航**） |
| `ax-os-studio-prove-figma-ref.png` | Prove 布局参考（**六步名以 PRD 为准**） |
| `../ax-os-ui/ax-os-login-v4-smart-hub.png` | L01 登录定稿 |

---

## 方法一：HTML → Figma（推荐 · 可编辑图层）

1. 安装 Figma 插件 **[html.to.design](https://www.html.to.design/)**
2. 用 Chrome 打开 `ax-os-figma-kit.html`（本地 `file://` 即可）
3. 顶部切换屏幕（L01 / L02 / S02 / S05 / S06 / H06）
4. 插件 → **Import webpage**
5. Frame 命名对齐 ID（如 `L01-Login`）

## 方法二：Design Tokens → Variables

1. 安装 **Tokens Studio for Figma**
2. Load `design-tokens.json` → Create variables

## 方法三：Cursor Figma MCP（设计 ↔ 代码）

见 [Cursor-Figma接入手册.md](./Cursor-Figma接入手册.md)。授权后可 whoami / 建文件 / 读 Frame 落代码。

## 方法四：PNG 铺底

`../ax-os-ui/ax-os-login-v4-smart-hub.png` → 锁定描摹（登录定稿）。

---

## 建议 Figma File 结构

```text
Ax-OS-FactoryOS-v1.0
├── 00-Design-Tokens
├── 01-Components
├── 04-Screens-Web
├── 05-Screens-H5
└── 99-Prototype
```

## Day1 屏幕

| ID | 名称 | 尺寸 |
|----|------|------|
| L01 | 登录 | 1440×900 |
| L02 | 首页 Dashboard | 1440×900 |
| S02 | Studio Connect | 1440×900 |
| S05 | Studio Prove | 1440×900 |
| S06 | Studio Freeze | 1440×900 |
| H06 | 工人确认卡 | 390×844 |

完整 32 页见 PRD v2.1 §4。

## 局限

- Agent **不能代替** Figma OAuth（须 Settings → Connect）
- 错误素材门禁见 PRD §13 / 规则 `figma-ax-os-workflow`
