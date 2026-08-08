---
name: yuquelake
description: Use when the user provides any document and wants to convert it to Yuque Lake format. Use when the user mentions "Lake格式", ".lake文件", "语雀卡片", "lakebook", or wants to transform any document for Yuque knowledge base import. Also use when the user has a Markdown, HTML, or text document and wants it formatted with Yuque's native Lake syntax including cards, alerts, and multi-column layouts.
---

# Yuque Lake 文档转换

## 概述

将任意格式的输入文档转换为语雀 Lake 格式。核心流程：规划 → 清洗 → 梳理 → 伪代码 → 语法。

第零步规划分析需求、选择处理路径；第一步到第四步执行转换。每一步的职责不同，分离它们是为了让 AI 聚焦于内容语义，脚本处理机械语法。

## 何时使用

- 用户提供任意文档，要求转换为 Lake 格式
- 用户提到 "Lake格式"、".lake文件"、"语雀卡片"、"lakebook"
- 用户要把文档导入语雀知识库
- 用户需要语雀原生格式（含卡片、提示框、多栏布局等）

## 何时不使用

- 用户仅要求 Markdown → 语雀（用语雀 API `format=markdown` 即可，不需要 Lake 转换）
- 用户仅询问语雀平台功能（非格式转换）

## 第零步：需求分析与处理规划

**目标**：分析用户需求，确定处理路径，输出处理规划表。

详细规划流程见 [planning-guide.md](references/planning-guide.md)。

### 核心原则

**任何文档的流程第一步永远都是清洗格式，无一例外。** 区别只在于清洗的对象不同（Markdown 标记 / HTML 标签 / 纯文本空白），步骤 1 永远执行。

### 规划内容

- **用户意图**：转换为 Lake / 导入知识库 / 批量迁移
- **输入格式**：Markdown / HTML / 纯文本 / 二进制
- **输入规模**：单文件 / 多文件
- **文档类型**：用户指定 / 自动检测
- **输出方式**：单 .lake / 多 .lake / .lakebook / API 直传

### 质量门

每步完成后检查质量门再进入下一步（详见规划流程指南）：
- 门 0：输入验证（步骤 1 前）
- 门 1：清洗验证（步骤 1 后）
- 门 2：梳理验证（步骤 2 后）
- 门 3：伪代码验证（步骤 3 后）
- 门 4：输出验证（步骤 4 后）

**输出**：处理规划表 + 选择的处理路径

## 第一步：清洗

**目标**：剥离所有格式标记，只保留原始内容 + 位置标记。

**输入**：文本格式的文档（Markdown、HTML、纯文本）。二进制文件（.docx、.pdf）需先提取文本。

### 1a. 删除（格式标记）

只删格式，不删内容：

