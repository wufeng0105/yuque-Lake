#!/usr/bin/env python3
"""
Lake 伪标签转换器 v4.2

基于真实 .lake 样本验证的语法映射，支持：
- 13 种 Card 伪标签（codeblock, image, math, hr, diagram, checkbox, label, file, date, calendar, datatable, board, yuque）
- 4 种非 Card 伪标签（alert, collapse, columns, inline-label）
- 文档头部自动生成（<!doctype lake> + <title> + 4 个 <meta>）
- ID 自动生成（5字符随机）
- tag-mapping.json 加载与同步验证（Card 元数据的唯一真实来源）

v4.2 改进：
- 新增: 加载 tag-mapping.json，启动时验证 Python Card 定义与 JSON 配置同步
- 修复: alert/collapse 嵌套处理用负向先行断言匹配最内层，替代 finditer+skip 方案

v4.1 修复：
- Bug: 内容 Card 无属性时不匹配（<card-codeblock>code</card-codeblock>）
- Bug: 自闭合内容 Card 不处理（<card-image src="url"/>）
- Bug: Yuque card URL 拼接不处理已有查询参数
- 改进: collapse 转换从 O(n²) 改为 O(n)（用 finditer + reversed）
- 改进: 内容 Card 嵌套检查不再误判文本中的 <card- 字符串

用法：
    python lake-converter.py input.html output.lake --title "文档标题"
    python lake-converter.py input.html --title "文档标题"
    python lake-converter.py input.html
"""

import sys
import os
import re
import json
import random
import string
import argparse
from urllib.parse import quote


# ========== 配置加载 ==========

def _load_tag_mapping():
    """加载 tag-mapping.json — Card 伪标签映射的唯一真实来源

    JSON 定义 Card 的元数据（cardName, cardType, selfClosing, attributes），
    Python 负责 JSON 模板无法覆盖的复杂转换逻辑（URL 构建、MIME 推断等）。
    _validate_card_sync() 确保两者保持同步。
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reference', 'tag-mapping.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 未找到 tag-mapping.json ({json_path})，跳过配置同步检查", file=sys.stderr)
        return {}

TAG_MAPPING = _load_tag_mapping()


def gen_id():
    """生成5字符随机ID（大小写字母+数字）"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=5))


# ========== Card 定义（基于真实 .lake 样本） ==========

# 自闭合 Card（无内容，type=block 的用 block，其余 inline）
SELF_CLOSING_CARDS = {
    'hr': {
        'card_type': 'block',
        'card_name': 'hr',
        'json': lambda attrs: {'id': gen_id()},
    },
    'checkbox': {
        'card_type': 'inline',
        'card_name': 'checkbox',
        'json': None,  # checkbox 直接用 value=data:true/false
        'value': lambda attrs: f"data:{'true' if attrs.get('checked', 'false').lower() == 'true' else 'false'}",
    },
    'label': {
        'card_type': 'inline',
        'card_name': 'label',
        'json': lambda attrs: {
            'label': attrs.get('text', ''),
            'colorIndex': int(attrs.get('color', '0')),
            'id': gen_id(),
        },
    },
    'calendar': {
        'card_type': 'block',
        'card_name': 'calendar',
        'json': lambda attrs: {
            'currentDate': int(attrs.get('date', '20260101')),
            'colorIndex': int(attrs.get('color', '0')),
            'schedules': {},
            'id': gen_id(),
        },
    },
    'datatable': {
        'card_type': 'block',
        'card_name': 'dataTable',
        'json': lambda attrs: {
            'sheetId': attrs.get('sheetId', ''),
            'docId': int(attrs.get('docId', '0')),
            'docType': 'Doc',
            'widthMode': 'contain',
            'tableId': int(attrs.get('tableId', '0')),
            'id': gen_id(),
        },
    },
    'board': {
        'card_type': 'block',
        'card_name': 'board',
        'json': lambda attrs: {
            'id': gen_id(),
        },
    },
}

