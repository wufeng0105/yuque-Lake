# CLAUDE.md — yuque-Lake 项目规则

## 项目概述

本项目用于语雀 Lake 格式的学习、转换和工具开发。Lake 是语雀的私有文档格式，本质是 HTML 的超集。

## 技术栈

- **Lake 格式**：HTML 超集，`<!doctype lake>` 声明，自定义 `<card>` 标签
- **编辑器核心**：`@alipay/lakex-doc` npm 包（v1.64.0+）
- **Lakebook**：tar 归档，含 `$meta.json`（tocYml YAML）和 JSON 文档条目
- **语雀 API**：format 参数支持 `markdown` 和 `lake`
- **Card 类型**：13 种有真实样本验证的 Card（codeblock, image, math, hr, diagram, checkbox, label, file, dateCard, calendar, dataTable, board, yuque）+ 4 种非 Card 结构（lake-alert, lake-collapse, lake-columns, ne-label）。详见 `skills/yuquelake/references/card-reference.md`

## 目录结构

```
yuque-Lake/
├── CLAUDE.md              # 项目规则（本文件）
├── README.md              # 项目说明
├── .gitignore
├── 验证文档集/            # 真实 .lake 样本文件
├── *.lake                # 测试导出的 .lake 文件
├── skills/                # 项目级 skill 开发目录
│   └── yuquelake/
│       ├── SKILL.md          # 四步流程主指令
│       ├── evals/             # 测试用例
│       ├── references/       # 参考文档
│       │   ├── card-reference.md    # 13 Card + 4 非 Card 结构
│       │   ├── lake-format-spec.md  # 标准 HTML 标签规范
│       │   ├── tag-mapping.json     # 伪标签→真实语法映射表
│       │   ├── methodology.md       # 文档结构化方法论
│       │   ├── lakebook-structure.md
│       │   └── document-types/      # 10 种文档类型骨架
│       └── scripts/
│           └── lake-converter.py   # 伪标签转换脚本 v4
└── .catpaw/skills/        # CatPaw 项目级 skill 部署目录（按需创建）
```

## 常用命令

```powershell
# Git 操作
git add -A && git commit -m "message"
git push origin master

# 克隆仓库（浅克隆）
git clone --depth 1 <url>

# 查询 npm 包信息
npm view @alipay/lakex-doc

# 下载 CDN 资源
Invoke-WebRequest -Uri "<url>" -OutFile "<file>"
```

## Skill 创建流程（skill-creator + writing-skills 综合）

本流程综合了 skill-creator、writing-skills 和 CatPaw create-skill 三个指南的最佳实践。

### 阶段一：需求捕获（Discovery）

1. **明确意图**：skill 能让 AI 做什么？何时触发？输出格式是什么？
2. **访谈与研究**：主动询问边界情况、输入/输出格式、示例文件、成功标准、依赖项
3. **检查可用 MCP**：研究时使用 context7、web_search 等工具并行收集上下文

### 阶段二：设计（Design）

1. **命名**：小写字母 + 数字 + 连字符，动词优先（如 `yuquelake`）
2. **描述（description）**：第三人称，以 "Use when..." 开头，只写触发条件，不写工作流摘要
3. **大纲**：规划主要章节，识别是否需要参考文件或脚本
4. **存储位置**：项目级 `.catpaw/skills/` 或个人级 `~/.catpaw/skills/`

### 阶段三：实现（Implementation）

#### SKILL.md 必需结构

```markdown
---
name: skill-name
description: Use when [具体触发条件和症状]
---

# Skill Name

## 概述
核心原则，1-2 句话。

## 何时使用
触发条件和症状列表。
何时不使用。

## 核心模式
Before/After 对比或具体步骤。

## 快速参考
表格或列表。

## 常见错误
问题 + 修复方法。
```

#### 关键规则

