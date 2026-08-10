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

**不可变元素清单**：在规划阶段必须先阅读 [knowledge/invariants.md](knowledge/invariants.md)——它定义了所有文档类型通用的内容保全基线。规划表中的内容清点结果将作为后续每个质量门的校验基准。

**规划内容**：用户意图、输入格式、输入规模、文档类型、内容清点（图片×N 链接×N 代码块×N 表格×N 附件×N 数学公式×N 流程图×N 话术×N）、输出方式。

**执行纪律**：每一步的输出必须在对话中显式呈现后才能进入下一步。不允许在脑中完成中间步骤直接跳到下一步。

**质量门**（每步完成后检查再进入下一步，过门必须展示对应产物）：
- 门 0：输入验证 → 展示规划表（含内容清点）
- 门 1：清洗验证 → 展示清洗后的纯文本（不可变元素标记数 ≥ 规划表清点数）
- 门 2：梳理验证 → 展示结构化大纲（每个不可变元素都有对应位置）
- 门 3：伪代码验证 → 展示伪标签 HTML（必须先完整阅读 card-guide.md）
- 门 4：输出验证 → 运行 `verify-content.py` 确认输出中不可变元素数量 ≥ 规划表清点数

### 红线规则

以下 6 条不可违反，违反即输出不合格：

