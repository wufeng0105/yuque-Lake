# 语雀 API — Lake 文档操作

## 认证

所有 API 请求需要 `X-Auth-Token` 头：

```python
headers = {
    "X-Auth-Token": "<your_token>",
    "Content-Type": "application/json",
    "User-Agent": "yuque-cli"
}
```

获取 Token：语雀 → 设置 → Token

## API 端点

基础 URL：`https://www.yuque.com/api/v2`

## 文档操作

### 创建 Lake 文档

```python
import requests

data = {
    "title": "文档标题",
    "slug": "doc-slug",
    "format": "lake",           # 关键：指定 Lake 格式（默认 markdown）
    "public": 1,                # 0=私有, 1=公开
    "body": "<!doctype lake><h1>标题</h1><p>内容</p>"
}

response = requests.post(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs",
    json=data,
    headers=headers
)
```

### 获取文档

```python
# 获取文档（默认返回 Lake 格式）
response = requests.get(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs/{slug}",
    headers=headers
)

# raw=1 返回 Markdown 格式
response = requests.get(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs/{slug}?raw=1",
    headers=headers
)
```

### 更新文档

```python
data = {
    "title": "新标题",
    "body": "<!doctype lake><h1>新标题</h1><p>新内容</p>"
}

response = requests.put(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs/{doc_id}",
    json=data,
    headers=headers
)
```

> 更新使用 `doc_id`（数字 ID），不是 `slug`。

### 删除文档

```python
response = requests.delete(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs/{doc_id}",
    headers=headers
)
```

### 列出知识库文档

```python
response = requests.get(
    "https://www.yuque.com/api/v2/repos/{namespace}/docs",
    headers=headers
)
```

## 知识库操作

### 列出知识库

```python
response = requests.get(
    "https://www.yuque.com/api/v2/users/{user_id}/repos",
    headers=headers
)
```

### 获取用户信息

```python
response = requests.get(
    "https://www.yuque.com/api/v2/user",
    headers=headers
)
```

## 响应格式

所有 API 返回 JSON：

```json
{
  "data": {
    "id": 12345,
    "title": "文档标题",
    "slug": "doc-slug",
    "format": "lake",
    "body": "<!doctype lake>...",
    "body_asl": "<!doctype lake>...",
    "word_count": 1000,
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z"
  }
}
```

## 常见错误

| HTTP 状态码 | 原因 | 解决方法 |
|-------------|------|----------|
| 401 | Token 无效或过期 | 重新生成 Token |
| 403 | 无权限 | 检查知识库权限 |
| 404 | namespace 或 slug 不存在 | 检查路径 |
| 429 | 请求频率超限 | 降低请求频率 |
