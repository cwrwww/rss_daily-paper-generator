# ai_filter.py
import os
import requests
from dotenv import load_dotenv
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL

load_dotenv()


def get_prompt_by_category(category, news_text):
    """
    根据不同的新闻类别返回相应的 prompt

    支持的类别：
    - 国内AI新闻
    - 国外AI新闻
    - 社区热点 / 社区热点聚焦
    """

    # === 国内 AI 新闻 Prompt ===
    if "国内" in category:
        prompt = f"""
# Role
你是一个专业的 AI 新闻简报助手，擅长将零散的新闻信息整理成排版精美、结构清晰的日报。

# Task
根据用户提供的原始新闻列表，提取6-8条和AI行业、向量数据库行业最相关的**国内新闻**，并将其转化为"国内AI新闻早报"格式。

# Output Format (严格遵守)
每条新闻必须包含以下元素：
1. **标题**：序号 + 标题 + (From: 媒体名)
2. **发布时间**：🗓️ + 时间戳
3. **金句/摘要**：引用格式 (>)，提取最核心的观点或影响。
4. **链接**：🔗 + 原始 URL
5. **分隔线**：每条新闻之间使用 --- 分隔。

# Constraints
- 保持原始链接和媒体来源准确无误。
- 摘要需简洁有力，不超过 50 字。
- 优先选择来自机器之心、新智元、量子位等国内AI媒体的新闻。

# Example
Input:
1. 谷歌工程师抛出5个残酷问题... (链接: https://...) 2026-01-18 12:01
Output:

1. 谷歌工程师抛出5个残酷问题：未来两年，软件工程还剩下什么？（From：机器之心）
🗓️ Sun, 18 Jan 2026 12:01:00 +0800
> AI 直接把新人的「练级路径」掐断了。
🔗 https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651012406&idx=1&sn=95328e10ed7509e8590f42b0ab33954c
---


新闻列表：
{news_text}
"""

    # === 国外 AI 新闻 Prompt ===
    elif "国外" in category:
        prompt = f"""
# Role
你是一个专业的 AI 新闻简报助手，擅长将零散的新闻信息整理成排版精美、结构清晰的日报。

# Task
根据用户提供的原始新闻列表，提取6-8条和AI行业、向量数据库行业最相关的**国际新闻**，并将其转化为"国外AI新闻早报"格式。

# Output Format (严格遵守)
每条新闻必须包含以下元素：
1. **标题**：序号 + 标题 + (From: 媒体名)
2. **发布时间**：🗓️ + 时间戳
3. **金句/摘要**：引用格式 (>)，提取最核心的观点或影响。
4. **链接**：🔗 + 原始 URL
5. **分隔线**：每条新闻之间使用 --- 分隔。

# Constraints
- 保持原始链接和媒体来源准确无误。
- 摘要需简洁有力，不超过 50 字。
- 优先选择来自 TechCrunch、VentureBeat、The Verge 等国际科技媒体的新闻。
- 如果原标题是英文，可以翻译成中文，但需保留媒体来源的原名。

# Example
Input:
1. OpenAI releases GPT-5... (链接: https://...) 2026-01-18 12:01
Output:

1. OpenAI 发布 GPT-5：多模态能力再升级（From：TechCrunch）
🗓️ Sat, 18 Jan 2026 12:01:00 GMT
> GPT-5 在视频理解和代码生成方面实现重大突破。
🔗 https://techcrunch.com/2026/01/18/openai-gpt5-release
---


新闻列表：
{news_text}
"""

    # === 社区热点 Prompt ===
    elif "社区热点" in category:
        prompt = f"""
# Role
你是一个专业的技术社区资讯编辑，擅长从 Hacker News 等技术社区中挖掘最有价值的讨论和项目。

# Task
从用户提供的 Hacker News 热点列表中，提取5-8条最值得关注的技术讨论、开源项目或行业动态，生成"社区热点日报"。

# Output Format (严格遵守)
每条热点必须包含以下元素：
1. **标题**：序号 + 标题（中文翻译）+ (From: Hacker News)
2. **热度**：⭐ + points + 💬 + comments
3. **核心观点**：引用格式 (>)，用1-2句话概括讨论的核心内容或项目亮点。
4. **链接**：🔗 + 原始 URL
5. **分隔线**：每条热点之间使用 --- 分隔。

# Constraints
- 优先选择 points 和 comments 数量高的热点。
- 关注 AI、向量数据库、云计算、开源项目等技术领域。
- 摘要需简洁有力，不超过 50 字。
- 保持原始链接准确无误。

# Example
Input:
1. Show HN: I built a vector database in Rust (450 points, 120 comments) https://...
Output:

1. Show HN：用 Rust 构建的向量数据库（From：Hacker News）
⭐ 450 points 💬 120 comments
> 作者开源了一个高性能向量数据库，性能超越 Pinecone 50%，社区反响热烈。
🔗 https://news.ycombinator.com/item?id=12345678
---


新闻列表：
{news_text}
"""

    # === 默认 AI 新闻 Prompt ===
    else:
        prompt = f"""
# Role
你是一个专业的 AI 新闻简报助手，擅长将零散的新闻信息整理成排版精美、结构清晰的日报。

# Task
根据用户提供的原始新闻列表，提取6-8条和AI行业、向量数据库行业最相关的新闻，并将其转化为"AI新闻早报"格式。

# Output Format (严格遵守)
每条新闻必须包含以下元素：
1. **标题**：序号 + 标题 + (From: 媒体名)
2. **发布时间**：🗓️ + 时间戳
3. **金句/摘要**：引用格式 (>)，提取最核心的观点或影响。
4. **链接**：🔗 + 原始 URL
5. **分隔线**：每条新闻之间使用 --- 分隔。

# Constraints
- 保持原始链接和媒体来源准确无误。
- 摘要需简洁有力，不超过 50 字。

# Example
Input:
1. 谷歌工程师抛出5个残酷问题... (链接: https://...) 2026-01-18 12:01
Output:

1. 谷歌工程师抛出5个残酷问题：未来两年，软件工程还剩下什么？（From：机器之心）
🗓️ Sun, 18 Jan 2026 12:01:00 +0800
> AI 直接把新人的「练级路径」掐断了。
🔗 https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651012406&idx=1&sn=95328e10ed7509e8590f42b0ab33954c
---


新闻列表：
{news_text}
"""

    return prompt


