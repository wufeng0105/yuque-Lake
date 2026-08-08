import re
from urllib.parse import unquote
import json

content = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\验证文档集\退款SOP.lake', encoding='utf-8').read()

# 找所有 image card
cards = re.findall(r'<card name="image" value="([^"]+)">', content)
print(f"Image cards found: {len(cards)}")
for i, val in enumerate(cards[:3]):
    decoded = json.loads(unquote(val[5:]))
    print(f"\n--- Image {i+1} ---")
    print(f"JSON: {json.dumps(decoded, ensure_ascii=False)}")

# 找所有 collapse card 中的 image
collapse_vals = re.findall(r'<card name="collapse" value="([^"]+)">', content)
for i, val in enumerate(collapse_vals[:2]):
    decoded = json.loads(unquote(val[5:]))
    body = decoded.get('body', '')
    images_in_body = re.findall(r'<card name="image" value="([^"]+)">', body)
    if images_in_body:
        print(f"\n--- Collapse {i+1} body has {len(images_in_body)} images ---")
        img_decoded = json.loads(unquote(images_in_body[0][5:]))
        print(f"Image JSON: {json.dumps(img_decoded, ensure_ascii=False)}")
