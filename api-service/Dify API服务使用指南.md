# UI/UX Pro Max - Dify API服务使用指南

## 📋 目录

1. [概述](#概述)
2. [架构设计](#架构设计)
3. [部署步骤](#部署步骤)
4. [Dify配置](#dify配置)
5. [API端点](#api端点)
6. [使用方法](#使用方法)
7. [示例代码](#示例代码)
8. [常见问题](#常见问题)

---

## 概述

本方案提供了一种**无需在Dify服务器上部署UI/UX Pro Max项目**，就能在Dify上使用其功能的方法。

### 核心思路

创建一个**独立的FastAPI服务**，Dify通过HTTP请求调用这个API，获取设计智能。

### 优势

- ✅ **无需部署**：不需要在Dify服务器上安装任何文件
- ✅ **独立运行**：API服务可以独立运行在任何服务器上
- ✅ **完整功能**：支持所有核心功能（设计系统生成、域搜索、技术栈指南）
- ✅ **灵活调用**：Dify可以通过HTTP请求调用API
- ✅ **易于维护**：API服务独立维护，不影响Dify

---

## 架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    Dify平台                              │
│  ┌───────────────────────────────────────────┐  │
│  │  应用 (App)                              │  │
│  │  ┌─────────────────────────────────┐   │  │
│  │  │  LLM节点                        │   │  │
│  │  └─────────────────────────────────┘   │  │
│  │              │                           │   │  │
│  │              ▼                           │   │  │
│  │  ┌─────────────────────────────────┐   │  │  │
│  │  │  HTTP请求工具                  │   │  │  │
│  │  │  ┌─────────────────────────┐   │  │  │
│  │  │  │  POST /generate-design-system   │   │  │  │
│  │  │  │  请求体: DesignSystemRequest   │   │  │  │
│  │  │  │  响应体: DesignSystemResponse  │   │  │  │
│  │  │  └─────────────────────────┘   │   │  │  │
│  └─────────────────────────────────────────┘   │  │
│  │              │                           │   │  │
│  │              ▼                           │   │  │  │
│  │  ┌─────────────────────────────────┐   │   │  │
│  │  │  UI/UX Pro Max API服务          │   │  │  │
│  │  │  ┌─────────────────────────────┐   │  │  │
│  │  │  │  FastAPI                      │   │  │  │
│  │  │  │  - 设计系统生成器            │   │  │  │
│  │  │  │  - 域搜索引擎                │   │  │  │
│  │  │  │  - 技术栈指南                │   │  │  │
│  │  │  │  - CSV数据库                  │   │  │  │
│  │  │  └─────────────────────────────┘   │  │  │  │
│  └─────────────────────────────────────────┘   │  │  │
└─────────────────────────────────────────────────┘   │  │  │
└─────────────────────────────────────────────────┘   │  │
└─────────────────────────────────────────────────┘   │  │
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│              独立API服务器                            │
│  ┌───────────────────────────────────────────┐  │
│  │  FastAPI服务                            │  │
│  │  ┌─────────────────────────────────┐   │  │
│  │  │  端点:                           │  │
│  │  │  - GET /docs (API文档)          │  │
│  │  │  - POST /generate-design-system      │  │
│  │  │  - POST /search-domain               │  │
│  │  │  - POST /search-stack-guidelines      │  │
│  │  │  - POST /generate-single-file-html   │  │
│  │  └─────────────────────────────────┘   │  │
│  └─────────────────────────────────────────┘   │  │
└─────────────────────────────────────────────────┘   │  │
```

### 数据流

```
用户请求
    │
    ▼
Dify应用
    │
    ├─ LLM节点分析需求
    │
    ▼
HTTP请求工具
    │
    ├─ POST请求到API服务
    │
    ▼
UI/UX Pro Max API服务
    │
    ├─ 读取CSV数据库
    ├─ 调用Python脚本
    ├─ 生成设计系统
    ├─ 返回JSON响应
    │
    ▼
HTTP响应
    │
    └─ 返回设计系统数据
    │
    ▼
Dify应用
    │
    └─ LLM节点根据设计系统生成HTML
```

---

## 部署步骤

### 步骤1: 准备API服务

#### 1.1 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn[standard] pydantic
```

#### 1.2 启动API服务

```bash
# 进入api-service目录
cd api-service

# 启动服务
python3 api_service.py
```

服务将在 `http://0.0.0.0:8000` 启动

#### 1.3 验证API

```bash
# 访问API文档
curl http://0.0.0.0:8000/docs

# 测试API端点
curl -X POST http://0.0.0.0:8000/generate-design-system \
  -H "Content-Type: application/json" \
  -d '{"query":"SaaS dashboard","output_format":"json"}'
```

### 步骤2: 在Dify中添加HTTP请求工具

#### 2.1 创建HTTP请求工具

在Dify工作流中创建一个自定义HTTP请求工具：

```yaml
nodes:
  - id: "call_api"
    type: "tool"
    title: "调用UI/UX Pro Max API"
    description: "通过HTTP请求调用UI/UX Pro Max API服务"
    config:
      method: POST
      url: "http://0.0.0.0:8000/generate-design-system"
      headers:
        Content-Type: "application/json"
      body: |
        {
          "query": "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}",
          "project_name": "{{#analyze_requirements.output.project_name#}}",
          "output_format": "json"
        }
      response_mapping:
        success: data
        error: error
```

#### 2.2 使用HTTP请求工具

在工作流中，LLM节点可以调用HTTP请求工具：

```yaml
nodes:
  - id: "analyze_requirements"
    type: "llm"
    prompt: |
      分析用户需求，提取产品类型和风格偏好
      
      用户需求: {{#start.text#}}
      
      请以JSON格式输出：
      {
        "product_type": "...",
        "style_preference": "...",
        "project_name": "..."
      }

  - id: "get_design_system"
    type: "tool"
    title: "获取设计系统"
    config:
      method: POST
      url: "http://0.0.0.0:8000/generate-design-system"
      headers:
        Content-Type: "application/json"
      body: |
        {
          "query": "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}",
          "project_name": "{{#analyze_requirements.output.project_name#}}",
          "output_format": "json"
        }
      response_mapping:
        success: data
        error: error

  - id: "generate_html"
    type: "llm"
    prompt: |
      你是一个专业的前端开发工程师。根据以下设计系统生成HTML代码。
      
      ## 设计系统
      {{#get_design_system.output.data#}}
      
      请生成完整的HTML代码。
```

---

## Dify配置

### 配置HTTP请求工具

#### 选项1: 使用内置HTTP请求工具

Dify支持内置的HTTP请求工具，可以直接使用。

**配置示例**:
```yaml
nodes:
  - id: "call_api"
    type: "tool"
    title: "调用UI/UX Pro Max API"
    description: "通过HTTP请求调用UI/UX Pro Max API服务"
    config:
      method: POST
      url: "http://0.0.0.0:8000/generate-design-system"
      headers:
        Content-Type: "application/json"
      body: |
        {
          "query": "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}",
          "project_name": "{{#analyze_requirements.output.project_name#}}",
          "output_format": "json"
        }
      response_mapping:
        success: data
        error: error
```

#### 选项2: 使用自定义代码节点

如果需要更复杂的逻辑，可以创建自定义代码节点：

```yaml
nodes:
  - id: "call_api_with_logic"
    type: "code"
    title: "调用API并处理响应"
    executor:
      type: "python"
      config:
        code: |
          import requests
          import json
          
          # 调用API
          url = "http://0.0.0.0:8000/generate-design-system"
          payload = {
              "query": "{{#query#}}",
              "project_name": "{{#project_name#}}",
              "output_format": "json"
          }
          
          response = requests.post(url, json=payload)
          
          # 输出响应
          print(json.dumps(response.json(), indent=2))
```

---

## API端点

### 1. GET /docs

**说明**: API文档

**响应**:
```json
{
  "name": "UI/UX Pro Max API",
  "version": "1.0.0",
  "description": "AI-powered UI/UX design intelligence for building professional UI/UX",
  "endpoints": {
    "/docs": "API文档",
    "/generate-design-system": "生成设计系统",
    "/search-domain": "搜索域",
    "/search-stack-guidelines": "搜索技术栈指南",
    "/generate-single-file-html": "生成单文件HTML"
  }
}
```

### 2. POST /generate-design-system

**说明**: 生成设计系统

**请求体**:
```json
{
  "query": "SaaS dashboard",
  "project_name": "MyApp",
  "output_format": "json"
}
```

**响应体**:
```json
{
  "success": true,
  "data": {
    "project_name": "MyApp",
    "pattern": {
      "name": "Hero + Features + CTA",
      "sections": "1. Hero, 2. Value prop, 3. Key features, 4. CTA, 5. Footer"
    },
    "style": {
      "name": "Soft UI Evolution",
      "type": "General",
      "keywords": "Evolved soft UI, better contrast, modern aesthetics",
      "best_for": "Modern enterprise apps, SaaS platforms, health/wellness"
    },
    "colors": {
      "primary": "#2563EB",
      "secondary": "#3B82F6",
      "cta": "#F97316",
      "background": "#F8FAFC",
      "text": "#1E293B"
    },
    "typography": {
      "heading": "Lora",
      "body": "Raleway",
      "google_fonts_url": "https://fonts.google.com/share?selection?family=..."
    },
    "key_effects": "Subtle hover (200-250ms)",
    "anti_patterns": "Excessive animation + Dark mode by default"
  },
  "error": null
}
```

### 3. POST /search-domain

**说明**: 搜索域

**请求体**:
```json
{
  "query": "glassmorphism",
  "domain": "style",
  "max_results": 5,
  "output_format": "json"
}
```

**响应体**:
```json
{
  "success": true,
  "domain": "style",
  "query": "glassmorphism",
  "count": 5,
  "results": [
    {
      "Style Category": "Glassmorphism",
      "Type": "General",
      "Keywords": "Glassmorphism, soft shadows, blur, translucent, modern",
      "Primary Colors": "Monochromatic, Black #000000",
      "Secondary Colors": "Neutral (Beige #F5F1E8)",
      "Effects & Animation": "Subtle hover (200-250ms)"
      "Best For": "Modern dashboards, SaaS platforms",
      "Performance": "⚡ Excellent",
      "Accessibility": "✓ WCAG AAA"
    },
    ...
  ],
  "error": null
}
```

### 4. POST /search-stack-guidelines

**说明**: 搜索技术栈指南

**请求体**:
```json
{
  "query": "form validation",
  "stack": "react-native",
  "max_results": 3,
  "output_format": "json"
}
```

**响应体**:
```json
{
  "success": true,
  "domain": "react-native",
  "query": "form validation",
  "count": 3,
  "results": [
    {
      "Category": "Components",
      "Guideline": "Use functional components",
      "Description": "Hooks-based components are standard",
      "Do": "Functional components with hooks",
      "Don't": "Class components",
      "Code Good": "const App = () => { }",
      "Code Bad": "class App extends Component",
      "Severity": "Medium",
      "Docs URL": "https://reactnative.dev/docs/intro-react"
    },
    ...
  ],
  "error": null
}
```

### 5. POST /generate-single-file-html

**说明**: 生成单文件HTML

**请求体**:
```json
{
  "design_system_file": "design_system.json",
  "project_name": "MyApp"
}
```

**响应体**:
```json
{
  "success": true,
  "html": "<!DOCTYPE html>...",
  "error": null
}
```

---

## 使用方法

### 方法1: 使用内置HTTP请求工具

#### 步骤1: 创建工作流

1. 登录Dify管理后台
2. 点击"创建应用"
3. 选择"聊天助手（Chatbot）"
4. 点击"工具"
5. 点击"添加自定义工具"
6. 配置HTTP请求工具

**配置示例**:
```yaml
title: "UI/UX设计助手"
description: "使用UI/UX Pro Max API生成设计系统"

nodes:
  - id: "start"
    type: "start"
    data:
      title: "开始"
      desc: "用户输入设计需求"

  - id: "analyze_requirements"
    type: "llm"
    prompt: |
      分析用户需求，提取产品类型和风格偏好
      
      用户需求: {{#start.text#}}
      
      请以JSON格式输出：
      {
        "product_type": "...",
        "style_preference": "...",
        "project_name": "..."
      }

  - id: "get_design_system"
    type: "tool"
    title: "获取设计系统"
    config:
      method: POST
      url: "http://0.0.0.0:8000/generate-design-system"
      headers:
        Content-Type: "application/json"
      body: |
        {
          "query": "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}",
          "project_name": "{{#analyze_requirements.output.project_name#}}",
          "output_format": "json"
        }
      response_mapping:
        success: data
        error: error

  - id: "generate_html"
    type: "llm"
    prompt: |
      你是一个专业的前端开发工程师。根据以下设计系统生成HTML代码。
      
      ## 设计系统
      {{#get_design_system.output.data#}}
      
      请生成完整的HTML代码。

  - id: "end"
    type: "end"
    data:
      title: "结束"
      outputs:
        - title: "HTML代码"
          value: "{{#generate_html.text#}}"

edges:
  - source: "start"
    target: "analyze_requirements"
  - source: "analyze_requirements"
    target: "get_design_system"
  - source: "get_design_system"
    target: "generate_html"
  - source: "generate_html"
    target: "end"
```

#### 步骤2: 测试工作流

1. 点击"运行工作流"
2. 输入测试需求
3. 查看输出结果

### 方法2: 使用自定义代码节点

#### 步骤1: 创建代码节点

1. 在Dify工作流中添加代码节点
2. 配置代码执行器为Python
3. 编写调用API的代码

**代码示例**:
```python
import requests
import json

# 调用API
url = "http://0.0.0.0:8000/generate-design-system"
payload = {
    "query": "{{#query#}}",
    "project_name": "{{#project_name#}}",
    "output_format": "json"
}

response = requests.post(url, json=payload)

# 输出响应
print(json.dumps(response.json(), indent=2))
```

#### 步骤2: 在工作流中使用

1. 在工作流中添加代码节点
2. 配置输入变量
3. 测试运行

---

## 示例代码

### 完整的工作流示例

```yaml
title: "UI/UX设计助手"
description: "使用UI/UX Pro Max API生成设计系统"

nodes:
  - id: "start"
    type: "start"
    data:
      title: "开始"
      desc: "用户输入设计需求"

  - id: "analyze_requirements"
    type: "llm"
    prompt: |
      分析用户需求，提取产品类型和风格偏好
      
      用户需求: {{#start.text#}}
      
      请以JSON格式输出：
      {
        "product_type": "...",
        "style_preference": "...",
        "project_name": "..."
      }

  - id: "get_design_system"
    type: "tool"
    title: "获取设计系统"
    config:
      method: POST
      url: "http://0.0.0.0:8000/generate-design-system"
      headers:
        Content-Type: "application/json"
      body: |
        {
          "query": "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}",
          "project_name": "{{#analyze_requirements.output.project_name#}}",
          "output_format": "json"
        }
      response_mapping:
        success: data
        error: error

  - id: "generate_html"
    type: "llm"
    prompt: |
      你是一个专业的前端开发工程师。根据以下设计系统生成HTML代码。
      
      ## 设计系统
      {{#get_design_system.output.data#}}
      
      请生成完整的HTML代码，包括：
      1. HTML5语义结构
      2. Tailwind CSS样式（内联）
      3. 响应式设计
      4. 无障碍支持
      5. SEO优化
      6. 性能优化

  - id: "end"
    type: "end"
    data:
      title: "结束"
      outputs:
        - title: "HTML代码"
          value: "{{#generate_html.text#}}"

edges:
  - source: "start"
    target: "analyze_requirements"
  - source: "analyze_requirements"
    target: "get_design_system"
  - source: "get_design_system"
    target: "generate_html"
  - source: "generate_html"
    target: "end"
```

### 自定义代码节点示例

```python
import requests
import json

def main():
    # 获取输入
    query = "{{#query#}}"
    project_name = "{{#project_name#}}"
    
    # 调用API
    url = "http://0.0.0.0:8000/generate-design-system"
    payload = {
        "query": query,
        "project_name": project_name,
        "output_format": "json"
    }
    
    response = requests.post(url, json=payload)
    
    # 输出响应
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    main()
```

---

## 常见问题

### Q1: API服务无法启动？

**A**: 
1. 检查端口占用
```bash
lsof -i :8000
```
2. 检查依赖是否安装
```bash
pip list | grep -E "fastapi|uvicorn"
```
3. 检查防火墙设置

### Q2: Dify无法连接到API服务？

**A**: 
1. 检查API服务是否运行
```bash
curl http://0.0.0.0:8000/docs
```
2. 检查网络连接
```bash
ping 0.0.0.0
```
3. 检查Dify网络设置

### Q3: HTTP请求工具返回错误？

**A**: 
1. 检查API服务日志
2. 检查请求体格式
3. 检查API端点URL是否正确

### Q4: 响应数据不完整？

**A**: 
1. 检查API服务返回的JSON结构
2. 检查CSV文件是否存在
3. 检查Python脚本语法

---

## 总结

UI/UX Pro Max可以通过**独立的API服务**在Dify上使用，无需部署任何文件。

### 核心优势

1. ✅ **无需部署**：不需要在Dify服务器上安装任何文件
2. ✅ **独立运行**：API服务可以独立运行在任何服务器上
3. ✅ **完整功能**：支持所有核心功能
4. ✅ **灵活调用**：Dify可以通过HTTP请求调用API
5. ✅ **易于维护**：API服务独立维护

### 使用场景

- 需要快速集成设计智能功能
- 不想在Dify上部署复杂的项目
- 需要在多个Dify实例中使用同一服务
- 需要独立运行API服务

### 下一步

1. 按照部署步骤启动API服务
2. 在Dify中添加HTTP请求工具
3. 测试工作流
4. 开始使用

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
