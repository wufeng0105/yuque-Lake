# RESTful API 接口规范文档

> **文档版本**：v3.0.0
> **文档状态**：正式发布
> **编写日期**：2026-08-08
> **编写人**：架构组

---

## 一、设计原则

### 1.1 REST 核心原则

| 原则 | 说明 | 示例 |
|------|------|------|
| 无状态 (Stateless) | 每次请求必须包含所有必要信息，服务端不存储会话状态 | 使用 Token 而非 Session |
| 统一接口 (Uniform Interface) | 通过 HTTP 方法明确操作意图 | GET /users 获取用户列表 |
| 资源导向 (Resource-Oriented) | 将一切视为资源，用 URL 唯一标识 | /users/123 表示 ID 为 123 的用户 |
| 可缓存 (Cacheable) | 响应应明确是否可缓存 | 通过 Cache-Control 头控制 |
| 分层系统 (Layered System) | 客户端无需关心底层架构 | API Gateway 模式 |

### 1.2 URL 设计规范

| 资源操作 | HTTP方法 | URL | 说明 |
|---------|---------|-----|------|
| 用户列表 | GET | /api/v1/users | 复数名词，表示资源集合 |
| 单个用户 | GET | /api/v1/users/{id} | 路径参数标识特定资源 |
| 创建用户 | POST | /api/v1/users | 返回 201 Created |
| 全量更新 | PUT | /api/v1/users/{id} | 幂等操作 |
| 部分更新 | PATCH | /api/v1/users/{id} | 非幂等 |
| 删除用户 | DELETE | /api/v1/users/{id} | 返回 204 No Content |
| 用户订单 | GET | /api/v1/users/{id}/orders | 嵌套资源 |
| 搜索用户 | GET | /api/v1/users?role=admin&active=true | 查询参数过滤 |

**常见反模式**：

```
❌ GET /api/getUser?id=123          # 动词冗余
❌ POST /api/updateUser/123         # 用 POST 做更新
❌ GET /api/users/delete/123        # URL 包含动词
```

---

## 二、HTTP 方法语义

### 2.1 方法定义

| 方法 | 幂等性 | 安全性 | 语义 | 成功响应码 |
|------|--------|--------|------|-----------|
| GET | ✅ 是 | ✅ 是 | 获取资源，不应修改数据 | 200 OK |
| POST | ❌ 否 | ❌ 否 | 创建新资源（非幂等） | 201 Created |
| PUT | ✅ 是 | ❌ 否 | 全量替换资源（幂等） | 200 OK |
| PATCH | ❌ 否 | ❌ 否 | 部分更新资源 | 200 OK |
| DELETE | ✅ 是 | ❌ 否 | 删除资源 | 204 No Content |
| HEAD | ✅ 是 | ✅ 是 | 获取响应头（不含body） | 200 OK |
| OPTIONS | ✅ 是 | ✅ 是 | 获取支持的HTTP方法 | 200 OK |

### 2.2 幂等性详解

**幂等操作**：重复调用结果相同。

| 操作类型 | 幂等性 | 实现方式 |
|---------|--------|---------|
| GET /users/123 | 幂等 | 读取操作天然幂等 |
| PUT /users/123 | 幂等 | 全量替换，重复执行结果相同 |
| DELETE /users/123 | 幂等 | 删除已删除的资源返回204 |
| POST /users | 非幂等 | 每次调用创建新资源 |
| PATCH /users/123 | 非幂等 | 部分更新可能非幂等 |

---

## 三、状态码使用规范

### 3.1 状态码分类

| 分类 | 范围 | 含义 |
|------|------|------|
| 1xx | 100-199 | 信息性状态码 |
| 2xx | 200-299 | 成功状态码 |
| 3xx | 300-399 | 重定向状态码 |
| 4xx | 400-499 | 客户端错误 |
| 5xx | 500-599 | 服务端错误 |

### 3.2 常用状态码

| 状态码 | 名称 | 使用场景 | 响应体 |
|--------|------|---------|--------|
| 200 | OK | GET/PUT/PATCH 成功 | 资源数据 |
| 201 | Created | POST 创建成功 | 新建资源数据 |
| 204 | No Content | DELETE 成功 | 无响应体 |
| 400 | Bad Request | 请求参数错误 | 错误详情 |
| 401 | Unauthorized | 未认证/Token无效 | 错误信息 |
| 403 | Forbidden | 无权限访问 | 错误信息 |
| 404 | Not Found | 资源不存在 | 错误信息 |
| 409 | Conflict | 资源冲突 | 错误详情 |
| 422 | Unprocessable Entity | 请求格式正确但语义错误 | 验证错误详情 |
| 429 | Too Many Requests | 限流 | Retry-After 头 |
| 500 | Internal Server Error | 服务端异常 | 错误ID |
| 502 | Bad Gateway | 网关错误 | 错误信息 |
| 503 | Service Unavailable | 服务不可用 | Retry-After 头 |
| 504 | Gateway Timeout | 网关超时 | 错误信息 |

---

## 四、请求与响应格式

### 4.1 统一请求头

