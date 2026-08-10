# CLAUDE.md — yuque-Lake 项目

## 项目定位

AI Skill 项目，将任意格式文档转换为语雀 Lake 格式（`.lake` 文件）。

核心设计原则：**四步流程，职责分离**——AI 负责内容语义（步骤 0-3），脚本负责机械语法（步骤 4）。各层之间通过明确接口协作，不越界。

## 技术栈

- **AI Skill**：SKILL.md + knowledge + reference + scripts，遵循渐进式加载
- **脚本**：Python 3，无第三方依赖（仅标准库）

## 目录结构

```
skills/yuquelake/
├── SKILL.md                          # 流程控制器 + 红线规则
├── knowledge/                         # 知识层 — AI 的内容决策依据
│   ├── invariants.md                 #   不可变元素清单（内容保全基线）
│   ├── planning-guide.md             #   规划流程：需求分析、决策树、质量门
│   ├── methodology.md                #   方法论约束（6 种信息类型、DITA、Minimalism）
│   ├── card-guide.md                 #   Card 能力目录 + 选择决策指南
│   └── document-types/               #   10 种文档类型写作指南
│       ├── sop.md
│       ├── technical-doc.md
│       ├── api-doc.md
│       ├── tutorial.md
│       ├── prd.md
│       ├── meeting-notes.md
│       ├── project-plan.md
│       ├── whitepaper.md
│       ├── product-manual.md
│       └── design-spec.md
├── reference/                         # 语法层 — 纯查阅手册
│   ├── lake-format.md                #   Lake 格式规范
│   ├── tag-mapping.json              #   伪标签→Lake 语法映射表（脚本加载，AI 不读）
│   └── lakebook.md                   #   .lakebook 结构
├── scripts/                           # 执行层 — 机械转换
│   ├── lake-converter.py             #   伪标签 → .lake
│   ├── md-to-lake.py                 #   Markdown → 伪标签 HTML
│   └── verify-content.py             #   内容保全校验（比对不可变元素数量）
└── evals/
    ├── evals.json
    └── fixtures/
```

## 四步架构与职责边界

| 步骤 | 执行者 | 职责 | 质量门 |
|------|--------|------|--------|
| Step 0 规划 | AI | 需求分析，内容清点，输出规划表 | 门 0：展示规划表（含内容清点） |
| Step 1 清洗 | AI | 剥离格式标记，保留内容 + 位置标记 | 门 1：不可变元素标记数 ≥ 清点数 |
| Step 2 梳理 | AI | 判断文档类型，重组内容结构 | 门 2：每个不可变元素都有对应位置 |
| Step 3 伪代码 | AI | 选择伪标签，生成伪标签 HTML | 门 3：展示伪标签 HTML |
| Step 4 语法 | lake-converter.py | 伪标签 → 真实 .lake 文件 | 门 4：运行 verify-content.py 校验 |

## 内容保全机制

- **invariants.md** 定义 9 类不可变元素（图片、链接、代码块、表格、附件、公式、流程图、话术、金额）
- **verify-content.py** 程序化校验输出中不可变元素数量 ≥ 输入清点数
- **红线规则**（SKILL.md §红线规则）：6 条绝对禁令，违反即输出不合格
- **归类原则**：document-types 中"归类（非核心）"列取代"删除"列——内容不可删除，只能移动到附录/折叠面板

## 常用命令

```powershell
# 内容保全校验
python skills/yuquelake/scripts/verify-content.py input output.lake

# 转换伪标签 HTML 为 .lake
python skills/yuquelake/scripts/lake-converter.py input.html output.lake --title "标题"

# Markdown 转伪标签 HTML
python skills/yuquelake/scripts/md-to-lake.py input.md output.html
```

## 已知问题

- `data-lake-id` 自动生成、`<span>` 文本包裹、列表拆分功能在 tag-mapping.json 中声明但脚本未实现。语雀编辑器导入时自动补全，不阻塞导入
- `lake-generator.py`（.lakebook 打包脚本）尚未实现
