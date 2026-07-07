# devkit · AI 研发流内核快照

## 是什么

standalone 迁出后 **DevKit AI 规则与 pipeline 落盘** 的只读快照根；umbrella 下仍指向 FactoryOS 根 `.cursor/factoryos/`。

## 子路径

| 路径 | 说明 |
|------|------|
| `kernel/factoryos/` | INDEX · GATES · STEP0 · DEV/TEST/VERIFY 细则快照 |
| `kernel/factoryos/PATH-SNAPSHOT.md` | 结构快照（与 umbrella 同构 · 禁词对账） |

## 门禁

```bash
./scripts/activate.sh
python scripts/devkit/bootstrap_standalone.py <app> <repo>
pnpm test:w11
```

## 变更纪律

- **禁止** 手改 `kernel/` 业务规则；真源在 FactoryOS `.cursor/factoryos/`
- 刷新快照须 **用户确认** + umbrella 同步 + `contracts/directory-readmes.yaml`
- 迁出后仅通过 `bootstrap_standalone.py` 覆盖 `.cursor/`

## 相关文档

- [README.md](../README.md) · [ENGINEERING.md](../ENGINEERING.md)
- [DEVKIT.md](../../../../.cursor/factoryos/DEVKIT.md)
