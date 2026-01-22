import re
from html import unescape

def clean_html(text):
    """清理HTML标签和特殊字符"""
    if not text:
        return ""

    # HTML解码
    text = unescape(text)

    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)

    # 移除多余的空白
    text = re.sub(r'\s+', ' ', text)

    # 去除首尾空格
    text = text.strip()

    return text
