# Lake Card 伪标签参考

> AI 编写 Lake 文档时使用伪标签，由转换脚本自动生成真实 `<card>` 标签。永远不要手动写 `<card>` 标签的 URL 编码。
>
> 以下所有语法均来自真实语雀文档导出的 `.lake` 文件验证。

## 伪标签一览（13 种 Card + 6 种非 Card 结构）

### Card 伪标签

| 伪标签 | Card name | type | 说明 |
|--------|-----------|------|------|
| `<card-codeblock>` | `codeblock` | inline | 代码块 |
| `<card-image>` | `image` | inline | 图片 |
| `<card-math>` | `math` | inline | 数学公式 |
| `<card-hr/>` | `hr` | block | 水平分割线 |
| `<card-diagram>` | `diagram` | block | Mermaid/PlantUML 图表 |
| `<card-checkbox/>` | `checkbox` | inline | 任务列表复选框 |
| `<card-label>` | `label` | inline | 标签/徽章 |
| `<card-file>` | `file` | inline | 附件 |
| `<card-date>` | `dateCard` | inline | 日期 |
| `<card-calendar/>` | `calendar` | block | 日历 |
| `<card-datatable/>` | `dataTable` | block | 电子表格（数据表） |
| `<card-board/>` | `board` | block | 画板/架构图 |
| `<card-yuque>` | `yuque` | block | 语雀内容嵌入 |

### 非 Card 伪标签（HTML + CSS class）

| 伪标签 | 真实标签 | 说明 |
|--------|---------|------|
| `<alert>` | `<blockquote class="lake-alert">` | 提示框 |
| `<collapse>` | `<details class="lake-collapse">` | 折叠面板 |
| `<columns>` | `<article class="lake-columns">` | 多栏布局容器 |
| `<column>` | `<article class="lake-column-item">` | 多栏布局列 |
| `<inline-label>` | `<span class="ne-label" data-color="N">` | 行内标签 |

---

## 详细语法与使用场景

### 代码块 `<card-codeblock>`

**何时使用**：展示任何需要复制的代码片段，包括命令行、脚本、配置文件。

```html
<card-codeblock mode="python">
def hello():
    print("Hello, World!")
    return 42
</card-codeblock>
```

**属性**：
- `mode`：语言（python, javascript, sql, bash, go, rust, json, yaml, diff, plain 等）

**真实 JSON 结构**（转换脚本自动生成）：
```json
{
  "search": "",
  "hideToolbar": true,
  "mode": "python",
  "code": "def hello():\n    print(\"Hello, World!\")\n    return 42",
  "heightLimit": true,
  "id": "随机5字符"
}
```

**SOP 使用样例**：程序员最爱的功能文档中，代码块用于展示快捷键说明和排序算法示例。

> 行内代码用标准 `<code>` 标签，不用 card。

---

### 图片 `<card-image>`

**何时使用**：展示截图、界面说明、流程图图片、示意图。

```html
<card-image src="https://example.com/screenshot.png"></card-image>
```

**带链接的图片**：
```html
<card-image src="https://example.com/logo.png" link="https://www.yuque.com"></card-image>
```

**属性**：
- `src`：图片 URL（必须）
- `link`：点击图片跳转的 URL（可选）
- `name`：图片说明文字（可选，显示为 title）

**真实 JSON 结构**（最小）：
```json
{
  "src": "https://...",
  "linkTarget": "",
  "title": null,
  "crop": [0, 0, 1, 1],
  "id": "随机5字符"
}
```

带链接时增加 `"link"` 字段。

**SOP 使用样例**：团建活动文档中展示酒店照片；旅行计划中展示行程地图；用研报告中展示操作步骤截图。

---

### 数学公式 `<card-math>`

**何时使用**：展示行内或行间数学公式，使用 LaTeX 语法。

```html
行内：<card-math code="E = mc^2"></card-math>

行间（居中）：
<p style="text-align: center"><card-math code="\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"></card-math></p>
```

