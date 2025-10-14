# 🗞️ rss_daily-paper-generator（RSS每日新闻生成）

一个轻量级、可自定义的 Python 工具，用于抓取并格式化 RSS 内容，自动生成简洁的每日资讯摘要。
用户只需替换 RSS 源，即可生成属于自己的“每日新闻简报”——无论是 AI、科技、财经还是体育内容都适用。

A lightweight, customizable Python tool that aggregates and formats RSS feeds into a clean daily news digest.  
Simply replace the RSS sources with your own to generate your personalized “daily paper” — perfect for AI, tech, finance, sports, or any topic you follow.

---

## 🌟 Features/功能特点

- **Universal RSS support/ 支持所有 RSS 源** — Works with any valid RSS/Atom feed  
- **Customizable sources/ 自定义数据源** — Replace or expand your RSS feeds easily  
- **Optional translation/ 可选翻译** — Automatically translate foreign content into Chinese  
- **Standardized output/ 标准化输出** — Title, summary, link, and publish time in unified format  
- **Lightweight/ 轻量化依赖** — Only needs `feedparser` and `requests`

---

## 🛠️ Installation

Clone the repo and set up your Python environment:

```bash
git clone https://github.com/cwrwww/rss_daily-paper-generator.git
cd rss_daily-paper-generator
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Usage
### 1️⃣ Define your feeds

Edit ```feeds.py``` to specify the RSS sources you want to track:
```
RSS_FEEDS = {
    "Tech News": [
        ("TechCrunch", "https://techcrunch.com/feed/"),
        ("The Verge", "https://www.theverge.com/rss/index.xml")
    ],
    "AI News": [
        ("Machine Heart", "https://wechat2rss.xlab.app/feed/51e92aad2728acdd1fda7314be32b16639353001.xml"),
        ("Aibase", "https://rsshub.app/aibase/news")
    ]
}
```

### 2️⃣ Run the main script
``` python main.py```


Example output:
```
=== 🚀 抓取 Tech News ===

1. Meta unveils new AI model for image segmentation（From: TechCrunch）
🗓️ 2025-10-14 09:00
Meta introduces SAM 3, pushing the frontier of conceptual understanding in computer vision.
🔗 https://techcrunch.com/sam3-ai/
```

## 🧪 Test a new RSS feed

You can test any RSS URL before adding it to your feed list:

```python test_rss.py```


Example:

```
=== 🧪 测试 RSS 源: https://rsshub.app/aibase/news ===
📄 Content-Type: application/xml; charset=utf-8
🌐 状态码: 200
✅ 成功解析，共 30 条

1. OpenAI 推出 GPT-5，模型理解力突破
🗓️ 2025-10-14 08:00
OpenAI 正式发布 GPT-5，大幅提升模型的...
🔗 https://aibase.com/news/...
```

## 🧰 Project Structure
```
rss_daily-paper-generator/
│
├── feeds.py          # Define your RSS sources
├── fetcher.py        # Core RSS parsing and translation logic
├── main.py           # Entry point: fetch all feeds by category
├── test_rss.py       # Quick RSS test tool
├── translator.py     # Optional: free translation API helper
├── scheduler.py      # Optional: auto-run daily via schedule
├── requirements.txt  # Dependencies
└── README.md
```

## 🗓️ Automation (optional)

To automatically generate your daily paper at specific times,
you can use schedule in Python or a cron job on your system.

Example with schedule:

import schedule
import time
from main import run

schedule.every().day.at("09:00").do(lambda: run("Tech News"))
schedule.every().day.at("13:00").do(lambda: run("AI News"))

while True:
    schedule.run_pending()
    time.sleep(60)

## 🧾 Requirements

Minimal dependencies:

feedparser
requests
schedule


## 📄 License

MIT License © 2025 cwrwww
