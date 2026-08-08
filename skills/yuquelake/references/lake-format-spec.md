# Lake 格式规范（完整版）

> 基于 `@alipay/lakex-doc` v1.64.0 + VSCode Lake 编辑器插件 + Yuque SDK 分析整理

## 1. 概述

Lake 是语雀（Yuque）的私有文档格式，本质是 **HTML 的超集**：
- 标准 HTML 标签（`<h1>`-`<h7>`, `<p>`, `<table>`, `<ul>`, `<ol>` 等）
- 自定义 `<card>` 标签（代码块、图片、公式等高级功能）
- 文档声明 `<!doctype lake>`

## 2. 文档结构

### 完整 .lake 文件

```html
<!doctype lake>
<h1>文档标题</h1>
<p>正文段落。</p>
<card name="codeblock" value="data:%7B%22code%22%3A%22...%22%7D"></card>
```

### 最小化结构

```html
<!doctype lake>
<h1>标题</h1>
<p>内容</p>
```

## 3. 标签体系

### 标题层级（H1-H7）

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

### 文本格式

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

### 段落与引用

```html
<p>普通段落</p>
<blockquote>引用块内容</blockquote>
```

### 链接

```html
<a href="https://example.com">外部链接</a>
<card name="yuque" value="data:...">语雀内部链接</card>
```

### 列表

```html
<ul><li>第一项</li><li>第二项</li></ul>
<ol><li>第一步</li><li>第二步</li></ol>
<ul><li>父项<ul><li>子项</li></ul></li></ul>
```

### 表格

```html
<table>
  <tbody>
    <tr><td>表头1</td><td>表头2</td></tr>
    <tr><td>数据1</td><td>数据2</td></tr>
  </tbody>
</table>
```

> Lake 表格使用 `<tbody>` 包裹所有行（包括表头），不使用 `<thead>`。

## 4. Card 标签系统

### 基本结构

```html
<card name="类型名" value="data:URL编码的JSON"></card>
```

### value 属性编码规则

1. 构造 JSON 对象
2. URL 编码整个 JSON 字符串（使用 `encodeURIComponent`）
3. 添加 `data:` 前缀

> 不要手动编码！使用伪标签 + 程序转换。

## 5. 注意事项

1. 永远不要手动写 `<card>` 标签 — URL 编码极易出错
2. 文档声明 `<!doctype lake>` 由程序自动添加
3. 文本内容中的 `<`、`>`、`&` 需要转义
4. Lake 使用 HTML 换行规则，`<br>` 可用于强制换行
5. 表格不使用 `<thead>`，所有行放在 `<tbody>` 中
6. body_asl 是实际展示的内容字段

## 6. 编辑器核心

- npm 包：`@alipay/lakex-doc`（v1.64.0+）
- CDN JS：`https://gw.alipayobjects.com/render/p/yuyan_npm/@alipay_lakex-doc/{version}/umd/doc.umd.js`
- CDN CSS：`https://gw.alipayobjects.com/render/p/yuyan_npm/@alipay_lakex-doc/{version}/umd/doc.css`
