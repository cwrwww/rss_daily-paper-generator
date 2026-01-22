import re
import feedparser
import requests
from clean_html import clean_html

def extract_hn_metrics(summary_html):
    """从Hacker News RSS的description字段中提取热度数据"""
    points_match = re.search(r"Points:\s*(\d+)", summary_html)
    comments_match = re.search(r"#\s*Comments:\s*(\d+)", summary_html)
    points = int(points_match.group(1)) if points_match else 0
    comments = int(comments_match.group(1)) if comments_match else 0
    return points, comments

def fetch_rss(feed_name, feed_url, max_items=500, translate=False):
    """解析RSS源并提取标题、摘要、链接、发布时间及热度"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; RSSTester/1.0; +https://example.com)"
    }
    try:
        resp = requests.get(feed_url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"⚠️ {feed_name} 请求失败: {resp.status_code}")
            return []
        feed = feedparser.parse(resp.content)
    except Exception as exc:
        print(f"⚠️ {feed_name} 请求异常: {exc}")
        feed = feedparser.parse(feed_url)

    if not feed.entries:
        print(f"⚠️ {feed_name} 无更新")
        return []

    items = []
    for entry in feed.entries[:max_items]:
        title = clean_html(entry.title or "")
        summary_html = entry.get("summary", "")
        summary = clean_html(summary_html)
        link = entry.link or ""
        published = getattr(entry, "published", "")
        comments_url = getattr(entry, "comments", "")

        # 如果是Hacker News源，则提取 Points & Comments
        points, comments = (0, 0)
        if "hackernews" in feed_url or "hnrss.org" in feed_url:
            points, comments = extract_hn_metrics(summary_html)

        # （可选）翻译
        if translate:
            from translator import translate_text
            title = translate_text(title)
            summary = translate_text(summary)

        items.append({
            "title": title.strip(),
            "summary": summary.strip(),
            "link": link.strip(),
            "published": published,
            "points": points,
            "comments": comments,
            "comments_url": comments_url
        })

    return items
