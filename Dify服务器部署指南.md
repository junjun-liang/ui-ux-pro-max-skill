# UI/UX Pro Max - Dify服务器部署指南

## 📋 目录

1. [概述](#概述)
2. [部署方式](#部署方式)
3. [Docker部署步骤](#docker部署步骤)
4. [本地开发部署步骤](#本地开发部署步骤)
5. [配置工具节点](#配置工具节点)
6. [测试工具功能](#测试工具功能)
7. [常见问题](#常见问题)

---

## 概述

本指南详细说明如何在Dify服务器上部署UI/UX Pro Max项目，让LLM可以把它作为工具调用。

### 部署方式对比

| 方式 | 部署难度 | 功能完整度 | 灵活性 | 推荐度 |
|------|----------|------------|----------|--------|
| **方式1: Docker部署（推荐）** | 中 | ⭐⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **方式2: 本地开发部署** | 低 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 推荐使用方式1

**理由**：
1. ✅ **功能完整**：支持所有核心功能（设计系统生成、域搜索、技术栈指南）
2. ✅ **Dify原生**：使用Dify的工具节点机制，无需额外配置
3. ✅ **易于维护**：遵循Dify的部署规范
4. ✅ **生产就绪**：适合生产环境部署

---

## 部署方式

### 方式1: Docker部署（推荐）

#### 优点
- ✅ 生产就绪
- ✅ 功能完整
- ✅ 易于维护
- ✅ 遵循Dify规范

#### 缺点
- 需要Docker环境
- 部署相对复杂

---

### 方式2: 本地开发部署

#### 优点
- ✅ 开发便捷
- ✅ 调试方便
- ✅ 无需Docker

#### 缺点
- 功能受限（只能使用工具节点）
- 不适合生产环境

---

## Docker部署步骤

### 步骤1: 准备部署文件

#### 1.1 创建部署目录

```bash
# 在项目根目录创建部署目录
mkdir -p deploy-dify
cd deploy-dify
```

#### 1.2 复制核心文件

```bash
# 复制Python脚本
cp ../src/ui-ux-pro-max/scripts/*.py .

# 复制CSV数据文件
cp -r ../src/ui-ux-pro-max/data/*.csv data/

# 复制stacks数据文件
cp -r ../src/ui-ux-pro-max/data/stacks/*.csv data/stacks/
```

#### 1.3 创建Dify工具配置

创建 `dify-tool.yaml`：

```yaml
identity:
  name: "ui_ux_pro_max"
  author: "UI/UX Pro Max Team"
  label:
    en_US: "UI/UX Pro Max"
    zh_Hans: "UI/UX Pro Max 设计智能"
  description:
    en_US: "AI-powered design intelligence for building professional UI/UX. Generate design systems, search UI styles, colors, typography, and UX guidelines."
    zh_Hans: "AI驱动的UI/UX设计智能工具。生成设计系统、搜索UI风格、配色、字体和UX指南。"
  icon: "🎨"
  tags: ["design", "ui", "ux", "frontend", "web", "mobile"]

supported_model_types: ["llm"]
configurate_methods: ["no-configuration"]
provider_credential_schema:
  type: "none"
```

创建 `dify-tools.yaml`：

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
          sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
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
          sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
          from search import search_stack_guidelines
          
          # 搜索技术栈指南
          query = sys.argv[1]
          stack = sys.argv[2]
          max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 3
          output_format = sys.argv[4] if len(sys.argv) > 4 else "markdown"
          
          result = search_stack_guidelines(query, stack, max_results)
          
          # 输出结果
          print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 步骤2: 进入Dify容器

```bash
# 查看Dify容器
docker ps | grep dify

# 进入API容器
docker exec -it dify-api-1 bash
```

### 步骤3: 创建工具目录

```bash
# 在Dify容器中创建工具目录
mkdir -p /app/api/core/tools/provider/builtin/ui_ux_pro_max
```

### 步骤4: 复制文件到Dify容器

#### 方法1: 使用docker cp

```bash
# 退出Dify容器
exit

# 从宿主机复制文件
docker cp deploy-dify/*.py dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp deploy-dify/data/*.csv dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
docker cp -r deploy-dify/data/stacks/*.csv dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/data/stacks/
docker cp deploy-dify/dify-tool.yaml dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp deploy-dify/dify-tools.yaml dify-api-1:/app/api/core/tools/provider/builtin/ui_ux_pro_max/

# 重新进入Dify容器
docker exec -it dify-api-1 bash
```

#### 方法2: 使用docker exec（推荐）

```bash
# 在宿主机执行
docker exec dify-api-1 bash -c "
    mkdir -p /app/api/core/tools/provider/builtin/ui_ux_pro_max
    mkdir -p /app/api/core/tools/provider/builtin/ui_ux_pro_max/data
    mkdir -p /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/stacks
"

# 复制文件
docker cp deploy-dify/*.py /app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp deploy-dify/data/*.csv /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
docker cp -r deploy-dify/data/stacks/*.csv /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/stacks/
docker cp deploy-dify/dify-tool.yaml /app/api/core/tools/provider/builtin/ui_ux_pro_max/
docker cp deploy-dify/dify-tools.yaml /app/api/core/tools/provider/builtin/ui_ux_pro_max/
```

### 步骤5: 设置文件权限

```bash
# 设置Python脚本权限
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.py

# 设置配置文件权限
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.yaml

# 设置数据目录权限
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/*.csv
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/stacks
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/stacks/*.csv
```

### 步骤6: 重启API服务

```bash
# 重启Dify API服务
docker restart dify-api-1

# 等待服务启动
sleep 10

# 检查服务状态
docker ps | grep dify-api
```

---

## 本地开发部署步骤

### 步骤1: 克隆Dify仓库

```bash
# 克隆Dify仓库
git clone https://github.com/langgenius/dify.git
cd dify
```

### 步骤2: 安装依赖

```bash
# 进入API目录
cd api

# 安装Python依赖
pip install -r requirements.txt

# 安装UI/UX Pro Max依赖（如果需要）
pip install csv
```

### 步骤3: 创建工具目录

```bash
# 创建工具目录
mkdir -p core/tools/provider/builtin/ui_ux_pro_max
```

### 步骤4: 复制文件

```bash
# 复制Python脚本
cp ../../../ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/*.py core/tools/provider/builtin/ui_ux_pro_max/

# 复制CSV数据文件
cp ../../../ui-ux-pro-max-skill/src/ui-ux-pro-max/data/*.csv core/tools/provider/builtin/ui_ux_pro_max/data/

# 复制stacks数据文件
cp -r ../../../ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/*.csv core/tools/provider/builtin/ui_ux_pro_max/data/stacks/

# 复制配置文件
cp ../../../ui-ux-pro-max-skill/dify-integration/dify-tool.yaml core/tools/provider/builtin/ui_ux_pro_max/
cp ../../../ui-ux-pro-max-skill/dify-integration/dify-tools.yaml core/tools/provider/builtin/ui_ux_pro_max/
```

### 步骤5: 启动API服务

```bash
# 启动Dify API服务
cd api
python main.py
```

---

## 配置工具节点

### 步骤1: 在Dify中添加工具

1. 登录Dify管理后台
2. 点击"创建应用"或"工作流"
3. 点击"工具"
4. 点击"添加自定义工具"
5. 选择"UI/UX Pro Max"
6. 配置工具参数（如果需要）

### 步骤2: 验证工具配置

1. 点击"UI/UX Pro Max"工具
2. 查看工具配置
3. 确认所有参数正确

### 步骤3: 测试工具功能

1. 创建测试工作流
2. 添加工具节点
3. 输入测试参数
4. 运行工作流
5. 查看输出结果

---

## 测试工具功能

### 测试1: 生成设计系统

**工作流配置**:
```yaml
title: "测试设计系统生成"
description: "测试UI/UX Pro Max的设计系统生成功能"

nodes:
  - id: "test_generate"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      测试UI/UX Pro Max的设计系统生成功能。
      
      请调用UI/UX Pro Max工具，查询"SaaS dashboard"，生成设计系统。

  - id: "check_output"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      检查设计系统输出是否包含必要信息：
      - Pattern
      - Style
      - Colors
      - Typography
      - Key Effects
      - Anti-Patterns
```

**工具调用**:
```yaml
nodes:
  - id: "test_generate"
    type: "tool"
    provider: "ui_ux_pro_max"
    tool: "generate_design_system"
    parameters:
      query: "SaaS dashboard"
      project_name: "TestApp"
      output_format: "markdown"
```

### 测试2: 搜索域

**工作流配置**:
```yaml
title: "测试域搜索"
description: "测试UI/UX Pro Max的域搜索功能"

nodes:
  - id: "test_search"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      测试UI/UX Pro Max的域搜索功能。
      
      请调用UI/UX Pro Max工具，搜索"glassmorphism"风格。

  - id: "check_results"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      检查搜索结果是否包含相关风格。
```

**工具调用**:
```yaml
nodes:
  - id: "test_search"
    type: "tool"
    provider: "ui_ux_pro_max"
    tool: "search_domain"
    parameters:
      query: "glassmorphism"
      domain: "style"
      max_results: 3
      output_format: "markdown"
```

### 测试3: 搜索技术栈指南

**工作流配置**:
```yaml
title: "测试技术栈指南搜索"
description: "测试UI/UX Pro Max的技术栈指南搜索功能"

nodes:
  - id: "test_stack"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      测试UI/UX Pro Max的技术栈指南搜索功能。
      
      请调用UI/UX Pro Max工具，搜索React Native的表单验证指南。

  - id: "check_results"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      检查搜索结果是否包含相关指南。
```

**工具调用**:
```yaml
nodes:
  - id: "test_stack"
    type: "tool"
    provider: "ui_ux_pro_max"
    tool: "search_stack_guidelines"
    parameters:
      query: "form validation"
      stack: "react-native"
      max_results: 3
      output_format: "markdown"
```

---

## 常见问题

### Q1: 工具未显示在Dify中？

**A**: 
1. 检查工具目录是否存在
```bash
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/
```
2. 检查配置文件是否存在
```bash
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.yaml
```
3. 重启API服务
```bash
docker restart dify-api-1
```

### Q2: 工具调用失败？

**A**: 
1. 检查Python脚本语法
```bash
docker exec dify-api-1 python3 -m py_compile /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.py
```
2. 检查依赖
```bash
docker exec dify-api-1 pip list | grep -E "csv|json|pathlib"
```
3. 检查数据文件
```bash
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/
```

### Q3: 搜索无结果？

**A**: 
1. 检查查询关键词
2. 尝试不同的域
3. 增加max_results参数
4. 检查CSV文件是否完整

### Q4: 文件权限错误？

**A**: 
```bash
# 设置正确的权限
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.py
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/*.yaml
chmod 755 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data
chmod 644 /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/*.csv
```

### Q5: 本地开发部署后工具未显示？

**A**: 
1. 确认文件已复制到正确位置
2. 重启API服务
3. 清除缓存
```bash
cd api
rm -rf __pycache__
python main.py
```

---

## 部署检查清单

### 部署前检查

- [ ] 所有Python脚本已复制
- [ ] 所有CSV数据文件已复制
- [ ] 所有stacks数据文件已复制
- [ ] 配置文件已复制
- [ ] 文件权限已设置
- [ ] 工具目录已创建

### 部署后检查

- [ ] 工具在Dify中显示
- [ ] 工具配置正确
- [ ] 工具调用成功
- [ ] 输出结果正确
- [ ] 所有功能测试通过

---

## 最佳实践

### 1. 文件组织

```
deploy-dify/
├── scripts/           # Python脚本
│   ├── search.py
│   ├── design_system.py
│   └── ...
├── data/             # CSV数据文件
│   ├── products.csv
│   ├── styles.csv
│   ├── colors.csv
│   ├── typography.csv
│   ├── ui-reasoning.csv
│   ├── charts.csv
│   ├── landing.csv
│   ├── ux-guidelines.csv
│   ├── google-fonts.csv
│   ├── icons.csv
│   ├── app-interface.csv
│   ├── react-performance.csv
│   └── stacks/           # 技术栈数据
│       ├── react-native.csv
│       ├── html-tailwind.csv
│       └── ...
├── dify-tool.yaml     # Dify工具提供者配置
└── dify-tools.yaml     # Dify工具定义
```

### 2. 权限设置

```bash
# Python脚本 - 可执行
chmod 755 deploy-dify/scripts/*.py

# CSV数据文件 - 可读
chmod 644 deploy-dify/data/*.csv

# 配置文件 - 可读
chmod 644 deploy-dify/*.yaml
```

### 3. 测试策略

1. **单元测试**：测试每个工具函数
2. **集成测试**：测试完整工作流
3. **性能测试**：测试大数据量下的性能
4. **错误处理测试**：测试错误场景

### 4. 监控

- 监控工具调用成功率
- 监控响应时间
- 监控错误日志
- 设置告警阈值

---

## 总结

UI/UX Pro Max可以通过两种方式在Dify服务器上部署：

### 方式1: Docker部署（推荐）
- ✅ 生产就绪
- ✅ 功能完整
- ✅ 易于维护
- ✅ 遵循Dify规范

### 方式2: 本地开发部署
- ✅ 开发便捷
- ✅ 调试方便
- ✅ 无需Docker

### 推荐使用方式1

**理由**：
1. ✅ **功能完整**：支持所有核心功能
2. ✅ **Dify原生**：使用Dify的工具节点机制
3. ✅ **易于维护**：遵循Dify的部署规范
4. ✅ **生产就绪**：适合生产环境部署

### 下一步

1. 选择部署方式
2. 按照部署步骤操作
3. 配置工具节点
4. 测试工具功能
5. 开始使用

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
