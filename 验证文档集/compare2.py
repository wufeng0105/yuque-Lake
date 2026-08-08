import re, json
from urllib.parse import unquote

sample = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOPdemo.lake', encoding='utf-8').read()
mine = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP-flat.lake', encoding='utf-8').read()

# 样本图片
s_imgs = re.findall(r'<card[^>]*name="image"[^>]*>', sample)
m_imgs = re.findall(r'<card[^>]*name="image"[^>]*>', mine)

print(f'样本图片: {len(s_imgs)}, 我的图片: {len(m_imgs)}')
print()

# 对比第一个图片的 JSON
if s_imgs and m_imgs:
    s_val = re.search(r'value="(data:[^"]+)"', s_imgs[0]).group(1)
    m_val = re.search(r'value="(data:[^"]+)"', m_imgs[0]).group(1)
    
    s_json = json.loads(unquote(s_val[5:]))
    m_json = json.loads(unquote(m_val[5:]))
    
    print('样本图片 JSON:')
    print(json.dumps(s_json, ensure_ascii=False, indent=2))
    print()
    print('我的图片 JSON:')
    print(json.dumps(m_json, ensure_ascii=False, indent=2))
    print()
    print(f'keys 匹配: {"PASS" if sorted(s_json.keys()) == sorted(m_json.keys()) else "FAIL"}')
    print(f'title 都是 null: {"PASS" if s_json.get("title") is None and m_json.get("title") is None else "FAIL"}')
    
    # 对比完整标签结构
    s_tag = re.sub(r'value="data:[^"]*"', 'value="DATA"', s_imgs[0])
    m_tag = re.sub(r'value="data:[^"]*"', 'value="DATA"', m_imgs[0])
    print(f'\n样本标签: {s_tag}')
    print(f'我的标签: {m_tag}')
    print(f'标签结构匹配: {"PASS" if s_tag == m_tag else "FAIL"}')
    
    # 检查图片是否在 <p> 内
    p_sample = len(re.findall(r'<p[^>]*><card[^>]*name="image"', sample))
    p_mine = len(re.findall(r'<p[^>]*><card[^>]*name="image"', mine))
    print(f'\n样本图片在<p>内: {p_sample}, 我的: {p_mine}')
