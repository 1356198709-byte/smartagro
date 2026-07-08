"""
第一次调大模型 API —— 用硅基流动（SiliconFlow）
你的 API 密钥自己保管，填在下面 API_KEY 的位置
"""
import requests
import json

# ====== 从密钥.txt读取密钥（sk-trczjhurhtbsdmdbmdjqyezkfunjgkucgprfazvldosqqvxq）======
with open("密钥.txt", "r", encoding="utf-8") as f:
    API_KEY = f.read().strip()
# =====================================================

# 硅基流动的 API 地址（免费的）
URL = "https://api.siliconflow.cn/v1/chat/completions"

# 选择模型：DeepSeek V3（免费额度能用）
# 也可以换成 "Qwen/Qwen2.5-7B-Instruct"（更快更轻量）
MODEL = "deepseek-ai/DeepSeek-V3"

def chat(prompt):
    """发送消息给大模型，返回它的回答"""

    # 构造请求——就是一段 JSON
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一个友好的助手，用中文回答。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,   # 0=死板 1=创意
        "max_tokens": 500     # 最多回复多长
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 发送请求——跟你写 FastAPI POST 接口一模一样
    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 提取大模型的回复
        answer = data["choices"][0]["message"]["content"]
        return answer
    else:
        return f"报错了：{response.status_code} —— {response.text}"


# ====== 测试 ======
if __name__ == "__main__":
    # 问一个问题试试
    result = chat("用一句话介绍什么是大模型API")
    print("=== 大模型回答 ===")
    print(result)
    print("\n调用成功！这就是你的第一个 API Demo。")
