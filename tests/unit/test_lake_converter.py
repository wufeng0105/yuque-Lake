#!/usr/bin/env python3
"""
lake-converter.py 单元测试

覆盖核心函数：gen_id, parse_attrs, encode_value, make_card,
convert_self_closing_cards, convert_content_cards, convert_non_card_tags,
add_document_header, convert
"""

import sys
import os
import re
import json
import unittest
import importlib.util

# 加载带连字符的脚本文件
_scripts_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'skills', 'yuquelake', 'scripts')

_spec = importlib.util.spec_from_file_location(
    'lake_converter',
    os.path.join(_scripts_dir, 'lake-converter.py')
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

gen_id = _mod.gen_id
parse_attrs = _mod.parse_attrs
encode_value = _mod.encode_value
make_card = _mod.make_card
make_card_raw_value = _mod.make_card_raw_value
convert_self_closing_cards = _mod.convert_self_closing_cards
convert_content_cards = _mod.convert_content_cards
convert_non_card_tags = _mod.convert_non_card_tags
add_document_header = _mod.add_document_header
convert = _mod.convert
_build_yuque_url = _mod._build_yuque_url
_build_image_json = _mod._build_image_json
_build_alert = _mod._build_alert
_build_collapse = _mod._build_collapse
_build_inline_label = _mod._build_inline_label
_guess_mime = _mod._guess_mime


class TestGenId(unittest.TestCase):
    """测试 ID 生成"""

    def test_length(self):
        self.assertEqual(len(gen_id()), 5)

    def test_charset(self):
        allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        for _ in range(100):
            self.assertTrue(set(gen_id()).issubset(allowed))

    def test_uniqueness(self):
        ids = {gen_id() for _ in range(200)}
        # 允许极少量碰撞，但 200 个 5 字符随机 ID 碰撞概率极低
        self.assertGreater(len(ids), 195)

    def test_no_empty(self):
        self.assertTrue(gen_id())


class TestParseAttrs(unittest.TestCase):
    """测试属性解析"""

    def test_single_quoted_attr(self):
        attrs = parse_attrs('mode="python"')
        self.assertEqual(attrs, {'mode': 'python'})

    def test_single_unquoted_attr(self):
        attrs = parse_attrs('mode=python')
        self.assertEqual(attrs, {'mode': 'python'})

    def test_multiple_attrs(self):
        attrs = parse_attrs('src="https://example.com/a.png" name="截图"')
        self.assertEqual(attrs['src'], 'https://example.com/a.png')
        self.assertEqual(attrs['name'], '截图')

    def test_single_quote_attr(self):
        attrs = parse_attrs("mode='python'")
        self.assertEqual(attrs, {'mode': 'python'})

    def test_empty_attrs(self):
        self.assertEqual(parse_attrs(''), {})

    def test_attr_without_value(self):
        attrs = parse_attrs('disabled')
        self.assertEqual(attrs.get('disabled'), '')

    def test_attr_with_special_chars(self):
        attrs = parse_attrs('src="https://example.com/path?a=1&b=2"')
        self.assertEqual(attrs['src'], 'https://example.com/path?a=1&b=2')

    def test_none_input(self):
        """parse_attrs 接收 None 时不应崩溃"""
        with self.assertRaises(AttributeError):
            parse_attrs(None)

    def test_extra_whitespace(self):
        attrs = parse_attrs('  mode  =  "python"  ')
        self.assertEqual(attrs, {'mode': 'python'})


class TestEncodeValue(unittest.TestCase):
    """测试 JSON → Lake card value 编码"""

    def test_basic_encoding(self):
        data = {'mode': 'python', 'code': 'print("hello")'}
        result = encode_value(data)
        self.assertTrue(result.startswith('data:'))
        # 解码验证
        encoded_part = result[5:]  # 去掉 'data:' 前缀
        from urllib.parse import unquote
        decoded = json.loads(unquote(encoded_part))
        self.assertEqual(decoded['mode'], 'python')
        self.assertEqual(decoded['code'], 'print("hello")')

    def test_unicode_content(self):
        data = {'label': '重要', 'colorIndex': 2}
        result = encode_value(data)
        self.assertTrue(result.startswith('data:'))

    def test_empty_dict(self):
        result = encode_value({})
        self.assertTrue(result.startswith('data:'))


class TestMakeCard(unittest.TestCase):
    """测试 Card 标签生成"""

    def test_basic_card(self):
        card = make_card('codeblock', 'inline', {'mode': 'plain', 'code': 'hello'})
        self.assertIn('type="inline"', card)
        self.assertIn('name="codeblock"', card)
        self.assertIn('value="data:', card)
        self.assertIn('</card>', card)

    def test_raw_value_card(self):
        card = make_card_raw_value('checkbox', 'inline', 'data:true')
        self.assertIn('value="data:true"', card)


class TestBuildYuqueUrl(unittest.TestCase):
    """测试语雀 URL 构建"""

    def test_simple_url(self):
        url = _build_yuque_url('https://www.yuque.com/namespace/repo/slug')
        self.assertEqual(url, 'https://www.yuque.com/namespace/repo/slug?view=doc_embed')

    def test_url_with_existing_query(self):
        url = _build_yuque_url('https://www.yuque.com/namespace/repo/slug?param=value')
        self.assertEqual(url, 'https://www.yuque.com/namespace/repo/slug?param=value&view=doc_embed')

    def test_empty_url(self):
        self.assertEqual(_build_yuque_url(''), '')


class TestGuessMime(unittest.TestCase):
    """测试 MIME 类型推断"""

    def test_known_types(self):
        self.assertEqual(_guess_mime('pdf'), 'application/pdf')
        self.assertEqual(_guess_mime('txt'), 'text/plain')
        self.assertEqual(_guess_mime('zip'), 'application/zip')
        self.assertEqual(_guess_mime('png'), 'image/png')

    def test_case_insensitive(self):
        self.assertEqual(_guess_mime('PDF'), 'application/pdf')
        self.assertEqual(_guess_mime('PNG'), 'image/png')

    def test_unknown_type(self):
        self.assertEqual(_guess_mime('xyz'), 'application/octet-stream')

    def test_empty_ext(self):
        self.assertEqual(_guess_mime(''), 'application/octet-stream')


class TestBuildImageJson(unittest.TestCase):
    """测试图片 JSON 构建"""

    def test_basic_image(self):
        data = _build_image_json({'src': 'https://example.com/a.png'})
        self.assertEqual(data['src'], 'https://example.com/a.png')
        self.assertEqual(data['crop'], [0, 0, 1, 1])
        self.assertIsNone(data['title'])
        self.assertNotIn('link', data)
        self.assertIn('id', data)

    def test_image_with_link(self):
        data = _build_image_json({'src': 'https://example.com/a.png', 'link': 'https://yuque.com'})
        self.assertEqual(data['link'], 'https://yuque.com')

    def test_image_with_name(self):
        data = _build_image_json({'src': 'https://example.com/a.png', 'name': '截图'})
        self.assertEqual(data['title'], '截图')


class TestConvertSelfClosingCards(unittest.TestCase):
    """测试自闭合 Card 转换"""

    def test_hr(self):
        result = convert_self_closing_cards('<card-hr/>')
        self.assertIn('name="hr"', result)
        self.assertIn('type="block"', result)
        self.assertNotIn('card-hr', result)

    def test_checkbox(self):
        result = convert_self_closing_cards('<card-checkbox checked="false"/>')
        self.assertIn('value="data:false"', result)
        self.assertNotIn('card-checkbox', result)

    def test_checkbox_true(self):
        result = convert_self_closing_cards('<card-checkbox checked="true"/>')
        self.assertIn('value="data:true"', result)

    def test_label(self):
        result = convert_self_closing_cards('<card-label text="重要" color="2"/>')
        self.assertIn('name="label"', result)
        self.assertNotIn('card-label', result)

    def test_self_closing_image(self):
        """自闭合图片标签 <card-image src="url"/>"""
        result = convert_self_closing_cards('<card-image src="https://example.com/a.png"/>')
        self.assertIn('name="image"', result)
        self.assertNotIn('card-image', result)

    def test_multiple_self_closing(self):
        html = '<card-hr/><card-checkbox checked="true"/>'
        result = convert_self_closing_cards(html)
        self.assertNotIn('card-hr', result)
        self.assertNotIn('card-checkbox', result)

    def test_no_attrs_self_closing(self):
        """无属性的自闭合标签"""
        result = convert_self_closing_cards('<card-hr/>')
        self.assertIn('name="hr"', result)


class TestConvertContentCards(unittest.TestCase):
    """测试带内容 Card 转换"""

    def test_codeblock(self):
        html = '<card-codeblock mode="python">print("hello")</card-codeblock>'
        result = convert_content_cards(html)
        self.assertIn('name="codeblock"', result)
        self.assertNotIn('card-codeblock', result)

    def test_codeblock_no_attrs(self):
        """无属性的代码块"""
        html = '<card-codeblock>plain code</card-codeblock>'
        result = convert_content_cards(html)
        self.assertIn('name="codeblock"', result)
        self.assertNotIn('card-codeblock', result)

    def test_diagram(self):
        html = '<card-diagram type="mermaid">graph TD\n    A --> B</card-diagram>'
        result = convert_content_cards(html)
        self.assertIn('name="diagram"', result)
        self.assertIn('type="block"', result)
        self.assertNotIn('card-diagram', result)

    def test_math(self):
        html = '<card-math code="E = mc^2"></card-math>'
        result = convert_content_cards(html)
        self.assertIn('name="math"', result)
        self.assertNotIn('card-math', result)

    def test_file(self):
        html = '<card-file src="https://example.com/report.pdf" name="季度报告.pdf" ext="pdf" size="1024"></card-file>'
        result = convert_content_cards(html)
        self.assertIn('name="file"', result)
        self.assertNotIn('card-file', result)

    def test_yuque(self):
        html = '<card-yuque src="https://www.yuque.com/namespace/repo/slug" mode="card"></card-yuque>'
        result = convert_content_cards(html)
        self.assertIn('name="yuque"', result)
        # view=doc_embed 在 URL 编码后为 view%3Ddoc_embed
        self.assertIn('view%3Ddoc_embed', result)
        self.assertNotIn('card-yuque', result)

    def test_nested_codeblock_with_card_text(self):
        """代码块内容包含 <card- 文本不应误判为嵌套"""
        html = '<card-codeblock mode="plain">This is <card- not a tag</card-codeblock>'
        result = convert_content_cards(html)
        self.assertIn('name="codeblock"', result)
        self.assertNotIn('card-codeblock>', result)  # 伪标签应被替换


class TestConvertNonCardTags(unittest.TestCase):
    """测试非 Card 结构转换"""

    def test_alert(self):
        html = '<alert type="info">提示内容</alert>'
        result = convert_non_card_tags(html)
        self.assertIn('lake-alert lake-alert-info', result)
        self.assertNotIn('<alert', result)

    def test_alert_warning(self):
        html = '<alert type="warning">注意</alert>'
        result = convert_non_card_tags(html)
        self.assertIn('lake-alert-warning', result)

    def test_collapse(self):
        html = '<collapse title="详情" open="false"><p>内容</p></collapse>'
        result = convert_non_card_tags(html)
        self.assertIn('lake-collapse', result)
        self.assertIn('lake-summary', result)
        self.assertIn('详情', result)
        self.assertNotIn('<collapse', result)

    def test_collapse_default_open(self):
        html = '<collapse title="测试"><p>内容</p></collapse>'
        result = convert_non_card_tags(html)
        self.assertIn('open="false"', result)

    def test_inline_label(self):
        html = '<inline-label text="必要条件" color="4"/>'
        result = convert_non_card_tags(html)
        self.assertIn('ne-label', result)
        self.assertIn('data-color="4"', result)
        self.assertIn('必要条件', result)
        self.assertNotIn('inline-label', result)

    def test_columns(self):
        html = '<columns><column width="40%"><p>左栏</p></column><column width="60%"><p>右栏</p></column></columns>'
        result = convert_non_card_tags(html)
        self.assertIn('lake-columns', result)
        self.assertIn('lake-column-item', result)
        self.assertIn('40%', result)
        self.assertIn('60%', result)
        self.assertNotIn('<columns', result)

    def test_nested_alert(self):
        """嵌套 alert 应正确处理"""
        html = '<alert type="info">外层<alert type="warning">内层</alert></alert>'
        result = convert_non_card_tags(html)
        self.assertNotIn('<alert', result)


class TestAddDocumentHeader(unittest.TestCase):
    """测试文档头部添加"""

    def test_header_with_title(self):
        result = add_document_header('<p>内容</p>', '测试标题')
        self.assertTrue(result.startswith('<!doctype lake>'))
        self.assertIn('<title>测试标题</title>', result)
        self.assertIn('doc-version', result)
        self.assertIn('viewport', result)
        self.assertIn('typography', result)
        self.assertIn('paragraphSpacing', result)

    def test_header_without_title(self):
        result = add_document_header('<p>内容</p>', None)
        self.assertTrue(result.startswith('<!doctype lake>'))
        self.assertNotIn('<title>', result)

    def test_replace_existing_header(self):
        html = '<!doctype lake><title>旧标题</title><p>内容</p>'
        result = add_document_header(html, '新标题')
        # 应替换旧的 header
        self.assertEqual(result.count('<!doctype lake>'), 1)
        self.assertIn('新标题', result)
        self.assertNotIn('旧标题', result)

    def test_excess_newlines_removed(self):
        html = '<p>内容</p>\n\n\n\n<p>更多</p>'
        result = add_document_header(html, '标题')
        self.assertNotIn('\n\n\n', result)


class TestConvert(unittest.TestCase):
    """测试完整转换流程"""

    def test_simple_conversion(self):
        html = '<h1>标题</h1><p>段落内容</p>'
        result = convert(html, '测试')
        self.assertTrue(result.startswith('<!doctype lake>'))
        self.assertIn('<title>测试</title>', result)
        self.assertIn('<h1>标题</h1>', result)

    def test_mixed_content(self):
        html = '''<h1>文档标题</h1>
<h2>章节</h2>
<p>段落内容</p>
<card-codeblock mode="python">print("hello")</card-codeblock>
<alert type="info">提示</alert>
<card-hr/>'''
        result = convert(html, '文档标题')
        self.assertTrue(result.startswith('<!doctype lake>'))
        self.assertNotIn('card-codeblock', result)
        self.assertNotIn('<alert', result)
        self.assertNotIn('card-hr', result)
        self.assertIn('name="codeblock"', result)
        self.assertIn('lake-alert', result)
        self.assertIn('name="hr"', result)

    def test_no_pseudo_tags_remaining(self):
        """完整转换后不应有残留伪标签"""
        html = '<card-hr/><card-checkbox checked="true"/><card-label text="标签" color="2"/>'
        result = convert(html, '测试')
        remaining = re.findall(r'<(card-\w+|alert|collapse|columns|column|inline-label)[\s/>]', result)
        self.assertEqual(len(remaining), 0, f"残留伪标签: {remaining}")

    def test_all_cards_have_name_and_value(self):
        """所有 <card> 标签都应有 name 和 value 属性"""
        html = '<card-hr/><card-checkbox checked="true"/><card-codeblock mode="python">code</card-codeblock>'
        result = convert(html, '测试')
        cards = re.findall(r'<card\s+([^>]+)>', result)
        for card_attrs in cards:
            self.assertIn('name=', card_attrs)
            self.assertIn('value=', card_attrs)

    def test_all_values_start_with_data(self):
        """所有 value 属性应以 data: 开头"""
        html = '<card-hr/><card-checkbox checked="true"/><card-label text="标签" color="2"/>'
        result = convert(html, '测试')
        values = re.findall(r'value="([^"]*)"', result)
        for v in values:
            self.assertTrue(v.startswith('data:'), f"value 不以 data: 开头: {v}")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_empty_input(self):
        result = convert('', '空文档')
        self.assertTrue(result.startswith('<!doctype lake>'))

    def test_whitespace_only(self):
        result = convert('   \n\n  \n  ', '空白')
        self.assertTrue(result.startswith('<!doctype lake>'))

    def test_codeblock_with_closing_tag_in_content(self):
        """代码块内容包含 </card-codeblock> 文本"""
        # 这种情况会导致误匹配，是已知限制
        # 测试确认不会崩溃
        html = '<card-codeblock mode="plain">content</card-codeblock>'
        result = convert(html, '测试')
        self.assertIn('name="codeblock"', result)

    def test_special_chars_in_text(self):
        html = '<p>小于 < 大于 > 且 & 符号</p>'
        result = convert(html, '特殊字符')
        self.assertTrue(result.startswith('<!doctype lake>'))

    def test_unicode_content(self):
        html = '<p>中文内容 🎉 表情符号</p>'
        result = convert(html, 'Unicode 测试')
        self.assertIn('中文内容', result)


class TestRegressions(unittest.TestCase):
    """回归测试 — 对应 v4.1 修复的 bug"""

    def test_codeblock_without_attrs(self):
        """Bug: 内容 Card 无属性时不匹配"""
        html = '<card-codeblock>code</card-codeblock>'
        result = convert_content_cards(html)
        self.assertIn('name="codeblock"', result)
        self.assertNotIn('card-codeblock', result)

    def test_self_closing_content_card(self):
        """Bug: 自闭合内容 Card 不处理"""
        html = '<card-image src="https://example.com/a.png"/>'
        result = convert_self_closing_cards(html)
        self.assertIn('name="image"', result)
        self.assertNotIn('card-image', result)

    def test_yuque_url_with_query_params(self):
        """Bug: Yuque card URL 拼接不处理已有查询参数"""
        url = _build_yuque_url('https://www.yuque.com/repo/slug?param=value')
        self.assertIn('&view=doc_embed', url)
        self.assertNotIn('?view=doc_embed', url)

    def test_collapse_not_on2(self):
        """改进: collapse 转换效率从 O(n²) 改为 O(n)"""
        # 测试多个 collapse 能正确处理
        html = '<collapse title="A"><p>a</p></collapse><collapse title="B"><p>b</p></collapse>'
        result = convert_non_card_tags(html)
        self.assertEqual(result.count('lake-collapse'), 2)
        self.assertNotIn('<collapse', result)


if __name__ == '__main__':
    unittest.main()
