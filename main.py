import sys
import os
import dotenv


from agents.home_agent import HomeAgent
from agents.online_agent import OnlineAgent



dotenv.load_dotenv()
# 在线客户端（智谱）
glm_api_key = os.getenv('GLM_API_KEY')

# 模式：local / online，默认本地
mode = "local"

# 读取系统提示词
with open("prompts/ReAct_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 实例化本地HomeAgent
local_agent = HomeAgent(system_prompt=system_prompt)

# 实例化在线Agent
online_agent = OnlineAgent(system_prompt=system_prompt, api_key=glm_api_key)

# 一个安全输入的函数，在控制台出现UnicodeDecodeError时返回空字符串，常见于输入中文后使用backspace删除
def safe_input(prompt=">>> "):
    try:
        return input(prompt)
    except UnicodeDecodeError:
        return ""


if __name__ == "__main__":
    while True:
        user_input = safe_input(">>>")
        if not user_input:
            continue

        # --- 模式切换指令 ---
        if user_input == "切换本地模式":
            mode = "local"
            print("##########注意##########")
            print()
            print("已切换到本地模式（Ollama）")
            print()
            print("##########注意##########")
            continue

        if user_input == "切换在线模式":
            mode = "online"
            print("##########注意##########")
            print()
            print("已切换到在线模式（智谱GLM-4.5）")
            print()
            print("##########注意##########")
            continue

        if user_input == "/bye":
            print("退出程序")
            sys.exit(0)


        # --- 按当前模式调用 ---
        if mode == "local":
            local_agent.run(user_input)
        else:
            online_agent.run(user_input)