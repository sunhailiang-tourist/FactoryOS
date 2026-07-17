# Cursor × Figma 接入手册（Ax OS）

| 项 | 内容 |
|----|------|
| **策略** | PRD → `factoryos-v2` 线框 → Figma（Token/原型）→ Figma MCP → 真前端 |
| **MCP** | 远程官方 `https://mcp.figma.com/mcp`（推荐） |
| **仓库配置** | `.cursor/mcp.json` |
| **Agent 规则** | `.cursor/rules/figma-ax-os-workflow.mdc` |
| **PRD** | `docs/设计/Ax-OS-产品PRD完整版-可还原原型-v2.0.md`（v2.1） |

---

## 一、一次性接入（约 5 分钟 · 必须你点授权）

> Agent **无法代替你完成 Figma OAuth**。下面 1～4 须在本机 Cursor UI 完成。

### 1. 确认仓库 MCP 配置

本仓库已写入：

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

路径：`.cursor/mcp.json`

### 2. 启用 Figma 插件（推荐）

在 Cursor Agent 聊天输入：

```text
/add-plugin figma
```

点 **Add Plugin**，装官方 Figma 插件（含 MCP + Skills）。

### 3. 连接并登录

1. `Cmd + Shift + P` → **Cursor Settings**  
2. 打开 **Tools & MCP**  
3. 找到 **figma** → 点 **Connect** / **Authenticate**  
4. 浏览器登录 Figma 账号并授权  

成功标志：MCP 列表显示 figma 为 **enabled / connected**（绿色）。

### 4. 重启一次 Agent 会话

新开一条 Agent 对话，发送：

```text
用 Figma MCP 调用 whoami，确认我已登录。
```

若返回 plan / 用户信息 → 接入完成。

---

## 二、Day 1 设计文件（按策略）

### 2.1 在 Figma 新建文件

文件名建议：`Ax-OS-FactoryOS-v1.0`

页面结构：

```text
00-Design-Tokens
01-Components
04-Screens-Web
05-Screens-H5
99-Prototype
```

### 2.2 导入 Token

1. Figma 安装 **Tokens Studio**  
2. Load：`docs/设计/figma/design-tokens.json`  
3. Create variables（Color / Spacing / Radius）

### 2.3 灌入线框（最快）

**路径 A（推荐）**：html.to.design

1. Chrome 打开 `docs/设计/figma/ax-os-figma-kit.html`  
2. 插件 html.to.design → Import  
3. 帧命名：`L01-Login` · `L02-Dashboard` · `S02-Connect` · `S05-Prove` · `S06-Freeze` · `H06-Confirm`

**路径 B**：对照 `factoryos-v2/*.html` 在 Cursor 里让 Agent 经 MCP `use_figma` 画关键 Frame（需已 Connect）。

### 2.4 登录定稿像素对齐

铺底：`docs/设计/ax-os-ui/ax-os-login-v4-smart-hub.png`  
文案必须是 **智能中枢系统**（禁用 V3「让制造不再黑箱」）。

### 2.5 原型连线（主线）

按 PRD §8：

- 主线 A：W-01→…→W-09  
- 主线 B：H-00→…→H-07  

---

## 三、Cursor 内常用 Prompt

### 3.1 确认接入

```text
调用 Figma MCP whoami，列出可用 plan。
```

### 3.2 从 Frame 落地代码

```text
Figma Frame：<粘贴链接>
按 docs/设计/Ax-OS-产品PRD完整版-可还原原型-v2.0.md 与 design-tokens.json，
实现到 src/apps/web-admin 对应路由；五域 IA 不可改；禁止新造侧栏文案。
```

### 3.3 从 PRD 补画布

```text
读取 PRD §4.1 核心 22 页与 factoryos-v2，
在 Figma 文件 <file_key> 的 04-Screens-Web 补齐缺失 Frame；
Studio 六步名必须为 Connect/Discover/Map/Prove/Freeze/Export。
```

### 3.4 设计→代码验收

```text
对比 Figma 选中 Frame 与当前 web-admin 页面：
列出 Token / 间距 / 文案 / 禁用态差异；只改 UI，不改业务规则。
```

---

## 四、与研发门禁的关系

| 层 | 工具 | 说明 |
|----|------|------|
| 规格 | PRD + 白皮书 | 产品真源 |
| 设计 | Figma + MCP | UX / 原型 |
| 线框运行时 | `factoryos-v2` HTML | 最快可点 |
| 编码 | SH-步步流 / WebDev | 写 `src/**` 仍须 gate |

Figma 接入 **不跳过** `gate plan` / `gate start`。

---

## 五、故障排除

| 现象 | 处理 |
|------|------|
| Tools & MCP 无 figma | 检查 `.cursor/mcp.json`；或 `/add-plugin figma` |
| Connect 失败 | 换网络 / 重新 OAuth；确认 Figma 账号有权建文件 |
| Agent 调不到 MCP | 新开对话；Settings 确认 figma 已 Enabled |
| 画出错误侧栏 | 引用规则 `figma-ax-os-workflow`；禁止参考 V3 dashboard PNG |
| 六步名变成 Simulate/Publish | 以 PRD / Integration-Studio 规格为准，删错误步进 |

---

## 七、已创建文件（2026-07-14）

| 项 | 值 |
|----|-----|
| **文件名** | Ax-OS-FactoryOS-v1.0 |
| **链接** | https://www.figma.com/design/PsgQYgwsLH1Vz2Z6LGLk8i |
| **fileKey** | `PsgQYgwsLH1Vz2Z6LGLk8i` |
| **团队** | FactoryOS（`team::1658790803485036225`） |
| **FigJam** | https://www.figma.com/board/x4eS1zdZCeucLavjVthzAN |
| **账号** | 孙海亮 |

### 已建页面

- `00-Cover` · `00-Design-Tokens`（15 Variables）· `01-Components` · `04-Screens-Web` · `05-Screens-H5` · `99-Prototype`

### Day1 Frame

**Web**：L01-Login · L02-KPI-Dashboard · S02-Studio-Connect · S05-Studio-Prove · S06-Studio-Freeze  

**H5**：H00-Entry · H03-Confirm · H07-Done  

### 下一步（任选）

1. 用 html.to.design / `generate_figma_design` 把 `factoryos-v2` 高保真灌入对应 Frame  
2. 在 Figma 里 Prototype 连主线 A/B  
3. 粘贴 Frame 链接给 Cursor → 落地 `web-admin` / `h5-worker`  

---

## 六、你完成授权后回复我

（历史步骤 · 已完成 Connect）

下一步我将：`whoami` → 创建 `Ax-OS-FactoryOS-v1.0` → 写入 Token 页结构 → 按 PRD 建 Day1 关键 Frame 骨架。
