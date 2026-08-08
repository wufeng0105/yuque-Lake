# 设计规范

## 章节骨架

1. **设计原则** — 价值观、设计理念
2. **设计令牌** — 颜色、字体、间距、圆角、阴影
3. **组件规范** — 每个组件的用法、属性、变体
4. **布局规则** — 栅格系统、响应式断点
5. **交互规范** — 动效、手势、状态转换
6. **无障碍** — 对比度、键盘操作、屏幕阅读器
7. **附录** — 版本历史、贡献指南

## 推荐 Lake Card

| 章节 | 推荐 Card |
|------|----------|
| 颜色色板 | `<table>` + `<card-image>` |
| 组件示例 | `<card-image>` |
| 布局栅格 | `<card-board>` |
| 交互动效 | `<card-video>` |
| 代码片段 | `<card-codeblock mode="css">` |

## 轻量示范

```html
<!doctype lake>
<h1>产品设计规范 v2.0</h1>
<h2>设计原则</h2>
<card-label label="核心原则"/>
<ol>
<li>一致性：相同含义的元素在全产品中表现一致</li>
<li>反馈：每个操作都有即时的视觉反馈</li>
<li>效率：最少点击完成目标操作</li>
</ol>
<h2>设计令牌</h2>
<card-collapse title="颜色">
<table><tbody>
<tr><td>--color-primary</td><td>#1890FF</td><td>主色</td></tr>
<tr><td>--color-success</td><td>#52C41A</td><td>成功</td></tr>
<tr><td>--color-danger</td><td>#FF4D4F</td><td>危险</td></tr>
</tbody></table>
<card-codeblock mode="css">
:root {
  --color-primary: #1890FF;
  --color-success: #52C41A;
  --color-danger: #FF4D4F;
}
</card-codeblock>
</card-collapse>
<card-collapse title="间距">
<p>基础间距 4px，间距阶数按 4 的倍数递增。</p>
<table><tbody>
<tr><td>--spacing-xs</td><td>4px</td></tr>
<tr><td>--spacing-sm</td><td>8px</td></tr>
<tr><td>--spacing-md</td><td>16px</td></tr>
<tr><td>--spacing-lg</td><td>24px</td></tr>
</tbody></table>
</card-collapse>
<h2>组件规范</h2>
<card-collapse title="按钮 Button">
<p>按钮有三种类型：主要、次要、文字。</p>
<card-image src="https://example.com/button-types.png" name="按钮类型"/>
<table><tbody>
<tr><td>type</td><td>primary / default / text</td><td>按钮类型</td></tr>
<tr><td>size</td><td>large / middle / small</td><td>按钮大小</td></tr>
<tr><td>disabled</td><td>boolean</td><td>是否禁用</td></tr>
</tbody></table>
</card-collapse>
<h2>无障碍</h2>
<p>文本与背景对比度不低于 4.5:1（WCAG AA 标准）。</p>
```
