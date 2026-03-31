# UI/UX Pro Max - Dify集成指南

## 📋 目录

1. [概述](#概述)
2. [准备工作](#准备工作)
3. [安装步骤](#安装步骤)
4. [配置步骤](#配置步骤)
5. [使用示例](#使用示例)
6. [工作流配置](#工作流配置)
7. [API调用](#api调用)
8. [故障排除](#故障排除)

---

## 概述

UI/UX Pro Max可以通过Dify的**自定义工具（Custom Tools）**功能集成，为LLM应用提供UI/UX设计智能。

### 集成架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Dify平台                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  应用 (App)                                  │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │  工作流 (Workflow)                  │   │  │
│  │  │  ┌─────────────────────────────────┐   │   │  │
│  │  │  │  LLM节点                    │   │   │  │
│  │  │  └─────────────────────────────────┘   │   │  │
│  │  │              │                       │   │  │
│  │  │              ▼                       │   │  │
│  │  │  ┌─────────────────────────────────┐   │   │  │
│  │  │  │  工具节点 (Tool Node)       │   │   │  │
│  │  │  │  ┌─────────────────────┐     │   │   │  │
│  │  │  │  │ UI/UX Pro Max     │     │   │   │  │
│  │  │  │  │ - 设计系统生成    │     │   │   │  │
│  │  │  │  │ - 域搜索          │     │   │   │  │
│  │  │  │  │ - 技术栈指南      │     │   │   │  │
│  │  │  │  └─────────────────────┘     │   │   │  │
│  │  │  └─────────────────────────────────┘   │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 核心功能

- **设计系统生成**: 基于产品类型生成完整的设计系统
- **域搜索**: 搜索UI风格、颜色、字体、图表、落地页、UX指南
- **技术栈指南**: 获取React、Next.js、Vue、SwiftUI等技术栈的特定指南
- **智能推荐**: BM25搜索引擎 + 161条推理规则

---

## 准备工作

### 1. 系统要求

- **Dify版本**: 0.6.0+
- **Python版本**: 3.8+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 2. 获取UI/UX Pro Max源码

```bash
# 克隆仓库
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
cd ui-ux-pro-max-skill

# 验证Python环境
python3 --version  # 应该是3.8+
```

### 3. 准备CSV数据文件

确保以下文件存在：
```
src/ui-ux-pro-max/data/
├── products.csv           # 161种产品类型
├── styles.csv            # 67种UI风格
├── colors.csv            # 161种配色方案
├── typography.csv        # 57种字体配对
├── charts.csv            # 25种图表类型
├── landing.csv           # 24种落地页模式
├── ux-guidelines.csv     # 99条UX指南
├── ui-reasoning.csv      # 161条推理规则
├── google-fonts.csv     # Google字体库
├── icons.csv            # 图标库
├── app-interface.csv    # 应用界面指南
├── react-performance.csv # React性能指南
└── stacks/              # 技术栈指南
    ├── react-native.csv
    ├── html-tailwind.csv
    ├── react.csv
    └── ...
```

---

## 安装步骤

### 方法1: Docker Compose集成（推荐）

#### 步骤1: 启动Dify

```bash
# 克隆Dify仓库
git clone https://github.com/langgenius/dify.git
cd dify/docker

# 启动Dify
docker compose up -d

# 等待服务启动
# 访问 http://localhost/install
```

#### 步骤2: 进入API容器

```bash
# 查看运行的容器
docker ps

# 进入API容器
docker exec -it dify-api-1 bash

# 或者使用docker-compose
docker compose exec api bash
```

#### 步骤3: 创建工具目录

```bash
# 在Dify的tools目录下创建ui-ux-pro-max工具
cd /app/api/core/tools/provider/builtin
mkdir -p ui_ux_pro_max
cd ui_ux_pro_max
```

#### 步骤4: 复制工具文件

```bash
# 从宿主机复制文件到容器
# 在宿主机执行
docker cp ui_ux_pro_max.py dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp provider.yaml dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp tools.yaml dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/

# 或者使用docker-compose
docker compose cp ui_ux_pro_max.py api:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker compose cp provider.yaml api:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker compose cp tools.yaml api:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
```

#### 步骤5: 复制CSV数据文件

```bash
# 在容器内创建数据目录
mkdir -p /app/api/core/tools/provider/builtin/ui_ux_pro_max/data

# 从宿主机复制数据文件
docker cp src/ui-ux-pro-max/data/ dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/

# 或者逐个复制
docker cp src/ui-ux-pro-max/data/products.csv dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
docker cp src/ui-ux-pro-max/data/styles.csv dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
# ... 其他CSV文件
```

#### 步骤6: 重启API服务

```bash
# 退出容器
exit

# 重启API容器
docker restart dify-api-1

# 或者重启所有服务
docker compose restart api
```

### 方法2: 本地开发集成

#### 步骤1: 克隆Dify仓库

```bash
git clone https://github.com/langgenius/dify.git
cd dify
```

#### 步骤2: 安装Python依赖

```bash
cd api
pip install -r requirements.txt
```

#### 步骤3: 创建工具目录

```bash
cd api/core/tools/provider/builtin
mkdir -p ui_ux_pro_max
cd ui_ux_pro_max
```

#### 步骤4: 复制工具文件

```bash
# 从UI/UX Pro Max项目复制
cp /path/to/ui-ux-pro-max-skill/dify-integration/ui_ux_pro_max.py .
cp /path/to/ui-ux-pro-max-skill/dify-integration/provider.yaml .
cp /path/to/ui-ux-pro-max-skill/dify-integration/tools.yaml .

# 创建数据目录并复制CSV文件
mkdir -p data
cp /path/to/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/*.csv data/
cp -r /path/to/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks data/
```

#### 步骤5: 修改数据路径

编辑`ui_ux_pro_max.py`，修改DATA_DIR：

```python
# 原始代码
DATA_DIR = Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "data"

# 修改为
DATA_DIR = Path(__file__).parent / "data"
```

#### 步骤6: 启动Dify API

```bash
# 返回Dify根目录
cd /path/to/dify

# 启动API服务
cd api
python main.py

# 或者使用gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 main:app
```

---

## 配置步骤

### 1. 在Dify中创建应用

1. 登录Dify管理后台
2. 点击"创建应用"
3. 选择"聊天助手（Chatbot）"或"工作流（Workflow）"

### 2. 配置工具

#### 方法A: 在聊天助手中添加工具

1. 进入应用设置
2. 点击"工具"
3. 点击"添加自定义工具"
4. 选择"UI/UX Pro Max"
5. 配置工具参数（如果需要）

#### 方法B: 在工作流中添加工具节点

1. 创建新工作流
2. 点击"+"添加节点
3. 选择"工具"
4. 选择"UI/UX Pro Max"
5. 选择具体的工具函数：
   - `generate_design_system`: 生成设计系统
   - `search_domain`: 搜索域
   - `search_stack_guidelines`: 搜索技术栈指南

### 3. 配置工具参数

#### generate_design_system

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| query | string | 是 | 搜索查询 | "SaaS dashboard" |
| project_name | string | 否 | 项目名称 | "MyApp" |
| output_format | string | 否 | 输出格式 | "markdown" 或 "json" |

#### search_domain

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| query | string | 是 | 搜索查询 | "glassmorphism" |
| domain | string | 否 | 搜索域 | "style", "color", "typography", etc. |
| max_results | integer | 否 | 最大结果数 | 3 (默认) |
| output_format | string | 否 | 输出格式 | "markdown" 或 "json" |

#### search_stack_guidelines

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| query | string | 是 | 搜索查询 | "form validation" |
| stack | string | 是 | 技术栈 | "react-native", "html-tailwind", etc. |
| max_results | integer | 否 | 最大结果数 | 3 (默认) |
| output_format | string | 否 | 输出格式 | "markdown" 或 "json" |

---

## 使用示例

### 示例1: 生成设计系统

#### 场景
用户请求："帮我做一个美容SPA网站的首页"

#### 工作流配置

```
开始节点
    │
    ▼
LLM节点 (提取需求)
    │
    ├─ 输入: "帮我做一个美容SPA网站的首页"
    ├─ 输出: 
    │   - 产品类型: Beauty/Spa Service
    │   - 风格偏好: 优雅、放松
    │   - 项目名称: Serenity Spa
    │
    ▼
工具节点 (UI/UX Pro Max)
    │
    ├─ 工具: generate_design_system
    ├─ 参数:
    │   - query: "美容SPA wellness"
    │   - project_name: "Serenity Spa"
    │   - output_format: "markdown"
    │
    ▼
LLM节点 (生成HTML)
    │
    ├─ 输入: 设计系统结果
    ├─ 输出: 完整的HTML代码
    │
    ▼
结束节点
```

#### 提示词模板

```
你是一个专业的前端开发工程师。使用UI/UX Pro Max工具生成HTML代码。

工作流程:
1. 分析用户需求，提取关键信息
2. 调用UI/UX Pro Max工具生成设计系统
3. 根据设计系统生成HTML代码
4. 应用所有设计规范
5. 遵循检查清单

用户请求: {{user_input}}

请先调用UI/UX Pro Max工具获取设计系统，然后生成HTML代码。
```

### 示例2: 搜索UI风格

#### 场景
用户请求："推荐一些适合SaaS产品的UI风格"

#### 工作流配置

```
开始节点
    │
    ▼
LLM节点 (提取需求)
    │
    ├─ 输入: "推荐一些适合SaaS产品的UI风格"
    ├─ 输出:
    │   - 产品类型: SaaS
    │   - 风格偏好: 现代、专业
    │
    ▼
工具节点 (UI/UX Pro Max)
    │
    ├─ 工具: search_domain
    ├─ 参数:
    │   - query: "SaaS modern professional"
    │   - domain: "style"
    │   - max_results: 5
    │   - output_format: "markdown"
    │
    ▼
LLM节点 (总结推荐)
    │
    ├─ 输入: 搜索结果
    ├─ 输出: 风格推荐总结
    │
    ▼
结束节点
```

### 示例3: 技术栈指南

#### 场景
用户请求："React Native表单验证的最佳实践是什么？"

#### 工作流配置

```
开始节点
    │
    ▼
LLM节点 (提取需求)
    │
    ├─ 输入: "React Native表单验证的最佳实践是什么？"
    ├─ 输出:
    │   - 技术栈: React Native
    │   - 主题: 表单验证
    │
    ▼
工具节点 (UI/UX Pro Max)
    │
    ├─ 工具: search_stack_guidelines
    ├─ 参数:
    │   - query: "form validation"
    │   - stack: "react-native"
    │   - max_results: 3
    │   - output_format: "markdown"
    │
    ▼
LLM节点 (总结指南)
    │
    ├─ 输入: 搜索结果
    ├─ 输出: 最佳实践总结
    │
    ▼
结束节点
```

---

## 工作流配置

### 完整的UI/UX设计助手工作流

```
┌─────────────────────────────────────────────────────────────┐
│                    开始节点                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM节点: 需求分析                        │
│  输入: 用户请求                                       │
│  输出: 产品类型、风格偏好、技术栈、项目名称              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│        工具节点: UI/UX Pro Max - 设计系统生成           │
│  工具: generate_design_system                           │
│  参数:                                                   │
│    - query: 产品类型 + 风格偏好                          │
│    - project_name: 项目名称                               │
│    - output_format: "markdown"                            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│        工具节点: UI/UX Pro Max - 颜色搜索               │
│  工具: search_domain                                    │
│  参数:                                                   │
│    - query: 产品类型 + 颜色偏好                          │
│    - domain: "color"                                     │
│    - max_results: 2                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│        工具节点: UI/UX Pro Max - 字体搜索               │
│  工具: search_domain                                    │
│  参数:                                                   │
│    - query: 产品类型 + 字体偏好                          │
│    - domain: "typography"                                │
│    - max_results: 2                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│        工具节点: UI/UX Pro Max - 技术栈指南             │
│  工具: search_stack_guidelines                           │
│  参数:                                                   │
│    - query: "responsive layout"                           │
│    - stack: "html-tailwind"                             │
│    - max_results: 3                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM节点: 代码生成                          │
│  输入: 设计系统 + 颜色 + 字体 + 技术栈指南              │
│  输出: 完整的HTML/CSS/JS代码                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM节点: 代码审查                          │
│  输入: 生成的代码                                      │
│  输出: 检查清单验证结果                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    结束节点                             │
│  输出: 完整的HTML代码 + 检查清单                       │
└─────────────────────────────────────────────────────────────┘
```

### 工作流配置文件示例

```yaml
name: "UI/UX Design Assistant"
description: "AI-powered UI/UX design assistant with UI/UX Pro Max integration"
version: "1.0.0"

nodes:
  - id: "start"
    type: "start"
    data:
      title: "开始"
      desc: "用户输入设计需求"

  - id: "analyze_requirements"
    type: "llm"
    data:
      title: "需求分析"
      model:
        provider: "openai"
        name: "gpt-4"
        mode: "chat"
      prompt_template: |
        分析用户的设计需求，提取以下信息：
        1. 产品类型（如：SaaS、电商、美容SPA等）
        2. 风格偏好（如：现代、优雅、极简等）
        3. 技术栈（如：HTML+Tailwind、React、Vue等）
        4. 项目名称（可选）
        
        用户需求: {{#start.text#}}
        
        请以JSON格式输出：
        {
          "product_type": "...",
          "style_preference": "...",
          "tech_stack": "...",
          "project_name": "..."
        }

  - id: "generate_design_system"
    type: "tool"
    data:
      title: "生成设计系统"
      provider_id: "ui_ux_pro_max"
      tool_name: "generate_design_system"
      tool_parameters:
        query: "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}"
        project_name: "{{#analyze_requirements.output.project_name#}}"
        output_format: "markdown"

  - id: "search_colors"
    type: "tool"
    data:
      title: "搜索配色方案"
      provider_id: "ui_ux_pro_max"
      tool_name: "search_domain"
      tool_parameters:
        query: "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}"
        domain: "color"
        max_results: 2
        output_format: "markdown"

  - id: "search_typography"
    type: "tool"
    data:
      title: "搜索字体配对"
      provider_id: "ui_ux_pro_max"
      tool_name: "search_domain"
      tool_parameters:
        query: "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}"
        domain: "typography"
        max_results: 2
        output_format: "markdown"

  - id: "search_stack_guidelines"
    type: "tool"
    data:
      title: "搜索技术栈指南"
      provider_id: "ui_ux_pro_max"
      tool_name: "search_stack_guidelines"
      tool_parameters:
        query: "responsive layout accessibility"
        stack: "{{#analyze_requirements.output.tech_stack#}}"
        max_results: 3
        output_format: "markdown"

  - id: "generate_code"
    type: "llm"
    data:
      title: "生成HTML代码"
      model:
        provider: "openai"
        name: "gpt-4"
        mode: "chat"
      prompt_template: |
        你是一个专业的前端开发工程师。根据以下设计系统生成HTML代码。
        
        ## 设计系统
        {{#generate_design_system.output#}}
        
        ## 配色方案
        {{#search_colors.output#}}
        
        ## 字体配对
        {{#search_typography.output#}}
        
        ## 技术栈指南
        {{#search_stack_guidelines.output#}}
        
        请生成完整的HTML代码，包括：
        1. HTML结构
        2. CSS样式（使用Tailwind CSS）
        3. 响应式设计
        4. 无障碍支持
        5. 性能优化
        
        技术栈: {{#analyze_requirements.output.tech_stack#}}

  - id: "review_code"
    type: "llm"
    data:
      title: "代码审查"
      model:
        provider: "openai"
        name: "gpt-4"
        mode: "chat"
      prompt_template: |
        审查以下HTML代码，检查是否符合设计系统要求：
        
        ## 生成的代码
        {{#generate_code.output#}}
        
        ## 检查清单
        - [ ] No emojis as icons (use SVG: Heroicons/Lucide)
        - [ ] cursor-pointer on all clickable elements
        - [ ] Hover states with smooth transitions (150-300ms)
        - [ ] Light mode: text contrast 4.5:1 minimum
        - [ ] Focus states visible for keyboard nav
        - [ ] prefers-reduced-motion respected
        - [ ] Responsive: 375px, 768px, 1024px, 1440px
        
        请输出检查结果和改进建议。

  - id: "end"
    type: "end"
    data:
      title: "结束"
      outputs:
        - title: "HTML代码"
          value: "{{#generate_code.output#}}"
        - title: "代码审查"
          value: "{{#review_code.output#}}"

edges:
  - source: "start"
    target: "analyze_requirements"
  - source: "analyze_requirements"
    target: "generate_design_system"
  - source: "analyze_requirements"
    target: "search_colors"
  - source: "analyze_requirements"
    target: "search_typography"
  - source: "analyze_requirements"
    target: "search_stack_guidelines"
  - source: "generate_design_system"
    target: "generate_code"
  - source: "search_colors"
    target: "generate_code"
  - source: "search_typography"
    target: "generate_code"
  - source: "search_stack_guidelines"
    target: "generate_code"
  - source: "generate_code"
    target: "review_code"
  - source: "review_code"
    target: "end"
```

---

## API调用

### 直接调用工具API

如果需要直接调用UI/UX Pro Max工具，可以使用Dify的API：

```python
import requests

# Dify API配置
DIFY_API_URL = "http://localhost/v1"
DIFY_API_KEY = "your-api-key"

# 调用generate_design_system工具
def call_generate_design_system(query, project_name=None):
    url = f"{DIFY_API_URL}/tools/run"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "tool_name": "generate_design_system",
        "parameters": {
            "query": query,
            "project_name": project_name,
            "output_format": "markdown"
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 调用search_domain工具
def call_search_domain(query, domain=None, max_results=3):
    url = f"{DIFY_API_URL}/tools/run"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "tool_name": "search_domain",
        "parameters": {
            "query": query,
            "domain": domain,
            "max_results": max_results,
            "output_format": "markdown"
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 调用search_stack_guidelines工具
def call_search_stack_guidelines(query, stack, max_results=3):
    url = f"{DIFY_API_URL}/tools/run"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "tool_name": "search_stack_guidelines",
        "parameters": {
            "query": query,
            "stack": stack,
            "max_results": max_results,
            "output_format": "markdown"
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 生成设计系统
    result = call_generate_design_system("美容SPA wellness", "Serenity Spa")
    print(result)
    
    # 搜索UI风格
    result = call_search_domain("glassmorphism", "style", 5)
    print(result)
    
    # 搜索技术栈指南
    result = call_search_stack_guidelines("form validation", "react-native", 3)
    print(result)
```

### 使用Dify SDK

```python
from dify_client import DifyClient

# 初始化客户端
client = DifyClient(
    api_key="your-api-key",
    base_url="http://localhost"
)

# 调用工具
result = client.tools.run(
    tool_name="generate_design_system",
    parameters={
        "query": "SaaS dashboard",
        "project_name": "MyApp",
        "output_format": "markdown"
    }
)

print(result)
```

---

## 故障排除

### 常见问题

#### 1. 工具未显示在Dify中

**问题**: 在Dify的工具列表中看不到UI/UX Pro Max

**解决方案**:
```bash
# 检查工具文件是否存在
ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/

# 检查文件权限
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.yaml
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.py

# 重启API服务
docker restart dify-api-1
```

#### 2. CSV文件未找到

**问题**: 工具报错"File not found: products.csv"

**解决方案**:
```bash
# 检查数据目录
ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/

# 检查CSV文件
ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/*.csv

# 如果文件不存在，重新复制
docker cp src/ui-ux-pro-max/data/*.csv dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
```

#### 3. 工具调用失败

**问题**: 调用工具时返回错误

**解决方案**:
```bash
# 查看API日志
docker logs dify-api-1 --tail 100

# 检查Python语法
python3 -m py_compile ui_ux_pro_max.py

# 测试工具
python3 ui_ux_pro_max.py
```

#### 4. 性能问题

**问题**: 工具调用响应慢

**解决方案**:
```python
# 在ui_ux_pro_max.py中添加缓存
import functools

@functools.lru_cache(maxsize=128)
def _load_csv(filepath):
    """Load CSV with caching"""
    # ... existing code

# 或者使用更快的CSV解析库
import polars as pd

def _load_csv(filepath):
    """Load CSV using polars for better performance"""
    df = pd.read_csv(filepath)
    return df.to_dicts()
```

### 调试技巧

#### 1. 启用详细日志

```python
# 在ui_ux_pro_max.py中添加日志
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.debug(f"Loading CSV from: {filepath}")
logger.debug(f"Search query: {query}")
logger.debug(f"Domain detected: {domain}")
```

#### 2. 测试工具功能

```python
# 创建测试脚本
def test_ui_ux_pro_max():
    print("Testing UI/UX Pro Max Tool...")
    
    # 测试1: 生成设计系统
    print("\n=== Test 1: Generate Design System ===")
    result = generate_design_system("SaaS dashboard", "MyApp")
    print(result)
    
    # 测试2: 搜索域
    print("\n=== Test 2: Search Domain ===")
    result = search_domain("glassmorphism", "style", 3)
    print(result)
    
    # 测试3: 搜索技术栈指南
    print("\n=== Test 3: Search Stack Guidelines ===")
    result = search_stack_guidelines("form validation", "react-native", 3)
    print(result)

if __name__ == "__main__":
    test_ui_ux_pro_max()
```

#### 3. 验证CSV数据

```python
# 验证CSV文件完整性
def validate_csv_files():
    import os
    
    csv_files = [
        "products.csv",
        "styles.csv",
        "colors.csv",
        "typography.csv",
        "charts.csv",
        "landing.csv",
        "ux-guidelines.csv",
        "ui-reasoning.csv"
    ]
    
    for csv_file in csv_files:
        filepath = DATA_DIR / csv_file
        if not filepath.exists():
            print(f"❌ Missing: {csv_file}")
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                print(f"✓ {csv_file}: {len(rows)} rows")

if __name__ == "__main__":
    validate_csv_files()
```

---

## 最佳实践

### 1. 错误处理

```python
# 在工具函数中添加错误处理
def generate_design_system(query: str, project_name: str = None, output_format: str = "markdown") -> str:
    try:
        generator = DesignSystemGenerator()
        design_system = generator.generate(query, project_name)
        
        if output_format == "json":
            return json.dumps(design_system, indent=2, ensure_ascii=False)
        return format_design_system_markdown(design_system)
    
    except FileNotFoundError as e:
        return f"Error: CSV file not found - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 2. 输入验证

```python
# 添加输入验证
def validate_query(query: str) -> bool:
    """Validate search query"""
    if not query or len(query.strip()) < 2:
        return False
    return True

def validate_domain(domain: str) -> bool:
    """Validate domain parameter"""
    valid_domains = list(CSV_CONFIG.keys())
    return domain in valid_domains

def validate_stack(stack: str) -> bool:
    """Validate stack parameter"""
    return stack in AVAILABLE_STACKS
```

### 3. 性能优化

```python
# 使用缓存装饰器
@functools.lru_cache(maxsize=256)
def _load_csv_with_cache(filepath):
    """Load CSV with caching"""
    return _load_csv(filepath)

# 批量处理
def batch_search(queries: List[str], domain: str) -> List[dict]:
    """Batch search multiple queries"""
    results = []
    for query in queries:
        result = search(query, domain, max_results=3)
        results.append(result)
    return results
```

### 4. 监控和日志

```python
# 添加性能监控
import time

def generate_design_system_with_metrics(query: str, project_name: str = None) -> tuple:
    """Generate design system with performance metrics"""
    start_time = time.time()
    
    result = generate_design_system(query, project_name)
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"Design system generated in {duration:.2f}s")
    
    return result, duration
```

---

## 总结

UI/UX Pro Max可以轻松集成到Dify系统中，为LLM应用提供强大的UI/UX设计智能。

### 核心优势

1. **易于集成**: 通过Dify的自定义工具功能快速集成
2. **功能强大**: 161种产品类型、67种UI风格、161种配色方案
3. **智能推荐**: BM25搜索引擎 + 161条推理规则
4. **多技术栈**: 支持13种技术栈的特定指南
5. **灵活输出**: 支持Markdown和JSON格式

### 使用场景

- 🎨 **设计系统生成**: 为新项目生成完整的设计系统
- 🔍 **UI风格搜索**: 搜索和推荐UI风格、颜色、字体
- 📱 **技术栈指南**: 获取React、Vue、SwiftUI等技术栈的最佳实践
- ✅ **代码审查**: 验证生成的代码是否符合设计规范

### 下一步

1. 按照安装步骤集成UI/UX Pro Max到Dify
2. 创建工作流配置文件
3. 测试工具功能
4. 部署到生产环境

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
