import requests
import json
from datetime import datetime
from config import FEISHU_WEBHOOK_URL

def send_to_feishu(content, title="📢 AI新闻日报"):
    """
    发送卡片消息到飞书群
    支持 Markdown 格式，展示效果更清晰美观

    Args:
        content: 消息内容（支持 Markdown）
        title: 卡片标题
    """
    if not FEISHU_WEBHOOK_URL:
        print("⚠️ 未配置飞书Webhook URL，跳过发送")
        return False

    # 构造飞书卡片消息体
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    ]
                }
            ]
        }
    }

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            headers=headers,
            data=json.dumps(card),
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 飞书卡片消息已成功发送")
                return True
            else:
                print(f"⚠️ 飞书返回错误: {result}")
                return False
        else:
            print(f"❌ 发送失败，状态码: {response.status_code}, 响应: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 发送到飞书时出错: {e}")
        return False
