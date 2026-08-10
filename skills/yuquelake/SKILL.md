---
name: yuquelake
description: Use when the user provides any document and wants to convert it to Yuque Lake format. Use when the user mentions "Lake格式", ".lake文件", "语雀卡片", "lakebook", or wants to transform any document for Yuque knowledge base import. Also use when the user has a Markdown, HTML, or text document and wants it formatted with Yuque's native Lake syntax including cards, alerts, and multi-column layouts. Make sure to use this skill whenever the user mentions Yuque (语雀), wants to import documents into a Yuque knowledge base, or needs Yuque-native document formatting — even if they don't explicitly ask for "Lake format" or say things like "转成语雀格式", "导入语雀", "语雀文档", "语雀知识库", or "语雀编辑器".
---

# Yuque Lake 文档转换

## 概述

将任意格式的输入文档转换为语雀 Lake 格式。核心流程：规划 → 清洗 → 梳理 → 伪代码 → 语法。

AI 负责内容语义（步骤 0-3），脚本负责机械语法（步骤 4）。各步之间通过明确接口协作，不越界。

## 何时使用

- 用户提供任意文档，要求转换为 Lake 格式
- 用户提到 "Lake格式"、".lake文件"、"语雀卡片"、"lakebook"
- 用户要把文档导入语雀知识库

## 何时不使用

- 用户仅要求 Markdown → 语雀（用语雀 API `format=markdown` 即可）
- 用户仅询问语雀平台功能（非格式转换）

## 第零步：需求分析与处理规划

**目标**：分析用户需求，确定处理路径，输出处理规划表。

详细规划流程见 [planning-guide.md](knowledge/planning-guide.md)。

**核心原则**：任何文档的流程第一步永远都是清洗格式，无一例外。不关注输入格式——Markdown、HTML、Lake、TXT、docx 等一律清洗干净。

**规划内容**：用户意图、输入格式、输入规模、文档类型、输出方式。

**执行纪律**：每一步的输出必须在对话中显式呈现后才能进入下一步。不允许在脑中完成中间步骤直接跳到下一步。

**质量门**（每步完成后检查再进入下一步，过门必须展示对应产物）：
- 门 0：输入验证 → 展示规划表
- 门 1：清洗验证 → 展示清洗后的纯文本
- 门 2：梳理验证 → 展示结构化大纲（含信息类型标注和信息提取结果）
- 门 3：伪代码验证 → 展示伪标签 HTML（必须先完整阅读 card-guide.md）
- 门 4：输出验证 → 展示验证结果

## 第一步：清洗

**目标**：剥离所有格式标记，只保留原始内容 + 位置标记。

**输入**：文本格式的文档（Markdown、HTML、纯文本）。二进制文件需先提取文本。

### 1a. 删除（格式标记）

只删格式，不删内容：Markdown 语法（`#`、`**`、`[]()` 等）、HTML 标签（`<div>`、`<span>` 等）、HTML 实体（先解码再删除）、多余空白（连续空格收敛为 1 个、连续空行收敛为 2 个）、控制字符（零宽空格等）。

### 1b. 保留（内容 + 位置标记）

| 保留类型 | 标记格式 |
|---------|---------|
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

**原则**：信息宁可多留不可丢失。辅助工具：`python scripts/md-to-lake.py input.md output.html`

**输出**：清洗后的纯文本（含位置标记），必须在对话中显式呈现，通过门 1 后再进入第二步。

## 第二步：按文档类型重新梳理

**目标**：通读清洗后的内容，判断文档类型，重组内容结构。**此步不碰任何语法，只做内容决策。**

### 2a. 判断文档类型

判断类型后，读取对应的写作指南，按指南中的结构规则和内容取舍规则重组内容：

| 文档类型 | 参考文件 |
|---------|---------|
| SOP | [knowledge/document-types/sop.md](knowledge/document-types/sop.md) |
| 技术文档 | [knowledge/document-types/technical-doc.md](knowledge/document-types/technical-doc.md) |
| API 文档 | [knowledge/document-types/api-doc.md](knowledge/document-types/api-doc.md) |
| 教程 | [knowledge/document-types/tutorial.md](knowledge/document-types/tutorial.md) |
| PRD | [knowledge/document-types/prd.md](knowledge/document-types/prd.md) |
| 会议记录 | [knowledge/document-types/meeting-notes.md](knowledge/document-types/meeting-notes.md) |
| 项目计划 | [knowledge/document-types/project-plan.md](knowledge/document-types/project-plan.md) |
| 白皮书 | [knowledge/document-types/whitepaper.md](knowledge/document-types/whitepaper.md) |
| 产品手册 | [knowledge/document-types/product-manual.md](knowledge/document-types/product-manual.md) |
| 设计规范 | [knowledge/document-types/design-spec.md](knowledge/document-types/design-spec.md) |

