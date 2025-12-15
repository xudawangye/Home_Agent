# Home_Agent

## 项目简介

由于此前购入了一款角色设定为“超级人工智能”的手办，不忍心让其仅作为摆件闲置，便萌生了将其改造为一个真正具备“思考能力”的智能家居中枢的想法。与此同时，我在学校学习《大模型》相关课程的过程中，系统接触了 **LangChain** 框架与 **ReAct（Reason + Act）** 推理模式。在课程学习与个人兴趣的共同驱动下，逐步完成了本项目的设计与实现。

本项目旨在以工程化方式，将课堂中所学的大模型推理范式与工具调用思想落地到真实代码环境中，构建一个支持 **本地模型 / 在线模型自由切换** 的智能体（Agent）原型系统，并最终部署于 **地瓜 RDK X5（8G）开发板** 上。

项目以“家庭智能助手 / 通用对话 Agent”为设想原点，重点并不在于单纯堆砌模型能力，而是尝试还原一个 **完整、清晰且具备可扩展性** 的 Agent 运行流程。因此在架构设计、提示词工程、模式切换以及工具调用机制等方面进行了较多探索。

目前项目仍处于持续完善阶段，代码与设计中难免存在不足，欢迎交流与指正。

---

## 核心特性

* **ReAct 推理模式**
  基于 Thought / Action / Observation 的 ReAct 思想，实现模型“先思考、再行动、再观察结果”的交互式推理流程，使模型具备初步的决策与执行能力。

* **本地 / 在线模型双模式切换**

  * **本地模式**：基于 Ollama 调用本地大模型（如 Qwen 系列），支持流式输出；
  * **在线模式**：通过 API 调用在线大模型（如智谱 GLM），在保持接口统一的前提下，实现运行模式的平滑切换。

* **Agent 封装设计**
  将不同运行模式抽象为 `HomeAgent` 与 `OnlineAgent`，并对外统一暴露 `run()` 接口，降低主程序与具体模型实现之间的耦合度。

* **系统提示词集中管理**
  使用独立的 Prompt 文件（如 `ReAct_system.txt`）集中管理系统提示词，便于对 Agent 行为进行统一约束与持续调优。

* **工具调用机制（Tool Calling）**
  Agent 可根据模型输出自动触发预定义工具，实现从“纯对话”向“可执行动作”的过渡，为后续接入真实智能家居设备奠定基础。

---

## 项目结构说明

```text
Home_Agent/
├── main.py                 # 程序入口，负责模式切换与用户交互
├── agents/
│   ├── home_agent.py       # 本地模型 Agent（Ollama）
│   └── online_agent.py     # 在线模型 Agent（API 调用）
├── tools/
│   └── light.py            # 示例工具（如灯光控制）
├── prompts/
│   └── ReAct_system.txt    # ReAct 系统提示词
├── .env                    # 环境变量（API Key 等）
└── README.md
```

---

## 运行方式

### 1. 环境配置

* 使用 **Python 3.10**；
* 安装 `requirements.txt` 中的依赖；
* 安装 Ollama：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

拉取并运行本地模型（示例）：

```bash
ollama run qwen2.5:1.5b
```

在项目根目录创建 `.env` 文件，并填写在线模型所需的 API Key，例如：

```text
GLM_API_KEY=your_api_key_here
```

---

### 2. 启动程序

```bash
python main.py
```

---

### 3. 交互指令示例

* **本地普通对话**

```text
>>> 为什么汽车会跑
```

* **本地工具调用**

```text
打开卧室的灯
```

* **模式切换**

```text
>>> 切换本地模式
>>> 切换在线模式
```

* **退出程序**

```text
>>> /bye
```

---

## 运行效果演示

> 本节用于展示项目在不同模式下的实际运行效果。以下示例均以 GIF 动图形式呈现，直观展示 Agent 的推理、模式切换与工具调用过程。

### 本地模式演示

* **本地问答示例**
![本地问答](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E6%9C%AC%E5%9C%B0%E6%99%AE%E9%80%9A%E7%9A%84%E5%AF%B9%E8%AF%9D.gif)

* **本地工具调用示例**
![本地工具调用](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E6%9C%AC%E5%9C%B0%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.gif)

### 模式切换演示

* **模式切换过程**
![在线 -> 本地 模式切换](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E5%88%87%E6%8D%A2%E6%9C%AC%E5%9C%B0%E6%A8%A1%E5%BC%8F.gif)

![本地 -> 在线 模式切换](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E5%88%87%E6%8D%A2%E5%9C%A8%E7%BA%BF%E6%A8%A1%E5%BC%8F.gif)

### 在线模式演示

* **在线问答示例**
![在线问答](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E5%9C%A8%E7%BA%BF%E6%99%AE%E9%80%9A%E5%AF%B9%E8%AF%9D.gif)

* **在线工具调用示例**
![在线工具调用](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E5%9C%A8%E7%BA%BF%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.gif)

* **异常处理**
![异常处理](https://raw.githubusercontent.com/xudawangye/Home_Agent/refs/heads/main/_ImageLibrary/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.gif)

---

## 设计思路说明

在项目设计过程中，主要围绕以下几个问题展开：

1. **如何让模型“像 Agent 一样思考”**
   通过 ReAct 系统提示词，引导模型显式输出思考过程与行动决策，使其不再局限于单轮问答，而是具备基本的推理与执行能力。

2. **如何降低模型与业务逻辑之间的耦合**
   通过 Agent 类对模型调用逻辑进行封装，使主程序仅关注输入与输出流程，而不直接依赖具体模型或调用方式。

3. **如何为后续功能扩展预留空间**
   当前仅实现了简单的工具示例，但整体结构支持后续接入更多工具，如文件处理、网络请求以及真实智能家居控制接口等。

---

## 当前不足与后续计划

* ReAct 推理过程仍较为依赖提示词约束，整体鲁棒性有待进一步增强；
* 工具调用目前基于规则解析实现，后续可尝试引入更标准化的 Function Calling 机制；
* 尚未引入长期记忆模块（Memory），上下文一致性仍有改进空间；
* 计划在后续版本中加入语音输入 / 输出、多 Agent 协作等功能。

---

## 致谢

本项目的灵感来源于课堂中对 **LangChain** 与 **ReAct 推理模式** 的学习与讨论，同时也参考了社区中大量优秀的开源项目与技术分享。感谢课程老师的指导以及相关开源社区的知识积累。

---

## 声明

本项目主要用于学习与技术探索，不保证在生产环境中的稳定性与安全性。如有不妥之处，欢迎指出与交流。
