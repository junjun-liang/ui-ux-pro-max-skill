#!/bin/bash

# UI/UX Pro Max - Dify快速部署脚本
# 用法: ./deploy-to-dify.sh [docker|local]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
DEPLOY_MODE=${1:-"docker"}

if [ "$DEPLOY_MODE" != "docker" ] && [ "$DEPLOY_MODE" != "local" ]; then
    log_error "Invalid deployment mode. Usage: $0 [docker|local]"
    exit 1
fi

log_info "Deployment mode: $DEPLOY_MODE"

# 检查Python版本
log_info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
log_success "Python version: $PYTHON_VERSION"

# 检查Dify是否运行
if [ "$DEPLOY_MODE" = "docker" ]; then
    log_info "Checking if Dify is running..."
    
    if ! docker ps | grep -q "dify-api"; then
        log_error "Dify API container is not running"
        log_info "Please start Dify first: cd dify/docker && docker compose up -d"
        exit 1
    fi
    
    log_success "Dify is running"
    
    # 获取API容器名称
    API_CONTAINER=$(docker ps --format "{{.Names}}" | grep "dify-api" | head -1)
    log_info "API container: $API_CONTAINER"
fi

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

log_info "Project root: $PROJECT_ROOT"

# 创建目标目录
if [ "$DEPLOY_MODE" = "docker" ]; then
    TARGET_DIR="/app/api/core/tools/provider/builtin/ui_ux_pro_max"
    DATA_DIR="$TARGET_DIR/data"
    
    log_info "Creating target directory in container..."
    docker exec "$API_CONTAINER" mkdir -p "$TARGET_DIR"
    docker exec "$API_CONTAINER" mkdir -p "$DATA_DIR"
else
    TARGET_DIR="$PROJECT_ROOT/dify/api/core/tools/provider/builtin/ui_ux_pro_max"
    DATA_DIR="$TARGET_DIR/data"
    
    log_info "Creating target directory..."
    mkdir -p "$TARGET_DIR"
    mkdir -p "$DATA_DIR"
fi

# 复制工具文件
log_info "Copying tool files..."

if [ "$DEPLOY_MODE" = "docker" ]; then
    docker cp "$SCRIPT_DIR/ui_ux_pro_max.py" "$API_CONTAINER:$TARGET_DIR/"
    docker cp "$SCRIPT_DIR/provider.yaml" "$API_CONTAINER:$TARGET_DIR/"
    docker cp "$SCRIPT_DIR/tools.yaml" "$API_CONTAINER:$TARGET_DIR/"
else
    cp "$SCRIPT_DIR/ui_ux_pro_max.py" "$TARGET_DIR/"
    cp "$SCRIPT_DIR/provider.yaml" "$TARGET_DIR/"
    cp "$SCRIPT_DIR/tools.yaml" "$TARGET_DIR/"
fi

log_success "Tool files copied"

# 复制CSV数据文件
log_info "Copying CSV data files..."

CSV_DIR="$PROJECT_ROOT/src/ui-ux-pro-max/data"

if [ ! -d "$CSV_DIR" ]; then
    log_error "CSV directory not found: $CSV_DIR"
    exit 1
fi

# 复制主CSV文件
for csv_file in products.csv styles.csv colors.csv typography.csv charts.csv landing.csv ux-guidelines.csv ui-reasoning.csv google-fonts.csv icons.csv app-interface.csv react-performance.csv; do
    if [ -f "$CSV_DIR/$csv_file" ]; then
        if [ "$DEPLOY_MODE" = "docker" ]; then
            docker cp "$CSV_DIR/$csv_file" "$API_CONTAINER:$DATA_DIR/"
        else
            cp "$CSV_DIR/$csv_file" "$DATA_DIR/"
        fi
        log_success "Copied: $csv_file"
    else
        log_warning "Not found: $csv_file"
    fi
done