# 带内容的 Card
CONTENT_CARDS = {
    'codeblock': {
        'card_type': 'inline',
        'card_name': 'codeblock',
        'json': lambda attrs, content: {
            'search': '',
            'hideToolbar': True,
            'mode': attrs.get('mode', 'plain'),
            'code': content,
            'heightLimit': True,
            'id': gen_id(),
        },
    },
    'image': {
        'card_type': 'inline',
        'card_name': 'image',
        'json': lambda attrs, content: _build_image_json(attrs),
    },
    'math': {
        'card_type': 'inline',
        'card_name': 'math',
        'json': lambda attrs, content: {
            'code': attrs.get('code', content),
            'id': gen_id(),
        },
    },
    'diagram': {
        'card_type': 'block',
        'card_name': 'diagram',
        'json': lambda attrs, content: {
            'type': attrs.get('type', 'mermaid'),
            'code': content,
            'id': gen_id(),
        },
    },
    'file': {
        'card_type': 'inline',
        'card_name': 'file',
        'json': lambda attrs, content: {
            'src': attrs.get('src', ''),
            'name': attrs.get('name', ''),
            'size': int(attrs.get('size', '0')),
            'ext': attrs.get('ext', ''),
            'source': '',
            'status': 'done',
            'download': True,
            'type': _guess_mime(attrs.get('ext', '')),
            'id': gen_id(),
        },
    },
    'date': {
        'card_type': 'inline',
        'card_name': 'dateCard',
        'json': lambda attrs, content: {
            'date': int(attrs.get('timestamp', '0')),
            'id': gen_id(),
        },
    },
    'yuque': {
        'card_type': 'block',
        'card_name': 'yuque',
        'json': lambda attrs, content: {
            'mode': attrs.get('mode', 'card'),
            'heightMode': 'default',
            'src': attrs.get('src', ''),
            'url': _build_yuque_url(attrs.get('src', '')),
            'detail': {
                'image': None,
                'title': attrs.get('title', ''),
                'type': 'doc',
                'desc': '',
            },
            'id': gen_id(),
        },
    },
}


def _build_image_json(attrs):
    """构建图片 card JSON"""
    data = {
        'src': attrs.get('src', ''),
        'linkTarget': '',
        'title': attrs.get('name') if attrs.get('name') else None,
        'crop': [0, 0, 1, 1],
        'id': gen_id(),
    }
    if attrs.get('link'):
        data['link'] = attrs['link']
    return data


def _build_yuque_url(src):
    """构建语雀嵌入 URL，处理已有查询参数"""
    if not src:
        return ''
    if '?' in src:
        return f"{src}&view=doc_embed"
    return f"{src}?view=doc_embed"


def _guess_mime(ext):
    """根据扩展名猜 MIME 类型"""
    mimes = {
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'zip': 'application/zip',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'mp4': 'video/mp4',
        'mp3': 'audio/mpeg',
    }
    return mimes.get(ext.lower(), 'application/octet-stream')


# ========== 非 Card 结构（HTML + CSS class） ==========

NON_CARD_TAGS = {
    'alert': {
        'real_tag': 'blockquote',
        'class_template': 'lake-alert lake-alert-{type}',
        'transform': lambda attrs, content: _build_alert(attrs, content),
    },
    'collapse': {
        'real_tag': 'details',
        'transform': lambda attrs, content: _build_collapse(attrs, content),
    },
    'inline-label': {
        'real_tag': 'span',
        'self_closing': True,
        'transform': lambda attrs, content: _build_inline_label(attrs),
    },
}


def _build_alert(attrs, content):
    """构建提示框"""
    alert_type = attrs.get('type', 'info')
    return f'<blockquote class="lake-alert lake-alert-{alert_type}">{content}</blockquote>'


def _build_collapse(attrs, content):
    """构建折叠面板"""
    title = attrs.get('title', '')
    open_val = 'true' if attrs.get('open', 'false').lower() == 'true' else 'false'
    return f'<details class="lake-collapse" open="{open_val}"><summary class="lake-summary">{title}</summary>{content}</details>'


