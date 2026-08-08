# yuque-Lake

语雀 Lake 格式学习与转换工具集。

## 关于 Lake 格式

Lake 是语雀（Yuque）的私有文档格式，本质是 HTML 的超集：

- **标准 HTML 标签**：`<h1>` ~ `<h7>`、`<p>`、`<table>`、`<ul>`、`<ol>`、`<blockquote>` 等
- **自定义 `<card>` 标签**：用于代码块、图片、数学公式、附件等高级功能
- **文档声明**：`<!doctype lake>`
- **标题层级**：支持 H1-H7（比 HTML 标准多一个 H7）
- **表格规则**：仅使用 `<tbody>`，不使用 `<thead>`

### Card 标签结构

```html
<card name="类型名" value="data:URL编码的JSON"></card>
```

`value` 属性格式：`data:` 前缀 + URL 编码的 JSON 字符串。

### 支持的 Card 类型

| name 值 | 说明 |
|---------|------|
| `codeblock` | 代码块 |
| `image` | 图片 |
| `math` | 数学公式 |
| `file` | 附件 |
| `hr` | 水平分割线 |
| `label` | 标签 |
| `yuque` | 语雀内部链接 |

### 示例

```html
<!doctype lake>
<h1>文档标题</h1>
<p>这是一段正文。</p>
<card name="codeblock" value="data:%7B%22code%22%3A%22def%20hello()%3A%5Cn%20%20%20%20print(%5C%22Hello%5C%22)%22%2C%22mode%22%3A%22python%22%7D"></card>
```

## 目录结构

```
yuque-Lake/
├── README.md          # 项目说明
├── .lake/             # Lake 格式示例文件
├── .lakebook/         # Lakebook 知识库打包文件
└── converter/         # 转换工具脚本
```

## 相关资源

- [语雀官方文档](https://www.yuque.com/yuque)
- Lake 格式规范详见项目内 `references/lake-format.md`
