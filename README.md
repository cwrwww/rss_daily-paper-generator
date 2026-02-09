# RSS Daily Paper Generator

一个基于 Python 的自动化新闻聚合工具，通过 RSS 抓取多源新闻，利用 AI 大模型生成结构化日报摘要，并自动推送至飞书群。

An automated news aggregation tool built with Python. It fetches multi-source news via RSS, generates structured daily report summaries using AI (via OpenRouter), and pushes them to Feishu (Lark) group chats.

## 功能特性

- **多分类 RSS 聚合** — 支持国内 AI 新闻、国外 AI 新闻、Hacker News 社区热点等多个分类
- **AI 智能摘要** — 通过 OpenRouter 调用主流大模型（Gemini / Claude / GPT 等），自动筛选并生成格式化日报
- **飞书群推送** — 以卡片消息形式推送至飞书群，支持 Markdown 排版
- **Hacker News 热度提取** — 自动解析 Points 和 Comments 数据，按热度排序
- **可选翻译** — 内置 MyMemory 翻译 API，可将英文内容翻译为中文
- **定时调度** — 内置 `schedule` 定时器，支持按星期和时间自动执行
- **AI 降级机制** — 未配置 API Key 时自动降级为纯文本报告，不影响基础功能
- **Docker 部署** — 提供 Dockerfile 和 docker-compose 配置，一键部署

## 项目结构

```
rss_daily-paper-generator/
├── main.py              # 主入口：抓取 → AI 摘要 → 飞书推送
├── config.py            # 配置管理：加载环境变量
├── feeds.py             # RSS 源定义：按分类管理订阅源
├── fetcher.py           # RSS 解析：抓取与数据提取
├── ai_filter.py         # AI 摘要：调用 OpenRouter 生成日报
├── feishu_bot.py        # 飞书推送：卡片消息发送
├── translator.py        # 翻译模块：MyMemory API
├── clean_html.py        # HTML 清洗：标签与特殊字符处理
├── utils.py             # 工具函数
├── scheduler.py         # 定时调度器：按计划自动执行
├── feed_test.py         # RSS 源测试工具
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 镜像构建
├── docker-compose.yml   # Docker Compose 编排
└── .env.example         # 环境变量示例
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cwrwww/rss_daily-paper-generator.git
cd rss_daily-paper-generator
```

### 2. 安装依赖

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的实际配置：

| 变量名 | 必填 | 说明 | 默认值 |
|--------|------|------|--------|
| `FEISHU_WEBHOOK_URL` | 是 | 飞书群自定义机器人 Webhook 地址 | - |
| `OPENROUTER_API_KEY` | 是 | OpenRouter API Key，用于 AI 摘要生成 | - |
| `OPENROUTER_MODEL` | 否 | 使用的 AI 模型 | `google/gemini-2.0-flash-exp:free` |

> **飞书 Webhook 获取方式**：飞书群 → 设置 → 群机器人 → 添加自定义机器人 → 复制 Webhook 地址
>
> **OpenRouter API Key 获取方式**：访问 https://openrouter.ai/keys 创建

### 4. 运行

```bash
# 手动执行一次
python main.py

# 启动定时调度
python scheduler.py
```

## RSS 源配置

编辑 `feeds.py` 自定义你的订阅源：

```python
RSS_FEEDS = {
    "国内AI新闻": [
        ("机器之心", "https://wechat2rss.xlab.app/feed/xxx.xml"),
        ("量子位", "https://www.qbitai.com/feed"),
    ],
    "国外AI新闻": [
        ("TechCrunch", "https://techcrunch.com/tag/ai/feed/"),
        ("VentureBeat", "https://venturebeat.com/category/ai/feed/"),
    ],
    "社区热点": [
        ("Hacker News", "https://hnrss.org/newest?points=200&comments=100&count=50"),
    ],
    # 添加更多分类...
}
```

分类名称可以自由定义，程序会根据分类名自动匹配对应的 AI Prompt 模板：

| 分类关键词 | Prompt 行为 |
|-----------|------------|
| 包含"国内" | 优先选择国内 AI 媒体新闻，中文输出 |
| 包含"国外" | 优先选择国际科技媒体，英文标题自动翻译 |
| 包含"社区热点" | 提取 Hacker News 热度数据，关注技术讨论 |
| 其他 | 通用 AI 新闻日报格式 |

## 测试 RSS 源

在添加新的 RSS 源之前，可以使用测试工具验证：

```bash
python feed_test.py
```

编辑 `feed_test.py` 中的 `test_urls` 列表添加你要测试的 URL，输出示例：

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

## 定时调度

`scheduler.py` 中预设了以下调度计划：

| 时间 | 任务 |
|------|------|
| 周一、周四 10:00 | 国内 AI 新闻日报 |
| 周一、周四 14:00 | 国外 AI 新闻日报 |
| 周二、周五 10:00 | HackerNews 社区热点日报 |

可以根据需求修改 `scheduler.py` 中的调度规则：

```python
# 每天执行
schedule.every().day.at("09:00").do(job_domestic)

# 指定星期执行
schedule.every().monday.at("10:00").do(job_domestic)

# 每隔 N 小时执行
schedule.every(6).hours.do(job_international)
```

## Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 确保 .env 文件已配置
cp .env.example .env
# 编辑 .env 填入实际值

# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Docker

```bash
# 构建镜像
docker build -t ainews-scheduler .

# 运行容器
docker run -d \
  --name ainews_scheduler \
  --env-file .env \
  -e TZ=Asia/Shanghai \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  ainews-scheduler
```

## 工作流程

```
1. 抓取 RSS        feeds.py 定义源 → fetcher.py 解析
       ↓
2. 数据清洗        clean_html.py 去除 HTML 标签
       ↓
3. AI 摘要生成     ai_filter.py → OpenRouter API → 大模型筛选 + 格式化
       ↓
4. 推送飞书        feishu_bot.py → 飞书群卡片消息
```

## 依赖

| 包名 | 用途 |
|------|------|
| `feedparser` | RSS/Atom 解析 |
| `requests` | HTTP 请求 |
| `python-dotenv` | 环境变量加载 |
| `schedule` | 定时任务调度 |
| `python-dateutil` | 日期时间处理 |
| `urllib3` | HTTP 底层支持 |

## License

MIT License
