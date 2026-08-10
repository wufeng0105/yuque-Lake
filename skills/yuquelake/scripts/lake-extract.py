#!/usr/bin/env python3
"""
Lake 输入内容提取器 v1.0

解析 .lake 文件中的 <card> 标签和 Lake 特殊结构，提取内容并输出为位置标记纯文本。
自动化 SKILL.md §1a-Lake 中描述的机械工作（URL 解码 + JSON 解析 + 字段提取）。

AI 负责决定如何使用提取后的内容（Step 2 梳理），本脚本只负责准确提取。

支持的 Card 类型：
- image: 提取 src, title
- codeblock: 提取 mode, code
- math: 提取 code
- diagram: 提取 type, code
- file: 提取 src, name, ext
- hr: 标记分割线
- checkbox: 提取 checked 状态
- label: 提取 text, colorIndex
- dateCard: 提取 timestamp
- calendar: 提取 currentDate
- yuque: 提取 src
- datatable: 提取 sheetId, docId（占位符）
- board: 占位符

支持的 Lake 特殊结构：
- <blockquote class="lake-alert-*">: 提取类型和内容
- <details class="lake-collapse">: 提取标题和内容
- <article class="lake-columns">: 提取各列内容
- <table class="lake-table">: 提取所有行数据

用法：
    python lake-extract.py input.lake
    python lake-extract.py input.lake output.txt
"""

import sys
import re
import json
import argparse
from urllib.parse import unquote


def decode_card_value(value_str):
    """解码 card 的 value 属性（data:URL编码JSON）"""
    if not value_str or not value_str.startswith('data:'):
        return {}
    try:
        json_str = unquote(value_str[5:])  # 去掉 data: 前缀后解码
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return {}


def extract_card_content(card_match):
    """从 <card> 标签匹配中提取内容，返回位置标记字符串"""
    full_match = card_match.group(0)
    name_match = re.search(r'name="([^"]*)"', full_match)
    value_match = re.search(r'value="([^"]*)"', full_match)

    if not name_match:
        return full_match  # 无法解析，原样返回

    card_name = name_match.group(1)
    value_str = value_match.group(1) if value_match else ''
    data = decode_card_value(value_str)

    if card_name == 'image':
        src = data.get('src', '')
        title = data.get('title', '') or ''
        return f'[IMAGE: {src} | {title}]'

    elif card_name == 'codeblock':
        mode = data.get('mode', 'plain')
        code = data.get('code', '')
        return f'[CODE: {mode}]\n{code}\n[END CODE]'

    elif card_name == 'math':
        code = data.get('code', '')
        return f'[MATH: {code}]'

    elif card_name == 'diagram':
        dtype = data.get('type', 'mermaid')
        code = data.get('code', '')
        return f'[DIAGRAM: {dtype}]\n{code}\n[END DIAGRAM]'

    elif card_name == 'file':
        src = data.get('src', '')
        name = data.get('name', '')
        ext = data.get('ext', '')
        return f'[FILE: {src} | {name} | {ext}]'

    elif card_name == 'hr':
        return '[HR]'

    elif card_name == 'checkbox':
        value = value_str.replace('data:', '')
        return f'[CHECKBOX: {value}]'

    elif card_name == 'label':
        text = data.get('label', '')
        color = data.get('colorIndex', 0)
        return f'[LABEL: {text} | {color}]'

    elif card_name == 'dateCard':
        timestamp = data.get('date', 0)
        return f'[DATE: {timestamp}]'

    elif card_name == 'calendar':
        date = data.get('currentDate', 0)
        return f'[CALENDAR: {date}]'

    elif card_name == 'yuque':
        src = data.get('src', '')
        return f'[LINK: {src} | 语雀文档嵌入]'

    elif card_name == 'dataTable':
        sheet_id = data.get('sheetId', '')
        doc_id = data.get('docId', 0)
        return f'[TABLE] 数据表(sheetId={sheet_id}, docId={doc_id}) [END TABLE]'

    elif card_name == 'board':
        return '[DIAGRAM: board]\n画板占位\n[END DIAGRAM]'

    else:
        return f'[CARD: {card_name}]'


def extract_alerts(content):
    """提取 <blockquote class="lake-alert-*"> 提示框"""
    pattern = r'<blockquote\s+class="lake-alert\s+lake-alert-(\w+)"[^>]*>(.*?)</blockquote>'
    def repl(m):
        alert_type = m.group(1)
        inner = m.group(2)
        # 剥离内部 HTML 标签，保留文本
        text = re.sub(r'<[^>]+>', '', inner).strip()
        return f'[ALERT: {alert_type}]\n{text}\n[END ALERT]'
    return re.sub(pattern, repl, content, flags=re.DOTALL)


def extract_collapse(content):
    """提取 <details class="lake-collapse"> 折叠面板"""
    pattern = r'<details\s+class="lake-collapse"[^>]*open="([^"]*)"[^>]*>\s*<summary\s+class="lake-summary"[^>]*>(.*?)</summary>(.*?)</details>'
    def repl(m):
        is_open = m.group(1)
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        inner = m.group(3)
        # 递归处理内部可能有的 card 标签
        inner = extract_cards(inner)
        # 剥离剩余 HTML 标签但保留位置标记
        inner = re.sub(r'<[^>]+>', '', inner).strip()
        return f'[COLLAPSE: {title} | open={is_open}]\n{inner}\n[END COLLAPSE]'
    return re.sub(pattern, repl, content, flags=re.DOTALL)


