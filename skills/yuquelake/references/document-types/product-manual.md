# 产品手册 / 用户指南

## 章节骨架

1. **简介** — 产品定位、核心功能概述
2. **快速上手** — 最短路径完成首次使用
3. **产品概述** — 界面布局、核心概念
4. **使用指南** — 分功能模块详解（基础 → 高级）
5. **故障排除** — 常见问题、原因和解决方案
6. **技术规格** — 参数、兼容性
7. **附录** — FAQ、术语表、快捷键、版本日志

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 界面说明 | `<card-image>` |
| 操作步骤 | `<card-collapse>` |
| FAQ | `<card-collapse>` |
| 快捷键 | `<table>` |
| 视频教程 | `<card-video>` |

## 轻量示范

```html
<!doctype lake>
<h1>数据分析平台用户手册</h1>
<h2>简介</h2>
<p>数据分析平台是面向运营团队的自助式数据分析和可视化工具。</p>
<h2>快速上手</h2>
<card-image src="https://example.com/quick-start.png" name="快速入门流程图"/>
<p>三步完成首次分析：导入数据 → 选择图表 → 配置维度。</p>
<h2>产品概述</h2>
<p>平台分为四大模块：数据源、数据集、仪表盘、报告。</p>
<h2>使用指南</h2>
<card-collapse title="创建数据源">
<p>进入「数据源」页面，点击新建，选择数据库类型，填写连接信息。</p>
<card-label label="提示"/>
<p>建议使用只读账号连接数据库，避免误操作。</p>
</card-collapse>
<card-collapse title="制作仪表盘">
<p>在「仪表盘」页面拖拽数据集字段到行列区域，自动生成图表。</p>
</card-collapse>
<h2>故障排除</h2>
<card-collapse title="数据源连接失败">
<p><strong>现象</strong>：测试连接提示超时。</p>
<p><strong>原因</strong>：数据库未开放平台 IP 访问权限。</p>
<p><strong>解决</strong>：在数据库白名单中添加平台 IP。</p>
</card-collapse>
<h2>快捷键</h2>
<table><tbody>
<tr><td>Ctrl + S</td><td>保存仪表盘</td></tr>
<tr><td>Ctrl + D</td><td>复制图表</td></tr>
<tr><td>Ctrl + Z</td><td>撤销操作</td></tr>
</tbody></table>
```
