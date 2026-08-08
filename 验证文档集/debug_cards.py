import re
data = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\repos\lakex-doc-extract\doc.umd.js', encoding='utf-8').read()

# Search for collapse card value
print("=== collapse card ===")
m = re.findall(r'createCard\("collapse".{0,200}', data)
for x in m[:3]:
    print(x[:250])

print("\n=== note card ===")
m2 = re.findall(r'createCard\("note".{0,200}', data)
for x in m2[:3]:
    print(x[:250])

print("\n=== label card ===")
m3 = re.findall(r'createCard\("label".{0,200}', data)
for x in m3[:3]:
    print(x[:250])

print("\n=== mermaid card ===")
m4 = re.findall(r'createCard\("mermaid".{0,200}', data)
for x in m4[:3]:
    print(x[:250])

print("\n=== hr card ===")
m5 = re.findall(r'createCard\("hr".{0,200}', data)
for x in m5[:3]:
    print(x[:250])