def _build_inline_label(attrs):
    """构建行内标签"""
    text = attrs.get('text', '')
    color = attrs.get('color', '0')
    return f'<span data-color="{color}" class="ne-label">{text}</span>'


# ========== 配置同步验证 ==========

def _validate_card_sync():
    """验证 Python Card 定义与 tag-mapping.json 保持同步

    检查方向：
    1. JSON 中每个 card 在 Python 中有对应实现
    2. cardName 和 cardType 一致
    3. Python 中每个 card 在 JSON 中有对应定义
    """
    if not TAG_MAPPING:
        return
    json_cards = TAG_MAPPING.get('cards', {})
    json_pseudo_tags = {c.get('pseudoTag', '') for c in json_cards.values()}

    # JSON → Python
    for key, card_def in json_cards.items():
        pseudo_tag = card_def.get('pseudoTag', '')
        short_name = pseudo_tag.replace('card-', '') if pseudo_tag else key
        is_self_closing = card_def.get('selfClosing', False)
        json_name = card_def.get('cardName', '')
        json_type = card_def.get('cardType', '')

        if is_self_closing:
            py_def = SELF_CLOSING_CARDS.get(short_name)
        else:
            py_def = CONTENT_CARDS.get(short_name)

        if py_def is None:
            print(f"警告: tag-mapping.json 定义了 {pseudo_tag}，但脚本未实现", file=sys.stderr)
        else:
            if py_def['card_name'] != json_name:
                print(f"警告: {pseudo_tag} cardName 不一致 (JSON: {json_name}, Python: {py_def['card_name']})", file=sys.stderr)
            if py_def['card_type'] != json_type:
                print(f"警告: {pseudo_tag} cardType 不一致 (JSON: {json_type}, Python: {py_def['card_type']})", file=sys.stderr)

    # Python → JSON
    for name in SELF_CLOSING_CARDS:
        pseudo = f"card-{name}"
        if pseudo not in json_pseudo_tags:
            print(f"警告: 脚本实现了 <{pseudo}>，但 tag-mapping.json 未定义", file=sys.stderr)

    for name in CONTENT_CARDS:
        pseudo = f"card-{name}"
        if pseudo not in json_pseudo_tags:
            print(f"警告: 脚本实现了 <{pseudo}>，但 tag-mapping.json 未定义", file=sys.stderr)


_validate_card_sync()


# ========== 属性解析 ==========

def parse_attrs(attr_str):
    """状态机解析 HTML 属性字符串"""
    attrs = {}
    i = 0
    s = attr_str.strip()
    while i < len(s):
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s):
            break
        start = i
        while i < len(s) and s[i] not in '=\t\n\r\f ':
            i += 1
        key = s[start:i]
        if not key:
            i += 1
            continue
        while i < len(s) and s[i].isspace():
            i += 1
        if i < len(s) and s[i] == '=':
            i += 1
            while i < len(s) and s[i].isspace():
                i += 1
            if i < len(s) and s[i] in '"\'':
                qc = s[i]
                i += 1
                vs = i
                while i < len(s) and s[i] != qc:
                    i += 1
                attrs[key] = s[vs:i]
                i += 1
            else:
                vs = i
                while i < len(s) and not s[i].isspace():
                    i += 1
                attrs[key] = s[vs:i]
        else:
            attrs[key] = ''
    return attrs


# ========== 编码 ==========

def encode_value(data):
    """将 JSON 编码为 Lake card value（data:URL编码JSON）"""
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return f"data:{quote(json_str, safe='')}"


def make_card(card_name, card_type, data):
    """生成真实 card 标签"""
    value = encode_value(data)
    return f'<card type="{card_type}" name="{card_name}" value="{value}"></card>'


def make_card_raw_value(card_name, card_type, value):
    """生成使用原始 value 的 card 标签（用于 checkbox）"""
    return f'<card type="{card_type}" name="{card_name}" value="{value}"></card>'


# ========== 转换逻辑 ==========

