#!/bin/bash
# 启动后端服务脚本

cd "$(dirname "$0")/../backend"

echo "正在启动后端服务..."

# 检查虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "⚠ 虚拟环境不存在，请先运行: python -m venv venv"
fi

# 检查依赖
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠ 依赖未安装，正在安装..."
    pip install -r requirements.txt
fi

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠ .env 文件不存在，从模板复制..."
    cp .env.example .env
    echo "请编辑 .env 文件配置参数"
fi

# 启动服务
echo "启动 FastAPI 服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
