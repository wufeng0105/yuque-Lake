# 知识沉淀 / 白皮书

## 章节骨架

1. **摘要** — 核心观点和结论，1-2 段
2. **背景与问题** — 行业现状、面临的挑战
3. **解决方案** — 方法论或技术方案详述
4. **技术优势** — 与现有方案对比、差异化价值
5. **实践案例** — 真实场景验证、数据支撑
6. **结论与展望** — 总结和未来方向
7. **参考资料** — 引用文献、相关链接

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 对比分析 | `<table>` |
| 架构图 | `<card-board>` |
| 数据趋势 | `<card-diagram type="mermaid">` |
| 参考链接 | `<card-yuque>` |
| 补充细节 | `<card-collapse>` |

## 轻量示范

```html
<!doctype lake>
<h1>分布式消息队列选型白皮书</h1>
<h2>摘要</h2>
<p>本文对比 Kafka、RabbitMQ、RocketMQ 三种主流消息队列在高并发订单场景下的表现，给出选型建议。</p>
<h2>背景与问题</h2>
<p>随着业务量增长，日均订单量突破千万级，同步调用导致接口超时频发。引入消息队列实现异步解耦成为迫切需求。</p>
<h2>方案对比</h2>
<table><tbody>
<tr><td>维度</td><td>Kafka</td><td>RabbitMQ</td><td>RocketMQ</td></tr>
<tr><td>吞吐量</td><td>百万级/秒</td><td>万级/秒</td><td>十万级/秒</td></tr>
<tr><td>延迟</td><td>毫秒级</td><td>微秒级</td><td>毫秒级</td></tr>
<tr><td>事务消息</td><td>不支持</td><td>不支持</td><td>支持</td></tr>
<tr><td>运维复杂度</td><td>中</td><td>低</td><td>高</td></tr>
</tbody></table>
<h2>推荐方案</h2>
<p>订单场景需要事务消息支持，且吞吐量要求十万级以上，推荐 RocketMQ。</p>
<card-collapse title="详细测试数据">
<p>在 1000 万消息堆积下，RocketMQ 消费延迟稳定在 50ms 以内，满足业务要求。</p>
</card-collapse>
<h2>结论</h2>
<p>对于需要事务保障的高并发订单系统，RocketMQ 是当前最优选择。</p>
<h2>参考资料</h2>
<card-yuque src="https://rocketmq.apache.org/docs/"/>
```