| Header | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | String | 是 | application/json |
| Authorization | String | 是 | Bearer {JWT Token} |
| X-Request-Id | String | 否 | 请求唯一标识，用于链路追踪 |
| X-App-Version | String | 否 | 客户端版本号 |
| Accept-Language | String | 否 | 语言偏好，默认 zh-CN |

### 4.2 统一响应格式

**成功响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "created_at": "2026-08-08T10:00:00Z"
  },
  "timestamp": "2026-08-08T10:00:00.000Z"
}
```

**错误响应**：

```json
{
  "code": 40001,
  "message": "参数验证失败",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    },
    {
      "field": "username",
      "message": "用户名长度必须在3-20个字符之间"
    }
  ],
  "timestamp": "2026-08-08T10:00:00.000Z",
  "request_id": "req-20260808-001"
}
```

**分页响应**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {"id": 1, "name": "用户1"},
      {"id": 2, "name": "用户2"}
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 150,
      "total_pages": 8,
      "has_next": true
    }
  },
  "timestamp": "2026-08-08T10:00:00.000Z"
}
```

### 4.3 分页参数规范

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | Integer | 1 | 页码，从1开始 |
| page_size | Integer | 20 | 每页条数，最大100 |
| sort | String | created_at:desc | 排序字段:排序方向 |
| fields | String | — | 返回指定字段，逗号分隔 |

---

## 五、错误码定义

### 5.1 业务错误码

| 错误码 | HTTP状态码 | 错误信息 | 说明 |
|--------|-----------|---------|------|
| 0 | 200 | success | 成功 |
| 40001 | 400 | 参数验证失败 | 请求参数不合法 |
| 40002 | 400 | 参数缺失 | 必填参数未提供 |
| 40003 | 400 | 参数格式错误 | 参数格式不符合要求 |
| 40101 | 401 | Token无效 | JWT Token过期或无效 |
| 40102 | 401 | Token已过期 | 需要刷新Token |
| 40301 | 403 | 无访问权限 | 用户无权访问该资源 |
| 40302 | 403 | 账号已禁用 | 账号被管理员禁用 |
| 40401 | 404 | 资源不存在 | 请求的资源未找到 |
| 40402 | 404 | 接口不存在 | 请求的API路径不存在 |
| 40901 | 409 | 资源已存在 | 创建时资源已存在 |
| 40902 | 409 | 版本冲突 | 乐观锁冲突 |
| 42201 | 422 | 业务规则校验失败 | 请求合法但违反业务规则 |
| 42901 | 429 | 请求过于频繁 | 触发限流 |
| 50001 | 500 | 服务器内部错误 | 未预期的异常 |
| 50002 | 500 | 数据库错误 | 数据库操作失败 |
| 50003 | 500 | 第三方服务异常 | 依赖的外部服务不可用 |
| 50301 | 503 | 服务维护中 | 系统维护中 |
| 50302 | 503 | 服务降级中 | 触发降级模式 |

---

## 六、认证与鉴权

### 6.1 JWT Token 认证流程

**认证流程**：

```
客户端                          API网关                        认证服务
  |                                |                              |
  |--- POST /api/v1/auth/login -->|                              |
  |                                |--- 转发到认证服务 ---------->|
  |                                |                              |--- 验证用户名密码
  |                                |                              |--- 生成JWT Token
  |                                |<-- 返回Token ---------------|
  |<-- 200 {token: "xxx"} --------|                              |
  |                                |                              |
  |--- GET /api/v1/users (Bearer) |                              |
  |                                |--- 验证Token签名和过期时间   |
  |                                |--- 提取用户信息              |
  |                                |--- 转发到用户服务            |
  |<-- 200 {data: [...]} ---------|                              |
```

### 6.2 Token 规范

**Access Token**：

| 属性 | 值 | 说明 |
|------|-----|------|
| 有效期 | 2小时 | 短期令牌 |
| 存储位置 | 客户端内存 | 避免localStorage |
| 传输方式 | Authorization Header | Bearer {token} |

**Refresh Token**：

| 属性 | 值 | 说明 |
|------|-----|------|
| 有效期 | 7天 | 长期令牌 |
| 存储位置 | HttpOnly Cookie | 防止XSS |
| 使用方式 | POST /auth/refresh | 刷新Access Token |

### 6.3 接口权限控制

