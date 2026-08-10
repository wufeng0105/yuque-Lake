#!/usr/bin/env python3
"""
md-to-lake.py 单元测试

覆盖核心函数：escape_html, strip_font_tags, convert_inline,
parse_table, convert_markdown
"""

import sys
import os
import unittest
import importlib.util

# 加载带连字符的脚本文件
_scripts_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'skills', 'yuquelake', 'scripts')

_spec = importlib.util.spec_from_file_location(
    'md_to_lake',
    os.path.join(_scripts_dir, 'md-to-lake.py')
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

escape_html = _mod.escape_html
strip_font_tags = _mod.strip_font_tags
convert_inline = _mod.convert_inline
parse_table = _mod.parse_table
convert_markdown = _mod.convert_markdown


class TestEscapeHtml(unittest.TestCase):

    def test_ampersand(self):
        self.assertEqual(escape_html('a & b'), 'a &amp; b')

    def test_less_than(self):
        self.assertEqual(escape_html('a < b'), 'a &lt; b')

    def test_greater_than(self):
        self.assertEqual(escape_html('a > b'), 'a &gt; b')

    def test_combined(self):
        self.assertEqual(escape_html('<div>&</div>'), '&lt;div&gt;&amp;&lt;/div&gt;')

    def test_no_special_chars(self):
        self.assertEqual(escape_html('hello world'), 'hello world')

    def test_empty_string(self):
        self.assertEqual(escape_html(''), '')


class TestStripFontTags(unittest.TestCase):

    def test_strip_open_font(self):
        self.assertEqual(strip_font_tags('<font color="red">text'), 'text')

    def test_strip_close_font(self):
        self.assertEqual(strip_font_tags('text</font>'), 'text')

    def test_strip_both(self):
        self.assertEqual(strip_font_tags('<font size="3">text</font>'), 'text')

    def test_no_font_tags(self):
        self.assertEqual(strip_font_tags('hello world'), 'hello world')

    def test_multiple_font_tags(self):
        result = strip_font_tags('<font>a</font><font>b</font>')
        self.assertEqual(result, 'ab')


class TestConvertInline(unittest.TestCase):

    def test_image(self):
        result = convert_inline('![alt text](https://example.com/img.png)')
        self.assertIn('card-image', result)
        self.assertIn('https://example.com/img.png', result)
        self.assertIn('alt text', result)

    def test_link(self):
        result = convert_inline('[click here](https://example.com)')
        self.assertIn('<a href="https://example.com"', result)
        self.assertIn('click here', result)
        self.assertIn('target="_blank"', result)

    def test_bold(self):
        result = convert_inline('**bold text**')
        self.assertIn('<strong>bold text</strong>', result)

    def test_italic(self):
        result = convert_inline('*italic text*')
        self.assertIn('<em>italic text</em>', result)

    def test_bold_italic(self):
        result = convert_inline('***both***')
        self.assertIn('<strong><em>both</em></strong>', result)

    def test_inline_code(self):
        result = convert_inline('`variable_name`')
        self.assertIn('<code>variable_name</code>', result)

    def test_strikethrough(self):
        result = convert_inline('~~deleted~~')
        self.assertIn('<del>deleted</del>', result)

    def test_font_tag_stripped(self):
        result = convert_inline('<font color="red">colored</font> text')
        self.assertNotIn('<font', result)
        self.assertIn('colored', result)

    def test_plain_text(self):
        result = convert_inline('just plain text')
        self.assertEqual(result, 'just plain text')

    def test_mixed_formats(self):
        result = convert_inline('**bold** and *italic* and `code`')
        self.assertIn('<strong>bold</strong>', result)
        self.assertIn('<em>italic</em>', result)
        self.assertIn('<code>code</code>', result)


class TestParseTable(unittest.TestCase):

    def test_simple_table(self):
        lines = [
            '| Name | Type |',
            '|------|------|',
            '| host | string |',
            '| port | int |',
        ]
        result = parse_table(lines)
        self.assertIsNotNone(result)
        self.assertIn('<table>', result)
        self.assertIn('<colgroup>', result)
        self.assertIn('<tbody>', result)
        self.assertIn('host', result)
        self.assertIn('string', result)

    def test_single_row_table(self):
        """单行表格应返回 None 或有效 HTML"""
        lines = ['| only header |']
        result = parse_table(lines)
        self.assertIsNone(result)

    def test_table_without_separator(self):
        """无分隔行的表格"""
        lines = [
            '| a | b |',
            '| c | d |',
        ]
        result = parse_table(lines)
        self.assertIsNotNone(result)
        self.assertIn('a', result)
        self.assertIn('c', result)

    def test_colgroup_width(self):
        lines = [
            '| a | b | c |',
            '|---|---|---|',
            '| 1 | 2 | 3 |',
        ]
        result = parse_table(lines)
        self.assertIn('<colgroup>', result)
        # 3 列应该有 3 个 <col> 标签
        self.assertEqual(result.count('<col '), 3)


class TestConvertMarkdown(unittest.TestCase):

    def test_heading(self):
        result = convert_markdown('# Title\n')
        self.assertIn('<h1>Title</h1>', result)

    def test_h2(self):
        result = convert_markdown('## Section\n')
        self.assertIn('<h2>Section</h2>', result)

    def test_h6(self):
        result = convert_markdown('###### Deep\n')
        self.assertIn('<h6>Deep</h6>', result)

    def test_paragraph(self):
        result = convert_markdown('This is a paragraph.\n')
        self.assertIn('<p>This is a paragraph.</p>', result)

    def test_code_block(self):
        md = '```python\nprint("hello")\n```\n'
        result = convert_markdown(md)
        self.assertIn('card-codeblock', result)
        self.assertIn('mode="python"', result)
        self.assertIn('print("hello")', result)

    def test_code_block_no_language(self):
        md = '```\nplain code\n```\n'
        result = convert_markdown(md)
        self.assertIn('card-codeblock', result)
        self.assertIn('mode="plain"', result)

    def test_horizontal_rule(self):
        result = convert_markdown('---\n')
        self.assertIn('<card-hr/>', result)

    def test_unordered_list(self):
        md = '- item 1\n- item 2\n- item 3\n'
        result = convert_markdown(md)
        self.assertIn('<ul>', result)
        self.assertIn('<li>item 1</li>', result)
        self.assertIn('<li>item 2</li>', result)

    def test_ordered_list(self):
        md = '1. first\n2. second\n3. third\n'
        result = convert_markdown(md)
        self.assertIn('<ol>', result)
        self.assertIn('<li>first</li>', result)

    def test_blockquote(self):
        md = '> This is a quote\n'
        result = convert_markdown(md)
        # 普通引用 → alert type="info"
        self.assertIn('alert', result)

    def test_blockquote_document_meta(self):
        """文档元信息引用 → blockquote"""
        md = '> 文档版本: v1.0\n'
        result = convert_markdown(md)
        self.assertIn('<blockquote>', result)

    def test_table(self):
        md = '| a | b |\n|---|---|\n| 1 | 2 |\n'
        result = convert_markdown(md)
        self.assertIn('<table>', result)
        self.assertIn('<tbody>', result)

    def test_empty_input(self):
        result = convert_markdown('')
        self.assertEqual(result, '')

    def test_mixed_content(self):
        md = '''# Title

Some paragraph text.

## Section

- list item
- another item

```python
code = "block"
```
'''
        result = convert_markdown(md)
        self.assertIn('<h1>Title</h1>', result)
        self.assertIn('<h2>Section</h2>', result)
        self.assertIn('<ul>', result)
        self.assertIn('card-codeblock', result)

    def test_nested_list(self):
        md = '- outer\n  - inner\n'
        result = convert_markdown(md)
        self.assertIn('data-lake-indent', result)

    def test_image_in_paragraph(self):
        md = '![alt](https://example.com/img.png)\n'
        result = convert_markdown(md)
        self.assertIn('card-image', result)

    def test_crlf_input(self):
        """CRLF 换行符"""
        md = '# Title\r\n\r\nParagraph\r\n'
        result = convert_markdown(md)
        self.assertIn('<h1>Title</h1>', result)


if __name__ == '__main__':
    unittest.main()
