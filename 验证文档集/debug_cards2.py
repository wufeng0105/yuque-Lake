import re
data = open(r'c:\Users\user\Documents\AgentCode\tools\新建文件夹\yuque-Lake\repos\lakex-doc-extract\doc.umd.js', encoding='utf-8').read()

# Search more broadly
print("=== collapse cardName ===")
m = re.findall(r'cardName:.?collapse.{0,200}', data)
for x in m[:3]: print(x[:250])

print("\n=== note cardName ===")
m2 = re.findall(r'cardName:.?note.{0,200}', data)
for x in m2[:3]: print(x[:250])

print("\n=== DefaultCardValue ===")
m3 = re.findall(r'DefaultCardValue.{0,200}', data)
for x in m3[:3]: print(x[:250])

print("\n=== fromLake for collapse ===")
m4 = re.findall(r'fromLake.{0,30}collapse.{0,200}', data)
for x in m4[:3]: print(x[:250])

print("\n=== fromLake for note ===")
m5 = re.findall(r'fromLake.{0,30}note.{0,200}', data)
for x in m5[:3]: print(x[:250])

# Try finding card value with title field
print("\n=== title field in card value ===")
m6 = re.findall(r'.{0,60}title.{0,60}(?:body|content|text).{0,60}', data)
for x in m6[:5]: print(x[:200])