**属性**：
- `code`：LaTeX 公式代码

**真实 JSON 结构**：
```json
{
  "code": "E = mc^2",
  "id": "随机5字符"
}
```

> 行间公式需包裹在 `<p style="text-align: center">` 中实现居中。

---

### 水平分割线 `<card-hr/>`

**何时使用**：分隔大章节、切换话题、视觉分隔。

```html
<card-hr/>
```

无属性。自闭合标签。

**真实 JSON 结构**：
```json
{"id": "随机5字符"}
```

> 注意：分割线是 `type="block"`，不是 `type="inline"`。

---

### Mermaid/PlantUML 图表 `<card-diagram>`

**何时使用**：流程图、决策树、时序图、甘特图、UML 图。Mermaid 语法简单优先使用。

```html
<!-- Mermaid 流程图 -->
<card-diagram type="mermaid">
graph TD
    A[开始] --> B{条件判断}
    B -->|是| C[处理请求]
    B -->|否| D[返回错误]
    C --> E[结束]
    D --> E
</card-diagram>

<!-- Mermaid 时序图 -->
<card-diagram type="mermaid">
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: GET /api/data
    Server-->>Client: 200 OK
</card-diagram>

<!-- Mermaid 甘特图 -->
<card-diagram type="mermaid">
gantt
    title 项目排期
    dateFormat YYYY-MM-DD
    section 设计阶段
    需求分析 :a1, 2024-01-01, 7d
    架构设计 :a2, after a1, 10d
    section 开发阶段
    后端开发 :a3, after a2, 14d
    前端开发 :a4, after a2, 10d
</card-diagram>

<!-- PlantUML -->
<card-diagram type="puml">
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
</card-diagram>
```

**属性**：
- `type`：图表类型，`mermaid` 或 `puml`

**真实 JSON 结构**：
```json
{
  "type": "mermaid",
  "code": "graph TD\n    A[开始] --> B{条件判断}\n...",
  "id": "随机5字符"
}
```

> 甘特图不是独立 Card，是 Mermaid 的 `gantt` 语法。

---

### 任务列表复选框 `<card-checkbox/>`

**何时使用**：创建任务清单、检查列表、待办事项。

```html
<!-- 未完成 -->
<card-checkbox checked="false"/>

<!-- 已完成 -->
<card-checkbox checked="true"/>
```

**属性**：
- `checked`：`true` 或 `false`

**真实语法**：
```html
<card type="inline" name="checkbox" value="data:false"></card>
<card type="inline" name="checkbox" value="data:true"></card>
```

> checkbox 不是独立使用的，需要放在任务列表 `<li>` 中。

**完整任务列表示例**：
```html
<ul class="lake-list">
  <li class="lake-list-node lake-list-task">
    <card-checkbox checked="false"/>
    <span>未完成任务</span>
  </li>
  <li class="lake-list-node lake-list-task">
    <card-checkbox checked="true"/>
    <span>已完成任务</span>
  </li>
</ul>
```

**SOP 使用样例**：旅行计划文档的"行前准备"清单——身份证、核酸报告、衣物、防晒用品等任务项。

---

### 标签/徽章 `<card-label>`

**何时使用**：标注状态、优先级、类型分类、注意事项标记。

```html
<card-label text="重要" color="2"/>
<card-label text="P0" color="0"/>
<card-label text="已废弃" color="4"/>
```

**属性**：
- `text`：标签文本
- `color`：颜色索引（数字 0-5+，不是字符串）

**真实 JSON 结构**：
```json
{
  "label": "提前值机更从容",
  "colorIndex": 2,
  "id": "随机5字符"
}
```

**SOP 使用样例**：旅行计划文档中"提前值机更从容"标签提示。

---

### 附件 `<card-file>`

**何时使用**：提供 PDF、Excel、ZIP、TXT 等文件下载。

