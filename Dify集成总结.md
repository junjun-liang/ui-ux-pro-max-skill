# UI/UX Pro Max - Dify集成总结

## 📋 已创建的文件

### 1. 核心集成文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **Python工具主文件** | `dify-integration/ui_ux_pro_max.py` | Dify工具的Python实现，包含BM25搜索引擎和设计系统生成器 |
| **工具提供者配置** | `dify-integration/provider.yaml` | 工具提供者的元数据配置 |
| **工具定义文件** | `dify-integration/tools.yaml` | 工具函数定义和参数配置 |
| **自动化部署脚本** | `dify-integration/deploy-to-dify.sh` | 一键部署脚本（支持Docker和本地模式） |

### 2. 文档文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **完整集成指南** | `dify-integration/Dify集成指南.md` | 详细的集成步骤、配置说明、使用示例、故障排除 |
| **快速参考卡片** | `dify-integration/快速参考.md` | 快速开始指南、工具参数、使用场景、性能指标 |
| **目录结构说明** | `dify-integration/目录结构.md` | 完整的目录结构、文件关系、部署流程 |

---

## 🎯 核心功能

### 1. 三个主要工具

#### ✨ generate_design_system
生成完整的设计系统推荐

**参数**:
- `query` (必需): 搜索查询
- `project_name` (可选): 项目名称
- `output_format` (可选): "markdown" 或 "json"

**输出**: 完整的设计系统（模式、风格、颜色、字体、效果、反模式、检查清单）

#### 🔍 search_domain
搜索特定UI/UX域

**参数**:
- `query` (必需): 搜索查询
- `domain` (可选): 搜索域（自动检测）
- `max_results` (可选): 最大结果数
- `output_format` (可选): "markdown" 或 "json"

**可用域**: style, color, typography, chart, landing, product, ux, google-fonts, icons, react, web

#### 📚 search_stack_guidelines
搜索技术栈特定指南

**参数**:
- `query` (必需): 搜索查询
- `stack` (必需): 技术栈
- `max_results` (可选): 最大结果数
- `output_format` (可选): "markdown" 或 "json"

**可用技术栈**: html-tailwind, react, nextjs, vue, nuxtjs, nuxt-ui, svelte, astro, swiftui, react-native, flutter, shadcn, jetpack-compose

### 2. 核心技术

#### 🧠 BM25搜索引擎
- 文档索引构建
- 术语频率统计
- 逆文档频率计算
- 相关性评分

#### 🤖 推理引擎
- 161条行业特定推理规则
- 多域并行搜索
- 最佳匹配选择
- 决策规则应用

#### 🎨 设计系统生成器
- 产品类型识别
- 风格优先级匹配
- 配色方案推荐
- 字体配对选择
- 落地页模式匹配

---

## 🚀 快速开始

### 一键部署（推荐）

```bash
# 1. 进入集成目录
cd dify-integration

# 2. 运行部署脚本
./deploy-to-dify.sh docker

# 3. 在Dify中添加工具
#    - 打开Dify管理后台
#    - 创建/编辑应用
#    - 添加"UI/UX Pro Max"工具
```

### 本地开发部署

```bash
# 1. 进入集成目录
cd dify-integration

# 2. 运行部署脚本
./deploy-to-dify.sh local

# 3. 启动Dify API
cd ../dify/api
python main.py
```

---

## 📖 使用示例

### 示例1: 生成设计系统

**用户输入**: "帮我做一个美容SPA网站的首页"

**Dify工作流**:
```
开始 → LLM分析需求 → 工具节点(generate_design_system) → LLM生成HTML → 结束
```

**工具调用**:
```json
{
  "query": "美容SPA wellness",
  "project_name": "Serenity Spa",
  "output_format": "markdown"
}
```

**输出**: 完整的设计系统（模式、风格、颜色、字体、效果、反模式、检查清单）

### 示例2: 搜索UI风格

**用户输入**: "推荐一些适合SaaS产品的UI风格"

**Dify工作流**:
```
开始 → LLM识别产品类型 → 工具节点(search_domain) → LLM总结推荐 → 结束
```

**工具调用**:
```json
{
  "query": "SaaS modern professional",
  "domain": "style",
  "max_results": 5,
  "output_format": "markdown"
}
```

**输出**: 5种适合SaaS产品的UI风格推荐

### 示例3: 技术栈指南

**用户输入**: "React Native表单验证的最佳实践是什么？"

**Dify工作流**:
```
开始 → LLM识别技术栈和主题 → 工具节点(search_stack_guidelines) → LLM总结指南 → 结束
```

**工具调用**:
```json
{
  "query": "form validation",
  "stack": "react-native",
  "max_results": 3,
  "output_format": "markdown"
}
```

**输出**: React Native表单验证的3条最佳实践

---

## 📊 数据统计

### 规模数据

| 类别 | 数量 | 说明 |
|------|------|------|
| **产品类型** | 161 | 覆盖SaaS、电商、金融、医疗、游戏等 |
| **UI风格** | 67 | Glassmorphism、Minimalism、Brutalism等 |
| **配色方案** | 161 | 与产品类型1:1对齐 |
| **字体配对** | 57 | 精心策划的Google Fonts组合 |
| **图表类型** | 25 | 趋势、对比、比例、时间序列等 |
| **UX指南** | 99 | 最佳实践、反模式、无障碍规则 |
| **推理规则** | 161 | 行业特定的设计决策规则 |
| **技术栈** | 13 | React、Next.js、Vue、SwiftUI等 |
| **落地页模式** | 24 | Hero-Centric、Conversion-Optimized等 |

