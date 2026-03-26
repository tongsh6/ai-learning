import fitz
from pathlib import Path

def text_to_pdf(text_file, pdf_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = fitz.open()
    page = doc.new_page()
    
    # 页面配置
    p_width = page.rect.width
    p_height = page.rect.height
    margin = 50
    curr_y = margin
    
    # 字体路径
    font_path = "/System/Library/Fonts/STHeiti Light.ttc"
    font_name = "zh"
    
    # 将文本按行拆分并简单排版
    # 考虑到 PyMuPDF 的 insert_text 不会自动折行，我们需要手动处理或使用其他方法
    # 这里我们使用简便的 insert_htmlbox（如果版本支持）或者按字数折行
    
    lines = content.split('\n')
    
    for line in lines:
        if not line.strip():
            curr_y += 10 # 空行
            continue
            
        # 设置字体大小
        font_size = 12
        if line.startswith('# '):
            font_size = 20
            line = line[2:]
        elif line.startswith('## '):
            font_size = 16
            line = line[3:]
        elif line.startswith('### '):
            font_size = 14
            line = line[4:]
            
        # 插入文本（简单的自动换行逻辑）
        # insert_textbox 可以处理换行
        rect = fitz.Rect(margin, curr_y, p_width - margin, p_height - margin)
        
        # 估算高度
        # 这里使用 insert_textbox，它返回剩余的文本高度
        # 如果超出页面，则新建一页
        rc = page.insert_textbox(rect, line, fontsize=font_size, fontname=font_name, fontfile=font_path, align=0)
        
        # 粗略估计行高
        # 每行 1.2 倍字体大小
        char_per_line = int((p_width - 2*margin) / (font_size * 0.8)) # 估算
        needed_lines = (len(line) // char_per_line) + 1
        curr_y += needed_lines * font_size * 1.5 + 5
        
        if curr_y > p_height - margin:
            page = doc.new_page()
            curr_y = margin

    doc.save(pdf_file)
    doc.close()
    print(f"PDF generated: {pdf_file}")

if __name__ == "__main__":
    text_path = "milestone-1/data/rag_intro_zh.txt"
    pdf_path = "milestone-1/data/rag_intro_zh.pdf"
    text_to_pdf(text_path, pdf_path)
