# API 文档

## 章节骨架

1. **概述** — API 的目的、功能、版本、认证方式
2. **快速入门** — 环境设置、最简调用示例
3. **认证与授权** — Token 获取、鉴权方式
4. **端点参考** — 每个端点的 URL、方法、参数、响应、错误码
5. **数据模型** — 请求/响应的数据结构定义
6. **高级主题** — 分页、批量操作、速率限制
7. **附录** — 错误码对照表、术语表、更新日志

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 调用示例 | `<card-codeblock mode="shell">` / `<card-codeblock mode="python">` |
| 端点参考 | `<card-collapse>` 每个端点折叠 |
| 数据模型 | `<table>` |
| 错误码 | `<table>` |
| 认证流程 | `<card-diagram type="mermaid">` |

## 轻量示范

```html
<!doctype lake>
<h1>用户服务 API 文档</h1>
<h2>概述</h2>
<p>用户服务 API 提供用户注册、登录、信息查询等功能。当前版本 v2.0。</p>
<h2>快速入门</h2>
<card-codeblock mode="shell">
curl -X POST https://api.example.com/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"xxx"}'
</card-codeblock>
<h2>认证与授权</h2>
<p>使用 Bearer Token 鉴权，Token 有效期 2 小时。</p>
<h2>端点参考</h2>
<card-collapse title="POST /v2/users — 创建用户">
<p>创建一个新用户账号。</p>
<p><strong>请求参数</strong></p>
<table><tbody>
<tr><td>username</td><td>string</td><td>必填</td><td>用户名</td></tr>
<tr><td>email</td><td>string</td><td>必填</td><td>邮箱</td></tr>
</tbody></table>
<p><strong>响应示例</strong></p>
<card-codeblock mode="json">
{"id": 1, "username": "admin", "created_at": "2024-01-01T00:00:00Z"}
</card-codeblock>
</card-collapse>
<h2>错误码</h2>
<table><tbody>
<tr><td>400</td><td>参数错误</td></tr>
<tr><td>401</td><td>未授权</td></tr>
<tr><td>404</td><td>资源不存在</td></tr>
</tbody></table>
```
