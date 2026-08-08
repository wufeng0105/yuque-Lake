# 语雀 Lake 格式规范（完整版）

> 来源：基于 `@alipay/lakex-doc` v1.64.0 + VSCode Lake 编辑器插件 + Yuque SDK 分析整理

## 1. 概述

Lake 是语雀（Yuque）的私有文档格式，本质是 **HTML 的超集**：
- 标准 HTML 标签（`<h1>`-`<h7>`, `<p>`, `<table>`, `<ul>`, `<ol>` 等）
- 自定义 `<card>` 标签（代码块、图片、公式等高级功能）
- 文档声明 `<!doctype lake>`

## 2. 文档结构

### 2.1 完整 .lake 文件

```html
<!doctype lake>
<h1>文档标题</h1>
<p>正文段落。</p>
<card name="codeblock" value="data:%7B%22code%22%3A%22...%22%7D"></card>
```

### 2.2 最小化结构

```html
<!doctype lake>
<h1>标题</h1>
<p>内容</p>
```

## 3. 标签体系

### 3.1 标题层级（H1-H7）

Lake 支持 H1 ~ H7（HTML 标准只到 H6）：

```html
<h1>一级标题</h1>  <!-- 文档主标题，每篇仅一个 -->
<h2>二级标题</h2>  <!-- 一级章节 -->
<h3>三级标题</h3>  <!-- 二级章节 -->
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>
<h7>七级标题</h7>
```

### 3.2 文本格式

```html
<p>普通段落文本</p>
<p><strong>加粗文本</strong></p>
<p><em>斜体文本</em></p>
<p><del>删除线</del></p>
<p><u>下划线</u></p>
<p>上标：x<sup>2</sup></p>
<p>下标：H<sub>2</sub>O</p>
<p>行内代码：<code>variable_name</code></p>
```

### 3.3 段落与引用

```html
<p>普通段落</p>
<blockquote>引用块内容</blockquote>
```

### 3.4 链接

```html
<a href="https://example.com">外部链接</a>
<card name="yuque" value="data:...">语雀内部链接</card>
```

### 3.5 列表

```html
<!-- 无序列表 -->
<ul><li>第一项</li><li>第二项</li></ul>

<!-- 有序列表 -->
<ol><li>第一步</li><li>第二步</li></ol>

<!-- 嵌套列表 -->
<ul><li>父项<ul><li>子项</li></ul></li></ul>
```

### 3.6 表格

```html
<table>
  <tbody>
    <tr><td>表头1</td><td>表头2</td></tr>
    <tr><td>数据1</td><td>数据2</td></tr>
  </tbody>
</table>
```

> ⚠️ Lake 表格使用 `<tbody>` 包裹所有行（包括表头），不使用 `<thead>`。

## 4. Card 标签系统

### 4.1 基本结构

```html
<card name="类型名" value="data:URL编码的JSON"></card>
```

### 4.2 value 属性编码规则

1. 构造 JSON 对象：`{"key": "value"}`
2. URL 编码整个 JSON 字符串（使用 `encodeURIComponent`）
3. 添加 `data:` 前缀

> ⚠️ 不要手动编码！使用 `lake-generator.py` 或编辑器自动处理。

### 4.3 完整 Card 类型列表（30+）

| name 值 | 说明 | 主要 JSON 字段 |
|---------|------|----------------|
| `codeblock` | 代码块 | `code`, `mode`, `name` |
| `image` | 图片 | `src`, `name` |
| `math` | 数学公式（KaTeX） | `code` |
| `file` | 附件 | `src`, `name` |
| `hr` | 水平分割线 | - |
| `label` | 标签/徽章 | `label` |
| `yuque` | 语雀内部文档链接 | `src`, `title` |
| `table` | 增强表格 | 表格数据 |
| `bookmark` | 书签/链接卡片 | URL 元数据 |
| `attachment` | 附件（同 file） | 附件数据 |
| `video` | 视频 | 视频 URL/ID |
| `audio` | 音频 | 音频 URL/ID |
| `status` | 状态标签 | 状态文本/颜色 |
| `note` | 笔记/提示框 | 提示内容 |
| `gantt` | 甘特图 | 甘特图数据 |
| `mermaid` | Mermaid 图表 | Mermaid 代码 |
| `plantuml` | PlantUML 图表 | PlantUML 代码 |
| `html` | 原始 HTML | HTML 代码 |
| `collapse` | 折叠面板 | 标题+内容 |
| `quote` | 引用卡片 | 引用内容 |
| `catalog` | 目录（TOC） | 自动生成 |
| `blockquote` | 增强引用块 | 引用内容 |
| `divider` | 分割线（同 hr） | - |
| `time` | 时间/日期 | 日期值 |
| `calendar` | 日历 | 日历数据 |
| `localdoc` | 本地文档引用 | 本地路径 |
| `api` | API 文档 | API 定义 |
| `codepen` | CodePen 嵌入 | Pen ID |
| `bilibili` | B站视频 | 视频 ID |
| `youtube` | YouTube 视频 | 视频 ID |
| `drawio` | Draw.io 绘图 | XML 数据 |
| `minder` | 思维导图 | 思维导图数据 |

### 4.4 编码示例

