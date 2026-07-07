# pages · 业务页面（按 module-id 分目录）

**页面不单独注册制** — 路由真源在 `router/modules/{module-id}/registry.ts`；打开模块前先读 **`contracts/README.md`**（**改 registry 须同步更新契约**，harness 强制）。

| 板块 | 路径 | 登记内容 |
|------|------|----------|
| **路由** | `router/modules/{module-id}/` | lazy 指向 `@/pages/{module-id}/*.lazy` |
| **路由契约** | `router/contracts/README.md` | 全站路由登记索引 |
| **页面** | `pages/{module-id}/*.lazy.tsx` | 模块入口 |
| **页面契约** | `pages/{module-id}/contracts/README.md` | 追踪链 ↔ registry **须一致** |
| **私有组件** | `pages/{module-id}/components/` | 仅本模块 import |
| 状态 | `store/modules/{module-id}/` | `*.store.ts`（按需） |
| API | `api/functions/{module-id}/` | `*.fn.ts` |
| 布局 | `layout/modules/{domain}/` | 域壳组件 |
| **全局组件** | `@/components/` | ≥2 模块复用 UI |

## 目录约定

```text
pages/{module-id}/
├── contracts/README.md      # 功能 · 业务 · 用法 · 追踪链
├── {PageName}.lazy.tsx      # 懒加载页面入口
└── components/              # 模块私有组件库（见 components/README.md）
    └── README.md
```

## 组件反冗余

- 只在一步向导里用的表单/卡片 → `pages/studio-connect/components/`
- 两个以上模块都要用 → 提升到 `src/components/`
- **禁止** 同一组件既在全局又在模块内各存一份

## Studio 六步

| module-id | route name | path | contracts |
|-----------|------------|------|-----------|
| studio-shell | studio.home | /studio | [contracts/README.md](./studio-shell/contracts/README.md) |
| studio-connect | studio.connect | /studio/connect | [contracts/README.md](./studio-connect/contracts/README.md) |
| studio-discover | studio.discover | /studio/discover | [contracts/README.md](./studio-discover/contracts/README.md) |
| studio-map | studio.map | /studio/map | [contracts/README.md](./studio-map/contracts/README.md) |
| studio-prove | studio.prove | /studio/prove | [contracts/README.md](./studio-prove/contracts/README.md) |
| studio-freeze | studio.freeze | /studio/freeze | [contracts/README.md](./studio-freeze/contracts/README.md) |
| studio-export | studio.export | /studio/export | [contracts/README.md](./studio-export/contracts/README.md) |

新建：`pnpm create:module`

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
