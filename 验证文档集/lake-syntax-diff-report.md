# Lake 语法对比差异报告

> 对比时间：2026-08-08
> 数据来源：语雀服务端返回的 `body_lake` 字段（真实 Lake 原始格式）
> 测试文档：https://www.yuque.com/feng-oftto/gpqwqv/lake-format-full-test

## 一、文档结构层面

### 1.1 文档声明

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 声明 | `<!doctype lake>` | `<!doctype lake>` | ✅ 一致 |
| meta 标签 | 未提及 | `<meta name="doc-version" content="1" /><meta name="viewport" content="fixed" /><meta name="typography" content="classic" /><meta name="paragraphSpacing" content="relax" />` | ❌ **缺失**：文档头部有 4 个 meta 标签 |

### 1.2 文本包裹

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 内容容器 | 无容器，直接标签 | 无容器，直接标签 | ✅ 一致（body_lake 中无 `<div class="lake-content">` 包裹） |
| ID 属性 | 未提及 | 每个标签都有 `data-lake-id` 和 `id` 属性 | ❌ **缺失**：skill 未说明每个元素都需要 `data-lake-id` 和 `id` |

### 1.3 文本内容

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 文本包裹 | 直接写文本 | 所有文本都包裹在 `<span data-lake-id="..." id="...">` 中 | ❌ **重大差异**：skill 中文本直接放在标签内，真实 Lake 中所有文本都被 `<span>` 包裹且带 `data-lake-id`/`id` |

## 二、基础排版标签

### 2.1 标题

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | `<h1>` ~ `<h7>` | `<h1>` ~ `<h6>`（未见 h7） | ⚠️ H7 未见使用 |
| 属性 | 仅标签 | `data-lake-id` + `id` 属性 | ❌ **缺失** |
| 文本包裹 | 直接文本 | `<span data-lake-id="..." id="...">文本</span>` | ❌ **缺失** |

### 2.2 段落与内联格式

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 段落 | `<p>` | `<p data-lake-id="..." id="...">` | ❌ 缺少 id 属性说明 |
| 加粗 | `<strong>` | `<strong><span data-lake-id="...">文本</span></strong>` | ❌ span 包裹 |
| 斜体 | `<em>` | `<em><span data-lake-id="...">文本</span></em>` | ❌ span 包裹 |
| 删除线 | `<del>` | `<del><span data-lake-id="...">文本</span></del>` | ❌ **差异**：skill 写的是 `<del>`，lake-format-spec.md 中也写的 `<del>`，但 body_html 中显示为 `<span style="text-decoration: line-through">`。body_lake 中确认是 `<del>` ✅ |
| 下划线 | `<u>` | `<u><span data-lake-id="...">文本</span></u>` | ❌ span 包裹 |
| 行内代码 | `<code>` | `<code data-lake-id="..." id="..."><span data-lake-id="...">文本</span></code>` | ❌ span 包裹 + id |
| 高亮 | 未提及 | `<span data-lake-id="..." id="..." style="background-color: #f3bb2f">文本</span>` | ❌ **缺失**：skill 完全没有记录高亮语法！实际用 `style="background-color: #f3bb2f"` 实现 |
| 上下标 | `<sup>`/`<sub>` | 直接 Unicode 字符（²、₂） | ❌ **重大差异**：skill 写的 `<sup>2</sup>`，真实 Lake 用 Unicode 上标字符 ² |

### 2.3 引用块

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | `<blockquote>` | `<blockquote data-lake-id="..." id="...">` | ❌ 缺少 id 说明 |
| 内容 | 直接 `<p>` | 内含 `<p data-lake-id="..." id="...">` | ❌ span 包裹 |

## 三、列表

### 3.1 无序列表

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | `<ul><li>项</li></ul>` | 每个项独占一个 `<ul>` | ❌ **重大差异**：skill 写的是所有 `<li>` 在一个 `<ul>` 内，真实 Lake 中每个 `<li>` 被单独包裹在 `<ul>` 中 |
| list 属性 | 未提及 | `<ul list="u3f87b612">` | ❌ **缺失**：每个 `<ul>` 有 `list` 属性关联同组列表 |
| start 属性 | 未提及 | `<ul start="2">` | ❌ **缺失**：同组列表项的序号属性 |
| 嵌套 | `<ul>` 内嵌 `<ul>` | 嵌套用 `<ul data-lake-indent="1">` | ❌ **差异**：嵌套方式不同 |
| li 属性 | 仅 `<li>` | `<li data-lake-id="..." id="...">` | ❌ 缺少 id |
| data-lake-index-type | 未提及 | `data-lake-index-type="0"` | ❌ **缺失** |

