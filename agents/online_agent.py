import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tools.light import turn_on

# 工具映射
tool_map = {
    "turn_on_light": turn_on
}


# 在线agent
class OnlineAgent:
    def __init__(self, system_prompt: str, api_key: str):
        self.system_prompt = system_prompt
        self.api_key = api_key
    
    # 运行主方法
    def run(self, user_input: str):
        # 初始化消息列表
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]

        while True:
            model = ChatOpenAI(
                temperature=0.7,
                base_url="https://open.bigmodel.cn/api/paas/v4",
                api_key=self.api_key,
                model_name="glm-4.5",
                streaming=True,
                timeout=300,
                max_retries=3,
            )

            content = ""

            # 真·流式输出
            for chunk in model.stream(messages):
                print(chunk.content, end="", flush=True)
                content += chunk.content
            print("\n")
            
            # 解析Action
            action_match = re.search(r"Action:\s*(\w+)", content)
            action_input = re.search(r"Action Input:\s*(.+)", content)

            if action_match:
                action = action_match.group(1)
                action_input = action_input.group(1).strip() if action_input else ""

                if action not in tool_map:
                    observation = f"工具 {action} 不存在"
                else:
                    observation = tool_map[action](action_input)
                    print(f"[DEBUG] tool result: {observation}")

                # 返回Observation
                messages.append({"role": "assistant", 
                                 "content": content}
                            )
                messages.append({
                    "role": "user",
                    "content": f"Observation: {observation}\n请只给出 Final Answer"
                })
                continue
            
            # 结束条件
            if "Final Answer:" in content:
                return
            
            return
