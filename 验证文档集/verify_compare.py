import re, json
from urllib.parse import unquote

content = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP.lake', encoding='utf-8').read()

print('=== 对比验证 ===\n')

# 1. 文档声明
print(f'1. 文档声明: {"PASS" if content.startswith("<!doctype lake>") else "FAIL"}')

# 2. type="inline" 检查
cards_with_type = re.findall(r'<card\s+type="inline"\s+name="(\w+)"', content)
cards_without_type = re.findall(r'<card\s+name="(\w+)"(?!\s+value)', content)
print(f'2. type="inline": {len(cards_with_type)} 个有, {len(cards_without_type)} 个缺')

# 3. 解码一个图片 card 看结构
collapses = re.findall(r'<card type="inline" name="collapse" value="([^"]+)"', content)
all_bodies = ''
for val in collapses:
    d = json.loads(unquote(val[5:]))
    all_bodies += d.get('body', '') + '\n'

# 图片
images = re.findall(r'<card type="inline" name="image" value="([^"]+)"', all_bodies)
print(f'\n3. 图片 card: {len(images)} 个')
for i, val in enumerate(images[:2]):
    d = json.loads(unquote(val[5:]))
    print(f'   图片{i+1} JSON: {json.dumps(d, ensure_ascii=False)[:120]}')

# 代码块
codeblocks = re.findall(r'<card type="inline" name="codeblock" value="([^"]+)"', all_bodies)
print(f'\n4. 代码块 card: {len(codeblocks)} 个')
for i, val in enumerate(codeblocks[:1]):
    d = json.loads(unquote(val[5:]))
    print(f'   代码块{i+1} JSON keys: {list(d.keys())}')

# 对比样本格式
print('\n=== 对比样本格式 ===')
sample_image = {"src":"https://...", "linkTarget":"", "title":None, "crop":[0,0,1,1], "id":"MDrbh"}
sample_codeblock = {"search":"", "hideToolbar":True, "mode":"plain", "code":"...", "heightLimit":True, "id":"PtYi4"}
print(f'样本图片 keys: {sorted(sample_image.keys())}')
print(f'样本代码块 keys: {sorted(sample_codeblock.keys())}')

if images:
    my_img = json.loads(unquote(images[0][5:]))
    print(f'我的图片 keys: {sorted(my_img.keys())}')
    print(f'图片 key 匹配: {"PASS" if sorted(my_img.keys()) == sorted(sample_image.keys()) else "MISMATCH"}')

if codeblocks:
    my_cb = json.loads(unquote(codeblocks[0][5:]))
    print(f'我的代码块 keys: {sorted(my_cb.keys())}')
    print(f'代码块 key 匹配: {"PASS" if sorted(my_cb.keys()) == sorted(sample_codeblock.keys()) else "MISMATCH"}')

print('\n=== 验证完成 ===')
