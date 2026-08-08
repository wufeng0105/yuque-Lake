# PRD（产品需求文档）

## 章节骨架

1. **产品简介** — 一句话描述产品核心价值、版本说明
2. **产品概览** — 功能清单、项目排期
3. **产品架构** — 信息结构图、产品结构图、业务流程图
4. **功能需求** — 每个功能的详细说明（页面、交互、规则）
5. **非功能需求** — 性能、安全、埋点
6. **附录** — 术语表、参考资料

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 功能清单 | `<table>` |
| 产品结构 | `<card-board>` |
| 业务流程 | `<card-diagram type="mermaid">` |
| 原型说明 | `<card-image>` + `<card-collapse>` |
| 排期 | `<card-diagram type="mermaid">` / `<table>` |

## 轻量示范

```html
<!doctype lake>
<h1>会员积分系统 PRD v1.0</h1>
<h2>产品简介</h2>
<p>为平台用户建立积分体系，通过消费和互动获取积分，提升用户粘性。</p>
<h2>功能清单</h2>
<table><tbody>
<tr><td>积分获取</td><td>消费按 1:1 累积积分</td><td>P0</td></tr>
<tr><td>积分兑换</td><td>积分兑换优惠券</td><td>P0</td></tr>
<tr><td>积分明细</td><td>查看积分收支记录</td><td>P1</td></tr>
</tbody></table>
<h2>产品架构</h2>
<card-diagram type="mermaid">
graph TD
  A[用户] --> B[消费]
  B --> C[积分增加]
  A --> D[兑换]
  D --> E[积分减少]
</card-diagram type="mermaid">
<h2>功能需求</h2>
<card-collapse title="积分获取规则">
<p><strong>触发条件</strong>：订单支付成功后触发。</p>
<p><strong>计算公式</strong>：积分 = 订单金额 × 会员等级系数。</p>
<p><strong>入账时间</strong>：T+1 日入账。</p>
<card-label label="边界情况"/>
<p>退款订单扣除对应积分，不足时积分变为负数并标记待补足。</p>
</card-collapse>
<h2>非功能需求</h2>
<p>积分计算接口响应时间 ≤ 100ms，支持并发 500 QPS。</p>
```