def extract_columns(content):
    """提取 <article class="lake-columns"> 多栏布局"""
    pattern = r'<article\s+class="lake-columns"[^>]*>(.*?)</article>'
    def repl(m):
        inner = m.group(1)
        col_pattern = r'<article\s+class="lake-column-item"[^>]*style="width:\s*([^"]*)"[^>]*>(.*?)</article>'
        cols = re.findall(col_pattern, inner, flags=re.DOTALL)
        if not cols:
            return m.group(0)
        parts = []
        for width, col_content in cols:
            col_content = extract_cards(col_content)
            col_content = re.sub(r'<[^>]+>', '', col_content).strip()
            parts.append(f'[COLUMN: {width}]\n{col_content}')
        return '[COLUMNS]\n' + '\n[COL]\n'.join(parts) + '\n[END COLUMNS]'
    return re.sub(pattern, repl, content, flags=re.DOTALL)


def extract_tables(content):
    """提取 <table class="lake-table"> 表格数据"""
    pattern = r'<table[^>]*class="[^"]*lake-table[^"]*"[^>]*>(.*?)</table>'
    def repl(m):
        inner = m.group(1)
        row_pattern = r'<tr[^>]*>(.*?)</tr>'
        rows = []
        for row_match in re.finditer(row_pattern, inner, flags=re.DOTALL):
            row_content = row_match.group(1)
            cell_pattern = r'<t[dh][^>]*>(.*?)</t[dh]>'
            cells = []
            for cell_match in re.finditer(cell_pattern, row_content, flags=re.DOTALL):
                cell_text = re.sub(r'<[^>]+>', '', cell_match.group(1)).strip()
                cells.append(cell_text)
            if cells:
                rows.append(' | '.join(cells))
        return '[TABLE]\n' + '\n'.join(rows) + '\n[END TABLE]'
    return re.sub(pattern, repl, content, flags=re.DOTALL)


def extract_cards(content):
    """提取所有 <card> 标签内容"""
    # <card type="..." name="..." value="..."></card>
    pattern = r'<card\s+[^>]*name="[^"]*"[^>]*></card>'
    return re.sub(pattern, lambda m: extract_card_content(m), content, flags=re.IGNORECASE)


def extract_links(content):
    """提取 <a href="..."> 链接"""
    pattern = r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    def repl(m):
        url = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        return f'[LINK: {url} | {text}]'
    return re.sub(pattern, repl, content, flags=re.DOTALL | re.IGNORECASE)


def extract_text_urls(content):
    """扫描正文中以 http:// 或 https:// 开头的纯文本 URL，标记为 [LINK: url | ]"""
    # 保护已有的位置标记，不在标记内扫描 URL
    # 按 [MARKER: ...] 分割内容，只在非标记部分扫描
    marker_pattern = r'(\[[A-Z_]+:[^\]]*\])'
    parts = re.split(marker_pattern, content)
    result = []
    for part in parts:
        if re.match(r'\[[A-Z_]+:', part):
            result.append(part)  # 标记内不处理
        else:
            url_pattern = r'(https?://[^\s<>"\'\]\)]+)'
            part = re.sub(url_pattern, lambda m: f'[LINK: {m.group(1)} | ]', part)
            result.append(part)
    return ''.join(result)


def strip_html_tags(content):
    """剥离剩余 HTML 标签，保留文本和位置标记"""
    # 保留 [IMAGE:...], [CODE:...] 等位置标记（方括号内的内容）
    # 剥离 <p>, <h1>-<h6>, <span>, <strong>, <em>, <div> 等
    # 但保留标题文本和段落换行
    content = re.sub(r'<h([1-6])[^>]*>', r'\n[H\1] ', content)
    content = re.sub(r'</h[1-6]>', '\n', content)
    content = re.sub(r'<p[^>]*>', '\n', content)
    content = re.sub(r'</p>', '\n', content)
    content = re.sub(r'<li[^>]*>', '\n- ', content)
    content = re.sub(r'</li>', '', content)
    content = re.sub(r'<br\s*/?>', '\n', content)
    # 剥离所有其他 HTML 标签
    content = re.sub(r'<[^>]+>', '', content)
    # 清理 HTML 实体
    content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    # 扫描纯文本 URL 并标记为 [LINK: ...]
    content = extract_text_urls(content)
    # 收敛空白
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def extract(content):
    """完整提取流程"""
    # 1. 提取折叠面板（可能包含 card，先处理）
    content = extract_collapse(content)
    # 2. 提取多栏布局
    content = extract_columns(content)
    # 3. 提取提示框
    content = extract_alerts(content)
    # 4. 提取表格
    content = extract_tables(content)
    # 5. 提取 card 标签
    content = extract_cards(content)
    # 6. 提取链接
    content = extract_links(content)
    # 7. 剥离剩余 HTML 标签
    content = strip_html_tags(content)
    return content


def main():
    parser = argparse.ArgumentParser(
        description='Lake 输入内容提取器：解析 .lake 文件，提取内容为位置标记纯文本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    python lake-extract.py input.lake
    python lake-extract.py input.lake output.txt

输出格式：
    [IMAGE: url | title]      图片
    [CODE: lang] code [END]   代码块
    [MATH: formula]           数学公式
    [DIAGRAM: type] code [END] 流程图
    [FILE: url | name | ext]  附件
    [LINK: url | text]        链接
    [TABLE] rows [END]        表格
    [ALERT: type] text [END]  提示框
    [COLLAPSE: title] text [END] 折叠面板
        """
    )
    parser.add_argument('input', help='输入 .lake 文件路径')
    parser.add_argument('output', nargs='?', help='输出 .txt 文件路径（不指定则输出到 stdout）')

    args = parser.parse_args()

    try:
        if args.input == '-':
            content = sys.stdin.read()
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
    except FileNotFoundError:
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"错误: 无权限读取文件: {args.input}", file=sys.stderr)
        sys.exit(1)

    result = extract(content)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"提取完成: {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"错误: 无权限写入文件: {args.output}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)


if __name__ == '__main__':
    main()