- **YAML frontmatter**：`name`（必需，max 64 chars）+ `description`（必需，max 1024 chars）
- **description 只写触发条件**：不要摘要工作流，否则 AI 会走捷径跳过 skill 正文
- **SKILL.md ≤ 500 行**：超长内容拆到 `references/` 目录
- **渐进式披露**：SKILL.md 放核心内容，参考文件按需加载
- **参考文件仅一层深度**：从 SKILL.md 直接链接，不嵌套
- **一个优秀示例胜过多个平庸示例**
- **路径用正斜杠**：`scripts/helper.py`，不用 `scripts\helper.py`

#### 目录结构

```
skill-name/
├── SKILL.md              # 必需 — 主指令
├── references/           # 可选 — 重型参考文档
│   └── reference.md
├── scripts/              # 可选 — 可执行脚本
│   └── helper.py
└── assets/               # 可选 — 模板、图标等
```

### 阶段四：验证（Verification）

验证清单：

- [ ] description 以 "Use when..." 开头，包含具体触发词
- [ ] description 是第三人称，不包含工作流摘要
- [ ] SKILL.md ≤ 500 行
- [ ] 术语一致（同一概念始终用同一个词）
- [ ] 文件引用仅一层深度
- [ ] 示例具体可运行，不是抽象模板
- [ ] 无时间敏感信息（如"2025年8月前用旧 API"）
- [ ] 路径使用正斜杠

### 阶段五：测试与迭代（Testing & Iteration）

#### TDD 映射

| TDD 概念 | Skill 创建 |
|-------------|----------------|
| 测试用例 | 真实用户会说的测试 prompt |
| 生产代码 | SKILL.md 文档 |
| 测试失败（RED） | 无 skill 时 AI 的基线行为 |
| 测试通过（GREEN） | 有 skill 时 AI 遵守指令 |
| 重构（REFACTOR） | 根据反馈关闭漏洞 |

#### 测试步骤（必须完整执行，不可跳过）

1. 设计 2-3 个真实用户会说的测试 prompt，保存到 `evals/evals.json`
2. **与用户确认测试用例**：“这些测试用例看起来对吗？需要增加或修改吗？”
3. **并行运行测试**：每个测试用例同时启动两个子代理：
   - with-skill：读取 SKILL.md 后执行任务，输出到 `eval-N/with_skill/outputs/`
   - without-skill（baseline）：无 skill 执行相同任务，输出到 `eval-N/without_skill/outputs/`
4. **起草 assertions**：在子代理运行期间，为每个测试用例编写可客观验证的断言
5. **评分**：子代理完成后，对每个输出逐条检查断言，保存到 `grading.json`
6. **启动 eval viewer**：用 `generate_review.py` 生成 HTML，让用户在浏览器中审查输出质量
7. **读取反馈**：用户审查后读取 `feedback.json`，空反馈表示满意
8. **迭代改进**：根据反馈修改 SKILL.md，重新运行所有测试
9. **重复**直到用户满意或反馈全空

### 阶段六：部署（Deployment）

#### CatPaw 存储位置

| 类型 | 路径 | 范围 |
|------|------|-------|
| 个人 | `~/.catpaw/skills/skill-name/` | 跨项目可用 |
| 项目 | `.catpaw/skills/skill-name/` | 仓库内共享 |

> ⚠️ **禁止**在 `~/.catpaw/skills-catpaw/` 创建 skill，该目录是系统内置 skill 专用。

#### 部署流程

1. 先在项目目录 `skills/yuquelake/` 开发和测试
2. 验证通过后复制到 `~/.catpaw/skills/yuquelake/`（全局）
3. 确认 skill 出现在 available_skills 列表中
4. 提交到 Git 并推送

## 编码规范

- Markdown 文件用 UTF-8 编码
- 路径使用正斜杠（`/`）
- YAML frontmatter 字段名用小写
- 代码块标注语言（```python, ```html, ```powershell）
- 表格使用标准 Markdown 表格语法
