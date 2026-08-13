#!/usr/bin/env python3
"""
内容保全校验脚本 v1.0

比对输入文件和输出 .lake 文件中不可变元素的数量，确保转换过程中没有丢失内容。

支持的输入格式：
- .lake：解析 <card> 标签
- .md / .markdown：解析 Markdown 语法
- .html / .htm：解析 HTML 标签
- .txt：纯文本（无格式元素可检测）

支持的输出格式：
- .lake：解析 <card> 标签

校验规则：输出中每种不可变元素数量 >= 输入中对应数量。
返回 0 表示校验通过，非 0 表示有内容丢失。

用法：
    python verify-content.py input.md output.lake
    python verify-content.py input.lake output.lake
    python verify-content.py input.html output.lake --verbose
"""

import sys
import os
import re
import argparse
from urllib.parse import unquote


# ========== 输入文件解析 ==========

def _zero_counts():
    """返回全零计数字典"""
    return {
        'images': 0,
        'links': 0,
        'code_blocks': 0,
        'tables': 0,
        'math': 0,
        'diagrams': 0,
        'files': 0,
        'quotes': 0,
    }


def count_lake_cards(content):
    """统计 Lake 特有的 <card> 标签元素和纯文本 URL。

    只计数 <card> 标签（image/codeblock/math/diagram/file/dataTable/board/yuque）
    以及正文中不在 <a> 标签内的纯文本 URL。
    不计数标准 HTML 标签（<table>/<a>/<blockquote> 等），避免与
    parse_lake/parse_html 中的 HTML 标签计数重复。
    """
    counts = _zero_counts()

    # <card> 标签：name="xxx" value="data:..."
    card_pattern = re.compile(r'<card\s+[^>]*name="([^"]*)"[^>]*>', re.IGNORECASE)
    for match in card_pattern.finditer(content):
        card_name = match.group(1)
        if card_name == 'image':
            counts['images'] += 1
        elif card_name == 'codeblock':
            counts['code_blocks'] += 1
        elif card_name == 'math':
            counts['math'] += 1
        elif card_name == 'diagram':
            counts['diagrams'] += 1
        elif card_name == 'file':
            counts['files'] += 1
        elif card_name == 'dataTable':
            counts['tables'] += 1
        elif card_name == 'board':
            counts['diagrams'] += 1

    # 语雀文档嵌入 <card name="yuque"> 也算链接
    yuque_count = len(re.findall(r'<card\s+[^>]*name="yuque"[^>]*>', content, re.IGNORECASE))
    counts['links'] += yuque_count

    # 纯文本 URL：正文中以 http:// 或 https:// 开头的文本
    # 排除已在 <a href="..."> 标签内的 URL 文本（避免双重计数）
    # 策略：先移除 <a>...</a> 整体（标签+内容），再移除其他 HTML 标签，然后扫描剩余文本
    text_for_url_scan = re.sub(r'<a\s+[^>]*>.*?</a>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    text_for_url_scan = re.sub(r'<[^>]+>', ' ', text_for_url_scan)
    # 移除 HTML 实体
    text_for_url_scan = text_for_url_scan.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    # 统计纯文本 URL（长度 > 10 避免匹配短碎片）
    text_urls = re.findall(r'(https?://[^\s<>"\']{10,})', text_for_url_scan)
    counts['links'] += len(text_urls)

    return counts


def parse_lake(content):
    """解析 .lake 文件，统计不可变元素"""
    counts = _zero_counts()

    # 标准 HTML 标签计数
    counts['links'] += len(re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>', content, re.IGNORECASE))
    counts['tables'] += len(re.findall(r'<table[^>]*>', content, re.IGNORECASE))
    counts['quotes'] += len(re.findall(r'<blockquote[^>]*>', content, re.IGNORECASE))

    # Lake 特有元素（<card> 标签 + 纯文本 URL）
    card_counts = count_lake_cards(content)
    for key in counts:
        counts[key] += card_counts[key]

    return counts


def parse_markdown(content):
    """解析 Markdown 文件，统计不可变元素"""
    counts = _zero_counts()

    # 图片: ![alt](url)
    counts['images'] = len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))

    # 链接: [text](url) - 排除图片
    all_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    counts['links'] = len(all_links) - counts['images']

    # 代码块: ```lang ... ```
    counts['code_blocks'] = len(re.findall(r'```', content)) // 2

    # 行内代码 `code` 不计入代码块，但如果没有块级代码，统计行内代码
    if counts['code_blocks'] == 0:
        inline_codes = re.findall(r'`([^`]+)`', content)
        # 行内代码不算作"代码块"，不计入

    # 表格: 以 | 开头的行（连续的 | 行算一个表格）
    lines = content.split('\n')
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and '|' in stripped[1:]:
            if not in_table:
                counts['tables'] += 1
                in_table = True
        else:
            in_table = False

    # 数学公式: $$ ... $$ 或 $...$
    counts['math'] = len(re.findall(r'\$\$', content)) // 2

    # Mermaid 图: ```mermaid ... ```
    counts['diagrams'] = len(re.findall(r'```mermaid', content, re.IGNORECASE))
    # PlantUML: ```puml ... ``` 或 ```plantuml ... ```
    counts['diagrams'] += len(re.findall(r'```(?:puml|plantuml)', content, re.IGNORECASE))

    # 引用: > text
    in_quote = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('>'):
            if not in_quote:
                counts['quotes'] += 1
                in_quote = True
        else:
            in_quote = False

    # HTML 标签在 Markdown 中也常见
    # <img src="...">
    counts['images'] += len(re.findall(r'<img\s+[^>]*src="([^"]*)"[^>]*>', content, re.IGNORECASE))
    # <a href="...">
    counts['links'] += len(re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>', content, re.IGNORECASE))
    # <table>
    html_tables = len(re.findall(r'<table[^>]*>', content, re.IGNORECASE))
    counts['tables'] += html_tables

    return counts


def parse_html(content):
    """解析 HTML 文件，统计不可变元素"""
    counts = _zero_counts()

    # 标准 HTML 标签
    counts['images'] += len(re.findall(r'<img\s+[^>]*src="([^"]*)"[^>]*>', content, re.IGNORECASE))
    counts['links'] += len(re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>', content, re.IGNORECASE))
    counts['code_blocks'] += len(re.findall(r'<pre[^>]*>', content, re.IGNORECASE))
    counts['tables'] += len(re.findall(r'<table[^>]*>', content, re.IGNORECASE))
    counts['quotes'] += len(re.findall(r'<blockquote[^>]*>', content, re.IGNORECASE))

    # Lake 特有元素（<card> 标签 + 纯文本 URL，不重复计数 HTML 标签）
    card_counts = count_lake_cards(content)
    for key in counts:
        counts[key] += card_counts[key]

    return counts


def parse_text(content):
    """纯文本无法检测格式元素，返回全 0"""
    return _zero_counts()


def parse_file(filepath):
    """根据文件扩展名选择解析器"""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='gbk') as f:
            content = f.read()

    if ext in ('.lake',):
        return parse_lake(content)
    elif ext in ('.md', '.markdown'):
        return parse_markdown(content)
    elif ext in ('.html', '.htm'):
        return parse_html(content)
    elif ext in ('.txt',):
        return parse_text(content)
    else:
        # 默认尝试自动检测
        if '<card' in content and 'name=' in content:
            return parse_lake(content)
        elif '<!doctype lake>' in content:
            return parse_lake(content)
        else:
            return parse_markdown(content)


# ========== 校验逻辑 ==========

ELEMENT_NAMES = {
    'images': '图片',
    'links': '链接',
    'code_blocks': '代码块',
    'tables': '表格',
    'math': '数学公式',
    'diagrams': '流程图/图表',
    'files': '附件',
    'quotes': '引用',
}


def verify(input_counts, output_counts):
    """比对输入输出，返回 (passed, details)"""
    passed = True
    details = []

    for key, name in ELEMENT_NAMES.items():
        in_count = input_counts[key]
        out_count = output_counts[key]
        if out_count < in_count:
            passed = False
            details.append({
                'element': name,
                'input_count': in_count,
                'output_count': out_count,
                'status': 'FAIL',
                'message': f'{name}丢失：输入 {in_count} 个，输出 {out_count} 个'
            })
        else:
            details.append({
                'element': name,
                'input_count': in_count,
                'output_count': out_count,
                'status': 'PASS',
                'message': f'{name}：输入 {in_count} 个，输出 {out_count} 个'
            })

    return passed, details


# ========== 主流程 ==========

def main():
    parser = argparse.ArgumentParser(
        description='内容保全校验：比对输入输出中不可变元素数量',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    python verify-content.py input.md output.lake
    python verify-content.py input.lake output.lake --verbose

退出码：
    0 = 校验通过（输出元素数 >= 输入元素数）
    1 = 校验失败（有内容丢失）
    2 = 文件错误
        """
    )
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出 .lake 文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示所有元素的校验结果（包括通过的）')

    args = parser.parse_args()

    # 检查文件存在
    if not os.path.isfile(args.input):
        print(f'错误：输入文件不存在: {args.input}', file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(args.output):
        print(f'错误：输出文件不存在: {args.output}', file=sys.stderr)
        sys.exit(2)

    # 解析
    input_counts = parse_file(args.input)
    output_counts = parse_file(args.output)

    # 校验
    passed, details = verify(input_counts, output_counts)

    # 输出结果
    print('=' * 60)
    print('内容保全校验报告')
    print('=' * 60)
    print(f'输入文件: {args.input}')
    print(f'输出文件: {args.output}')
    print('-' * 60)

    if args.verbose:
        for d in details:
            status_icon = '✓' if d['status'] == 'PASS' else '✗'
            print(f'  {status_icon} {d["message"]}')
    else:
        failed = [d for d in details if d['status'] == 'FAIL']
        if failed:
            for d in failed:
                print(f'  ✗ {d["message"]}')
        else:
            print('  ✓ 所有不可变元素保全检查通过')

    print('-' * 60)

    if passed:
        print('结果: 通过 ✓')
        sys.exit(0)
    else:
        failed_count = sum(1 for d in details if d['status'] == 'FAIL')
        print(f'结果: 失败 ✗ ({failed_count} 项内容丢失)')
        sys.exit(1)


if __name__ == '__main__':
    main()