| API路径 | 方法 | 需要认证 | 需要权限 | 说明 |
|---------|------|---------|---------|------|
| /api/v1/auth/login | POST | 否 | — | 登录接口 |
| /api/v1/auth/register | POST | 否 | — | 注册接口 |
| /api/v1/users | GET | 是 | user:read | 查看用户列表 |
| /api/v1/users | POST | 是 | user:create | 创建用户 |
| /api/v1/users/{id} | PUT | 是 | user:update | 更新用户 |
| /api/v1/users/{id} | DELETE | 是 | user:delete | 删除用户 |
| /api/v1/admin/* | * | 是 | admin | 管理后台接口 |

---

## 七、接口限流规范

### 7.1 限流策略

| 限流类型 | 策略 | 适用场景 | 实现 |
|---------|------|---------|------|
| 全局限流 | 10,000 QPS | 保护系统整体 | Sentinel |
| API级限流 | 500 QPS/API | 防止单接口过载 | Sentinel |
| 用户级限流 | 100 QPM/用户 | 防止单用户滥用 | Redis + Lua |
| IP级限流 | 60 QPM/IP | 防止恶意IP | Nginx limit_req |

### 7.2 限流响应

当触发限流时，返回 429 状态码：

```json
{
  "code": 42901,
  "message": "请求过于频繁，请稍后再试",
  "retry_after": 60,
  "timestamp": "2026-08-08T10:00:00.000Z"
}
```

响应头包含：

| Header | 说明 | 示例 |
|--------|------|------|
| X-RateLimit-Limit | 限制总数 | 100 |
| X-RateLimit-Remaining | 剩余次数 | 0 |
| X-RateLimit-Reset | 重置时间（秒） | 60 |
| Retry-After | 建议重试等待时间 | 60 |

---

## 八、接口版本管理

### 8.1 版本策略

采用 URL 路径版本控制：`/api/v{major_version}/resource`

| 版本 | 基线路径 | 状态 | 废弃日期 |
|------|---------|------|---------|
| v1 | /api/v1/ | 已废弃 | 2025-12-31 |
| v2 | /api/v2/ | 兼容维护 | 2026-12-31（计划） |
| v3 | /api/v3/ | 当前版本 | — |

### 8.2 版本兼容性规则

| 变更类型 | 是否需要新版本 | 兼容性 |
|---------|--------------|--------|
| 新增字段 | 否 | 向后兼容 |
| 删除字段 | 是 | 不兼容 |
| 修改字段类型 | 是 | 不兼容 |
| 新增接口 | 否 | 向后兼容 |
| 修改接口语义 | 是 | 不兼容 |

---

## 九、接口文档示例

### 9.1 用户注册接口

```
POST /api/v3/users/register
```

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| username | String | 是 | 用户名，3-20个字符 | zhangsan |
| password | String | 是 | 密码，8-32个字符，需包含大小写字母和数字 | Pass@1234 |
| email | String | 是 | 邮箱格式 | zhangsan@example.com |
| phone | String | 是 | 手机号，11位数字 | 13800138000 |
| captcha | String | 是 | 图形验证码 | a1b2c3 |

**请求示例**：

```json
{
  "username": "zhangsan",
  "password": "Pass@1234",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "captcha": "a1b2c3"
}
```

**成功响应**（201 Created）：

```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "id": 100001,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "phone": "138****8000",
    "created_at": "2026-08-08T10:00:00Z"
  },
  "timestamp": "2026-08-08T10:00:00.000Z"
}
```

**错误响应**（400 Bad Request）：

```json
{
  "code": 40001,
  "message": "参数验证失败",
  "errors": [
    {"field": "username", "message": "用户名已存在"},
    {"field": "email", "message": "邮箱格式不正确"}
  ],
  "timestamp": "2026-08-08T10:00:00.000Z",
  "request_id": "req-20260808-001"
}
```

### 9.2 获取订单列表接口

```
GET /api/v3/orders?page=1&page_size=20&status=paid&sort=created_at:desc
```

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| page | Integer | 否 | 页码，默认1 | 1 |
| page_size | Integer | 否 | 每页条数，默认20，最大100 | 20 |
| status | String | 否 | 订单状态过滤 | paid |
| start_date | Date | 否 | 开始日期 | 2026-08-01 |
| end_date | Date | 否 | 结束日期 | 2026-08-08 |
| sort | String | 否 | 排序字段:方向 | created_at:desc |

**成功响应**（200 OK）：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "DD2026080800001",
        "user_id": 100001,
        "status": "paid",
        "total_amount": 299.90,
        "items": [
          {"product_id": "P001", "name": "商品A", "quantity": 2, "price": 99.95},
          {"product_id": "P002", "name": "商品B", "quantity": 1, "price": 100.00}
        ],
        "created_at": "2026-08-08T10:00:00Z",
        "paid_at": "2026-08-08T10:05:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 150,
      "total_pages": 8,
      "has_next": true
    }
  },
  "timestamp": "2026-08-08T10:00:00.000Z"
}
```

---

## 十、附录

### 附录A：接口安全检查清单

| 检查项 | 要求 | 状态 |
|--------|------|------|
| HTTPS传输 | 所有API必须使用HTTPS | ✅ |
| 身份认证 | 除公开接口外必须携带Token | ✅ |
| 权限校验 | 每个接口需校验用户权限 | ✅ |
| 参数校验 | 所有入参需进行类型和范围校验 | ✅ |
| SQL注入防护 | 使用参数化查询，禁止SQL拼接 | ✅ |
| XSS防护 | 输出数据进行HTML转义 | ✅ |
| CSRF防护 | 非GET请求校验CSRF Token | ✅ |
| 限流防护 | 配置接口级和用户级限流 | ✅ |
| 敏感数据脱敏 | 响应中手机号、身份证号等脱敏 | ✅ |
| 审计日志 | 记录所有写操作的审计日志 | ✅ |

---

*本文档为 API 接口规范文档，仅供开发团队内部使用。*
