#!/usr/bin/env python3
"""
.lakebook 打包生成器 v1.0

将多个 .lake 文件打包为 .lakebook 归档（tar 格式），用于语雀知识库导入。

.lakebook 结构：
    archive.lakebook (tar)
    ├── $meta.json          # 知识库元数据（含 tocYml YAML）
    ├── {doc1_slug}.json     # 文档条目 1
    ├── {doc2_slug}.json     # 文档条目 2
    └── ...

用法：
    python lake-generator.py -o output.lakebook doc1.lake doc2.lake --title "知识库名"
    python lake-generator.py -o output.lakebook *.lake --title "知识库名"
    python lake-generator.py -o output.lakebook lake-output/ --title "知识库名"
"""

import sys
import os
import re
import json
import uuid
import argparse
import tarfile
import io
from datetime import datetime, timezone


def slugify(title):
    """将标题转为 URL slug"""
    # 中文保留，只处理特殊字符
    slug = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title.strip())
    slug = re.sub(r'-+', '-', slug).strip('-').lower()
    return slug or 'untitled'


def extract_title_from_lake(content):
    """从 .lake 文件内容中提取标题"""
    m = re.search(r'<title>(.*?)</title>', content)
    if m:
        return m.group(1).strip()
    # 尝试从 H1 提取
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return 'Untitled'


def make_doc_entry(lake_content, doc_id, slug, title):
    """生成文档条目 JSON"""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return {
        "doc": {
            "body": lake_content,
            "body_asl": lake_content,
            "body_draft": lake_content,
            "body_draft_asl": lake_content,
            "content_updated_at": now,
            "cover": "",
            "created_at": now,
            "description": "",
            "editor_meta": "",
            "first_published_at": now,
            "format": "lake",
            "id": doc_id,
            "public": 0,
            "published_at": now,
            "slug": slug,
            "status": 0,
            "title": title,
            "updated_at": now,
            "user_id": 0,
            "word_count": len(re.sub(r'<[^>]+>', '', lake_content))
        },
        "doc_digest": ""
    }


def make_meta(kb_title, docs):
    """生成 $meta.json"""
    # 构建 TOC YAML
    toc_lines = [
        "- type: META",
        "  title: " + kb_title,
        "  uuid: " + str(uuid.uuid4()),
        "  level: 0",
        ""
    ]

    prev_uuid = ''
    for doc in docs:
        doc_uuid = str(uuid.uuid4())
        toc_lines.extend([
            "- type: DOC",
            "  title: " + doc['title'],
            f"  uuid: {doc_uuid}",
            f"  url: {doc['slug']}",
            f"  prev_uuid: {prev_uuid}",
            "  sibling_uuid: ''",
            "  child_uuid: ''",
            "  parent_uuid: ''",
            f"  doc_id: {doc['id']}",
            "  level: 0",
            f"  id: {doc['id']}",
            "  open_window: 1",
            "  visible: 1",
            f"  slug: {doc['slug']}",
            ""
        ])
        prev_uuid = doc_uuid

    toc_yml = '\n'.join(toc_lines)

    meta_inner = {
        "book": {
            "path": "",
            "public": 0,
            "tocYml": toc_yml,
            "type": "Doc"
        },
        "config": {
            "endecryptType": 0
        },
        "docs": [],
        "version": "1"
    }

    return {
        "meta": json.dumps(meta_inner, ensure_ascii=False),
        "meta_digest": ""
    }


def generate_lakebook(lake_files, output_path, kb_title):
    """打包 .lakebook"""
    docs = []
    doc_id_base = 10000

    for idx, lake_path in enumerate(lake_files):
        try:
            with open(lake_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (FileNotFoundError, PermissionError) as e:
            print(f"警告: 跳过文件 {lake_path}: {e}", file=sys.stderr)
            continue

        title = extract_title_from_lake(content)
        slug = slugify(title)
        doc_id = doc_id_base + idx

        docs.append({
            'title': title,
            'slug': slug,
            'id': doc_id,
            'content': content
        })

    if not docs:
        print("错误: 没有有效的 .lake 文件可打包", file=sys.stderr)
        sys.exit(1)

    # 生成 $meta.json
    meta = make_meta(kb_title, docs)

    # 打包为 tar 归档
    with tarfile.open(output_path, 'w') as tar:
        # 添加 $meta.json
        meta_json = json.dumps(meta, ensure_ascii=False, indent=2)
        meta_info = tarfile.TarInfo(name='$meta.json')
        meta_info.size = len(meta_json.encode('utf-8'))
        tar.addfile(meta_info, io.BytesIO(meta_json.encode('utf-8')))

        # 添加文档条目
        for doc in docs:
            doc_entry = make_doc_entry(doc['content'], doc['id'], doc['slug'], doc['title'])
            doc_json = json.dumps(doc_entry, ensure_ascii=False)
            doc_info = tarfile.TarInfo(name=f"{doc['slug']}.json")
            doc_info.size = len(doc_json.encode('utf-8'))
            tar.addfile(doc_info, io.BytesIO(doc_json.encode('utf-8')))

    print(f"打包完成: {output_path}（{len(docs)} 个文档）", file=sys.stderr)
    for doc in docs:
        print(f"  - {doc['title']} → {doc['slug']}.json", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='.lakebook 打包生成器：将多个 .lake 文件打包为语雀知识库导入格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    python lake-generator.py -o kb.lakebook doc1.lake doc2.lake --title "我的知识库"
    python lake-generator.py -o kb.lakebook lake-output/*.lake --title "SOP知识库"
        """
    )
    parser.add_argument('inputs', nargs='+', help='输入 .lake 文件或目录')
    parser.add_argument('-o', '--output', required=True, help='输出 .lakebook 文件路径')
    parser.add_argument('--title', default='Yuque Knowledge Base', help='知识库名称')

    args = parser.parse_args()

    # 收集所有 .lake 文件
    lake_files = []
    for inp in args.inputs:
        if os.path.isdir(inp):
            for fname in sorted(os.listdir(inp)):
                if fname.endswith('.lake'):
                    lake_files.append(os.path.join(inp, fname))
        elif inp.endswith('.lake') and os.path.isfile(inp):
            lake_files.append(inp)
        else:
            print(f"警告: 跳过 {inp}（不是 .lake 文件或目录）", file=sys.stderr)

    if not lake_files:
        print("错误: 未找到 .lake 文件", file=sys.stderr)
        sys.exit(1)

    generate_lakebook(lake_files, args.output, args.title)


if __name__ == '__main__':
    main()
