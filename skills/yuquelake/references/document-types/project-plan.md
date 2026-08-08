# 项目计划

## 章节骨架

1. **项目目标** — 项目要达成什么、成功标准
2. **范围说明** — 包含什么、不包含什么
3. **工作分解结构** — 将项目拆分为可管理的任务包
4. **进度计划** — 甘特图、里程碑、关键路径
5. **资源分配** — 人员、设备、预算
6. **风险管理** — 风险列表、影响评估、应对措施
7. **沟通计划** — 汇报频率、沟通渠道、干系人

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 甘特图 | `<card-diagram type="mermaid">` |
| 工作分解 | `<card-board>` |
| 里程碑 | `<card-dateline>` / `<table>` |
| 资源分配 | `<table>` |
| 风险矩阵 | `<table>` |

## 轻量示范

```html
<!doctype lake>
<h1>积分系统项目计划</h1>
<h2>项目目标</h2>
<p>2024 年 12 月 31 日前上线会员积分系统，支撑日均 100 万用户。</p>
<h2>范围说明</h2>
<p><strong>包含</strong>：积分获取、积分兑换、积分明细查询。</p>
<p><strong>不包含</strong>：积分商城（二期）。</p>
<h2>工作分解结构</h2>
<card-board>
- 积分系统
  - 需求分析
  - 架构设计
  - 开发
    - 积分获取
    - 积分兑换
    - 积分明细
  - 测试
  - 上线
</card-board>
<h2>进度计划</h2>
<card-diagram type="mermaid">
title 积分系统项目甘特图
section 需求
需求分析 :a1, 2024-10-01, 10d
section 设计
架构设计 :a2, after a1, 7d
section 开发
积分获取 :a3, after a2, 14d
积分兑换 :a4, after a2, 10d
section 测试
集成测试 :a5, after a3, 7d
section 上线
上线部署 :a6, after a5, 3d
</card-diagram type="mermaid">
<h2>里程碑</h2>
<table><tbody>
<tr><td>需求评审完成</td><td>10-10</td></tr>
<tr><td>开发完成</td><td>11-15</td></tr>
<tr><td>测试通过</td><td>12-10</td></tr>
<tr><td>正式上线</td><td>12-20</td></tr>
</tbody></table>
<h2>风险管理</h2>
<table><tbody>
<tr><td>风险</td><td>影响</td><td>概率</td><td>应对</td></tr>
<tr><td>第三方支付接口延期</td><td>高</td><td>中</td><td>提前对接，准备 Mock</td></tr>
<tr><td>高并发性能不达标</td><td>高</td><td>低</td><td>压测验证</td></tr>
</tbody></table>
```
