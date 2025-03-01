import fitz  # PyMuPDF

doc = fitz.open('data\Python-CXSJ.pdf')
doc = doc[46:165]
text = ''
for page in doc:
    print()
    text += page.get_text()

# 清理文本
lines = text.split('\n')
cleaned_lines = []

for line in lines:
    # 跳过只有数字的行
    if line.strip().isdigit():
        continue
        
    # 跳过全英文代码行
    if line.strip() and all(c.isascii() for c in line.strip()):
        continue
        
    # 跳过过短的索引行(少于4个字符)
    if len(line.strip()) < 8:
        continue
        
    cleaned_lines.append(line)
# 删除错误的引号
text = '\n'.join(cleaned_lines)
text = text.replace('', '')
# 统计字数
char_count = len(text.replace('\n', '').replace(' ', ''))
print(f"文本总字数: {char_count}")


# 将提取的文本保存到文件
with open('data/python_tutorial_contents_cxsj.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"成功保存PDF文本内容")
