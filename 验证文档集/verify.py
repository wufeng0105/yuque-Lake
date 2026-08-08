import re
from urllib.parse import unquote
import json

content = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP.lake', encoding='utf-8').read()

print('=== Lake 文件验证 ===\n')

# 1. 文档声明
print(f'1. 文档声明: {"PASS" if content.startswith("<!doctype lake>") else "FAIL"}')

# 2. 残留伪标签
pseudo = re.findall(r'<card-\w+', content)
print(f'2. 残留伪标签: {"PASS (0)" if not pseudo else f"FAIL ({len(pseudo)})"}')

# 3. Card 统计
cards = re.findall(r'<card\s+name="(\w+)"\s+value="(data:[^"]+)"', content)
bad = re.findall(r'<card(?!\s+name=)', content)
print(f'3. Card 标签: {len(cards)} 个, 缺 name/value: {len(bad)}')

types = {}
for name, val in cards:
    types[name] = types.get(name, 0) + 1
print(f'   类型分布: {types}')

# 4. value 格式
bad_val = [(n,v) for n,v in cards if not v.startswith('data:')]
print(f'4. value 格式: {"PASS" if not bad_val else "FAIL"}')

# 5. HTML 标签
html_tags = re.findall(r'<(h[1-7]|p|table|tbody|tr|td|ul|ol|li|a|strong|code|blockquote)\b', content)
tc = {}
for t in html_tags:
    tc[t] = tc.get(t, 0) + 1
print(f'5. HTML 标签: {tc}')

# 6. 图片验证（含 collapse 内嵌的）
all_images = re.findall(r'<card name="image" value="([^"]+)"', content)
print(f'6. 图片 card: {len(all_images)} 个')
for i, val in enumerate(all_images):
    d = json.loads(unquote(val[5:]))
    print(f'   图片{i+1}: status={d.get("status","?")}, src={d.get("src","?")[:60]}...')

# 7. 验证图片 URL 数量（原始 8 张）
original_urls = [
    '1770882309717',
    '1778909325863',
    '1770882325630',
    '1770882388716',
    '1778909459116',
    '1778909498739',
    '1778909521534',
    '1778909542132',
]
found = 0
for url_part in original_urls:
    if url_part in content:
        found += 1
print(f'7. 图片 URL 完整性: {found}/{len(original_urls)}')

# 8. 链接验证
links = re.findall(r'href="([^"]+)"', content)
print(f'8. 链接: {len(links)} 个')
for l in links:
    print(f'   {l[:70]}')

# 9. 话术验证（code 标签内的话术）
code_tags = re.findall(r'<code>([^<]+)</code>', content)
print(f'9. 行内代码(话术): {len(code_tags)} 处')
for c in code_tags[:3]:
    print(f'   {c[:50]}...')

print('\n=== 验证完成 ===')