def convert_self_closing_cards(html):
    """转换自闭合 Card 伪标签（包括 SELF_CLOSING_CARDS 和 CONTENT_CARDS 的自闭合形式）"""
    # 1. 处理 SELF_CLOSING_CARDS
    for pseudo_name, config in SELF_CLOSING_CARDS.items():
        # 带属性的: <card-xxx attr="val" />
        pattern = rf'<card-{pseudo_name}(\s[^>]*?)\s*/>'
        def repl(m, pn=pseudo_name, cfg=config):
            attrs = parse_attrs(m.group(1) or '')
            if cfg.get('value'):
                return make_card_raw_value(cfg['card_name'], cfg['card_type'], cfg['value'](attrs))
            return make_card(cfg['card_name'], cfg['card_type'], cfg['json'](attrs))
        html = re.sub(pattern, repl, html)

        # 无属性的: <card-xxx/>
        pattern2 = rf'<card-{pseudo_name}\s*/>'
        def repl2(m, pn=pseudo_name, cfg=config):
            if cfg.get('value'):
                return make_card_raw_value(cfg['card_name'], cfg['card_type'], cfg['value']({}))
            return make_card(cfg['card_name'], cfg['card_type'], cfg['json']({}))
        html = re.sub(pattern2, repl2, html)

    # 2. 处理 CONTENT_CARDS 的自闭合形式（如 <card-image src="url"/>）
    for pseudo_name, config in CONTENT_CARDS.items():
        pattern = rf'<card-{pseudo_name}(\s[^>]*?)\s*/>'
        def repl3(m, pn=pseudo_name, cfg=config):
            attrs = parse_attrs(m.group(1) or '')
            data = cfg['json'](attrs, '')
            return make_card(cfg['card_name'], cfg['card_type'], data)
        html = re.sub(pattern, repl3, html)

    return html


def convert_content_cards(html):
    """转换带内容的 Card 伪标签（多趟扫描处理嵌套）"""
    for _ in range(20):
        changed = False
        for pseudo_name, config in CONTENT_CARDS.items():
            # 修复 Bug: 属性组改为可选，支持无属性的 <card-codeblock>code</card-codeblock>
            pattern = rf'<card-{pseudo_name}(\s+[^>]*?)?>(.*?)</card-{pseudo_name}>'
            matches = list(re.finditer(pattern, html, flags=re.DOTALL))
            for m in reversed(matches):
                content = m.group(2) or ''
                # 改进: 只跳过内部还含「未转换的」伪标签的（而非文本中的 <card- 字符串）
                # 用正则匹配真正的伪标签开头（<card- 后跟字母，再跟空格或 > 或 />）
                if re.search(r'<card-\w+(\s[^>]*?)?[/]?>', content):
                    continue
                attrs_str = m.group(1) or ''
                attrs = parse_attrs(attrs_str)
                data = config['json'](attrs, content)
                card = make_card(config['card_name'], config['card_type'], data)
                html = html[:m.start()] + card + html[m.end():]
                changed = True
        if not changed:
            break
    return html