不限于以上类型。如果文档不属于任何已知类型，自行命名并定义结构。

### 2b. 方法论约束

用 [methodology.md](knowledge/methodology.md) 中的方法论约束结构设计：

- **Information Mapping**：每个内容块归为 6 种信息类型之一（Procedure/Process/Principle/Concept/Structure/Fact）
- **Minimalism**：以行动为导向，只保留完成任务所需信息
- **DITA**：按 Concept/Task/Reference 组织，不混杂内容类型

**Gate 2 验证清单**（全部通过才能进入第三步）：
- [ ] 每个内容块已归类到 Information Mapping 6 种类型之一（Procedure/Process/Principle/Concept/Structure/Fact）
- [ ] 内容块不混杂类型（DITA 强类型分离——一个内容块不同时是步骤又是概念）
- [ ] 散乱参数/条件/话术/指标已识别并提取为结构化形式（遵循 card-guide.md 第三部分信息提取规则）
- [ ] 结构化大纲遵循文档类型的章节骨架
- [ ] 大纲中无任何伪标签或格式标记

**输出**：按文档类型重新组织的结构化内容大纲（纯文本，无任何标签，每个内容块标注信息类型），必须在对话中显式呈现，通过门 2 后再进入第三步。

## 第三步：加伪代码

**目标**：在第二步梳理好的结构上，选择伪标签。**此步只做语法选择，不重做内容决策。**

### 伪标签格式

极简格式：`<card-type attr="val">内容</card-type>`

**Card 伪标签**（13 种）：`card-codeblock`、`card-image`、`card-math`、`card-hr`、`card-diagram`、`card-checkbox`、`card-label`、`card-file`、`card-date`、`card-calendar`、`card-datatable`、`card-board`、`card-yuque`

**非 Card 伪标签**（4 种）：`alert`、`collapse`、`columns`、`inline-label`

### 选择指南

**强制前置**：进入此步前，必须完整阅读 [card-guide.md](knowledge/card-guide.md)。它包含三个部分：
1. Card 能力目录——每种 Card 适合什么内容
2. 选择决策指南——按信息类型分组的决策树（先判断信息类型，再选呈现形式）
3. 信息提取规则——散乱信息识别与结构化提取规则

未阅读 card-guide.md 不得选择任何伪标签。各文档类型写作指南的「语法选择」章节会引导你回到此处。

### 规则

- 永远写伪标签，不要手写真实 `<card>` 标签的 URL 编码
- 文本中的 `<`、`>`、`&` 转义为 `&lt;`、`&gt;`、`&amp;`
- 表格用 `<table><tbody>`，不用 `<thead>`；需要 `<colgroup>` 定义列宽
- 辅助工具：`python scripts/md-to-lake.py input.md output.html`

**输出**：带伪标签的 HTML 文件，必须在对话中显式呈现，通过门 3 后再进入第四步。

## 第四步：加语法和相关内容

**目标**：转换脚本读取伪标签 HTML，生成真实 `.lake` 文件。**此步完全机械化，由脚本执行。**

```bash
python scripts/lake-converter.py input.html output.lake --title "文档标题"
```

脚本自动完成：伪标签 → 真实 `<card>` 标签（含 JSON 构造 + URL 编码）、非 Card 伪标签 → 真实 HTML + CSS class、补充文档头、清理多余空行。

### 验证

- `<!doctype lake>` 在文件开头
- 无残留伪标签（搜索 `card-` 前缀，应为 0 个）
- 所有 `<card>` 标签都有 `name` 和 `value` 属性，`value` 以 `data:` 开头

## 参考文件

**知识层（AI 读取，做内容决策）**：
- [knowledge/planning-guide.md](knowledge/planning-guide.md) — 规划流程：需求分析、决策树、质量门
- [knowledge/methodology.md](knowledge/methodology.md) — 文档结构化方法论（6 种信息类型、DITA、Minimalism）
- [knowledge/card-guide.md](knowledge/card-guide.md) — Card 能力目录 + 选择决策指南
- [knowledge/document-types/](knowledge/document-types/) — 10 种文档类型写作指南

**语法层（AI 读取，查阅格式规范）**：
- [reference/lake-format.md](reference/lake-format.md) — Lake 格式规范（HTML 标签用法、转义规则）
- [reference/lakebook.md](reference/lakebook.md) — .lakebook 打包结构

**执行层（AI 不读，脚本自动加载）**：
- [scripts/lake-converter.py](scripts/lake-converter.py) — 伪标签转换脚本（内部加载 tag-mapping.json）
- [scripts/md-to-lake.py](scripts/md-to-lake.py) — Markdown 转伪标签 HTML 脚本
