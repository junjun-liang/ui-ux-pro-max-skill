# UI/UX Pro Max - Dify代码执行节点使用指南

## 📋 目录

1. [概述](#概述)
2. [实现方案](#实现方案)
3. [部署步骤](#部署步骤)
4. [使用方法](#使用方法)
5. [工具列表](#工具列表)
6. [常见问题](#常见问题)

---

## 概述

UI/UX Pro Max可以作为Dify的**代码执行节点（Code Execution Node）**来使用，提供4个核心代码执行工具。

### 什么是代码执行节点？

**代码执行节点**是指：
- ✅ 可以执行任意Python代码
- ✅ 可以读写文件
- ✅ 可以安装依赖
- ✅ 可以运行系统命令
- ✅ 在独立环境中运行

### 与工具节点的区别

| 特性 | 工具节点 | 代码执行节点 |
|------|----------|--------------|
| **执行方式** | Python脚本 | Shell命令 |
| **输入输出** | JSON/Markdown | 标准输出/文件 |
| **文件访问** | 只读 | 读写 |
| **环境隔离** | 共享环境 | 独立环境 |
| **适用场景** | 数据处理、搜索 | 脚本执行、文件操作 |

---

## 实现方案

### 方案1: 直接改造为代码执行节点（推荐）

#### 优点
- ✅ **完全控制**：可以执行任意Python代码
- ✅ **可读写文件**：可以读取CSV文件、写入设计系统到文件
- ✅ **可安装依赖**：如果需要额外的Python库，可以动态安装
- ✅ **更好的隔离**：代码执行节点在独立环境中运行，不会影响Dify API
- ✅ **灵活性**：可以执行复杂的文件操作、系统命令

#### 缺点
- ❌ 需要修改现有配置
- ❌ 需要创建新的提供者配置
- ❌ 需要重新部署

#### 适用场景
- 需要执行复杂的Python脚本
- 需要读写文件
- 需要安装依赖
- 需要运行系统命令

---

### 方案2: 保持工具节点，添加代码执行功能

#### 优点
- ✅ **保持灵活性**：可以在工具节点中调用代码执行
- ✅ **混合使用**：可以同时使用工具和代码执行
- ✅ **无需修改**：保持现有工具节点结构
- ✅ **快速部署**：无需重新部署

#### 缺点
- ❌ 功能受限：代码执行功能受限
- ❌ 无法读写文件：只能在工具环境中执行
- ❌ 无法安装依赖：无法动态安装Python库

#### 适用场景
- 主要使用工具节点功能
- 偶尔需要代码执行辅助
- 不需要复杂的文件操作

---

## 部署步骤

### 方案1部署步骤

#### 步骤1: 创建代码执行提供者配置

创建新的配置文件 `code-execution.yaml`：

```yaml
identity:
  name: "ui_ux_pro_max_code"
  author: "UI/UX Pro Max Team"
  label:
    en_US: "UI/UX Pro Max Code"
    zh_Hans: "UI/UX Pro Max 代码执行"
  description:
    en_US: "Code execution node for UI/UX design intelligence. Execute Python scripts for design system generation, domain search, and stack guidelines."
    zh_Hans: "UI/UX设计智能代码执行节点。执行Python脚本生成设计系统、域搜索和技术栈指南。"
  icon: "🎨"
  tags: ["design", "ui", "ux", "code-execution", "python"]

supported_model_types: ["llm"]
configurate_methods: ["no-configuration"]
provider_credential_schema:
  type: "none"
```

#### 步骤2: 创建代码执行工具定义

创建新的配置文件 `code-execution-tools.yaml`：

```yaml
tools:
  - identity:
      name: "generate_design_system"
      author: "UI/UX Pro Max Team"
      label:
        en_US: "Generate Design System"
        zh_Hans: "生成设计系统"
    parameters:
      query:
        type: "string"
        required: true
      project_name:
        type: "string"
        required: false
      output_format:
        type: "string"
        enum: ["markdown", "json"]
        default: "markdown"
    executor:
      type: "python"
      config:
        code: |
          import sys
          import json
          from pathlib import Path
          
          # 读取设计系统
          design_system_file = sys.argv[1] if len(sys.argv) > 1 else "design_system.json"
          
          with open(design_system_file, 'r', encoding='utf-8') as f:
              design_system = json.load(f.read())
          
          # 输出设计系统
          print(json.dumps(design_system, indent=2, ensure_ascii=False))

  - identity:
      name: "search_domain"
      author: "UI/UX Pro Max Team"
      label:
        en_US: "Search Domain"
        zh_Hans: "搜索域"
    parameters:
      query:
        type: "string"
        required: true
      domain:
        type: "string"
        enum: ["style", "color", "typography", "chart", "landing", "product", "ux", "google-fonts", "icons", "react", "web"]
      max_results:
        type: "integer"
        default: 3
        minimum: 1
        maximum: 10
      output_format:
        type: "string"
        enum: ["markdown", "json"]
        default: "markdown"
    executor:
      type: "python"
      config:
        code: |
          import sys
          import json
          from pathlib import Path
          
          # 导入搜索函数
          sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
          from search import search
          
          # 搜索域
          query = sys.argv[1]
          domain = sys.argv[2] if len(sys.argv) > 2 else None
          max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 3
          output_format = sys.argv[4] if len(sys.argv) > 4 else "markdown"
          
          result = search(query, domain, max_results)
          
          # 输出结果
          print(json.dumps(result, indent=2, ensure_ascii=False))

  - identity:
      name: "search_stack_guidelines"
      author: "UI/UX Pro Max Team"
      label:
        en_US: "Search Stack Guidelines"
        zh_Hans: "搜索技术栈指南"
    parameters:
      query:
        type: "string"
        required: true
      stack:
        type: "string"
        enum: ["html-tailwind", "react", "nextjs", "vue", "nuxtjs", "nuxt-ui", "svelte", "astro", "swiftui", "react-native", "flutter", "shadcn", "jetpack-compose"]
      max_results:
        type: "integer"
        default: 3
        minimum: 1
        maximum: 10
      output_format:
        type: "string"
        enum: ["markdown", "json"]
        default: "markdown"
    executor:
      type: "python"
      config:
        code: |
          import sys
          import json
          from pathlib import Path
          
          # 导入搜索函数
          sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
          from search import search_stack_guidelines
          
          # 搜索技术栈指南
          query = sys.argv[1]
          stack = sys.argv[2]
          max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 3
          output_format = sys.argv[4] if len(sys.argv) > 4 else "markdown"
          
          result = search_stack_guidelines(query, stack, max_results)
          
          # 输出结果
          print(json.dumps(result, indent=2, ensure_ascii=False))

  - identity:
      name: "generate_single_file_html"
      author: "UI/UX Pro Max Team"
      label:
        en_US: "Generate Single File HTML"
        zh_Hans: "生成单文件HTML"
    parameters:
      design_system_file:
        type: "string"
        required: true
      project_name:
        type: "string"
        required: false
    executor:
      type: "python"
      config:
        code: |
          import sys
          import json
          from pathlib import Path
          
          # 读取设计系统
          with open(sys.argv[1], 'r', encoding='utf-8') as f:
              design_system = json.load(f.read())
          
          # 提取设计系统信息
          project_name = design_system.get("project_name", sys.argv[2] if len(sys.argv) > 2 else "MyApp")
          pattern = design_system.get("pattern", {})
          style = design_system.get("style", {})
          colors = design_system.get("colors", {})
          typography = design_system.get("typography", {})
          
          # 生成Single File HTML代码
          html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="{project_name} - 专业设计">
    <meta name="keywords" content="{project_name.lower()}, design, ui, ux">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typography.get('google_fonts_url', '')}" rel="stylesheet">
    
    <style>
        /* Tailwind Config */
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '{colors.get('primary', '#2563EB')}',
                        secondary: '{colors.get('secondary', '#3B82F6')}',
                        cta: '{colors.get('cta', '#F97316')}',
                        background: '{colors.get('background', '#F8FAFC')}',
                        text: '{colors.get('text', '#1E293B')}',
                    }},
                    fontFamily: {{
                        heading: ['{typography.get('heading', 'Inter')}', 'serif'],
                        body: ['{typography.get('body', 'Inter')}', 'sans-serif'],
                    }},
                }},
            }}
        }}
    </style>
</head>
<body class="bg-background text-text">
    <!-- Hero Section -->
    <section class="min-h-screen flex items-center justify-center">
        <div class="container mx-auto px-4 text-center">
            <h1 class="font-heading text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-text mb-6">
                {project_name}
            </h1>
            <p class="font-body text-lg sm:text-xl md:text-2xl text-text/80 mb-8 max-w-3xl mx-auto">
                {pattern.get('description', '专业的解决方案')}
            </p>
            <button class="bg-cta text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-cta/90 transition-colors duration-200">
                立即开始
            </button>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="py-16 bg-white">
        <div class="container mx-auto px-4">
            <h2 class="font-heading text-3xl sm:text-4xl font-bold text-text text-center mb-12">
                核心功能
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="bg-background rounded-xl p-8 shadow-lg">
                    <h3 class="font-heading text-xl font-semibold text-primary mb-3">功能1</h3>
                    <p class="font-body text-text/70">功能1的详细说明</p>
                </div>
                <div class="bg-background rounded-xl p-8 shadow-lg">
                    <h3 class="font-heading text-xl font-semibold text-primary mb-3">功能2</h3>
                    <p class="font-body text-text/70">功能2的详细说明</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="bg-text py-8">
        <div class="container mx-auto px-4 text-center">
            <p class="font-body text-white/80">
                © 2024 {project_name}. All rights reserved.
            </p>
        </div>
    </footer>
</body>
</html>
"""
          
          # 输出HTML代码
          print(html)
```

#### 步骤3: 复制文件到Dify容器

```bash
# 复制代码执行配置文件
docker cp code-execution.yaml dify-api-1:/app/api/core/tools/provider/builtin/
docker cp code-execution-tools.yaml dify-api-1:/app/api/core/tools/provider/builtin/

# 重启API服务
docker restart dify-api-1
```

#### 步骤4: 在Dify中添加代码执行节点

1. 登录Dify管理后台
2. 点击"创建应用"
3. 选择"聊天助手（Chatbot）"或"工作流（Workflow）"
4. 点击"工具"
5. 点击"添加自定义工具"
6. 选择"UI/UX Pro Max Code"
7. 配置工具（如果需要）

---

### 方案2部署步骤

#### 步骤1: 修改现有工具节点配置

在 `tools.yaml` 中为现有工具添加代码执行支持：

```yaml
tools:
  - identity:
      name: "generate_design_system"
      # ... 其他参数保持不变
    executor:
      type: "python"
      config:
        code: |
          # ... 代码执行配置
```

#### 步骤2: 重启Dify API服务

```bash
docker restart dify-api-1
```

#### 步骤3: 在Dify中使用

1. 登录Dify管理后台
2. 创建或编辑应用
3. 在工作流中添加工具节点
4. 调用工具，选择"代码执行"选项

---

## 使用方法

### 方案1使用示例

#### 示例1: 生成设计系统

**Dify工作流**:
```
开始 → LLM分析需求 → 代码执行节点(generate_design_system) → LLM生成HTML → 结束
```

**工具调用**:
```json
{
  "query": "SaaS dashboard",
  "project_name": "MyApp",
  "output_format": "markdown"
}
```

**输出**: 完整的设计系统（JSON格式）

#### 示例2: 搜索域

**Dify工作流**:
```
开始 → LLM识别搜索需求 → 代码执行节点(search_domain) → LLM总结结果 → 结束
```

**工具调用**:
```json
{
  "query": "glassmorphism",
  "domain": "style",
  "max_results": 5,
  "output_format": "markdown"
}
```

**输出**: 搜索结果（JSON格式）

#### 示例3: 生成单文件HTML

**Dify工作流**:
```
开始 → LLM分析需求 → 工具节点(generate_design_system) → 代码执行节点(generate_single_file_html) → LLM生成HTML → 结束
```

**工具调用**:
```json
{
  "design_system_file": "design_system.json",
  "project_name": "MyApp"
}
```

**输出**: 完整的HTML代码

---

### 方案2使用示例

#### 示例1: 生成设计系统（工具节点）

**Dify工作流**:
```
开始 → LLM分析需求 → 工具节点(generate_design_system) → LLM生成HTML → 结束
```

**工具调用**:
```json
{
  "query": "SaaS dashboard",
  "project_name": "MyApp",
  "output_format": "markdown"
}
```

**输出**: 完整的设计系统（JSON格式）

#### 示例2: 搜索域（工具节点）

**Dify工作流**:
```
开始 → LLM识别搜索需求 → 工具节点(search_domain) → LLM总结结果 → 结束
```

**工具调用**:
```json
{
  "query": "glassmorphism",
  "domain": "style",
  "max_results": 5,
  "output_format": "markdown"
}
```

**输出**: 搜索结果（JSON格式）

---

## 工具列表

### 代码执行节点工具

| 工具名称 | 说明 | 参数 |
|----------|------|------|
| **generate_design_system** | 生成设计系统 | query, project_name, output_format |
| **search_domain** | 搜索域 | query, domain, max_results, output_format |
| **search_stack_guidelines** | 搜索技术栈指南 | query, stack, max_results, output_format |
| **generate_single_file_html** | 生成单文件HTML | design_system_file, project_name |

### 工具节点工具

| 工具名称 | 说明 | 参数 |
|----------|------|------|
| **generate_design_system** | 生成设计系统 | query, project_name, output_format |
| **search_domain** | 搜索域 | query, domain, max_results, output_format |
| **search_stack_guidelines** | 搜索技术栈指南 | query, stack, max_results, output_format |

---

## 常见问题

### Q1: 代码执行节点未显示在Dify中？

**A**: 
1. 检查配置文件是否存在
```bash
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/code-execution*
```
2. 重启API服务
```bash
docker restart dify-api-1
```

### Q2: 工具调用失败？

**A**: 
1. 检查Python脚本语法
```bash
docker exec dify-api-1 python3 -m py_compile code-execution-tools.yaml
```
2. 检查依赖
```bash
docker exec dify-api-1 pip list | grep -E "csv|json|pathlib"
```

### Q3: 无法读写文件？

**A**: 
1. 检查文件权限
```bash
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
```
2. 检查数据目录路径
```bash
docker exec dify-api-1 cat /app/api/core/tools/provider/builtin/ui_ux_pro_max/ui_ux_pro_max.py | grep DATA_DIR
```

### Q4: 代码执行超时？

**A**: 
1. 检查执行时间限制
2. 优化Python脚本性能
3. 减少数据量

---

## 总结

UI/UX Pro Max可以作为Dify的**代码执行节点**来使用，提供4个核心代码执行工具：

### 核心工具

1. **generate_design_system** - 生成设计系统
2. **search_domain** - 搜索域
3. **search_stack_guidelines** - 搜索技术栈指南
4. **generate_single_file_html** - 生成单文件HTML

### 推荐方案

**方案1: 直接改造为代码执行节点**（推荐）
- ✅ 完全控制
- ✅ 可读写文件
- ✅ 可安装依赖
- ✅ 更好的隔离

**方案2: 保持工具节点，添加代码执行功能**
- ✅ 保持灵活性
- ✅ 无需修改
- ✅ 快速部署

### 下一步

1. 选择实现方案
2. 按照部署步骤操作
3. 在Dify中测试工具
4. 开始使用

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
