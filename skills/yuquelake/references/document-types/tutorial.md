# 教程

## 章节骨架

1. **引言与概述** — 学习目标、前置知识、适用人群
2. **基础知识** — 必要的理论背景和概念
3. **核心内容** — 分步骤讲解，每步配示例
4. **实践与练习** — 动手任务，巩固所学
5. **总结与扩展** — 回顾要点、推荐进阶资源

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 代码示例 | `<card-codeblock>` |
| 流程说明 | `<card-diagram type="mermaid">` |
| 知识点总结 | `<card-collapse>` |
| 注意事项 | `<card-label label="提示">` |
| 图片说明 | `<card-image>` |

## 轻量示范

```html
<!doctype lake>
<h1>Python 数据分析入门教程</h1>
<h2>引言</h2>
<p>本教程帮助你从零开始使用 Python 进行数据分析。</p>
<p><strong>学习目标</strong>：掌握 pandas 数据读取、清洗、分析全流程。</p>
<p><strong>前置知识</strong>：Python 基础语法。</p>
<h2>基础知识</h2>
<p>pandas 是 Python 最常用的数据分析库，核心数据结构是 DataFrame。</p>
<h2>核心内容</h2>
<card-collapse title="第一步：安装环境">
<card-codeblock mode="shell">
pip install pandas jupyter
</card-codeblock>
</card-collapse>
<card-collapse title="第二步：读取数据">
<card-codeblock mode="python">
import pandas as pd
df = pd.read_csv("data.csv")
print(df.head())
</card-codeblock>
</card-collapse>
<card-collapse title="第三步：数据清洗">
<card-codeblock mode="python">
df = df.dropna()
df["price"] = df["price"].astype(float)
</card-codeblock>
</card-collapse>
<h2>实践与练习</h2>
<card-label label="练习"/>
<p>下载销售数据集，完成以下任务：</p>
<ol>
<li>统计每个地区的销售总额</li>
<li>找出销售额 Top 10 的产品</li>
</ol>
<h2>总结</h2>
<p>本教程介绍了 pandas 数据分析的基本流程：读取 → 清洗 → 分析。</p>
```