def convert_non_card_tags(html):
    """转换非 Card 伪标签（HTML + CSS class）"""
    # 处理 inline-label（自闭合）
    pattern = r'<inline-label(\s[^>]*?)\s*/>'
    def repl_label(m):
        attrs = parse_attrs(m.group(1) or '')
        return NON_CARD_TAGS['inline-label']['transform'](attrs, '')
    html = re.sub(pattern, repl_label, html)

    # 处理 alert（带内容，用负向先行断言匹配最内层，逐层处理嵌套）
    for _ in range(20):
        # (?:(?!<alert\s)[\s\S])*? 确保内容中不含嵌套 alert 开标签
        pattern = r'<alert(\s+[^>]*?)?>((?:(?!<alert\s)[\s\S])*?)</alert>'
        match = re.search(pattern, html, flags=re.DOTALL)
        if not match:
            break
        attrs = parse_attrs(match.group(1) or '')
        content = match.group(2) or ''
        result = NON_CARD_TAGS['alert']['transform'](attrs, content)
        html = html[:match.start()] + result + html[match.end():]

    # 处理 collapse（带内容，用负向先行断言匹配最内层，逐层处理嵌套）
    for _ in range(20):
        pattern = r'<collapse(\s+[^>]*?)?>((?:(?!<collapse\s)[\s\S])*?)</collapse>'
        match = re.search(pattern, html, flags=re.DOTALL)
        if not match:
            break
        attrs = parse_attrs(match.group(1) or '')
        content = match.group(2) or ''
        result = NON_CARD_TAGS['collapse']['transform'](attrs, content)
        html = html[:match.start()] + result + html[match.end():]

    # 处理 columns（带 column 子标签）
    pattern = r'<columns>(.*?)</columns>'
    def repl_columns(m):
        inner = m.group(1) or ''
        col_pattern = r'<column(\s[^>]*?)>(.*?)</column>'
        cols = re.findall(col_pattern, inner, flags=re.DOTALL)
        col_html = ''
        for col_attrs_str, col_content in cols:
            col_attrs = parse_attrs(col_attrs_str or '')
            width = col_attrs.get('width', '50%')
            col_html += f'<article class="lake-column-item" style="width: {width}">{col_content}</article>'
        return f'<article class="lake-columns">{col_html}</article>'
    html = re.sub(pattern, repl_columns, html, flags=re.DOTALL)

    return html


def add_document_header(html, title):
    """添加文档头部"""
    header = '<!doctype lake>'
    if title:
        header += f'<title>{title}</title>'
    header += '<meta name="doc-version" content="1" />'
    header += '<meta name="viewport" content="fixed" />'
    header += '<meta name="typography" content="classic" />'
    header += '<meta name="paragraphSpacing" content="relax" />'

    stripped = html.strip()
    if stripped.lower().startswith('<!doctype lake'):
        html = re.sub(r'<!doctype lake>\s*(<title>.*?</title>)?', '', html, count=1, flags=re.IGNORECASE)

    result = header + html.strip()
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip() + '\n'


def convert(html, title=None):
    """完整转换流程

    待实现功能（tag-mapping.json standardHtmlTags 中定义但尚未实现）：
    - data-lake-id 自动生成：为每个 HTML 元素（h1-h6, p, td, li 等）添加 data-lake-id 和 id 属性
    - <span> 文本包裹：将所有文本节点用 <span data-lake-id id> 包裹
    - 列表拆分：每个 <li> 独立到各自的 <ul>/<ol>，通过 list 属性关联
    这些功能在语雀编辑器导入时会自动补全，当前版本不阻塞导入。
    """
    # 1. 转换自闭合 Card（含 CONTENT_CARDS 的自闭合形式）
    html = convert_self_closing_cards(html)
    # 2. 转换带内容 Card（多趟）
    html = convert_content_cards(html)
    # 3. 转换非 Card 结构
    html = convert_non_card_tags(html)
    # 4. 添加文档头部
    html = add_document_header(html, title)
    return html


def main():
    parser = argparse.ArgumentParser(description='Lake 伪标签转换器 v4.2')
    parser.add_argument('input', help='输入 HTML 文件路径')
    parser.add_argument('output', nargs='?', help='输出 .lake 文件路径（不指定则输出到 stdout）')
    parser.add_argument('--title', default=None, help='文档标题')

    args = parser.parse_args()

    try:
        if args.input == '-':
            html = sys.stdin.read()
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                html = f.read()
    except FileNotFoundError:
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"错误: 无权限读取文件: {args.input}", file=sys.stderr)
        sys.exit(1)

    result = convert(html, args.title)

    # 检查残留伪标签
    remaining = re.findall(r'<(card-\w+|alert|collapse|columns|column|inline-label)[\s/>]', result)
    if remaining:
        unique = set(remaining)
        print(f"警告: {len(remaining)} 个未转换伪标签: {unique}", file=sys.stderr)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"转换完成: {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"错误: 无权限写入文件: {args.output}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)


if __name__ == '__main__':
    main()
