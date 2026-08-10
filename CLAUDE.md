# CLAUDE.md — yuque-Lake 项目

## 项目定位

这是一个 AI Skill 项目，将任意格式文档转换为语雀 Lake 格式（`.lake` 文件）。

核心设计原则：**四步流程，职责分离**——AI 负责内容语义（步骤 0-3），脚本负责机械语法（步骤 4）。各层之间通过明确的接口契约协作，不越界。

## 技术栈

- **AI Skill**：SKILL.md + knowledge + reference + scripts，遵循渐进式加载（SKILL.md < 200 行，详情按需读取）
- **脚本**：Python 3，无第三方依赖（仅标准库）
- **测试**：unittest，109 个用例覆盖两个脚本的核心函数

## 四步架构与职责边界

| 步骤 | 执行者 | 职责 | 读取的参考文件 | 禁止越界 |
|------|--------|------|--------------|---------|
| Step 0 规划 | AI | 分析需求，选择路径，输出规划表 | planning-guide.md | 不碰格式语法 |
| Step 1 清洗 | AI（或 md-to-lake.py 辅助） | 剥离格式标记，保留内容 + 位置标记 | SKILL.md 中的清洗规则 | 不做内容重组 |
| Step 2 梳理 | AI（核心步骤） | 判断文档类型，重组内容结构 | knowledge/document-types/*.md + methodology.md | 不碰任何语法标签 |
| Step 3 伪代码 | AI | 在梳理好的结构上选择伪标签 | knowledge/card-guide.md | 不重做内容决策 |
| Step 4 语法 | lake-converter.py | 伪标签 → 真实 .lake 文件 | reference/tag-mapping.json（脚本读取，AI 不读） | 不做任何内容修改 |

**职责分离的红线**：
- 知识层（document-types）只管"写什么内容、怎么组织"——不准出现"推荐 Card"固定映射表，不准在"语法选择"章节列出内容块到 Card 的映射条目
- 语法层（card-guide）管"什么内容特征用什么 Card" + "散乱信息如何提取"——不准出现语法细节（属性列表、JSON 结构、真实 HTML）
- 执行层（scripts + tag-mapping.json）只管机械转换——不准做内容决策

## 目录结构（重构后目标）

```
skills/yuquelake/
├── SKILL.md                         # 流程控制器（只管"做什么、何时读什么"）
├── knowledge/                        # 知识层 — AI 的内容决策依据
│   ├── document-types/               #   文档类型写作指南（全部按 sop.md 模式）
│   │   ├── sop.md                    #   已优化，作为模板
│   │   ├── technical-doc.md
│   │   ├── api-doc.md
│   │   ├── tutorial.md
│   │   ├── prd.md
│   │   ├── meeting-notes.md
│   │   ├── project-plan.md
│   │   ├── whitepaper.md
│   │   ├── product-manual.md
│   │   └── design-spec.md
│   ├── methodology.md                #   方法论约束（与文档类型关联）
│   └── card-guide.md                 #   Card 能力目录 + 选择决策指南
├── reference/                        # 语法层 — 纯查阅手册
│   ├── lake-format.md                #   Lake 格式规范（纯格式，无 SOP 样例）
│   ├── tag-mapping.json              #   脚本配置（AI 不读）
│   └── lakebook.md                   #   .lakebook 结构
├── scripts/                          # 执行层 — 机械转换
│   ├── lake-converter.py
│   └── md-to-lake.py
└── evals/
    ├── evals.json
    └── fixtures/
tests/
└── unit/
    ├── test_lake_converter.py
    └── test_md_to_lake.py
```

## 各层文件规范

### SKILL.md（流程控制器）

- 只包含：流程概述、何时使用/不使用、质量门、各步骤指引到对应文件的链接
- 行数控制 < 200 行
- 禁止内联详细的清洗规则表、文档类型表、伪标签表（这些在各层参考文件中）
- 禁止引用 tag-mapping.json（那是脚本配置，AI 不需要读）
- 伪标签格式极简（`<card-type attr="val">内容</card-type>`），在 SKILL.md 中一次性说明即可，不需要专门的语法参考文件

### knowledge/document-types/*.md（文档类型写作指南）

每个文件必须包含以下结构，统一以 sop.md 为模板：

```markdown
# 你是 XX 文档写作专家

## 你的角色
（角色定义 + 专业能力描述）

## 内容验证
（清洗后验证 Checklist，继承 SKILL.md 的通用门 + 文档类型专属检查项）

## 写作规则
### 结构规则
（章节骨架 + 每章的写作约束，不是简单的标题列表）
### 内容取舍规则
（保留什么、简化什么、删除什么——基于 Information Mapping 6 种信息类型）

## 语法选择
根据内容特征自主选择伪标签。**进入此步前，必须先完整阅读 card-guide.md**——未阅读不得选择任何伪标签。
```

**禁止**：
- 禁止出现"推荐 Lake Card"固定映射表（如 `| 章节 | 推荐 Card |`）
- 禁止在"语法选择"章节列出内容块到 Card 的映射条目（那是 card-guide.md 的事）
- 禁止包含完整的"轻量示范"伪标签 HTML（那是语法层的事）
- 禁止出现伪标签的语法细节（属性列表、JSON 结构等——那是执行层的事）

**必须**：
- 标注该文档类型主要涉及 methodology.md 中的哪些信息类型（如 SOP 以 Procedure 为主）
- 写作规则要具体到可执行，不是泛泛而谈

### knowledge/card-guide.md（Card 能力目录 + 选择决策指南 + 信息提取规则）

这是替代固化的"推荐 Card"表和旧版语法参考的关键文件。包含四个部分：

**第一部分：Card 能力目录**

每种 Card 一段描述：它是什么、适合什么内容、不适合什么场景。不写语法细节（不写属性列表、不写 JSON 结构、不写真实 HTML），只写"这个 Card 能做什么，什么情况下用它"。

**第二部分：选择决策指南**

采用三级优先决策树：先判断信息类型（Information Mapping 6 种），再按类型匹配内容块模式，最后选择呈现形式。决策树按信息类型分组，不扁平罗列。

**第三部分：信息提取规则**

定义散乱信息的识别与结构化提取规则。包含规则总表（散乱信息特征 → 提取为 table/列表）、提取决策树（3 步判断流程）、提取示例、提取约束。

**第四部分：布局建议**

图片、折叠面板、提示框、多栏、分割线、表格的布局规则。

**核心原则**：AI 只需要知道"什么内容用什么 Card"和"散乱信息怎么提取"，不需要知道"Card 的语法长什么样"。伪标签格式本身极简（`<card-type attr="val">内容</card-type>`），在 SKILL.md 中一次性说明即可。真正复杂的语法（JSON 构造、URL 编码）都是步骤 4 脚本的事。

### knowledge/methodology.md（方法论约束）

- 定义 6 种信息类型、DITA 3 种主题类型、Minimalism 原则
- 每个 document-types 文件引用其中的具体信息类型（不是泛泛引用整个文件）
- 不是孤岛——必须在文档类型写作规则中落地应用

### reference/lake-format.md（Lake 格式规范）

- 纯格式：文档结构、HTML 标签用法、转义规则、data-lake-id 规则
- 禁止出现"SOP 使用样例"段落
- 禁止重复 pseudo-tags.md 的内容

### reference/tag-mapping.json（脚本配置）

- 纯机器配置：cardName, cardType, selfClosing, attributes, jsonTemplate
- AI 不读此文件——SKILL.md 的参考列表中不包含它
- lake-converter.py 启动时加载并验证与 Python Card 定义同步
- standardHtmlTags 中声明但脚本未实现的功能（data-lake-id, span 包裹, 列表拆分）必须在文档中明确标注为"待实现"

### scripts/（执行层）

- `lake-converter.py`：伪标签 HTML → .lake 文件。只做机械转换，不做内容决策
- `md-to-lake.py`：Markdown → 伪标签 HTML。辅助完成步骤 1（清洗）和步骤 3（格式转换），不做步骤 2（内容重组）
- 两个脚本的 docstring 必须准确描述其职责范围，不夸大

## 语雀 MCP（开发辅助，不集成进 skill）

语雀 MCP 是开发和维护 skill 的辅助工具，用于补充知识、验证结果。skill 本身保持解耦，不依赖 MCP。

MCP 能力：读取知识库/文档、创建/更新文档、搜索、管理 TOC 和小记、管理 board 资源。

开发场景：
1. **补充文档类型知识**：读取语雀 SOP 知识库中的真实文档（如旅行计划、团建活动、工作周报等），分析不同文档类型的实际结构和内容模式，用于完善 knowledge/document-types/*.md
2. **逆向学习 Lake 语法**：读取真实语雀文档的 lake 格式源码，学习 Card 的真实 JSON 结构和属性，用于完善 tag-mapping.json 和 card-guide.md
3. **验证转换结果**：转换后的 .lake 文件可通过 MCP 创建到语雀知识库，人工验证渲染效果

用户语雀账号：feng-oftto
- 知识库1：默认知识库（namespace: feng-oftto/gpqwqv）
- 知识库2：SOP（namespace: feng-oftto/uza1bs，17 篇文档）

SOP 知识库文档类型分布：SOP/流程类（旅行计划、团建活动、工作周报）、技术类（系分文档、接口文档、架构图）、产品类（需求文档、需求管理、用研报告）、管理类（项目立项、项目复盘、会议记录、看板）、其他（程序员最爱的功能、画册、缺陷管理、故障复盘）

## 测试与验证

- 测试框架：unittest（不依赖 pytest）
- 测试文件：`tests/unit/test_lake_converter.py`（61 个用例）、`tests/unit/test_md_to_lake.py`（48 个用例）
- 加载带连字符文件名的脚本使用 `importlib.util`，不能用 `import`
- 运行测试：`python -m unittest tests.unit.test_lake_converter tests.unit.test_md_to_lake -v`
- 修改脚本后必须运行测试确认无回归

## 重构执行规则

执行重构时遵循以下顺序和约束：

### 执行顺序

1. **先建目录结构**：创建 `knowledge/` 和 `reference/` 目录
2. **迁移语法层文件**：`card-reference.md` 内容拆分——Card 能力描述和选择指南迁移到 `knowledge/card-guide.md`，语法细节（属性、JSON 结构）直接删除（AI 不需要）。`lake-format-spec.md` → `reference/lake-format.md`（同时删除 SOP 样例），`tag-mapping.json` → `reference/tag-mapping.json`，`lakebook-structure.md` → `reference/lakebook.md`
3. **创建 card-guide.md**：合并旧 card-reference.md 的 Card 能力描述 + 从各 document-types 文件"推荐 Card"表提取的决策树，放在 `knowledge/card-guide.md`
4. **迁移文档类型文件**：`document-types/*.md` → `knowledge/document-types/*.md`，同时逐个升级为"写作专家"模式（以 sop.md 为模板）
5. **迁移 methodology.md**：`methodology.md` → `knowledge/methodology.md`，并在每个 document-types 文件中建立引用关系
6. **重写 SKILL.md**：精简为流程控制器，更新所有文件路径引用
7. **更新脚本中的路径引用**：`lake-converter.py` 中 `tag-mapping.json` 的相对路径
8. **更新测试中的路径引用**：测试文件中加载脚本的路径
9. **更新 evals.json**：文件路径引用
10. **运行测试验证**：确保所有测试通过

### 约束

- **不删除任何脚本代码**：scripts/ 下的代码只改路径引用，不改逻辑
- **不改变 tag-mapping.json 的数据结构**：只改文件位置
- **保留 sop.md 的内容不变**：它是模板，其他文件向它看齐
- **每个 document-types 文件必须标注信息类型**：在"写作规则"中引用 methodology.md 的具体信息类型
- **card-guide.md 不允许出现语法细节**（属性列表、JSON 结构、真实 HTML）：只写 Card 能力、选择决策指南、信息提取规则和布局建议
- **document-types 文件的"语法选择"章节只包含引导语**：不列内容块到 Card 的映射条目，强制引导 AI 阅读 card-guide.md
- **Gate 2 验证清单包含信息类型标注和信息提取验证**：不是新增门，是在现有门中增强检查项
- **lake-format.md 中不允许出现任何"SOP 使用样例"段落**
- **不再保留 pseudo-tags.md**：Card 能力描述合并到 card-guide.md，语法细节归 tag-mapping.json（脚本读）
- **SKILL.md 的参考文件列表中不包含 tag-mapping.json**：它是脚本配置，AI 不读

## 常用命令

```powershell
# 运行测试
python -m unittest tests.unit.test_lake_converter tests.unit.test_md_to_lake -v

# 转换伪标签 HTML 为 .lake
python skills/yuquelake/scripts/lake-converter.py input.html output.lake --title "标题"

# Markdown 转伪标签 HTML
python skills/yuquelake/scripts/md-to-lake.py input.md output.html
```

## 已知问题与注意事项

- `data-lake-id` 自动生成、`<span>` 文本包裹、列表拆分功能在 tag-mapping.json 中声明但脚本未实现。语雀编辑器导入时会自动补全这些属性，当前版本不阻塞导入
- `lake-generator.py`（.lakebook 打包脚本）尚未实现，文档中已标注手动打包方案
- `md-to-lake.py` 只做步骤 1（清洗）和步骤 3（格式转换），不做步骤 2（内容重组）。`planning-guide.md` 中如仍引用旧的"自动完成步骤 1-3"描述，需同步修正