# 复制stacks目录
if [ -d "$CSV_DIR/stacks" ]; then
    log_info "Copying stacks directory..."
    
    if [ "$DEPLOY_MODE" = "docker" ]; then
        docker exec "$API_CONTAINER" mkdir -p "$DATA_DIR/stacks"
        docker cp "$CSV_DIR/stacks/" "$API_CONTAINER:$DATA_DIR/"
    else
        mkdir -p "$DATA_DIR/stacks"
        cp -r "$CSV_DIR/stacks/"* "$DATA_DIR/stacks/"
    fi
    
    log_success "Stacks directory copied"
else
    log_warning "Stacks directory not found"
fi

# 设置文件权限
if [ "$DEPLOY_MODE" = "docker" ]; then
    log_info "Setting file permissions..."
    docker exec "$API_CONTAINER" chmod 644 "$TARGET_DIR"/*.yaml
    docker exec "$API_CONTAINER" chmod 755 "$TARGET_DIR"/*.py
    docker exec "$API_CONTAINER" chmod 644 "$DATA_DIR"/*.csv
    docker exec "$API_CONTAINER" chmod 755 "$DATA_DIR/stacks"/*.csv
    
    log_success "File permissions set"
fi

# 重启API服务
if [ "$DEPLOY_MODE" = "docker" ]; then
    log_info "Restarting API service..."
    docker restart "$API_CONTAINER"
    
    log_info "Waiting for API to be ready..."
    sleep 10
    
    log_success "API service restarted"
fi

# 验证安装
log_info "Verifying installation..."

if [ "$DEPLOY_MODE" = "docker" ]; then
    # 检查文件是否存在
    if docker exec "$API_CONTAINER" test -f "$TARGET_DIR/ui_ux_pro_max.py"; then
        log_success "✓ ui_ux_pro_max.py exists"
    else
        log_error "✗ ui_ux_pro_max.py not found"
    fi
    
    if docker exec "$API_CONTAINER" test -f "$TARGET_DIR/tools.yaml"; then
        log_success "✓ tools.yaml exists"
    else
        log_error "✗ tools.yaml not found"
    fi
    
    if docker exec "$API_CONTAINER" test -f "$DATA_DIR/products.csv"; then
        log_success "✓ products.csv exists"
    else
        log_error "✗ products.csv not found"
    fi
    
    # 测试Python脚本
    log_info "Testing Python script..."
    if docker exec "$API_CONTAINER" python3 -c "import sys; sys.path.insert(0, '$TARGET_DIR'); import ui_ux_pro_max; print('Import successful')"; then
        log_success "✓ Python script imports successfully"
    else
        log_error "✗ Python script import failed"
    fi
else
    # 本地模式验证
    if [ -f "$TARGET_DIR/ui_ux_pro_max.py" ]; then
        log_success "✓ ui_ux_pro_max.py exists"
    else
        log_error "✗ ui_ux_pro_max.py not found"
    fi
    
    if [ -f "$TARGET_DIR/tools.yaml" ]; then
        log_success "✓ tools.yaml exists"
    else
        log_error "✗ tools.yaml not found"
    fi
    
    if [ -f "$DATA_DIR/products.csv" ]; then
        log_success "✓ products.csv exists"
    else
        log_error "✗ products.csv not found"
    fi
    
    # 测试Python脚本
    log_info "Testing Python script..."
    if python3 -c "import sys; sys.path.insert(0, '$TARGET_DIR'); import ui_ux_pro_max; print('Import successful')"; then
        log_success "✓ Python script imports successfully"
    else
        log_error "✗ Python script import failed"
    fi
fi

# 完成
echo ""
log_success "=========================================="
log_success "UI/UX Pro Max deployment complete!"
log_success "=========================================="
echo ""
log_info "Next steps:"
log_info "1. Open Dify dashboard: http://localhost"
log_info "2. Create or edit an application"
log_info "3. Add 'UI/UX Pro Max' tool to your workflow"
log_info "4. Start using the tool!"
echo ""
log_info "For more information, see: Dify集成指南.md"
echo ""
