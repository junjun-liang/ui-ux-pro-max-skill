# UI/UX Pro Max - LangChain Agent

## 📋 项目概述

本项目直接在ui-ux-pro-max-skill项目中使用LangChain框架创建智能UI/UX设计助手。

### 功能特性

- ✅ **智能代理**：自动选择和调用UI/UX Pro Max工具
- ✅ **3个核心工具**：生成设计系统、搜索域、搜索技术栈指南
- ✅ **记忆管理**：保存对话历史，支持上下文感知
- ✅ **错误处理**：优雅处理工具调用错误
- ✅ **交互式对话**：支持多轮对话

---

## 🚀 快速开始

### 步骤1: 安装依赖

```bash
# 进入项目目录
cd /home/meizu/Documents/my_agent_project/ui-ux-pro-max-skill

# 安装Poetry（如果未安装）
curl -sSL https://install.python-poetry.org | python3 -

# 添加Poetry到PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证安装
poetry --version
```

### 步骤2: 安装项目依赖

```bash
# 安装依赖
poetry install

# 激活虚拟环境
source $(poetry env info --path)/bin/activate
```

### 步骤3: 配置环境变量

创建`.env`文件：

```env
# OpenAI API密钥
OPENAI_API_KEY=sk-your-api-key-here

# 可选：其他API密钥
# ANTHROPIC_API_KEY=your-anthropic-key
# COHERE_API_KEY=your-cohere-key
```

### 步骤4: 运行Agent

```bash
# 使用Poetry运行
poetry run python agent.py

# 或激活虚拟环境后运行
source $(poetry env info --path)/bin/activate
python agent.py
```

---

## 🎯 使用示例

### 示例1: 生成设计系统

**用户输入**:
```
帮我生成一个SaaS仪表盘的设计系统
```

**Agent行为**:
1. 分析需求 → 产品类型: SaaS
2. 调用 `ui_ux_pro_max_generate_design_system`
3. 返回完整的设计系统

**输出**:
```markdown
## Design System: SaaS Dashboard

### Pattern
- **Name:** Hero + Features + CTA
- **Conversion Focus:** Trust-driven with clear value prop
- **CTA Placement:** Above fold

### Style
- **Name:** Glassmorphism
- **Type:** General
- **Keywords:** Glassmorphism, soft shadows, blur, translucent
- **Best For:** Modern dashboards, SaaS platforms

### Colors
| Role | Hex |
|------|-----|
| Primary | #2563EB |
| Secondary | #3B82F6 |
| CTA | #F97316 |
| Background | #F8FAFC |
| Text | #1E293B |

### Typography
- **Heading:** Inter
- **Body:** Inter
- **Mood:** Professional, clean, modern

### Key Effects
Soft shadows + Blur effects + Smooth transitions (200-250ms)

### Avoid (Anti-patterns)
- Excessive animation
- Dark mode by default
- Low contrast colors
```

---

### 示例2: 搜索UI风格

**用户输入**:
```
推荐一些适合美容SPA的UI风格
```

**Agent行为**:
1. 分析需求 → 产品类型: Beauty/Spa Service
2. 调用 `ui_ux_pro_max_search_domain`
3. 域: style
4. 返回风格推荐

**输出**:
```markdown
## UI Pro Max Search Results

**Domain:** style | **Query:** beauty spa wellness | **Found:** 3 results

### Result 1
- **Style Category:** Soft UI Evolution
- **Type:** General
- **Keywords:** Evolved soft UI, better contrast, modern aesthetics
- **Best For:** Modern enterprise apps, SaaS platforms, health/wellness
- **Performance:** ⚡ Excellent
- **Accessibility:** ✓ WCAG AA

### Result 2
- **Style Category:** Minimalism & Swiss Style
- **Type:** General
- **Keywords:** Clean, simple, spacious, functional
- **Best For:** Enterprise apps, dashboards
- **Performance:** ⚡ Excellent
- **Accessibility:** ✓ WCAG AAA

### Result 3
- **Style Category:** Neumorphism
- **Type:** General
- **Keywords:** Soft shadows, depth, tactile, organic
- **Best For:** Wellness, beauty, lifestyle brands
- **Performance:** Good
- **Accessibility:** ✓ WCAG AA
```

---

### 示例3: 搜索技术栈指南

**用户输入**:
```
React Native表单验证的最佳实践是什么？
```

**Agent行为**:
1. 分析需求 → 技术栈: React Native
2. 主题: 表单验证
3. 调用 `ui_ux_pro_max_search_stack_guidelines`
4. 返回最佳实践

