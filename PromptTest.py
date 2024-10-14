from fastapi import FastAPI, Request
import requests
import json

app = FastAPI()

# 配置API的URL和API密钥
API_URL = "http://localhost:11434/api/generate"
HEADERS = {
    'Content-Type': 'application/json',
}

def get_llama_response(prompt):
    # 构造请求数据
    # payload = {
    #     "prompt": prompt,
    #     "max_length": 200,
    #     "temperature": 0.7
    # }

    payload = {
        'model': 'llama3.1',
        "prompt": prompt
    }

    try:
        # 发送请求
        response = requests.post(API_URL, data=json.dumps(payload), headers=HEADERS)
        response.raise_for_status()

        str_response = response.text
        total_response = ''
        for x in str_response.split('\n'):
            try:
                total_response += json.loads(x)['response']
            except:
                break
        # print(total_response)
        return total_response
        # if 'choices' in response_json and len(response_json['choices']) > 0:
        #     return response_json['choices'][0].get('text', 'API没有返回结果').strip()
        # else:
        #     return "API返回格式有误"

    except requests.exceptions.RequestException as e:
        return f"API请求出错: {e}"

# 暴露一个小程序接口
@app.post("/metaminder_chat")
async def metaminder_chat(request: Request):
    req_data = await request.json()
    user_input = req_data.get("message")

    # 结合prompt发送到llama
    prompt = (
        f"你是一个智慧医疗服务机器人，你面对的是患者。你需要结合一定的科学性，用浅显的语言表达一些深奥的医学难题。在对话的末尾，一定要"
        f"加上“请问还有什么要帮助你的呢？”现在，你的患者向你提问：'{user_input}'。")

    # 获取llama的回复
    llama_response = get_llama_response(prompt)

    return {"response": llama_response}

# 主函数
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



