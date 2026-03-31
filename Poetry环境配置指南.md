# UI/UX Pro Max - Poetry环境配置指南

## 📋 目录

1. [概述](#概述)
2. [Poetry安装](#poetry安装)
3. [环境配置](#环境配置)
4. [项目依赖](#项目依赖)
5. [常见问题](#常见问题)

---

## 概述

本指南详细说明如何配置Poetry环境，以便在LangChain开发中使用UI/UX Pro Max。

### 为什么需要Poetry？

**Poetry**是一个现代Python依赖管理和打包工具，提供：
- ✅ 依赖隔离（虚拟环境）
- ✅ 锁定文件（可重现的构建）
- ✅ 简洁的配置（pyproject.toml）
- ✅ 更好的依赖解析
- ✅ 与LangChain完美集成

---

## Poetry安装

### 步骤1: 安装Poetry

#### 方法1: 使用官方安装脚本（推荐）

```bash
# 使用官方安装脚本
curl -sSL https://install.python-poetry.org | python3 -

# 添加Poetry到PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证安装
poetry --version
```

#### 方法2: 使用pip安装

```bash
# 使用pip安装
pip install poetry

# 验证安装
poetry --version
```

#### 方法3: 使用包管理器安装

**Ubuntu/Debian**:
```bash
# 使用apt安装
sudo apt update
sudo apt install -y python3-pip
pip install poetry

# 验证安装
poetry --version
```

**macOS (Homebrew)**:
```bash
# 使用Homebrew安装
brew install poetry

# 验证安装
poetry --version
```

**Fedora/CentOS/RHEL**:
```bash
# 使用dnf安装
sudo dnf install -y python3-pip
pip install poetry

# 验证安装
poetry --version
```

---

## 环境配置

### 步骤2: 配置PATH

#### 方法1: 永久配置（推荐）

**对于zsh用户**:

```bash
# 编辑~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 验证配置
echo $PATH
which poetry
```

**对于bash用户**:

```bash
# 编辑~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 重新加载配置
source ~/.bashrc

# 验证配置
echo $PATH
which poetry
```

#### 方法2: 临时配置（当前会话）

```bash
# 临时设置PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证配置
which poetry
poetry --version
```

#### 方法3: 使用完整路径

```bash
# 直接使用完整路径
/home/meizu/.local/bin/poetry --version
```

---

## 项目依赖

### 步骤3: 安装LangChain和UI/UX Pro Max依赖

#### 创建pyproject.toml

在项目根目录创建或编辑`pyproject.toml`：

```toml
[tool.poetry]
name = "ui-ux-pro-max-langchain"
version = "0.1.0"
description = "UI/UX Pro Max - LangChain集成"
authors = ["UI/UX Pro Max Team"]
readme = "README.md"
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"
langchain = "^0.1.0"
langchain-openai = "^0.1.0"
langchain-community = "^0.1.0"
pydantic = "^2.0.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
black = "^24.0.0"
flake8 = "^7.0.0"
mypy = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
dev = "python langchain_agent.py"
test = "pytest"
lint = "flake8 ."
format = "black ."
```

#### 安装依赖

```bash
# 进入项目目录
cd /home/meizu/Documents/my_agent_project/ui-ux-pro-max-skill

# 安装Poetry依赖
poetry install

# 激活虚拟环境
source $(poetry env info --path)/bin/activate

# 验证安装
poetry show
```

---

## 使用示例

### 示例1: 创建LangChain代理

创建`langchain_agent.py`：

```python
"""
UI/UX Pro Max - LangChain代理
使用Poetry环境运行
"""

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_tools import UI_UX_PRO_MAX_TOOLS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
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

#### 运行代理

```bash
# 使用Poetry运行
poetry run dev

# 或使用完整路径
/home/meizu/.local/bin/poetry run dev

# 或激活虚拟环境后运行
source $(poetry env info --path)/bin/activate
python langchain_agent.py
```

### 示例2: 测试工具

创建`test_tools.py`：

```python
"""
UI/UX Pro Max - 工具测试
使用Poetry环境运行
"""

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain_tools import UI_UX_PRO_MAX_TOOLS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 创建代理
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 测试工具
if __name__ == "__main__":
    print("UI/UX Pro Max - 工具测试")
    
    # 测试1: 生成设计系统
    print("\n测试1: 生成设计系统")
    response = agent.run("帮我生成一个SaaS仪表盘的设计系统")
    print(f"结果: {response}")
    
    # 测试2: 搜索UI风格
    print("\n测试2: 搜索UI风格")
    response = agent.run("推荐一些适合SaaS产品的UI风格")
    print(f"结果: {response}")
    
    # 测试3: 搜索技术栈指南
    print("\n测试3: 搜索技术栈指南")
    response = agent.run("React Native表单验证的最佳实践是什么？")
    print(f"结果: {response}")
```

#### 运行测试

```bash
# 使用Poetry运行
poetry run test
```

---

## 常见问题

### Q1: Poetry命令未找到？

**A**: 
1. 检查Poetry是否安装
```bash
which poetry
```
2. 检查PATH配置
```bash
echo $PATH
```
3. 重新加载shell配置
```bash
# 对于zsh
source ~/.zshrc

# 对于bash
source ~/.bashrc
```

### Q2: 依赖安装失败？

**A**: 
1. 检查Python版本
```bash
python3 --version
```
2. 清除Poetry缓存
```bash
poetry cache clear pypi --all
```
3. 重新安装依赖
```bash
poetry install --no-cache
```

### Q3: 虚拟环境激活失败？

**A**: 
1. 检查虚拟环境路径
```bash
poetry env info --path
```
2. 手动激活
```bash
source $(poetry env info --path)/bin/activate
```
3. 验证激活
```bash
which python
python --version
```

### Q4: LangChain导入错误？

**A**: 
1. 检查LangChain是否安装
```bash
poetry show | grep langchain
```
2. 重新安装LangChain
```bash
poetry update langchain
```
3. 检查Python路径
```bash
which python
python -c "import sys; print(sys.path)"
```

### Q5: UI/UX Pro Max工具导入错误？

**A**: 
1. 检查工具文件是否存在
```bash
ls -la langchain_tools.py
```
2. 检查Python路径
```bash
python -c "import sys; print(sys.path)"
```
3. 检查依赖
```bash
poetry show | grep -E "csv|json|pathlib"
```

---

## 最佳实践

### 1. 依赖管理

```bash
# 安装依赖
poetry install

# 更新依赖
poetry update

# 添加新依赖
poetry add langchain-community

# 添加开发依赖
poetry add --group dev pytest
```

### 2. 虚拟环境管理

```bash
# 查看虚拟环境信息
poetry env info

# 激活虚拟环境
source $(poetry env info --path)/bin/activate

# 退出虚拟环境
deactivate

# 删除虚拟环境
poetry env remove --all
```

### 3. 脚本管理

```bash
# 添加脚本到pyproject.toml
[tool.poetry.scripts]
dev = "python langchain_agent.py"
test = "pytest"
lint = "flake8 ."
format = "black ."

# 运行脚本
poetry run dev
poetry run test
poetry run lint
poetry run format
```

### 4. 环境变量管理

创建`.env`文件：

```env
# OpenAI API密钥
OPENAI_API_KEY=your-api-key-here

# 其他API密钥
ANTHROPIC_API_KEY=your-anthropic-key
```

在Python中加载：

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

---

## 快速开始

### 完整配置流程

```bash
# 1. 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. 配置PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 3. 验证安装
poetry --version

# 4. 进入项目目录
cd /home/meizu/Documents/my_agent_project/ui-ux-pro-max-skill

# 5. 安装依赖
poetry install

# 6. 激活虚拟环境
source $(poetry env info --path)/bin/activate

# 7. 运行代理
poetry run dev
```

---

## 总结

Poetry是UI/UX Pro Max LangChain开发的理想依赖管理工具。

### 核心优势

1. ✅ **依赖隔离**：虚拟环境隔离项目依赖
2. ✅ **可重现构建**：锁定文件确保一致性
3. ✅ **简洁配置**：pyproject.toml统一管理
4. ✅ **LangChain集成**：完美支持LangChain生态
5. ✅ **跨平台**：支持Linux、macOS、Windows

### 下一步

1. 安装Poetry
2. 配置PATH
3. 安装项目依赖
4. 创建LangChain代理
5. 测试工具功能
6. 开始使用

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
