# UI/UX Pro Max - LangChain集成示例

## 📋 项目概述

本项目展示了如何将UI/UX Pro Max集成到LangChain中，创建智能UI/UX设计助手。

### 功能特性

- ✅ **智能代理**：自动选择和调用UI/UX Pro Max工具
- ✅ **记忆管理**：保存对话历史，支持上下文感知
- ✅ **多工具支持**：3个核心工具
- ✅ **错误处理**：优雅处理工具调用错误
- ✅ **交互式对话**：支持多轮对话

---

## 🚀 快速开始

### 步骤1: 安装Poetry

```bash
# 使用官方安装脚本
curl -sSL https://install.python-poetry.org | python3 -

# 添加Poetry到PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证安装
poetry --version
```

### 步骤2: 克隆项目

```bash
# 克隆UI/UX Pro Max项目
cd /path/to/projects
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
cd ui-ux-pro-max-skill
```

### 步骤3: 进入示例项目

```bash
# 进入LangChain示例目录
cd langchain-example
```

### 步骤4: 安装依赖

```bash
# 安装项目依赖
poetry install

# 激活虚拟环境
source $(poetry env info --path)/bin/activate
```

### 步骤5: 配置环境变量

创建`.env`文件：

```env
# OpenAI API密钥
OPENAI_API_KEY=sk-your-api-key-here

# 可选：其他API密钥
ANTHROPIC_API_KEY=your-anthropic-key
```

### 步骤6: 运行代理

```bash
# 使用Poetry运行
poetry run dev

# 或使用完整路径
/home/meizu/.local/bin/poetry run dev

# 或激活虚拟环境后运行
source $(poetry env info --path)/bin/activate
python examples/basic_agent.py
```

---

## 🛠️ 项目结构

```
langchain-example/
├── pyproject.toml              # Poetry配置文件
├── examples/                  # 示例代码
│   ├── basic_agent.py        # 基础代理示例
│   ├── advanced_agent.py      # 高级代理示例
│   └── multi_agent.py       # 多代理协作示例
├── tests/                     # 测试文件
│   ├── test_tools.py          # 工具测试
│   ├── test_agent.py          # 代理测试
│   └── conftest.py          # 测试配置
├── .env.example              # 环境变量示例
└── README.md                 # 项目说明
```

---

## 🎯 使用示例

### 示例1: 生成设计系统

**用户输入**:
```
帮我生成一个美容SPA网站的设计系统
```

**代理行为**:
1. 分析需求 → 产品类型: Beauty/Spa Service
2. 调用 `ui_ux_pro_max_generate_design_system`
3. 返回完整的设计系统

**输出**:
```markdown
## Design System: Beauty Spa

### Pattern
- **Name:** Hero-Centric + Social Proof
- **Conversion Focus:** Emotion-driven with trust elements
- **CTA Placement:** Above fold

### Style
- **Name:** Soft UI Evolution
- **Keywords:** Evolved soft UI, better contrast
- **Best For:** Wellness, beauty, lifestyle brands

### Colors
| Role | Hex |
|------|-----|
| Primary | #E8B4B8 |
| Secondary | #A8D5BA |
| CTA | #D4AF37 |

### Typography
- **Heading:** Lora
- **Body:** Raleway
- **Mood:** Calm, wellness, health

### Key Effects
Soft shadows + Smooth transitions (200-300ms)

### Avoid (Anti-patterns)
- Bright neon colors
- Harsh animations
- Dark mode
```

---

### 示例2: 搜索UI风格

**用户输入**:
```
推荐一些适合SaaS产品的UI风格
```

**代理行为**:
1. 分析需求 → 产品类型: SaaS
2. 调用 `ui_ux_pro_max_search_domain`
3. 域: style
4. 返回风格推荐

**输出**:
```markdown
## UI Pro Max Search Results

**Domain:** style | **Query:** SaaS modern professional

**Found:** 5 results

### Result 1
- **Style Category:** Glassmorphism
- **Type:** General
- **Keywords:** Glassmorphism, soft shadows, blur, translucent
- **Best For:** Modern dashboards, SaaS platforms
- **Performance:** ⚡ Excellent
- **Accessibility:** ✓ WCAG AAA

### Result 2
- **Style Category:** Minimalism & Swiss Style
- **Type:** General
- **Keywords:** Clean, simple, spacious, functional
- **Best For:** Enterprise apps, dashboards
- **Performance:** ⚡ Excellent
- **Accessibility:** ✓ WCAG AAA
```

---

### 示例3: 搜索技术栈指南

**用户输入**:
```
React Native表单验证的最佳实践是什么？
```

**代理行为**:
1. 分析需求 → 技术栈: React Native
2. 调用 `ui_ux_pro_max_search_stack_guidelines`
3. 返回最佳实践