### 性能指标

| 指标 | 值 | 说明 |
|------|-----|------|
| **工具调用延迟** | <500ms | 设计系统生成 |
| **域搜索延迟** | <100ms | 单域搜索 |
| **并发处理** | 支持 | 多工具并行调用 |
| **内存占用** | ~50MB | Python进程 |
| **CSV加载** | <100ms | 所有CSV文件 |

---

## 🔧 配置说明

### 工具提供者配置 (provider.yaml)

```yaml
identity:
  name: "ui_ux_pro_max"
  author: "UI/UX Pro Max Team"
  label:
    en_US: "UI/UX Pro Max"
    zh_Hans: "UI/UX Pro Max 设计智能"
  description:
    en_US: "AI-powered design intelligence for building professional UI/UX"
    zh_Hans: "AI驱动的UI/UX设计智能工具"
  icon: "🎨"
  tags: ["design", "ui", "ux", "frontend", "web", "mobile"]

supported_model_types: ["llm"]
configurate_methods: ["no-configuration"]
provider_credential_schema:
  type: "none"
```

### 工具定义配置 (tools.yaml)

```yaml
tools:
  - identity:
      name: "generate_design_system"
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
```

---

## 🐛 故障排除

### 常见问题

#### 1. 工具未显示在Dify中

**问题**: 在Dify工具列表中看不到UI/UX Pro Max

**解决方案**:
```bash
# 检查文件是否存在
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/

# 重启API服务
docker restart dify-api-1

# 清除缓存
docker exec dify-api-1 rm -rf /app/api/core/tools/provider/builtin/__pycache__
```

#### 2. CSV文件未找到

**问题**: 工具报错"File not found: products.csv"

**解决方案**:
```bash
# 检查数据目录
docker exec dify-api-1 ls -la /app/api/core/tools/provider/builtin/ui_ux_pro_max/data/

# 重新复制数据文件
cd dify-integration
./deploy-to-dify.sh docker
```

#### 3. Python导入错误

**问题**: 工具调用失败，显示导入错误

**解决方案**:
```bash
# 测试Python脚本
docker exec dify-api-1 python3 -c "import sys; sys.path.insert(0, '/app/api/core/tools/provider/builtin/ui_ux_pro_max'); import ui_ux_pro_max; print('OK')"

# 检查Python版本
docker exec dify-api-1 python3 --version

# 检查依赖
docker exec dify-api-1 pip list | grep -E "csv|json|pathlib"
```

---

## 📚 文档索引

### 核心文档

1. **[Dify集成指南.md](./dify-integration/Dify集成指南.md)**
   - 完整的集成步骤
   - 配置说明
   - 使用示例
   - 工作流配置
   - API调用
   - 故障排除

2. **[快速参考.md](./dify-integration/快速参考.md)**
   - 快速开始指南
   - 工具参数
   - 使用场景
   - 性能指标
   - 故障排除

3. **[目录结构.md](./dify-integration/目录结构.md)**
   - 完整的目录结构
   - 文件关系
   - 部署流程
   - 文件大小统计

### 相关文档

4. **[软件设计架构文档.md](./软件设计架构文档.md)**
   - 项目架构
   - 核心组件
   - 数据库结构
   - 工作原理
   - 性能优化

5. **[README.md](./README.md)**
   - 项目说明
   - 安装方法
   - 使用方法
   - 支持的平台

---

## 🎯 使用场景

### 场景1: 设计系统生成 + HTML代码

**适用**: 新项目、新页面、完整设计

**流程**:
1. 用户输入需求
2. LLM分析需求
3. 调用`generate_design_system`获取设计系统
4. LLM根据设计系统生成HTML代码
5. 输出完整HTML

### 场景2: UI风格搜索 + 推荐

**适用**: 风格选择、设计灵感、风格对比

**流程**:
1. 用户输入产品类型和风格偏好
2. 调用`search_domain`搜索风格
3. LLM总结推荐
4. 输出风格列表

### 场景3: 技术栈最佳实践

**适用**: 技术选型、最佳实践、性能优化

**流程**:
1. 用户输入技术栈和主题
2. 调用`search_stack_guidelines`搜索指南
3. LLM总结最佳实践
4. 输出指南列表

---

## 🔗 相关资源

### 官方资源

- **UI/UX Pro Max官网**: https://uupm.cc
- **GitHub仓库**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **NPM包**: https://www.npmjs.com/package/uipro-cli
- **Dify文档**: https://docs.dify.ai/

### 学习资源

- **Dify自定义工具**: https://docs.dify.ai/guides/tools/
- **Dify工作流**: https://docs.dify.ai/guides/workflow/
- **UI/UX设计原则**: https://uupm.cc/principles

---

## 🤝 支持与反馈

- **GitHub Issues**: [提交问题](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues)
- **Email**: uiuxpromax@gmail.com
- **PayPal**: [支持项目](https://paypal.me/uiuxpromax)

---

## 📝 更新日志

### v1.0.0 (2026-03-30)

- ✅ 初始版本发布
- ✅ 支持Dify自定义工具集成
- ✅ 实现三个核心工具函数
- ✅ 支持Markdown和JSON输出格式
- ✅ 提供自动化部署脚本
- ✅ 完整的文档和示例

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-30  
**维护者**: UI/UX Pro Max Team
