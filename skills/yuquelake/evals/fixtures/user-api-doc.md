# 用户服务 API 文档

## 概述

用户服务 API 提供用户注册、登录、信息查询等功能。当前版本 v2.0。

## 认证方式

使用 Bearer Token 鉴权，Token 有效期 2 小时。

## 端点列表

### POST /v2/users — 创建用户

创建一个新用户账号。

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名，3-20字符 |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码，至少8位 |

**响应示例**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /v2/users/:id — 查询用户

根据用户ID查询用户信息。

**响应示例**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "status": "active"
}
```

## 错误码

| 状态码 | 说明 |
|--------|------|
| 400 | 参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如用户名已存在） |
| 500 | 服务器内部错误 |