**输出**:
```markdown
## UI Pro Max Stack Guidelines

**Stack:** react-native | **Query:** form validation | **Found:** 3 results

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

### Result 3
- **Category:** Validation
- **Guideline:** Implement proper validation
- **Description:** Validate form inputs properly
- **Do:** Use validation libraries like Formik, React Hook Form
- **Don't:** Manual validation without libraries
- **Code Good:** `const schema = Yup.object().shape({...})`
- **Code Bad:** Manual if/else validation
- **Severity:** High
- **Docs URL:** https://reactnative.dev/docs/forms
```

---

## 🛠️ 项目结构

```
ui-ux-pro-max-skill/
├── pyproject.toml              # Poetry配置文件
├── agent.py                   # LangChain Agent主文件
├── src/ui-ux-pro-max/         # UI/UX Pro Max源代码
│   ├── scripts/               # Python脚本
│   │   ├── search.py          # 搜索函数
│   │   ├── design_system.py    # 设计系统生成器
│   │   └── core.py            # BM25搜索引擎核心
│   └── data/                 # CSV数据库
│       ├── products.csv        # 161种产品类型
│       ├── styles.csv         # 67种UI风格
│       ├── colors.csv         # 161种配色方案
│       ├── typography.csv     # 57种字体配对
│       ├── charts.csv         # 25种图表类型
│       ├── landing.csv        # 24种落地页模式
│       ├── ux-guidelines.csv  # 99条UX指南
│       ├── ui-reasoning.csv   # 161条推理规则
│       └── stacks/           # 技术栈指南
│           ├── react-native.csv
│           └── html-tailwind.csv
└── .env.example               # 环境变量示例
```

---

## 🎨 核心工具

### 1. GenerateDesignSystemTool

**功能**: 生成完整的设计系统推荐

**参数**:
- `query`: 搜索查询（必需）
- `project_name`: 项目名称（可选）
- `output_format`: 输出格式（markdown或json）

**输出**: 完整的设计系统，包括模式、风格、颜色、字体、效果和反模式

---

### 2. SearchDomainTool

**功能**: 搜索特定的UI/UX域

**参数**:
- `query`: 搜索查询（必需）
- `domain`: 搜索域（可选，自动检测）
- `max_results`: 最大结果数（默认3）
- `output_format`: 输出格式（markdown或json）

**可用域**:
- `style`: UI风格
- `color`: 配色方案
- `typography`: 字体配对
- `chart`: 图表类型
- `landing`: 落地页模式
- `product`: 产品类型
- `ux`: UX指南
- `google-fonts`: Google字体
- `icons`: 图标库
- `react`: React性能
- `web`: 应用界面指南

---

### 3. SearchStackGuidelinesTool

**功能**: 搜索技术栈特定的指南和最佳实践

**参数**:
- `query`: 搜索查询（必需）
- `stack`: 技术栈（必需）
- `max_results`: 最大结果数（默认3）
- `output_format`: 输出格式（markdown或json）

**可用技术栈**:
- `html-tailwind`: HTML + Tailwind CSS
- `react`: React
- `nextjs`: Next.js
- `vue`: Vue
- `nuxtjs`: Nuxt.js
- `nuxt-ui`: Nuxt UI
- `svelte`: Svelte
- `astro`: Astro
- `swiftui`: SwiftUI
- `react-native`: React Native
- `flutter`: Flutter
- `shadcn`: shadcn/ui
- `jetpack-compose`: Jetpack Compose

---

## 🧪 高级用法

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

## 🐛 故障排除

### 问题1: Poetry命令未找到

**解决方案**:
```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 添加到PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证安装
poetry --version
```

### 问题2: 依赖安装失败

**解决方案**:
```bash
# 清除Poetry缓存
poetry cache clear pypi --all

# 重新安装依赖
poetry install --no-cache
```

### 问题3: UI/UX Pro Max函数导入错误

**解决方案**:
```python
# 检查Python路径
import sys
print(sys.path)

# 检查UI/UX Pro Max项目路径
from pathlib import Path
project_path = Path(__file__).parent / "src" / "ui-ux-pro-max"
print(project_path)
```

### 问题4: Agent无法调用工具

**解决方案**:
```python
# 启用详细日志
agent = initialize_agent(
    tools=UI_UX_PRO_MAX_TOOLS,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,  # 启用详细日志
    handle_parsing_errors=True,
    max_iterations=5
)
```

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
    max_execution_time=60,  # 设置最大执行时间
)
```

---

## 📚 相关文档

- **[Poetry环境配置指南.md](./Poetry环境配置指南.md)** - Poetry安装和配置
- **[LangChain集成指南.md](./LangChain集成指南.md)** - LangChain集成详细说明
- **[数据文件参数说明文档.md](./数据文件参数说明文档.md)** - 数据文件参数说明
- **[软件设计架构文档.md](./软件设计架构文档.md)** - 项目架构说明

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**项目版本**: 0.1.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
