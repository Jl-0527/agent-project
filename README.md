# 扫地机器人智能客服

基于 LangChain、LangGraph、DashScope 和 Chroma 构建的扫地机器人问答示例。应用通过 RAG 检索本地知识库，并提供天气、用户使用记录查询和使用报告等 Agent 工具。

## 环境要求

- Python 3.10
- DashScope API Key

聊天模型通过 OpenAI 兼容接口调用，因此需要 `OPENAI_API_KEY`；文本向量模型使用 DashScope，需要 `DASHSCOPE_API_KEY`。请勿将密钥提交到仓库。

## 安装与运行

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

配置当前 PowerShell 会话的 API Key：

```powershell
$env:OPENAI_API_KEY = "你的 DashScope API Key"
$env:DASHSCOPE_API_KEY = "你的 DashScope API Key"
```

首次运行或知识文件变更后，构建本地向量库：

```powershell
python -m rag.vector_store
```

启动聊天应用：

```powershell
streamlit run app.py
```

Streamlit 启动后会在终端显示本地访问地址。

## 项目结构

```text
agent/       Agent 定义及工具、中间件
config/      模型、知识库和提示词配置
data/        机器人知识库及示例使用记录
model/       聊天模型与 Embedding 工厂
prompts/     Agent、RAG 和报告提示词
rag/         文档索引与检索问答
utils/       配置、文件、日志和提示词辅助模块
app.py       Streamlit 聊天界面入口
```

知识文件放在 `data/` 下，当前支持 `.txt` 和 `.pdf`。运行时生成的 Chroma 数据库、MD5 索引和日志保存在本地，不需要提交到 Git。
