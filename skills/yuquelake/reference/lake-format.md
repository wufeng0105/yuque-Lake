# Lake 格式规范

> 基于真实语雀文档导出的 `.lake` 文件分析整理。所有语法均有真实样本验证。

## 1. 概述

Lake 是语雀（Yuque）的私有文档格式，本质是 **HTML 的超集**：
- 文档声明 `<!doctype lake>`
- 标准 HTML 标签（`<h1>`-`<h6>`, `<p>`, `<table>`, `<ul>`, `<ol>` 等）
- 自定义 `<card>` 标签（代码块、图片、公式等高级功能）
- 非 Card 的特殊 HTML + CSS class 结构（提示框、折叠面板、多栏布局等）

## 2. 文档结构

### 完整文档头部

```html
<!doctype lake>
<title>文档标题</title>
<meta name="doc-version" content="1" />
<meta name="viewport" content="fixed" />
<meta name="typography" content="classic" />
<meta name="paragraphSpacing" content="relax" />
```

**头部要素**：
- `<!doctype lake>` — 文档声明（必须）
- `<title>` — 文档标题
- 4 个 `<meta>` 标签 — 版本、视口、排版、段落间距

> 转换脚本自动添加头部。AI 编写伪标签时不需要写这些。

### 文档主体

头部之后直接是内容标签，无 `<html>`、`<head>`、`<body>` 包裹。

## 3. 元素 ID 与文本包裹

### data-lake-id 和 id 属性

真实 Lake 中，**每个元素**都有 `data-lake-id` 和 `id` 属性：

```html
<p data-lake-id="uf987e51e" id="uf987e51e">...</p>
<h2 data-lake-id="hWCY3" id="hWCY3">...</h2>
<td data-lake-id="u7644ecd7" id="u7644ecd7">...</td>
```

### 文本 span 包裹

真实 Lake 中，**所有文本**都包裹在 `<span data-lake-id="..." id="...">` 中：

```html
<p data-lake-id="xxx" id="xxx">
  <span data-lake-id="yyy" id="yyy">文本内容</span>
</p>
```

> 转换脚本自动生成 ID 和 span 包裹。AI 编写伪标签时直接写文本即可。

## 4. 标准 HTML 标签

### 标题层级（H1-H6）

Lake 支持 H1 ~ H6：

```html
<h1>一级标题</h1>  <!-- 文档主标题，每篇仅一个 -->
<h2>二级标题</h2>  <!-- 一级章节 -->
<h3>三级标题</h3>  <!-- 二级章节 -->
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>
```

| 标签 | 场景 |
|------|------|
| `<h1>` | 文档主标题，每篇仅一个 |
| `<h2>` | 一级章节标题 |
| `<h3>` | 二级章节标题 |
| `<h4>` | 三级章节标题 |
| `<h5>`-`<h6>` | 深层嵌套的细节标题，少用 |

### 段落与内联格式

```html
<p>普通段落文本</p>
<p><strong>加粗文本</strong></p>
<p><em>斜体文本</em></p>
<p><del>删除线</del></p>
<p><u>下划线</u></p>
<p>行内代码：<code>variable_name</code></p>
<p>上标：x<sup>2</sup></p>
<p>下标：H<sub>2</sub>O</p>
```

| 标签 | 场景 |
|------|------|
| `<p>` | 段落正文，最基础的文本容器 |
| `<strong>` | 强调关键词、重要提醒 |
| `<em>` | 补充说明、次要强调 |
| `<del>` | 标记已废弃或移除的内容 |
| `<u>` | 强调标注（少用，易与超链接混淆） |
| `<sup>` | 数学上标、脚注引用 |
| `<sub>` | 化学下标、变量下标 |
| `<code>` | 行内代码、命令名、文件名、变量名 |

### 文字样式

**高亮**（背景色）：
```html
<span style="background-color: #f3bb2f">高亮文本</span>
```

**文字颜色**：
```html
<span style="color: #E8323C">红色文本</span>
```

**文字颜色 + 背景色**：
```html
<span style="color: #8C8C8C; background-color: #F5F5F5">灰色文本带灰底</span>
```

### 换行

```html
<p>第一行<br />第二行</p>
```

`<br />` 或 `<br>` 均可，用于段内强制换行。

### 引用块

```html
<blockquote>
  <p>引用块内容</p>
</blockquote>
```

**何时使用**：
- 引用外部资料原文
- 强调重要观点
- 文档模板中的说明提示

> 需要带颜色的提示框样式时用 `<alert>`（见 card-guide.md）。

### 链接

```html
<a href="https://example.com" target="_blank">外部链接文本</a>
```

链接默认添加 `target="_blank"`。

### 列表

#### 无序列表

真实 Lake 中每个 `<li>` 独占一个 `<ul>`，通过 `list` 属性关联同组：

```html
<ul list="xxx"><li>项 1</li></ul>
<ul list="yyy" start="2"><li>项 2</li></ul>
<ul list="zzz" start="3"><li>项 3</li></ul>
```

> AI 写伪标签时可简化为标准嵌套写法，转换脚本处理拆分。

#### 有序列表

```html
<ol list="xxx"><li>项 1</li></ol>
<ol list="yyy" start="2"><li>项 2</li></ol>
```

#### 嵌套列表

嵌套用 `data-lake-indent` 属性：

