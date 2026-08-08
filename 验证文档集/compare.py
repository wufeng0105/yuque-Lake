import re, json
from urllib.parse import unquote

# 读取样本和我的输出
sample = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOPdemo.lake', encoding='utf-8').read()
mine = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP.lake', encoding='utf-8').read()

print('=== 样本图片 card ===')
# 样本中所有图片 card
sample_imgs = re.findall(r'<card[^>]*name="image"[^>]*>', sample)
print(f'数量: {len(sample_imgs)}')
if sample_imgs:
    print(f'完整标签: {sample_imgs[0][:300]}')
    # 解码 value
    val_match = re.search(r'value="(data:[^"]+)"', sample_imgs[0])
    if val_match:
        d = json.loads(unquote(val_match.group(1)[5:]))
        print(f'JSON: {json.dumps(d, ensure_ascii=False)}')

print('\n=== 我的图片 card（从 collapse body 中解码）===')
# 我的输出：图片在 collapse body 里
collapses = re.findall(r'<card[^>]*name="collapse"[^>]*value="([^"]+)"', mine)
print(f'collapse 数量: {len(collapses)}')

for i, val in enumerate(collapses):
    d = json.loads(unquote(val[5:]))
    body = d.get('body', '')
    imgs_in_body = re.findall(r'<card[^>]*name="image"[^>]*>', body)
    if imgs_in_body:
        print(f'\ncollapse {i+1}: {d.get("title","")[:30]}')
        print(f'  body 内图片数: {len(imgs_in_body)}')
        print(f'  图片标签: {imgs_in_body[0][:300]}')
        val_match = re.search(r'value="(data:[^"]+)"', imgs_in_body[0])
        if val_match:
            img_d = json.loads(unquote(val_match.group(1)[5:]))
            print(f'  图片JSON: {json.dumps(img_d, ensure_ascii=False)}')
        # 检查图片是否在 <p> 标签内
        p_wrap = re.findall(r'<p[^>]*><card[^>]*name="image"', body)
        print(f'  图片在 <p> 内: {len(p_wrap)} 个')
        break

print('\n=== 结构对比 ===')
print(f'样本: 有 <p> 包裹图片 = {"<p" in sample and "name=\"image\"" in sample}')
print(f'样本: 有 collapse = {"name=\"collapse\"" in sample}')
print(f'样本: 有 note = {"name=\"note\"" in sample}')
print(f'我的: 有 <p> 包裹图片 = True')
print(f'我的: 有 collapse = {"name=\"collapse\"" in mine}')
print(f'我的: 有 note = {"name=\"note\"" in mine}')
