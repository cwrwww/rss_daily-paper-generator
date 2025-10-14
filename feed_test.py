import requests
import feedparser
from datetime import datetime

def test_rss(url, max_items=3):
    """测试RSS源是否可用，并打印标准格式输出"""
    print(f"\n=== 🧪 测试 RSS 源: {url} ===")

    headers = {"User-Agent": "Mozilla/5.0 (compatible; RSSTester/1.0; +https://example.com)"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print("📄 Content-Type:", resp.headers.get("Content-Type", "未知"))
        print("🌐 状态码:", resp.status_code)
        if resp.status_code != 200:
            print("❌ 请求失败，请检查URL是否正确或源是否被屏蔽。")
            return

        feed = feedparser.parse(resp.text)
        entries = feed.entries
        print(f"✅ 成功解析，共 {len(entries)} 条")
        if not entries:
            print("⚠️ 解析为空，可能需要带UA访问或不是标准RSS格式。")
            return

        # 打印前几条标准化输出
        print("\n=== 示例输出 ===")
        for i, entry in enumerate(entries[:max_items], 1):
            title = entry.get("title", "").strip()
            summary = entry.get("summary", "").strip()
            link = entry.get("link", "").strip()

            pub_date = entry.get("published") or entry.get("updated") or ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")

            print(f"\n{i}. {title}\n🗓️ {pub_date}\n{summary[:100]}...\n🔗 {link}")

    except Exception as e:
        print(f"❌ 抓取出错: {e}")


if __name__ == "__main__":
    # 👉 在这里临时填入你想测试的新 RSS 源
    test_urls = [
        "https://rsshub.app/aibase/news",
        # 例如:
        # "https://techcrunch.com/tag/ai/feed/",
        # "https://wechat2rss.xlab.app/feed/xxxxxx.xml",
    ]

    for url in test_urls:
        test_rss(url)