```html
<card-file src="https://www.yuque.com/attachments/..." name="季度报告.pdf" ext="pdf" size="388"></card-file>
```

**属性**：
- `src`：文件 URL（必须）
- `name`：文件名（必须）
- `ext`：文件扩展名
- `size`：文件大小（字节）

**真实 JSON 结构**：
```json
{
  "src": "https://www.yuque.com/attachments/...",
  "name": "返利.txt",
  "size": 388,
  "ext": "txt",
  "source": "",
  "status": "done",
  "download": true,
  "taskId": "...",
  "taskType": "upload",
  "type": "text/plain",
  "id": "随机5字符"
}
```

---

### 日期 `<card-date>`

**何时使用**：标记日期、时间戳。

```html
<card-date timestamp="1786195371446"/>
```

**属性**：
- `timestamp`：Unix 毫秒时间戳

**真实 JSON 结构**：
```json
{
  "date": 1786195371446,
  "id": "随机5字符"
}
```

---

### 日历 `<card-calendar/>`

**何时使用**：展示日历视图，适合会议安排、排期展示。

```html
<card-calendar date="20260801" color="0"/>
```

**属性**：
- `date`：当前日期，`YYYYMMDD` 格式的整数
- `color`：颜色索引

**真实 JSON 结构**：
```json
{
  "currentDate": 20260801,
  "colorIndex": 0,
  "schedules": {},
  "id": "随机5字符"
}
```

---

### 电子表格 `<card-datatable/>`

**何时使用**：需要动态排序、筛选、多视图切换的数据表格。比 HTML `<table>` 功能更强。

```html
<card-datatable sheetId="xxx" tableId="123"/>
```

> 此 Card 的 JSON 包含 `sheetId`、`docId`、`tableId` 等服务端数据，无法通过伪标签从零创建。通常在编辑器中插入后由系统自动生成。

**SOP 使用样例**：需求文档的"变更记录"表；看板文档的任务管理看板；画册文档的图片集；团建活动文档的人员报名表。

---

### 画板/架构图 `<card-board/>`

**何时使用**：复杂架构图、流程图、里程碑时间线。需要精细控制布局时使用。

```html
<card-board/>
```

> 此 Card 的 JSON 包含完整的 `diagramData`（图形坐标、形状、连线等），结构极为复杂，无法通过伪标签从零创建。在编辑器中通过画板工具创建。

**SOP 使用样例**：需求文档的"产品逻辑"架构图；项目立项的"里程碑"时间线画板。

---

### 语雀内容嵌入 `<card-yuque>`

**何时使用**：嵌入语雀知识库内的其他文档或数据表，带卡片预览。

```html
<!-- 卡片模式（带预览） -->
<card-yuque src="https://www.yuque.com/namespace/repo/slug" mode="card"></card-yuque>

<!-- 嵌入模式（完整展示） -->
<card-yuque src="https://www.yuque.com/namespace/repo/slug" mode="embed"></card-yuque>
```

**属性**：
- `src`：语雀文档 URL
- `mode`：`card`（卡片预览）或 `embed`（嵌入展示）

**真实 JSON 结构**（关键字段）：
```json
{
  "mode": "card",
  "heightMode": "default",
  "src": "https://www.yuque.com/...",
  "url": "https://www.yuque.com/...?view=doc_embed",
  "detail": {
    "image": "...",
    "title": "文档标题",
    "type": "doc",
    "desc": "描述..."
  },
  "id": "随机5字符"
}
```

**SOP 使用样例**：看板文档嵌入数据表视图；画册文档嵌入图片集；系分文档嵌入 PRD 等相关资料。

---

## 非 Card 伪标签

### 提示框 `<alert>`

**何时使用**：突出提示信息、警告、重要说明。不是 Card，是带 CSS class 的 blockquote。

