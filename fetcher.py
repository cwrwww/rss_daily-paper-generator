import requests
import feedparser
from datetime import datetime
from translator import translate_text

def fetch_rss(feed_name, feed_url, max_items=20, translate=False):
    """解析RSS源（带UA请求），支持可选翻译 + 发布时间"""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AInewsBot/1.0; +https://example.com)"}

    try:
        resp = requests.get(feed_url, headers=headers, timeout=10)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
    except Exception as e:
        print(f"⚠️ {feed_name} 抓取失败: {e}")
        return []

    if not feed.entries:
        print(f"⚠️ {feed_name} 无法读取或源无更新")
        return []

    items = []
    for entry in feed.entries[:max_items]:
        title = entry.title or ""
        summary = entry.get("summary", "")
        link = entry.link or ""

        pub_date = entry.get("published") or entry.get("updated") or ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")

        if translate:
            title = translate_text(title)
            summary = translate_text(summary)

        items.append({
            "title": title.strip(),
            "summary": summary.strip(),
            "link": link,
            "published": pub_date
        })

    print(f"✅ {feed_name} 抓取成功，共 {len(items)} 条")
    return items
