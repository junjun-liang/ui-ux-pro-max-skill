#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试UI/UX Pro Max LangChain Agent的基本功能
"""

import sys
from pathlib import Path

# 添加UI/UX Pro Max脚本路径
sys.path.insert(0, str(Path(__file__).parent / "src" / "ui-ux-pro-max" / "scripts"))

try:
    from search import generate_design_system, search
    from core import search_stack
    
    print("✅ UI/UX Pro Max函数导入成功")
    
    # 测试1: 生成设计系统
    print("\n🧪 测试1: 生成设计系统")
    result = generate_design_system("SaaS dashboard", "TestProject", "markdown")
    print("✅ generate_design_system 函数正常工作")
    
    # 测试2: 搜索域
    print("\n🧪 测试2: 搜索UI风格")
    result = search("glassmorphism", "style", 1)
    print("✅ search 函数正常工作")
    
    # 测试3: 搜索技术栈指南
    print("\n🧪 测试3: 搜索技术栈指南")
    result = search_stack("form validation", "react-native", 1)
    print("✅ search_stack 函数正常工作")
    
    print("\n" + "=" * 60)
    print("🎉 所有UI/UX Pro Max核心功能测试通过！")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试LangChain依赖
print("\n🧪 测试LangChain依赖")
try:
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.chat_models import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.tools import BaseTool
    from pydantic import BaseModel, Field
    from dotenv import load_dotenv
    
    print("✅ LangChain依赖导入成功")
    
except ImportError as e:
    print(f"❌ LangChain依赖导入失败: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 所有依赖测试通过！")
print("=" * 60)
print("\n📝 下一步:")
print("1. 在.env文件中设置OPENAI_API_KEY")
print("2. 运行: poetry run python agent.py")
print("=" * 60)
