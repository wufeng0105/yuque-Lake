#!/usr/bin/env python3
"""
Markdown → Lake 伪标签 HTML 转换器

处理 SKILL.md 四步流程中的格式转换部分：
- 步骤 1（清洗）：剥离 Markdown 格式标记，保留纯文本 + 位置信息
- 步骤 3（伪代码）：将 Markdown 结构转换为伪标签 HTML

支持的 Markdown 特性：
- 标题（h1-h6）、段落、加粗、斜体、行内代码、删除线
- 代码块（```lang ... ```）→ <card-codeblock>
- 图表（```mermaid/puml/plantuml ... ```）→ <card-diagram>
- 图片（![alt](url)）→ <card-image>
- 链接（[text](url)）→ <a>
- 表格（| ... |）→ <table>
- 无序列表、有序列表
- 任务清单（- [ ] / - [x]）→ <ul class="lake-list"> + <card-checkbox>
- 引用块（> text）→ <alert> 或 <blockquote>
- 数学公式（$$...$$ / $...$）→ <card-math>
- 水平分割线（---）→ <card-hr/>

注意：步骤 2（按文档类型重新梳理内容结构）是 AI 的职责，不是本脚本的功能。
本脚本不做内容重组，只做格式转换。

用法：
    python md-to-lake.py input.md output.html
    python md-to-lake.py input.md
"""

import sys
import re
import argparse