### 3.2 有序列表

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | `<ol><li>项</li></ol>` | 每个项独占一个 `<ol>` | ❌ 同无序列表 |
| start 属性 | 未提及 | `<ol start="2">` | ❌ **缺失** |
| 嵌套 | `<ol>` 内嵌 `<ol>` | `<ol data-lake-indent="1">` | ❌ 差异同无序 |

### 3.3 任务列表

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | 未提及 | `<ul class="lake-list">` + `<li class="lake-list-node lake-list-task">` | ❌ **完全缺失**：skill 完全没有记录任务列表语法 |
| checkbox | 未提及 | `<card type="inline" name="checkbox" value="data:true">` / `data:false` | ❌ **完全缺失**：使用 card 标签实现 checkbox |

## 四、表格

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 标签 | `<table><tbody><tr><td>...</td></tr></tbody></table>` | `<table data-lake-id="..." id="..." class="lake-table" style="width: 750px">` | ❌ **缺失**：class、style 属性 |
| colgroup | 未提及 | `<colgroup><col width="150"></colgroup>` | ❌ **缺失**：列宽用 colgroup/col 定义 |
| thead | skill 说不使用 thead | 真实 Lake 中确实无 `<thead>` | ✅ 一致 |
| td 属性 | 无 | `<td data-lake-id="..." id="..." width="150">` | ❌ 缺少 id 和 width |
| td 内容 | 直接文本 | `<p data-lake-id="..."><span data-lake-id="...">文本</span></p>` | ❌ **缺失**：每个 td 内有 `<p>` + `<span>` 包裹 |

## 五、Card 标签——重大差异区

### 5.1 代码块

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| card 类型 | `type="inline"` | `type="inline"` | ✅ 一致 |
| card name | `name="codeblock"` | `name="codeblock"` | ✅ 一致 |
| JSON 字段 | skill 提到 `mode`、`code`、`id` | `{"search":"","hideToolbar":true,"mode":"python","code":"...","heightLimit":true,"id":"..."}` | ❌ **缺失字段**：`search`、`hideToolbar`、`heightLimit` 未在 skill 中说明 |
| 代码转义 | 未说明 | 代码内 `"` 转义为 `%5C%22`，换行转义为 `%5Cn` | ❌ **缺失**：未说明 code 字段内的转义规则 |

### 5.2 图片

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| card 类型 | `type="inline"` | `type="inline"` | ✅ 一致 |
| card name | `name="image"` | `name="image"` | ✅ 一致 |
| JSON 字段 | skill 提到 `src`、`title` | `{"src":"...","linkTarget":"","title":null,"crop":[0,0,1,1],"id":"..."}` | ❌ **缺失字段**：`linkTarget`、`crop` 未在 skill 中完整说明 |
| title | skill 说 name=标题 | `title: null` | ⚠️ 实际为 null |

### 5.3 数学公式

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| card 类型 | 未说明（伪标签暗示 inline） | `type="inline"` | ❌ **缺失** |
| card name | `name="math"` | `name="math"` | ✅ 一致 |
| JSON 字段 | skill 提到 `code` | `{"code":"E = mc^2","id":"..."}` | ❌ **缺失**：未说明 `id` 字段 |
| 行间公式 | 未说明 | 在 `<p style="text-align: center">` 内放置 math card | ❌ **缺失**：未说明行间公式的居中处理 |

### 5.4 水平分割线

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| card 类型 | 未说明 | `type="block"` | ❌ **重大差异**：分割线是 `type="block"` 而非 `type="inline"` |
| card name | `name="hr"` | `name="hr"` | ✅ 一致 |
| JSON 字段 | 无 | `{"id":"..."}` | ❌ **缺失**：需要 id 字段 |

### 5.5 Mermaid 图表

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 伪标签 | `<card-mermaid>` | 真实标签 `name="diagram"` | ❌ **重大差异**：card name 不是 `mermaid` 而是 `diagram` |
| card 类型 | 未说明 | `type="block"` | ❌ **缺失** |
| JSON 字段 | 未说明 | `{"type":"mermaid","code":"...","id":"..."}` | ❌ **缺失**：JSON 结构完全未说明 |
| 甘特图 | skill 说 `<card-gantt>` | 甘特图也是 `name="diagram"` + `type="mermaid"` | ❌ **重大差异**：甘特图不是独立 card，而是 diagram card 的一种 mermaid 语法 |