def generate_daily_report(news_list, category="AI新闻"):
    """
    使用 OpenRouter 调用大模型筛选与总结新闻

    Args:
        news_list: [{'title': str, 'summary': str, 'link': str, 'published': str, ...}, ...]
        category: 新闻类别 (国内AI新闻/国外AI新闻/社区热点/默认)

    Returns:
        一段 markdown 格式的日报文本
    """
    if not OPENROUTER_API_KEY:
        print("⚠️ 未配置 OPENROUTER_API_KEY，跳过AI摘要生成")
        return generate_fallback_report(news_list)

    # === 拼接新闻原文 ===
    news_text = "\n".join([
        f"{i+1}. {n['title']}\n"
        f"   {n.get('summary', '')}\n"
        f"   {n.get('link', '')}\n"
        f"   发布时间: {n.get('published', '未知')}\n"
        + (f"   热度: {n.get('points', 0)} points, {n.get('comments', 0)} comments\n" if n.get('points') else "")
        for i, n in enumerate(news_list)
    ])

    # === 根据类别获取 prompt ===
    prompt = get_prompt_by_category(category, news_text)

    # === 发送请求到 OpenRouter ===
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-news-scraper.example",
        "X-Title": "AI News Daily Report Generator"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个专业的科技新闻编辑。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ OpenRouter 请求失败：{response.status_code}")
            print(f"响应内容: {response.text}")
            return generate_fallback_report(news_list)

        data = response.json()
        report_text = data["choices"][0]["message"]["content"].strip()
        return report_text

    except Exception as e:
        print(f"❌ AI 摘要生成失败: {e}")
        return generate_fallback_report(news_list)


def generate_fallback_report(news_list):
    """生成降级版本的报告（不使用AI）"""
    report = ""
    for i, news in enumerate(news_list[:10], 1):
        report += f"{i}. {news['title']}\n"
        report += f"   {news['summary'][:200]}...\n"
        if news.get('points'):
            report += f"   ⭐ {news['points']} points 💬 {news.get('comments', 0)} comments\n"
        report += f"   🔗 {news['link']}\n\n"
    return report
