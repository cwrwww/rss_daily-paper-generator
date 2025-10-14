import requests

def translate_text(text, target_lang="zh-CN"):
    """使用 MyMemory 免费API 将英文翻译成中文"""
    if not text.strip():
        return ""
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": f"en|{target_lang}"}
        resp = requests.get(url, params=params, timeout=8)
        return resp.json()["responseData"]["translatedText"]
    except Exception as e:
        print(f"⚠️ 翻译失败: {e}")
        return text
