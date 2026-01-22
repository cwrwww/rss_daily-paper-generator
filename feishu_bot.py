import requests
import json
from config import FEISHU_WEBHOOK_URL

def send_to_feishu(content, title="AI新闻日报"):
    """发送消息到飞书群"""
    if not FEISHU_WEBHOOK_URL:
        print("⚠️ 未配置飞书Webhook URL，跳过发送")
        return False

    # 构造飞书消息体
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": content
                            }
                        ]
                    ]
                }
            }
        }
    }

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            headers=headers,
            data=json.dumps(message),
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 消息已成功发送到飞书")
                return True
            else:
                print(f"⚠️ 飞书返回错误: {result}")
                return False
        else:
            print(f"⚠️ 发送失败，状态码: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 发送到飞书时出错: {e}")
        return False
