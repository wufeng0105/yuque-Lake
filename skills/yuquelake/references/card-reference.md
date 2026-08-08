# Lake Card 伪标签参考

> AI 编写 Lake 文档时使用伪标签，由程序自动转换为 `<card>` 标签。

## 伪标签 vs 真实标签

| 伪标签（AI 写） | 真实标签（程序转换后） | 说明 |
|----------------|----------------------|------|
| `<card-codeblock>` | `<card name="codeblock">` | 代码块 |
| `<card-image>` | `<card name="image">` | 图片 |
| `<card-math>` | `<card name="math">` | 数学公式 |
| `<card-yuque>` | `<card name="yuque">` | 语雀内部链接 |
| `<card-file>` | `<card name="file">` | 附件 |
| `<card-hr/>` | `<card name="hr">` | 水平分割线 |
| `<card-label>` | `<card name="label">` | 标签/徽章 |
| `<card-mermaid>` | `<card name="mermaid">` | Mermaid 图表 |
| `<card-plantuml>` | `<card name="plantuml">` | PlantUML 图表 |
| `<card-drawio>` | `<card name="drawio">` | Draw.io 绘图 |
| `<card-minder>` | `<card name="minder">` | 思维导图 |
| `<card-gantt>` | `<card name="gantt">` | 甘特图 |
| `<card-collapse>` | `<card name="collapse">` | 折叠面板 |
| `<card-bookmark>` | `<card name="bookmark">` | 书签/链接卡片 |
| `<card-video>` | `<card name="video">` | 视频 |
| `<card-audio>` | `<card name="audio">` | 音频 |
| `<card-status>` | `<card name="status">` | 状态标签 |
| `<card-note>` | `<card name="note">` | 提示框 |
| `<card-quote>` | `<card name="quote">` | 引用卡片 |
| `<card-catalog/>` | `<card name="catalog">` | 目录（自动生成） |
| `<card-blockquote>` | `<card name="blockquote">` | 增强引用块 |
| `<card-divider/>` | `<card name="divider">` | 分割线（同 hr） |
| `<card-time>` | `<card name="time">` | 时间/日期 |
| `<card-calendar>` | `<card name="calendar">` | 日历 |
| `<card-localdoc>` | `<card name="localdoc">` | 本地文档引用 |
| `<card-api>` | `<card name="api">` | API 文档 |
| `<card-codepen>` | `<card name="codepen">` | CodePen 嵌入 |
| `<card-bilibili>` | `<card name="bilibili">` | B站视频 |
| `<card-youtube>` | `<card name="youtube">` | YouTube 视频 |
| `<card-html>` | `<card name="html">` | 原始 HTML |

## 常用伪标签详细语法

### 代码块

```html
<card-codeblock mode="python" name="示例代码">
def hello():
    print("Hello, World!")
</card-codeblock>
```

**属性**：
- `mode`：语言（python, javascript, sql, bash, go, rust 等）
- `name`：代码块标题（可选）

### 图片

```html
<card-image src="https://example.com/screenshot.png" name="操作界面截图"></card-image>
```

**属性**：
- `src`：图片 URL
- `name`：图片说明（可选）

### 数学公式

```html
<card-math code="E = mc^2"></card-math>
```

**属性**：
- `code`：LaTeX 公式代码

### 语雀内部链接

```html
<card-yuque src="/namespace/repo/doc-slug" title="文档标题"></card-yuque>
```

**属性**：
- `src`：语雀文档路径
- `title`：链接标题

### 附件

```html
<card-file src="https://example.com/report.pdf" name="季度报告.pdf"></card-file>
```

**属性**：
- `src`：附件 URL
- `name`：文件名

### 水平分割线

```html
<card-hr/>
```

无属性。

### 标签/徽章

```html
<card-label label="重要"/>
<card-label label="已完成"/>
```

**属性**：
- `label`：标签文本

### Mermaid 图表

```html
<card-mermaid>
graph TD
    A[开始] --> B{条件判断}
    B -->|是| C[处理]
    B -->|否| D[结束]
    C --> D
</card-mermaid>
```

### PlantUML 图表

```html
<card-plantuml>
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
</card-plantuml>
```

### 折叠面板

```html
<card-collapse title="点击展开详情">
<p>这里是被折叠的内容。</p>
<p>可以包含多个段落。</p>
</card-collapse>
```

**属性**：
- `title`：折叠面板标题

### 书签/链接卡片

```html
<card-bookmark src="https://example.com" title="示例网站"></card-bookmark>
```

### 视频

```html
<card-video src="https://example.com/video.mp4"></card-video>
```

### B站视频

```html
<card-bilibili src="BV1xx411c7mD"></card-bilibili>
```

**属性**：
- `src`：B站视频 BV 号

### YouTube 视频

```html
<card-youtube src="dQw4w9WgXcQ"></card-youtube>
```

**属性**：
- `src`：YouTube 视频 ID

### 提示框

```html
<card-note type="info">
这是一个信息提示框。
</card-note>
```

**type 可选值**：`info`, `warning`, `error`, `success`

### 状态标签

```html
<card-status text="进行中" color="blue"></card-status>
```

**属性**：
- `text`：状态文本
- `color`：颜色（blue, green, red, orange, gray）

### 目录

```html
<card-catalog/>
```

自动生成文档目录，无需属性。
