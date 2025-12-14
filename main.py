from ollama import chat as ollama_chat
from openai import OpenAI
import sys
import os
import dotenv
from agents.home_agent import HomeAgent
from agents.online_agent import OnlineAgent



dotenv.load_dotenv()
# 在线客户端（智谱）
glm_api_key = os.getenv('GLM_API_KEY')

# 模式：local / online
mode = "local"

# 读取系统提示词
with open("prompts/ReAct_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 实例化本地HomeAgent
local_agent = HomeAgent(system_prompt=system_prompt)

# 实例化在线Agent
online_agent = OnlineAgent(system_prompt=system_prompt, api_key=glm_api_key)


def safe_input(prompt=">>> "):
    try:
        return input(prompt)
    except UnicodeDecodeError:
        return ""


# 原有的本地模型调用方法，已废弃，实际调用为HomeAgent的run方法
# def call_local_model(user_input):
#     """调用本地 Ollama 模型（流式输出）"""
#     stream = ollama_chat(
#         model='qwen2.5:1.5b',
#         messages=[
#             {'role': 'system', 'content': system_prompt},
#             {'role': 'user', 'content': user_input}
#         ],
#         stream=True,
#     )

#     content = ""
#     for chunk in stream:
#         if chunk.message.content:
#             txt = chunk.message.content
#             print(txt, end="", flush=True)
#             content += txt

#     print()
#     return content


# def call_online_model(user_input):
#     llm = ChatOpenAI(
#         temperature=0.7,
#         base_url="https://open.bigmodel.cn/api/paas/v4",
#         api_key=glm_api_key,
#         model_name="glm-4.5",
#         streaming=True,
#     )

#     # Prompt 模板（必须！否则 messages 会报错）
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ])

#     chain = prompt | llm

#     # 真·流式输出
#     for chunk in chain.stream({"input": user_input}):
#         print(chunk.content, end="", flush=True)
#     print("\n")

if __name__ == "__main__":
    while True:
        user_input = safe_input(">>>")
        if not user_input:
            continue

        # --- 模式切换指令 ---
        if user_input == "切换本地模式":
            mode = "local"
            print("已切换到本地模式（Ollama）")
            continue

        if user_input == "切换在线模式":
            mode = "online"
            print("已切换到在线模式（智谱ai）")
            continue

        if user_input == "/bye":
            print("退出程序")
            sys.exit(0)


        # --- 按当前模式调用 ---
        if mode == "local":
            local_agent.run(user_input)
        else:
            online_agent.run(user_input)