```html
<!-- 信息提示 -->
<alert type="info">
这是信息提示框内容。
</alert>

<!-- 警告提示 -->
<alert type="warning">
注意：此操作不可逆。
</alert>

<!-- 彩色提示 -->
<alert type="color2">
7月28日（周四）— 7月30日（周日）
</alert>
```

**属性**：
- `type`：`info`、`warning`、`color2`（可能还有 color1、color3 等）

**真实 Lake 语法**：
```html
<blockquote class="lake-alert lake-alert-info">
  <p><span>这是信息提示框内容。</span></p>
</blockquote>
```

**SOP 使用样例**：工作周报顶部的"字多 ≠ 有价值"信息提示；旅行计划的航班信息警告框。

---

### 折叠面板 `<collapse>`

**何时使用**：分层信息组织——详细信息折叠不打扰主流程。

```html
<collapse title="点击展开详情" open="false">
  <p>这里是被折叠的内容。</p>
  <p>可以包含多个段落、表格、代码块。</p>
</collapse>
```

**属性**：
- `title`：折叠面板标题
- `open`：`true`（默认展开）或 `false`（默认折叠）

**真实 Lake 语法**：
```html
<details class="lake-collapse" open="false">
  <summary class="lake-summary">点击展开详情</summary>
  <p>折叠的内容</p>
</details>
```

**SOP 使用样例**：工作周报中"具体详见数据接口"的折叠区域。

---

### 多栏布局 `<columns>`

**何时使用**：左右分栏对比展示、图文并排、时间线与详情并排。

```html
<columns>
  <column width="40%">
    <p>左栏内容</p>
  </column>
  <column width="60%">
    <p>右栏内容</p>
  </column>
</columns>
```

**属性**：
- `width`：列宽百分比

**真实 Lake 语法**：
```html
<article class="lake-columns">
  <article class="lake-column-item" style="width: 40.000000%">
    <p>左栏内容</p>
  </article>
  <article class="lake-column-item" style="width: 60.000000%">
    <p>右栏内容</p>
  </article>
</article>
```

**SOP 使用样例**：旅行计划文档中"行程时间"左右分栏——左栏显示日期，右栏显示航班信息。

---

### 行内标签 `<inline-label>`

**何时使用**：在列表项内嵌入标签，标记必要条件、类型分类。

```html
<inline-label text="必要条件" color="4"/>
<inline-label text="非必要条件" color="3"/>
```

**真实 Lake 语法**：
```html
<span data-color="4" class="ne-label">必要条件</span>
```

**SOP 使用样例**：用研报告文档的招募标准列表——"团队人数5-20人"标记为"必要条件"。

---

## 标准标签 vs Card 选择指南

| 需求 | 标准标签 | Card 替代 | 建议 |
|------|----------|----------|------|
| 行内代码 | `<code>var</code>` | — | 用标准标签 |
| 引用 | `<blockquote>` | `<alert>` | 普通引用用标准标签；需要 info/warning 样式时用 alert |
| 分割线 | — | `<card-hr/>` | 用 card |
| 外部链接 | `<a href="...">` | — | 用标准标签 |
| 表格 | `<table><tbody>` | `<card-datatable/>` | 简单表格用标准标签；需要动态排序/筛选用 datatable |
| 列表 | `<ul>`/`<ol>` | — | 用标准标签 |
| 任务清单 | — | `<card-checkbox/>` + `<ul class="lake-list">` | 用 card |
| 上下标 | `<sup>`/`<sub>` | — | 用标准标签 |
| 高亮 | `<span style="background-color: #f3bb2f">` | — | 用标准标签 |
| 文字颜色 | `<span style="color: #E8323C">` | — | 用标准标签 |

## ID 生成规则

所有 Card 的 JSON 中都需要一个 `id` 字段。观察真实样本的规则：
- 5 个字符的随机字符串
- 包含大小写字母和数字（如 `c9HaJ`、`afHYG`、`NLJ29`）
- 转换脚本自动生成，不需要手动指定
