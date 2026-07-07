# WEB-PROFILE Test 红测（repo 级）

**非** WEB-PROFILE 验收盘。真源验收盘：

```bash
cd src/apps/web-admin && ./scripts/activate.sh
```

本目录 pytest 仅用于 Test Agent **编码前红测**（W-11 等），驱动 Dev 实现；**禁止** 在 STU `gate step` 中替代 App harness。
