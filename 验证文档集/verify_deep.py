import re, json
from urllib.parse import unquote

content = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP.lake', encoding='utf-8').read()

print('=== 深度验证（含 collapse body 内部）===\n')

# 解码所有 collapse 的 body
collapses = re.findall(r'<card name="collapse" value="([^"]+)"', content)
notes = re.findall(r'<card name="note" value="([^"]+)"', content)

all_bodies = ''
for val in collapses:
    d = json.loads(unquote(val[5:]))
    all_bodies += d.get('body', '') + '\n'
for val in notes:
    d = json.loads(unquote(val[5:]))
    all_bodies += d.get('body', '') + '\n'

# 在 body 中搜索
images = re.findall(r'<card name="image"', all_bodies)
print(f'body 内图片 card: {len(images)} 个')

image_vals = re.findall(r'<card name="image" value="([^"]+)"', all_bodies)
for i, val in enumerate(image_vals):
    d = json.loads(unquote(val[5:]))
    print(f'  图片{i+1}: status={d.get("status")}, src={d.get("src","?")[:60]}...')

code_tags = re.findall(r'<code>([^<]+)</code>', all_bodies)
print(f'\nbody 内行内代码(话术): {len(code_tags)} 处')
for c in code_tags:
    print(f'  {c[:60]}')

links = re.findall(r'href="([^"]+)"', all_bodies)
print(f'\nbody 内链接: {len(links)} 个')
for l in links:
    print(f'  {l[:70]}')

codeblocks = re.findall(r'<card name="codeblock"', all_bodies)
print(f'\nbody 内代码块: {len(codeblocks)} 个')

labels = re.findall(r'<card name="label"', all_bodies)
print(f'body 内标签 card: {len(labels)} 个')

notes_in_body = re.findall(r'<card name="note"', all_bodies)
print(f'body 内嵌套 note card: {len(notes_in_body)} 个')

print('\n=== 深度验证完成 ===')