```html
<ul list="xxx"><li>第一级</li></ul>
<ul list="yyy" data-lake-indent="1"><li>第二级</li></ul>
<ul list="zzz" data-lake-indent="2"><li>第三级</li></ul>
```

#### 混合列表

有序和无序可以混合嵌套：

```html
<ol list="xxx"><li>有序项</li></ol>
<ul list="yyy" data-lake-indent="1"><li>无序子项</li></ul>
<ol list="zzz" data-lake-indent="2"><li>有序子子项</li></ol>
```

### 表格

```html
<table class="lake-table" style="width: 750px">
  <colgroup>
    <col width="150">
    <col width="150">
    <col width="150">
  </colgroup>
  <tbody>
    <tr>
      <td><p>参数名</p></td>
      <td><p>类型</p></td>
      <td><p>说明</p></td>
    </tr>
    <tr>
      <td><p>host</p></td>
      <td><p>string</p></td>
      <td><p>服务器地址</p></td>
    </tr>
  </tbody>
</table>
```

**表格要素**：
- `class="lake-table"` — 表格 class（必须）
- `style="width: Npx"` — 表格宽度
- `<colgroup><col width="N">` — 列宽定义
- `<tbody>` 包裹所有行（包括表头行），**不使用 `<thead>`**
- 每个 `<td>` 内的内容包裹在 `<p>` 中

#### 表格对齐

在 `<p>` 上使用 `style="text-align"`：

```html
<td><p style="text-align: left">左对齐</p></td>
<td><p style="text-align: center">居中</p></td>
<td><p style="text-align: right">右对齐</p></td>
```

#### 单元格背景色

```html
<td style="background-color: #F5F5F5">...</td>
```

#### 单元格合并

```html
<td colSpan="3">合并三列</td>
<td rowSpan="2">合并两行</td>
```

#### 单元格垂直对齐

```html
<td style="vertical-align: middle">垂直居中</td>
<td style="vertical-align: top">顶部对齐</td>
```

常见场景：某些行有多行内容时，使用 `vertical-align: middle` 让标签列垂直居中。

#### 表格宽度模式

```html
<table width-mode="contain" margin="true">
```

- `width-mode="contain"` — 宽度自适应容器
- `margin="true"` — 表格边距

## 5. Card 标签系统

### 数据表（dataTable）与普通表格的区别

语雀中有两种表格：

| 类型 | HTML 结构 | 特点 |
|------|----------|------|
| 普通表格 | `<table class="lake-table">` | 静态内容，AI 可从零创建 |
| 数据表 | `<table class="ne-dataTable">` 或 `<card name="dataTable">` | 含服务端数据（sheetId/docId/tableId），无法从零创建 |

数据表在 HTML 中使用 `<thead>` + `<tbody>` 结构（与普通表格不同），第一行为表头。`lake-extract.py` 会自动识别并提取数据表内容。

### 基本结构

```html
<card type="inline" name="cardType" value="data:URL编码的JSON"></card>
```

### type 属性

- `type="inline"` — 行内 Card（codeblock, image, math, checkbox, label, file, dateCard）
- `type="block"` — 块级 Card（hr, diagram, calendar, dataTable, board, yuque）

### value 属性编码规则

1. 构造 JSON 对象
2. URL 编码整个 JSON 字符串（使用 `encodeURIComponent`）
3. 添加 `data:` 前缀

> 永远不要手动编码。使用伪标签 + 转换脚本。详见 card-guide.md。

## 6. 特殊字符处理

### HTML 转义

文本内容中的特殊字符需转义：

| 原字符 | 转义为 |
|--------|--------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |

### 代码块内转义

代码块内容在 JSON 的 `code` 字段中，URL 编码处理：
- `"` → `%5C%22`（先转义引号再 URL 编码）
- 换行 → `%5Cn`
- `\` → `%5C%5C`

> 转换脚本自动处理转义。

## 7. 不支持的 Markdown 语法

以下 Markdown 语法在语雀 Markdown 导入时**不被支持**，会降级为纯文本或丢失：

| 语法 | 处理结果 |
|------|---------|
| GitHub emoji `:smile:` | 原样保留为文本，不转换 |
| 定义列表 `Term\n: Definition` | 变成普通段落 + `<br />` |
| `<kbd>` 键盘标签 | 标签被剥离，变纯文本 |
| `<mark>` 高亮标签 | 标签被剥离，无样式 |
| `<details>` 折叠（Markdown 写法） | 变成普通段落，无折叠功能 |
| `*[HTML]: 缩写` | 原样保留为文本 |
| `<!-- HTML 注释 -->` | 完全移除 |
| `<user@example.com>` 自动链接 | 不转换，原样保留为文本 |
| 嵌套引用 `>>` | 不嵌套，变成平铺的独立引用块 |

> 要使用折叠面板、提示框等功能，必须通过 Lake 伪标签或语雀编辑器创建。

## 8. 注意事项

1. 永远不要手动写 `<card>` 标签 — URL 编码极易出错
2. 文档声明和 meta 标签由转换脚本自动添加
3. `data-lake-id`、`id` 属性和 `<span>` 文本包裹由转换脚本自动生成（待实现，语雀编辑器导入时自动补全）
4. 表格不使用 `<thead>`，所有行放在 `<tbody>` 中
5. 表格需要 `<colgroup>` 定义列宽
6. 列表项通过 `list` 属性关联同组，不是嵌套在同一个 `<ul>`/`<ol>` 内
7. 文字颜色和高亮用 `style` 属性，不是 Markdown 语法
