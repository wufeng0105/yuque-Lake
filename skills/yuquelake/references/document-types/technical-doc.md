# 技术文档（架构说明）

## 章节骨架

1. **文档概述** — 编写目的、适用范围、版本历史
2. **需求与目标** — 业务背景、功能需求、非功能需求
3. **系统架构** — 总体架构图、模块划分、交互流程
4. **核心模块设计** — 每个模块的功能、输入输出、接口定义
5. **技术选型** — 技术栈及选型理由
6. **数据设计** — ER 图、数据表结构、索引设计
7. **部署架构** — 环境配置、部署拓扑图
8. **风险与对策** — 技术风险及应对措施

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 架构图 | `<card-board>` / `<card-diagram type="mermaid">` |
| 模块设计 | `<card-collapse>` |
| 技术选型 | `<table>` |
| 数据结构 | `<table>` / `<card-codeblock mode="sql">` |
| 部署拓扑 | `<card-board>` |

## 轻量示范

```html
<!doctype lake>
<h1>订单系统架构设计文档</h1>
<h2>文档概述</h2>
<p>本文档描述订单系统的架构设计，指导开发实施。</p>
<h2>需求与目标</h2>
<p>支持日均 100 万订单量，响应时间 ≤ 200ms。</p>
<h2>系统架构</h2>
<card-diagram type="mermaid">
graph TD
  A[用户端] --> B[API 网关]
  B --> C[订单服务]
  C --> D[数据库]
  C --> E[消息队列]
</card-diagram type="mermaid">
<h2>核心模块设计</h2>
<card-collapse title="订单创建模块">
<p>接收用户下单请求，校验库存，生成订单记录，发送消息到队列。</p>
</card-collapse>
<card-collapse title="订单支付模块">
<p>对接支付网关，处理支付回调，更新订单状态。</p>
</card-collapse>
<h2>技术选型</h2>
<table><tbody>
<tr><td>语言</td><td>Go</td><td>高并发、低延迟</td></tr>
<tr><td>数据库</td><td>PostgreSQL</td><td>事务支持完善</td></tr>
<tr><td>消息队列</td><td>Kafka</td><td>高吞吐量</td></tr>
</tbody></table>
<h2>风险与对策</h2>
<card-label label="风险"/>
<p>数据库单点故障 → 主从复制 + 自动切换</p>
```
