import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL

def generate_daily_report(news_list, category="AI新闻"):
    """使用OpenRouter API生成AI日报摘要"""
    if not OPENROUTER_API_KEY:
        print("⚠️ 未配置OPENROUTER_API_KEY，跳过AI摘要生成")
        return "\n".join([f"{i+1}. {news['title']}\n{news['summary']}\n🔗 {news['link']}\n"
                         for i, news in enumerate(news_list)])

    # 构造新闻内容
    news_content = ""
    for i, news in enumerate(news_list, 1):
        news_content += f"{i}. 标题: {news['title']}\n"
        news_content += f"   摘要: {news['summary']}\n"
        news_content += f"   链接: {news['link']}\n"
        if news.get('points') or news.get('comments'):
            news_content += f"   热度: {news.get('points', 0)} points, {news.get('comments', 0)} comments\n"
        news_content += "\n"

    # 根据不同类别定制prompt
    if "社区热点" in category:
        system_prompt = """你是一个专业的技术资讯编辑。请从以下Hacker News热点新闻中，挑选出5-8条最值得关注的内容，生成一份简洁的日报。

要求：
1. 优先选择热度高（points和comments多）的新闻
2. 关注AI、向量数据库、云计算、数据库等技术领域
3. 每条新闻用1-2句话概括核心内容
4. 保留原标题和链接
5. 使用中文输出
6. 格式：序号. 标题 - 简短描述（热度信息）[链接]"""
    else:
        system_prompt = f"""你是一个专业的{category}编辑。请从以下新闻中，挑选出5-8条最重要、最有价值的内容，生成一份简洁的日报。

要求：
1. 关注AI技术突破、产品发布、行业动态等重要新闻
2. 每条新闻用1-2句话概括核心内容和价值
3. 保留原标题和链接
4. 使用中文输出
5. 格式：序号. 标题 - 简短描述 [链接]"""

    # 调用OpenRouter API
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"以下是今天的{category}:\n\n{news_content}"}
            ]
        }

        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            report = result['choices'][0]['message']['content']
            return report
        else:
            print(f"⚠️ API调用失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return generate_fallback_report(news_list)

    except Exception as e:
        print(f"❌ AI摘要生成失败: {e}")
        return generate_fallback_report(news_list)


def generate_fallback_report(news_list):
    """生成降级版本的报告（不使用AI）"""
    report = ""
    for i, news in enumerate(news_list[:10], 1):
        report += f"{i}. {news['title']}\n"
        report += f"   {news['summary'][:200]}...\n"
        if news.get('points'):
            report += f"   热度: {news['points']} points, {news.get('comments', 0)} comments\n"
        report += f"   🔗 {news['link']}\n\n"
    return report
