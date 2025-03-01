import json

# 读取JSON文件
with open('data/python_tutorial_contents_liaoxuefeng_5-44_chapter.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取content内容
content = '\n'.join([chapter['content'] for chapter in data])

# 保存为txt文件
with open('data/python_tutorial_contents_liaoxuefeng.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print('成功将JSON内容转换为TXT文件')