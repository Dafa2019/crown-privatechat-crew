# Crown PrivateChat Crew — 故障排查指南

> 本文档记录 `crown-privatechat-crew` 项目在搭建和部署过程中遇到的真实问题及解决方案。

---

## 1. SSL 证书问题（Docker 容器内）

**现象：** 在 Windows Server Core 容器中运行 `crewai login` 时报错：

```
SSL: CERTIFICATE_VERIFY_FAILED
```

**原因：** Windows Server Core 容器缺少根证书，Python 的 SSL 模块无法验证 HTTPS 连接。

**解决方案：** 设置环境变量指向 `certifi` 包的证书文件。注意路径必须使用**正斜杠**：

```bash
# 先确认 certifi 的 cacert.pem 路径
python -c "import certifi; print(certifi.where())"
# 输出类似: C:/Python312/Lib/site-packages/certifi/cacert.pem
```

然后设置环境变量：

```bash
# Linux / Docker 容器内
export SSL_CERT_FILE="C:/Python312/Lib/site-packages/certifi/cacert.pem"
export REQUESTS_CA_BUNDLE="C:/Python312/Lib/site-packages/certifi/cacert.pem"
```

```dockerfile
# Dockerfile 中永久设置
ENV SSL_CERT_FILE="C:/Python312/Lib/site-packages/certifi/cacert.pem"
ENV REQUESTS_CA_BUNDLE="C:/Python312/Lib/site-packages/certifi/cacert.pem"
```

> 注意：路径中使用正斜杠 `/`，不要用反斜杠 `\`，否则可能被转义导致路径解析失败。

---

## 2. CrewAI AMP GUI 不支持单 Agent 选模型

**现象：** 在 AMP 的 GUI 界面中，只能设置一个全局默认模型，无法为每个 Agent 单独指定不同的模型。

**原因：** AMP GUI 目前只提供全局模型配置入口。

**解决方案：** 在代码中为每个 Agent 显式指定 `llm` 参数：

```yaml
# config/agents.yaml
privacy_crypto_engineer:
  role: "Privacy & Crypto Engineer"
  goal: "设计端到端加密方案"
  backstory: "..."
  llm: "anthropic/claude-sonnet-4-6"

threat_modeler:
  role: "Threat Modeler"
  goal: "识别安全威胁"
  backstory: "..."
  llm: "openai/gpt-4o"
```

或者在 Python 代码中直接设置：

```python
@agent
def privacy_crypto_engineer(self) -> Agent:
    return Agent(
        config=self.agents_config['privacy_crypto_engineer'],
        llm="anthropic/claude-sonnet-4-6",
        verbose=True,
    )
```

> 代码中的 `llm` 参数会覆盖 AMP GUI 的全局默认模型。

---

## 3. SerperDevTool 需要 API Key

**现象：** 使用 `SerperDevTool` 进行网络搜索时报错，提示缺少 API Key。

**原因：** `SerperDevTool` 依赖 Serper.dev 的搜索 API，需要设置 `SERPER_API_KEY` 环境变量。

**解决方案：**

1. 前往 [https://serper.dev](https://serper.dev) 注册账号（免费额度 2500 次搜索）
2. 在 Dashboard 中获取 API Key
3. 在 AMP 的 Environment Variables 中添加：

```
Key:   SERPER_API_KEY
Value: <你的 API Key>
```

本地开发时，在 `.env` 文件中添加：

```bash
SERPER_API_KEY=your_api_key_here
```

---

## 4. Handle 不能为空

**现象：** 创建 Agent 时报错，提示 Handle 字段为空或无效。

**原因：** CrewAI AMP 中创建 Agent 时，Handle 是必填字段，用于唯一标识该 Agent。

**解决方案：** 使用英文短横线（kebab-case）格式填写 Handle：

```
# 正确格式
privacy-crypto-engineer
threat-modeler
compliance-analyst

# 错误格式
Privacy Crypto Engineer    ← 不能有空格
privacy_crypto_engineer    ← 不能用下划线
                           ← 不能留空
```

---

## 5. hierarchical process 的 manager_agent 配置

**现象：** 使用 `Process.hierarchical` 时报错：

```
pydantic_core.ValidationError: Manager agent should not be included in agents list
```

**原因：** `manager_agent` 被同时放入了 `agents=[]` 列表中，CrewAI 不允许这样做。

**解决方案（二选一）：**

### 方案 A：使用 `manager_llm` 自动创建 Manager

让 CrewAI 自动生成一个 Manager Agent，不需要手动定义：

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,       # 所有 worker agents
        tasks=self.tasks,
        process=Process.hierarchical,
        manager_llm="anthropic/claude-sonnet-4-6",  # 自动创建 manager
        verbose=True,
    )
```

### 方案 B：手动定义 Manager 并从 agents 列表中排除

```python
@agent
def brain(self) -> Agent:
    """Manager agent — 用 @agent 装饰器加载 YAML 配置"""
    return Agent(
        config=self.agents_config['brain'],
        verbose=True,
    )

@crew
def crew(self) -> Crew:
    # 从 self.agents 中过滤掉 brain
    worker_agents = [a for a in self.agents if a.role != self.brain().role]
    return Crew(
        agents=worker_agents,
        tasks=self.tasks,
        process=Process.hierarchical,
        manager_agent=self.brain(),  # 单独传入 manager
        verbose=True,
    )
```

> 关键原则：`manager_agent`（或 `manager_llm`）和 `agents` 列表互斥，Manager 绝对不能出现在 `agents` 中。