### 5.6 折叠面板

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 真实表现 | `<card-collapse>` | Markdown 的 `<details>` 标签被转为普通 `<p>` | ❌ **重大差异**：`<details>` 未被识别，折叠功能通过 Markdown API 无法实现 |
| 说明 | — | 需要在语雀编辑器中手动操作或通过 Lake card 创建 | ❌ Markdown 传入的 `<details>` 不生效 |

### 5.7 提示框（> [!INFO] 等）

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 真实表现 | `<card-note type="info">` | `> [!INFO]` 被转为普通 `<blockquote>`，文本中的 `[!INFO]` 被原样保留 | ❌ **重大差异**：Markdown 的 `> [!INFO]` 语法**没有被识别为特殊提示框**，只变成了普通引用 |
| 说明 | — | 语雀的提示框可能需要在编辑器中手动操作，或使用特定的 Lake card 格式 | ❌ Markdown API 无法直接创建提示框 card |

### 5.8 未通过 Markdown 测试的 Card

以下 card 类型无法通过 Markdown API 创建，需要直接写入 Lake 格式：

| Card 类型 | 说明 |
|-----------|------|
| `<card-label>` | 标签/徽章 |
| `<card-yuque>` | 语雀内部链接 |
| `<card-bookmark>` | 书签/链接卡片 |
| `<card-note>` | 提示框 |
| `<card-status>` | 状态标签 |
| `<card-time>` | 时间/日期 |
| `<card-catalog/>` | 目录 |
| `<card-collapse>` | 折叠面板 |
| `<card-plantuml>` | PlantUML 图表 |
| `<card-drawio>` | Draw.io 绘图 |
| `<card-minder>` | 思维导图 |

## 六、链接

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 外部链接 | `<a href="...">文本</a>` | `<a href="..." target="_blank" data-lake-id="..." id="..."><span data-lake-id="...">文本</span></a>` | ❌ **缺失**：`target="_blank"` 默认添加、`data-href` 属性、span 包裹 |

## 七、脚注

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| 语法 | 未提及 | `[^1]` 被转为 `<a href="脚注内容" target="_blank"><span>^1</span></a>` | ❌ **完全缺失**：skill 未记录脚注语法，且脚注处理有问题（链接 href 是脚注内容而非锚点） |

## 八、特殊字符

| 项目 | skill 参考文件 | 真实 Lake | 差异 |
|------|---------------|-----------|------|
| HTML 转义 | 需转义 `<>&` | 在 body_lake 中确认：`<` → `&lt;`、`>` → `&gt;`、`&` → `&amp;` | ✅ 一致 |
| 代码块内转义 | 未说明 | 代码块内容在 JSON 的 code 字段中，`"` → `%5C%22`、换行 → `%5Cn` | ❌ **缺失** |

## 九、总结

### 重大差异（需要立即修复）

1. **所有文本都需要 `<span data-lake-id="..." id="...">` 包裹** — skill 完全没有说明这一点
2. **所有元素都需要 `data-lake-id` 和 `id` 属性** — skill 完全没有说明
3. **文档头部需要 4 个 meta 标签** — skill 完全没有说明
4. **代码块 card JSON 缺少 `search`、`hideToolbar`、`heightLimit` 字段** — skill 不完整
5. **图片 card JSON 缺少 `linkTarget`、`crop` 字段** — skill 不完整
6. **分割线是 `type="block"` 而非 `type="inline"`** — skill 错误
7. **Mermaid 图表的 card name 是 `diagram` 而非 `mermaid`** — skill 错误
8. **甘特图不是独立 card，而是 diagram card 的 mermaid 语法** — skill 错误
9. **任务列表使用 `checkbox` card** — skill 完全缺失
10. **列表结构：每个 `<li>` 独占一个 `<ul>/<ol>`，用 `list` 属性关联** — skill 描述错误
11. **表格需要 `colgroup`/`col` 定义列宽** — skill 缺失
12. **高亮用 `style="background-color: #f3bb2f"`** — skill 完全缺失
13. **上下标用 Unicode 字符而非 `<sup>`/`<sub>`** — skill 描述与实际不一致
14. **Markdown API 无法创建提示框、折叠面板等高级 Card** — skill 未说明这一限制

### 需要验证的 Card（需直接用 Lake 格式测试）

以下 card 需要直接用 `format=lake` 创建文档来验证真实语法：
- label、yuque、bookmark、note、status、time、catalog、collapse、plantuml、drawio、minder