**输出**:
```markdown
## UI Pro Max Stack Guidelines

**Stack:** react-native | **Query:** form validation

**Found:** 3 results

### Result 1
- **Category:** Components
- **Guideline:** Use functional components
- **Description:** Hooks-based components are standard
- **Do:** Functional components with hooks
- **Don't:** Class components
- **Code Good:** `const App = () => { }`
- **Code Bad:** `class App extends Component`
- **Severity:** Medium
- **Docs URL:** https://reactnative.dev/docs/intro-react

### Result 2
- **Category:** Forms
- **Guideline:** Use controlled components
- **Description:** Use controlled components for form inputs
- **Do:** `<TextInput value={value} onChange={onChange} />`
- **Don't:** Uncontrolled components
- **Code Good:** `const [value, setValue] = useState('')`
- **Code Bad:** `<input type="text" />`
- **Severity:** High
- **Docs URL:** https://reactnative.dev/docs/forms
```

---

## 🔧 高级用法

### 自定义工具行为

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CustomDesignSystemTool(BaseTool):
    """自定义设计系统工具"""
    
    name = "custom_generate_design_system"
    description = "生成设计系统并添加自定义逻辑"
    
    def _run(self, query: str, project_name: str = "MyApp") -> str:
        # 调用UI/UX Pro Max函数
        result = generate_design_system(query, project_name, "json")
        
        # 添加自定义逻辑
        design_system = json.loads(result)
        design_system["custom_field"] = "自定义值"
        design_system["timestamp"] = datetime.now().isoformat()
        
        return json.dumps(design_system, indent=2, ensure_ascii=False)
```

### 多代理协作

```python
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI

# 创建设计代理
design_agent = initialize_agent(
    tools=[generate_design_system_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS
)

# 创建搜索代理
search_agent = initialize_agent(
    tools=[search_domain_tool, search_stack_guidelines_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS
)

# 创建主代理
master_agent = initialize_agent(
    tools=[design_agent, search_agent],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS
)

# 运行主代理
response = master_agent.run("帮我设计一个美容SPA网站")
```

### 链式调用

```python
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

# 创建提示模板
prompt1 = PromptTemplate(
    input_variables=["query"],
    template="分析以下设计需求：{query}"
)

prompt2 = PromptTemplate(
    input_variables=["analysis"],
    template="根据分析结果生成设计系统：{analysis}"
)

# 创建链
chain = SequentialChain(
    chains=[
        LLMChain(llm=llm, prompt=prompt1),
        LLMChain(llm=llm, prompt=prompt2)
    ],
    input_variables=["query"]
)

# 运行链
result = chain.run(query="SaaS dashboard")
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
poetry run test

# 运行特定测试
poetry run pytest tests/test_tools.py
poetry run pytest tests/test_agent.py
```

### 测试覆盖

- ✅ 工具调用测试
- ✅ 代理决策测试
- ✅ 错误处理测试
- ✅ 记忆管理测试

---

## 📊 性能优化

### 1. 减少工具调用次数

```python
# 使用缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_generate_design_system(query, project_name, output_format):
    return generate_design_system(query, project_name, output_format)
```

### 2. 异步调用

```python
# 使用异步工具
from langchain.agents import initialize_agent, Tool, AgentType

agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    max_execution_time=60
)
```

### 3. 批量处理

```python
# 批量生成多个设计系统
queries = ["SaaS dashboard", "ecommerce", "fintech"]

for query in queries:
    result = agent.run(f"生成{query}的设计系统")
    print(result)
```

---

## 🐛 故障排除

### 常见问题

#### Q1: Poetry命令未找到？

**A**:
```bash
# 检查Poetry是否安装
which poetry

# 如果未安装，安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 添加到PATH
export PATH="$HOME/.local/bin:$PATH"
```

#### Q2: 依赖安装失败？

**A**:
```bash
# 清除Poetry缓存
poetry cache clear pypi --all

# 重新安装依赖
poetry install --no-cache

# 检查Python版本
python3 --version
```

#### Q3: UI/UX Pro Max工具导入错误？

**A**:
```python
# 检查Python路径
import sys
print(sys.path)

# 检查UI/UX Pro Max项目路径
from pathlib import Path
project_path = Path(__file__).parent.parent / "ui-ux-pro-max-skill"
print(project_path)
```

#### Q4: 代理无法调用工具？

**A**:
```python
# 启用详细日志
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,  # 启用详细日志
    handle_parsing_errors=True
)
```

---

## 📚 相关文档

- **[Poetry环境配置指南.md](../Poetry环境配置指南.md)** - Poetry安装和配置
- **[LangChain集成指南.md](../LangChain集成指南.md)** - LangChain集成详细说明
- **[数据文件参数说明文档.md](../数据文件参数说明文档.md)** - UI/UX Pro Max数据文件说明
- **[软件设计架构文档.md](../软件设计架构文档.md)** - 项目架构说明

---

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE) 文件

---

**项目版本**: 0.1.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