| 删除类型 | 示例 |
|---------|------|
| Markdown 语法 | `#`、`**`、`*`、`_`、`>`、`` ` ``、`---`、`[]()`、`![]()` |
| HTML 标签 | `<div>`、`<span>`、`<font>`、`<b>`、`<i>`、`<p>`、`<br>` |
| HTML 实体 | `&nbsp;`→空格、`&amp;`→`&` 先解码再删除 |
| 多余空白 | 连续空格收敛为 1 个、连续空行收敛为 2 个 |
| 控制字符 | 零宽空格（U+200B）、不可见控制符 |

### 1b. 保留（内容 + 位置标记）

以下内容**必须保留**：

| 保留类型 | 标记格式 |
|---------|---------|
| 文字内容 | 纯文本，无需标记 |
| 图片 | `[IMAGE: url \| alt说明]` |
| 链接 | `[LINK: url \| 链接文本]` |
| 代码块 | `[CODE: 语言]` 代码 `[END CODE]` |
| 行内代码 | `[INLINE_CODE: 原文]` |
| 表格 | `[TABLE]` 行1\|行2 `[END TABLE]` |
| 列表 | `[LIST: ordered/unordered, level=N]` 项1 项2 `[END LIST]` |
| 引用 | `[QUOTE: 原文]` |
| 数学公式 | `[MATH: LaTeX原文]` |

### 1c. 验证

- [ ] 图片/链接/代码块数量与原文一致
- [ ] 表格行列数完整
- [ ] 内容顺序与原文一致
- [ ] 无残留格式标记
- [ ] 无控制字符

**原则**：信息宁可多留不可丢失。

**输出**：纯文本 + 位置标记，顺序与原文一致

## 第二步：按文档类型重新梳理

**目标**：通读清洗后的内容，判断文档类型，重组内容结构。**此步不碰任何语法，只做内容决策。**

这是最关键的一步，决定后续质量。

### 2a. 判断文档类型

| 文档类型 | 说明 |
|---------|------|
| SOP | 操作流程、标准作业程序 |
| 技术文档 | 架构说明、技术方案 |
| API 文档 | 接口定义、请求/响应示例 |
| 教程 | 教学课程、学习材料 |
| PRD | 产品需求文档 |
| 会议记录 | 会议纪要、决议 |
| 项目计划 | 里程碑、任务排期 |
| 知识沉淀 | 白皮书、经验总结 |
| 产品手册 | 功能说明、用户指南 |
| 设计规范 | 设计规则、规范标准 |

不限于以上类型。如果文档不属于任何已知类型，自行命名并定义结构。

判断类型后，读取对应的骨架参考文件：

| 文档类型 | 参考文件 |
|---------|---------|
| SOP | [references/document-types/sop.md](references/document-types/sop.md) |
| 技术文档 | [references/document-types/technical-doc.md](references/document-types/technical-doc.md) |
| API 文档 | [references/document-types/api-doc.md](references/document-types/api-doc.md) |
| 教程 | [references/document-types/tutorial.md](references/document-types/tutorial.md) |
| PRD | [references/document-types/prd.md](references/document-types/prd.md) |
| 会议记录 | [references/document-types/meeting-notes.md](references/document-types/meeting-notes.md) |
| 项目计划 | [references/document-types/project-plan.md](references/document-types/project-plan.md) |
| 知识沉淀 | [references/document-types/whitepaper.md](references/document-types/whitepaper.md) |
| 产品手册 | [references/document-types/product-manual.md](references/document-types/product-manual.md) |
| 设计规范 | [references/document-types/design-spec.md](references/document-types/design-spec.md) |

### 2b. 方法论约束

用 [methodology.md](references/methodology.md) 中的方法论约束结构设计：

- **Information Mapping**：每个内容块归为 6 种信息类型之一（Procedure/Process/Principle/Concept/Structure/Fact）
- **Minimalism**：以行动为导向，只保留完成任务所需信息
- **DITA**：按 Concept/Task/Reference 组织，不混杂内容类型

### 2c. 内容取舍

- 代码块 → 保留/简化/转为步骤说明
- 表格 → 保留结构/转成列表/拆解为图文
- 图片 → 保留/移除/补充说明
- 链接 → 保留/转为引用/移除

**输出**：按文档类型重新组织的结构化内容大纲（纯文本，无任何标签）

## 第三步：加伪代码

**目标**：在第二步梳理好的结构化内容上，添加伪标签。**此步只做语法选择，不重做内容决策。**

### 3a. 选择伪标签

根据内容块的语义，选择合适的伪标签。参考 [card-reference.md](references/card-reference.md) 确认每个标签的用法。

**Card 伪标签**（13 种）：

| 伪标签 | 说明 |
|--------|------|
| `<card-codeblock mode="python">代码</card-codeblock>` | 代码块 |
| `<card-image src="url"></card-image>` | 图片 |
| `<card-math code="E=mc^2"></card-math>` | 数学公式 |
| `<card-hr/>` | 水平分割线 |
| `<card-diagram type="mermaid">graph TD; A-->B</card-diagram>` | Mermaid/PlantUML 图表 |
| `<card-checkbox checked="false"/>` | 任务列表复选框 |
| `<card-label text="重要" color="2"/>` | 标签 |
| `<card-file src="url" name="file.pdf"/>` | 附件 |
| `<card-date timestamp="1786195371446"/>` | 日期 |
| `<card-calendar date="20260801"/>` | 日历 |
| `<card-datatable/>` | 电子表格（占位符） |
| `<card-board/>` | 画板（占位符） |
| `<card-yuque src="url" mode="card"></card-yuque>` | 语雀内容嵌入 |

**非 Card 伪标签**（4 种）：

| 伪标签 | 说明 |
|--------|------|
| `<alert type="info">内容</alert>` | 提示框（info/warning/color2） |
| `<collapse title="标题" open="false">内容</collapse>` | 折叠面板 |
| `<columns><column width="40%">内容</column></columns>` | 多栏布局 |
| `<inline-label text="必要" color="4"/>` | 行内标签 |

**规则**：
- 永远写伪标签，不要手写真实 `<card>` 标签的 URL 编码
- 文本中的 `<`、`>`、`&` 转义为 `&lt;`、`&gt;`、`&amp;`
- 表格用 `<table><tbody>`，不用 `<thead>`；需要 `<colgroup>` 定义列宽
- 伪标签与真实 Lake 语法的映射关系见 [tag-mapping.json](references/tag-mapping.json)

**输出**：带伪标签的 HTML 文件

## 第四步：加语法和相关内容

**目标**：转换脚本读取伪标签 HTML，生成真实 `.lake` 文件。**此步完全机械化，由脚本执行。**

### 4a. 转换

```bash
python scripts/lake-converter.py input.html output.lake --title "文档标题"
```

脚本自动完成：
- 伪标签 → 真实 `<card>` 标签（含 JSON 构造 + URL 编码）
- 非 Card 伪标签 → 真实 HTML + CSS class
- 补充 `<!doctype lake>` + `<title>` + 4 个 `<meta>` 标签
- 清理多余空行

### 4b. 验证

转换后检查：
- `<!doctype lake>` 在文件开头
- 无残留伪标签（搜索 `card-` 前缀，应为 0 个）
- 所有 `<card>` 标签都有 `name` 和 `value` 属性
- `value` 以 `data:` 开头

## 参考文件

- [references/card-reference.md](references/card-reference.md) — 13 种 Card 伪标签 + 4 种非 Card 结构语法与场景
- [references/tag-mapping.json](references/tag-mapping.json) — 伪标签到真实 Lake 语法的映射表（脚本读取）
- [references/lake-format-spec.md](references/lake-format-spec.md) — 标准 HTML 标签使用场景
- [references/lakebook-structure.md](references/lakebook-structure.md) — .lakebook 打包结构
- [references/planning-guide.md](references/planning-guide.md) — 规划流程：需求分析、决策树、质量门、批量处理
- [references/methodology.md](references/methodology.md) — 文档结构化方法论参考
- [scripts/lake-converter.py](scripts/lake-converter.py) — 伪标签转换脚本
- [scripts/md-to-lake.py](scripts/md-to-lake.py) — Markdown 转伪标签 HTML 脚本