#### 代码块
```html
<!-- AI 写（伪标签） -->
<card-codeblock mode="python" name="示例代码">
def hello():
    print("Hello, World!")
</card-codeblock>

<!-- 程序转换后（Lake 格式） -->
<card name="codeblock" value="data:%7B%22code%22%3A%22def%20hello%28%29%3A%5Cn%20%20%20%20print%28%22Hello%2C%20World%21%22%29%5Cn%22%2C%22mode%22%3A%22python%22%2C%22name%22%3A%22%E7%A4%BA%E4%BE%8B%E4%BB%A3%E7%A0%81%22%7D"></card>
```

#### 图片
```html
<!-- AI 写（伪标签） -->
<card-image src="https://example.com/screenshot.png" name="操作界面截图"></card-image>

<!-- 程序转换后 -->
<card name="image" value="data:%7B%22src%22%3A%22https%3A//example.com/screenshot.png%22%2C%22name%22%3A%22%E6%93%8D%E4%BD%9C%E7%95%8C%E9%9D%A2%E6%88%AA%E5%9B%BE%22%7D"></card>
```

## 5. Lakebook 打包结构

### 5.1 文件格式

`.lakebook` 本质是一个 **tar 归档文件**（可用解压工具打开）。

### 5.2 内部结构

```
knowledge-base.lakebook (tar archive)
├── $meta.json          # 元数据（包含 tocYml）
├── chapter-uuid-1.json  # 文档条目 1
├── chapter-uuid-2.json  # 文档条目 2
└── ...
```

### 5.3 $meta.json 结构

```json
{
  "meta": "{\"book\":{\"path\":\"...\",\"public\":0,\"tocYml\":\"...\",\"type\":\"...\"},\"config\":{\"endecryptType\":0},\"docs\":[],\"version\":\"...\"}",
  "meta_digest": "..."
}
```

**meta.book 字段**：
- `path`: 知识库路径
- `public`: 0=私有, 1=公开
- `tocYml`: YAML 格式的目录结构（见下方）
- `type`: 类型

### 5.4 tocYml 结构（YAML）

```yaml
- type: DOC          # DOC=文档, TITLE=仅标题
  title: 第一章
  uuid: abc-123
  url: chapter-1      # 对应 .json 文件名
  prev_uuid: ''
  sibling_uuid: ''
  child_uuid: ''
  parent_uuid: ''
  doc_id: 12345
  level: 0           # 0=根层级
  id: 12345
  open_window: 1
  visible: 1
```

### 5.5 文档条目 JSON 结构

```json
{
  "doc": {
    "body": "<!doctype lake>...",           // Lake 格式内容（HTML）
    "body_asl": "<!doctype lake>...",       // 实际展示内容（ASL = Application Specific Language）
    "body_draft": "...",                    // 草稿内容
    "body_draft_asl": "...",                // 草稿 ASL
    "content_updated_at": "2024-01-01T00:00:00.000Z",
    "cover": "",
    "created_at": "2024-01-01T00:00:00.000Z",
    "description": "",
    "editor_meta": "...",
    "first_published_at": "2024-01-01T00:00:00.000Z",
    "format": "lake",                       // 文档格式: "markdown" 或 "lake"
    "id": 12345,
    "public": 1,
    "published_at": "2024-01-01T00:00:00.000Z",
    "slug": "chapter-1",
    "status": 0,
    "title": "第一章",
    "updated_at": "2024-01-01T00:00:00.000Z",
    "user_id": 67890,
    "word_count": 1000
  },
  "doc_digest": "..."
}
```

## 6. API 操作

### 6.1 创建 Lake 文档

```javascript
POST /api/v2/repos/{namespace}/docs
{
  "title": "文档标题",
  "slug": "doc-slug",
  "format": "lake",           // 指定 Lake 格式（默认 markdown）
  "public": 1,                // 0=私有, 1=公开
  "body": "<!doctype lake><h1>标题</h1><p>内容</p>"
}
```

### 6.2 获取文档

```javascript
GET /api/v2/repos/{namespace}/docs/{slug}?raw=1
// raw=1 返回 Markdown 格式
```

## 7. 注意事项

1. **永远不要手动写 `<card>` 标签** — URL 编码极易出错
2. **文档声明** — `<!doctype lake>` 由程序自动添加
3. **HTML 转义** — 文本内容中的 `<`、`>`、`&` 需要转义
4. **换行处理** — Lake 使用 HTML 换行规则
5. **表格** — 不使用 `<thead>`，所有行放在 `<tbody>` 中
6. **body_asl** — 实际展示的内容字段，与 `body` 内容相同（Lake 格式时）

## 8. 相关资源

- **编辑器核心**：`@alipay/lakex-doc` npm 包（v1.64.0+），CDN 地址：
  - `https://gw.alipayobjects.com/render/p/yuyan_npm/@alipay_lakex-doc/{version}/umd/doc.umd.js`
  - `https://gw.alipayobjects.com/render/p/yuyan_npm/@alipay_lakex-doc/{version}/umd/doc.css`
- **VSCode 插件**：https://github.com/ilimei/vscode-plugin-lake-editor
- **Yuque SDK**：https://github.com/yuque/sdk
- **Yuque OpenAPI**：https://www.yuque.com/yuque/developer/api
