from feeds import RSS_FEEDS
from fetcher import fetch_rss

def run(category):
    """根据分类抓取新闻"""
    print(f"\n=== 🚀 抓取 {category} ===")
    feeds = RSS_FEEDS.get(category, [])
    all_news = []

    # 只有国外AI新闻才翻译
    translate = (category == "国外AI新闻")

    for name, url in feeds:
        items = fetch_rss(name, url, max_items=5, translate=translate)
        # 在每条新闻的标题中标注来源
        for item in items:
            item["title"] = f"{item['title']}（From：{name}）"
        all_news.extend(items)

    # === 输出结果（包含发布时间）===
    for i, news in enumerate(all_news, 1):
        pub_time = news.get("published", "") or "🕒 时间未知"
        print(f"\n{i}. {news['title']}\n🗓️ {pub_time}\n{news['summary']}\n🔗 {news['link']}")

    return all_news


if __name__ == "__main__":
    # 早上运行国内AI新闻（不翻译）
    run("国内AI新闻")

    # 中午运行国外AI新闻（自动翻译）
    run("国外AI新闻")
