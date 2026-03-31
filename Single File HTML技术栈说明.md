# UI/UX Pro Max - Single File HTML 技术栈说明

## 📋 目录

1. [概述](#概述)
2. [技术栈配置](#技术栈配置)
3. [使用方法](#使用方法)
4. [最佳实践](#最佳实践)
5. [示例代码](#示例代码)
6. [常见问题](#常见问题)

---

## 概述

UI/UX Pro Max完全支持**Single File HTML**（单文件HTML）技术栈，适用于生成纯HTML + CSS的单文件页面，无需JavaScript框架或构建步骤。

### 什么是Single File HTML？

**Single File HTML**是指：
- ✅ 纯HTML + CSS
- ✅ 使用Tailwind CSS进行样式
- ✅ 不使用JavaScript框架（React、Vue等）
- ✅ 不需要构建步骤
- ✅ 直接在浏览器中打开
- ✅ 适合简单页面（落地页、产品介绍、博客文章）

### 适用场景

| 场景 | 说明 |
|------|------|
| **落地页** | 产品介绍、服务展示、SaaS产品 |
| **营销页** | 营销活动、促销页面、限时优惠 |
| **博客文章** | 技术文章、教程、新闻 |
| **文档页面** | API文档、使用指南、FAQ |
| **个人主页** | 个人作品集、简历、作品展示 |

---

## 技术栈配置

### 当前支持的技术栈

UI/UX Pro Max支持以下技术栈：

| 技术栈 | 说明 | 适用场景 |
|--------|------|----------|
| **html-tailwind** | HTML + Tailwind CSS | ⭐ **推荐用于单文件HTML** |
| react | React | 复杂应用、SPA |
| nextjs | Next.js | SSR、SEO优化 |
| vue | Vue | 渐进式框架 |
| nuxtjs | Nuxt.js | SSR、SEO优化 |
| nuxt-ui | Nuxt UI | Vue组件库 |
| svelte | Svelte | 高性能、编译时优化 |
| astro | Astro | 静态站点、内容站点 |
| swiftui | SwiftUI | iOS应用 |
| react-native | React Native | 跨平台移动应用 |
| flutter | Flutter | 跨平台移动应用 |
| shadcn | shadcn/ui | React组件库 |
| jetpack-compose | Jetpack Compose | Android应用 |

### 推荐使用html-tailwind

对于单文件HTML场景，**强烈推荐使用`html-tailwind`技术栈**，因为：
- ✅ 无需构建步骤
- ✅ 直接在浏览器中运行
- ✅ Tailwind CSS提供完整的样式系统
- ✅ 适合简单页面
- ✅ 性能优秀

---

## 使用方法

### 方法1: 在Dify中指定技术栈

#### 步骤1: 创建应用

1. 登录Dify管理后台
2. 点击"创建应用"
3. 选择"聊天助手（Chatbot）"或"工作流（Workflow）"

#### 步骤2: 配置工作流

在工作流中添加一个LLM节点，用于生成Single File HTML代码：

```yaml
nodes:
  - id: "generate_html"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      你是一个专业的前端开发工程师。使用UI/UX Pro Max工具生成Single File HTML代码。
      
      工作流程:
      1. 分析用户需求
      2. 调用UI/UX Pro Max工具获取设计系统
      3. 根据设计系统生成HTML代码
      4. 确保代码符合最佳实践
      
      技术栈: Single File HTML (html-tailwind)
      
      用户需求: {{#start.text#}}
      
      请生成完整的HTML代码，包括：
      - HTML5语义结构
      - Tailwind CSS样式
      - 响应式设计
      - 无障碍支持
      - SEO优化
      - 性能优化
      
      要求：
      - 所有CSS内联（<style>标签）
      - 不使用外部CSS/JS文件
      - 使用Tailwind CDN
      - 优化图片
      - 确保色彩对比度
```

#### 步骤3: 添加工具节点

在工作流中添加UI/UX Pro Max工具节点：

```yaml
nodes:
  - id: "generate_design_system"
    type: "tool"
    provider: "ui_ux_pro_max"
    tool: "generate_design_system"
    parameters:
      query: "{{#analyze_requirements.output.product_type#}} {{#analyze_requirements.output.style_preference#}}"
      project_name: "{{#analyze_requirements.output.project_name#}}"
      output_format: "markdown"
```

#### 步骤4: 添加HTML生成节点

```yaml
nodes:
  - id: "generate_single_file_html"
    type: "llm"
    model:
      provider: "openai"
      name: "gpt-4"
    prompt: |
      你是一个专业的前端开发工程师。根据以下设计系统生成Single File HTML代码。
      
      ## 设计系统
      {{#generate_design_system.output#}}
      
      ## 技术栈要求
      - Single File HTML (html-tailwind)
      - 所有CSS内联
      - 使用Tailwind CDN
      - 不使用外部文件
      
      请生成完整的HTML代码，包括：
      1. HTML5语义结构
      2. Tailwind CSS样式（内联）
      3. 响应式设计（Tailwind响应式类）
      4. 无障碍支持（WCAG AA/AAA）
      5. SEO优化（meta标签、语义HTML）
      6. 性能优化（懒加载、压缩图片）
      
      要求：
      - 单个HTML文件
      - 所有CSS在<style>标签中
      - 使用Tailwind CDN: <script src="https://cdn.tailwindcss.com"></script>
      - 不使用外部CSS/JS文件
      - 优化图片（lazy loading、WebP格式）
      - 确保色彩对比度（WCAG AA）
```

---

### 方法2: 直接使用Python脚本

#### 步骤1: 生成设计系统

```bash
cd src/ui-ux-pro-max/scripts

python3 search.py "SaaS dashboard" --design-system -p "MyApp" -f markdown
```

#### 步骤2: 生成HTML代码

创建一个Python脚本，根据设计系统生成HTML：

```python
# generate_single_file_html.py

import sys
import json

def generate_html(design_system_file):
    """根据设计系统生成Single File HTML代码"""
    
    # 读取设计系统
    with open(design_system_file, 'r', encoding='utf-8') as f:
        design_system = json.load(f.read())
    
    # 提取设计系统信息
    project_name = design_system.get("project_name", "MyApp")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    
    # 生成HTML代码
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="{project_name} - 专业SaaS仪表盘">
    <meta name="keywords" content="SaaS, dashboard, analytics, {project_name.lower()}">
    
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
            <h1 class="font-heading text-4xl md:text-5xl font-bold mb-6">
                {project_name}
            </h1>
            <p class="font-body text-lg md:text-xl text-text/80 mb-8 max-w-3xl mx-auto">
                {pattern.get('description', '专业的SaaS仪表盘解决方案')}
            </p>
            <button class="bg-cta text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-cta/90 transition-colors duration-200">
                立即开始
            </button>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="py-16 bg-white">
        <div class="container mx-auto px-4">
            <h2 class="font-heading text-3xl font-bold text-center mb-12">
                核心功能
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Feature Cards -->
                <div class="bg-background rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-200">
                    <h3 class="font-heading text-xl font-semibold text-primary mb-3">
                        数据可视化
                    </h3>
                    <p class="font-body text-text/70">
                        实时数据监控和分析
                    </p>
                </div>
                <div class="bg-background rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-200">
                    <h3 class="font-heading text-xl font-semibold text-primary mb-3">
                        用户管理
                    </h3>
                    <p class="font-body text-text/70">
                        完整的用户权限管理
                    </p>
                </div>
                <div class="bg-background rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-200">
                    <h3 class="font-heading text-xl font-semibold text-primary mb-3">
                        报表生成
                    </h3>
                    <p class="font-body text-text/70">
                        自定义报表和导出
                    </p>
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_single_file_html.py <design_system.json>")
        sys.exit(1)
    
    design_system_file = sys.argv[1]
    generate_html(design_system_file)
```

#### 步骤3: 运行脚本

```bash
python3 generate_single_file_html.py design_system.json > index.html
```

---

## 最佳实践

### 1. HTML5语义结构

✅ **使用语义化HTML元素**

```html
<!-- 好的示例 -->
<header>
    <nav>
        <ul>
            <li><a href="#home">首页</a></li>
            <li><a href="#features">功能</a></li>
            <li><a href="#pricing">价格</a></li>
        </ul>
    </nav>
</header>
<main>
    <section id="home">
        <h1>欢迎</h1>
        <p>这是首页内容</p>
    </section>
    <section id="features">
        <h2>功能</h2>
        <article>
            <h3>功能1</h3>
            <p>功能1的详细说明</p>
        </article>
    </section>
    <section id="pricing">
        <h2>价格</h2>
        <table>
            <thead>
                <tr>
                    <th>套餐</th>
                    <th>价格</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>基础版</td>
                    <td>免费</td>
                </tr>
            </tbody>
        </table>
    </section>
</main>
<footer>
    <p>© 2024 版权信息</p>
</footer>

<!-- 不好的示例 -->
<div>
    <div class="header">
        <div class="nav">
            <div class="menu">
                <div class="item"><a href="#">首页</a></div>
                <div class="item"><a href="#">功能</a></div>
            </div>
        </div>
    </div>
    <div class="content">
        <div class="title"><h1>欢迎</h1></div>
        <div class="section"><h2>功能</h2></div>
        <div class="section"><h2>价格</h2></div>
    </div>
    <div class="footer"><p>© 2024</p></div>
</div>
```

### 2. Tailwind CSS内联

✅ **所有CSS在<style>标签中**

```html
<style>
    /* Tailwind CDN */
    @import url('https://cdn.tailwindcss.com') layer(base);
    
    /* Tailwind Config */
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    primary: '#2563EB',
                    secondary: '#3B82F6',
                    cta: '#F97316',
                    background: '#F8FAFC',
                    text: '#1E293B',
                },
                fontFamily: {
                    heading: ['Lora', 'serif'],
                    body: ['Raleway', 'sans-serif'],
                },
            }
        }
    }
    
    /* Custom CSS */
    .custom-class {
        /* 自定义样式 */
    }
</style>
```

### 3. 响应式设计

✅ **使用Tailwind响应式类**

```html
<!-- 容器 -->
<div class="container mx-auto px-4">
    <!-- 网格布局 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- 卡片 -->
        <div class="bg-white rounded-xl p-6 shadow-lg">
            <h3 class="text-xl font-semibold">标题</h3>
            <p class="text-text/70">内容</p>
        </div>
    </div>
</div>

<!-- 响应式图片 -->
<img src="image.jpg" class="w-full h-auto md:w-1/2 lg:w-1/3" alt="描述">

<!-- 响应式文本 -->
<p class="text-sm md:text-base lg:text-lg">响应式文本</p>
```

### 4. 无障碍支持

✅ **确保色彩对比度符合WCAG标准**

```html
<!-- 好的示例：高对比度 -->
<button class="bg-primary text-white px-6 py-3 rounded-lg">
    主按钮
</button>

<!-- 不好的示例：低对比度 -->
<button class="bg-gray-200 text-gray-400 px-6 py-3 rounded-lg">
    按钮
</button>
```

✅ **添加无障碍属性**

```html
<!-- 图片alt属性 -->
<img src="image.jpg" alt="产品截图" class="w-full h-auto">

<!-- 按钮标签 -->
<button aria-label="提交表单" class="bg-primary text-white">
    提交
</button>

<!-- 表单标签 -->
<label for="email" class="sr-only">邮箱地址</label>
<input type="email" id="email" class="border rounded-lg px-4 py-2" required>

<!-- 链接关系 -->
<nav aria-label="主导航">
    <ul>
        <li><a href="#" aria-current="page">首页</a></li>
        <li><a href="#features">功能</a></li>
    </ul>
</nav>
```

### 5. SEO优化

✅ **添加meta标签**

```html
<!-- 基础meta标签 -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>页面标题 - 品牌名称</title>

<!-- SEO meta标签 -->
<meta name="description" content="页面描述（150-160字符）">
<meta name="keywords" content="关键词1, 关键词2, 关键词3">

<!-- Open Graph -->
<meta property="og:title" content="页面标题">
<meta property="og:description" content="页面描述">
<meta property="og:image" content="https://example.com/image.jpg">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="页面标题">
<meta name="twitter:description" content="页面描述">
<meta name="twitter:image" content="https://example.com/image.jpg">

<!-- Canonical URL -->
<link rel="canonical" href="https://example.com/">
```

### 6. 性能优化

✅ **优化图片加载**

```html
<!-- 懒加载 -->
<img src="image.jpg" loading="lazy" class="w-full h-auto" alt="描述">

<!-- 响应式图片 -->
<picture>
    <source srcset="image-small.jpg 1x, image-medium.jpg 2x" media="(max-width: 768px)">
    <source srcset="image-large.jpg 1x" media="(min-width: 769px)">
    <img src="image.jpg" alt="描述" class="w-full h-auto">
</picture>

<!-- WebP格式 -->
<picture>
    <source srcset="image.webp" type="image/webp">
    <img src="image.jpg" alt="描述" class="w-full h-auto">
</picture>
```

✅ **使用Tailwind性能优化**

```html
<style>
    /* 使用@apply减少重复代码 */
    .btn {
        @apply hover:scale-105;
        @apply active:scale-105;
    }
    
    .btn:hover {
        @apply hover:scale-105;
    }
    
    .btn:active {
        @apply active:scale-105;
    }
</style>
```

---

## 示例代码

### 完整的Single File HTML示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serenity Spa - 高端美容SPA</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="Serenity Spa - 专业美容护理服务，让您在宁静的环境中焕发新生">
    <meta name="keywords" content="美容, SPA, 护理, 放松, 健康">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Serenity Spa - 高端美容SPA">
    <meta property="og:description" content="Serenity Spa - 专业美容护理服务，让您在宁静的环境中焕发新生">
    <meta property="og:image" content="https://serenity-spa.com/og-image.jpg">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Tailwind Config */
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#2563EB',
                        secondary: '#3B82F6',
                        cta: '#F97316',
                        background: '#F8FAFC',
                        text: '#1E293B',
                        'soft-pink': '#E8B4B8',
                        'sage-green': '#A8D5BA',
                        'gold': '#D4AF37',
                    },
                    fontFamily: {
                        heading: ['Lora', 'serif'],
                        body: ['Raleway', 'sans-serif'],
                    },
                    boxShadow: {
                        'soft': '0 2px 8px rgba(37, 99, 235, 0.1)',
                        'soft-lg': '0 4px 16px rgba(37, 99, 235, 0.15)',
                    },
                    transitionDuration: {
                        '200': '200ms',
                        '300': '300ms',
                    }
                }
            }
        }
    </style>
</head>
<body class="bg-background text-text">
    <!-- 导航栏 -->
    <nav class="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm shadow-sm z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <span class="font-heading text-2xl font-bold text-primary">Serenity</span>
                    <span class="font-heading text-2xl font-light text-soft-pink ml-1">Spa</span>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="#services" class="text-text hover:text-primary transition-colors duration-200">服务</a>
                    <a href="#about" class="text-text hover:text-primary transition-colors duration-200">关于</a>
                    <a href="#testimonials" class="text-text hover:text-primary transition-colors duration-200">评价</a>
                    <a href="#contact" class="text-text hover:text-primary transition-colors duration-200">联系</a>
                </div>
                <button class="bg-cta text-white px-6 py-2 rounded-lg font-semibold text-lg hover:bg-cta/90 transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    立即预约
                </button>
            </div>
        </div>
    </nav>
    
    <!-- Hero Section -->
    <section class="min-h-screen flex items-center justify-center bg-gradient-to-br from-soft-pink/20 via-background to-sage-green/20 pt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 class="font-heading text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-text mb-6">
                释放内心的宁静
            </h1>
            <p class="font-body text-lg sm:text-xl md:text-2xl text-text/80 mb-8 max-w-3xl mx-auto">
                在Serenity Spa，我们提供顶级的美容护理服务，让您在宁静的环境中焕发新生
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button class="bg-cta text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-cta/90 transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    预约体验
                </button>
                <button class="bg-white text-primary border-2 border-primary px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-50 transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    了解更多
                </button>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section id="services" class="py-16 md:py-24 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="font-heading text-3xl sm:text-4xl font-bold text-text text-center mb-12">
                我们的服务
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- 服务卡片 1 -->
                <div class="card bg-background rounded-xl p-8 shadow-soft hover:shadow-soft-lg transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    <div class="w-16 h-16 bg-soft-pink/20 rounded-full flex items-center justify-center mb-6">
                        <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m6"></path>
                        </svg>
                    </div>
                    <h3 class="font-heading text-xl font-semibold text-text mb-3">面部护理</h3>
                    <p class="font-body text-text/70">深层清洁、保湿、抗衰老护理，让您的肌肤焕发光彩</p>
                </div>
                
                <!-- 服务卡片 2 -->
                <div class="card bg-background rounded-xl p-8 shadow-soft hover:shadow-soft-lg transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    <div class="w-16 h-16 bg-sage-green/20 rounded-full flex items-center justify-center mb-6">
                        <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-.707-.707m2.828 9.9a5 5 0 00-6.364 0z"></path>
                        </svg>
                    </div>
                    <h3 class="font-heading text-xl font-semibold text-text mb-3">身体护理</h3>
                    <p class="font-body text-text/70">全身按摩、身体磨砂、SPA护理，舒缓身心</p>
                </div>
                
                <!-- 服务卡片 3 -->
                <div class="card bg-background rounded-xl p-8 shadow-soft hover:shadow-soft-lg transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    <div class="w-16 h-16 bg-gold/20 rounded-full flex items-center justify-center mb-6">
                        <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                    </div>
                    <h3 class="font-heading text-xl font-semibold text-text mb-3">美容护理</h3>
                    <p class="font-body text-text/70">美甲、美睫、美发，打造完美形象</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="bg-text py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center mb-4 md:mb-0">
                    <span class="font-heading text-xl font-bold text-white">Serenity</span>
                    <span class="font-heading text-xl font-light text-soft-pink ml-1">Spa</span>
                </div>
                <div class="flex space-x-6 mb-4 md:mb-0">
                    <a href="#" class="text-white/80 hover:text-white transition-colors duration-200">隐私政策</a>
                    <a href="#" class="text-white/80 hover:text-white transition-colors duration-200">服务条款</a>
                    <a href="#" class="text-white/80 hover:text-white transition-colors duration-200">联系我们</a>
                </div>
            </div>
            <div class="mt-8 text-center text-white/60 text-sm">
                © 2024 Serenity Spa. All rights reserved.
            </div>
        </div>
    </footer>
</body>
</html>
```

---

## 常见问题

### Q1: Single File HTML支持哪些功能？

**A**: Single File HTML支持：
- ✅ HTML5语义结构
- ✅ Tailwind CSS样式
- ✅ 响应式设计
- ✅ 无障碍支持
- ✅ SEO优化
- ✅ 性能优化
- ✅ 不使用JavaScript框架

### Q2: 如何在Dify中指定Single File HTML技术栈？

**A**: 在工作流的LLM节点提示词中指定：

```
技术栈: Single File HTML (html-tailwind)
```

### Q3: Single File HTML需要构建步骤吗？

**A**: 不需要。Single File HTML：
- ✅ 直接在浏览器中打开
- ✅ 无需npm install
- ✅ 无需构建命令
- ✅ 无需打包工具

### Q4: Single File HTML支持JavaScript吗？

**A**: 支持，但建议：
- ✅ 最小化JavaScript使用
- ✅ 优先使用CSS实现效果
- ✅ 仅在必要时使用JS

### Q5: 如何优化Single File HTML的性能？

**A**: 优化方法：
- ✅ 使用Tailwind CDN的@apply指令
- ✅ 懒加载图片
- ✅ 使用WebP格式
- ✅ 压缩图片
- ✅ 最小化CSS大小
- ✅ 使用响应式图片

---

## 总结

UI/UX Pro Max完全支持**Single File HTML**技术栈，可以生成：

- ✅ 纯HTML + CSS的单文件页面
- ✅ 使用Tailwind CSS进行样式
- ✅ 无需构建步骤
- ✅ 直接在浏览器中打开
- ✅ 适合简单页面（落地页、产品介绍、博客文章）

### 核心优势

1. **无需构建**: 直接在浏览器中运行
2. **快速开发**: 无需配置构建工具
3. **易于部署**: 单个HTML文件即可
4. **性能优秀**: Tailwind CSS优化
5. **SEO友好**: 语义化HTML结构
6. **无障碍支持**: WCAG AA/AAA标准

### 使用场景

- 落地页
- 产品介绍页
- 营销页
- 博客文章
- 文档页面
- 个人主页

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
