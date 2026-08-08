---
name: yuquelake
description: Use when working with Yuque Lake format — writing Lake HTML documents, generating .lake or .lakebook files, using Lake card tags, creating codeblocks/images/math/mermaid cards, or interacting with Yuque API for Lake documents. Also use when the user mentions "Lake格式", ".lake文件", "语雀卡片", "lakebook", or wants to understand/generate Yuque's native document format.
---

# Yuque Lake 格式工具

## 概述

Lake 是语雀（Yuque）的私有文档格式，本质是 HTML 的超集。本 skill 指导 AI 正确编写 Lake 格式文档、使用 Card 伪标签、生成 `.lake`/`.lakebook` 文件，以及通过语雀 API 操作 Lake 文档。

## 何时使用

- 用户要求编写或生成 Lake 格式文档（`.lake` 文件）
- 用户要求创建语雀知识库导入包（`.lakebook` 文件）
- 用户提到 "Lake格式"、".lake文件"、"语雀卡片"、"lakebook"
- 用户要在语雀文档中插入代码块、图片、公式、图表等 Card 内容
- 用户要通过语雀 API 创建/更新 Lake 格式文档
- 用户要理解或分析 Lake 格式的文档内容

## 何时不使用

- 用户仅要求将 Markdown 转换为语雀格式 → 使用 `yuque-markdown` skill
- 用户仅询问语雀平台功能（非格式转换/生成）
- 用户要求编辑已有语雀文档（非生成新文档）

## Lake 格式核心规则

### 1. 文档声明

每个 Lake 文档以 `<!doctype lake>` 开头：

```html
<!doctype lake>
<h1>文档标题</h1>
<p>正文内容。</p>
```

### 2. 标准 HTML 标签

Lake 支持标准 HTML 标签，与 HTML 的差异：
- 标题支持 **H1-H7**（比 HTML 多一个 H7）
- 表格只用 `<tbody>`，**不用 `<thead>`**
- 文本格式：`<strong>`, `<em>`, `<del>`, `<u>`, `<sup>`, `<sub>`, `<code>`
- 列表：`<ul>`, `<ol>`, 嵌套列表
- 引用：`<blockquote>`
- 链接：`<a href="...">`

### 3. Card 伪标签（AI 编写方式）

AI **不直接写 `<card>` 标签**（URL 编码极易出错），而是写伪标签，由程序转换：

| 伪标签 | 说明 | 示例 |
|--------|------|------|
| `<card-codeblock mode="python">code</card-codeblock>` | 代码块 | 见下方示例 |
| `<card-image src="url" name="说明"/>` | 图片 | |
| `<card-math code="E=mc^2"/>` | 数学公式 | |
| `<card-yuque src="/doc/xxx" title="标题"/>` | 语雀内部链接 | |
| `<card-file src="url" name="文件名.pdf"/>` | 附件 | |
| `<card-hr/>` | 水平分割线 | |
| `<card-label label="重要"/>` | 标签/徽章 | |
| `<card-mermaid>graph TD</card-mermaid>` | Mermaid 图表 | |
| `<card-plantuml>@startuml</card-plantuml>` | PlantUML 图表 | |
| `<card-collapse title="标题">内容</card-collapse>` | 折叠面板 | |
| `<card-bookmark src="url"/>` | 书签/链接卡片 | |
| `<card-video src="url"/>` | 视频 | |
| `<card-audio src="url"/>` | 音频 | |

完整 Card 类型列表见 [references/card-reference.md](references/card-reference.md)。

### 4. 编码示例

AI 写伪标签：
```html
<card-codeblock mode="python" name="示例代码">
def hello():
    print("Hello, World!")
</card-codeblock>
```

程序转换后（Lake 格式）：
```html
<card name="codeblock" value="data:%7B%22code%22%3A%22def%20hello...%22%7D"></card>
```

## 工作流

### 场景 A：生成单篇 .lake 文件

1. 确定文档内容结构（标题、段落、代码块等）
2. 用伪标签编写 Lake HTML 内容
3. 添加 `<!doctype lake>` 声明
4. 保存为 `.lake` 文件
5. 可直接拖入语雀编辑器导入

### 场景 B：生成 .lakebook 知识库包

1. 为每篇文档编写 Lake HTML 内容（场景 A）
2. 确定知识库目录结构（TOC）
3. 生成 `$meta.json`（含 tocYml YAML）
4. 为每篇文档生成 JSON 条目
5. 打包为 tar 归档

详见 [references/lakebook-structure.md](references/lakebook-structure.md)。

### 场景 C：通过 API 创建 Lake 文档

```python
import requests

headers = {"X-Auth-Token": "<token>", "Content-Type": "application/json"}
data = {
    "title": "文档标题",
    "slug": "doc-slug",
    "format": "lake",  # 关键：指定 Lake 格式
    "public": 1,
    "body": "<!doctype lake><h1>标题</h1><p>内容</p>"
}
requests.post("https://www.yuque.com/api/v2/repos/{namespace}/docs",
              json=data, headers=headers)
```

## 常见错误

| 错误 | 修复方法 |
|------|----------|
| 手动写 `<card>` 标签的 URL 编码 | 永远用伪标签，让程序转换 |
| 表格使用 `<thead>` | Lake 不用 `<thead>`，所有行放 `<tbody>` |
| 忘记 `<!doctype lake>` 声明 | 文档开头必须加声明 |
| 文本中未转义 `<`, `>`, `&` | 转义为 `&lt;`, `&gt;`, `&amp;` |
| 混淆 .lake 和 .lakebook | .lake 是单文档，.lakebook 是知识库打包 |
| body 和 body_asl 字段混淆 | Lake 格式时两者内容相同，body_asl 是实际展示字段 |

## 参考文件

- [references/lake-format-spec.md](references/lake-format-spec.md) — 完整 Lake 格式规范
- [references/card-reference.md](references/card-reference.md) — 全部 30+ Card 类型伪标签语法
- [references/lakebook-structure.md](references/lakebook-structure.md) — .lakebook 打包结构
- [references/yuque-api.md](references/yuque-api.md) — 语雀 API Lake 文档操作
