"""
UI/UX Pro Max - LangChain Agent (LangChain 1.2+)
直接在ui-ux-pro-max-skill项目中使用LangChain框架创建智能UI/UX设计助手
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import sys
import os
from pathlib import Path

# 导入UI/UX Pro Max函数
sys.path.insert(0, str(Path(__file__).parent / "src" / "ui-ux-pro-max" / "scripts"))
from search import generate_design_system, search
from core import search_stack


@tool
def generate_design_system_tool(query: str, project_name: str = "MyApp", output_format: str = "markdown") -> str:
    """生成完整的设计系统推荐，包括模式、风格、颜色、字体、效果和反模式。
    
    输入示例：
    - query: "SaaS dashboard"
    - project_name: "MyApp"
    - output_format: "markdown"
    """
    print("invoke generate design system tool")
    result = generate_design_system(query, project_name, output_format)
    print(result)
    return result


@tool
def search_domain_tool(query: str, domain: str = None, max_results: int = 3) -> str:
    """搜索特定的UI/UX域，包括风格、颜色、字体、图表、落地页、UX指南等。
    
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
    """
    print("invoke search domain tool")
    result = search(query, domain, max_results)
    print(result)
    return result


@tool
def search_stack_guidelines_tool(query: str, stack: str, max_results: int = 3, output_format: str = "markdown") -> str:
    """搜索技术栈特定的指南和最佳实践。
    
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
    print("invoke search stack guidelines tool")
    result = search_stack(query, stack, max_results)
    print(result)
    return result


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 检查API密钥
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("错误: OPENAI_API_KEY环境变量未设置")
        print("请在.env文件中设置OPENAI_API_KEY")
        print("示例: OPENAI_API_KEY=sk-...")
        return
    
    # 创建LLM
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        api_key="sk-9471c8ab90c64ec8a16c8f8fb63e029f",
        temperature=0.7,
    )
    
    # 创建系统提示
    system_prompt = """你是一个专业的UI/UX设计助手。你可以使用以下工具来帮助用户：
    
    可用工具：
    - generate_design_system_tool: 生成完整的设计系统
    - search_domain_tool: 搜索特定的UI/UX域
    - search_stack_guidelines_tool: 搜索技术栈指南
    
    工作流程：
    1. 分析用户需求
    2. 如果需要设计系统，调用generate_design_system_tool
    3. 如果需要搜索特定域，调用search_domain_tool
    4. 如果需要技术栈指南，调用search_stack_guidelines_tool
    5. 根据工具结果提供设计建议
    
    请根据用户需求智能选择和调用工具。"""
    
    # 创建代理
    agent = create_agent(
        model=llm,
        tools=[generate_design_system_tool, search_domain_tool, search_stack_guidelines_tool],
        system_prompt=system_prompt
    )
    
    # 运行代理
    print("=" * 60)
    print("UI/UX Pro Max - LangChain Agent")
    print("=" * 60)
    print()
    print("🎨 UI/UX Pro Max - 智能设计助手")
    print()
    print("📋 可用工具:")
    print("  1. generate_design_system_tool - 生成设计系统")
    print("  2. search_domain_tool - 搜索UI/UX域")
    print("  3. search_stack_guidelines_tool - 搜索技术栈指南")
    print()
    print("💡 使用提示:")
    print("  - '帮我生成一个SaaS仪表盘的设计系统'")
    print("  - '推荐一些适合美容SPA的UI风格'")
    print("  - 'React Native表单验证的最佳实践是什么？'")
    print()
    print("⌨ 输入'exit'退出")
    print()
    
    while True:
        user_input = input("用户: ")
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print()
            print("👋 再见！")
            print()
            break
        
        try:
            response = agent.invoke({"messages": [("user", user_input)]})
            print()
            print(f"🤖 代理: {response['messages'][-1].content}")
            print()
        except Exception as e:
            print()
            print(f"❌ 错误: {str(e)}")
            print()


if __name__ == "__main__":
    main()
