# api/request · HTTP 封装

全站 **唯一** HTTP 出口。`api/functions` 通过 `http` 发请求；**禁止** `modules/*` 直接 `fetch`。

## 文件

| 文件 | 职责 |
|------|------|
| `client.ts` | get/post/put/patch/del |
| `interceptors.ts` | X-Actor-Role · X-Actor-User-Id |
| `errors.ts` | ApiError · NetworkError |
| `types.ts` | RequestConfig |
