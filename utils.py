# utils.py
from datetime import datetime

def current_time_str():
    """返回当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M')
