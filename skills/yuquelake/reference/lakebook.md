# .lakebook 打包结构

## 概述

`.lakebook` 是语雀知识库的导出/导入格式，本质是一个 **tar 归档文件**。

## 内部结构

```
knowledge-base.lakebook (tar archive)
├── $meta.json              # 知识库元数据（含 tocYml YAML）
├── {doc1_url}.json          # 文档条目 1
├── {doc2_url}.json          # 文档条目 2
└── ...
```

## $meta.json 结构

```json
{
  "meta": "{\"book\":{\"path\":\"...\",\"public\":0,\"tocYml\":\"...\",\"type\":\"...\"},\"config\":{\"endecryptType\":0},\"docs\":[],\"version\":\"...\"}",
  "meta_digest": "..."
}
```

### meta.book 字段

| 字段 | 说明 |
|------|------|
| `path` | 知识库路径 |
| `public` | 0=私有, 1=公开 |
| `tocYml` | YAML 格式的目录结构 |
| `type` | 类型 |

## tocYml 结构（YAML）

```yaml
- type: DOC              # DOC=文档, TITLE=仅标题, META=根节点
  title: 第一章
  uuid: abc-123
  url: chapter-1          # 对应 .json 文件名
  prev_uuid: ''
  sibling_uuid: ''
  child_uuid: ''
  parent_uuid: ''
  doc_id: 12345
  level: 0               # 0=根层级
  id: 12345
  open_window: 1
  visible: 1
  slug: chapter-1
```

### TOC 节点字段

| 字段 | 说明 |
|------|------|
| `type` | `META`=根节点, `DOC`=文档, `TITLE`=仅标题/目录 |
| `title` | 节点标题 |
| `uuid` | 节点唯一标识 |
| `url` | 文档 URL slug（对应 .json 文件名） |
| `prev_uuid` | 前一个兄弟节点 UUID |
| `sibling_uuid` | 下一个兄弟节点 UUID |
| `child_uuid` | 第一个子节点 UUID |
| `parent_uuid` | 父节点 UUID |
| `doc_id` | 文档 ID |
| `level` | 层级深度（0=根） |
| `open_window` | 是否在新窗口打开 |
| `visible` | 是否可见 |

## 文档条目 JSON 结构

```json
{
  "doc": {
    "body": "<!doctype lake>...",
    "body_asl": "<!doctype lake>...",
    "body_draft": "...",
    "body_draft_asl": "...",
    "content_updated_at": "2024-01-01T00:00:00.000Z",
    "cover": "",
    "created_at": "2024-01-01T00:00:00.000Z",
    "description": "",
    "editor_meta": "...",
    "first_published_at": "2024-01-01T00:00:00.000Z",
    "format": "lake",
    "id": 12345,
    "public": 1,
    "published_at": "2024-01-01T00:00:00.000Z",
    "slug": "chapter-1",
    "status": 0,
    "title": "第一章",
    "updated_at": "2024-01-01T00:00:00.000Z",
    "user_id": 67890,
    "word_count": 1000
  },
  "doc_digest": "..."
}
```

### 关键字段说明

| 字段 | 说明 |
|------|------|
| `body` | Lake 格式内容（HTML） |
| `body_asl` | 实际展示内容（ASL = Application Specific Language） |
| `body_draft` | 草稿内容 |
| `body_draft_asl` | 草稿 ASL |
| `format` | 文档格式：`"markdown"` 或 `"lake"` |
| `status` | 文档状态 |
| `slug` | 文档 URL slug |

> Lake 格式时 `body` 和 `body_asl` 内容相同。

## 程序化生成 lakebook

> **注意**：`lake-generator.py` 尚未实现。以下为手动打包方案。

```bash
# 手动打包：先用 lake-converter.py 逐个生成 .lake 文件，再用 tar 打包
python scripts/lake-converter.py doc1.html doc1.lake --title "文档1"
python scripts/lake-converter.py doc2.html doc2.lake --title "文档2"

# 打包为 .lakebook（本质是 tar 归档，非压缩）
tar cf 知识库.lakebook manifest.json doc1.lake doc2.lake
```

`manifest.json` 结构见上方「元数据」章节。

## 导入方式

1. 进入语雀知识库
2. 点击「设置」→「导入」
3. 选择 `.lakebook` 文件
4. 确认导入