1. **不可删除不可变元素**——图片、链接、代码块、表格、附件、公式、流程图、话术、金额。详见 [invariants.md](knowledge/invariants.md)
2. **Lake 输入不可直接剥离 `<card>` 标签**——`<card>` 是内容载体不是格式标记，必须先解析提取内容。详见 §1a-Lake
3. **不可删除内容，只能归类**——非核心内容移到附录/折叠面板，不可消失。详见各 document-types/*.md 的"归类"列
4. **不可跳过质量门**——每步必须展示产物并通过验证才能进入下一步
5. **不可跳过 Step 0 内容清点**——清点结果是所有后续质量门的校验基准
6. **不可混杂文档类型**——SOP 不含 API 端点，PRD 不含操作步骤。详见 [methodology.md](knowledge/methodology.md) DITA 约束

## 第一步：清洗

**目标**：剥离所有格式标记，只保留原始内容 + 位置标记。

**输入**：文本格式的文档（Markdown、HTML、Lake、纯文本）。二进制文件需先提取文本。

### 1a. 删除（格式标记）

只删格式，不删内容：Markdown 语法（`#`、`**`、`[]()` 等）、HTML 标签（`<div>`、`<span>` 等）、HTML 实体（先解码再删除）、多余空白（连续空格收敛为 1 个、连续空行收敛为 2 个）、控制字符（零宽空格等）。

### 1a-Lake. Lake 格式输入的特殊清洗规则

当输入是 `.lake` 文件时，`<card>` 标签既是格式标记也是内容载体——直接当作 HTML 标签剥离会导致图片、代码、公式等内容全部丢失。Lake 格式的清洗需要先解析 `<card>` 标签，提取其中的内容，再按标准清洗流程处理。

Lake `<card>` 标签结构：`<card type="inline" name="cardName" value="data:URL编码的JSON">`。内容信息封装在 `value` 属性的 URL 编码 JSON 中。清洗时按以下步骤处理：

1. **识别所有 `<card>` 标签**，按 `name` 属性分类
2. **解码 `value` 属性**：去掉 `data:` 前缀 → `decodeURIComponent` → `JSON.parse`
3. **按 card 类型提取内容并转为位置标记**：

| Card 类型 | 提取字段 | 转为标记 |
|-----------|---------|----------|
| `image` | `src`, `title` | `[IMAGE: src \| title]` |
| `codeblock` | `mode`, `code` | `[CODE: mode]` code `[END CODE]` |
| `math` | `code` | `[MATH: code]` |
| `diagram` | `type`, `code` | `[DIAGRAM: type]` code `[END DIAGRAM]` |
| `file` | `src`, `name`, `ext` | `[FILE: src \| name \| ext]` |
| `hr` | — | `[HR]` |
| `checkbox` | `checked` | `[CHECKBOX: checked]` |
| `label` | `label`, `colorIndex` | `[LABEL: label \| colorIndex]` |
| `dateCard` | `date` | `[DATE: timestamp]` |
| `calendar` | `currentDate` | `[CALENDAR: date]` |
| `yuque` | `src` | `[LINK: src \| 语雀文档嵌入]` |
| `datatable` | `sheetId`, `docId` | `[TABLE]` 数据表占位 `[END TABLE]` |
| `board` | — | `[DIAGRAM: board]` 画板占位 `[END DIAGRAM]` |

4. **用位置标记替换 `<card>` 标签**，然后继续标准清洗流程
5. **非 Card 的 Lake 特殊结构**也需提取内容：
   - `<blockquote class="lake-alert">` → 提取类型和内容，标记为 `[ALERT: type]` 内容 `[END ALERT]`
   - `<details class="lake-collapse">` → 提取标题和内容，标记为 `[COLLAPSE: title]` 内容 `[END COLLAPSE]`
   - `<article class="lake-columns">` → 提取各列内容，标记为 `[COLUMNS]` 列1内容 `[COL]` 列2内容 `[END COLUMNS]`
   - `<table class="lake-table">` → 提取所有行数据，标记为 `[TABLE]` 行1\|行2 `[END TABLE]`

这个过程确保 Lake 格式输入中的所有内容载体被正确解析为位置标记，不会在后续清洗中被当作普通 HTML 标签剥离。

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
| 附件 | `[FILE: src \| name \| ext]` |
| 流程图/图表 | `[DIAGRAM: type]` 代码 `[END DIAGRAM]` |

### 1b-补. 纯文本 URL 扫描

链接不只指数 `<a href>` 标签和 `<card name="yuque">` 嵌入。正文中以 `http://` 或 `https://` 开头的**纯文本 URL** 也是链接，必须保留。这类 URL 常见于从其他文档复制粘贴时遗留的裸链接（如语雀文档地址、外部系统地址）。

清洗时，除了 `lake-extract.py` 自动识别的 `<a href>` 和 `<card>` 标签链接外，AI 还必须：
1. **在 Step 0 内容清点时主动扫描提取结果中的纯文本 URL**（以 `http://` 或 `https://` 开头的文本行），计入链接数量
2. **在 Step 1 清洗时为纯文本 URL 添加 `[LINK: url | ]` 标记**，使其不被当作普通文字遗漏

遗漏纯文本 URL 是内容保全最常见的失职点。原因：纯文本 URL 不是 HTML 标签，不会被 `lake-extract.py` 的 `extract_links()` 捕获，也不会被 `verify-content.py` 的链接检测覆盖。唯一防线是 AI 在 Step 0 主动扫描。如果 Step 0 遗漏，后续所有质量门都会"正确地"放过——因为校验基准本身就错了。

### 1c. 验证

- [ ] 图片/链接/代码块/表格/附件/公式/流程图数量与 Step 0 规划表清点一致
- [ ] 链接数量包含 `<a href>` 标签链接 + `<card name="yuque">` 嵌入链接 + 纯文本 URL 三类之和
- [ ] 表格行列数完整
- [ ] 内容顺序与原文一致
- [ ] 无残留格式标记
- [ ] **Lake 输入特有**：无残留 `<card>` 标签（所有 card 已转为位置标记）

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

### 2c. 不可变元素锚定

梳理过程中重组章节、合并段落、调整顺序时，必须为 [invariants.md](knowledge/invariants.md) 中定义的每个不可变元素指定在输出结构中的位置。这叫"锚定"——每个不可变元素都必须在大纲中有一个明确的锚点。

操作方式：遍历 Step 0 内容清点中的每个元素，在梳理后的结构大纲中找到它的归属位置。如果找不到位置，说明该元素在重组中被遗漏了——回头检查是被合并了（允许）还是被删除了（不允许）。

**Gate 2 验证清单**（全部通过才能进入第三步）：
- [ ] 每个内容块已归类到 Information Mapping 6 种类型之一（Procedure/Process/Principle/Concept/Structure/Fact）
- [ ] 内容块不混杂类型（DITA 强类型分离——一个内容块不同时是步骤又是概念）
- [ ] 散乱参数/条件/话术/指标已识别并提取为结构化形式（遵循 card-guide.md 第三部分信息提取规则）
- [ ] 结构化大纲遵循文档类型的章节骨架
- [ ] 大纲中无任何伪标签或格式标记
- [ ] **不可变元素锚定**：Step 0 清点中的每个不可变元素都在大纲中有明确归属位置

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
- **内容保全校验**：运行 `python scripts/verify-content.py input output.lake`，确认输出中不可变元素数量 ≥ Step 0 规划表清点数。校验脚本返回非零退出码时，必须修正后重新输出。

## 参考文件

**知识层（AI 读取，做内容决策）**：
- [knowledge/planning-guide.md](knowledge/planning-guide.md) — 规划流程：需求分析、决策树、质量门
- [knowledge/invariants.md](knowledge/invariants.md) — 不可变元素清单（内容保全基线，所有文档类型通用）
- [knowledge/methodology.md](knowledge/methodology.md) — 文档结构化方法论（6 种信息类型、DITA、Minimalism）
- [knowledge/card-guide.md](knowledge/card-guide.md) — Card 能力目录 + 选择决策指南
- [knowledge/document-types/](knowledge/document-types/) — 10 种文档类型写作指南

**语法层（AI 读取，查阅格式规范）**：
- [reference/lake-format.md](reference/lake-format.md) — Lake 格式规范（HTML 标签用法、转义规则）
- [reference/lakebook.md](reference/lakebook.md) — .lakebook 打包结构

**执行层（AI 不读，脚本自动加载）**：
- [scripts/lake-converter.py](scripts/lake-converter.py) — 伪标签转换脚本
- [scripts/md-to-lake.py](scripts/md-to-lake.py) — Markdown 转伪标签 HTML 脚本
- [scripts/verify-content.py](scripts/verify-content.py) — 内容保全校验脚本（比对输入输出中不可变元素数量）
- [reference/tag-mapping.json](reference/tag-mapping.json) — 伪标签→Lake 语法映射表（由 lake-converter.py 加载，位于 reference/ 但属执行层）
