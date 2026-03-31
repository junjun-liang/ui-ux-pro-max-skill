"""
UI/UX Pro Max - 独立API服务
为Dify提供HTTP API接口，无需在Dify服务器上部署
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import sys
import json
from pathlib import Path

# ============ CONFIGURATION ============
# API配置
API_HOST = "0.0.0.0"
API_PORT = 8000

# 数据目录
DATA_DIR = Path(__file__).parent / "src" / "ui-ux-pro-max" / "data"

# ============ DATA MODELS ============
class DesignSystemRequest(BaseModel):
    """设计系统生成请求"""
    query: str
    project_name: Optional[str] = None
    output_format: str = "markdown"

class SearchDomainRequest(BaseModel):
    """域搜索请求"""
    query: str
    domain: Optional[str] = None
    max_results: int = 3
    output_format: str = "markdown"

class SearchStackGuidelinesRequest(BaseModel):
    """技术栈指南搜索请求"""
    query: str
    stack: str
    max_results: int = 3
    output_format: str = "markdown"

class GenerateSingleFileHTMLRequest(BaseModel):
    """单文件HTML生成请求"""
    design_system_file: str
    project_name: Optional[str] = None

# ============ RESPONSE MODELS ============
class DesignSystemResponse(BaseModel):
    """设计系统响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class SearchResponse(BaseModel):
    """搜索响应"""
    success: bool
    domain: Optional[str] = None
    query: Optional[str] = None
    count: int = 0
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class GenerateHTMLResponse(BaseModel):
    """HTML生成响应"""
    success: bool
    html: Optional[str] = None
    error: Optional[str] = None

# ============ FASTAPI APP ============
app = FastAPI(title="UI/UX Pro Max API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ API ENDPOINTS ============
@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径 - API信息"""
    return {
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

@app.post("/generate-design-system", response_model=DesignSystemResponse)
async def generate_design_system(request: DesignSystemRequest):
    """生成设计系统"""
    try:
        # 导入搜索函数
        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
        from search import generate_design_system as gen_design
        
        # 生成设计系统
        result = gen_design(request.query, request.project_name, request.output_format)
        
        return DesignSystemResponse(success=True, data=result)
    except Exception as e:
        return DesignSystemResponse(success=False, error=str(e))

@app.post("/search-domain", response_model=SearchResponse)
async def search_domain(request: SearchDomainRequest):
    """搜索域"""
    try:
        # 导入搜索函数
        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
        from search import search as search_func
        
        # 搜索域
        result = search_func(request.query, request.domain, request.max_results, request.output_format)
        
        return SearchResponse(
            success=True,
            domain=request.domain or "auto",
            query=request.query,
            count=result.get("count", 0),
            results=result.get("results", []),
            error=None
        )
    except Exception as e:
        return SearchResponse(success=False, error=str(e))

@app.post("/search-stack-guidelines", response_model=SearchResponse)
async def search_stack_guidelines(request: SearchStackGuidelinesRequest):
    """搜索技术栈指南"""
    try:
        # 导入搜索函数
        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))
        from search import search_stack_guidelines as search_stack_func
        
        # 搜索技术栈指南
        result = search_stack_func(request.query, request.stack, request.max_results, request.output_format)
        
        return SearchResponse(
            success=True,
            domain=request.stack,
            query=request.query,
            count=result.get("count", 0),
            results=result.get("results", []),
            error=None
        )
    except Exception as e:
        return SearchResponse(success=False, error=str(e))

@app.post("/generate-single-file-html", response_model=GenerateHTMLResponse)
async def generate_single_file_html(request: GenerateSingleFileHTMLRequest):
    """生成单文件HTML"""
    try:
        # 读取设计系统文件
        design_system_file = Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "data" / request.design_system_file
        
        if not design_system_file.exists():
            return GenerateHTMLResponse(success=False, error=f"Design system file not found: {request.design_system_file}")
        
        with open(design_system_file, 'r', encoding='utf-8') as f:
            design_system = json.load(f.read())
        
        # 提取设计系统信息
        project_name = design_system.get("project_name", request.project_name or "MyApp")
        pattern = design_system.get("pattern", {})
        style = design_system.get("style", {})
        colors = design_system.get("colors", {})
        typography = design_system.get("typography", {})
        
        # 生成HTML代码
        html = generate_html_from_design_system(project_name, pattern, style, colors, typography)
        
        return GenerateHTMLResponse(success=True, html=html)
    except Exception as e:
        return GenerateHTMLResponse(success=False, error=str(e))

def generate_html_from_design_system(project_name: str, pattern: dict, style: dict, colors: dict, typography: dict) -> str:
    """根据设计系统生成单文件HTML代码"""
    
    # 提取设计系统信息
    primary_color = colors.get('primary', '#2563EB')
    secondary_color = colors.get('secondary', '#3B82F6')
    cta_color = colors.get('cta', '#F97316')
    background_color = colors.get('background', '#F8FAFC')
    text_color = colors.get('text', '#1E293B')
    
    heading_font = typography.get('heading', 'Inter')
    body_font = typography.get('body', 'Inter')
    google_fonts_url = typography.get('google_fonts_url', '')
    
    # 生成HTML
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
    {f'<link href="{google_fonts_url}" rel="stylesheet">' if google_fonts_url else ''}
    
    <style>
        /* Tailwind Config */
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '{primary_color}',
                        secondary: '{secondary_color}',
                        cta: '{cta_color}',
                        background: '{background_color}',
                        text: '{text_color}',
                    }},
                    fontFamily: {{
                        heading: ['{heading_font}', 'serif'],
                        body: ['{body_font}', 'sans-serif'],
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
    return html

# ============ RUN SERVER ============
if __name__ == "__main__":
    print("Starting UI/UX Pro Max API Server...")
    print(f"API will be available at http://{API_HOST}:{API_PORT}")
    print(f"API docs will be available at http://{API_HOST}:{API_PORT}/docs")
    
    # 运行服务器
    uvicorn.run(app, host=API_HOST, port=API_PORT)
