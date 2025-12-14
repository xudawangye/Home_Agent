import re
from ollama import chat as ollama_chat

from tools.light import turn_on


TOOL_MAP = {
    "turn_on_light": turn_on
}


class HomeAgent:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt


    def run(self, user_input: str):
        # 初始化消息列表，用作发送给模型的上下文
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]

        while True:
            resp = ollama_chat(
                model="qwen2.5:1.5b",
                messages=messages,
                stream=True,
            )

            content = "" # 用于累积模型返回的文本内容
            for chunk in resp:
                if chunk.message.content: # 如果当前 chunk 包含文本内容
                    print(chunk.message.content, end="", flush=True) # 实时打印该 chunk 的内容，不自动换行并立即刷新
                    content += chunk.message.content # 将该 chunk 的内容追加到 content 中
            print()

            # ---- 结束条件 ----
            if "Final Answer:" in content:
                return

            # ---- 解析 Action ----
            action_match = re.search(r"Action:\s*(\w+)", content) # 使用正则查找 Action 名称
            input_match = re.search(r"Action Input:\s*(.+)", content) # 使用正则查找 Action Input 内容

            if action_match: # 如果找到了 Action
                action = action_match.group(1) # 提取 Action 名称
                action_input = input_match.group(1).strip() if input_match else "" # 提取 Action Input（如存在）并去除首尾空白

                if action not in TOOL_MAP:
                    observation = f"工具 {action} 不存在"
                else:
                    observation = TOOL_MAP[action](action_input)
                    print(f"[DEBUG] tool result: {observation}")

                # 把 Observation 回喂
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": f"Observation: {observation}\n请只给出 Final Answer"
                })
                continue

            # ---- 3. 没 Final、没 Action：当普通聊天 ----
            return