def escape_html(text):
    """转义 HTML 特殊字符"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


# 支持图表的代码块语言
DIAGRAM_LANGS = {'mermaid': 'mermaid', 'puml': 'puml', 'plantuml': 'puml'}


def strip_font_tags(text):
    """剥离 <font> 标签，保留内容"""
    text = re.sub(r'<font[^>]*>', '', text)
    text = re.sub(r'</font>', '', text)
    return text


def convert_inline(text):
    """转换行内格式"""
    # 先剥离 font 标签
    text = strip_font_tags(text)
    
    # 块级数学公式 $$...$$
    text = re.sub(r'\$\$(.+?)\$\$',
                  lambda m: f'<card-math code="{escape_html(m.group(1).strip())}"/>', text, flags=re.DOTALL)

    # 行内数学公式 $...$（不匹配 $$ 和已被处理的）
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)',
                  lambda m: f'<card-math code="{escape_html(m.group(1).strip())}"/>', text)

    # 图片 ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', 
                  lambda m: f'<card-image src="{m.group(2)}" name="{m.group(1)}"></card-image>', text)
    
    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: f'<a href="{m.group(2)}" target="_blank">{m.group(1)}</a>', text)
    
    # 加粗+斜体 ***text***
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
    
    # 加粗 **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # 斜体 *text* 或 _text_
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'<em>\1</em>', text)
    
    # 行内代码 `code`
    text = re.sub(r'`([^`]+)`', lambda m: f'<code>{escape_html(m.group(1))}</code>', text)
    
    # 删除线 ~~text~~
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    
    return text


def parse_table(lines):
    """解析 Markdown 表格为 HTML"""
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)
    
    if len(rows) < 2:
        return None
    
    # 第二行是分隔行（|---|---|），跳过
    if all(re.match(r'^[-:]+$', c.replace(' ', '')) for c in rows[1]):
        header = rows[0]
        body_rows = rows[2:]
    else:
        header = rows[0]
        body_rows = rows[1:]
    
    num_cols = len(header)
    col_width = max(100, 800 // num_cols)
    
    html = '<table>\n<colgroup>'
    for _ in range(num_cols):
        html += f'<col width="{col_width}">'
    html += '</colgroup>\n<tbody>\n'
    
    # 表头行
    html += '<tr>'
    for cell in header:
        html += f'<td>{convert_inline(cell)}</td>'
    html += '</tr>\n'
    
    # 数据行
    for row in body_rows:
        html += '<tr>'
        for i, cell in enumerate(row):
            if i < num_cols:
                html += f'<td>{convert_inline(cell)}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n'
    return html


def convert_markdown(md_text):
    """将 Markdown 转换为伪标签 HTML"""
    lines = md_text.split('\n')
    html_lines = []
    i = 0
    in_blockquote = False
    blockquote_lines = []
    
    while i < len(lines):
        line = lines[i]
        
        # 代码块（含图表：mermaid/puml/plantuml）
        if line.strip().startswith('```'):
            lang = line.strip().lstrip('`').strip() or 'plain'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code = '\n'.join(code_lines)
            # 图表语言 → card-diagram，普通代码 → card-codeblock
            diagram_type = DIAGRAM_LANGS.get(lang.lower())
            if diagram_type:
                html_lines.append(f'<card-diagram type="{diagram_type}">{escape_html(code)}</card-diagram>\n')
            else:
                html_lines.append(f'<card-codeblock mode="{lang}">{escape_html(code)}</card-codeblock>\n')
            continue
        
        # 水平分割线
        if re.match(r'^---+\s*$', line.strip()):
            html_lines.append('<card-hr/>\n')
            i += 1
            continue
        
        # 表格
        if line.strip().startswith('|') and i + 1 < len(lines) and lines[i + 1].strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            table_html = parse_table(table_lines)
            if table_html:
                html_lines.append(table_html)
            continue
        
        # 标题
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            title_text = convert_inline(m.group(2).strip())
            html_lines.append(f'<h{level}>{title_text}</h{level}>\n')
            i += 1
            continue
        
        # 引用块
        if line.strip().startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            quote_text = '\n'.join(quote_lines)
            quote_text = convert_inline(quote_text)
            
            # 判断是否是文档元信息（版本、状态、日期等）
            if any(kw in quote_text for kw in ['文档版本', '文档状态', '编写日期', '编写人', '文档编号', '发布版本', '发布日期', '发布类型', '发布负责人']):
                html_lines.append(f'<blockquote>{quote_text}</blockquote>\n')
            else:
                html_lines.append(f'<alert type="info">{quote_text}</alert>\n')
            continue
        
        # 任务清单（- [ ] 或 - [x]）
        if re.match(r'^\s*[-*+]\s+\[[ xX]\]\s+', line):
            list_items = []
            base_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                m = re.match(r'^(\s*)[-*+]\s+\[([ xX])\]\s+(.+)', lines[i])
                if m:
                    indent = len(m.group(1))
                    level = (indent - base_indent) // 2
                    checked = 'true' if m.group(2).lower() == 'x' else 'false'
                    text = convert_inline(m.group(3).strip())
                    list_items.append((level, checked, text))
                    i += 1
                elif lines[i].strip() == '':
                    i += 1
                    if i < len(lines) and re.match(r'^\s*[-*+]\s+\[[ xX]\]\s+', lines[i]):
                        continue
                    else:
                        break
                else:
                    break

            html_lines.append('<ul class="lake-list">\n')
            for level, checked, text in list_items:
                indent_attr = f' data-lake-indent="{level}"' if level > 0 else ''
                html_lines.append(f'<li class="lake-list-node lake-list-task"{indent_attr}><card-checkbox checked="{checked}"/>{text}</li>\n')
            html_lines.append('</ul>\n')
            continue

        # 无序列表
        if re.match(r'^\s*[-*+]\s+', line):
            list_items = []
            base_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                m = re.match(r'^(\s*)[-*+]\s+(.+)', lines[i])
                if m:
                    indent = len(m.group(1))
                    level = (indent - base_indent) // 2
                    text = convert_inline(m.group(2).strip())
                    list_items.append((level, text))
                    i += 1
                elif lines[i].strip() == '':
                    i += 1
                    # 检查下一行是否还是列表项
                    if i < len(lines) and re.match(r'^\s*[-*+]\s+', lines[i]):
                        continue
                    else:
                        break
                else:
                    break
            
            html_lines.append('<ul>\n')
            for level, text in list_items:
                if level > 0:
                    html_lines.append(f'<li data-lake-indent="{level}">{text}</li>\n')
                else:
                    html_lines.append(f'<li>{text}</li>\n')
            html_lines.append('</ul>\n')
            continue
        
        # 有序列表
        if re.match(r'^\s*\d+\.\s+', line):
            list_items = []
            base_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                m = re.match(r'^(\s*)(\d+)\.\s+(.+)', lines[i])
                if m:
                    indent = len(m.group(1))
                    level = (indent - base_indent) // 2
                    text = convert_inline(m.group(3).strip())
                    list_items.append((level, text))
                    i += 1
                elif lines[i].strip() == '':
                    i += 1
                    if i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                        continue
                    else:
                        break
                else:
                    break
            
            html_lines.append('<ol>\n')
            for level, text in list_items:
                if level > 0:
                    html_lines.append(f'<li data-lake-indent="{level}">{text}</li>\n')
                else:
                    html_lines.append(f'<li>{text}</li>\n')
            html_lines.append('</ol>\n')
            continue
        
        # 空行
        if line.strip() == '':
            i += 1
            continue
        
        # 普通段落
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != '' and not lines[i].strip().startswith(('#', '|', '```', '>', '- ', '* ', '+ ', '---')) and not re.match(r'^\s*\d+\.\s+', lines[i]):
            para_lines.append(lines[i])
            i += 1
        
        para_text = ' '.join(l.strip() for l in para_lines)
        para_text = convert_inline(para_text)
        html_lines.append(f'<p>{para_text}</p>\n')
    
    return ''.join(html_lines)


def main():
    parser = argparse.ArgumentParser(description='Markdown → Lake 伪标签 HTML 转换器')
    parser.add_argument('input', help='输入 Markdown 文件')
    parser.add_argument('output', nargs='?', help='输出 HTML 文件')
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"错误: 无权限读取文件: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    html = convert_markdown(md_text)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"转换完成: {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"错误: 无权限写入文件: {args.output}", file=sys.stderr)
            sys.exit(1)
    else:
        print(html)


if __name__ == '__main__':
    main()
