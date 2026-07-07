# e2e · Playwright 端到端

## 是什么

**壳层与导航** E2E；验证 router · layout · 关键页面可达，无后端依赖。

## 子路径

| 路径 | 说明 |
|------|------|
| `shell.spec.ts` | AppShell · Studio smoke |
| `../playwright.config.ts` | 浏览器与 baseURL |

## 门禁

```bash
pnpm e2e
pnpm check
```

## 变更纪律

- 用例须无 live API；业务联调归 STU plan
- 新目录须用户确认 + directory-readmes 登记

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md)
- [验收用例-WEB-PROFILE](../../../../contracts/acceptance/验收用例-WEB-PROFILE-前端工程自治.md)
