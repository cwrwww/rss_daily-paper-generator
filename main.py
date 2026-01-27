from feeds import RSS_FEEDS
from fetcher import fetch_rss
from ai_filter import generate_daily_report
from feishu_bot import send_to_feishu

def run(category):
    """根据分类抓取新闻"""
    print(f"\n=== 🚀 抓取 {category} ===")
    feeds = RSS_FEEDS.get(category, [])
    all_news = []

    for name, url in feeds:
        items = fetch_rss(name, url, max_items=500)
        for item in items:
            item["title"] = f"{item['title']}（From：{name}）"
        all_news.extend(items)

    for i, news in enumerate(all_news, 1):
        pub_time = news.get("published", "") or "🕒 时间未知"
        print(f"\n{i}. {news['title']}\n🗓️ {pub_time}\n{news['summary']}\n🔗 {news['link']}")

    return all_news

def run_daily(category):
    """抓取 + 摘要 + 发送"""
    all_news = run(category)
    if not all_news:
        print(f"\n=== ⚠️ {category} 无可用新闻，跳过摘要与发送 ===")
        return

    print("\n=== 🧠 生成AI日报中... ===")
    report = generate_daily_report(all_news, category=category)
    print(report)

    # 根据不同类型设置不同标题
    title_map = {
        "国内AI新闻": "📢 国内 AI 新闻日报",
        "国外AI新闻": "📢 国外 AI 新闻日报",
        "社区热点": "📢 HackerNews社区热点日报",
        "社区热点聚焦": "📢 社区热点聚焦日报",
        "行业热点聚焦": "📢 行业热点聚焦日报"
    }
    title = title_map.get(category, f"📢 {category}日报")

    print("\n=== 📤 正在发送到飞书群... ===")
    send_to_feishu(report, title=title)

def run_community_daily_report():
    """生成社区热点日报（包含两部分）"""

    # === Step 1: 抓取社区热点 ===
    print("\n=== 🚀 第一部分：社区热点 ===")
    community_news = run("社区热点")

    # === Step 2: 抓取社区热点聚焦 ===
    print("\n=== 🚀 第二部分：社区热点聚焦 ===")
    focus_news = run("社区热点聚焦")

    # === Step 3: 分别生成两部分的日报 ===
    print("\n=== 🧠 生成社区热点部分... ===")
    community_report = generate_daily_report(community_news, category="社区热点")

    print("\n=== 🧠 生成社区热点聚焦部分... ===")
    focus_report = generate_daily_report(focus_news, category="社区热点聚焦")

    # === Step 4: 拼接成完整日报 ===
    full_report = f""" HackerNews社区热点日报

 📰 社区热点

{community_report}

---

 🎯 社区热点聚焦

{focus_report}
"""

    print("\n=== ✅ 完整日报 ===")
    print(full_report)

    # === Step 5: 推送到飞书 ===
    print("\n=== 📤 正在发送到飞书群... ===")
    send_to_feishu(full_report, title="📢 HackerNews社区热点日报")

    return full_report

if __name__ == "__main__":
    # 运行示例
    run_daily("国外AI新闻")
    run_community_daily_report()