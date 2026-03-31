# UI/UX Pro Max - LangChain集成指南

## 📋 目录

1. [概述](#概述)
2. [集成方式](#集成方式)
3. [实现步骤](#实现步骤)
4. [使用示例](#使用示例)
5. [高级用法](#高级用法)
6. [常见问题](#常见问题)

---

## 概述

UI/UX Pro Max可以轻松集成到LangChain中，作为LLM可调用的工具。

### 什么是LangChain？

**LangChain**是一个用于构建LLM应用的框架，支持：
- ✅ 工具调用（Tools）
- ✅ 链式调用（Chains）
- ✅ 代理（Agents）
- ✅ 记忆（Memory）
- ✅ 提示模板（Prompt Templates）

### 集成优势

- ✅ **无缝集成**：UI/UX Pro Max作为LangChain工具
- ✅ **LLM调用**：LLM可以自动调用UI/UX Pro Max功能
- ✅ **链式调用**：可以组合多个工具调用
- ✅ **代理支持**：可以创建智能代理
- ✅ **类型安全**：支持Pydantic模型验证

---

## 集成方式

### 方式1: 创建自定义LangChain工具（推荐）

#### 优点
- ✅ 完全控制工具行为
- ✅ 支持复杂参数验证
- ✅ 可以添加自定义逻辑
- ✅ 支持异步调用

#### 缺点
- 需要编写更多代码
- 需要处理错误

---

### 方式2: 使用LangChain的Python函数工具

#### 优点
- ✅ 快速集成
- ✅ 代码简洁
- ✅ 自动类型推断

#### 缺点
- 功能受限
- 无法添加复杂逻辑

---

### 方式3: 创建LangChain代理

#### 优点
- ✅ 智能决策
- ✅ 自动工具选择
- ✅ 支持多轮对话

#### 缺点
- 复杂度高
- 需要更多配置

---

## 实现步骤

### 方式1: 创建自定义LangChain工具

#### 步骤1: 创建工具类

创建 `langchain_tools.py`：

```python
"""
UI/UX Pro Max - LangChain工具
将UI/UX Pro Max的功能封装为LangChain工具
"""

from langchain.tools import BaseTool
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any
import sys
import json
from pathlib import Path

# 导入UI/UX Pro Max函数
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
from search import generate_design_system, search, search_stack_guidelines


class GenerateDesignSystemInput(BaseModel):
    """设计系统生成输入"""
    query: str = Field(description="搜索查询，描述你的产品")
    project_name: Optional[str] = Field(default=None, description="项目名称（可选）")
    output_format: str = Field(default="markdown", description="输出格式：markdown或json")


class SearchDomainInput(BaseModel):
    """域搜索输入"""
    query: str = Field(description="搜索查询")
    domain: Optional[str] = Field(default=None, description="搜索域（可选）")
    max_results: int = Field(default=3, description="最大结果数（1-10）")
    output_format: str = Field(default="markdown", description="输出格式：markdown或json")


class SearchStackGuidelinesInput(BaseModel):
    """技术栈指南搜索输入"""
    query: str = Field(description="搜索查询")
    stack: str = Field(description="技术栈名称")
    max_results: int = Field(default=3, description="最大结果数（1-10）")
    output_format: str = Field(default="markdown", description="输出格式：markdown或json")


class GenerateDesignSystemTool(BaseTool):
    """生成设计系统工具"""
    
    name = "ui_ux_pro_max_generate_design_system"
    description = """生成完整的设计系统推荐，包括模式、风格、颜色、字体、效果和反模式。
    
    输入示例：
    - query: "SaaS dashboard"
    - project_name: "MyApp"
    - output_format: "markdown"
    """
    
    args_schema: Type[GenerateDesignSystemInput] = GenerateDesignSystemInput
    
    def _run(self, query: str, project_name: Optional[str] = None, output_format: str = "markdown") -> str:
        """同步执行工具"""
        result = generate_design_system(query, project_name, output_format)
        return result
    
    async def _arun(self, query: str, project_name: Optional[str] = None, output_format: str = "markdown", 
                  run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """异步执行工具"""
        result = generate_design_system(query, project_name, output_format)
        return result


class SearchDomainTool(BaseTool):
    """搜索域工具"""
    
    name = "ui_ux_pro_max_search_domain"
    description = """搜索特定的UI/UX域，包括风格、颜色、字体、图表、落地页、UX指南等。
    
    可用域：
    - style: UI风格
    - color: 配色方案
    - typography: 字体配对
    - chart: 图表类型
    - landing: 落地页模式
    - product: 产品类型
    - ux: UX指南
    - google-fonts: Google字体
    - icons: 图标库
    - react: React性能
    - web: 应用界面指南
    
    输入示例：
    - query: "glassmorphism"
    - domain: "style"
    - max_results: 5
    - output_format: "markdown"
    """
    
    args_schema: Type[SearchDomainInput] = SearchDomainInput
    
    def _run(self, query: str, domain: Optional[str] = None, max_results: int = 3, 
              output_format: str = "markdown") -> str:
        """同步执行工具"""
        result = search(query, domain, max_results, output_format)
        return result
    
    async def _arun(self, query: str, domain: Optional[str] = None, max_results: int = 3, 
                  output_format: str = "markdown", 
                  run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """异步执行工具"""
        result = search(query, domain, max_results, output_format)
        return result


class SearchStackGuidelinesTool(BaseTool):
    """搜索技术栈指南工具"""
    
    name = "ui_ux_pro_max_search_stack_guidelines"
    description = """搜索技术栈特定的指南和最佳实践。
    
    可用技术栈：
    - html-tailwind: HTML + Tailwind CSS
    - react: React
    - nextjs: Next.js
    - vue: Vue
    - nuxtjs: Nuxt.js
    - nuxt-ui: Nuxt UI
    - svelte: Svelte
    - astro: Astro
    - swiftui: SwiftUI
    - react-native: React Native
    - flutter: Flutter
    - shadcn: shadcn/ui
    - jetpack-compose: Jetpack Compose
    
    输入示例：
    - query: "form validation"
    - stack: "react-native"
    - max_results: 3
    - output_format: "markdown"
    """
    
    args_schema: Type[SearchStackGuidelinesInput] = SearchStackGuidelinesInput
    
    def _run(self, query: str, stack: str, max_results: int = 3, 
              output_format: str = "markdown") -> str:
        """同步执行工具"""
        result = search_stack_guidelines(query, stack, max_results, output_format)
        return result
    
    async def _arun(self, query: str, stack: str, max_results: int = 3, 
                  output_format: str = "markdown", 
                  run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """异步执行工具"""
        result = search_stack_guidelines(query, stack, max_results, output_format)
        return result


# 工具列表
UI_UX_PRO_MAX_TOOLS = [
    GenerateDesignSystemTool(),
    SearchDomainTool(),
    SearchStackGuidelinesTool()
]
```

#### 步骤2: 创建LangChain代理

创建 `langchain_agent.py`：

```python
"""
UI/UX Pro Max - LangChain代理
创建智能代理，自动选择和调用UI/UX Pro Max工具
"""

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StdOutCallbackHandler
from langchain_tools import UI_UX_PRO_MAX_TOOLS

# 创建LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7
)

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=5
)

# 运行代理
if __name__ == "__main__":
    print("UI/UX Pro Max - LangChain代理")
    print("输入你的设计需求，代理将自动调用UI/UX Pro Max工具")
    print("输入'exit'退出\n")
    
    while True:
        user_input = input("用户: ")
        
        if user_input.lower() == 'exit':
            print("再见！")
            break
        
        try:
            response = agent.run(user_input)
            print(f"\n代理: {response}\n")
        except Exception as e:
            print(f"错误: {str(e)}")
```

---

### 方式2: 使用LangChain的Python函数工具

#### 步骤1: 创建Python函数工具

创建 `langchain_function_tools.py`：

```python
"""
UI/UX Pro Max - LangChain Python函数工具
使用LangChain的Python函数工具快速集成UI/UX Pro Max
"""

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional
import sys
import json
from pathlib import Path

# 导入UI/UX Pro Max函数
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
from search import generate_design_system, search, search_stack_guidelines


class GenerateDesignSystemInput(BaseModel):
    """设计系统生成输入"""
    query: str = Field(description="搜索查询")
    project_name: Optional[str] = Field(default=None, description="项目名称")
    output_format: str = Field(default="markdown", description="输出格式")


class SearchDomainInput(BaseModel):
    """域搜索输入"""
    query: str = Field(description="搜索查询")
    domain: Optional[str] = Field(default=None, description="搜索域")
    max_results: int = Field(default=3, description="最大结果数")
    output_format: str = Field(default="markdown", description="输出格式")


class SearchStackGuidelinesInput(BaseModel):
    """技术栈指南搜索输入"""
    query: str = Field(description="搜索查询")
    stack: str = Field(description="技术栈名称")
    max_results: int = Field(default=3, description="最大结果数")
    output_format: str = Field(default="markdown", description="输出格式")


def generate_design_system_func(query: str, project_name: Optional[str] = None, output_format: str = "markdown") -> str:
    """生成设计系统函数"""
    result = generate_design_system(query, project_name, output_format)
    return result


def search_domain_func(query: str, domain: Optional[str] = None, max_results: int = 3, 
                   output_format: str = "markdown") -> str:
    """搜索域函数"""
    result = search(query, domain, max_results, output_format)
    return result


def search_stack_guidelines_func(query: str, stack: str, max_results: int = 3, 
                             output_format: str = "markdown") -> str:
    """搜索技术栈指南函数"""
    result = search_stack_guidelines(query, stack, max_results, output_format)
    return result


# 创建LangChain工具
generate_design_system_tool = StructuredTool.from_function(
    func=generate_design_system_func,
    name="ui_ux_pro_max_generate_design_system",
    description="生成完整的设计系统推荐",
    args_schema=GenerateDesignSystemInput
)

search_domain_tool = StructuredTool.from_function(
    func=search_domain_func,
    name="ui_ux_pro_max_search_domain",
    description="搜索特定的UI/UX域",
    args_schema=SearchDomainInput
)

search_stack_guidelines_tool = StructuredTool.from_function(
    func=search_stack_guidelines_func,
    name="ui_ux_pro_max_search_stack_guidelines",
    description="搜索技术栈特定的指南",
    args_schema=SearchStackGuidelinesInput
)

# 工具列表
UI_UX_PRO_MAX_TOOLS = [
    generate_design_system_tool,
    search_domain_tool,
    search_stack_guidelines_tool
]
```

---

### 方式3: 创建LangChain代理

#### 步骤1: 创建智能代理

创建 `langchain_smart_agent.py`：

```python
"""
UI/UX Pro Max - LangChain智能代理
创建智能代理，根据用户需求自动选择和调用UI/UX Pro Max工具
"""

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain_tools import UI_UX_PRO_MAX_TOOLS

# 创建LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7
)

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的UI/UX设计助手。你可以使用以下工具来帮助用户：
    
    可用工具：
    - ui_ux_pro_max_generate_design_system: 生成完整的设计系统
    - ui_ux_pro_max_search_domain: 搜索特定的UI/UX域
    - ui_ux_pro_max_search_stack_guidelines: 搜索技术栈指南
    
    工作流程：
    1. 分析用户需求
    2. 如果需要设计系统，调用ui_ux_pro_max_generate_design_system
    3. 如果需要搜索特定域，调用ui_ux_pro_max_search_domain
    4. 如果需要技术栈指南，调用ui_ux_pro_max_search_stack_guidelines
    5. 根据工具结果提供设计建议
    
    请根据用户需求智能选择和调用工具。"""),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
])

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=5
)

# 运行代理
if __name__ == "__main__":
    print("UI/UX Pro Max - LangChain智能代理")
    print("输入你的设计需求，代理将自动选择和调用UI/UX Pro Max工具")
    print("输入'exit'退出\n")
    
    while True:
        user_input = input("用户: ")
        
        if user_input.lower() == 'exit':
            print("再见！")
            break
        
        try:
            response = agent.run(user_input)
            print(f"\n代理: {response}\n")
        except Exception as e:
            print(f"错误: {str(e)}")
```

---

## 使用示例

### 示例1: 生成设计系统

```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain_tools import UI_UX_PRO_MAX_TOOLS

# 创建LLM
llm = ChatOpenAI(model_name="gpt-4")

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行代理
response = agent.run("帮我生成一个SaaS仪表盘的设计系统")
print(response)
```

### 示例2: 搜索UI风格

```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain_tools import UI_UX_PRO_MAX_TOOLS

# 创建LLM
llm = ChatOpenAI(model_name="gpt-4")

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行代理
response = agent.run("推荐一些适合SaaS产品的UI风格")
print(response)
```

### 示例3: 搜索技术栈指南

```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain_tools import UI_UX_PRO_MAX_TOOLS

# 创建LLM
llm = ChatOpenAI(model_name="gpt-4")

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行代理
response = agent.run("React Native表单验证的最佳实践是什么？")
print(response)
```

---

## 高级用法

### 1. 自定义工具行为

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

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

### 2. 链式调用

```python
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain_tools import UI_UX_PRO_MAX_TOOLS

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
print(result)
```

### 3. 多代理协作

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
print(response)
```

---

## 常见问题

### Q1: 工具调用失败？

**A**: 
1. 检查UI/UX Pro Max函数是否正确导入
2. 检查工具参数是否正确
3. 检查LLM API密钥是否正确

### Q2: 代理无法选择正确的工具？

**A**: 
1. 检查工具描述是否清晰
2. 检查工具参数是否正确
3. 增加verbose=True查看代理决策过程

### Q3: 如何添加新的工具？

**A**: 
1. 创建新的工具类
2. 继承BaseTool
3. 实现_run和_arun方法
4. 添加到工具列表

### Q4: 如何优化代理性能？

**A**: 
1. 减少max_iterations
2. 使用更快的LLM模型
3. 缓存工具结果
4. 使用异步调用

---

## 总结

UI/UX Pro Max可以通过三种方式集成到LangChain中：

### 方式对比

| 方式 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **方式1: 自定义LangChain工具** | 完全控制、支持复杂逻辑 | 需要更多代码 | ⭐⭐⭐⭐⭐ |
| **方式2: Python函数工具** | 快速集成、代码简洁 | 功能受限 | ⭐⭐⭐⭐ |
| **方式3: LangChain代理** | 智能决策、自动工具选择 | 复杂度高 | ⭐⭐⭐⭐⭐ |

### 推荐使用方式1

**理由**：
1. ✅ **完全控制**：可以自定义工具行为
2. ✅ **支持复杂逻辑**：可以添加自定义逻辑
3. ✅ **异步支持**：支持异步调用
4. ✅ **类型安全**：使用Pydantic模型验证
5. ✅ **易于扩展**：可以轻松添加新工具

### 核心工具

1. **ui_ux_pro_max_generate_design_system** - 生成设计系统
2. **ui_ux_pro_max_search_domain** - 搜索域
3. **ui_ux_pro_max_search_stack_guidelines** - 搜索技术栈指南

### 下一步

1. 选择集成方式
2. 按照实现步骤操作
3. 创建LangChain代理
4. 测试工具功能
5. 开始使用

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
